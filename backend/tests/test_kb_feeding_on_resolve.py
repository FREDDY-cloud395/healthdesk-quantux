import unittest
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlmodel import Session, select
from fastapi import BackgroundTasks
from app.db.session import engine
from app.models.entities import Ticket, TicketStatus, KBArticle, KBArticleContribution, TicketAuditLog, TicketComment
from app.api.endpoints.tickets import resolve_ticket, TicketResolveRequest

class TestKBFeedingOnResolve(unittest.TestCase):
    def setUp(self):
        self.session = Session(engine)
        self.test_ticket = Ticket(
            id="TEST-KB-FEED-" + datetime.utcnow().strftime("%H%M%S"),
            title="Prueba de alimentacion KB en resolucion",
            description="Falla recurrente al autenticar en receta electronica",
            institution_code="OSDE",
            platform_code="CAT_RECETA",
            requester_username="solicitante",
            status=TicketStatus.EN_CURSO,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(self.test_ticket)
        self.session.commit()

    def tearDown(self):
        # Limpieza
        self.session.rollback()
        self.session.close()

    def test_resolve_ticket_feeds_kb_properly(self):
        req = TicketResolveRequest(
            resolution_notes="Se renovo certificado TLS del servicio de prescripcion y se reiniciaron los workers.",
            is_workaround=False,
            resolved_by_username="admin",
            root_cause="Expiracion de certificado TLS en pasarela intermedia",
            publish_to_kb=True
        )
        bg = BackgroundTasks()
        res = resolve_ticket(self.test_ticket.id, req, bg, self.session)

        self.assertEqual(res.status, TicketStatus.RESUELTO)
        self.assertTrue(res.contributed_to_kb)
        self.assertIsNotNone(res.associated_kb_id)

        # Verificar artículo creado
        art = self.session.get(KBArticle, res.associated_kb_id)
        self.assertIsNotNone(art)
        self.assertEqual(art.category, "Receta Digital")
        self.assertIn("Expiracion de certificado TLS", art.content)
        self.assertEqual(art.source_ticket_id, self.test_ticket.id)

        # Verificar contribución en KBArticleContribution
        contrib = self.session.exec(
            select(KBArticleContribution).where(
                KBArticleContribution.article_id == art.id,
                KBArticleContribution.ticket_id == self.test_ticket.id
            )
        ).first()
        self.assertIsNotNone(contrib)
        self.assertEqual(contrib.contributor_username, "admin")

        # Verificar comentarios y logs
        comment = self.session.exec(
            select(TicketComment).where(TicketComment.ticket_id == self.test_ticket.id)
        ).first()
        self.assertIsNotNone(comment)
        self.assertIn("Base de Conocimiento Actualizada", comment.message)

if __name__ == "__main__":
    unittest.main()
