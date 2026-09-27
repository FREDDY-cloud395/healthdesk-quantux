import re

with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Prepare ISSUE-78 definition
issue_78_card = """        {
        "id": "ISSUE-78",
        "title": "[P0 - GOBERNANZA AGÉNTICA] Protocolo Demonio: Propuesta Técnica Previa en Retrabajo y Ejecución de Desarrollo Bajo Demanda al Clic del Solution Owner",
        "epic": "EP-01: Arquitectura y Gobierno del Producto",
        "sp": 5,
        "sprint": "Sprint 6",
        "status": "progress",
        "discipline": "Architecture / Agentic Automation & Governance",
        "type": "TASK",
        "priority": "P0",
        "business_impact": {
                "classification": "GOBERNANZA AGÉNTICA Y CONTROL TOTAL DEL DESARROLLO",
                "summary": "Establece el protocolo mandatorio: ante una tarjeta observada en Retrabajo, el agente diagnostica y formula la Propuesta Técnica de Solución dejándola visible para revisión; el Solution Owner inspecciona la propuesta y, únicamente si la aprueba, hace clic en el Demonio para disparar la ejecución real del código.",
                "kpi_affected": "Control de Calidad de Código & Auditoría de Remediación Automatizada",
                "risk_if_delayed": "Desarrollos autónomos no autorizados o pérdida de supervisión sobre las remediaciones del Demonio."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-78",
        "doc_title": "DOC-GOV-010 (ISSUE-78)",
        "doc_desc": "Protocolo formal de retrabajo: análisis y propuesta previa, y ejecución diferida bajo demanda del Demonio.",
        "attachment_image": "assets/capturas/ISSUE-78_protocolo_demonio.png",
        "issue_details": {
                "severity": "P0 — Máxima Prioridad Ordenada por Solution Owner",
                "component": "scripts/build_full_scrumban_board.py, docs/00_Tablero_Scrumban_Quantux.html, backend/app/api/endpoints/demon.py, docs/02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md",
                "description": "El Solution Owner dictó la regla estricta: 'lo que debes hacer cuando detectes que una tarjeta pase a retrabajo es analizar la observación y proponer la solución, asi lo dejas listo para que lo revise y si lo apruebo le doy clic al demonio para que ejecute el desarrollo de la solución, confirmame si me entiendes y pon una tarjeta de máxima prioriodad y empieza con su ejecución de inmediato'.",
                "root_cause": "Inconsistencia conceptual previa donde el agente ejecutaba código antes de que el Solution Owner aprobara la propuesta técnica y disparara el Demonio.",
                "solution": "Implementar en cada tarjeta de retrabajo el bloque 'Propuesta Técnica de Solución del Agente' con diagnóstico de causa raíz y plan de cambios, dejando el botón del Demonio como el trigger oficial que aprueba y ejecuta el desarrollo de código.",
                "acceptance_criteria": [
                        "Escenario 1: Al pasar una tarjeta a Retrabajo, el agente analiza la observación y registra la Propuesta Técnica de Solución sin modificar código productivo.",
                        "Escenario 2: La tarjeta en Retrabajo y su modal exhiben claramente la Observación del SO y la Propuesta Técnica del Agente.",
                        "Escenario 3: La ejecución del desarrollo de la solución se dispara única y exclusivamente cuando el Solution Owner hace clic en el botón del Demonio.",
                        "Escenario 4: La tarjeta ISSUE-78 queda registrada en el tablero como P0 con estado En Ejecución (progress)."
                ]
        }
},"""

# Insert ISSUE-78 before extra_tasks.extend(sprint6_so_traceability_cards)
target_insert = '    extra_tasks.extend(sprint6_so_traceability_cards)'
if target_insert in code and '"ISSUE-78"' not in code:
    code = code.replace(target_insert, issue_78_card + '\n' + target_insert)
    print("Inserted ISSUE-78 card definition!")

# 2. Update SPRINT6_NEW_SET to include ISSUE-78
code = code.replace('"ISSUE-77"]', '"ISSUE-77", "ISSUE-78"]')
print("Updated SPRINT6_NEW_SET with ISSUE-78!")

