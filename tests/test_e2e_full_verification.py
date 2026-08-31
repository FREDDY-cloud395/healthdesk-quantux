"""
Suite de Pruebas Automatizadas E2E Integral
HealthDesk Quantux — Verificación de Funcionalidades del MVP al 100%
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import re
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def request(method, path, data=None, headers=None):
    if "?" in path:
        base, query = path.split("?", 1)
        params = urllib.parse.parse_qsl(query)
        encoded_query = urllib.parse.urlencode(params)
        url = f"{BASE_URL}{base}?{encoded_query}"
    else:
        url = f"{BASE_URL}{path}"
    req_headers = headers or {}
    req_data = None
    if data is not None:
        if isinstance(data, dict):
            req_data = json.dumps(data).encode("utf-8")
            req_headers["Content-Type"] = "application/json"
        elif isinstance(data, str):
            req_data = data.encode("utf-8")
        else:
            req_data = data
            
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
            content_type = res.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return res.status, json.loads(body.decode("utf-8")), res.headers
            else:
                return res.status, body.decode("utf-8", errors="replace"), res.headers
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            err_json = json.loads(body.decode("utf-8"))
            return e.code, err_json, e.headers
        except:
            return e.code, body.decode("utf-8", errors="replace"), e.headers

def run_suite():
    passed = []
    failed = []

    def test(name, condition, details=""):
        if condition:
            print(f"  [PASS] {name} {details}")
            passed.append(name)
        else:
            print(f"  [FAIL] {name} - {details}")
            failed.append((name, details))

    print("\n=======================================================")
    print(" INICIANDO VERIFICACIÓN E2E DE FUNCIONALIDADES MVP")
    print("=======================================================\n")

    # -------------------------------------------------------------
    # 1. SERVIDOR, HTML PRINCIPAL Y ASSETS
    # -------------------------------------------------------------
    print("--> 1. Verificación de Frontend y Assets...")
    status, html, _ = request("GET", "/")
    test("Endpoint Raíz (Status 200)", status == 200)
    test("HTML contiene Selector Institucional (#dash-filter-inst)", 'id="dash-filter-inst"' in html)
    test("HTML contiene Botón Refrescar Dashboard (#btn-refresh-dash)", 'id="btn-refresh-dash"' in html)
    test("HTML contiene Modal Nueva Solicitud (#modal-ticket)", 'id="modal-ticket"' in html)
    test("HTML contiene Badge Prioridad Dinámica (#modal-calculated-priority)", 'id="modal-calculated-priority"' in html)
    test("HTML contiene Modal Nuevo Usuario (#modal-user)", 'id="modal-user"' in html)
    test("HTML contiene Modal de Autenticación y Cambio de Usuario (#modal-auth-login)", 'id="modal-auth-login"' in html)
    test("HTML NO contiene selector inseguro de cambio de rol al vuelo", 'role-pill-group' not in html)
    test("HTML contiene Cockpit Operativo (col-list, col-detail)", 'id="col-list"' in html and 'id="col-detail"' in html)
    test("HTML contiene Botón Topbar Cerrar Sesión / Cambiar Usuario (#btn-top-switch-user)", 'id="btn-top-switch-user"' in html)
    test("HTML contiene Widget Sidebar de Usuario (#btn-sidebar-user-profile)", 'id="btn-sidebar-user-profile"' in html)
    test("HTML contiene Enlaces de Respaldo CSV Directo", '/api/v1/tickets/export/csv' in html and '/api/v1/tickets/audit/export/csv' in html)

    # Verificar que NO hay funciones ficticias o mocks en index.html
    test("HTML NO contiene botones falsos ni mocks", 
         'testNotificationDiagnostic' not in html and 
         'saveNotificationSettings' not in html and 
         'testSystemHealthDiagnostic' not in html and 
         'showConfigToast' not in html)

    # Verificar JS y CSS
    st_js1, js1, _ = request("GET", "/js/api.js")
    st_js2, js2, _ = request("GET", "/js/app.js")
    st_css, css, _ = request("GET", "/css/styles.css")
    test("Carga de /js/api.js (Status 200)", st_js1 == 200 and len(js1) > 1000)
    test("Carga de /js/app.js (Status 200)", st_js2 == 200 and len(js2) > 5000)
    test("Carga de /css/styles.css (Status 200)", st_css == 200 and len(css) > 5000)

    # -------------------------------------------------------------
    # 2. TABLAS MAESTRAS, AUTENTICACIÓN Y ESTADO DE API
    # -------------------------------------------------------------
    print("\n--> 2. Verificación de Tablas Maestras y API...")
    status, api_info, _ = request("GET", "/api")
    test("Endpoint /api Estado ONLINE", status == 200 and api_info.get("status") == "ONLINE")

    status, plats, _ = request("GET", "/api/v1/platforms")
    test("Maestro de Plataformas (9 Oficiales)", status == 200 and len(plats) == 9, f"Plataformas: {len(plats)}")

    status, insts, _ = request("GET", "/api/v1/institutions")
    test("Maestro de Instituciones (14 Oficiales)", status == 200 and len(insts) >= 14, f"Instituciones: {len(insts)}")

    status, ops, _ = request("GET", "/api/v1/users/operators")
    test("Listado de Operadores de Soporte", status == 200 and len(ops) > 0, f"Operadores: {len(ops)}")

    status, users, _ = request("GET", "/api/v1/users")
    test("Directorio de Usuarios", status == 200 and len(users) >= 3, f"Usuarios: {len(users)}")

    # Pruebas de Autenticación y Cierre de Sesión (POST /login)
    st_l1, u_admin, _ = request("POST", "/api/v1/auth/login", {"username": "admin", "password": "quantux123"})
    test("Login Usuario Admin con Password Válido", st_l1 == 200 and u_admin.get("role") == "ADMIN", f"Usuario: {u_admin.get('full_name')}")

    st_l2, u_sop, _ = request("POST", "/api/v1/auth/login", {"username": "soporte", "password": "quantux123"})
    test("Login Usuario Soporte con Password Válido", st_l2 == 200 and u_sop.get("role") == "SOPORTE", f"Usuario: {u_sop.get('full_name')}")

    st_l3, u_sol, _ = request("POST", "/api/v1/auth/login", {"username": "solicitante", "password": "quantux123"})
    test("Login Usuario Solicitante con Password Válido", st_l3 == 200 and u_sol.get("role") == "SOLICITANTE", f"Usuario: {u_sol.get('full_name')}")

    st_inv_u, err_u, _ = request("POST", "/api/v1/auth/login", {"username": "usuario_inexistente_999", "password": "quantux123"})
    test("Rechazo de Usuario Inexistente (401 Unauthorized)", st_inv_u == 401)

    st_inv_p, err_p, _ = request("POST", "/api/v1/auth/login", {"username": "admin", "password": "password_erroneo"})
    test("Rechazo de Password Incorrecto (401 Unauthorized)", st_inv_p == 401)

    # -------------------------------------------------------------
    # 3. MATRIZ DE PRIORIZACIÓN ITIL EN TIEMPO REAL
    # -------------------------------------------------------------
    print("\n--> 3. Verificación de Matriz de Prioridad ITIL...")
    itil_matrix_tests = [
        ("ALTO", "ALTO", "P1"),
        ("ALTO", "MEDIO", "P2"),
        ("MEDIO", "ALTO", "P2"),
        ("MEDIO", "MEDIO", "P3"),
        ("ALTO", "BAJO", "P3"),
        ("BAJO", "ALTO", "P3"),
        ("MEDIO", "BAJO", "P4"),
        ("BAJO", "MEDIO", "P4"),
        ("BAJO", "BAJO", "P5"),
    ]
    for imp, urg, expected_prio in itil_matrix_tests:
        st, res, _ = request("GET", f"/api/v1/calculate-priority?impact={imp}&urgency={urg}")
        actual_prio = res.get("priority")
        test(f"Cálculo ITIL ({imp} x {urg} = {expected_prio})", st == 200 and actual_prio == expected_prio, f"Resultado: {actual_prio}")

    # -------------------------------------------------------------
    # 4. TABLERO DE CONTROL Y FILTRO INSTITUCIONAL EN VIVO
    # -------------------------------------------------------------
    print("\n--> 4. Verificación de Métricas y Filtro Institucional...")
    status, global_metrics, _ = request("GET", "/api/v1/tickets/metrics/summary")
    test("Métricas Globales (Dashboard)", status == 200 and global_metrics.get("total_tickets", 0) > 0, 
         f"Total: {global_metrics.get('total_tickets')}, P1: {global_metrics.get('p1_critical_tickets')}")

    # Filtrar por OSDE
    status, osde_metrics, _ = request("GET", "/api/v1/tickets/metrics/summary?institution_code=OSDE")
    test("Métricas Filtradas por OSDE", status == 200 and osde_metrics.get("total_tickets", 0) > 0 and osde_metrics.get("total_tickets") <= global_metrics.get("total_tickets"),
         f"Total OSDE: {osde_metrics.get('total_tickets')} vs Global: {global_metrics.get('total_tickets')}")
    test("Desglose Institucional solo incluye OSDE", list(osde_metrics.get("by_institution", {}).keys()) == ["OSDE"])

    # Filtrar por SWISS_MEDICAL
    status, swiss_metrics, _ = request("GET", "/api/v1/tickets/metrics/summary?institution_code=SWISS_MEDICAL")
    test("Métricas Filtradas por SWISS_MEDICAL", status == 200 and swiss_metrics.get("total_tickets", 0) > 0,
         f"Total Swiss Medical: {swiss_metrics.get('total_tickets')}")

    # Filtrar por Plataforma
    status, plat_metrics, _ = request("GET", "/api/v1/tickets/metrics/summary?platform_code=CAT_RECETA")
    test("Métricas Filtradas por Plataforma CAT_RECETA", status == 200 and plat_metrics.get("total_tickets", 0) > 0,
         f"Total CAT_RECETA: {plat_metrics.get('total_tickets')}")

    # -------------------------------------------------------------
    # 5. CREACIÓN, FILTRADO Y CICLO DE VIDA COMPLETO FSM
    # -------------------------------------------------------------
    print("\n--> 5. Verificación de Ciclo de Vida FSM de Tickets...")
    # Crear un nuevo ticket
    new_ticket_payload = {
        "title": "Falla de acceso concurrente en módulo asistencial",
        "description": "Se detecta error de conectividad y timeout al cargar turnos del día.",
        "platform_code": "CAT_RECETA",
        "institution_code": "OSDE",
        "impact": "ALTO",
        "urgency": "ALTO",
        "ticket_type": "INCIDENTE",
        "requester_username": "solicitante"
    }
    status, created_ticket, _ = request("POST", "/api/v1/tickets", new_ticket_payload)
    test("Creación de Solicitud (POST /api/v1/tickets)", status == 200 and "id" in created_ticket, f"ID: {created_ticket.get('id')}")
    ticket_id = created_ticket.get("id")
    test("Prioridad Asignada Automáticamente P1", created_ticket.get("priority") == "P1")
    test("Estado Inicial NUEVO", created_ticket.get("status") == "NUEVO")

    # Consultar detalle del ticket
    status, detail, _ = request("GET", f"/api/v1/tickets/{ticket_id}")
    test("Consulta Detalle de Ticket (GET /api/v1/tickets/{id})", status == 200 and detail.get("ticket", {}).get("id") == ticket_id)

    # Agregar Comentario Público y Privado
    st_c1, c1, _ = request("POST", f"/api/v1/tickets/{ticket_id}/comments", {
        "author_username": "soporte",
        "message": "Iniciando diagnóstico técnico de infraestructura.",
        "is_internal": False
    })
    test("Registro de Comentario Público", st_c1 == 200 and c1.get("message") == "Iniciando diagnóstico técnico de infraestructura.")

    st_c2, c2, _ = request("POST", f"/api/v1/tickets/{ticket_id}/comments", {
        "author_username": "admin",
        "message": "Nota interna confidencial para el equipo de servicio en producción.",
        "is_internal": True
    })
    test("Registro de Nota Interna Privada", st_c2 == 200 and c2.get("is_internal") is True)

    # FSM Paso 1: Asignar / Derivar
    status, assigned_ticket, _ = request("PATCH", f"/api/v1/tickets/{ticket_id}/assign", {
        "assignee_username": "soporte",
        "support_level": "N2",
        "reason": "Derivación a especialista de servicio en producción N2",
        "changed_by_username": "admin"
    })
    test("FSM Paso 1: Asignación a Operador (N2)", status == 200 and assigned_ticket.get("status") == "ASIGNADO" and assigned_ticket.get("assignee_username") == "soporte")

    # FSM Paso 2: Cambiar a En Curso
    status, in_progress_ticket, _ = request("PATCH", f"/api/v1/tickets/{ticket_id}/status", {
        "new_status": "EN_CURSO",
        "reason": "Comenzando análisis de logs y pruebas de conexión",
        "changed_by_username": "soporte"
    })
    test("FSM Paso 2: Cambio de Estado a EN_CURSO", status == 200 and in_progress_ticket.get("status") == "EN_CURSO")

    # FSM Paso 3: Resolver Ticket con Notas Técnicas
    status, resolved_ticket, _ = request("POST", f"/api/v1/tickets/{ticket_id}/resolve", {
        "resolution_notes": "Se reinició el servicio de autenticación y se verificó el restablecimiento del acceso.",
        "is_workaround": False,
        "resolved_by_username": "soporte"
    })
    test("FSM Paso 3: Resolución Técnica (RESUELTO)", status == 200 and resolved_ticket.get("status") == "RESUELTO" and resolved_ticket.get("resolved_at") is not None)

    # FSM Paso 4: Cerrar Ticket con Conformidad del Solicitante
    status, closed_ticket, _ = request("POST", f"/api/v1/tickets/{ticket_id}/close", {
        "closed_by_username": "solicitante",
        "feedback": "Conformidad asistencial verificada satisfactoriamente en puesto de servicio en producción."
    })
    test("FSM Paso 4: Cierre Definitivo con Conformidad (CERRADO)", status == 200 and closed_ticket.get("status") == "CERRADO" and closed_ticket.get("closed_at") is not None)

    # Verificar Historial de Auditoría Inmutable del Ticket
    status, detail_final, _ = request("GET", f"/api/v1/tickets/{ticket_id}")
    audit_logs = detail_final.get("audit_logs", [])
    test("Bitácora de Auditoría Inmutable Registrada", status == 200 and len(audit_logs) >= 4, f"Registros de auditoría: {len(audit_logs)}")

    # -------------------------------------------------------------
    # 6. FILTROS Y BÚSQUEDA DE BANDEJA
    # -------------------------------------------------------------
    print("\n--> 6. Verificación de Filtros de Mesa de Ayuda...")
    st, t_status, _ = request("GET", "/api/v1/tickets?status=CERRADO")
    test("Filtro por Estado CERRADO", st == 200 and all(t.get("status") == "CERRADO" for t in t_status))

    st, t_prio, _ = request("GET", "/api/v1/tickets?priority=P1")
    test("Filtro por Prioridad P1", st == 200 and all(t.get("priority") == "P1" for t in t_prio))

    st, t_inst, _ = request("GET", "/api/v1/tickets?institution_code=OSDE")
    test("Filtro por Institución OSDE", st == 200 and all(t.get("institution_code") == "OSDE" for t in t_inst))

    st, t_search, _ = request("GET", "/api/v1/tickets?search=acceso")
    test("Búsqueda por Texto Libre ('acceso')", st == 200 and len(t_search) > 0)

    # -------------------------------------------------------------
    # 7. EXPORTACIÓN CSV DE BASE DE TICKETS Y AUDITORÍA
    # -------------------------------------------------------------
    print("\n--> 7. Verificación de Exportaciones CSV...")
    st, csv_tickets, hd_t = request("GET", "/api/v1/tickets/export/csv")
    test("Exportación CSV de Base de Tickets (Status 200)", st == 200 and "id,titulo" in csv_tickets.lower())
    test("Cabecera Content-Type text/csv", "text/csv" in hd_t.get("Content-Type", ""))

    st, csv_audit, hd_a = request("GET", "/api/v1/tickets/audit/export/csv")
    test("Exportación CSV de Bitácora de Auditoría (Status 200)", st == 200 and "campo_modificado" in csv_audit.lower())

    # -------------------------------------------------------------
    # 8. ALTA DE USUARIOS
    # -------------------------------------------------------------
    print("\n--> 8. Verificación de Gestión de Usuarios...")
    import time
    uname = f"op_qa_{int(time.time())}"
    new_user_payload = {
        "username": uname,
        "full_name": "Lic. Carlos Paez (Soporte Servicio en Producción)",
        "email": f"{uname}@quantux.com",
        "role": "SOPORTE",
        "institution_code": "OSDE"
    }
    st, created_user, _ = request("POST", "/api/v1/users", new_user_payload)
    test("Alta de Usuario en Backend", st == 200 and created_user.get("username") == uname)

    st, all_users, _ = request("GET", "/api/v1/users")
    test("Persistencia del Nuevo Usuario en el Directorio", any(u.get("username") == uname for u in all_users))

    # -------------------------------------------------------------
    # 9. BASE DE CONOCIMIENTO (KB ARTICLES CRUD)
    # -------------------------------------------------------------
    print("\n--> 9. Verificación de Base de Conocimiento (KB Articles)...")
    kb_payload = {
        "title": "Protocolo de Recuperación de Enlace LIS HL7 en Contingencia",
        "category": "DIAGNOSTICO",
        "content": "Pasos para reiniciar el listener HL7 y forzar el reenvío de resultados pendientes.",
        "author_username": "freddy.cortes"
    }
    st, created_art, _ = request("POST", "/api/v1/articles", kb_payload)
    test("Creación de Artículo KB (Status 200)", st == 200 and created_art.get("id") is not None)
    art_id = created_art.get("id")

    st, arts, _ = request("GET", "/api/v1/articles?category=DIAGNOSTICO")
    test("Filtro de Artículos por Categoría", st == 200 and any(a.get("id") == art_id for a in arts))

    st, searched_arts, _ = request("GET", "/api/v1/articles?search=listener")
    test("Búsqueda en Base de Conocimiento", st == 200 and any(a.get("id") == art_id for a in searched_arts))

    if art_id:
        st, del_res, _ = request("DELETE", f"/api/v1/articles/{art_id}")
        test("Eliminación de Artículo KB", st == 200)

    # -------------------------------------------------------------
    # 10. CONFIGURACIÓN DEL SISTEMA Y MATRIZ DE SLAs
    # -------------------------------------------------------------
    print("\n--> 10. Verificación de Configuración del Sistema...")
    st, cfg, _ = request("GET", "/api/v1/config")
    test("Consulta de Configuración del Sistema (Status 200)", st == 200 and cfg.get("sla_p1_response") is not None)

    cfg_update = {
        "sla_p1_response": 10,
        "sla_p1_resolution": 90,
        "notify_p1_critical": True,
        "require_resolution_note": True
    }
    st, upd_cfg, _ = request("PUT", "/api/v1/config", cfg_update)
    test("Actualización de Parámetros Globales de SLA", st == 200 and upd_cfg.get("sla_p1_response") == 10 and upd_cfg.get("sla_p1_resolution") == 90)

    # -------------------------------------------------------------
    # 11. OMNI-BUSCADOR Y FILTRADO POR RESPONSABLE ASIGNADO
    # -------------------------------------------------------------
    print("\n--> 11. Verificación de Omni-Búsqueda y Filtro Asignados a Mí...")
    st, mine_tickets, _ = request("GET", "/api/v1/tickets?assignee_username=laura.benitez")
    test("Filtro de Tickets Asignados por Username", st == 200 and all(t.get("assignee_username") == "laura.benitez" for t in mine_tickets))

    st, omni_name_tickets, _ = request("GET", "/api/v1/tickets?search=Freddy Cortés")
    test("Omni-Búsqueda por Nombre Completo con Acentos", st == 200 and len(omni_name_tickets) > 0)

    st, omni_plat_tickets, _ = request("GET", "/api/v1/tickets?search=Receta Digital")
    test("Omni-Búsqueda por Nombre de Plataforma Clínica", st == 200 and len(omni_plat_tickets) > 0)

    # -------------------------------------------------------------
    # RESUMEN FINAL
    # -------------------------------------------------------------
    print("\n=======================================================")
    print(f" RESUMEN DE PRUEBAS: {len(passed)} APROBADAS, {len(failed)} FALLIDAS")
    print("=======================================================")

    if failed:
        print("\n[!] PRUEBAS CON FALLO:")
        for name, detail in failed:
            print(f"  - {name}: {detail}")
        return False
    else:
        print("\n[OK] TODAS LAS PRUEBAS QA E2E PASARON AL 100% DE FORMA EXITOSA.")
        return True

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)

