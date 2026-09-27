import re
import json

with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ISSUE-34 status to rework
content = re.sub(
    r'("id":\s*"ISSUE-34",\s*"title":\s*"[^"]*",\s*"epic":\s*"[^"]*",\s*"sp":\s*\d+,\s*"sprint":\s*"Sprint 6",\s*"status":\s*)"qa"',
    r'\1"rework",\n            "so_feedback": {\n                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",\n                "date": "2026-09-27",\n                "reviewer": "Freddy Cortés (Solution Owner)",\n                "notes": "ISSUE-34, no se desarrolló la solución: paso a retrabajo."\n            }',
    content
)

# 2. Update MEJ-11 status to rework
content = re.sub(
    r'("id":\s*"MEJ-11",\s*"title":\s*"[^"]*",\s*"epic":\s*"[^"]*",\s*"sp":\s*\d+,\s*"sprint":\s*"Sprint 6",\s*"status":\s*)"qa"',
    r'\1"rework",\n            "so_feedback": {\n                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",\n                "date": "2026-09-27",\n                "reviewer": "Freddy Cortés (Solution Owner)",\n                "notes": "MEJ-11 enviado a retrabajo no se desarrolló la solución."\n            }',
    content
)

# 3. Update ISSUE-41 status to rework
content = re.sub(
    r'("id":\s*"ISSUE-41",\s*"title":\s*"[^"]*",\s*"epic":\s*"[^"]*",\s*"sp":\s*\d+,\s*"sprint":\s*"Sprint 6",\s*"status":\s*)"qa"',
    r'\1"rework",\n            "so_feedback": {\n                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",\n                "date": "2026-09-27",\n                "reviewer": "Freddy Cortés (Solution Owner)",\n                "notes": "ISSUE-41 no se desarrolló la solución los botones todavía se muestran."\n            }',
    content
)

# 4. Update MEJ-12 status to rework
content = re.sub(
    r'("id":\s*"MEJ-12",\s*"title":\s*"[^"]*",\s*"epic":\s*"[^"]*",\s*"sp":\s*\d+,\s*"sprint":\s*"Sprint 6",\s*"status":\s*)"qa"',
    r'\1"rework",\n            "so_feedback": {\n                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",\n                "date": "2026-09-27",\n                "reviewer": "Freddy Cortés (Solution Owner)",\n                "notes": "MEJ-12, no se hizo el desarrollo y las capturas no son lo que te pasé, se debe corregir en este sprint."\n            }',
    content
)

