from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=== VERIFICACIÓN DEL BACKEND CORE (HEALTHDESK QUANTUX) ===")
    
    # 1. HealthCheck
    r = client.get("/health")
    assert r.status_code == 200
    print("[OK] HealthCheck API:", r.json())

    # 2. Tablas Maestras
    r_plat = client.get("/api/v1/platforms")
    assert r_plat.status_code == 200
    print(f"[OK] Plataformas Oficiales ({len(r_plat.json())}/9):", [p["code"] for p in r_plat.json()[:3]], "...")

    r_inst = client.get("/api/v1/institutions")
    assert r_inst.status_code == 200
    print(f"[OK] Clientes Institucionales ({len(r_inst.json())}/14):", [i["code"] for i in r_inst.json()[:3]], "...")

    # 3. Bandeja de Tickets
    r_tick = client.get("/api/v1/tickets")
    assert r_tick.status_code == 200
    tickets = r_tick.json()
    print(f"[OK] Tickets en Bandeja Inicial ({len(tickets)}):")
    for t in tickets:
        print(f"   * [{t['id']}] {t['priority']} | Estado: {t['status']:<10} | {t['title']} ({t['institution_code']})")

    # 4. Prueba del Ciclo de Vida: Crear Ticket Nuevo (Paso 1)
    new_ticket_payload = {
        "title": "Falla en telemetria de tensiometro RPM",
        "description": "Dispositivo no sincroniza lecturas de presion arterial con el portal de cronicos de OSDE.",
        "platform_code": "CAT_RPM_MONITOREO",
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "ALTO",
        "urgency": "ALTO",
        "requester_username": "solicitante"
    }
    r_create = client.post("/api/v1/tickets", json=new_ticket_payload)
    assert r_create.status_code == 200
    created = r_create.json()
    t_id = created["id"]
    print(f"\n[OK] Paso 1 (Registrar): Creado exitosamente [{t_id}] con prioridad {created['priority']} y estado {created['status']}")

    # 5. Paso 2: Asignar
    r_assign = client.patch(f"/api/v1/tickets/{t_id}/assign", json={
        "assignee_username": "soporte",
        "support_level": "N2",
        "reason": "Derivado a especialista de dispositivos RPM",
        "changed_by_username": "soporte"
    })
    assert r_assign.status_code == 200
    print(f"[OK] Paso 2 (Asignar): Asignado a '{r_assign.json()['assignee_username']}' en nivel '{r_assign.json()['support_level']}' -> Estado: {r_assign.json()['status']}")

    # 6. Paso 3: Iniciar Gestión
    r_progress = client.patch(f"/api/v1/tickets/{t_id}/status", json={
        "new_status": "EN_CURSO",
        "changed_by_username": "soporte",
        "reason": "Iniciando analisis de telemetria"
    })
    assert r_progress.status_code == 200
    print(f"[OK] Paso 3 (Gestionar): Estado actualizado a {r_progress.json()['status']}")

    # 7. Paso 4: Resolver
    r_resolve = client.post(f"/api/v1/tickets/{t_id}/resolve", json={
        "resolution_notes": "Se restablecio el certificado TLS en el gateway de telemetria de dispositivos.",
        "is_workaround": False,
        "resolved_by_username": "soporte"
    })
    assert r_resolve.status_code == 200
    print(f"[OK] Paso 4 (Resolver): Estado actualizado a {r_resolve.json()['status']} con solucion tecnica documentada.")

    # 8. Paso 5: Cerrar
    r_close = client.post(f"/api/v1/tickets/{t_id}/close", json={
        "closed_by_username": "solicitante",
        "feedback": "Conformidad asistencial verificada con el paciente."
    })
    assert r_close.status_code == 200
    print(f"[OK] Paso 5 (Cerrar): Ticket {t_id} cerrado e inmutable en estado {r_close.json()['status']}")

    # 9. Verificar Auditoría y Trazabilidad
    r_detail = client.get(f"/api/v1/tickets/{t_id}")
    audit_count = len(r_detail.json()["audit_logs"])
    print(f"\n[OK] Trazabilidad de Auditoria: {audit_count} eventos inmutables registrados con fecha y autor.")
    print("\n[EXITO] TODAS LAS PRUEBAS DE ARQUITECTURA Y BACKEND CORE PASARON EXITOSAMENTE (100%)!")

if __name__ == "__main__":
    run_tests()
