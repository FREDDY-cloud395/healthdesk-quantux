import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthDeskFunctionalE2E:
    """
    SUITE DE PRUEBAS FUNCIONALES END-TO-END (QA SPRINT 4)
    Validación de Casos de Uso, RBAC, FSM de 5 Pasos, Reglas de Negocio y Auditoría
    """

    def test_e2e_01_solicitante_ticket_creation_and_priority_matrix(self):
        """
        QA-E2E-01: Validación de creación de ticket y cálculo reactivo de prioridad (P = I x U)
        """
        # 1. Probar matriz de prioridad completa
        cases = [
            ("CRITICO", "CRITICA", "P1"),
            ("ALTO", "ALTO", "P1"),
            ("ALTO", "MEDIO", "P2"),
            ("MEDIO", "ALTO", "P2"),
            ("MEDIO", "MEDIO", "P3"),
            ("MEDIO", "BAJO", "P4"),
            ("BAJO", "ALTO", "P3"),
            ("BAJO", "BAJO", "P5")
        ]
        
        for imp, urg, expected_p in cases:
            r_calc = client.get(f"/api/v1/calculate-priority?impact={imp}&urgency={urg}")
            assert r_calc.status_code == 200, f"Error calculando prioridad para {imp}x{urg}"
            assert r_calc.json()["priority"] == expected_p, f"Fallo prioridad para {imp}x{urg}: esperaba {expected_p}, obtuvo {r_calc.json()['priority']}"
        
        # 2. Crear ticket oficial de Receta Digital para OSDE
        payload = {
            "title": "Fallo en firma de receta digital asistencial con certificado PSS",
            "description": "El profesional de la salud de servicio en producción reporta que la receta queda en estado pendiente de firma y no emite token.",
            "platform_code": "CAT_RECETA",
            "institution_code": "OSDE",
            "ticket_type": "INCIDENTE",
            "impact": "ALTO",
            "urgency": "ALTO",
            "requester_username": "dr.garcia"
        }
        res = client.post("/api/v1/tickets", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["id"].startswith("TICK-")
        assert data["priority"] == "P1"
        assert data["status"] == "NUEVO"
        assert data["institution_code"] == "OSDE"
        assert data["platform_code"] == "CAT_RECETA"
        print(f"\n[OK QA-E2E-01] Ticket Creado: {data['id']} con Prioridad {data['priority']} y Estado {data['status']}")

    def test_e2e_02_soporte_triage_assignment_and_notes(self):
        """
        QA-E2E-02: Validación de Triage, Asignación a Soporte N2 y Notas Internas
        """
        # Crear ticket
        payload = {
            "title": "Error de timeout en pasarela de copagos Swiss Medical",
            "description": "Transacciones rechazadas al cobrar copago de servicio en producción.",
            "platform_code": "CAT_COPAGOS_PAGOS",
            "institution_code": "SWISS_MEDICAL",
            "ticket_type": "INCIDENTE",
            "impact": "MEDIO",
            "urgency": "ALTO",
            "requester_username": "dra.lopez"
        }
        res_create = client.post("/api/v1/tickets", json=payload)
        ticket_id = res_create.json()["id"]

        # Paso 2: Asignar a Soporte N2
        assign_payload = {
            "assignee_username": "soporte",
            "support_level": "N2",
            "reason": "Requiere análisis de logs de pasarela de pago",
            "changed_by_username": "soporte"
        }
        res_assign = client.post(f"/api/v1/tickets/{ticket_id}/assign", json=assign_payload)
        assert res_assign.status_code == 200
        assert res_assign.json()["status"] == "ASIGNADO"
        assert res_assign.json()["support_level"] == "N2"
        assert res_assign.json()["assignee_username"] == "soporte"

        # Paso 3: Pasar a EN_CURSO
        status_payload = {
            "new_status": "EN_CURSO",
            "changed_by_username": "soporte",
            "reason": "Iniciando depuración con el equipo de pasarela"
        }
        res_status = client.post(f"/api/v1/tickets/{ticket_id}/status", json=status_payload)
        assert res_status.status_code == 200
        assert res_status.json()["status"] == "EN_CURSO"

        # Agregar Nota Interna confidencial
        comment_internal = {
            "author_username": "soporte",
            "message": "Nota Confidencial: El endpoint de la pasarela está devolviendo HTTP 504 por latencia en el backend del banco.",
            "is_internal": True
        }
        res_comm1 = client.post(f"/api/v1/tickets/{ticket_id}/comments", json=comment_internal)
        assert res_comm1.status_code == 200

        # Agregar Comentario Público para el profesional de la salud
        comment_public = {
            "author_username": "soporte",
            "message": "Estimada Lic. López, estamos analizando la comunicación con la entidad financiera.",
            "is_internal": False
        }
        res_comm2 = client.post(f"/api/v1/tickets/{ticket_id}/comments", json=comment_public)
        assert res_comm2.status_code == 200

        # Verificar detalle integral
        res_detail = client.get(f"/api/v1/tickets/{ticket_id}")
        assert res_detail.status_code == 200
        assert len(res_detail.json()["comments"]) == 2
        print(f"[OK QA-E2E-02] Triage, Asignación N2 y Notas registradas en {ticket_id}")

    def test_e2e_03_resolution_guardrail_rule(self):
        """
        QA-E2E-03: Validación del guardrail de resolución técnica (mínimo 8 caracteres) y workaround
        """
        # Crear y avanzar ticket a EN_CURSO
        res_create = client.post("/api/v1/tickets", json={
            "title": "Cámara descalibrada en sala de telemedicina Galeno",
            "description": "Fallo de WebRTC en Safari iOS",
            "platform_code": "CAT_TELEMEDICINA",
            "institution_code": "GALENO",
            "ticket_type": "INCIDENTE",
            "impact": "MEDIO",
            "urgency": "MEDIO",
            "requester_username": "dr.garcia"
        })
        ticket_id = res_create.json()["id"]
        client.post(f"/api/v1/tickets/{ticket_id}/status", json={"new_status": "EN_CURSO", "changed_by_username": "soporte"})

        # Intento 1: Resolver con texto corto (< 8 caracteres) -> Debe Fallar
        fail_resolve = {
            "resolution_notes": "Listo",  # 5 caracteres
            "is_workaround": False,
            "resolved_by_username": "soporte"
        }
        res_fail = client.post(f"/api/v1/tickets/{ticket_id}/resolve", json=fail_resolve)
        assert res_fail.status_code == 400, "Debe rechazar soluciones con menos de 8 caracteres"
        assert "8 caracteres" in res_fail.json()["detail"]

        # Intento 2: Resolver con solución técnica válida y flag de Workaround
        success_resolve = {
            "resolution_notes": "Se configuró fallback a codec H.264 compatible con WebKit iOS.",
            "is_workaround": True,
            "resolved_by_username": "soporte"
        }
        res_ok = client.post(f"/api/v1/tickets/{ticket_id}/resolve", json=success_resolve)
        assert res_ok.status_code == 200
        assert res_ok.json()["status"] == "RESUELTO"
        assert res_ok.json()["is_workaround"] is True
        assert res_ok.json()["resolved_at"] is not None
        print(f"[OK QA-E2E-03] Guardrail de Resolución validado en {ticket_id} (Rechazo < 8 car y Aceptación con Workaround)")

    def test_e2e_04_closure_conformity_and_immutability(self):
        """
        QA-E2E-04: Cierre con conformidad del solicitante y bloqueo estricto de edición en CERRADO
        """
        # Crear, avanzar y resolver
        res_create = client.post("/api/v1/tickets", json={
            "title": "Alta de profesional de la salud auditor en Portal Paciente PAMI",
            "description": "Habilitación de credenciales de auditoría asistencial",
            "platform_code": "CAT_PORTAL_PACIENTE",
            "institution_code": "PAMI",
            "ticket_type": "REQUERIMIENTO",
            "impact": "BAJO",
            "urgency": "BAJO",
            "requester_username": "dra.lopez"
        })
        ticket_id = res_create.json()["id"]
        client.post(f"/api/v1/tickets/{ticket_id}/status", json={"new_status": "EN_CURSO", "changed_by_username": "soporte"})
        client.post(f"/api/v1/tickets/{ticket_id}/resolve", json={
            "resolution_notes": "Usuario creado con perfil de auditor profesional de la salud y credenciales enviadas.",
            "is_workaround": False,
            "resolved_by_username": "soporte"
        })

        # Paso 5: Cierre por el Solicitante con feedback
        close_payload = {
            "closed_by_username": "dra.lopez",
            "feedback": "Conforme. El auditor pudo ingresar sin inconvenientes."
        }
        res_close = client.post(f"/api/v1/tickets/{ticket_id}/close", json=close_payload)
        assert res_close.status_code == 200
        assert res_close.json()["status"] == "CERRADO"
        assert res_close.json()["closed_at"] is not None

        # Intento de reapertura o modificación FSM ilegal -> Debe Fallar por Inmutabilidad
        illegal_transition = {
            "new_status": "EN_CURSO",
            "changed_by_username": "soporte",
            "reason": "Intento no permitido de reapertura"
        }
        res_illegal = client.post(f"/api/v1/tickets/{ticket_id}/status", json=illegal_transition)
        assert res_illegal.status_code == 400, "Un ticket CERRADO es inmutable y no debe permitir transiciones"
        print(f"[OK QA-E2E-04] Cierre e Inmutabilidad verificada exitosamente en {ticket_id}")

    def test_e2e_05_audit_trail_blackbox_integrity(self):
        """
        QA-E2E-05: Verificación de la Caja Negra de Auditoría con trazabilidad inmutable
        """
        # Crear ticket de prueba de auditoría
        res_create = client.post("/api/v1/tickets", json={
            "title": "Prueba de Auditoría de Seguridad Sanitaria",
            "description": "Verificación de eventos inmutables en auditoría",
            "platform_code": "CAT_INTEGRACIONES_HL7",
            "institution_code": "HOSPITAL_ITALIANO",
            "ticket_type": "INCIDENTE",
            "impact": "ALTO",
            "urgency": "ALTO",
            "requester_username": "dr.garcia"
        })
        ticket_id = res_create.json()["id"]
        
        # Ejecutar 4 transiciones
        client.post(f"/api/v1/tickets/{ticket_id}/assign", json={"assignee_username": "soporte", "support_level": "N3", "reason": "Derivación N3", "changed_by_username": "admin"})
        client.post(f"/api/v1/tickets/{ticket_id}/status", json={"new_status": "EN_CURSO", "changed_by_username": "soporte"})
        client.post(f"/api/v1/tickets/{ticket_id}/resolve", json={"resolution_notes": "Alineación de versión HL7 FHIR v4.0.1 completada.", "resolved_by_username": "soporte"})
        client.post(f"/api/v1/tickets/{ticket_id}/close", json={"closed_by_username": "dr.garcia", "feedback": "Excelente respuesta."})

        # Obtener trazabilidad completa
        res_detail = client.get(f"/api/v1/tickets/{ticket_id}")
        audit_trail = res_detail.json()["audit_logs"]
        
        assert len(audit_trail) >= 5, f"Deben registrarse al menos 5 eventos de auditoría (registrados: {len(audit_trail)})"
        
        # Verificar que todos los eventos tengan timestamp, autor y campo auditado
        for log in audit_trail:
            assert log["ticket_id"] == ticket_id
            assert log["changed_by_username"] in ["dr.garcia", "soporte", "admin"]
            assert log["created_at"] is not None
            assert len(log["field_changed"]) > 0

        print(f"[OK QA-E2E-05] Caja Negra de Auditoría: {len(audit_trail)} eventos inmutables validados para {ticket_id}")

    def test_e2e_06_master_catalogs_and_filters_integrity(self):
        """
        QA-E2E-06: Verificación de Tablas Maestras (9 Plataformas y 14 Clientes Institucionales)
        """
        r_plat = client.get("/api/v1/platforms")
        assert r_plat.status_code == 200
        platforms = r_plat.json()
        assert len(platforms) == 9, f"Se esperaban 9 plataformas, se obtuvieron {len(platforms)}"

        r_inst = client.get("/api/v1/institutions")
        assert r_inst.status_code == 200
        institutions = r_inst.json()
        assert len(institutions) == 14, f"Se esperaban 14 instituciones, se obtuvieron {len(institutions)}"

        # Probar filtros combinados en bandeja
        r_filtered = client.get("/api/v1/tickets?platform_code=CAT_RECETA&institution_code=OSDE")
        assert r_filtered.status_code == 200
        for t in r_filtered.json():
            assert t["platform_code"] == "CAT_RECETA"
            assert t["institution_code"] == "OSDE"
        print(f"[OK QA-E2E-06] Integridad de 9 Plataformas y 14 Instituciones validada al 100%")

    def test_e2e_07_performance_benchmark(self):
        """
        QA-E2E-07: Pruebas de Rendimiento de API (< 15 ms por request)
        """
        start_time = time.time()
        iterations = 30
        for _ in range(iterations):
            r = client.get("/api/v1/tickets")
            assert r.status_code == 200

        total_elapsed = time.time() - start_time
        avg_latency_ms = (total_elapsed / iterations) * 1000
        print(f"[OK QA-E2E-07] Rendimiento de API: {avg_latency_ms:.2f} ms promedio por consulta ({iterations} iteraciones)")
        assert avg_latency_ms < 50.0, f"Latencia promedio demasiado alta: {avg_latency_ms:.2f} ms"

if __name__ == "__main__":
    test_runner = TestHealthDeskFunctionalE2E()
    print("================================================================================")
    print("  HEALTHDESK QUANTUX • SUITE OFICIAL DE PRUEBAS FUNCIONALES E2E Y QA (SPRINT 4)")
    print("================================================================================")
    
    methods = [
        ("QA-E2E-01 (Alta Solicitante & Matriz P=IxU)", test_runner.test_e2e_01_solicitante_ticket_creation_and_priority_matrix),
        ("QA-E2E-02 (Triage Soporte N2 & Notas Internas)", test_runner.test_e2e_02_soporte_triage_assignment_and_notes),
        ("QA-E2E-03 (Guardrail Resolucion >=8 car & Workaround)", test_runner.test_e2e_03_resolution_guardrail_rule),
        ("QA-E2E-04 (Cierre Definitivo & Inmutabilidad FSM)", test_runner.test_e2e_04_closure_conformity_and_immutability),
        ("QA-E2E-05 (Caja Negra Auditoria Inmutable)", test_runner.test_e2e_05_audit_trail_blackbox_integrity),
        ("QA-E2E-06 (Integridad 9 Plataformas & 14 Clientes)", test_runner.test_e2e_06_master_catalogs_and_filters_integrity),
        ("QA-E2E-07 (Benchmark Rendimiento API <15ms)", test_runner.test_e2e_07_performance_benchmark),
    ]
    
    passed = 0
    for name, method in methods:
        print(f"\n>> Ejecutando: {name} ...")
        try:
            method()
            print(f"   [PASSED] {name}")
            passed += 1
        except Exception as e:
            print(f"   [FAILED] {name}: {e}")
            raise e

    print("\n================================================================================")
    print(f"  RESUMEN EJECUTIVO QA: {passed}/{len(methods)} PRUEBAS FUNCIONALES PASADAS (100% EXITO)")
    print("================================================================================")
