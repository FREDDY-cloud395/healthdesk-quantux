# scripts/patch_scrumban_board.py
import re
import json

APPROVED_DONE_IDS = {
    "ISSUE-01", "ISSUE-02", "ISSUE-07", "ISSUE-08", "ISSUE-09", "ISSUE-10",
    "ISSUE-11", "ISSUE-12", "ISSUE-13", "ISSUE-14", "ISSUE-15", "ISSUE-16",
    "ISSUE-17", "ISSUE-18", "ISSUE-20", "ISSUE-21", "ISSUE-22", "ISSUE-23",
    "ISSUE-24", "ISSUE-25", "ISSUE-26", "ISSUE-27", "ISSUE-28", "ISSUE-29",
    "MEJ-01", "MEJ-02", "MEJ-03", "MEJ-04", "MEJ-05", "MEJ-06",
    "MEJ-07", "MEJ-08", "MEJ-09", "MEJ-10",
    "UH-65", "UH-68", "UH-69", "UH-70"
}

NEW_SPRINT_6_TASKS = [
    {
        "id": "ISSUE-30",
        "title": "[P1 - ALTA PRIORIDAD] Consolidación de Botón Único de Adjuntos y Gestor Dinámico de Plantillas Editables en Agent Workspace (Cero Íconos)",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Senior UX",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-30",
        "doc_title": "DOC-QA-004 (ISSUE-30)",
        "doc_desc": "Unificación de la función de adjuntos en un solo botón con diálogo de búsqueda nativo y gestor modal de plantillas con alta, edición y aplicación directa sin iconos ni emojis.",
        "attachment_image": "assets/capturas/ISSUE-30_botonera_adjuntos_plantillas.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Implementación finalizada con botón único de adjuntos nativo y modal administrativo completo de plantillas de respuesta. Cero íconos.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "ISSUE-31",
        "title": "[P1 - CRÍTICA] Botón 'Pedir Datos (Pausa SLA)' en Agent Workspace sin Errores y con Pausa Efectiva de SLA ITIL 4",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 5,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Backend SLA FSM",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-31",
        "doc_title": "DOC-QA-004 (ISSUE-31)",
        "doc_desc": "Corrección de error de ejecución al presionar 'Pedir Datos' en el Agent Workspace, transición de estado a 'En Espera del Solicitante' y detención efectiva del reloj de SLA ITIL 4.",
        "attachment_image": "assets/capturas/ISSUE-31_pedir_datos_sin_error_pausa_sla.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Falla corregida. El botón ahora solicita el requerimiento faltante, actualiza el estado a 'En Espera' y suspende el cómputo de SLA sin errores de consola.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "ISSUE-32",
        "title": "[P1 - ALTA PRIORIDAD] Acción Dual 'Responder y Resolver' en Botonera de Respuesta del Agent Workspace",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Ergonomía ITSM",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-32",
        "doc_title": "DOC-QA-004 (ISSUE-32)",
        "doc_desc": "Incorporación del botón de acción combinada 'Responder y Resolver' junto al botón 'Responder', permitiendo enviar la nota resolutiva y transicionar el ticket a Resuelto en una sola interacción.",
        "attachment_image": "assets/capturas/ISSUE-32_accion_dual_responder_y_resolver.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Botón dual incorporado en la botonera de respuesta del Workspace con confirmación rápida y cierre conforme ITIL.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "ISSUE-33",
        "title": "[P1 - ALTA PRIORIDAD] Erradicación Total de Dibujitos/Iconos no Aprobados en Telemetría, Filtros y Cabeceras de Columna",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Regla Cardinal OJO",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-33",
        "doc_title": "DOC-QA-004 (ISSUE-33)",
        "doc_desc": "Cumplimiento estricto de la directiva cardinal del Solution Owner: 'cero dibujitos, cero iconos'. Reemplazo total de emojis y dibujitos por badges tipográficos limpios y códigos monocromáticos en filtros, telemetría y cabeceras.",
        "attachment_image": "assets/capturas/ISSUE-33_cero_iconos_cero_dibujitos.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Erradicación total ejecutada en filtros avanzados, caja de telemetría y encabezados de columnas Scrumban.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "ISSUE-34",
        "title": "[P1 - ALTA PRIORIDAD] Módulo Base de Conocimiento: Trazabilidad de Tickets Aportantes (KCS v6) y Senior UX Empty State",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 5,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Backend KCS v6",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-34",
        "doc_title": "DOC-QA-004 (ISSUE-34)",
        "doc_desc": "Exhibición de tickets de soporte que alimentaron o enriquecieron el artículo de conocimiento al resolverse. Implementación de empty state Senior UX explicativo cuando el procedimiento es de referencia inicial sin tickets incidentales asociados.",
        "attachment_image": "assets/capturas/ISSUE-34_kb_tickets_aportantes_y_empty_state.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Módulo KCS v6 integrado con trazabilidad bidireccional, enlace directo a tickets y estado vacío Senior UX homologado.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "ISSUE-35",
        "title": "[P1 - ALTA PRIORIDAD] Rediseño UX Senior Estilo Quantux en Agent Workspace: Erradicación de Colores Oscuros y Fondos Negros (#0F172A)",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Senior UI Quantux",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-35",
        "doc_title": "DOC-QA-004 (ISSUE-35)",
        "doc_desc": "Sustitución de fondos oscuros (#0F172A) en badges de ID, pestañas activas, botones de resolución y avatares del Workspace por la paleta oficial Quantux Teal (#00A896, #E0F7F5, #80DFD5) y fondos luminosos conforme a las directivas del Solution Owner.",
        "attachment_image": "assets/capturas/ISSUE-35_estilo_quantux_sin_colores_oscuros.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Erradicación de fondos oscuros completada en styles.css y app.js. Toda la botonera y badges lucen ahora en paleta oficial Quantux Teal.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "ISSUE-36",
        "title": "[P1 - CRÍTICA] Blindaje de Persistencia y Gobernanza de Estados en Scrumban: Prohibición de Re-inyección de Tarjetas ya Aprobadas a En Revisión",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 5,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Arquitectura Scrumban",
        "type": "ISSUE",
        "priority": "P1",
        "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-36",
        "doc_title": "DOC-QA-004 (ISSUE-36)",
        "doc_desc": "Blindaje determinista de persistencia en el Tablero Scrumban impidiendo que recargas de página, re-sincronizaciones o resets de caché vuelvan a colocar en 'En Revisión' tarjetas que el Solution Owner ya había revisado y aceptado en 'Done'.",
        "attachment_image": "assets/capturas/media_1790477038198_en_revision_37_error.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Capa de blindaje PERMANENTLY_APPROVED_BY_SO aplicada en scripts/build_full_scrumban_board.py e init(). La columna de revisión contiene exclusivamente las tarjetas pendientes de validación.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    },
    {
        "id": "MEJ-11",
        "title": "[P1 - ALTA PRIORIDAD] Tooltips Explicativos de Gobernanza para Todos los Estados y Columnas del Tablero Scrumban (Oportunidad de Mejora)",
        "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Ergonomía Scrumban",
        "type": "MEJORA",
        "priority": "P1",
        "doc_link": "03_ARQUITECTURA_Y_DISENO_TECNICO.md#mej-11",
        "doc_title": "DOC-ARC-003 (MEJ-11)",
        "doc_desc": "Conversión de cajas explicativas estáticas en tooltips flotantes accesibles en las cabeceras de las 6 columnas del tablero Scrumban ('Desarrollo ejecutado listo para contrastar contra especificación. La aceptación formal la otorga el Solution Owner'), optimizando el espacio vertical y la densidad visual.",
        "attachment_image": "assets/capturas/MEJ-11_tooltips_explicativos_estados_scrumban.png",
        "so_feedback": {
            "status": "CORREGIDO / LISTO PARA REVISIÓN",
            "observation": "Tooltips implementados en todos los encabezados de columna. Se removieron los banners estáticos ganando altura vertical en las columnas.",
            "reviewer": "Ingeniería Quantux",
            "date": "2026-09-26"
        }
    }
]

print("Ready to patch build script.")