# 5. Insert ISSUE-59, ISSUE-60, ISSUE-61, ISSUE-62 into extra_tasks before tasks.extend(extra_tasks)
new_tasks_code = '''        },
        {
            "id": "ISSUE-59",
            "title": "[P1 - ALTA CRITICIDAD] Restricción RBAC Perfil Analista de Soporte: Ocultamiento de 'Centro de Ayuda' y 'Mando Operativo'",
            "epic": "EP-01: Acceso, Roles y Permisos Básicos",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Frontend / RBAC & Seguridad Operativa",
            "type": "ISSUE",
            "priority": "P1",
            "business_impact": {
                "classification": "ALTO IMPACTO OPERATIVO / SEGURIDAD RBAC",
                "summary": "Evita fugas de información operacional y previene que los analistas operen fuera de sus competencias de soporte N1/N2/N3.",
                "kpi_affected": "Cumplimiento Normativo ITIL & Confidencialidad de Operaciones",
                "risk_if_delayed": "Acceso no autorizado a dashboards globales de mando y confusión de perfiles de usuario solicitante."
            },
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-59",
            "doc_title": "DOC-REQ-010 (ISSUE-59)",
            "doc_desc": "Ocultamiento categórico de Centro de Ayuda (#tab-requester-portal) y Mando Operativo (#tab-unified-hub) en la barra de navegación para analistas.",
            "attachment_image": "assets/capturas/ISSUE-59_perfil_analista_ocultar_centro_ayuda_mando_operativo.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Requerimiento Expreso Solution Owner",
                "component": "frontend/js/app.js (applyRolePermissions), frontend/index.html",
                "description": "El Solution Owner dictaminó: 'el perfil de analista no debe ver los módulos: Centro de ayuda, Mando Operativo'.",
                "root_cause": "applyRolePermissions() permitía la visibilidad de Centro de Ayuda para roles técnicos y Mando Operativo estaba habilitado por defecto.",
                "solution": "Aplicar display: none !important tanto a #tab-requester-portal como a #tab-unified-hub para roles analista/soporte y redirigir a Mesa de Ayuda.",
                "acceptance_criteria": [
                    "Escenario 1: Al iniciar sesión un analista de soporte, en el menú lateral NO figuran 'Centro de Ayuda' ni 'Mando Operativo'.",
                    "Escenario 2: El analista únicamente accede a Mesa de Ayuda, Tablero Kanban N3, Base de Conocimiento y Manual.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6."
                ]
            }
        },
        {
            "id": "ISSUE-60",
            "title": "[P1 - ALTA CRITICIDAD] Persistencia Integral y Actualización Reactiva de la Configuración de SLA Institucional en la Tarjeta 360°",
            "epic": "EP-02: Gestión de Instituciones y Multi-Tenant",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Frontend / Full-Stack & Persistencia Multi-Tenant",
            "type": "ISSUE",
            "priority": "P1",
            "business_impact": {
                "classification": "ALTO IMPACTO DE NEGOCIO / CONTINUIDAD OPERATIVA",
                "summary": "Garantiza que los acuerdos de nivel de servicio (SLAs) pactados con sanatorios y obras sociales se apliquen efectivamente a los tickets y no se pierdan al refrescar.",
                "kpi_affected": "Cumplimiento de SLA Contractual & Trazabilidad de Salud Operativa",
                "risk_if_delayed": "Pérdida de configuraciones de SLA pactadas con prestadores de salud, incumplimiento de contratos y multas regulatorias."
            },
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-60",
            "doc_title": "DOC-REQ-011 (ISSUE-60)",
            "doc_desc": "Persistencia de SLA en localStorage y backend PUT /api/v1/institutions/{code}/sla con actualización inmediata de tarjeta 360° y tabla.",
            "attachment_image": "assets/capturas/ISSUE-60_persistencia_sla_institucional_tarjeta_360.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Falla de Persistencia y Gobernanza SLA",
                "component": "frontend/js/app.js (saveZdOrgSettings, renderInstitutionsCatalog, updateInstSlaTiles), frontend/index.html",
                "description": "El Solution Owner reportó: 'la configuración de SLA no se guarda y no se actualiza en la tarjeta de la institución, issue urgente de solucionar ahora, analiza todas la capturas que te adjunto'.",
                "root_cause": "1. saveZdOrgSettings() no persistía los cambios en almacenamiento local ni backend; 2. renderInstitutionsCatalog() forzaba valores fijos ignorando inst.sla_policy; 3. Los 4 tiles P1-P4 no reaccionaban al cambio del selector; 4. Saltos de línea en contadores de pestañas.",
                "solution": "1. Persistir política en localStorage y backend; 2. Actualizar reactivamente tarjetas y tabla ejecutiva con badges de color dinámicos; 3. Implementar updateInstSlaTiles() dinámico; 4. white-space: nowrap en pestañas.",
                "acceptance_criteria": [
                    "Escenario 1: Al guardar la política de SLA de una institución, se persiste y al refrescar con F5 se mantiene inalterada.",
                    "Escenario 2: La tarjeta 360° y la tabla ejecutiva reflejan inmediatamente el nuevo SLA con su color correspondiente.",
                    "Escenario 3: Los 4 tiles de tiempos P1-P4 se recalculan en vivo al mover el dropdown.",
                    "Escenario 4: Las pestañas del modal no presentan saltos de línea antiestéticos."
                ]
            }
        },
        {
            "id": "ISSUE-61",
            "title": "[P1 - ALTA CRITICIDAD] Motor Real de Simulación de Sobrecarga y Rebalanceo Algorítmico Efectivo en Mando Operativo",
            "epic": "EP-04: Torre de Control y Asignación Automatizada",
            "sp": 5,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Full-Stack / Algoritmos de Balanceo & Mando Operativo",
            "type": "ISSUE",
            "priority": "P1",
            "business_impact": {
                "classification": "ALTO IMPACTO ASISTENCIAL / DISPONIBILIDAD TÉCNICA",
                "summary": "Permite redistribuir equitativamente la carga de miles de incidentes clínicos entre analistas activos, evitando la saturación al 100% y acelerando la resolución.",
                "kpi_affected": "Tiempo Medio de Resolución (MTTR) & Homogeneidad de Capacidad Operativa",
                "risk_if_delayed": "Colapso asistencial de analistas saturados (ej. Carlos Páez con 405 tickets) mientras otros analistas permanecen ociosos."
            },
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-61",
            "doc_title": "DOC-REQ-012 (ISSUE-61)",
            "doc_desc": "Corrección integral de los endpoints /auto-rebalance y /stress-test-imbalance para operar sobre tickets reales en curso y balancear equitativamente los analistas operativos.",
            "attachment_image": "assets/capturas/ISSUE-61_simular_sobrecarga_y_rebalancear_mando_operativo.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Requerimiento Expreso Solution Owner",
                "component": "backend/app/api/endpoints/team_leader.py, frontend/js/app.js (autoBalanceUnifiedHub, triggerStressTestScenario)",
                "description": "El Solution Owner instruyó: 'los botones de simular carga y rebalancear no funcionan, solo simulan funcionar, isssu de alta criticidad sumar al sprit actual', adjuntando captura de Carlos Páez colapsado con 405 tickets.",
                "root_cause": "1. auto-rebalance solo procesaba tickets con status ASIGNADO ignorando EN_CURSO y P1; 2. stress-test-imbalance limitaba a 240 tickets sin impactar la base real visible; 3. La tabla en frontend no reconciliaba dinámicamente con los analistas operativos principales.",
                "solution": "1. Reformular auto_rebalance_workload() para redistribuir tickets activos (ASIGNADO y EN_CURSO) entre los analistas del equipo N1, N2, N3; 2. Reformular stress_test_imbalance() para generar sobrecarga real visible; 3. Sincronizar reactivamente el Mando Operativo.",
                "acceptance_criteria": [
                    "Escenario 1: Al hacer clic en 'Simular Sobrecarga', se genera un desbalance real en la base de datos y la alerta detecta sobrecarga.",
                    "Escenario 2: Al hacer clic en 'Balancear Carga' o 'Nivelar Carga', los tickets se redistribuyen de forma efectiva y equitativa en la base de datos.",
                    "Escenario 3: La tabla de analistas refleja la nueva distribución homogénea y el banner pasa a 'Mesa de ayuda Equilibrada'."
                ]
            }
        },
        {
            "id": "ISSUE-62",
            "title": "[P1 - ALTO IMPACTO] Supresión y Ocultamiento de la Sub-Vista Confusa 'Niveles ITIL' (N1/N2/N3) en el Centro de Administración",
            "epic": "EP-02: Gestión de Instituciones y Multi-Tenant",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Frontend / UX Architecture & Simplificación",
            "type": "ISSUE",
            "priority": "P1",
            "business_impact": {
                "classification": "ALTO IMPACTO DE USABILIDAD Y CLARIDAD DE PRODUCTO",
                "summary": "Elimina interfaces abstractas y no didácticas que confunden al administrador, consolidando la gestión de SLAs en la Ficha 360° Institucional.",
                "kpi_affected": "Claridad de Experiencia de Usuario (SUS) & Eficiencia de Administración",
                "risk_if_delayed": "Confusión conceptual entre administradores hospitalarios sobre dónde se definen y aplican los SLAs reales."
            },
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-62",
            "doc_title": "DOC-REQ-013 (ISSUE-62)",
            "doc_desc": "Evaluación funcional y ocultamiento de platforms-subview-helpdesks y pestaña btn-subtab-helpdesks para mantener el foco en Instituciones, Módulos y Matriz.",
            "attachment_image": "assets/capturas/ISSUE-62_ocultar_modulo_no_didactico_niveles_itil.png",
            "issue_details": {
                "severity": "P1 — Alto Impacto / Decisión de Diseño del Solution Owner",
                "component": "frontend/index.html (#btn-subtab-helpdesks, #platforms-subview-helpdesks), frontend/js/app.js",
                "description": "El Solution Owner instruyó: 'toda este módulo no es nada didactico no se entiend para qiue está, evalua si aporta valor si es así rediseña si no ocultalo, issue de alto impacto hacer en este sprint', adjuntando captura de 'Mesas de Ayuda & Niveles de Atención ITIL'.",
                "root_cause": "Módulo con esquemas estáticos, inputs desconectados y '0 Mesas Activas' que duplicaba confusamente la parametrización de SLA institucional.",
                "solution": "Evaluación: No aporta valor operativo y genera ruido visual. Ocultar #btn-subtab-helpdesks y #platforms-subview-helpdesks, preservando las 3 vistas de alto valor: Instituciones Sanitarias, Módulos Clínicos y Matriz de Habilitación.",
                "acceptance_criteria": [
                    "Escenario 1: En la vista de Administración / Directorio de Plataformas ya NO aparece la sub-pestaña 'Niveles ITIL'.",
                    "Escenario 2: La navegación queda simplificada y enfocada en Instituciones Sanitarias, Módulos Clínicos y Matriz Institucional.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6."
                ]
            }
        }
    ]
    tasks.extend(extra_tasks)'''

