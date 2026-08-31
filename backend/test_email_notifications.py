"""
Suite de Pruebas Unitarias y de Integración para UH-35 (Servicio de Emails y Notificaciones FSM)
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.db.session import engine, init_db
from app.models.entities import Ticket, EmailNotificationLog

client = TestClient(app)

def test_full_email_notification_lifecycle():
    init_db()
    
    # 1. Crear un Ticket P1 Crítico
    payload_create = {
        "title": "Falla total en servicio de Recetas Digitales de Servicio en Producción",
        "description": "Profesionales de la Salud de servicio en producción informan bloqueo general al firmar recetas electrónicas.",
        "platform_code": "CAT_RECETA",
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "CRITICO",
        "urgency": "CRITICA",
        "requester_username": "solicitante"
    }
    
    res = client.post("/api/v1/tickets", json=payload_create)
    assert res.status_code == 200, res.text
    ticket_data = res.json()
    ticket_id = ticket_data["id"]
    assert ticket_data["priority"] == "P1"
    print(f"✅ Ticket Creado con ID: {ticket_id} (Prioridad P1)")

    # 2. Verificar que se dispararon los emails de Creación y Alerta Roja P1
    with Session(engine) as session:
        logs = session.exec(select(EmailNotificationLog).where(EmailNotificationLog.ticket_id == ticket_id)).all()
        event_types = [l.event_type for l in logs]
        print(f"📧 Emails generados en Creación: {event_types}")
        assert "TICKET_CREATED" in event_types
        assert "P1_ALERT" in event_types

    # 3. Asignar Responsable N2
    payload_assign = {
        "assignee_username": "soporte",
        "support_level": "N2",
        "reason": "Derivado a N2 para análisis de certificados de firma digital",
        "changed_by_username": "soporte"
    }
    res = client.post(f"/api/v1/tickets/{ticket_id}/assign", json=payload_assign)
    assert res.status_code == 200, res.text
    print(f"✅ Ticket Asignado a Soporte N2")

    # 4. Transicionar a EN_CURSO
    payload_status = {
        "new_status": "EN_CURSO",
        "reason": "Iniciando reinicio de microservicio de tokens",
        "changed_by_username": "soporte"
    }
    res = client.post(f"/api/v1/tickets/{ticket_id}/status", json=payload_status)
    assert res.status_code == 200, res.text
    print(f"✅ Ticket en Estado EN_CURSO")

    # 5. Resolver con Workaround
    payload_resolve = {
        "resolution_notes": "Se realizó failover a servidor secundario y se reanudó la emisión.",
        "is_workaround": True,
        "resolved_by_username": "soporte"
    }
    res = client.post(f"/api/v1/tickets/{ticket_id}/resolve", json=payload_resolve)
    assert res.status_code == 200, res.text
    print(f"✅ Ticket Resuelto con Guardrail y Workaround")

    # 6. Cerrar Ticket con Conformidad
    payload_close = {
        "feedback": "Verificado por profesional de la salud de servicio en producción, emisión funcionando correctamente.",
        "closed_by_username": "solicitante"
    }
    res = client.post(f"/api/v1/tickets/{ticket_id}/close", json=payload_close)
    assert res.status_code == 200, res.text
    print(f"✅ Ticket Cerrado Definitivamente")

    # 7. Validar todos los logs en el endpoint de notificaciones
    res_notif = client.get(f"/api/v1/tickets/{ticket_id}/notifications")
    assert res_notif.status_code == 200
    all_notifs = res_notif.json()
    print(f"📊 Total notificaciones registradas para el ticket: {len(all_notifs)}")
    
    all_event_types = [n["event_type"] for n in all_notifs]
    print(f"📋 Cadena completa de eventos notificados: {all_event_types}")
    
    assert "TICKET_CREATED" in all_event_types
    assert "P1_ALERT" in all_event_types
    assert "TICKET_ASSIGNED" in all_event_types
    assert "STATUS_CHANGED" in all_event_types
    assert "TICKET_RESOLVED" in all_event_types
    assert "TICKET_CLOSED" in all_event_types
    
    # Verificar que el HTML contiene la marca Quantux
    for n in all_notifs:
        assert "HEALTHDESK" in n["body_html"]
        assert "QUANTUX" in n["body_html"]
        assert n["sent_status"].startswith("SENT")

    print("\n🎉 TODAS LAS PRUEBAS DE NOTIFICACIONES POR EMAIL (UH-35) PASARON EXITOSAMENTE (100%).\n")

if __name__ == "__main__":
    test_full_email_notification_lifecycle()
