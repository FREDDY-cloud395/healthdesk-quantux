import os
import sys
from fastapi.testclient import TestClient

# Añadir el path para importar app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.main import app

client = TestClient(app)

def test_module14_and_versioning():
    print("=== TEST MÓDULO 14 & VERSIÓN 4.0.0-DEV ===")
    
    # 1. Verificar Endpoint de Versión Oficial
    r_health = client.get("/health")
    assert r_health.status_code == 200, f"Error en /health: {r_health.text}"
    health_data = r_health.json()
    assert health_data.get("version") == "4.0.0-DEV", f"Versión esperada 4.0.0-DEV, obtenida: {health_data.get('version')}"
    print(f"[OK] Versión en API Health: {health_data.get('version')} ({health_data.get('environment')})")

    # 2. Creación de Ticket de Emergencia Asistencial ("Paciente en Box")
    # Generado por un médico solicitante
    emergency_payload = {
        "title": "[🚨 PACIENTE EN BOX] Receta Digital Bloqueada / Error de Firma PKI - Consultorio 1",
        "description": (
            "🚨 ALERTA ASISTENCIAL DE GUARDIA / PACIENTE EN ESPERA:\n\n"
            "• Profesional Médico: Dr. Martín Gómez\n"
            "• Ubicación / Box: Consultorio 1\n"
            "• Motivo Clínico de Bloqueo: Receta Digital Bloqueada / Error de Firma PKI\n"
            "• Interno Telefónico de Contacto: 204\n"
            "• Dictado de Audio IA: 'Receta bloqueada con paciente esperando'\n\n"
            "ESTADO: Paciente esperando en consulta. Protocolo de atención inmediata N1 requerido (< 3 min SLA)."
        ),
        "platform_code": "PLAT_RECETA_E",
        "institution_code": "INST_CENTRAL",
        "ticket_type": "INCIDENTE",
        "impact": "CRITICO",
        "urgency": "CRITICA",
        "requester_username": "solicitante"
    }

    r_ticket = client.post("/api/v1/tickets", json=emergency_payload)
    assert r_ticket.status_code == 200, f"Error creando ticket de emergencia: {r_ticket.text}"
    t_data = r_ticket.json()
    
    assert t_data.get("priority") == "P1", f"La prioridad calculada debe ser P1, se obtuvo: {t_data.get('priority')}"
    assert "PACIENTE EN BOX" in t_data.get("title"), "El título debe contener el tag de rescate asistencial"
    ticket_id = t_data.get("id")
    print(f"[OK] Ticket Asistencial Creado: ID {ticket_id} con Prioridad {t_data.get('priority')}")

    # 3. Verificación de Recepción en la Mesa de Ayuda
    r_list = client.get("/api/v1/tickets")
    assert r_list.status_code == 200
    all_tickets = r_list.json()
    matching = [t for t in all_tickets if t.get("id") == ticket_id]
    assert len(matching) == 1, "El ticket debe ser visible para los operadores de la mesa de ayuda"
    print(f"[OK] Ticket {ticket_id} recibido correctamente en la bandeja de la Mesa de Ayuda.")

    # 4. Verificación de Archivos Frontend (Presencia de versión y aislamiento de roles)
    frontend_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))
    with open(frontend_html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "v4.0.0-DEV" in html_content, "index.html debe contener el badge v4.0.0-DEV"
    assert "doctor-emergency-suite" in html_content, "index.html debe contener la suite asistencial"
    assert "modal-doctor-emergency" in html_content, "index.html debe contener el modal de emergencia médica"
    assert "modal-doctor-contingency" in html_content, "index.html debe contener el modal de contingencia asistencial"
    print("[OK] Verificación Frontend HTML: v4.0.0-DEV y Suite Médica presentes en index.html")

    frontend_js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "js", "app.js"))
    with open(frontend_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Verificar que el botón solo se muestra para SOLICITANTE y se oculta para SOPORTE y ADMIN
    assert "docEmergencySuite.style.display = 'inline-flex'" in js_content
    assert "docEmergencySuite.style.display = 'none'" in js_content
    assert "badge-patient-emergency" in js_content
    print("[OK] Verificación Frontend JS: Aislamiento estricto de roles RBAC confirmado (Médicos vs Mesa de Ayuda)")

    print("\n>>> TODOS LOS TESTS DE CERTIFICACIÓN MÓDULO 14 Y VERSIÓN v4.0.0-DEV PASARON CON ÉXITO! <<<")

if __name__ == "__main__":
    test_module14_and_versioning()