if '"id": "ISSUE-59"' not in content:
    content = content.replace(
        '        }\n    ]\n    tasks.extend(extra_tasks)',
        new_tasks_code
    )

# 6. Update syncIssueInBacklog REWORK set
old_rework_block = '''        if (PERMANENTLY_APPROVED_BY_SO.has(tasks[idx].id)) {
          tasks[idx].status = 'done';
        } else if (tasks[idx].id === 'ISSUE-06') {
          // Requerimiento explícito Solution Owner: enviar ISSUE-06 a retrabajo
          tasks[idx].status = 'rework';
          tasks[idx].so_feedback = initialItem.so_feedback;
          tasks[idx].attachment_image = initialItem.attachment_image;
        } else if (!tasks[idx].status) {
          tasks[idx].status = initialItem.status || 'qa';
        }'''

new_rework_block = '''        const REWORK_SO_IDS = new Set([
          "ISSUE-06", "ISSUE-34", "MEJ-11", "ISSUE-41", "MEJ-12"
        ]);
        if (PERMANENTLY_APPROVED_BY_SO.has(tasks[idx].id)) {
          tasks[idx].status = 'done';
        } else if (REWORK_SO_IDS.has(tasks[idx].id)) {
          tasks[idx].status = 'rework';
          tasks[idx].priority = 'P1';
          if (initialItem.so_feedback) tasks[idx].so_feedback = initialItem.so_feedback;
          if (initialItem.attachment_image) tasks[idx].attachment_image = initialItem.attachment_image;
        } else if (!tasks[idx].status) {
          tasks[idx].status = initialItem.status || 'sprint';
        }'''

content = content.replace(old_rework_block, new_rework_block)

# Also ensure in init() that newly added tasks get status 'sprint' if newly introduced
old_init_push = '''        const existing = tasks.find(t => t.id === initTask.id);
        if (!existing) {
          tasks.push(JSON.parse(JSON.stringify(initTask)));
        } else {'''

new_init_push = '''        const existing = tasks.find(t => t.id === initTask.id);
        if (!existing) {
          tasks.push(JSON.parse(JSON.stringify(initTask)));
        } else {
          existing.title = initTask.title;
          existing.sprint = initTask.sprint;
          existing.sp = initTask.sp;
          existing.priority = initTask.priority;
          existing.type = initTask.type;
          existing.discipline = initTask.discipline;
          if (initTask.business_impact) existing.business_impact = initTask.business_impact;
          if (initTask.so_feedback) existing.so_feedback = initTask.so_feedback;
          if (initTask.attachment_image) existing.attachment_image = initTask.attachment_image;
          if (initTask.issue_details) existing.issue_details = initTask.issue_details;'''

content = content.replace(old_init_push, new_init_push)

with open('scripts/build_full_scrumban_board.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scripts/build_full_scrumban_board.py successfully.")