# 3. Add proposed_solution to existing rework cards in the Python definitions if not present
rework_proposals = {
    "ISSUE-06": "Diagnóstico: El enlace del ticket en el asistente abría un modal sin desvincular backdrops. Propuesta: Implementar openTicketDetailDirect() con unificación de backdrop y cierre reactivo en app.js.",
    "ISSUE-31": "Diagnóstico: Orden de cola en reingreso a QA no respetaba FIFO. Propuesta: Forzar tasks.push(movedTask) en triggerDemonRework y drop() en scripts/build_full_scrumban_board.py.",
    "ISSUE-34": "Diagnóstico: Falta trazabilidad de tickets precursores en base de conocimientos. Propuesta: Integrar metadata de tickets aportantes KCS v6 en backend/app/services/ai_triage.py y empty state.",
    "MEJ-11": "Diagnóstico: Ausencia de explicación de políticas de columna en cabeceras. Propuesta: Inyectar tooltips flotantes 'i' de gobernanza en las 6 columnas y erradicar emojis residuales.",
    "ISSUE-41": "Diagnóstico: Visibilidad indebida de módulos de gestión en navegación lateral. Propuesta: Forzar display: none !important permanente en index.html y bloqueo en applyRolePermissions().",
    "MEJ-12": "Diagnóstico: Falta de telemetría visual del proceso de remediación. Propuesta: Barra roja institucional (#DC2626) con cronómetro y etapas técnicas en tiempo real."
}

# Update card rendering in rework panel to display the proposed solution
old_rework_label = """            <!-- OBSERVACIONES DEL SO / BUG A CORREGIR -->"""
new_rework_block = """            <!-- PROPUESTA TÉCNICA DEL AGENTE (ISSUE-78) -->
            <div style="background: #FFFFFF; border: 1.5px solid #FBCFE8; border-radius: 5px; padding: 6px 8px; margin-bottom: 6px;">
              <div style="font-size: 9px; font-weight: 800; color: #831843; display: flex; align-items: center; gap: 4px; margin-bottom: 2px;">
                <span>🛠️</span> PROPUESTA TÉCNICA DEL AGENTE:
              </div>
              <div style="font-size: 9.5px; color: #334155; line-height: 1.35;">
                ${task.proposed_solution || 'Analizando observación para formular plan de remediación técnica...'}
              </div>
            </div>

            <!-- OBSERVACIONES DEL SO / BUG A CORREGIR -->"""

if old_rework_label in code and "PROPUESTA TÉCNICA DEL AGENTE (ISSUE-78)" not in code:
    code = code.replace(old_rework_label, new_rework_block)
    print("Updated card rework panel with Proposed Solution block!")

# Update button text to emphasize approval and execution
old_demon_btn = """>
              <span>🔥</span> Demonio
            </button>"""
new_demon_btn = """>
              <span>🔥</span> Demonio (Aprobar y Ejecutar Desarrollo)
            </button>"""
if old_demon_btn in code:
    code = code.replace(old_demon_btn, new_demon_btn)
    print("Updated Demonio button text!")

# Also ensure proposed_solution is populated for initial tasks
for tid, prop in rework_proposals.items():
    pattern = f'("id": "{tid}"[\\s\\S]*?"status": "rework"[\\s\\S]*?)(}})'
    # We can inject in JS initApp where existing is updated
init_enrich = """      // Enriquecer propuestas técnicas en tarjetas de retrabajo (ISSUE-78)
      const REWORK_PROPOSALS = {
        "ISSUE-06": "Diagnóstico: Enlace en asistente sin desvinculación de backdrops. Propuesta: openTicketDetailDirect() con backdrop unificado en app.js.",
        "ISSUE-31": "Diagnóstico: Orden de cola en reingreso a QA sin FIFO. Propuesta: Inserción estricta al final con tasks.push(movedTask).",
        "ISSUE-34": "Diagnóstico: Falta de tickets precursores en base KCS v6. Propuesta: Metadata de tickets aportantes en ai_triage.py y empty state.",
        "MEJ-11": "Diagnóstico: Ausencia de políticas de columnas en cabeceras. Propuesta: Tooltips 'i' flotantes en las 6 cabeceras y cero emojis.",
        "ISSUE-41": "Diagnóstico: Visibilidad indebida de módulos de gestión. Propuesta: display: none !important permanente en index.html y bloqueo en applyRolePermissions().",
        "MEJ-12": "Diagnóstico: Falta de telemetría de remediación. Propuesta: Barra roja institucional (#DC2626) con cronometraje en tiempo real."
      };
      tasks.forEach(t => {
        if (REWORK_PROPOSALS[t.id]) {
          t.proposed_solution = REWORK_PROPOSALS[t.id];
        }
        if (t.id === 'ISSUE-78') {
          t.status = 'progress';
          t.progress_pct = 75;
        }
      });
"""

target_init_app = '      tasks.forEach(task => {'
if target_init_app in code and "REWORK_PROPOSALS" not in code:
    code = code.replace(target_init_app, init_enrich + '\n' + target_init_app)
    print("Injected REWORK_PROPOSALS enrichment into init()!")

with open('scripts/build_full_scrumban_board.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated scripts/build_full_scrumban_board.py!")
