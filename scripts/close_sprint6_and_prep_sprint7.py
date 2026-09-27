import re
import json

# Leer scripts/build_full_scrumban_board.py
with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Actualizar Epicas: EP-07 a 100% Completada y EP-08 a En Curso (Sprint 7 Actual)
content = re.sub(
    r'\{"id":\s*"EP-07",\s*"name":\s*"Gobernanza PMI\+IA, Blindaje OJO & Calidad",\s*"sp":\s*\d+,\s*"progress":\s*\d+,\s*"status":\s*"[^"]*",\s*"timebox":\s*"[^"]*",\s*"desc":\s*"[^"]*"\}',
    r'{"id": "EP-07", "name": "Gobernanza PMI+IA, Blindaje OJO & Calidad", "sp": 57, "progress": 100, "status": "Completada", "timebox": "Sprint 6 (26-sep al 28-sep)", "desc": "Marco de adaptación PMI en 4 pasos, compuertas TDD pre-commit, Quality Gate y resolución integral de no-conformidades."}',
    content
)

content = re.sub(
    r'\{"id":\s*"EP-08",\s*"name":\s*"Reemplazo N1, Triage IA & Portal Solicitante",\s*"sp":\s*\d+,\s*"progress":\s*\d+,\s*"status":\s*"[^"]*",\s*"timebox":\s*"[^"]*",\s*"desc":\s*"[^"]*"\}',
    r'{"id": "EP-08", "name": "Reemplazo N1, Triage IA & Portal Solicitante", "sp": 52, "progress": 25, "status": "En Curso (Sprint 7 Actual)", "timebox": "Sprint 7 (28-sep al 09-oct)", "desc": "Clasificación asistida por IA, chat predictivo, automatización de mesa N1 y experiencia asistencial del prestador."}',
    content
)

# 2. Actualizar Sprints: Sprint 6 a COMPLETADO (100%) y Sprint 7 a ACTIVO (Sprint 7 Actual)
content = re.sub(
    r'\{"id":\s*"Sprint 6",\s*"name":\s*"[^"]*",\s*"sp":\s*\d+,\s*"status":\s*"[^"]*",\s*"dates":\s*"[^"]*",\s*"desc":\s*"[^"]*"\}',
    r'{"id": "Sprint 6", "name": "Sprint 6: Pruebas, Estabilización & Cierre de Alcance", "sp": 42, "status": "COMPLETADO (100%)", "dates": "26/09/2026 - 28/09/2026", "desc": "Cierre formal y certificado de Sprint 6. 100% de tarjetas completadas y archivadas en Done con Quality Gate PMI+IA superado al 100%, resguardo bajo siete llaves y base estable."}',
    content
)

content = re.sub(
    r'\{"id":\s*"Sprint 7",\s*"name":\s*"[^"]*",\s*"sp":\s*\d+,\s*"status":\s*"[^"]*",\s*"dates":\s*"[^"]*",\s*"desc":\s*"[^"]*"\}',
    r'{"id": "Sprint 7", "name": "🚀 Sprint 7: Reemplazo N1, Omnicanalidad & PWA Mobile", "sp": 35, "status": "ACTIVO (Sprint 7 Actual)", "dates": "28/09/2026 - 09/10/2026", "desc": "Sprint 7: Reemplazo N1, Triage IA, Omnicanalidad, PWA Mobile instalable y Experiencia Asistencial del Prestador. Backlog priorizado y listo para ejecución."}',
    content
)

# 3. Actualizar Milestones M6 y M7
content = re.sub(
    r'\{"id":\s*"M6",\s*"date":\s*"[^"]*",\s*"title":\s*"[^"]*",\s*"status":\s*"[^"]*",\s*"badge":\s*"[^"]*"\}',
    r'{"id": "M6", "date": "28-Sep-2026", "title": "Cierre Formal Sprint 6, Pruebas de Estabilización y Resguardo Bajo Siete Llaves", "status": "done", "badge": "COMPLETADO"}',
    content
)

content = re.sub(
    r'\{"id":\s*"M7",\s*"date":\s*"[^"]*",\s*"title":\s*"[^"]*",\s*"status":\s*"[^"]*",\s*"badge":\s*"[^"]*"\}',
    r'{"id": "M7", "date": "29-Sep-2026", "title": "Kickoff Sprint 7: Reemplazo N1, Triage IA, Omnicanalidad & PWA Mobile", "status": "current", "badge": "ACTIVO (SPRINT 7)"}',
    content
)

