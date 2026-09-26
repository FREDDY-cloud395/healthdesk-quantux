"""
Test Suite: Bot Gestor de Tickets Multi-Rol y Enriquecimiento de Base de Conocimiento (KCS v6)
Implementado con unittest para ejecución nativa en cualquier entorno Python.

Verifica:
1. Interacción activa del bot con todos los roles y sectores (Mesa de Ayuda, Solicitante, Especialistas N2/N3, Pasarelas).
2. Registro estricto de comentarios con autor, rol y sector en cada transición.
3. Evaluación de negocio al resolver: discriminación entre conocimiento transferible (asociación a KB) y rutinas administrativas (sin asociación).
4. Consulta desde Base de Conocimiento recuperando los tickets específicos que sumaron información al resolverse.
5. Endpoints REST de bot y KB.
"""

import sys
import os
import unittest
from datetime import datetime

# Asegurar path de backend en sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.db.session import engine, init_db
from app.models.entities import (
    Ticket, TicketStatus, TicketType, PriorityLevel, ImpactLevel, UrgencyLevel,
    TicketComment, KBArticle, KBArticleContribution
)
from app.services.ticket_manager_bot import TicketManagerBot

class TestTicketManagerBotAndKB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_01_business_kb_qualification_rules(self):
        """Valida que la regla de negocio discrimine correctamente incidencias técnicas de rutinas."""
        # Incidencia técnica en Receta Digital -> Debe calificar para KB
        tech_ticket = Ticket(
            id="TICK-TEST-QUAL-01",
            title="Falla de validación biométrica en endpoint SISA",
            description="Error de conectividad y timeout recurrente al validar receta electrónica.",
            platform_code="CAT_RECETA",
            institution_code="ALEMAN",
            ticket_type=TicketType.INCIDENTE,
            impact=ImpactLevel.ALTO,
            urgency=UrgencyLevel.ALTA,
            priority=PriorityLevel.P1,
            status=TicketStatus.NUEVO,
            requester_username="solicitante"
        )
        qualifies, matcher = TicketManagerBot.evaluate_business_kb_qualification(tech_ticket)
        self.assertTrue(qualifies)
        self.assertIsNotNone(matcher)
        self.assertEqual(matcher["category"], "Receta Digital")

        # Requerimiento administrativo trivial -> NO debe calificar para KB
        admin_ticket = Ticket(
            id="TICK-TEST-QUAL-02",
            title="Solicitud de olvido de contraseña y reseteo simple",
            description="Olvido de contraseña por vacaciones. Solicita blanqueo habitual.",
            platform_code="CAT_PORTAL",
            institution_code="OSDE",
            ticket_type=TicketType.REQUERIMIENTO,
            impact=ImpactLevel.BAJO,
            urgency=UrgencyLevel.BAJA,
            priority=PriorityLevel.P4,
            status=TicketStatus.NUEVO,
            requester_username="solicitante"
        )
        qualifies_admin, matcher_admin = TicketManagerBot.evaluate_business_kb_qualification(admin_ticket)
        self.assertFalse(qualifies_admin)
        self.assertIsNone(matcher_admin)

    def test_02_multi_role_dialogue_and_kb_association(self):
        """Valida el ciclo de vida completo de un ticket técnico interactuando con roles y asociando a KB."""
        with Session(engine) as session:
            t_id = f"TICK-BOT-UNIT-{int(datetime.utcnow().timestamp())}"
            test_ticket = Ticket(
                id=t_id,
                title="Error 504 en pasarela al validar recetas de guardia",
                description="Las terminales no pueden confirmar recetas por caída en pasarela externa.",
                platform_code="CAT_RECETA",
                institution_code="ITALIANO",
                ticket_type=TicketType.INCIDENTE,
                impact=ImpactLevel.CRITICO,
                urgency=UrgencyLevel.CRITICA,
                priority=PriorityLevel.P1,
                status=TicketStatus.NUEVO,
                requester_username="dr_lopez"
            )
            session.add(test_ticket)
            session.commit()

            # Paso 1: NUEVO -> ASIGNADO
            res1 = TicketManagerBot.process_ticket_step(session, test_ticket)
            self.assertEqual(res1["previous_status"], "NUEVO")
            self.assertEqual(res1["new_status"], "ASIGNADO")
            self.assertIsNotNone(test_ticket.assignee_username)

            # Paso 2: ASIGNADO -> EN_CURSO (Diálogo Solicitante y Soporte N1)
            res2 = TicketManagerBot.process_ticket_step(session, test_ticket)
            self.assertEqual(res2["previous_status"], "ASIGNADO")
            self.assertEqual(res2["new_status"], "EN_CURSO")

            # Paso 3: EN_CURSO -> EN_CURSO (Intervención Especialista N2 y Pasarela Externa)
            res3 = TicketManagerBot.process_ticket_step(session, test_ticket)
            self.assertEqual(res3["previous_status"], "EN_CURSO")

            # Paso 4: EN_CURSO -> RESUELTO (Evaluación de Negocio y aporte a KB)
            res4 = TicketManagerBot.process_ticket_step(session, test_ticket)
            self.assertEqual(res4["new_status"], "RESUELTO")
            self.assertTrue(res4["associated_to_kb"])
            self.assertTrue(test_ticket.contributed_to_kb)
            self.assertIsNotNone(test_ticket.associated_kb_id)

            # Verificar que se crearon los comentarios con autor, rol y sector
            comments = session.exec(
                select(TicketComment).where(TicketComment.ticket_id == t_id)
            ).all()
            self.assertGreaterEqual(len(comments), 4)

            roles = [c.author_role for c in comments if c.author_role]
            sectors = [c.author_sector for c in comments if c.author_sector]
            self.assertIn("SOPORTE_N1", roles)
            self.assertIn("SOLICITANTE", roles)
            self.assertIn("ESPECIALISTA_N2", roles)
            self.assertGreaterEqual(len(sectors), 3)

            # Paso 5: RESUELTO -> CERRADO (Conformidad asistencial CSAT 5/5)
            res5 = TicketManagerBot.process_ticket_step(session, test_ticket)
            self.assertEqual(res5["new_status"], "CERRADO")
            self.assertEqual(test_ticket.rating_stars, 5)

            # Verificar registro formal en KBArticleContribution
            contrib = session.exec(
                select(KBArticleContribution).where(KBArticleContribution.ticket_id == t_id)
            ).first()
            self.assertIsNotNone(contrib)
            self.assertEqual(contrib.article_id, test_ticket.associated_kb_id)
            self.assertEqual(contrib.contributor_role, "ESPECIALISTA_N2")

    def test_03_kb_query_shows_contributing_tickets(self):
        """Valida que al consultar la Base de Conocimiento se expongan los tickets que sumaron información."""
        with Session(engine) as session:
            contrib = session.exec(select(KBArticleContribution)).first()
            self.assertIsNotNone(contrib, "Debe existir al menos un aporte a KB registrado")
            target_art_id = contrib.article_id
            contributing_tkt_id = contrib.ticket_id

        # 1. Consultar el artículo por ID
        res = self.client.get(f"/api/v1/articles/{target_art_id}")
        self.assertEqual(res.status_code, 200)
        art_data = res.json()
        self.assertIn("contributing_tickets", art_data)
        self.assertGreaterEqual(art_data["contributing_tickets_count"], 1)
        tkt_ids = [t["ticket_id"] for t in art_data["contributing_tickets"]]
        self.assertIn(contributing_tkt_id, tkt_ids)

        # 2. Consultar endpoint dedicado de tickets contribuyentes
        res_contribs = self.client.get(f"/api/v1/articles/{target_art_id}/contributing-tickets")
        self.assertEqual(res_contribs.status_code, 200)
        contrib_list = res_contribs.json()
        self.assertIsInstance(contrib_list, list)
        self.assertGreaterEqual(len(contrib_list), 1)
        first_c = contrib_list[0]
        self.assertIn("ticket_id", first_c)
        self.assertIn("contributor_role", first_c)
        self.assertIn("contributor_sector", first_c)
        self.assertIn("contribution_summary", first_c)

        # 3. Consultar listado general de artículos enriquecidos
        res_list = self.client.get("/api/v1/articles")
        self.assertEqual(res_list.status_code, 200)
        all_arts = res_list.json()
        matched_art = next((a for a in all_arts if a["id"] == target_art_id), None)
        self.assertIsNotNone(matched_art)
        self.assertGreaterEqual(matched_art["contributing_tickets_count"], 1)

    def test_04_tickets_api_bot_endpoints(self):
        """Valida los endpoints REST del bot: advance-cycle, advance-to-resolution, kb-contribution."""
        # 1. POST /api/v1/tickets/bot/advance-cycle
        res_cycle = self.client.post("/api/v1/tickets/bot/advance-cycle?count=2")
        self.assertEqual(res_cycle.status_code, 200)
        cycle_data = res_cycle.json()
        self.assertEqual(cycle_data["status"], "success")
        self.assertIn("processed_count", cycle_data)

        # 2. Crear ticket nuevo para probar advance-to-resolution
        with Session(engine) as session:
            now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            t_id = f"TICK-API-UNIT-{now_str}"
            t = Ticket(
                id=t_id,
                title="Inconsistencia de vademécum en dispensación ambulatoria",
                description="Medicamento bloqueado por discrepancia de cobertura nacional.",
                platform_code="CAT_RECETA",
                institution_code="OSDE",
                ticket_type=TicketType.INCIDENTE,
                impact=ImpactLevel.ALTO,
                urgency=UrgencyLevel.ALTA,
                priority=PriorityLevel.P2,
                status=TicketStatus.NUEVO,
                requester_username="solicitante"
            )
            session.add(t)
            session.commit()

        # 3. POST /api/v1/tickets/{ticket_id}/bot/advance-to-resolution
        res_adv = self.client.post(f"/api/v1/tickets/{t_id}/bot/advance-to-resolution")
        self.assertEqual(res_adv.status_code, 200)
        adv_data = res_adv.json()
        self.assertEqual(adv_data["status"], "success")
        self.assertIn(adv_data["final_status"], ("RESUELTO", "CERRADO"))
        self.assertTrue(adv_data["associated_to_kb"])

        # 4. GET /api/v1/tickets/{ticket_id}/kb-contribution
        res_ticket_contrib = self.client.get(f"/api/v1/tickets/{t_id}/kb-contribution")
        self.assertEqual(res_ticket_contrib.status_code, 200)
        tc_data = res_ticket_contrib.json()
        self.assertTrue(tc_data["contributed_to_kb"])
        self.assertEqual(tc_data["ticket_id"], t_id)
        self.assertIn("article_id", tc_data)
        self.assertIn("contributor_role", tc_data)
        self.assertIn("contributor_sector", tc_data)


if __name__ == "__main__":
    unittest.main()
