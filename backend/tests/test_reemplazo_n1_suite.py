import unittest
import json
import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlmodel import Session, select
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import engine
from app.models.entities import Ticket, TicketStatus, PriorityLevel, ImpactLevel, UrgencyLevel, User, UserRole, TicketAuditLog, TicketComment
from app.core.fsm import validate_status_transition, is_sla_paused_status, calculate_priority

def new_test_id():
    return f"TEST-{uuid.uuid4().hex[:8].upper()}"

def make_test_ticket(**kwargs):
    defaults = {
        "id": new_test_id(),
        "platform_code": "CONSULTORIO_DIGITAL",
        "institution_code": "OSDE",
        "requester_username": "solicitante",
        "requester_name": "Dr. Usuario Test",
        "status": TicketStatus.NUEVO,
    }
    defaults.update(kwargs)
    return Ticket(**defaults)

class TestReemplazoN1Suite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_fsm_7_states_and_sla_pause(self):
        """Valida las transiciones del ciclo de vida ITIL 4 (7 estados) y la pausa de SLA en esperas externas."""
        # Estados válidos de la FSM
        self.assertTrue(validate_status_transition(TicketStatus.NUEVO, TicketStatus.ASIGNADO))
        self.assertTrue(validate_status_transition(TicketStatus.ASIGNADO, TicketStatus.EN_CURSO))
        self.assertTrue(validate_status_transition(TicketStatus.EN_CURSO, TicketStatus.ESPERANDO_AL_PRESTADOR))
        self.assertTrue(validate_status_transition(TicketStatus.EN_CURSO, TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA))
        self.assertTrue(validate_status_transition(TicketStatus.ESPERANDO_AL_PRESTADOR, TicketStatus.EN_CURSO))
        self.assertTrue(validate_status_transition(TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA, TicketStatus.EN_CURSO))
        self.assertTrue(validate_status_transition(TicketStatus.EN_CURSO, TicketStatus.RESUELTO))
        self.assertTrue(validate_status_transition(TicketStatus.RESUELTO, TicketStatus.CERRADO))
        
        # Pausa de SLA
        self.assertTrue(is_sla_paused_status(TicketStatus.ESPERANDO_AL_PRESTADOR))
        self.assertTrue(is_sla_paused_status(TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA))
        self.assertFalse(is_sla_paused_status(TicketStatus.EN_CURSO))
        self.assertFalse(is_sla_paused_status(TicketStatus.ASIGNADO))

        t = make_test_ticket(
            title="Prueba FSM 7 Estados",
            description="Verificando ciclo ITIL y pausas SLA"
        )
        t_id = t.id
        with Session(engine) as session:
            session.add(t)
            session.commit()

        # Mover a ASIGNADO
        r = self.client.post(f"/api/v1/tickets/{t_id}/status", json={"new_status": "ASIGNADO", "changed_by_username": "soporte"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ASIGNADO")
        self.assertFalse(r.json()["sla_paused"])

        # Mover a EN_CURSO
        r = self.client.post(f"/api/v1/tickets/{t_id}/status", json={"new_status": "EN_CURSO", "changed_by_username": "soporte"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "EN_CURSO")
        self.assertFalse(r.json()["sla_paused"])

        # Mover a ESPERANDO_AL_PRESTADOR -> SLA Pausado
        r = self.client.post(f"/api/v1/tickets/{t_id}/status", json={"new_status": "ESPERANDO_AL_PRESTADOR", "changed_by_username": "soporte"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ESPERANDO_AL_PRESTADOR")
        self.assertTrue(r.json()["sla_paused"])

        # Retornar a EN_CURSO -> SLA Activo
        r = self.client.post(f"/api/v1/tickets/{t_id}/status", json={"new_status": "EN_CURSO", "changed_by_username": "soporte"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "EN_CURSO")
        self.assertFalse(r.json()["sla_paused"])

        # Mover a EN_ESPERA_PASARELA_OSDE_SISA -> SLA Pausado
        r = self.client.post(f"/api/v1/tickets/{t_id}/status", json={"new_status": "EN_ESPERA_PASARELA_OSDE_SISA", "changed_by_username": "soporte"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "EN_ESPERA_PASARELA_OSDE_SISA")
        self.assertTrue(r.json()["sla_paused"])
        print("[OK] TEST-01: Ciclo ITIL 4 de 7 estados y pausas SLA validados con exito.")

    def test_02_balancer_protects_in_progress_tickets(self):
        """Valida que el balanceador inteligente SOLO redistribuya tickets ASIGNADOS y NUNCA toque tickets EN_CURSO."""
        t_in_progress = make_test_ticket(
            title="Ticket Activo En Curso",
            description="El analista esta trabajando activamente",
            status=TicketStatus.EN_CURSO,
            assignee_username="cpaez"
        )
        t_assigned_1 = make_test_ticket(
            title="Ticket Asignado 1",
            description="En espera de atencion inicial",
            status=TicketStatus.ASIGNADO,
            assignee_username="cpaez"
        )
        t_assigned_2 = make_test_ticket(
            title="Ticket Asignado 2",
            description="En espera de atencion inicial",
            status=TicketStatus.ASIGNADO,
            assignee_username="cpaez"
        )
        prog_id = t_in_progress.id

        with Session(engine) as session:
            session.add(t_in_progress)
            session.add(t_assigned_1)
            session.add(t_assigned_2)
            session.commit()

        # Ejecutar rebalanceo tactico entre cpaez y dnavarro
        payload = {
            "analyst_usernames": ["cpaez", "dnavarro"],
            "strategy": "even",
            "team_leader_username": "cdaneri"
        }
        res = self.client.post("/api/v1/team-leader/custom-rebalance", json=payload)
        self.assertEqual(res.status_code, 200)

        # Verificar en base de datos: el ticket EN_CURSO sigue intacto en cpaez
        with Session(engine) as session:
            check_prog = session.get(Ticket, prog_id)
            self.assertEqual(check_prog.assignee_username, "cpaez")
            self.assertEqual(check_prog.status, TicketStatus.EN_CURSO)
        print("[OK] TEST-02: Balanceador de carga respeta y blinda taxativamente tickets EN_CURSO.")

    def test_03_kcs_closure_json_schema(self):
        """Valida el cierre estructurado bajo estandar KCS v6 / ITIL 4 KEDB."""
        t = make_test_ticket(
            title="Error Token OTP Consultorio Digital",
            description="Prestador bloqueado en firma electronica",
            status=TicketStatus.EN_CURSO,
            assignee_username="cpaez"
        )
        t_id = t.id
        with Session(engine) as session:
            session.add(t)
            session.commit()

        kcs_body = {
            "cierre_ticket_metadata": {
                "version_metodologia": "KCS_v6",
                "tipo_resolucion": "DEFINITIVA",
                "tiempo_dedicado_minutos": 12,
                "resuelto_por": "cpaez",
                "nivel_soporte": "N1"
            },
            "clasificacion_itil": {
                "nivel_1_macro": "SISTEMAS_ASISTENCIALES",
                "nivel_2_sistema": "CONSULTORIO_DIGITAL_OSDE",
                "nivel_3_componente": "MODULO_RECETA_ELECTRONICA",
                "nivel_4_sintoma_falla": "BLOQUEO_FIRMA_DIGITAL_OTP"
            },
            "diagnostico_causa_raiz": {
                "categoria_origen": "DESINCRONIZACION_PASARELA_REPOSITORIO",
                "descripcion_rca": "Desalineacion temporal entre reloj local de app movil y pasarela OSDE.",
                "codigo_error_sistema": "ERR_VAL_OTP_TIMEOUT",
                "recurrencia_conocida": True
            },
            "procedimiento_resolutivo_secuencial": [
                "Paso 1: Sincronizar reloj de dispositivo prestador con hora NTP de red.",
                "Paso 2: Limpiar cache de sesion en portal de Consultorio Digital.",
                "Paso 3: Regenerar token OTP y validar emision exitosa de receta."
            ],
            "articulo_kcs_candidato": {
                "propuesto_para_kb": True,
                "titulo_articulo": "Solucion a Desincronizacion OTP en Consultorio Digital",
                "resumen_solucion": "Se forzo la sincronizacion de reloj NTP en el dispositivo prestador y se reemitio token OTP con exito.",
                "visibilidad": "INTERNO_SOPORTE"
            }
        }

        res = self.client.post(f"/api/v1/tickets/{t_id}/kcs-close", json=kcs_body)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["ticket"]["status"], "RESUELTO")
        self.assertIsNotNone(data["ticket"]["kcs_data"])
        
        parsed_kcs = json.loads(data["ticket"]["kcs_data"])
        self.assertEqual(parsed_kcs["clasificacion_itil"]["nivel_2_sistema"], "CONSULTORIO_DIGITAL_OSDE")
        self.assertEqual(parsed_kcs["diagnostico_causa_raiz"]["codigo_error_sistema"], "ERR_VAL_OTP_TIMEOUT")
        self.assertEqual(len(parsed_kcs["procedimiento_resolutivo_secuencial"]), 3)
        print("[OK] TEST-03: Cierre KCS v6 estructurado validado y persistido con exito.")

    def test_04_csat_mandatory_justification_and_leader_rescue(self):
        """Valida que calificaciones de 1 o 2 estrellas exijan justificacion obligatoria y el protocolo de rescate del Lider."""
        t = make_test_ticket(
            title="Ticket para Calificacion Negativa",
            description="El prestador quedo desconforme",
            status=TicketStatus.RESUELTO,
            resolution_notes="Solucion tecnica brindada"
        )
        t_id = t.id
        with Session(engine) as session:
            session.add(t)
            session.commit()

        # Intento de calificar con 1 estrella SIN justificacion -> Debe fallar con HTTP 422
        bad_req = {
            "closed_by_username": "solicitante",
            "rating_stars": 1,
            "rating_feedback": ""  # Vacio
        }
        res_fail = self.client.post(f"/api/v1/tickets/{t_id}/close", json=bad_req)
        self.assertEqual(res_fail.status_code, 422)
        self.assertIn("Para calificaciones de 1 o 2 estrellas es obligatorio", res_fail.json()["detail"])

        # Calificar con 2 estrellas CON justificacion -> Debe tener exito y marcar requires_service_recovery = True
        ok_req = {
            "closed_by_username": "solicitante",
            "rating_stars": 2,
            "rating_feedback": "Demoraron demasiado en darme una respuesta y tuve que reprogramar turnos."
        }
        res_ok = self.client.post(f"/api/v1/tickets/{t_id}/close", json=ok_req)
        self.assertEqual(res_ok.status_code, 200)
        t_closed = res_ok.json()
        self.assertEqual(t_closed["status"], "CERRADO")
        self.assertEqual(t_closed["rating_stars"], 2)
        self.assertTrue(t_closed["requires_service_recovery"])

        # Protocolo de Rescate ejecutado por el Lider de Soporte
        rescue_payload = {
            "rescue_notes": "Me comunique telefonicamente con la Dra. Valenzuela, le explique la causa de la demora y acordamos un canal prioritario de atencion. Conformidad recuperada.",
            "team_leader_username": "cdaneri",
            "rescue_status": "RESCATADO_CON_CONFORMIDAD"
        }
        res_rescue = self.client.post(f"/api/v1/tickets/{t_id}/rescue", json=rescue_payload)
        self.assertEqual(res_rescue.status_code, 200)
        
        # Verificar que el ticket quedo desmarcado de alerta y con el informe del lider
        with Session(engine) as session:
            t_after = session.get(Ticket, t_id)
            self.assertFalse(t_after.requires_service_recovery)
            self.assertEqual(t_after.rescue_leader_username, "cdaneri")
            self.assertEqual(t_after.rescue_status, "RESCATADO_CON_CONFORMIDAD")
            self.assertIn("Conformidad recuperada", t_after.rescue_notes)

            # Verificar que se creo el comentario visible en el historial
            comments = session.exec(select(TicketComment).where(TicketComment.ticket_id == t_id)).all()
            has_rescue_comment = any("[INFORME DE RESCATE CSAT DEL LÍDER DE SOPORTE]" in c.message for c in comments)
            self.assertTrue(has_rescue_comment)

        print("[OK] TEST-04: Exigencia de justificacion CSAT y protocolo de rescate con informe inmutable validados.")

    def test_05_major_incident_mim_parent_child_linking(self):
        """Valida el cartel discreto MIM, vinculacion desde el hijo al padre y trazabilidad bidireccional."""
        t_parent = make_test_ticket(
            title="Caida Pasarela de Pagos y Autorizaciones OSDE",
            description="Incidente critico mayor que afecta a todos los prestadores",
            is_major_incident=True,
            status=TicketStatus.EN_CURSO,
            assignee_username="dnavarro",
            requester_username="admin"
        )
        t_child = make_test_ticket(
            title="Error al autorizar consulta ambulatoria",
            description="No responde el validador en linea",
            status=TicketStatus.EN_CURSO,
            assignee_username="cpaez",
            requester_username="solicitante"
        )
        parent_id = t_parent.id
        child_id = t_child.id

        with Session(engine) as session:
            session.add(t_parent)
            session.add(t_child)
            session.commit()

        # Vincular ticket hijo al ticket padre mediante endpoint /link-parent
        link_res = self.client.post(f"/api/v1/tickets/{child_id}/link-parent", json={
            "parent_ticket_id": parent_id,
            "linked_by_username": "cpaez"
        })
        self.assertEqual(link_res.status_code, 200)

        # Consultar detalle del Padre -> debe contener child_id en linked_child_ticket_ids
        parent_detail = self.client.get(f"/api/v1/tickets/{parent_id}").json()
        self.assertIn(child_id, parent_detail["linked_child_ticket_ids"])

        # Consultar detalle del Hijo -> debe tener parent_ticket_id referenciando al Padre
        child_detail = self.client.get(f"/api/v1/tickets/{child_id}").json()
        self.assertEqual(child_detail["ticket"]["parent_ticket_id"], parent_id)

        # Resolver el ticket Padre -> debe propagar en cascada la resolucion al ticket Hijo
        res_resolve = self.client.post(f"/api/v1/tickets/{parent_id}/resolve", json={
            "resolution_notes": "Servicio de pasarela OSDE restablecido tras reinicio de cluster de microservicios.",
            "resolved_by_username": "dnavarro",
            "is_workaround": False
        })
        self.assertEqual(res_resolve.status_code, 200)

        # Verificar que el hijo tambien quedo en RESUELTO
        with Session(engine) as session:
            child_check = session.get(Ticket, child_id)
            self.assertEqual(child_check.status, TicketStatus.RESUELTO)
            self.assertIn(parent_id, child_check.resolution_notes)

        print("[OK] TEST-05: Cartel MIM, relacion Padre-Hijo y resolucion en cascada validados exitosamente.")

if __name__ == "__main__":
    unittest.main()