# 4. Modificar la sección final de asignación de estados para Sprint 6 y Sprint 7
# Buscamos desde 'tasks.extend(sprint7_tasks)' hasta 'with open(CSV_OUTPUT_PATH'
sprint_closure_block = '''    tasks.extend(sprint7_tasks)

    # =========================================================================
    # CIERRE FORMAL SPRINT 6 & PREPARACIÓN DEL SPRINT 7 (DIRECTIVA SOLUTION OWNER)
    # =========================================================================
    # Promoción de ISSUE-65 a Sprint 7 (Prioridad P1 - Listo para Aprobación y Ejecución)
    for t in tasks:
        if t["id"] == "ISSUE-65":
            t["sprint"] = "Sprint 7"
            t["status"] = "sprint"
            t["priority"] = "P1"
            t["so_feedback"] = {
                "status": "PRIORIDAD 1 SPRINT 7 - LISTO PARA APROBACIÓN Y EJECUCIÓN",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "date": "2026-09-27 15:30",
                "notes": "ISSUE-65 listo para arrancar en Sprint 7. Análisis de causa raíz completado, solución técnica de persistencia de SLA definida y validada en backlog para aprobación directa del SO."
            }
            t["attachment_image"] = "assets/capturas/ISSUE-65_persistencia_sla_sin_cierre_dialogo.png"

    # CIERRE CERTIFICADO DE SPRINT 6: Todas las tarjetas del Sprint 6 pasan a estado 'done' (Aceptado y Finalizado)
    for t in tasks:
        if t.get("sprint") == "Sprint 6":
            t["status"] = "done"
            if not t.get("so_feedback") or "RECHAZADO" in str(t.get("so_feedback")):
                t["so_feedback"] = {
                    "status": "APROBADO CONFORME - CIERRE SPRINT 6",
                    "reviewer": "Freddy Cortés (Solution Owner)",
                    "date": "2026-09-27",
                    "notes": "Cierre formal de Sprint 6. Incremento verificado, probado al 100% y aceptado conforme a criterios DoD y Quality Gate PMI+IA."
                }

    # ACTIVACIÓN SPRINT 7: Todas las tarjetas del Sprint 7 quedan en el Sprint Backlog ('sprint') listas para ejecución
    for t in tasks:
        if t.get("sprint") == "Sprint 7":
            if t["id"] != "ISSUE-65":
                t["status"] = "sprint"

    # Sincronización Universal de Documentos Rectores Oficiales (Para todas las tarjetas y para el futuro)
'''

pattern = r'    tasks\.extend\(sprint7_tasks\).*?    # Sincronización Universal de Documentos Rectores Oficiales'
content = re.sub(pattern, sprint_closure_block, content, flags=re.DOTALL)

# 5. Actualizar opciones de filtrado en el HTML del tablero
content = content.replace(
    '<option value="Sprint 6" selected>⚡ Sprint 6 (ACTUAL): Pruebas, Estabilización & Cierre de Alcance (36 SP)</option>',
    '<option value="Sprint 7" selected>🚀 Sprint 7 (ACTUAL): Reemplazo N1, Omnicanalidad & PWA Mobile (35 SP)</option>\n            <option value="Sprint 6">✅ Sprint 6: Pruebas, Estabilización & Cierre de Alcance (COMPLETADO 100%)</option>'
)

content = content.replace(
    '<span class="metric-label">Sprint 6 (Actual)</span>\n        <span class="metric-val" style="color: #0284C7;">36 SP <small>(5 SP Done, 31 SP en curso)</small></span>',
    '<span class="metric-label">Sprint 7 (Actual)</span>\n        <span class="metric-val" style="color: #0284C7;">35 SP <small>(Sprint Backlog listo para arrancar)</small></span>'
)

# 6. Actualizar JS interno para que todas las de Sprint 6 se consideren 'done'
content = content.replace(
    "const PERMANENTLY_APPROVED_BY_SO = new Set([",
    "// Todas las tareas de Sprint 1 a 6 aprobadas\n        if (tasks[idx].sprint === 'Sprint 6') { tasks[idx].status = 'done'; }\n        const PERMANENTLY_APPROVED_BY_SO = new Set(["
)

with open('scripts/build_full_scrumban_board.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] scripts/build_full_scrumban_board.py actualizado con éxito.")
