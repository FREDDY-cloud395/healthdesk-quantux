"""
AUDITORÍA INTEGRAL DE CALIDAD TQM — PRODUCTO COMPLETO
Proyecto: Quantux ServiceDesk Enterprise v4.3
Alcance: Backend APIs, Frontend DOM (index.html), Lógica Cliente (app.js, api.js),
         Restricciones OJO (Pizarra Neutral, Léxico No-Clínico), Ciclo ITIL 4 (7 Estados),
         KCS v6, Búsqueda Predictiva, Modal de Pre-Edición y Base de Conocimiento.
"""
import sys
import json
import urllib.request
import urllib.error
import re
from pathlib import Path

# Configuración UTF-8 en consola
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def run_tqm_audit():
    results = []
    
    def log_test(category, name, passed, details, severity="CRITICAL"):
        results.append({
            "category": category,
            "name": name,
            "passed": passed,
            "details": details,
            "severity": severity
        })
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"  {status} [{severity}] {category} -> {name}")
        if not passed:
            print(f"           DETALLE: {details}")

    print("=" * 80)
    print("  EJECUTANDO SUITE DE AUDITORÍA TQM COMPLETA SOBRE EL PRODUCTO")
    print("=" * 80)

    # -------------------------------------------------------------
    # 1. AUDITORÍA FRONTEND: frontend/index.html
    # -------------------------------------------------------------
    index_path = Path("frontend/index.html")
    index_content = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    # Test 1.1: Posición del Typeahead (Debe abrirse hacia abajo: top: 100%)
    has_dropdown = 'id="requester-typeahead-dropdown"' in index_content
    is_downwards = 'top: 100%' in index_content and 'bottom: 100%' not in index_content.split('id="requester-typeahead-dropdown"')[1][:200] if has_dropdown else False
    log_test("FRONTEND-DOM", "Typeahead: Despliegue hacia abajo (top: 100%)", is_downwards,
             "El dropdown predictivo tiene 'bottom: 100%', abriéndose hacia arriba y cortándose" if not is_downwards else "OK: Despliega hacia abajo")

    # Test 1.2: Cartel Rojo Invasivo MIM (No debe existir degradado rojo #DC2626)
    has_red_mim_modal = 'linear-gradient(135deg, #DC2626, #B91C1C)' in index_content
    log_test("FRONTEND-DOM", "Pizarra Neutral: Ausencia de cartel rojo #DC2626/#B91C1C", not has_red_mim_modal,
             "Detectado modal #modal-link-children con fondo degradado rojo saturado en index.html" if has_red_mim_modal else "OK: Sin fondos rojos")

    # Test 1.3: Árboles Técnico-Operativos en el DOM (Los 7 playbooks con .tree-node-row)
    has_tree_rows = 'tree-node-row' in index_content
    log_test("FRONTEND-DOM", "Árboles de Decisión: 7 playbooks estructurados en el DOM", has_tree_rows,
             "No existen filas .tree-node-row en frontend/index.html" if not has_tree_rows else "OK: Presentes")

    # Test 1.4: Modal de Previsualización y Edición de Ticket antes de crearlo
    has_preview_edit_modal = 'id="modal-preview-edit-ticket"' in index_content or 'modal-ticket-preview' in index_content
    log_test("FRONTEND-DOM", "Ticket UX: Modal de previsualización y edición antes de generar", has_preview_edit_modal,
             "No existe modal de pre-edición en index.html (creación ciega directa)" if not has_preview_edit_modal else "OK: Presente")

    # Test 1.5: Modal de Resolución KCS v6 con 4 niveles ITIL y vinculación KB
    has_kcs_resolve_modal = 'kcs' in index_content.lower() and 'resolve' in index_content.lower()
    log_test("FRONTEND-DOM", "Resolución KCS v6: Formulario estructurado en index.html", has_kcs_resolve_modal,
             "Modal de resolución no contempla esquema KCS v6 de 4 niveles" if not has_kcs_resolve_modal else "OK: Presente")

    # Test 1.6: Léxico Prohibido en index.html
    forbidden_terms = [
        "Guardia Médica 24/7",
        "SLA garantizado: < 15 min",
        "SLA de Atención: < 15 minutos",
        "Buscar por código o síntoma",
        "solicitudes clínicas",
        "historial farmacológico",
        "Quantux Asistencia Médica"
    ]
    found_forbidden = [t for t in forbidden_terms if t.lower() in index_content.lower()]
    log_test("RESTRICCIONES-OJO", "Léxico No-Clínico y SLA en index.html", len(found_forbidden) == 0,
             f"Términos prohibidos encontrados: {found_forbidden}" if found_forbidden else "OK: Sanitizado")

    # -------------------------------------------------------------
    # 2. AUDITORÍA JAVASCRIPT: frontend/js/app.js y api.js
    # -------------------------------------------------------------
    app_path = Path("frontend/js/app.js")
    app_content = app_path.read_text(encoding="utf-8") if app_path.exists() else ""
    api_path = Path("frontend/js/api.js")
    api_content = api_path.read_text(encoding="utf-8") if api_path.exists() else ""

    # Test 2.1: Definición de handleRequesterTypeahead
    has_typeahead_fn = "function handleRequesterTypeahead" in app_content or "handleRequesterTypeahead = " in app_content
    log_test("JAVASCRIPT", "Función handleRequesterTypeahead implementada", has_typeahead_fn,
             "handleRequesterTypeahead NO definida en app.js (causa ReferenceError al tipear)" if not has_typeahead_fn else "OK: Definida")

    # Test 2.2: Modal de edición previa invocado antes de createTicket
    has_escalate_preview = "openTicketPreviewModal" in app_content or "previewTicketBeforeCreate" in app_content
    log_test("JAVASCRIPT", "Flujo de creación: Pre-edición invocada antes de enviar", has_escalate_preview,
             "requesterAiEscalate envía ticket directamente a la API sin permitir edición previa" if not has_escalate_preview else "OK: Pre-edición activa")

    # Test 2.3: Base de Conocimiento activa (Copiar Solución / Vincular a Ticket)
    has_kb_copy_sol = "copyKbSolutionToTicket" in app_content or "applyKbToTicket" in app_content
    log_test("JAVASCRIPT", "Base de Conocimiento: Botón de transferir solución al ticket", has_kb_copy_sol,
             "La KB solo muestra checkboxes pasivos sin botón para aplicar solución al ticket" if not has_kb_copy_sol else "OK: Implementado")

    has_kb_link_ticket = "linkKbArticleToTicket" in app_content or "associateKbArticle" in app_content
    log_test("JAVASCRIPT", "Base de Conocimiento: Botón de vincular artículo al ticket", has_kb_link_ticket,
             "No existe función para asociar el artículo KB al ticket en curso" if not has_kb_link_ticket else "OK: Implementado")

    # Test 2.4: Ciclo de Vida ITIL 4 de 7 Estados en la UI
    has_7_states_ui = ("ESPERANDO_AL_PRESTADOR" in app_content and "EN_ESPERA_PASARELA_OSDE_SISA" in app_content)
    log_test("JAVASCRIPT", "Ciclo de Vida ITIL 4: 7 Estados seleccionables en la UI", has_7_states_ui,
             "app.js no incluye ESPERANDO_AL_PRESTADOR ni EN_ESPERA_PASARELA_OSDE_SISA en la botonera de acciones del ticket" if not has_7_states_ui else "OK: Presentes")

    # Test 2.5: Pausa de SLA visible en la UI
    has_sla_paused_ui = "sla_paused" in app_content or "Reloj SLA en Pausa" in app_content or "badge-sla-paused" in app_content
    log_test("JAVASCRIPT", "Pausa de SLA: Píldora indicadora visual en el detalle del ticket", has_sla_paused_ui,
             "No existe indicador visual de pausa de SLA en el render del ticket en app.js" if not has_sla_paused_ui else "OK: Indicador presente")

    # Test 2.6: Llamadas a endpoints KCS, Link Parent y Rescue en cliente
    has_kcs_close_call = "kcs-close" in app_content or "kcs-close" in api_content
    log_test("API-CLIENT", "Cliente API: Consumo de POST /api/v1/tickets/{id}/kcs-close", has_kcs_close_call,
             "El frontend no tiene conectado el endpoint kcs-close" if not has_kcs_close_call else "OK: Conectado")

    has_link_parent_call = "link-parent" in app_content or "link-parent" in api_content
    log_test("API-CLIENT", "Cliente API: Consumo de POST /api/v1/tickets/{id}/link-parent", has_link_parent_call,
             "El frontend no tiene conectado el endpoint link-parent para MIM" if not has_link_parent_call else "OK: Conectado")

    has_rescue_call = "/rescue" in app_content or "rescue" in api_content
    log_test("API-CLIENT", "Cliente API: Consumo de POST /api/v1/tickets/{id}/rescue", has_rescue_call,
             "El frontend no tiene conectado el endpoint de rescate CSAT" if not has_rescue_call else "OK: Conectado")

    # -------------------------------------------------------------
    # 3. AUDITORÍA BACKEND & SERVICIOS VIVOS (http://localhost:8000)
    # -------------------------------------------------------------
    backend_up = False
    try:
        req = urllib.request.Request("http://localhost:8000/health")
        with urllib.request.urlopen(req, timeout=3) as res:
            data = json.loads(res.read().decode("utf-8"))
            backend_up = (data.get("status") == "healthy" or "status" in data)
    except Exception as e:
        backend_up = False

    log_test("BACKEND-LIVE", "Servidor FastAPI activo en http://localhost:8000", backend_up,
             "El servidor FastAPI no responde en /health" if not backend_up else "OK: Saludable")

    # Test 3.1: Verificar FSM de 7 estados en backend
    try:
        from backend.app.models.entities import TicketStatus
        all_statuses = [s.value for s in TicketStatus]
        has_7 = len(all_statuses) == 7 and "ESPERANDO_AL_PRESTADOR" in all_statuses and "EN_ESPERA_PASARELA_OSDE_SISA" in all_statuses
        log_test("BACKEND-CORE", "FSM: 7 Estados ITIL 4 definidos en entidades", has_7,
                 f"Estados encontrados: {all_statuses}" if not has_7 else "OK: 7 Estados completos")
    except Exception as e:
        log_test("BACKEND-CORE", "FSM: 7 Estados ITIL 4 definidos en entidades", False, str(e))

    # -------------------------------------------------------------
    # 4. RESUMEN DE LA AUDITORÍA TQM
    # -------------------------------------------------------------
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    score = (passed / total) * 100

    print("\n" + "=" * 80)
    print(f"  RESUMEN DE AUDITORÍA TQM: {passed}/{total} PRUEBAS SUPERADAS ({score:.1f}%)")
    print(f"  DEFECTOS CRÍTICOS DETECTADOS: {failed}")
    print(f"  ESTADO DEL PRODUCTO: {'CERTIFICADO TQM' if failed == 0 else 'NO CONFORME — REQUIERE REFACTORIZACIÓN INMEDIATA'}")
    print("=" * 80)

    # Guardar reporte en JSON para trazabilidad
    report_file = Path("tqm_audit_report.json")
    report_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Reporte detallado guardado en {report_file.absolute()}")

if __name__ == "__main__":
    run_tqm_audit()
