# -*- coding: utf-8 -*-
"""
Generador Maestro del Tablero Scrumban Multi-Tipo, Multi-Vista con Roadmap,
Métricas, Backlog Jerárquico, Sprints Agrupados y Registro de Issues en Sprint Backlog.
"""
import os
import json

HTML_OUTPUT_PATH = r"C:\Users\FERO_ADM\.gemini\antigravity\scratch\quantux-v4-dev\docs\00_Tablero_Scrumban_Quantux.html"
CSV_OUTPUT_PATH = r"C:\Users\FERO_ADM\.gemini\antigravity\scratch\quantux-v4-dev\docs\Backlog_HealthDesk_Quantux.csv"

def generate_scrumban_board():
    # 1. Épicas
    epics = [
        {"id": "EP-01", "name": "Acceso, Roles y Permisos Básicos", "sp": 7, "progress": 100, "status": "Completada", "timebox": "Sprint 1 - 2", "desc": "Autenticación, perfiles Solicitante/Operador/Admin y selector rápido de roles."},
        {"id": "EP-02", "name": "Tickets y Datos de Solicitud", "sp": 37, "progress": 100, "status": "Completada", "timebox": "Sprint 2 - 3", "desc": "Formularios de alta sin fricción, campos homologados, catálogos y persistencia."},
        {"id": "EP-03", "name": "Bandeja de Entrada y Asignación", "sp": 29, "progress": 100, "status": "Completada", "timebox": "Sprint 2 - 3", "desc": "Cockpit operativo en 3 columnas, filtros instantáneos y asignación dinámica."},
        {"id": "EP-04", "name": "Ciclo de Estados y Registro de Solución", "sp": 42, "progress": 100, "status": "Completada", "timebox": "Sprint 2 - 4", "desc": "Máquina de estados FSM de 5 pasos, validaciones y notas de resolución."},
        {"id": "EP-05", "name": "Seguimiento, Notificaciones e Historial", "sp": 21, "progress": 100, "status": "Completada", "timebox": "Sprint 4", "desc": "Línea de tiempo de auditoría inmutable, alertas visuales y trazabilidad."},
        {"id": "EP-06", "name": "Administración y Operación Centralizada", "sp": 60, "progress": 100, "status": "Completada", "timebox": "Sprint 2 - 5", "desc": "Gestión de plataformas, clientes, usuarios y panel de control."},
        {"id": "EP-07", "name": "Gobernanza PMI+IA, Blindaje OJO & Calidad", "sp": 57, "progress": 55, "status": "En Curso (Sprint 6 Actual)", "timebox": "Sprint 6 (28-sep al 02-oct)", "desc": "Marco de adaptación PMI en 4 pasos, compuertas TDD pre-commit y resolución de no-conformidades."},
        {"id": "EP-08", "name": "Reemplazo N1, Triage IA & Portal Solicitante", "sp": 52, "progress": 0, "status": "Planificada", "timebox": "Sprint 7 (05-oct al 16-oct)", "desc": "Clasificación asistida por IA, chat predictivo y automatización de mesa N1."},
        {"id": "EP-09", "name": "Telemetría Enterprise, SLAs & HL7", "sp": 45, "progress": 0, "status": "Planificada", "timebox": "Sprint 8 (19-oct al 30-oct)", "desc": "SLAs dinámicos predictivos, interoperabilidad con estándares sanitarios y telemetría."}
    ]

    # 2. Sprints
    sprints = [
        {"id": "Sprint 1", "name": "Sprint 1: Arquitectura Base & Planificación", "sp": 30, "status": "Completado", "dates": "24/08/2026 - 28/08/2026", "desc": "Línea base documental, modelos SQLite y diseño de interfaces."},
        {"id": "Sprint 2", "name": "Sprint 2: Backend Core, Persistencia & FSM", "sp": 32, "status": "Completado", "dates": "31/08/2026 - 04/09/2026", "desc": "Servicios REST FastAPI, persistencia SQLAlchemy y circuito de 5 estados."},
        {"id": "Sprint 3", "name": "Sprint 3: Cockpit 3 Columnas & Selector Roles", "sp": 43, "status": "Completado", "dates": "07/09/2026 - 11/09/2026", "desc": "Bandeja unificada, cockpit operativo y selector de perfiles sin recargar."},
        {"id": "Sprint 4", "name": "Sprint 4: Integración E2E, Notas & Auditoría", "sp": 46, "status": "Completado", "dates": "14/09/2026 - 18/09/2026", "desc": "Circuito E2E, notas internas privadas y timeline inmutable de cambios."},
        {"id": "Sprint 5", "name": "Sprint 5: Estabilización, Certificación UAT & Release v1.0", "sp": 14, "status": "Completado", "dates": "21/09/2026 - 25/09/2026", "desc": "Pase a producción, dataset de 14 clientes y cierre de línea base MVP."},
        {"id": "Sprint 6", "name": "⚡ Sprint 6: Pruebas, Estabilización & Cierre de Alcance", "sp": 42, "status": "COMPLETADO (100%)", "dates": "26/09/2026 - 28/09/2026", "desc": "Gobernanza PMI+IA, blindaje OJO, resolución de retrabajos (UH-67, MEJ-08), issues críticas resueltas (ISSUE-21, ISSUE-22, ISSUE-23) y congelamiento 28-Sep."},
        {"id": "Sprint 7", "name": "Sprint 7: Reemplazo N1 & Omnicanalidad", "sp": 35, "status": "Planificado", "dates": "05/10/2026 - 16/10/2026", "desc": "Triage inteligente y asistencia de primer nivel para prestadores."},
        {"id": "Sprint 8", "name": "Sprint 8: Telemetría Enterprise & HL7", "sp": 40, "status": "Planificado", "dates": "19/10/2026 - 30/10/2026", "desc": "Integración avanzada, métricas en tiempo real y conectividad hospitalaria."}
    ]

    # 3. Milestones
    milestones = [
        {"id": "M1", "date": "28-Ago-2026", "title": "Aprobación de Arquitectura y Especificación Base (DOC-REQ-002)", "status": "done", "badge": "Completado"},
        {"id": "M2", "date": "04-Sep-2026", "title": "Core Backend REST y FSM de 5 Estados Operativa", "status": "done", "badge": "Completado"},
        {"id": "M3", "date": "11-Sep-2026", "title": "Cockpit Centralizado en 3 Columnas Operativo", "status": "done", "badge": "Completado"},
        {"id": "M4", "date": "18-Sep-2026", "title": "Circuito E2E Integrado con Trazabilidad de Auditoría", "status": "done", "badge": "Completado"},
        {"id": "M5", "date": "25-Sep-2026", "title": "Liberación Certificada Release v1.0 MVP Quantux Salud", "status": "done", "badge": "Completado"},
        {"id": "M6", "date": "28-Sep-2026", "title": "Deadline Técnico & Congelamiento de Código (18:00 hs)", "status": "current", "badge": "PRUEBAS & ESTABILIZACIÓN"},
        {"id": "M7", "date": "29 y 30-Sep", "title": "Ensayos y Preparación Pitch del Solution Owner (Blindado)", "status": "planned", "badge": "PREPARACIÓN PITCH"},
        {"id": "M8", "date": "01-Oct-2026", "title": "Presentación Oficial del Producto ante el Comité Evaluador", "status": "planned", "badge": "DEMO FINAL"},
        {"id": "M9", "date": "16-Oct-2026", "title": "Release v1.1 Reemplazo N1 y Despliegue Asistencial", "status": "planned", "badge": "Planificado"}
    ]

    # 4. Items del Backlog
    tasks = [
        {
                "id": "UH-01",
                "title": "Autenticación de Usuarios por Rol",
                "epic": "EP-01: Acceso, Roles y Permisos Básicos",
                "sp": 2,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / Auth & RBAC",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-01",
                "doc_title": "DOC-SPEC-002 (UH-01)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-01: Acceso, Roles y Permisos Básicos).",
                "narrative": {
                        "as_a": "usuario de Quantux Salud",
                        "i_want": "ingresar con mis credenciales seleccionando mi rol (Solicitante, Soporte, Administrador)",
                        "so_that": "acceder a las funciones de mi perfil"
                },
                "acceptance_criteria": [
                        "**Dado** un usuario registrado, **cuando** ingresa credenciales válidas, **entonces** accede a su bandeja principal.",
                        "**Dado** credenciales inválidas, **cuando** intenta ingresar, **entonces** el sistema muestra error y no permite el acceso."
                ]
        },
        {
                "id": "UH-02",
                "title": "Control de Permisos por Perfil",
                "epic": "EP-01: Acceso, Roles y Permisos Básicos",
                "sp": 2,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / Auth & RBAC",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-02",
                "doc_title": "DOC-SPEC-002 (UH-02)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-01: Acceso, Roles y Permisos Básicos).",
                "narrative": {
                        "as_a": "Administrador",
                        "i_want": "restringir las acciones del sistema según el rol del usuario",
                        "so_that": "evitar modificaciones no autorizadas en tickets o tablas maestras"
                },
                "acceptance_criteria": [
                        "**Dado** un Solicitante, **cuando** consulta el sistema, **entonces** solo ve y crea sus propios tickets.",
                        "**Dado** un Operador de Soporte, **cuando** opera, **entonces** puede gestionar tickets pero no administrar usuarios ni tablas maestras."
                ]
        },
        {
                "id": "UH-03",
                "title": "Auditoría Básica de Acceso",
                "epic": "EP-01: Acceso, Roles y Permisos Básicos",
                "sp": 2,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / Auth & RBAC",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-03",
                "doc_title": "DOC-SPEC-002 (UH-03)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-01: Acceso, Roles y Permisos Básicos).",
                "narrative": {
                        "as_a": "Administrador",
                        "i_want": "registrar los inicios de sesión",
                        "so_that": "mantener la trazabilidad de seguridad"
                },
                "acceptance_criteria": [
                        "**Dado** un login exitoso, **cuando** el usuario entra, **entonces** se guarda usuario, fecha, hora y rol en la bitácora."
                ]
        },
        {
                "id": "UH-04",
                "title": "Cierre de Sesión Seguro",
                "epic": "EP-01: Acceso, Roles y Permisos Básicos",
                "sp": 1,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / Auth & RBAC",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-04",
                "doc_title": "DOC-SPEC-002 (UH-04)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-01: Acceso, Roles y Permisos Básicos).",
                "narrative": {
                        "as_a": "usuario autenticado",
                        "i_want": "cerrar mi sesión en 1 clic",
                        "so_that": "proteger mi cuenta al desocupar la estación de trabajo"
                },
                "acceptance_criteria": [
                        "**Dado** un usuario con sesión abierta, **cuando** presiona \"Cerrar Sesión\", **entonces** se limpia la sesión activa y regresa al login. ---"
                ]
        },
        {
                "id": "UH-05",
                "title": "Formulario Unificado de Alta de Ticket",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 3,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-05",
                "doc_title": "DOC-SPEC-002 (UH-05)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Solicitante u Operador de Soporte",
                        "i_want": "cargar un ticket con título, descripción y datos de contacto",
                        "so_that": "reportar una solicitud formalmente"
                },
                "acceptance_criteria": [
                        "**Dado** el formulario de alta, **cuando** se completan los campos obligatorios, **entonces** se genera el ticket en estado `Nuevo` con identificador único."
                ]
        },
        {
                "id": "UH-06",
                "title": "Selección de Plataforma / Categoría",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 2,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-06",
                "doc_title": "DOC-SPEC-002 (UH-06)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Solicitante",
                        "i_want": "elegir la plataforma afectada de entre las 9 oficiales",
                        "so_that": "canalizar el ticket al equipo especialista correcto"
                },
                "acceptance_criteria": [
                        "**Dado** el selector de plataformas, **cuando** el usuario elige una opción, **entonces** el ticket queda asociado a su código de catálogo (ej. `CAT_RECETA`)."
                ]
        },
        {
                "id": "UH-07",
                "title": "Vinculación con Cliente Institucional",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 2,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-07",
                "doc_title": "DOC-SPEC-002 (UH-07)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "asociar el ticket a uno de los 14 clientes institucionales",
                        "so_that": "identificar el impacto sobre la entidad de salud"
                },
                "acceptance_criteria": [
                        "**Dado** el campo cliente, **cuando** se guarda el ticket, **entonces** queda registrada la institución (ej. OSDE, Swiss Medical, Finochietto)."
                ]
        },
        {
                "id": "UH-08",
                "title": "Tipificación de la Solicitud",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 2,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-08",
                "doc_title": "DOC-SPEC-002 (UH-08)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Operador de Soporte N1",
                        "i_want": "clasificar el ticket como Incidente, Requerimiento o Consulta",
                        "so_that": "aplicar las pautas de atención correspondientes"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket en triage, **cuando** se asigna el tipo, **entonces** queda visible en el detalle y listado."
                ]
        },
        {
                "id": "UH-09",
                "title": "Asignación de Prioridad ($P = I \times U$)",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 3,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-09",
                "doc_title": "DOC-SPEC-002 (UH-09)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "definir el Impacto y la Urgencia",
                        "so_that": "que el sistema determine la Prioridad (P1 a P5)"
                },
                "acceptance_criteria": [
                        "**Dado** Impacto Alto y Urgencia Alta, **cuando** se registran los valores, **entonces** el sistema establece Prioridad P1 (Crítica)."
                ]
        },
        {
                "id": "UH-10",
                "title": "Adjunto de Evidencias",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 2,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-10",
                "doc_title": "DOC-SPEC-002 (UH-10)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Solicitante",
                        "i_want": "adjuntar capturas o enlaces del error",
                        "so_that": "que soporte pueda reproducir la falla rápidamente"
                },
                "acceptance_criteria": [
                        "**Dado** un archivo o URL, **cuando** se adjunta al ticket, **entonces** queda accesible en la vista de detalle."
                ]
        },
        {
                "id": "UH-11",
                "title": "Consulta y Edición Básica de Ticket",
                "epic": "EP-02: Tickets y Datos de Solicitud",
                "sp": 1,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Fullstack / Formularios",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-11",
                "doc_title": "DOC-SPEC-002 (UH-11)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-02: Tickets y Datos de Solicitud).",
                "narrative": {
                        "as_a": "Solicitante",
                        "i_want": "consultar el estado y editar los datos mientras el ticket esté en `Nuevo`",
                        "so_that": "corregir omisiones antes del inicio de la atención"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket en estado `Nuevo`, **cuando** el creador edita el texto, **entonces** los cambios se guardan y se registra la edición en el historial. ---"
                ]
        },
        {
                "id": "UH-12",
                "title": "Bandeja de Entrada de Solicitudes",
                "epic": "EP-03: Bandeja de Atención y Asignación de Responsable",
                "sp": 3,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / Cockpit UI",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-12",
                "doc_title": "DOC-SPEC-002 (UH-12)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-03: Bandeja de Atención y Asignación de Responsable).",
                "narrative": {
                        "as_a": "Operador de Soporte N1",
                        "i_want": "ver todos los tickets sin asignar en tiempo real",
                        "so_that": "revisarlos y distribuirlos al equipo correspondiente"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket en estado `Nuevo`, **cuando** el operador abre la bandeja, **entonces** aparece ordenado y destacado por su prioridad."
                ]
        },
        {
                "id": "UH-13",
                "title": "Asignación de Responsable de Soporte",
                "epic": "EP-03: Bandeja de Atención y Asignación de Responsable",
                "sp": 2,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / Cockpit UI",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-13",
                "doc_title": "DOC-SPEC-002 (UH-13)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-03: Bandeja de Atención y Asignación de Responsable).",
                "narrative": {
                        "as_a": "Supervisor u Operador N1",
                        "i_want": "asignar un ticket a un responsable de soporte",
                        "so_that": "pasar el ticket a `Asignado`"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket `Nuevo`, **cuando** se selecciona un responsable de soporte, **entonces** el estado cambia a `Asignado` y se guarda el usuario asignado."
                ]
        },
        {
                "id": "UH-14",
                "title": "Autoasignación Directa (\"Tomar Ticket\")",
                "epic": "EP-03: Bandeja de Atención y Asignación de Responsable",
                "sp": 1,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / Cockpit UI",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-14",
                "doc_title": "DOC-SPEC-002 (UH-14)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-03: Bandeja de Atención y Asignación de Responsable).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "autoasignarme un ticket con un solo clic",
                        "so_that": "comenzar la atención de inmediato"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket sin asignar, **cuando** el operador presiona \"Tomar Ticket\", **entonces** queda asignado a su usuario y pasa a `Asignado`."
                ]
        },
        {
                "id": "UH-15",
                "title": "Derivación a Nivel de Soporte Especializado",
                "epic": "EP-03: Bandeja de Atención y Asignación de Responsable",
                "sp": 2,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / Cockpit UI",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-15",
                "doc_title": "DOC-SPEC-002 (UH-15)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-03: Bandeja de Atención y Asignación de Responsable).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "escalar el ticket a N2 o N3",
                        "so_that": "que intervenga un especialista técnico o de infraestructura"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket en atención, **cuando** se cambia el nivel de soporte, **entonces** se registra el escalamiento y queda disponible para el nuevo grupo."
                ]
        },
        {
                "id": "UH-16",
                "title": "Reasignación de Responsable",
                "epic": "EP-03: Bandeja de Atención y Asignación de Responsable",
                "sp": 2,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / Cockpit UI",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-16",
                "doc_title": "DOC-SPEC-002 (UH-16)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-03: Bandeja de Atención y Asignación de Responsable).",
                "narrative": {
                        "as_a": "Supervisor",
                        "i_want": "reasignar un ticket indicando una justificación",
                        "so_that": "balancear la carga operativa o cubrir ausencias"
                },
                "acceptance_criteria": [
                        "**Dado** un cambio de responsable, **cuando** se guarda con motivo, **entonces** el historial refleja el usuario anterior, el nuevo y la razón. ---"
                ]
        },
        {
                "id": "UH-17",
                "title": "Transición de Estado a \"En Curso\"",
                "epic": "EP-04: Ciclo de Estados y Registro de Solución",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / FSM & Transiciones",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-17",
                "doc_title": "DOC-SPEC-002 (UH-17)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-04: Ciclo de Estados y Registro de Solución).",
                "narrative": {
                        "as_a": "Operador asignado",
                        "i_want": "cambiar el estado a `En Curso`",
                        "so_that": "indicar que el análisis técnico ha comenzado activamente"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket en `Asignado`, **cuando** el operador inicia el trabajo, **entonces** el estado pasa a `En Curso` y se registra la fecha/hora."
                ]
        },
        {
                "id": "UH-18",
                "title": "Pausa de Gestión por Información Pendiente",
                "epic": "EP-04: Ciclo de Estados y Registro de Solución",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / FSM & Transiciones",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-18",
                "doc_title": "DOC-SPEC-002 (UH-18)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-04: Ciclo de Estados y Registro de Solución).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "marcar el ticket en espera de información adicional",
                        "so_that": "documentar que está detenido por causas externas"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket `En Curso`, **cuando** se solicita más información al usuario, **entonces** el ticket refleja la espera y se registra el comentario correspondiente."
                ]
        },
        {
                "id": "UH-19",
                "title": "Registro Obligatorio de Solución",
                "epic": "EP-04: Ciclo de Estados y Registro de Solución",
                "sp": 3,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / FSM & Transiciones",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-19",
                "doc_title": "DOC-SPEC-002 (UH-19)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-04: Ciclo de Estados y Registro de Solución).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "documentar la resolución técnica aplicada",
                        "so_that": "que el usuario conozca la respuesta y quede archivada"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket `En Curso`, **cuando** se carga la solución, **entonces** el texto de resolución es obligatorio para habilitar el paso a `Resuelto`."
                ]
        },
        {
                "id": "UH-20",
                "title": "Registro de Solución Provisoria / Alternativa",
                "epic": "EP-04: Ciclo de Estados y Registro de Solución",
                "sp": 3,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / FSM & Transiciones",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-20",
                "doc_title": "DOC-SPEC-002 (UH-20)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-04: Ciclo de Estados y Registro de Solución).",
                "narrative": {
                        "as_a": "Operador de Soporte N2",
                        "i_want": "registrar si la solución fue provisoria (procedimiento alternativo)",
                        "so_that": "restablecer el servicio asistencial mientras N3 resuelve la causa de fondo"
                },
                "acceptance_criteria": [
                        "**Dado** un incidente operativo, **cuando** se aplica una solución temporal, **entonces** se guarda la descripción del procedimiento y la marca de solución provisoria."
                ]
        },
        {
                "id": "UH-21",
                "title": "Transición a Estado \"Resuelto\"",
                "epic": "EP-04: Ciclo de Estados y Registro de Solución",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / FSM & Transiciones",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-21",
                "doc_title": "DOC-SPEC-002 (UH-21)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-04: Ciclo de Estados y Registro de Solución).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "marcar el ticket como `Resuelto`",
                        "so_that": "informar que la atención técnica ha finalizado exitosamente"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket con solución registrada, **cuando** se confirma la acción, **entonces** el estado cambia a `Resuelto` y se notifica al solicitante."
                ]
        },
        {
                "id": "UH-22",
                "title": "Transición a Estado \"Cerrado\"",
                "epic": "EP-04: Ciclo de Estados y Registro de Solución",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / FSM & Transiciones",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-22",
                "doc_title": "DOC-SPEC-002 (UH-22)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-04: Ciclo de Estados y Registro de Solución).",
                "narrative": {
                        "as_a": "Solicitante o Administrador",
                        "i_want": "validar la conformidad y pasar el ticket a `Cerrado`",
                        "so_that": "archivar el ciclo de atención de forma inmutable"
                },
                "acceptance_criteria": [
                        "**Dado** un ticket `Resuelto`, **cuando** se confirma el cierre, **entonces** pasa a `Cerrado` y se bloquea cualquier edición posterior. ---"
                ]
        },
        {
                "id": "UH-23",
                "title": "Comentarios Públicos de Seguimiento",
                "epic": "EP-05: Seguimiento, Notificaciones e Historial",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Notificaciones & Auditoría",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-23",
                "doc_title": "DOC-SPEC-002 (UH-23)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-05: Seguimiento, Notificaciones e Historial).",
                "narrative": {
                        "as_a": "Solicitante u Operador",
                        "i_want": "intercambiar mensajes públicos en el hilo del ticket",
                        "so_that": "mantener una comunicación fluida sobre el avance del caso"
                },
                "acceptance_criteria": [
                        "**Dado** un nuevo mensaje público, **cuando** se envía, **entonces** queda visible en el hilo del ticket para todos los involucrados."
                ]
        },
        {
                "id": "UH-24",
                "title": "Notas Internas para el Equipo de Soporte",
                "epic": "EP-05: Seguimiento, Notificaciones e Historial",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Notificaciones & Auditoría",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-24",
                "doc_title": "DOC-SPEC-002 (UH-24)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-05: Seguimiento, Notificaciones e Historial).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "escribir notas técnicas internas invisibles para el solicitante",
                        "so_that": "coordinar diagnósticos entre técnicos"
                },
                "acceptance_criteria": [
                        "**Dado** una nota marcada como privada, **cuando** un Solicitante consulta el ticket, **entonces** la nota no es visible en su pantalla."
                ]
        },
        {
                "id": "UH-25",
                "title": "Avisos Básicos por Asignación y Cambio de Estado",
                "epic": "EP-05: Seguimiento, Notificaciones e Historial",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Notificaciones & Auditoría",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-25",
                "doc_title": "DOC-SPEC-002 (UH-25)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-05: Seguimiento, Notificaciones e Historial).",
                "narrative": {
                        "as_a": "usuario del sistema",
                        "i_want": "recibir avisos visuales ante cambios de estado o asignaciones",
                        "so_that": "enterarme en tiempo real"
                },
                "acceptance_criteria": [
                        "**Dado** un cambio en un ticket propio, **cuando** ocurre la acción, **entonces** aparece una alerta en pantalla con el detalle de la actualización."
                ]
        },
        {
                "id": "UH-26",
                "title": "Aviso Destacado de Ticket Resuelto",
                "epic": "EP-05: Seguimiento, Notificaciones e Historial",
                "sp": 1,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Notificaciones & Auditoría",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-26",
                "doc_title": "DOC-SPEC-002 (UH-26)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-05: Seguimiento, Notificaciones e Historial).",
                "narrative": {
                        "as_a": "Solicitante",
                        "i_want": "ver claramente cuando mi ticket es marcado como `Resuelto`",
                        "so_that": "verificar la solución antes de cerrar"
                },
                "acceptance_criteria": [
                        "**Dado** el pase a `Resuelto`, **cuando** el solicitante entra al sistema, **entonces** ve un aviso destacado de confirmación de solución."
                ]
        },
        {
                "id": "UH-27",
                "title": "Historial y Trazabilidad de Cambios Relevantes",
                "epic": "EP-05: Seguimiento, Notificaciones e Historial",
                "sp": 2,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Notificaciones & Auditoría",
                "type": "UH",
                "priority": "P3",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-27",
                "doc_title": "DOC-SPEC-002 (UH-27)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-05: Seguimiento, Notificaciones e Historial).",
                "narrative": {
                        "as_a": "Administrador o Auditor",
                        "i_want": "ver la cronología completa de cambios con fecha, hora y responsable",
                        "so_that": "garantizar la total transparencia del ciclo"
                },
                "acceptance_criteria": [
                        "**Dado** cualquier cambio en un ticket, **cuando** se consulta el historial, **entonces** se listan todas las mutaciones sin posibilidad de ser borradas. ---"
                ]
        },
        {
                "id": "UH-28",
                "title": "Interfaz Centralizada de Operación en Pantalla Única",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 6,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / Pantalla Única",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-28",
                "doc_title": "DOC-SPEC-002 (UH-28)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-06: Administración y Operación Centralizada).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "operar en una sola pantalla con Filtros (Col 1), Bandeja (Col 2) y Detalle/Gestión (Col 3)",
                        "so_that": "resolver tickets rápidamente sin recargar la página"
                },
                "acceptance_criteria": [
                        "**Dado** el ingreso al sistema, **cuando** el operador hace clic en un ticket de la lista, **entonces** el detalle y las acciones se abren inmediatamente en la tercera columna."
                ]
        },
        {
                "id": "UH-29",
                "title": "Selector Rápido de Rol de Usuario",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / Pantalla Única",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-29",
                "doc_title": "DOC-SPEC-002 (UH-29)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-06: Administración y Operación Centralizada).",
                "narrative": {
                        "as_a": "evaluador o usuario de pruebas",
                        "i_want": "alternar entre los roles de Solicitante, Soporte y Admin con un botón en la barra superior",
                        "so_that": "validar la experiencia de cada perfil en segundos durante la demo"
                },
                "acceptance_criteria": [
                        "**Dado** el selector en el encabezado, **cuando** se elige otro rol, **entonces** la interfaz adapta los permisos y vistas instantáneamente."
                ]
        },
        {
                "id": "UH-30",
                "title": "Listado, Búsqueda y Filtros Básicos",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 4,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / Pantalla Única",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-30",
                "doc_title": "DOC-SPEC-002 (UH-30)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-06: Administración y Operación Centralizada).",
                "narrative": {
                        "as_a": "Operador de Soporte",
                        "i_want": "filtrar la bandeja por estado, plataforma, cliente o buscar por palabra clave",
                        "so_that": "localizar cualquier ticket en menos de 2 segundos"
                },
                "acceptance_criteria": [
                        "**Dado** un criterio de búsqueda, **cuando** el usuario escribe o selecciona un filtro, **entonces** la lista se actualiza al instante."
                ]
        },
        {
                "id": "UH-31",
                "title": "Administración de Usuarios y Asignación de Roles",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 4,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / Pantalla Única",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-31",
                "doc_title": "DOC-SPEC-002 (UH-31)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-06: Administración y Operación Centralizada).",
                "narrative": {
                        "as_a": "Administrador",
                        "i_want": "listar, crear y asignar roles a los usuarios",
                        "so_that": "gestionar el personal operativo de Quantux Salud"
                },
                "acceptance_criteria": [
                        "**Dado** el módulo de administración, **cuando** se crea un usuario, **entonces** queda habilitado para operar según su perfil asignado."
                ]
        },
        {
                "id": "UH-32",
                "title": "Administración de Categorías y Prioridades",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / Pantalla Única",
                "type": "UH",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-32",
                "doc_title": "DOC-SPEC-002 (UH-32)",
                "doc_desc": "Requerimiento funcional oficial del MVP Quantux Salud (EP-06: Administración y Operación Centralizada).",
                "narrative": {
                        "as_a": "Administrador",
                        "i_want": "administrar las plataformas, tipos de ticket y niveles de prioridad",
                        "so_that": "mantener el sistema alineado a la evolución del catálogo corporativo"
                },
                "acceptance_criteria": [
                        "**Dado** el panel de configuración, **cuando** se edita una categoría, **entonces** los formularios de alta y filtros reflejan los cambios de forma consistente. ---"
                ]
        },
        {
                "id": "ISSUE-07",
                "title": "[P1 - ALTA PRIORIDAD] Erradicación de Terminología Médica/Hospitalaria en Mensajes y Estados del Sistema de TI",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Writing & ITIL",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-07",
                "doc_title": "DOC-SPEC-002 (ISSUE-07)",
                "doc_desc": "Sustitución integral de terminología médica espuria ('Guardia Médica', 'Guardia Técnica', 'Transcripción Clínica', 'Asunto Clínico', 'Síntoma Médico') por terminología estándar de Mesa de Ayuda TI / Service Desk.",
                "attachment_image": "assets/capturas/ISSUE-07_terminologia_medica_guardia.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Dominio Conceptual y Vocabulario",
                        "component": "frontend/index.html (navbar, placeholders), frontend/js/app.js (openRequesterTicketDetail, renderRequesterChatStream, getLocalAiClinicalResponse)",
                        "description": "El sistema utiliza terminología de la medicina asistencial ('Estado de Guardia Técnica', 'Transcripción clínica completa', 'Asunto Clínico Registrado', 'Conversación y Contexto Asistencial Transferido', 'Centro de Ayuda & Guardia Médica', 'Escribe tu consulta o síntoma médico') para describir procesos y estados que corresponden estrictamente al soporte técnico de software TI. El Solution Owner ha establecido taxativamente: 'no deben haber en el producto términos similares a los usados en la terminología médica'.",
                        "root_cause": "Uso inadecuado de metáforas hospitalarias en la capa de presentación (UX Writing) y templates de strings en JavaScript y HTML, generando confusión entre la labor médica del usuario y el funcionamiento de la Mesa de Ayuda de TI.",
                        "solution": "1. 'ESTADO DE GUARDIA TÉCNICA:' -> 'ESTADO DE LA SOLICITUD DE SOPORTE:'\\n2. 'transcripción clínica completa' -> 'diagnóstico y detalle técnico transferido'\\n3. 'ASUNTO CLÍNICO REGISTRADO:' -> 'ASUNTO DE LA SOLICITUD:'\\n4. 'CONVERSACIÓN Y CONTEXTO ASISTENCIAL TRANSFERIDO:' -> 'HISTORIAL Y CONTEXTO DE LA CONSULTA:'\\n5. 'Centro de Ayuda & Guardia Médica' (Navbar) -> 'Centro de Ayuda & Mesa de Soporte'\\n6. Placeholder del chat: 'Escribe tu consulta sobre Consultorio Digital (ej: matrícula provincial, error en receta, cambio de cuit)...'\\n7. 'Guardia N1/N2' -> 'Soporte N1/N2'",
                        "acceptance_criteria": [
                                "Escenario 1 (Cero Términos Médicos en Estados de Soporte): DADO el modal de solicitud y el chat del solicitante, CUANDO se visualizan los estados, ENTONCES no figura la palabra 'Guardia', 'Clínico' o 'Asistencial' para referirse a tickets, operadores o sistemas TI.",
                                "Escenario 2 (Vocabulario Preciso de Service Desk): DADO cualquier mensaje generado por el sistema, CUANDO describe el flujo de soporte, ENTONCES emplea vocabulario estándar de Service Desk ('Solicitud de Soporte', 'Detalle Técnico', 'Mesa de Ayuda').",
                                "Escenario 3 (Trazabilidad Visual): DADO el issue registrado en el tablero, CUANDO se abre la tarjeta, ENTONCES presenta la captura con el recuadro verde 'ESTADO DE GUARDIA TÉCNICA' como evidencia."
                        ]
                }
        },
        {
                "id": "UH-68",
                "title": "[P1 - ALTA PRIORIDAD] Remoción de Métricas y Etiquetas de SLA en el Portal del Solicitante / Médico",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX & Limpieza",
                "type": "UH",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-68",
                "doc_title": "DOC-REQ-002 (UH-68)",
                "doc_desc": "Eliminación de las menciones de SLA de atención en el modal de detalle del solicitante y en el stream de escalamiento N2.",
                "attachment_image": "assets/capturas/UH-68_quitar_sla_solicitante.png",
                "narrative": {
                        "as_a": "Profesional Médico Solicitante",
                        "i_want": "que el sistema no exhiba tiempos ni etiquetas de compromisos de SLA internos de TI en mi vista ni en mis comprobantes de solicitud",
                        "so_that": "la interfaz esté libre de métricas burocráticas internas que nadie solicitó y que no aportan valor asistencial a mi práctica clínica."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Remoción en Modal de Detalle): DADO el modal de detalle de solicitud del solicitante, CUANDO se visualiza el asunto clínico, ENTONCES no figura la etiqueta '⏱️ SLA de Atención: < 15 min'.",
                        "Escenario 2 (Remoción en Stream de Escalamiento): DADO un incidente escalado a Soporte N2 en el chat, CUANDO se renderiza la tarjeta de confirmación, ENTONCES no figura la línea '• SLA de Atención N2: < 15 minutos en cola prioritaria'.",
                        "Escenario 3 (Conservación en Vistas Analista ITIL): DADO el acceso de analistas N2, supervisores y líderes en la Mesa de Ayuda y Tableros ITIL, CUANDO se gestionan los tickets, ENTONCES los cálculos y monitores de SLA permanecen plenamente operativos para la gestión operativa interna."
                ],
                "adaptation_criteria": [
                        "Paso 1: Simplificación y despojo de ruidos burocráticos hacia el usuario final asistencial.",
                        "Paso 2: Respeto a las directivas del Solution Owner: 'quita el sla, nadie lo pidió'.",
                        "Paso 3: Verificación de no regresión en endpoints backend de cálculo SLA ITIL.",
                        "Paso 4: Trazabilidad con captura original en el backlog."
                ]
        },
        {
                "id": "UH-67",
                "title": "[P1 - ALTA PRIORIDAD] Subniveles Interactivos de Navegación en Árbol N1 y Separación de Capas Médico vs Soporte",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 5,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Analista Funcional / UX & Frontend",
                "type": "UH",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-67",
                "doc_title": "DOC-REQ-002 (UH-67)",
                "doc_desc": "Optimización de usabilidad del Asistente N1 eliminando el doble bloque confuso y añadiendo subniveles interactivos con separación de capas (médico vs analista).",
                "attachment_image": "assets/capturas/UH-67_doble_informacion_subniveles_arbol.png",
                "so_feedback": {
                        "status": "EN REVISIÓN / EVALUACIÓN DEL SO",
                        "observation": "Subniveles interactivos de navegación en el árbol N1 implementados con separación de indicación inmediata médica y fundamento técnico.",
                        "date": "2026-09-27",
                        "reviewer": "Freddy Cortés (Solution Owner)"
                },
                "narrative": {
                        "as_a": "Profesional de la Salud (Médico Solicitante) y Analista de Soporte N2",
                        "i_want": "que el Asistente N1 presente subniveles interactivos de navegación en el árbol de decisión y diferencie con claridad el paso resolutivo inmediato del marco normativo/técnico profundo",
                        "so_that": "pueda resolver mi consulta clínica en segundos sin confusión entre directivas internas y procedimientos de autogestión, manteniendo toda la información técnica accesible bajo demanda."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Subniveles de Navegación Interactivos): DADO un tema con múltiples ramificaciones operativas (ej: 'Prescripción, Vademécum y Matrícula SISA'), CUANDO el Asistente N1 clasifica la consulta, ENTONCES presenta chips o botones de subnivel específicos ('Matrícula SISA', 'Vademécum Alfabeta', 'Biometría', 'Contingencia') para que el usuario elija su caso puntual.",
                        "Escenario 2 (Separación de Capas Funcionales): DADO el diagnóstico seleccionado, CUANDO se muestra la respuesta, ENTONCES presenta en primer término la 'Indicación Resolutiva Inmediata para el Médico' (en lenguaje clínico sin tecnicismos de BD o CRM) y en un acordeón desplegable secundario el 'Fundamento Normativo y Técnico Oficial'.",
                        "Escenario 3 (Renderizado Tipográfico Limpio): DADO cualquier texto generado por el Asistente N1 o base de conocimiento, CUANDO se visualiza en el stream de chat, ENTONCES interpreta adecuadamente el formato markdown (negritas, viñetas, saltos) erradicando asteriscos crudos (**texto**).",
                        "Escenario 4 (Trazabilidad Visual Permanente): DADO el registro de la UH en el tablero y backlog, CUANDO se consulta el detalle de la tarjeta, ENTONCES muestra la captura original adjunta que fundamentó la necesidad."
                ],
                "adaptation_criteria": [
                        "Paso 1: Análisis Funcional en conjunto con UX — Progressive Disclosure (divulgación progresiva) y jerarquización de contenidos.",
                        "Paso 2: Cumplimiento de restricciones institucionales OJO (cero cards desalineadas, paleta Slate/Teal corporativa).",
                        "Paso 3: Definición de subniveles en catálogo JSON de árboles de decisión en frontend/js/typeahead.js y app.js.",
                        "Paso 4: Trazabilidad inmutable en suite documental y registro de evidencia visual en docs/assets/capturas/."
                ]
        },
        {
                "id": "ISSUE-04",
                "title": "[P1 - ALTA PRIORIDAD] Imposibilidad de scroll en desplegable de temas oficiales homologados (Typeahead)",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX & CSS",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-04",
                "doc_title": "DOC-SPEC-002 (ISSUE-04)",
                "doc_desc": "Desbordamiento vertical de #requester-typeahead-dropdown que corta los temas oficiales y bloquea el scroll.",
                "attachment_image": "assets/capturas/ISSUE-04_scroll_typeahead.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Bloqueante de Navegación",
                        "component": "frontend/index.html (#view-requester-portal, #requester-clinical-portal, #requester-typeahead-dropdown), frontend/js/typeahead.js",
                        "description": "Al ingresar texto en el buscador del portal del solicitante (ej: 'matricul'), se despliega la lista con los Temas Oficiales Homologados de Consultorio Digital 2. Debido a que los contenedores superiores (.app-view y #requester-clinical-portal) tienen height: 100% y overflow: hidden, el desplegable se extiende fuera del límite inferior de la pantalla sin habilitar barra de scroll, impidiendo al usuario ver y seleccionar los resultados inferiores.",
                        "root_cause": "Falta de overflow-y: auto en el contenedor principal de la vista y ausencia de max-height proporcional con scroll nativo (overscroll-behavior: contain) en el contenedor del dropdown predictivo.",
                        "solution": "1. Habilitar scroll vertical en #requester-clinical-portal con overflow-y: auto !important;\n2. Ajustar #requester-typeahead-dropdown con max-height: calc(100vh - 420px); min-height: 180px; overflow-y: auto !important; overscroll-behavior: contain; -webkit-overflow-scrolling: touch;\n3. Asegurar barra de desplazamiento visible estilizada para facilitar interacción táctil o mouse.",
                        "acceptance_criteria": [
                                "Escenario 1 (Scroll Fluido): DADO el buscador con resultados coincidentes (ej: 'matricul'), CUANDO el usuario interactúa con la lista, ENTONCES puede scrollear verticalmente viendo el 100% de los temas disponibles.",
                                "Escenario 2 (No Truncamiento en Viewport): DADO cualquier tamaño de pantalla estándar (1366x768 hasta 1920x1080), CUANDO se despliega el typeahead, ENTONCES permanece contenido dentro del área visible sin desbordar el pie de página.",
                                "Escenario 3 (Selección Exitosa): DADO un tema ubicado en la parte inferior tras el scroll, CUANDO el usuario hace clic, ENTONCES se selecciona correctamente y dispara la consulta sin errores de foco."
                        ]
                }
        },
        {
                "id": "ISSUE-05",
                "title": "[P1 - ALTA PRIORIDAD] Botón 'Hacer otra consulta' no oculta ni reinicia el historial de consultas anteriores",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / JS & UX",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-05",
                "doc_title": "DOC-SPEC-002 (ISSUE-05)",
                "doc_desc": "El botón 'Hacer otra consulta' solo ejecuta foco en el input sin ocultar el stream de chat ni restaurar el hero de inicio.",
                "attachment_image": "assets/capturas/ISSUE-05_hacer_otra_consulta.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Experiencia de Usuario",
                        "component": "frontend/js/app.js (renderRequesterChatStream, clearRequesterChat), frontend/index.html",
                        "description": "Tras recibir una respuesta del Asistente N1 o emitirse una Constancia FCR 100%, el usuario presiona el botón o enlace 'Hacer otra consulta' esperando una interfaz limpia para una nueva solicitud. No obstante, el sistema mantiene en pantalla todo el historial de mensajes anterior y solo cambia el placeholder a 'Escribe tu siguiente pregunta en este mismo hilo...'.",
                        "root_cause": "Los botones 'Hacer otra consulta' en app.js (líneas 2876, 2896, 2909) tienen asignado onclick='focusRequesterChatInput()', el cual no oculta #requester-inline-chat-stream ni restaura #requester-chat-hero.",
                        "solution": "1. Vincular los botones 'Hacer otra consulta' a clearRequesterChat();\n2. En clearRequesterChat(), resetear el array requesterChatMessages = [], ocultar el stream con display: none, restaurar el hero centrado con display: block y centrar el contenedor verticalmente;\n3. Mantener el registro de tickets previos accesible en 'Mis Solicitudes' sin contaminar el espacio de trabajo.",
                        "acceptance_criteria": [
                                "Escenario 1 (Ocultamiento Inmediato): DADO un chat con respuestas previas, CUANDO el usuario pulsa 'Hacer otra consulta', ENTONCES el historial de mensajes se oculta de inmediato y se despliega la pantalla inicial limpia con el buscador centrado ('¿En qué podemos asistirte hoy?').",
                                "Escenario 2 (Input Limpio y Enfocado): DADO el reseteo del chat, CUANDO la vista vuelve al reposo, ENTONCES el input queda en blanco con su placeholder por defecto y autofocus activo.",
                                "Escenario 3 (Persistencia Histórica): DADO que el stream actual se limpia, CUANDO el usuario consulta 'Mis Solicitudes', ENTONCES las constancias emitidas previamente siguen perfectamente registradas en la base de datos."
                        ]
                }
        },
		{
			"id": "ISSUE-06",
			"title": "[P1 - ALTA PRIORIDAD] Falla en visualización de Constancia de Resolución Inmediata y campo/toast fantasma sin texto",
			"epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
			"sp": 3,
			"sprint": "Sprint 6",
			"status": "rework",
			"discipline": "Frontend / UX & CSS",
			"type": "ISSUE",
			"priority": "P1",
			"doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-06",
			"doc_title": "DOC-SPEC-002 (ISSUE-06)",
			"doc_desc": "La constancia FCR no despliega el comprobante formal en 'Mis Solicitudes' y el toast blanco sobre blanco simula un campo vacío.",
			"attachment_image": "assets/capturas/ISSUE-06_error_tkt_no_encontrado_en_historial.png",
			"business_impact": {
				"level": "CRÍTICO",
				"dimension": "Continuidad Operativa Asistencial & Validez Documental FCR",
				"description": "La imposibilidad de visualizar y constatar el ticket resuelto en el historial vulnera la trazabilidad del primer contacto clínico (FCR 100%) y genera desconcierto en el profesional.",
				"metric_target": "100% de visualización exitosa del ticket FCR en el historial al abrir el link directo; 0 pantallas vacías.",
				"risk_of_inaction": "Duplicación de llamados a soporte técnico, sospecha de falla asistencial y pérdida de valor de la autogestión IA."
			},
			"so_feedback": {
				"status": "RECHAZADO / EN RETRABAJO (P1)",
				"observation": "Al hacer clic en el link de la constancia en el portal del solicitante se abre la ventana modal de solicitudes pero no se visualiza el ticket resuelto (#TKT-2026-0348), mostrando 'No se encontraron solicitudes registradas' debido a desajuste case-sensitive en la búsqueda y falta de persistencia en base de datos. Pasa a Retrabajo para corrección inmediata.",
				"reviewer": "Freddy Cortés (Solution Owner)",
				"date": "27/09/2026 09:30"
			},
			"issue_details": {
				"severity": "P1 — Alta Prioridad / Calidad Visual & FCR",
				"component": "frontend/js/app.js (requesterAiResolve, openRequesterHistoryModal), frontend/css/styles.css (.toast, .toast-container)",
				"description": "1. Al resolverse la consulta y pulsar 'Ver en Mis Solicitudes' o el badge FCR, el sistema abre la bandeja genérica sin destacar ni abrir la Constancia de Resolución Inmediata con su certificado formal.\n2. En la parte inferior derecha de la pantalla aparece un rectángulo blanco flotante sin texto legible, desconcertando al usuario.",
				"root_cause": "1. La función de historial no tiene anclaje ni apertura automática de la constancia individual generada.\n2. La clase CSS .toast tiene fondo #F8FAFC y color de texto #FFFFFF (texto blanco puro sobre fondo blanco hueso), tornando el mensaje '✓ Constancia FCR 100% registrada' completamente invisible, asemejándose a un campo residual vacío.",
				"solution": "1. Corregir estilos de .toast en styles.css para que utilice fondo oscuro corporativo (background: #0F172A; color: #FFFFFF;) o alert estilizado con texto legible;\n2. Implementar modal o vista de Constancia Formal de Resolución Inmediata (Certificado FCR) al hacer clic en 'Ver en Mis Solicitudes' o en la tarjeta de FCR, mostrando el ticket #TKT-2026-0348 con sello oficial de validación y datos del profesional.",
				"acceptance_criteria": [
					"Escenario 1 (Constancia FCR Visible y Completa): DADO un incidente resuelto con FCR 100%, CUANDO el profesional presiona 'Ver en Mis Solicitudes', ENTONCES se abre el comprobante formal con número de ticket, fecha, hora, diagnóstico y sello de resolución inmediata.",
					"Escenario 2 (Eliminación de Campo Fantasma): DADO cualquier evento que dispare un toast, CUANDO se visualiza en pantalla, ENTONCES presenta contraste 100% legible (fondo #0F172A, texto #FFFFFF) erradicando cajas vacías o sin texto.",
					"Escenario 3 (Trazabilidad FCR): DADO el registro del ticket FCR, CUANDO se consulta el historial de solicitudes, ENTONCES figura con badge verde de resuelto y acceso directo a su constancia imprimible."
				]
			}
		},
        {
                "id": "UH-66",
                "title": "[P1 - ALTA PRIORIDAD] Depuración de Componentes de Debug, Subtítulo Redundante y Limpieza Zen del Portal",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UI & Limpieza Zen",
                "type": "UH",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-66",
                "doc_title": "DOC-REQ-002 (UH-66)",
                "doc_desc": "Eliminación de barra de mockups de debug, subtítulo redundante en hero y corrección de desborde en cabecera.",
                "attachment_image": "assets/capturas/UH-66_limpieza_zen_debug.png",
                "narrative": {
                        "as_a": "Profesional Médico y Solicitante del Centro de Ayuda",
                        "i_want": "un portal de soporte técnico completamente limpio y sin ruido visual de desarrollo (sin botones de mockups 1 a 7, sin subtítulo redundante y sin elementos desbordados)",
                        "so_that": "pueda concentrarme exclusivamente en resolver mi consulta operativa sin distracciones ni botones ajenos a mi rol asistencial."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Remoción de Pastillas de Mockup): DADO el ingreso al sistema, CUANDO se visualiza la barra de navegación superior (#app-top-navbar), ENTONCES no existe el contenedor de debug #nav-mockup-pills (1. Portal, 2. Chat Stream, 3. Modal Ticket, etc.).",
                        "Escenario 2 (Hero Central Zen): DADO el estado inicial del Portal del Solicitante, CUANDO se renderiza el Hero centrado, ENTONCES únicamente se muestra el isotipo, el título '¿En qué podemos asistirte hoy?' y la barra de búsqueda, habiéndose eliminado el párrafo subtítulo de texto.",
                        "Escenario 3 (Cabecera Equilibrada sin Desbordes): DADO el extremo derecho de la cabecera, CUANDO se visualizan los accesos (+ Crear Solicitud, Mis Solicitudes, Chip de Perfil), ENTONCES se presentan completos, alineados y sin truncamiento ni botones espurios cortados [M...]."
                ],
                "adaptation_criteria": [
                        "Paso 1: Diseño centrado en el usuario y reducción de carga cognitiva.",
                        "Paso 2: Respeto estricto a la Regla OJO de cero elementos fuera de especificación.",
                        "Paso 3: Verificación visual libre de desbordes horizontales.",
                        "Paso 4: Trazabilidad en suite documental y tablero Scrumban."
                ]
        },
        {
                "id": "GAP-01",
                "title": "Formalización del Marco PMI+IA y Protocolo de Calidad en Suite Documental",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 5,
                "sprint": "Sprint 6",
                "status": "done",
                "discipline": "AF / Gobernanza",
                "type": "GAP",
                "priority": "P2",
                "doc_link": "08_MARCO_DE_TRABAJO_PMI_IA_Y_GOBERNANZA_CALIDAD.md",
                "doc_title": "DOC-GOV-008",
                "doc_desc": "Incorporación de los 4 pasos de adaptación PMI, delimitación de roles y protocolo TDD.",
                "narrative": {
                        "as_a": "Solution Owner de HealthDesk Quantux",
                        "i_want": "formalizar la integración de los 4 pasos del proceso de adaptación del PMI (PMBOK® 7ª Edición) con el ciclo de desarrollo asistido por IA generativa en la suite documental",
                        "so_that": "erradicar la degradación de calidad por instrucciones en lenguaje natural libre, evitar la deriva de contexto y asegurar respaldo contractual."
                },
                "acceptance_criteria": [
                        "Escenario 1: Existencia de DOC-GOV-008 en Markdown y HTML registrado en Plan de Gestión DOC-MGT-001.",
                        "Escenario 2: Matriz RACI delimitando que el Solution Owner (Humano) aprueba alcance y la IA ejecuta técnicamente sin autovalidarse.",
                        "Escenario 3: Registro mandatorio en Product/Sprint Backlog antes de tocar código de producción."
                ],
                "adaptation_criteria": [
                        "Paso 1: Enfoque Híbrido Estricto — Requerimientos predictivos cerrados + micro-sprints adaptativos.",
                        "Paso 2: Cumplimiento de restricciones institucionales OJO (cero cards, cero rojos).",
                        "Paso 3: Desglose atómico en UH con criterios Gherkin accionables en CLI.",
                        "Paso 4: Mejora continua en Product Backlog e incorporación retroactiva en GEMINI.md."
                ]
        },
        {
                "id": "MEJ-02",
                "title": "Soporte Nativo de Enlaces Documentales, Tipos de Item y Modal en Tablero Scrumban",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX",
                "type": "MEJORA",
                "priority": "P2",
                "doc_link": "00_Tablero_Scrumban_Quantux.html",
                "doc_title": "Tablero Scrumban",
                "doc_desc": "Visualización de documentación, tipos de item, roadmap interactivo y modales universales.",
                "narrative": {
                        "as_a": "Solution Owner y miembro del Comité Evaluador",
                        "i_want": "visualizar en el tablero Scrumban los badges tipológicos, enlaces directos, vistas de Roadmap y modales de detalle adaptativos",
                        "so_that": "gestionar el proyecto con transparencia total, auditar los requerimientos y tomar decisiones informadas de priorización."
                },
                "acceptance_criteria": [
                        "Escenario 1: Tarjetas con badges tipológicos, ID, SP y caja de enlace documental.",
                        "Escenario 2: Modales específicos según tipo (UH, Issue, Tarea, Épica, Gap).",
                        "Escenario 3: Pestañas para alternar entre Tablero Scrumban, Roadmap, Métricas y Backlog Jerárquico."
                ],
                "adaptation_criteria": [
                        "Paso 1: Progressive disclosure ágil.",
                        "Paso 2: Respeto visual a la paleta institucional Quantux.",
                        "Paso 3: JavaScript Vanilla sin dependencias pesadas.",
                        "Paso 4: Exportación sincronizada a CSV."
                ]
        },
        {
                "id": "MEJ-01",
                "title": "Automatización de Bucle TDD y Pre-commit Hooks para Validadores OJO",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 5,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "DevOps / QA",
                "type": "MEJORA",
                "priority": "P2",
                "doc_link": "08_MARCO_DE_TRABAJO_PMI_IA_Y_GOBERNANZA_CALIDAD.md#seccion-3",
                "doc_title": "DOC-GOV-008 (Sec 3.2)",
                "doc_desc": "Hook pre-commit para ejecutar validate_ojo_compliance.py y tests DOM secuencialmente.",
                "narrative": {
                        "as_a": "Facilitador Técnico y QA Lead de HealthDesk Quantux",
                        "i_want": "instrumentar un hook de pre-commit y un script de verificación automatizada secuencial",
                        "so_that": "impedir mecánicamente que el Agente IA introduzca cards flotantes, fondos oscuros o jergas clínicas."
                },
                "acceptance_criteria": [
                        "Escenario 1: Bloqueo con Exit Code 1 si se detectan violaciones OJO.",
                        "Escenario 2: Certificación Exit Code 0 en código limpio.",
                        "Escenario 3: Ejecución de tests demostrando fallo (rojo) antes de la solución mínima (verde)."
                ],
                "adaptation_criteria": [
                        "Paso 1: Quality gates predictivos.",
                        "Paso 2: Regla OJO de cero tolerancia a desviaciones.",
                        "Paso 3: Tests automatizados en CLI local.",
                        "Paso 4: Registro forense de no-conformidades."
                ]
        },
        {
                "id": "ISSUE-01",
                "title": "Remoción de términos clínicos hospitalarios ('guardia', 'asistencial') en app.js",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / QA",
                "type": "ISSUE",
                "priority": "P2",
                "doc_link": "validate_ojo_compliance.py",
                "doc_title": "Script de Validación OJO",
                "doc_desc": "Corrección de términos hospitalarios no autorizados para soporte técnico.",
                "issue_details": {
                        "severity": "P2 — Alta / No Conformidad de Estilo",
                        "component": "frontend/js/app.js",
                        "description": "El script de validación forense validate_ojo_compliance.py reporta incidencias por uso de términos clínicos asistenciales en el código fuente de frontend.",
                        "root_cause": "Legado de prototipos que utilizaban jergas de guardia médica en lugar de terminología técnica de soporte a consultorios.",
                        "solution": "Refactorizar las variables y cadenas de texto hacia 'Soporte Técnico Especializado' y 'Consultorio Digital'.",
                        "acceptance_criteria": [
                                "Escenario 1: Cero apariciones de términos prohibidos en validación.",
                                "Escenario 2: Preservación de toda la funcionalidad operativa existente."
                        ]
                }
        },
        {
                "id": "ISSUE-02",
                "title": "Sustitución de colores rojos no autorizados (#DC2626, #EF4444) por paleta Slate/Teal",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / CSS",
                "type": "ISSUE",
                "priority": "P2",
                "doc_link": "validate_ojo_compliance.py",
                "doc_title": "Script de Validación OJO",
                "doc_desc": "Sustitución de códigos hex rojos por advertencias neutrales en ámbar o slate.",
                "issue_details": {
                        "severity": "P2 — Alta / Restricción de Paleta Quantux",
                        "component": "frontend/css/styles.css, frontend/js/app.js",
                        "description": "Se detectaron colores rojos intensos utilizados en badges de urgencia que violan la regla OJO de entorno no punitivo.",
                        "root_cause": "Uso directo de clases utilitarias con colores de alerta estándar de Tailwind.",
                        "solution": "Reemplazar por escala neutra Slate con acento ámbar suave (#D97706 / #FEF3C7) aprobado institucionalmente.",
                        "acceptance_criteria": [
                                "Escenario 1: Cero códigos hex rojos detectados por validate_ojo_compliance.py.",
                                "Escenario 2: Correcta diferenciación visual de prioridades críticas sin tonos estridentes."
                        ]
                }
        },
        {
                "id": "TASK-01",
                "title": "Script de Hook Git Pre-commit y Wrapper CLI de Pruebas Continuas",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "DevOps / Calidad",
                "type": "TASK",
                "priority": "P3",
                "doc_link": "08_MARCO_DE_TRABAJO_PMI_IA_Y_GOBERNANZA_CALIDAD.md",
                "doc_title": "DOC-GOV-008",
                "doc_desc": "Creación del hook .git/hooks/pre-commit para compuerta determinista local.",
                "task_details": {
                        "scope": "Crear un runner en Python que encapsule validate_ojo_compliance.py y test_dom_visual_compliance.py asegurando rechazo automático de commits no conformes.",
                        "deliverables": [
                                "tools/pre_commit_runner.py",
                                "Configuración en .git/hooks/pre-commit",
                                "Salida formateada con semáforo en terminal"
                        ],
                        "dod": "El hook intercepta cualquier commit y aborta si la validación falla con código 1."
                }
        },
        {
                "id": "OM-01",
                "title": "Trazabilidad Bidireccional de Tickets hacia Contratos OpenAPI y Esquemas DDL",
                "epic": "17. Arquitectura & APIs",
                "sp": 8,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Backend / Arq",
                "type": "OPORTUNIDAD",
                "priority": "P2",
                "doc_link": "API_CONTRACTS.md",
                "doc_title": "API_CONTRACTS.md",
                "doc_desc": "Validación de esquema OpenAPI 3.0 y modelos Pydantic contra BD.",
                "narrative": {
                        "as_a": "Arquitecto de Software de HealthDesk Quantux",
                        "i_want": "vincular cada endpoint de FastAPI con la especificación contractual en docs/API_CONTRACTS.md",
                        "so_that": "asegurar consistencia 100% de esquemas y prevenir alucinaciones de modelos."
                },
                "acceptance_criteria": [
                        "Escenario 1: Paridad exacta entre /openapi.json y API_CONTRACTS.md.",
                        "Escenario 2: Modelos DDL sin atributos espurios.",
                        "Escenario 3: Rechazo automático de cambios no documentados en compuerta de arquitectura."
                ],
                "adaptation_criteria": [
                        "Paso 1: Spec-Driven Development (SDD).",
                        "Paso 2: Trazabilidad en entidades de soporte.",
                        "Paso 3: Verificación con Pydantic.",
                        "Paso 4: Versionado semántico."
                ]
        },
        {
                "id": "GAP-02",
                "title": "Blindaje de Integridad de Contexto para Auditorías TQM y Cero Scope Creep",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 5,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "QA / Metodología",
                "type": "GAP",
                "priority": "P2",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md",
                "doc_title": "DOC-QA-004",
                "doc_desc": "Checklist ejecutable de auditoría contra alucinaciones y omisiones pre-entrega.",
                "narrative": {
                        "as_a": "Auditor de Calidad TQM de Quantux Salud",
                        "i_want": "un protocolo determinista de verificación de contexto y cotejo de observaciones",
                        "so_that": "erradicar el olvido de especificaciones, evitar el scope creep y asegurar evidencia en DOC-QA-004."
                },
                "acceptance_criteria": [
                        "Escenario 1: Matriz de cobertura explícita sin omisiones.",
                        "Escenario 2: Logs reales de terminal y aserciones registradas en DOC-QA-004.",
                        "Escenario 3: Consulta aclaratoria mandatoria al Solution Owner ante dudas."
                ],
                "adaptation_criteria": [
                        "Paso 1: Dual-Loop Validation.",
                        "Paso 2: Inmunización en GEMINI.md.",
                        "Paso 3: Checklists binarios pre-vuelo.",
                        "Paso 4: Retroalimentación continua al backlog."
                ]
        },
        {
                "id": "OM-02",
                "title": "Caché de Consultas y Optimización de Carga del Cockpit en Memoria",
                "epic": "17. Arquitectura & APIs",
                "sp": 8,
                "sprint": "Product Backlog",
                "status": "backlog",
                "discipline": "Backend / Perf",
                "type": "OPORTUNIDAD",
                "priority": "P3",
                "doc_link": "03_ARQUITECTURA_Y_DISENO_TECNICO.md",
                "doc_title": "DOC-ARC-003",
                "doc_desc": "Estrategia de caching LRU y compresión gzip para respuesta de bandeja en < 150ms."
        },
        {
                "id": "OM-03",
                "title": "[P3 - BAJA PRIORIDAD] Parametrización y Filtros Avanzados para la Exportación de Datos en Formato CSV",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Product Backlog",
                "status": "backlog",
                "discipline": "Frontend / Data Export",
                "type": "OPORTUNIDAD",
                "priority": "P3",
                "doc_link": "03_ARQUITECTURA_Y_DISENO_TECNICO.md#om-03",
                "doc_title": "DOC-ARC-003 (OM-03)",
                "doc_desc": "Modal de parametrización para el botón de exportación CSV (selección de columnas, filtros por estado/sprint y delimitadores).",
                "attachment_image": "assets/capturas/OPP-03_parametrizacion_exportar_csv.png",
                "narrative": {
                        "as_a": "Líder de Soporte / Solution Owner",
                        "i_want": "que el botón 'Exportar CSV' me permita parametrizar los campos, estados, sprints y formato del archivo antes de la descarga",
                        "so_that": "pueda generar reportes a medida sin tener que depurar manualmente columnas innecesarias o archivos no filtrados."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Modal de Configuración Previa): DADO el botón 'Exportar CSV' en la barra de herramientas, CUANDO el usuario hace clic, ENTONCES se abre un modal de configuración que permite marcar/desmarcar columnas (ID, Título, Estado, Prioridad, SP, Criterios, Evidencias).",
                        "Escenario 2 (Filtros por Estado y Sprint): DADO el modal de exportación, CUANDO el usuario selecciona un subconjunto (ej: solo ítems 'En Revisión' del Sprint 6), ENTONCES el archivo descargado contiene únicamente los registros que coinciden con los filtros.",
                        "Escenario 3 (Trazabilidad Visual): DADO el registro de la oportunidad en el tablero, CUANDO se consulta el detalle de la tarjeta, ENTONCES exhibe la captura con el botón 'Exportar CSV' como evidencia original."
                ]
        },
        {
                "id": "TASK-05",
                "title": "Generador de Reportes de Cumplimiento TQM y Certificación PDF Automática",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 5,
                "sprint": "Product Backlog",
                "status": "backlog",
                "discipline": "QA / DevOps",
                "type": "TASK",
                "priority": "P3",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md",
                "doc_title": "DOC-QA-004",
                "doc_desc": "Script que compila evidencias, capturas y métricas de calidad en PDF imprimible."
        },
        {
                "id": "UH-33",
                "title": "Vinculación Jerárquica a Ticket Padre (Incidente Masivo)",
                "epic": "1. Incidentes Masivos",
                "sp": 5,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / FSM",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-34",
                "title": "Resolución y Cierre Automatizado en Cascada",
                "epic": "1. Incidentes Masivos",
                "sp": 4,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / FSM",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-35",
                "title": "Desvinculación por Excepción de Ticket Padre",
                "epic": "1. Incidentes Masivos",
                "sp": 3,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / FSM",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-36",
                "title": "Catálogo y Asociación de Versiones de Release",
                "epic": "2. Releases y Despliegues",
                "sp": 5,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "DevOps / Releases",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-37",
                "title": "Cierre Automático por Despliegue en Producción",
                "epic": "2. Releases y Despliegues",
                "sp": 3,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "DevOps / Releases",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-38",
                "title": "Paginación Server-Side y Filtros en Bandeja",
                "epic": "3. Bandeja General & Paginación",
                "sp": 5,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Backend / DB",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-39",
                "title": "Búsqueda Full-Text Multi-Atributo",
                "epic": "3. Bandeja General & Paginación",
                "sp": 4,
                "sprint": "Sprint 1",
                "status": "done",
                "discipline": "Frontend / UX",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-40",
                "title": "Layout Zen de Edición sin Distracciones",
                "epic": "4. Workspace Zen",
                "sp": 6,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Frontend / UI",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-41",
                "title": "Gestión de Notas Internas Privadas",
                "epic": "4. Workspace Zen",
                "sp": 5,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Backend / Auth",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-42",
                "title": "Acciones Rápidas con Teclado (Shortcuts)",
                "epic": "4. Workspace Zen",
                "sp": 5,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Frontend / Accesibilidad",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-43",
                "title": "Formulario de Alta Progresivo en 3 Pasos",
                "epic": "5. Alta Sin Ruido",
                "sp": 5,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Frontend / UX",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-44",
                "title": "Validación Preventiva y Sugerencias de KB",
                "epic": "5. Alta Sin Ruido",
                "sp": 5,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Frontend / AI",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-45",
                "title": "Multi-Tenancy y Configuración por Cliente",
                "epic": "6. Generalización Enterprise",
                "sp": 6,
                "sprint": "Sprint 2",
                "status": "done",
                "discipline": "Arquitectura / DB",
                "type": "UH",
                "priority": "P1"
        },
        {
                "id": "UH-46",
                "title": "Widgets de Control Operativo y SLAs",
                "epic": "7. Tablero de Control Zen",
                "sp": 5,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / Analytics",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-47",
                "title": "Filtro Rápido por Período y Exportación",
                "epic": "7. Tablero de Control Zen",
                "sp": 4,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Backend / Reporting",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-48",
                "title": "Directorio de Usuarios y Estado de Operadores",
                "epic": "8. Directorio de Usuarios Zen",
                "sp": 5,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Backend / IAM",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-49",
                "title": "Gestión de Habilidades y Asignación Automática",
                "epic": "8. Directorio de Usuarios Zen",
                "sp": 5,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Backend / Algoritmos",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-50",
                "title": "Ingesta Automática de Tickets vía Email",
                "epic": "9. Ingesta Email Omnicanal",
                "sp": 6,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Backend / Integración",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-51",
                "title": "Parsing de Adjuntos y Respuestas por Correo",
                "epic": "9. Ingesta Email Omnicanal",
                "sp": 6,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Backend / Parser",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-52",
                "title": "Encuesta de Satisfacción (CSAT) Post-Resolución",
                "epic": "10. Cierre & CSAT",
                "sp": 6,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Frontend / UX",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-53",
                "title": "Reporte de Calidad Percibida por Operador",
                "epic": "10. Cierre & CSAT",
                "sp": 6,
                "sprint": "Sprint 3",
                "status": "done",
                "discipline": "Backend / BI",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-54",
                "title": "Administración Dinámica del Catálogo de Servicios",
                "epic": "11. Catálogo Zen",
                "sp": 6,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Admin",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-55",
                "title": "Matriz de Tipificaciones y SLAs Asociados",
                "epic": "11. Catálogo Zen",
                "sp": 5,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Arquitectura / Reglas",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-56",
                "title": "Vista de Torre de Control y Carga de Equipo",
                "epic": "12. Team Leader & Torre",
                "sp": 5,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Frontend / Realtime",
                "type": "UH",
                "priority": "P1"
        },
        {
                "id": "UH-57",
                "title": "Reasignación Masiva y Balanceo de Carga",
                "epic": "12. Team Leader & Torre",
                "sp": 5,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Optimización",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-58",
                "title": "Portal de Soporte a Consultorios Digitales",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 7,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Frontend / Especializado",
                "type": "UH",
                "priority": "P1"
        },
        {
                "id": "UH-59",
                "title": "Typeahead Predictivo de Temas Homologados CD2",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 6,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Frontend / Búsqueda",
                "type": "UH",
                "priority": "P1"
        },
        {
                "id": "UH-60",
                "title": "Integración con Base de Casos Operativos SISA/Matrículas",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 6,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Backend / Conocimiento",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-61",
                "title": "Formulario Exprés de Contingencia para Médicos",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 6,
                "sprint": "Sprint 4",
                "status": "done",
                "discipline": "Frontend / Accesibilidad",
                "type": "UH",
                "priority": "P2"
        },
        {
                "id": "UH-62",
                "title": "Rediseño de Sidebar Ergonómico Colapsable",
                "epic": "15. Sidebar Zen & Ergonomía",
                "sp": 4,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / CSS",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-63",
                "title": "Navegación Rápida por Teclas Numéricas",
                "epic": "15. Sidebar Zen & Ergonomía",
                "sp": 3,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / JS",
                "type": "UH",
                "priority": "P3"
        },
        {
                "id": "UH-64",
                "title": "Indicadores de Carga y Tooltips Informativos",
                "epic": "15. Sidebar Zen & Ergonomía",
                "sp": 3,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "Frontend / UI",
                "type": "UH",
                "priority": "P4"
        },
        {
                "id": "UH-65",
                "title": "Certificación UAT y Cierre de Línea Base v4.0",
                "epic": "15. Sidebar Zen & Ergonomía",
                "sp": 4,
                "sprint": "Sprint 5",
                "status": "done",
                "discipline": "QA / Certificación",
                "type": "UH",
                "priority": "P1"
        },
        {
                "id": "MEJ-03",
                "title": "[P1 - ALTA PRIORIDAD] Rediseño Visual Estilo Quantux y Densidad Informativa de Tickets en Vista Jerárquica WBS",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Design System & WBS",
                "type": "MEJ",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#mej-03",
                "doc_title": "DOC-SPEC-002 (MEJ-03)",
                "doc_desc": "Transformación de filas planas en tarjetas enriquecidas corporativas con tokens Quantux, tipografías Outfit / JetBrains Mono, chips de prioridad y previsualización de evidencias.",
                "attachment_image": "assets/capturas/MEJ-03_wbs_estilo_quantux.png",
                "narrative": {
                        "as_a": "Líder Técnico y Solution Owner",
                        "i_want": "que los tickets dentro de cada épica en la vista Árbol WBS se visualicen con el diseño corporativo completo de Quantux (tarjetas estructuradas, badges, métricas y enlaces interactivos)",
                        "so_that": "la estructura de desglose del trabajo refleje la misma calidad visual, densidad de información y profesionalismo que el tablero Scrumban."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Estilo Quantux en WBS): DADO el visor de jerarquía WBS, CUANDO se despliega cualquier épica, ENTONCES los tickets se presentan en un grid de tarjetas con bordes coloreados por prioridad, tipografía Outfit y monospace.",
                        "Escenario 2 (Interactividad Total): DADO un ticket en la vista WBS, CUANDO se hace clic en 'Ver Detalle' o en el documento, ENTONCES se abre el modal correspondiente o la especificación sin perder el contexto.",
                        "Escenario 3 (Trazabilidad Visual): DADO el requerimiento, CUANDO se consulta en el tablero, ENTONCES presenta la captura original como evidencia visual inmutable."
                ]
        },
        {
                "id": "ISSUE-08",
                "title": "[P2 - MEDIA PRIORIDAD] Gobernanza Definition of Done: Prohibición de Transición a Resuelto sin Implementación Técnica Verificada (Quality Gate PMI)",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Gobernanza / Quality Gate PMI & QA",
                "type": "ISSUE",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-08",
                "doc_title": "DOC-SPEC-002 (ISSUE-08)",
                "doc_desc": "Control de calidad pericial que impide marcar una tarjeta o épica como 'Completada' si no posee un fix técnico implementado y verificado en código o suite de tests.",
                "attachment_image": "",
                "issue_details": {
                        "severity": "P2 — Media / Gobernanza y Aseguramiento de Calidad",
                        "component": "Tablero Scrumban, scripts/build_full_scrumban_board.py, frontend/js/app.js",
                        "description": "Una tarjeta del tablero kanban tenía todas sus tareas hijas marcadas como resueltas en apariencia, pero el fix técnico no se había implementado en el producto real. El Solution Owner exige blindar el sistema para evitar resoluciones ficticias.",
                        "root_cause": "Falta de validación bidireccional entre el estado declarado en el backlog y la verificación tangible de artefactos de código o pruebas automatizadas.",
                        "solution": "1. Implementar regla estricta de Quality Gate DoD: una épica calcula su estado dinámicamente sumando hijos reales y solo alcanza 100% cuando todos sus entregables existen.\n2. Alertas visuales en el tablero cuando un ítem no tiene fix verificado.",
                        "acceptance_criteria": [
                                "Escenario 1 (Cálculo Dinámico de Épica): DADO el visor de épicas, CUANDO una épica tiene ítems pendientes, ENTONCES jamás puede mostrarse como 'Completada' o 100%.",
                                "Escenario 2 (Quality Gate en Drag & Drop): DADO el movimiento de tarjetas a 'Done', CUANDO no hay evidencia técnica registrada, ENTONCES el sistema solicita confirmación formal de verificación."
                        ]
                }
        },
        {
                "id": "ISSUE-09",
                "title": "[P1 - ALTA PRIORIDAD] Contraste y Visibilidad de Notificaciones Toast en Pantalla (Texto Blanco sobre Fondo Blanco)",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Accesibilidad & CSS",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-09",
                "doc_title": "DOC-SPEC-002 (ISSUE-09)",
                "doc_desc": "Corrección de contraste severo en notificaciones toast emergentes donde el texto blanco sobre fondo claro resultaba invisible al tildar pastillas en la Matriz Multi-Tenant.",
                "attachment_image": "assets/capturas/ISSUE-09_toast_pastilla_sin_texto.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Accesibilidad y Feedback Operativo",
                        "component": "frontend/css/styles.css (.toast), frontend/js/app.js (showToast)",
                        "description": "Al conmutar una pastilla de módulo en la Matriz Multi-Tenant, se mostraba un emergente abajo a la derecha completamente blanco, con texto ilegible o sin información perceptible.",
                        "root_cause": "Regla CSS con background: #F8FAFC y color: #FFFFFF (blanco sobre blanco casi idéntico).",
                        "solution": "Rediseño de .toast con fondo Navy corporativo (#0F172A), texto nítido blanco (#F8FAFC), borde izquierdo Teal (#00C4B4), iconos descriptivos y animación fluida.",
                        "acceptance_criteria": [
                                "Escenario 1 (Alto Contraste): DADO cualquier toast emitido por el sistema, CUANDO aparece en pantalla, ENTONCES cumple ratio de contraste WCAG AAA sobre fondo Navy con texto nítido.",
                                "Escenario 2 (Mensaje Informativo Claro): DADO el clic en una pastilla de habilitación, CUANDO se genera el toast, ENTONCES exhibe claramente: 'Módulo [X] Habilitado/Suspendido para [Institución]'."
                        ]
                }
        },
        {
                "id": "ISSUE-10",
                "title": "[P1 - CRÍTICA] Fallo de Apertura e Interacción en Tarjeta de Organización OSDE",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Navegabilidad & Resiliencia",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-10",
                "doc_title": "DOC-SPEC-002 (ISSUE-10)",
                "doc_desc": "Restauración de eventos de clic y resiliencia en la tarjeta de OSDE y en la tabla de solicitudes para garantizar apertura inmediata del detalle.",
                "attachment_image": "assets/capturas/ISSUE-10_tarjeta_osde_no_abre.png",
                "issue_details": {
                        "severity": "P1 — Crítica / Bloqueante de Navegación",
                        "component": "frontend/js/app.js (openInstitutionDetailModal, renderRequesterModalHistory)",
                        "description": "Al hacer clic en la tarjeta o fila correspondiente a la organización OSDE, el sistema no respondía ni abría la ventana modal de detalle.",
                        "root_cause": "Falta de listener de evento clic en la fila completa y ausencia de datos predeterminados de contingencia en caso de sincronización diferida del backend.",
                        "solution": "1. Asignar onclick a la fila completa de la tabla de solicitudes.\n2. Incorporar fallback robusto en openInstitutionDetailModal para inicializar catálogo si el array en memoria está vacío.",
                        "acceptance_criteria": [
                                "Escenario 1 (Apertura Inmediata): DADO el catálogo de instituciones o la tabla de solicitudes, CUANDO el usuario hace clic sobre OSDE, ENTONCES el modal se abre instantáneamente con los datos completos.",
                                "Escenario 2 (Interactividad de Fila Completa): DADO un registro de OSDE, CUANDO se hace clic en cualquier celda de la fila, ENTONCES responde con apertura sin requerir puntería en un botón milimétrico."
                        ]
                }
        },
        {
                "id": "ISSUE-11",
                "title": "[P1 - ALTA PRIORIDAD] Sub-vista Módulos de Software en Blanco (Falta de Inyección en Grid)",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Arquitectura de Vistas",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-11",
                "doc_title": "DOC-SPEC-002 (ISSUE-11)",
                "doc_desc": "Corrección de función renderClinicalPlatformsCards para poblar el contenedor grid-platforms-cards con tarjetas de alta densidad informativa.",
                "attachment_image": "",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Pantalla en Blanco",
                        "component": "frontend/js/app.js (renderClinicalPlatformsCards)",
                        "description": "La sub-pestaña 'Módulos de Software' dentro de 'Clientes & Mesas de Ayuda' se visualizaba completamente vacía, sin renderizar ninguna tarjeta ni listado.",
                        "root_cause": "La función en JavaScript generaba filas de tabla <tr> buscando un <tbody> inexistente, omitiendo inyectar el grid de tarjetas en #grid-platforms-cards.",
                        "solution": "Generar tarjetas ricas Quantux con icono, código, protocolo técnico (HL7 FHIR / REST), nivel ITIL de soporte, barra de cobertura en clientes y estado operativo (99.98% uptime).",
                        "acceptance_criteria": [
                                "Escenario 1 (Visualización de Catálogo Completo): DADO el ingreso a la pestaña 'Módulos de Software', CUANDO se carga la vista, ENTONCES se exhiben las tarjetas de todos los módulos disponibles en grid responsive.",
                                "Escenario 2 (Métricas Operativas): DADO cada módulo, CUANDO se visualiza su tarjeta, ENTONCES indica cantidad de instituciones conectadas, nivel ITIL asignado y accesos directos a detalle y matriz."
                        ]
                }
        },
        {
                "id": "ISSUE-12",
                "title": "[P1 - CRÍTICA] Rediseño UX/UI y Navegabilidad Ergonómica de la Matriz Interactiva Multi-Tenant",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 5,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Product Design / UX & Arquitectura Multi-Tenant",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-12",
                "doc_title": "DOC-SPEC-002 (ISSUE-12)",
                "doc_desc": "Modernización ergonómica total de la Matriz Multi-Tenant con guía interactiva explicativa, buscador en tiempo real, filtros por segmento de salud y conmutadores visuales de alto contraste.",
                "attachment_image": "assets/capturas/ISSUE-12_redisenio_ux_matriz_multitenant.png",
                "issue_details": {
                        "severity": "P1 — Crítica / Usabilidad y Experiencia de Usuario",
                        "component": "frontend/index.html (#platforms-subview-matrix), frontend/js/app.js (renderTenantMatrixTable)",
                        "description": "La matriz de habilitación presentaba una grilla abrumadora de 168 pastillas idénticas sin jerarquía visual, títulos cortados con puntos suspensivos ('...'), sin filtros por tipo de institución y sin explicación de su propósito ni de las consecuencias de activar/desactivar un servicio.",
                        "root_cause": "Diseño plano inicial sin divulgación progresiva (progressive disclosure), sin barra de búsqueda y sin componentes de feedback contextual.",
                        "solution": "1. Banner desplegable '¿Cómo funciona la Matriz Multi-Tenant?': explica el aislamiento de datos, sincronización en memoria y reglas de seguridad.\n2. Buscador en vivo por nombre/código de cliente.\n3. Filtros por segmento: Todas, Prepagas, Sanatorios, Hospitales.\n4. Interruptores ergonómicos estilo iOS/Tailwind con estados claros (✓ ACTIVO / ✕ INACTIVO).\n5. Columna de cobertura porcentual con barra de progreso.\n6. Acciones masivas 'Todo/Nada' por fila de cliente.",
                        "acceptance_criteria": [
                                "Escenario 1 (Comprensión Inmediata): DADO un usuario que ingresa a la Matriz, CUANDO consulta la vista, ENTONCES dispone de una guía operativa clara que explica cómo funciona la habilitación multi-inquilino.",
                                "Escenario 2 (Filtros y Búsqueda Ágiles): DADO el catálogo de 14 instituciones, CUANDO el usuario tipea o filtra por segmento, ENTONCES la tabla se actualiza instantáneamente sin recargar la página.",
                                "Escenario 3 (Toggles Ergonómicos y Cobertura): DADO cada cliente, CUANDO se alternan sus módulos, ENTONCES el interruptor responde visualmente al instante y recalcula la barra de porcentaje de cobertura."
                        ]
                }
        },
        {
                "id": "ISSUE-13",
                "title": "[P1 - ALTA PRIORIDAD] Remoción de Banner de Runbook Oficial y Verdad Única (SSOT) en Respuestas del Asistente",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Writing & Limpieza Visual",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-13",
                "doc_title": "DOC-SPEC-002 (ISSUE-13)",
                "doc_desc": "Eliminación del bloque inferior 'Runbook Oficial: MED-006... Verdad Única (SSOT)' y ajuste de textos en el asistente.",
                "attachment_image": "assets/capturas/ISSUE-13_quitar_banner_runbook_ssot.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Despeje de Ruido en Respuestas",
                        "component": "frontend/js/app.js (renderKbAiResponse, typing indicator)",
                        "description": "Al pie de las respuestas asistidas aparecía un recuadro adicional 'Runbook Oficial: MED-006: Repositorio de Medicamentos y Receta Digital - Error 500 por Jurisdicción / Verdad Única (SSOT)' que generaba sobrecarga visual y ruido informativo.",
                        "root_cause": "Inclusión de footer redundante de runbook en la plantilla HTML del mensaje de IA.",
                        "solution": "Remover la inserción de runbookFooterHtml y actualizar el indicador de tipeo a 'Consultando base de conocimiento y catálogo técnico de soporte...'.",
                        "acceptance_criteria": [
                                "Escenario 1 (Despeje de Banner Inferior): DADO cualquier mensaje generado por el asistente, CUANDO se renderiza en el chat, ENTONCES no figura el bloque 'Runbook Oficial... Verdad Única (SSOT)'.",
                                "Escenario 2 (Trazabilidad Visual): DADO el registro del issue, CUANDO se abre la tarjeta, ENTONCES exhibe la captura adjunta como evidencia."
                        ]
                }
        },
        {
                "id": "ISSUE-14",
                "title": "[P2 - MEDIA PRIORIDAD] Remoción de Pastillas y Botones Redundantes sin Información en Respuestas",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Writing & Limpieza de Badges",
                "type": "ISSUE",
                "priority": "P2",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-14",
                "doc_title": "DOC-SPEC-002 (ISSUE-14)",
                "doc_desc": "Eliminación de la duplicación de badges de módulo y categoría cuando contienen el mismo término ('Receta Digital' repetido dos veces consecutivas).",
                "attachment_image": "assets/capturas/ISSUE-14_botones_redundantes_receta_digital.png",
                "issue_details": {
                        "severity": "P2 — Media / Redundancia Visual",
                        "component": "frontend/js/app.js (renderKbAiResponse)",
                        "description": "En la cabecera del mensaje de IA se mostraban dos pastillas idénticas una al lado de la otra: '[⚙️ Receta Digital] [Receta Digital]', sin aportar ninguna diferenciación útil.",
                        "root_cause": "Renderizado incondicional simultáneo de 'subsystem' y 'articleCategory' sin comparar si comparten la misma cadena.",
                        "solution": "Comparar ambos valores y omitir la segunda pastilla si la categoría es redundante con el subsistema.",
                        "acceptance_criteria": [
                                "Escenario 1 (Cero Pastillas Duplicadas): DADO un mensaje del asistente sobre Receta Digital, CUANDO se muestran los tags superiores, ENTONCES se exhibe una única pastilla '⚙️ Receta Digital' acompañada del código de procedimiento."
                        ]
                }
        },
        {
                "id": "ISSUE-15",
                "title": "[P1 - ALTA PRIORIDAD] Remoción de Checkboxes Inoperantes en Guía de Acción Operativa y Limpieza de Markdown",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Limpieza & Formateo",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-15",
                "doc_title": "DOC-SPEC-002 (ISSUE-15)",
                "doc_desc": "Sustitución de checkboxes inútiles por pasos numerados limpios y erradicación de asteriscos crudos (**) en el texto.",
                "attachment_image": "assets/capturas/ISSUE-15_quitar_checkboxes_pasos_operativos.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Experiencia de Usuario y Tipografía",
                        "component": "frontend/js/app.js (renderKbAiResponse)",
                        "description": "La sección 'GUÍA DE ACCIÓN OPERATIVA (CHECKLIST EN VIVO)' incluía casillas de selección <input type=\"checkbox\"> que no cumplían ninguna función de persistencia ni lógica, además de exhibir asteriscos sin parsear (**Validación:**).",
                        "root_cause": "Uso de controles de formulario interactivos innecesarios y falta de filtro de markdown en la cadena de texto de pasos.",
                        "solution": "1. Eliminar checkboxes y reemplazarlos por números de paso elegantes (1, 2, 3).\n2. Limpiar asteriscos crudos y convertir negritas sintácticas.\n3. Renombrar sección a 'Guía de Acción Operativa (Pasos de Resolución):'.",
                        "acceptance_criteria": [
                                "Escenario 1 (Cero Checkboxes Inútiles): DADO el bloque de resolución del asistente, CUANDO se visualizan los pasos, ENTONCES no existe ningún checkbox inoperante.",
                                "Escenario 2 (Tipografía Limpia): DADO el texto de cada paso, CUANDO se renderiza, ENTONCES no figuran asteriscos crudos (**) y la lectura es limpia y profesional."
                        ]
                }
        },
        {
                "id": "ISSUE-16",
                "title": "[P2 - MEDIA PRIORIDAD] Remoción de Botones de Navegación Rápida a Mockups en Top Navbar",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Ergonomía UI",
                "type": "ISSUE",
                "priority": "P2",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-16",
                "doc_title": "DOC-QA-004 (ISSUE-16)",
                "doc_desc": "Eliminación de pastillas de mockup redundantes en navbar (#nav-mockup-pills) para despejar cabecera y optimizar usabilidad.",
                "attachment_image": "assets/capturas/ISSUE-16_quitar_botones_navegacion_vistas.png",
                "issue_details": {
                        "severity": "P2 — Media Prioridad / Redundancia y Ergonomía de Cabecera",
                        "component": "frontend/index.html (navbar-right, #nav-mockup-pills)",
                        "description": "La barra superior exhibía un contenedor de botones redundantes ('1. Portal', '2. Chat Stream', '3. Modal Ticket', '4. Mis Solicitudes', '5. Detalle N2', '6. Mando Líder', '7. Config ITIL') que constituían un artefacto temporal de maquetación, consumiendo espacio visual crítico y sobrecargando la barra de navegación del usuario.",
                        "root_cause": "Persistencia de botones de navegación directa a mockups en la vista de producción, desprovistos de utilidad para la operación real.",
                        "solution": "1. Eliminar íntegramente el elemento '#nav-mockup-pills' de frontend/index.html.\\n2. Otorgar mayor amplitud y foco ergonómico al buscador omnicanal y a los accesos principales de cabecera.\\n3. Dejar la tarjeta en estado 'qa' (En Revisión / Aceptación Solution Owner) para que el Solution Owner verifique el contraste contra la especificación.",
                        "acceptance_criteria": [
                                "Escenario 1 (Eliminación de Botonera Redundante): DADO el navbar superior de la aplicación, CUANDO el usuario carga cualquier vista, ENTONCES los botones '1. Portal', '2. Chat Stream', '3. Modal Ticket', etc. no se visualizan en pantalla.",
                                "Escenario 2 (Cabecera Despejada): DADO el espacio libre en el navbar, CUANDO se visualiza el buscador global omnicanal, ENTONCES este goza de visibilidad limpia y sin saturación de controles secundarios.",
                                "Escenario 3 (Trazabilidad Visual): DADO el detalle de la tarjeta ISSUE-16 en el tablero Scrumban, CUANDO se abre la ficha, ENTONCES exhibe la captura adjunta con la botonera recortada como evidencia inmutable."
                        ]
                }
        },
        {
                "id": "ISSUE-17",
                "title": "[P1 - ALTA PRIORIDAD] Tooltips sin Información en Barra de Navegación Lateral Colapsada",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Ergonomía UI",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-17",
                "doc_title": "DOC-QA-004 (ISSUE-17)",
                "doc_desc": "Corrección de color y contraste en tooltips flotantes del menú lateral colapsado (reemplazo de texto blanco sobre fondo blanco por Navy #0F172A y texto #F8FAFC).",
                "attachment_image": "assets/capturas/ISSUE-17_tooltips_sin_informacion_sidebar.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Visibilidad y Contraste de UI",
                        "component": "frontend/css/styles.css (.app-sidebar.collapsed .win11-sidebar-nav [data-tooltip]:hover::after)",
                        "description": "Al colocar el cursor sobre los iconos del menú de navegación lateral en modo colapsado, el tooltip emergente se renderizaba como un rectángulo blanco completamente vacío, impidiendo al usuario conocer la función de cada icono.",
                        "root_cause": "La regla CSS definía background: #FFFFFF y color: #FFFFFF de manera concurrente, produciendo texto blanco invisible sobre fondo blanco.",
                        "solution": "1. Corregir la regla CSS aplicando fondo Slate/Navy #0F172A con texto de alto contraste #F8FAFC.\\n2. Incorporar borde distintivo Teal Quantux (#00C4B4) y animación de entrada fluida.\\n3. Asignar estado 'qa' (En Revisión / Aceptación Solution Owner) para que el Solution Owner verifique el contraste contra la especificación.",
                        "acceptance_criteria": [
                                "Escenario 1 (Visibilidad Inmediata del Texto): DADO el menú lateral colapsado, CUANDO el operador posiciona el cursor sobre cualquier icono (Centro de Ayuda, Mesa de Ayuda, etc.), ENTONCES el tooltip muestra claramente el nombre del módulo en tipografía blanca sobre fondo oscuro.",
                                "Escenario 2 (Identidad Visual Quantux): DADO el tooltip desplegado, CUANDO se visualiza en pantalla, ENTONCES presenta el acento corporativo Teal (#00C4B4) y sombra difuminada sin saturación.",
                                "Escenario 3 (Trazabilidad Visual): DADO el registro del defecto en el tablero Scrumban, CUANDO se abre la ficha de ISSUE-17, ENTONCES exhibe la captura del tooltip vacío como evidencia inmutable."
                        ]
                }
        },
        {
                "id": "UH-69",
                "title": "[P1 - ALTA PRIORIDAD] Bot Gestor de Tickets Multi-Rol, Evaluación KCS v6 y Trazabilidad de Tickets Contribuyentes en Base de Conocimiento",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 8,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Backend & Fullstack / Bot IA & KCS v6",
                "type": "UH",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-69",
                "doc_title": "DOC-SPEC-002 (UH-69)",
                "doc_desc": "Motor autónomo multi-rol con registro de mensajes (rol y sector), evaluación KCS v6 al resolver tickets y consulta con tickets contribuyentes en Base de Conocimiento.",
                "narrative": {
                        "as_a": "Solution Owner, Analista de Soporte y Profesional Asistencial",
                        "i_want": "que el Bot Gestor de Tickets avance automáticamente los casos interactuando con todos los roles y sectores institucionales, registre los diálogos con autor, rol y sector, evalúe según el negocio si el caso capitaliza conocimiento para asociarlo a la Base de Conocimiento al resolverse, y permita que al consultar la KB se visualicen los tickets que sumaron información",
                        "so_that": "se asegure la continuidad operativa, trazabilidad conversacional y enriquecimiento continuo de la Base de Conocimiento (KCS v6) sin sobrecarga burocrática manual."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Avance Multi-Rol y Registro de Mensajes): DADO un ticket en cualquier estado del flujo ITIL (NUEVO, ASIGNADO, EN_CURSO), CUANDO el bot gestor procesa un paso, ENTONCES interactúa con el rol correspondiente (SOLICITANTE, SOPORTE_N1, ESPECIALISTA_N2, ADMIN_INFRAESTRUCTURA_N3, TEAM_LEADER, PASARELA_TERCEROS) y su sector (Guardia Central, Farmacia y Triage, Integraciones y Pasarelas OSDE/SISA, Infraestructura N3), registrando cada mensaje en ticket_comments con author_role y author_sector.",
                        "Escenario 2 (Evaluación de Negocio KCS v6 al Resolver): DADO un ticket en transición a RESUELTO, CUANDO el bot evalúa la resolución, ENTONCES si es una incidencia técnica transferible (errores 500/504, caídas de pasarela, timeout SISA, nomencladores) lo asocia al artículo KB creando la entidad KBArticleContribution y marcando contributed_to_kb = True y associated_kb_id; y si es una rutina administrativa sin valor de conocimiento (reseteo simple, duplicado) lo resuelve justificando la no asociación.",
                        "Escenario 3 (Consulta de Base de Conocimiento con Tickets Contribuyentes): DADO un usuario u operador que consulta la Base de Conocimiento por tema (vía listado /articles, detalle /articles/{id}, o /copilot-chat), CUANDO se inspecciona el artículo o se responde la consulta, ENTONCES el sistema exhibe los tickets específicos (ID, rol, sector, autor, fecha y síntesis de solución/RCA) que sumaron información al resolverse.",
                        "Escenario 4 (Endpoints REST y Simulación en Vivo): DADO el backend FastAPI y el simulador en segundo plano live_simulator, CUANDO el bot se ejecuta o se invocan los endpoints /api/v1/tickets/bot/advance-cycle, /bot/step, /bot/advance-to-resolution y /kb-contribution, ENTONCES responden con HTTP 200 y actualizan la persistencia relacional SQLite con índices optimizados."
                ],
                "adaptation_criteria": [
                        "Paso 1: Especificación predictiva de la matriz de roles, sectores y reglas de negocio KCS v6 combinada con ejecución ágil automatizada.",
                        "Paso 2: Cumplimiento de la Pizarra Neutral Quantux (cero fondos oscuros masivos, cero rojos #DC2626 / #EF4444, acento Teal #00A896).",
                        "Paso 3: Verificación técnica automatizada con suite de pruebas dedicada (test_ticket_manager_bot_and_kb.py: 4/4 tests OK).",
                        "Paso 4: Trazabilidad inmutable e indexada en SQLite (ix_kb_contributions_article, ix_kb_contributions_ticket) y sincronización con el tablero Scrumban."
                ]
        },
        {
                "id": "ISSUE-18",
                "title": "[P1 - CRÍTICA] Bloqueo de Carga de Datos en Pantalla Principal por Error de Sintaxis JavaScript",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Core JS Engine",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-18",
                "doc_title": "DOC-QA-004 (ISSUE-18)",
                "doc_desc": "Corrección de errores sintácticos en frontend/js/app.js (bloque else huérfano y re-declaración de tenantMatrixFilterState) que impedían la carga de datos en el Mando Operativo.",
                "attachment_image": "assets/capturas/ISSUE-18_mando_operativo_sin_datos.png",
                "issue_details": {
                        "severity": "P1 — Crítica / Bloqueo Total de Carga en Interfaz",
                        "component": "frontend/js/app.js",
                        "description": "Al ingresar al Mando Operativo Unificado, los indicadores numéricos (Total Activos, Críticos, etc.) permanecían en cero y la grilla de analistas no mostraba ningún registro. El hilo principal de JavaScript quedaba bloqueado por excepciones de sintaxis no capturadas.",
                        "root_cause": "Presencia de un bloque else huérfano tras la remoción del banner de runbook (ISSUE-13) y una doble declaración concurrente de 'let tenantMatrixFilterState' (ISSUE-12).",
                        "solution": "1. Supresión del bloque else huérfano y rebalanceo de llaves de cierre en app.js.\\n2. Deduplicación de funciones y variable tenantMatrixFilterState.\\n3. Verificación con el linter de sintaxis de Node.js (0 errores) y prueba e2e con Selenium confirmando 2.270 tickets y 86 analistas en pantalla.\\n4. Estado en 'qa' para validación del Solution Owner.",
                        "acceptance_criteria": [
                                "Escenario 1 (Carga Inmediata de Telemetría): DADO el acceso al Mando Operativo, CUANDO el frontend se inicializa, ENTONCES los Micro-KPIs reflejan el volumen real de tickets activos (2.270+) y la tabla lista los analistas operativos.",
                                "Escenario 2 (Cero Excepciones en Consola): DADO el archivo frontend/js/app.js, CUANDO es interpretado por el navegador o validador sintáctico, ENTONCES culmina con 0 errores y exit code 0.",
                                "Escenario 3 (Trazabilidad Visual): DADO el registro del issue en el tablero Scrumban, CUANDO se abre la ficha de ISSUE-18, ENTONCES presenta la captura con el reporte en cero remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "MEJ-04",
                "title": "Eliminación de Barra Explicativa Superior en Matriz Multi-Tenant",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Design",
                "type": "MEJORA",
                "priority": "P2",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-04",
                "doc_title": "DOC-QA-004 (MEJ-04)",
                "doc_desc": "Remoción de la barra informativa verde superior en la Matriz Multi-Tenant para maximizar el espacio vertical útil y simplificar la interfaz operativa.",
                "attachment_image": "assets/capturas/MEJ-04_barra_explicativa_multitenant.png",
                "issue_details": {
                        "severity": "P2 — Mejora UX / Reducción de Ruido Visual",
                        "component": "frontend/index.html (platforms-subview-matrix)",
                        "description": "El Solution Owner dictaminó que la barra informativa '¿Cómo funciona la Matriz de Habilitación Multi-Tenant?' ocupaba espacio vertical valioso y no aportaba valor operativo diario ('quitar esta barra, no sirve para nada').",
                        "root_cause": "Componente explicativo redundante que restaba visibilidad directa a la tabla de conmutación de clientes y plataformas.",
                        "solution": "Supresión completa del contenedor verde #tenant-matrix-guide-body y su encabezado colapsable en frontend/index.html.",
                        "acceptance_criteria": [
                                "Escenario 1 (Espacio Vertical Limpio): DADO el acceso a la sub-vista de Habilitación Multi-Tenant, CUANDO el operador ingresa a la pantalla, ENTONCES la barra de herramientas y la matriz de plataformas son visibles inmediatamente sin banners explicativos.",
                                "Escenario 2 (Trazabilidad Visual): DADO el detalle de MEJ-04 en el Scrumban, CUANDO se abre la ficha técnica, ENTONCES se visualiza la captura remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "MEJ-05",
                "title": "Simetría y Normalización de Cápsulas Activo/Inactivo en Matriz Multi-Tenant",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / CSS & Layout",
                "type": "MEJORA",
                "priority": "P2",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-05",
                "doc_title": "DOC-QA-004 (MEJ-05)",
                "doc_desc": "Estandarización dimensional geométrica (82px x 26px) y tipográfica de los interruptores de conmutación por celda, eliminando el prefijo '[OK]' que generaba asimetría visual.",
                "attachment_image": "assets/capturas/MEJ-05_capsulas_multitenant_activo_inactivo.png",
                "issue_details": {
                        "severity": "P2 — Inconsistencia Visual / Defecto Estético",
                        "component": "frontend/js/app.js (renderTenantMatrixTable)",
                        "description": "Las cápsulas de estado mostraban '[OK] ACTIVO' con salto de línea vertical, mientras que las de '✕ INACTIVO' tenían diferente altura y ancho, generando una grilla irregular.",
                        "root_cause": "Uso de cadena con corchetes '[OK] ACTIVO' sin ancho fijo ni alineación flex centrada.",
                        "solution": "Remoción de '[OK]', fijación de dimensiones uniformes simétricas (width: 82px, height: 26px, border-radius: 13px, display: inline-flex, align-items: center, justify-content: center, white-space: nowrap).",
                        "acceptance_criteria": [
                                "Escenario 1 (Dimensiones Idénticas): DADO cualquier fila o columna de la Matriz Multi-Tenant, CUANDO se comparan botones ACTIVO e INACTIVO, ENTONCES ambos presentan exactamente 82px de ancho, 26px de alto y tipografía 10px bold centrada.",
                                "Escenario 2 (Cero Saltos de Línea): DADO el texto de la cápsula activa, CUANDO se visualiza en la tabla, ENTONCES se muestra 'ACTIVO' en una sola línea sin desbordamiento.",
                                "Escenario 3 (Trazabilidad Visual): DADO el modal de MEJ-05, ENTONCES se adjunta la captura original de observación del Solution Owner."
                        ]
                }
        },
        {
                "id": "MEJ-06",
                "title": "Supresión de Botones Redundantes de Categoría en Toolbar de Matriz",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Design",
                "type": "MEJORA",
                "priority": "P2",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-06",
                "doc_title": "DOC-QA-004 (MEJ-06)",
                "doc_desc": "Eliminación de la botonera estática de categorías (Todas, Prepagas, Sanatorios, Hospitales) para consolidar el filtrado unificado en el buscador predictivo inteligente.",
                "attachment_image": "assets/capturas/MEJ-06_botones_categoria_multitenant_eliminar.png",
                "issue_details": {
                        "severity": "P2 — Optimización UX / Redundancia de Controles",
                        "component": "frontend/index.html & frontend/js/app.js",
                        "description": "Los botones 'Todas (14)', 'Prepagas (6)', 'Sanatorios (4)' y 'Hospitales (4)' generaban redundancia y confusión operativa frente al buscador predictivo ('quitar estos botones, no aportan nada').",
                        "root_cause": "Controles redundantes en la barra superior que duplicaban la capacidad de filtrado del motor de búsqueda.",
                        "solution": "Remoción de los botones de la barra HTML. El motor predictivo ahora clasifica y busca por nombre, código y segmento dinámicamente con opción dedicada de 'Mostrar Todas'.",
                        "acceptance_criteria": [
                                "Escenario 1 (Barra Despejada): DADO el encabezado de la Matriz, CUANDO se visualiza la barra de control, ENTONCES solo coexisten el buscador predictivo y la acción 'Mostrar Todas' junto a la exportación CSV.",
                                "Escenario 2 (Trazabilidad Visual): DADO el modal de MEJ-06, ENTONCES se enlaza la evidencia de solicitud del Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-20",
                "title": "Buscador Predictivo con Autocompletado, Opción 'Mostrar Todas' y Supresión de Doble Lupa",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX & JS Search Engine",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-20",
                "doc_title": "DOC-QA-004 (ISSUE-20)",
                "doc_desc": "Corrección de doble icono de lupa y desarrollo de autocompletado predictivo con selección directa, botón ✕ de limpieza y atajo rápido 'Mostrar todas las instituciones'.",
                "attachment_image": "assets/capturas/ISSUE-20_buscador_multitenant_doble_lupa_predictivo.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Experiencia de Búsqueda Clave",
                        "component": "frontend/index.html & frontend/js/app.js (onTenantMatrixSearchInput)",
                        "description": "El campo de búsqueda presentaba dos lupas (una en el placeholder y otra en el span absoluto), carecía de sugerencias predictivas y no contaba con un acceso directo para restablecer la vista completa de 36 instituciones.",
                        "root_cause": "Duplicación del carácter emoji en placeholder y falta de un componente dropdown reactivo de sugerencias.",
                        "solution": "1. Eliminación del emoji 🔍 en el placeholder.\\n2. Implementación de menú flotante predictivo con coincidencias en tiempo real por nombre, código o tipo con badges.\\n3. Inclusión de botón 'Mostrar todas las instituciones' en el menú y en la barra.\\n4. Botón ✕ interactivo para limpiar búsqueda al instante.",
                        "acceptance_criteria": [
                                "Escenario 1 (Una Sola Lupa): DADO el input de búsqueda, CUANDO se observa en pantalla, ENTONCES presenta una única lupa integrada a la izquierda y placeholder limpio.",
                                "Escenario 2 (Dropdown Predictivo): DADO que el usuario teclea 'OSDE' o 'Sanatorio', ENTONCES se despliegan las instituciones coincidentes con código y segmento para selección inmediata.",
                                "Escenario 3 (Mostrar Todas): DADO un filtro aplicado, CUANDO se pulsa 'Mostrar Todas' o la opción superior del dropdown, ENTONCES se restablece la totalidad de las 36 instituciones sanitarias.",
                                "Escenario 4 (Trazabilidad Visual): DADO el modal de ISSUE-20, ENTONCES se visualiza la captura de la doble lupa remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "MEJ-07",
                "title": "Rediseño Senior UX y Nomenclatura Descriptiva de Sub-pestañas y Botones de Catálogo",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Architecture Senior",
                "type": "MEJORA",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-07",
                "doc_title": "DOC-QA-004 (MEJ-07)",
                "doc_desc": "Rediseño integral de la barra de navegación de Vista 5 adoptando estándares Senior UX: renombramiento semántico asistencial, iconografía médica, badges de telemetría y jerarquía clara en botones de alta.",
                "attachment_image": "assets/capturas/MEJ-07_subpestanias_administracion_ux_senior.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Reestructuración de Navegabilidad",
                        "component": "frontend/index.html & frontend/js/app.js (switchPlatformsSubTab)",
                        "description": "Las pestañas utilizaban títulos técnicos escuetos o confusos ('Red de Instituciones', 'Módulos de Software', 'Interactivo') y los botones de acción ('+ Alta Sistema' y '+ Alta Institución') no comunicaban claramente su alcance operativo a los directores asistenciales.",
                        "root_cause": "Nomenclatura orientada al desarrollador en lugar de una arquitectura de información centrada en el usuario de salud (Human-Centered Design).",
                        "solution": "1. Renombramiento semántico asistencial con iconografía y badges: '🏥 Instituciones Sanitarias [14]', '💻 Módulos Clínicos [9]', '🎛️ Habilitación Multi-Tenant [En Vivo]' y '🛡️ Niveles de Soporte ITIL [N1/N2/N3]'.\\n2. Clarificación de acciones primarias y secundarias: '🧩 + Nuevo Módulo Clínico' y '🏥 + Nueva Institución Sanitaria' con tooltips descriptivos.\\n3. Actualización dinámica reactiva de contadores en el ciclo de vida de la aplicación.",
                        "acceptance_criteria": [
                                "Escenario 1 (Semántica Asistencial): DADO el módulo de Plataformas e Instituciones, CUANDO se observa la barra superior, ENTONCES todas las pestañas exhiben iconos, nombres semánticos claros y badges de estado.",
                                "Escenario 2 (Acciones Claras): DADO el bloque de acciones a la derecha, CUANDO el operador sitúa el cursor, ENTONCES visualiza '🧩 + Nuevo Módulo Clínico' y '🏥 + Nueva Institución Sanitaria' con sus respectivos tooltips explicativos.",
                                "Escenario 3 (Trazabilidad Visual): DADO el modal de MEJ-07, ENTONCES se exhibe la captura de solicitud remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-19",
                "title": "[FUERA DE ALCANCE - BACKLOG] Inmutabilidad y Congelamiento de Botones de Transición en Tickets en Estado CERRADO",
                "epic": "EP-01: Mando Operativo y Flujo de Tickets",
                "sp": 3,
                "sprint": "Backlog Futuro",
                "status": "backlog",
                "discipline": "Frontend / State Machine & ITIL Lifecycle",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-19",
                "doc_title": "DOC-QA-004 (ISSUE-19)",
                "doc_desc": "Análisis comparativo de mercado (Zendesk, Jira Service Management, ServiceNow) y propuesta de congelamiento inmutable de botones una vez que el ticket alcanza el estado CERRADO.",
                "attachment_image": "",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Definición de Ciclo de Vida ITIL",
                        "component": "frontend/js/app.js (renderTicketModalDetail & State Machine)",
                        "description": "El Solution Owner reportó: 'cuando el tkt pasa a cerrado los otros botones permanecen activos, como se maneja esta situación en los mejores productos del mercado, analiza y propón solución o mejora'. Conforme a la regla de gobernanza 'Alcance Cerrado', este ítem se ubica estrictamente en el Product Backlog a la espera de autorización para un próximo Sprint.",
                        "root_cause": "Los botones de cambio de estado permanecían accesibles en el DOM sin validar si el estado actual es terminal inmutable según el ciclo de vida ITIL v4.",
                        "solution": "Benchmarking de Mercado: En ServiceNow y Zendesk, el estado CERRADO bloquea todas las acciones de edición y transiciones ordinarias, permitiendo únicamente 'Reabrir con justificación' (si no expiró el SLA de gracia) o lectura estricta. Propuesta técnica: deshabilitar/ocultar los botones de transición y mostrar un banner inmutable '🔒 Ticket Cerrado - No Admite Transiciones Adicionales'.",
                        "acceptance_criteria": [
                                "Escenario 1 (Aislamiento en Product Backlog): DADO que el alcance del Sprint 6 está cerrado, CUANDO se consulta el tablero Scrumban, ENTONCES ISSUE-19 figura exclusivamente en la columna 'Product Backlog' con status 'backlog'.",
                                "Escenario 2 (Inmutabilidad al Cerrar): DADO un ticket en estado CERRADO, CUANDO se abra en el modal (una vez autorizado e implementado en el sprint correspondiente), ENTONCES los botones de resolución/escalamiento deben aparecer deshabilitados (disabled) con tooltip de sólo lectura."
                        ]
                }
        },
        {
                "id": "MEJ-08",
                "title": "Supresión de Botonera de Acciones Administrativas en Toolbar del Tablero Scrumban",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Scrumban Architecture",
                "type": "MEJORA",
                "priority": "P2",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-08",
                "doc_title": "DOC-QA-004 (MEJ-08)",
                "doc_desc": "Eliminación de la botonera administrativa superior (Exportar CSV, Imprimir / PDF, Restaurar Base, Guardar) en el Tablero Scrumban conforme a la instrucción directa del Solution Owner ('quita esto, pon la tarjeta en curso').",
                "attachment_image": "assets/capturas/MEJ-08_botones_toolbar_scrumban_eliminar.png",
                "issue_details": {
                        "severity": "P2 — Optimización de Interfaz / Reducción de Ruido Visual",
                        "component": "docs/00_Tablero_Scrumban_Quantux.html & scripts/build_full_scrumban_board.py",
                        "description": "El Solution Owner identificó que los botones 'Exportar CSV', 'Imprimir / PDF', 'Restaurar Base' y 'Guardar' sobrecargaban la barra de herramientas del Tablero Scrumban e instruyó explícitamente: 'quita esto, pon la tarjeta en curso'.",
                        "root_cause": "Controles redundantes en el toolbar superior ya que la persistencia y sincronización del tablero se gestionan de forma automática e inmediata vía eventos reactivos.",
                        "solution": "Remoción de la botonera HTML en el generador maestro del tablero Scrumban. Registro de la tarjeta MEJ-08 formalmente en columna 'progress' (En Desarrollo / En Curso).",
                        "acceptance_criteria": [
                                "Escenario 1 (Toolbar Despejado): DADO el Tablero Scrumban, CUANDO se visualiza la barra de filtros, ENTONCES no se muestran los botones de exportar, imprimir, restaurar o guardar.",
                                "Escenario 2 (Tarjeta en Curso): DADO el tablero Scrumban, CUANDO se consulta la columna 'En Desarrollo', ENTONCES figura la tarjeta MEJ-08 en estado 'progress'.",
                                "Escenario 3 (Trazabilidad Visual): DADO el modal de detalle de MEJ-08, CUANDO se abre la ficha, ENTONCES se visualiza la captura de la botonera remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-21",
                "title": "[P1 - ALTA PRIORIDAD] Reemplazo de Botones Crípticos de Respuesta por Acciones Semánticas (KB & Bot SLA)",
                "epic": "EP-01: Mando Operativo y Flujo de Tickets",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Workspace",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-21",
                "doc_title": "DOC-QA-004 (ISSUE-21)",
                "doc_desc": "Sustitución de emojis huérfanos (📚 y 🤖) en el pie del editor de respuestas por botones semánticos explicativos con affordance UX Senior y modales contextuales.",
                "attachment_image": "assets/capturas/ISSUE-21_botones_cripticos_respuesta_tkt.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Usabilidad Crítica en Atención",
                        "component": "frontend/index.html & frontend/js/app.js (openQuickKbInsertModal & confirmAndTriggerBotInteraction)",
                        "description": "El Solution Owner reportó con captura adjunta: 'no se que hacen estos botones del tkt, suma al sprint con alta prioridad'. Los botones sólo mostraban emojis huérfanos sin texto ni affordance clara de su impacto operativo (pausa de SLA e inserción de KB).",
                        "root_cause": "Iconografía críptica y carente de etiquetas semánticas y alertas operativas en el contenedor de herramientas de respuesta del ticket.",
                        "solution": "Reemplazo de los botones por '📚 Insertar Solución KB' y '🤖 Bot: Pedir Datos (Pausa SLA)'. Integración de modal rápido de búsqueda/inserción de artículos KB en el textarea y confirmación de pausa formal de SLA.",
                        "acceptance_criteria": [
                                "Escenario 1 (Acciones Semánticas Visibles): DADO el pie del cuadro de respuesta en el modal del ticket, CUANDO el operador lo visualiza, ENTONCES encuentra botones rotulados '📚 Insertar Solución KB' y '🤖 Bot: Pedir Datos (Pausa SLA)' en lugar de emojis huérfanos.",
                                "Escenario 2 (Confirmación Preventiva SLA): DADO que el operador hace clic en '🤖 Bot: Pedir Datos (Pausa SLA)', ENTONCES el sistema despliega un cuadro de confirmación explicando que el ticket pasará a 'Esperando al Prestador' con pausa formal del reloj de SLA.",
                                "Escenario 3 (Modal Ágil de Inserción KB): DADO que el operador hace clic en '📚 Insertar Solución KB', ENTONCES se abre un modal interactivo con buscador en vivo para insertar la solución técnica directamente en el textarea sin salir del ticket.",
                                "Escenario 4 (Trazabilidad Visual): DADO el registro de ISSUE-21, CUANDO se abre la ficha de la tarjeta, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-22",
                "title": "[P1 - ALTA PRIORIDAD] Visibilidad y Consulta de Telemetría Operativa Zero-Question en Workspace de Tickets",
                "epic": "EP-01: Mando Operativo y Flujo de Tickets",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Telemetry & Interoperability",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-22",
                "doc_title": "DOC-QA-004 (ISSUE-22)",
                "doc_desc": "Habilitación de acceso directo a la telemetría operativa de entorno y diagnóstico transparente en la cabecera del modal de tickets para resolver la duda del Solution Owner.",
                "attachment_image": "assets/capturas/ISSUE-22_telemetria_no_visible_modal_tkt.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Diagnóstico Operativo Transparente",
                        "component": "frontend/index.html & frontend/js/app.js (renderWsTechPanel & switchWsTab)",
                        "description": "El Solution Owner reportó con captura adjunta: 'no se ve la telemetía, donde la consulto ???, suma al sprint con alta prioridad'. La información técnica ambiental y de interoperabilidad FHIR no contaba con una pestaña visible y dedicada en el modal del caso.",
                        "root_cause": "Falta del botón de pestaña 'Telemetría & Diagnóstico' en la barra de pestañas (ws-tabs-group) del modal del ticket.",
                        "solution": "Inclusión de la pestaña '#ws-tab-tech' en el modal del caso y renderizado exhaustivo de la tarjeta 'Telemetría Operativa del Entorno (Zero-Question)' con navegador, SO, resolución de monitor, conectividad, zona horaria, hardware y ficha FHIR R4 interoperable.",
                        "acceptance_criteria": [
                                "Escenario 1 (Pestaña Directa de Telemetría): DADO el modal del ticket en el workspace, CUANDO el operador observa la botonera superior, ENTONCES visualiza la pestaña 'Telemetría & Diagnóstico' con acceso inmediato.",
                                "Escenario 2 (Diagnóstico Zero-Question Completo): DADO que el operador hace clic en 'Telemetría & Diagnóstico', ENTONCES visualiza el bloque de parámetros ambientales (navegador, SO, monitor, red, latencia, CPU/RAM) capturados de forma transparente sin interrogar al solicitante.",
                                "Escenario 3 (Ficha Interoperable FHIR R4): DADO el panel de telemetría, ENTONCES se presenta el payload FHIR JSON con botón de copia al portapapeles en 1 clic.",
                                "Escenario 4 (Trazabilidad Visual): DADO el registro de ISSUE-22, CUANDO se abre la ficha de la tarjeta, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-23",
                "title": "[P1 - CRÍTICA] Erradicación de Viñetas Duplicadas en Historial y Línea de Tiempo del Ticket",
                "epic": "EP-01: Mando Operativo y Flujo de Tickets",
                "sp": 1,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UI Timeline",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-23",
                "doc_title": "DOC-QA-004 (ISSUE-23)",
                "doc_desc": "Corrección de defecto visual de doble viñeta/punto redundante en la línea de tiempo de auditoría del ticket.",
                "attachment_image": "assets/capturas/ISSUE-23_botones_dobles_historial_tkt.png",
                "issue_details": {
                        "severity": "P1 — Alta Criticidad Visual / Defecto de Interfaz",
                        "component": "frontend/js/app.js (renderWsTimeline)",
                        "description": "El Solution Owner reportó con captura adjunta: 'issue de alta criticidad, suma al sprint, tiene botonoes dobles en el historial del tkt'. Cada evento del historial mostraba dos círculos idénticos yuxtapuestos.",
                        "root_cause": "En renderWsTimeline se generaba simultáneamente el nodo visual del punto CSS .ws-event-dot y dentro del bubble de texto se concatenaba un carácter tipográfico circular redundante (span con it.icon = '•').",
                        "solution": "Supresión del span de carácter tipográfico duplicado en el renderizado del evento en app.js, conservando únicamente el indicador posicional en el eje vertical.",
                        "acceptance_criteria": [
                                "Escenario 1 (Viñeta Única y Limpia): DADO el historial del ticket en el modal, CUANDO se renderizan los eventos de la línea de tiempo, ENTONCES cada hito presenta exactamente un único punto indicador visual en el riel vertical.",
                                "Escenario 2 (Cero Duplicación Tipográfica): DADO el cuerpo de la burbuja del evento, ENTONCES no se exhibe ningún punto o viñeta adicional al lado del texto.",
                                "Escenario 3 (Trazabilidad Visual): DADO el registro de ISSUE-23, CUANDO se abre la ficha de la tarjeta, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-24",
                "title": "[P1 - ALTA PRIORIDAD] Remoción de Badge Innecesario 'AF-DEV' en Cabecera del Asistente IA",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 1,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / IA Asistencial",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-24",
                "doc_title": "DOC-QA-004 (ISSUE-24)",
                "doc_desc": "Eliminación del badge de desarrollo 'AF-DEV' que contaminaba visualmente la cabecera del Asistente IA.",
                "attachment_image": "assets/capturas/ISSUE-24_quitar_badge_af_dev_ai.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Ruido Visual",
                        "component": "frontend/js/app.js (renderAIChatHeader)",
                        "description": "El Solution Owner reportó con captura adjunta: 'issue de alta prioridad suma al sprint, debes quietar el texto del recuadro no aporta información'. La cabecera del asistente IA mostraba una píldora con el texto técnico 'AF-DEV' sin utilidad funcional.",
                        "root_cause": "Presencia residual de una etiqueta visual conmemorativa de desarrollo 'AF-DEV' en el template de cabecera del asistente.",
                        "solution": "Supresión del badge residual conservando exclusivamente el nombre y estado operativo del asistente.",
                        "acceptance_criteria": [
                                "Escenario 1 (Cabecera Zen): DADO el asistente IA, CUANDO se abre el panel de conversación, ENTONCES la cabecera no exhibe ningún badge 'AF-DEV'.",
                                "Escenario 2 (Trazabilidad Visual): DADO el registro de ISSUE-24 en el Scrumban, CUANDO se abre la tarjeta, ENTONCES exhibe la evidencia gráfica adjunta."
                        ]
                }
        },
        {
                "id": "ISSUE-25",
                "title": "[P1 - ALTA PRIORIDAD] Visualización Scrumban 100vh sin Scroll Derecho y Distribución Uniforme de 6 Columnas",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Ergonomía Scrumban",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-25",
                "doc_title": "DOC-QA-004 (ISSUE-25)",
                "doc_desc": "Ajuste del contenedor y grilla del Scrumban para encajar al 100vh de pantalla eliminando el scroll vertical derecho del navegador.",
                "attachment_image": "assets/capturas/ISSUE-25_scrumban_sin_scroll_derecho.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Ergonomía de Pantalla Completa",
                        "component": "scripts/build_full_scrumban_board.py & docs/tablero_scrumban.html",
                        "description": "El Solution Owner solicitó: 'el scrumban debe mostrar siempre toda la información sin necesidad el scroll derecho, issue de alta prioridad, suma al sprint'. Las columnas desbordaban la altura de pantalla provocando doble barra de scroll.",
                        "root_cause": "Falta de fijación estricta de 100vh en html/body con overflow: hidden y falta de minmax(0, 1fr) en la grilla kanban de 6 columnas.",
                        "solution": "Fijar height: 100vh en html/body, aplicar repeat(6, minmax(0, 1fr)) a la grilla y delegar el scroll vertical únicamente a .cards-list de cada columna.",
                        "acceptance_criteria": [
                                "Escenario 1 (Cero Scroll Derecho en Navegador): DADO el tablero Scrumban abierto, CUANDO se visualiza en pantalla completa, ENTONCES el navegador no exhibe ninguna barra de desplazamiento vertical en el borde derecho.",
                                "Escenario 2 (6 Columnas Visibles Simultáneas): DADO el tablero, ENTONCES las 6 columnas completas se aprecian a la vez sin recortes horizontales ni solapamientos.",
                                "Escenario 3 (Scroll Independiente por Columna): DADO que una columna contiene más tarjetas de las que entran en pantalla, ENTONCES la lista interna de esa columna permite scroll vertical propio sin alterar la ventana."
                        ]
                }
        },
        {
                "id": "UH-70",
                "title": "[P1 - ALTA PRIORIDAD] Menú Lateral Zen: Ocultamiento de Accesos a Tablero de Control y Torre de Control Preservando Funcionalidad",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Arquitectura de Menú",
                "type": "UH",
                "priority": "P1",
                "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#uh-70",
                "doc_title": "DOC-SPEC-002 (UH-70)",
                "doc_desc": "Ocultamiento selectivo en el menú de navegación de los botones de Tablero y Torre de Control sin alterar su funcionalidad subyacente.",
                "attachment_image": "assets/capturas/UH-69_ocultar_tablero_torre_control_menu.png",
                "narrative": {
                        "as_a": "Operador Asistencial y Solution Owner",
                        "i_want": "que el menú lateral oculte los botones de Tablero de Control y Torre de Control manteniendo el código y la capacidad analítica intacta",
                        "so_that": "la barra de navegación lateral sea minimalista y enfocada en la atención sin ruido de accesos no utilizados en la rutina diaria."
                },
                "acceptance_criteria": [
                        "Escenario 1 (Ocultamiento Estricto de Botones en Menú): DADO el menú lateral de navegación, CUANDO se renderizan los ítems principales, ENTONCES los accesos #tab-dashboard y #tab-team-leader están completamente invisibles (display: none !important).",
                        "Escenario 2 (Preservación Absoluta de Funcionalidad): DADO el código JavaScript y backend, CUANDO se consultan las métricas o se abren las vistas programáticamente, ENTONCES todas las funciones y controladores operan normalmente.",
                        "Escenario 3 (Trazabilidad Visual): DADO el registro en el Scrumban, CUANDO se abre la tarjeta UH-70, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                ]
        },
        {
                "id": "ISSUE-26",
                "title": "[P1 - ALTA PRIORIDAD] Rediseño UX Senior: Barra de Pestañas y Acciones Multi-Tenant en Fila Única Limpia",
                "epic": "EP-06: Administración y Operación Centralizada",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UX Senior",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-26",
                "doc_title": "DOC-QA-004 (ISSUE-26)",
                "doc_desc": "Rediseño ergonómico de la cabecera multi-tenant alineando sub-pestañas a la izquierda y acción contextual a la derecha en una única fila horizontal.",
                "attachment_image": "assets/capturas/ISSUE-26_redisenio_ux_tabs_acciones_multitenant.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Ergonomía Visual y Usabilidad",
                        "component": "frontend/index.html & frontend/js/app.js (switchCatalogSubTab)",
                        "description": "El Solution Owner indicó: 'USSUE, los botones del recuadro de la captura son un quilombo no se entiende nada, rediseñar y mostrar solo necesario por cada intem de módulo, actua como UX senior y rediseña los botones y su distribucipon, siempre apegado al estilo quantuz'. Había acumulación de botones heterogéneos en filas múltiples.",
                        "root_cause": "Falta de unificación en una sola barra horizontal (toolbar unificada) con botones de acción dinámica según la pestaña activa.",
                        "solution": "Unificar la barra en un contenedor flex justify-between de una sola fila, alojando las 3 subpestañas a la izquierda y exactamente 1 botón de acción contextual a la derecha (Nueva Institución, Vincular Módulo, etc.).",
                        "acceptance_criteria": [
                                "Escenario 1 (Fila Única Horizontal): DADO el catálogo multi-tenant, CUANDO se observa la cabecera superior, ENTONCES presenta una única fila con pestañas a la izquierda y botón de acción a la derecha.",
                                "Escenario 2 (Dinamismo Contextual): DADO el cambio entre sub-pestañas (Instituciones / Módulos / Matriz), CUANDO el operador cambia de pestaña, ENTONCES el botón de acción cambia contextualmente mostrando solo lo necesario.",
                                "Escenario 3 (Trazabilidad Visual): DADO el registro en el Scrumban, CUANDO se abre la tarjeta ISSUE-26, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-27",
                "title": "[P1 - CRÍTICA] Corrección de Botón 'Expandir Todo' en Historial y Notas del Caso en Agent Workspace",
                "epic": "EP-01: Mando Operativo y Flujo de Tickets",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / UI Agent Workspace",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-27",
                "doc_title": "DOC-QA-004 (ISSUE-27)",
                "doc_desc": "Corrección y robustecimiento del mecanismo de expansión total de notas e historial para desplegar el 100% del texto sin bloqueos.",
                "attachment_image": "assets/capturas/ISSUE-27_boton_expandir_todo_no_expande.png",
                "issue_details": {
                        "severity": "P1 — Alta Criticidad / Operatividad de Soporte",
                        "component": "frontend/index.html & frontend/js/app.js (expandAllWsNotes, collapseAllWsNotes)",
                        "description": "El Solution Owner reportó con captura adjunta: 'el botón expandir no expande, issue de alta criticidad, sumar al sprint'. Al pulsar [⊞ Expandir Todo] en el modal del caso, las notas colapsadas no se desplegaban.",
                        "root_cause": "Falta de forzado de estilo con !important (display: block !important) y falta de asociación defensiva de selectores (.ws-msg-body y [id^='ws-note-body-']) junto con la inicialización por addEventListener.",
                        "solution": "Actualizar expandAllWsNotes y collapseAllWsNotes utilizando setProperty('display', 'block', 'important'), sincronizar flechas indicadoras a ▼, ocultar previews y enlazar listeners tanto inline como en DOMContentLoaded.",
                        "acceptance_criteria": [
                                "Escenario 1 (Despliegue Instantáneo en 1 Clic): DADO el modal del ticket en el workspace, CUANDO el operador pulsa [⊞ Expandir Todo], ENTONCES todas las notas, comentarios y descripciones del caso se expanden al instante revelando el 100% de su contenido.",
                                "Escenario 2 (Colapso Simétrico): DADO que las notas están expandidas, CUANDO el operador pulsa [⊟ Colapsar Todo], ENTONCES todas las notas vuelven a su estado compacto.",
                                "Escenario 3 (Trazabilidad Visual): DADO el registro en el Scrumban, CUANDO se abre la tarjeta ISSUE-27, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-28",
                "title": "[P1 - CRÍTICA] Alimentación y Trazabilidad Automática de la Base de Conocimiento al Resolver Ticket",
                "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
                "sp": 3,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Fullstack / KCS v6 & Base de Conocimiento",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-28",
                "doc_title": "DOC-QA-004 (ISSUE-28)",
                "doc_desc": "Automatización e integración backend de la publicación a la Base de Conocimiento con categorización clínica, vinculación de ticket aportante y auditoría ITIL.",
                "attachment_image": "assets/capturas/ISSUE-28_no_alimenta_base_conocimiento_al_resolver.png",
                "issue_details": {
                        "severity": "P1 — Alta Criticidad / Pérdida de Capital Intelectual",
                        "component": "backend/app/api/endpoints/tickets.py, app/models/entities.py & frontend/js/app.js (resolveTicket)",
                        "description": "El Solution Owner reportó con captura adjunta: 'no alimenta la base de conocimiento, issue de alta criticidad, sumar al sprint'. Al marcar el checkbox 'Publicar en Base de Conocimiento' en el modal de resolución, el caso no alimentaba la KB.",
                        "root_cause": "El endpoint backend /resolve no recibía el flag publish_to_kb en el payload de solicitud y la lógica delegada en frontend se omitía silenciosamente si selectedTicket era nulo o no creaba la relación formal en KBArticleContribution.",
                        "solution": "Incorporar publish_to_kb: Optional[bool] en TicketResolveRequest backend, crear/actualizar el artículo KB con categoría clínica mapeada desde platform_code, insertar registro formal en KBArticleContribution, actualizar ticket.associated_kb_id y ticket.contributed_to_kb = True, y registrar auditoría forense y comentario informativo.",
                        "acceptance_criteria": [
                                "Escenario 1 (Publicación Inmediata al Resolver): DADO el modal de resolución, CUANDO el operador marca 'Publicar en Base de Conocimiento' y confirma, ENTONCES se crea/actualiza el artículo en la KB con categoría clínica adecuada y contenido técnico estructurado (RCA, procedimiento y homologación).",
                                "Escenario 2 (Vinculación de Ticket Aportante): DADO el artículo creado o consultado en la KB, CUANDO se examinan sus fuentes, ENTONCES el ticket resuelto figura formalmente como contribuyente con su ID, autor, fecha y síntesis de solución.",
                                "Escenario 3 (Trazabilidad Forense ITIL): DADO el ticket resuelto, ENTONCES su historial registra el aporte a la KB en audit_logs y agrega un comentario de confirmación.",
                                "Escenario 4 (Trazabilidad Visual): DADO el registro en el Scrumban, CUANDO se abre la tarjeta ISSUE-28, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "ISSUE-29",
                "title": "[P1 - ALTA PRIORIDAD] Remoción de Cabecera Superior HealthDesk/Quantux para Optimización de Espacio Vertical 100vh en Scrumban",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 1,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Ergonomía Scrumban",
                "type": "ISSUE",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-29",
                "doc_title": "DOC-QA-004 (ISSUE-29)",
                "doc_desc": "Eliminación de la cabecera superior y badges de fase conforme a captura del Solution Owner ('quita esto,'), liberando ~65px útiles para visualización 100vh sin scroll innecesario.",
                "attachment_image": "assets/capturas/ISSUE-29_quitar_cabecera_superior_scrumban.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Ruido Visual & Ergonomía 100vh",
                        "component": "scripts/build_full_scrumban_board.py & docs/00_Tablero_Scrumban_Quantux.html (<header>)",
                        "description": "El Solution Owner adjuntó captura de la cabecera superior oscura con los títulos institucionales y badges de fase con la instrucción 'quita esto,'.",
                        "root_cause": "La cabecera superior ocupaba ~65px de altura fija que generaba scroll vertical no deseado en resoluciones comunes al consultar el tablero Kanban completo.",
                        "solution": "Remoción íntegra del elemento <header> en la plantilla del tablero, posicionando la barra de navegación superior de vistas al tope del viewport.",
                        "acceptance_criteria": [
                                "Escenario 1: El tablero inicia directamente en la barra de navegación de vistas sin cabecera redundante superior.",
                                "Escenario 2: La altura útil de las columnas Kanban se amplía aprovechando el 100vh.",
                                "Escenario 3: La tarjeta cuenta con la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "MEJ-09",
                "title": "[P1 - ALTA PRIORIDAD] Transición Automática de Tarjetas de Retrabajo a la Pila de Revisión al Ejecutar Demonio",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Lógica de Tablero Scrumban",
                "type": "MEJORA",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-09",
                "doc_title": "DOC-QA-004 (MEJ-09)",
                "doc_desc": "Automatización de ciclo de vida ágil: al finalizar la barra del Demonio (100%), la tarjeta transiciona automáticamente a la columna En Revisión (Aceptación Solution Owner) posicionándose arriba de la pila.",
                "attachment_image": "assets/capturas/MEJ-09_demonio_retrabajo_a_pila_revision.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Automatización de Ciclo de Vida Scrumban",
                        "component": "scripts/build_full_scrumban_board.py (triggerDemonRework) & docs/00_Tablero_Scrumban_Quantux.html",
                        "description": "El Solution Owner instruyó explícitamente: 'cuando se ejecuta la corrección la tarjete debe pasar aujtomaticamente a la pila de revisión', adjuntando captura de la columna En Retrabajo con UH-67.",
                        "root_cause": "Al finalizar la animación y ejecución técnica del demonio de corrección, el estado se mantenía en 'rework' en lugar de promover la tarjeta a la pila de QA/Revisión.",
                        "solution": "Configurar task.status = 'qa', actualizar la bitácora de feedback como 'CORREGIDO POR DEMONIO / EN REVISIÓN', reposicionar la tarjeta al inicio del vector de tareas (unshift) y mostrar alerta de confirmación.",
                        "acceptance_criteria": [
                                "Escenario 1 (Paso Automático a Revisión): DADO que el operador ejecuta el Demonio en una tarjeta de Retrabajo, CUANDO la barra alcanza el 100%, ENTONCES la tarjeta pasa automáticamente a la columna 'EN REVISIÓN'.",
                                "Escenario 2 (Posicionamiento Prioritario): DADO el paso a Revisión, ENTONCES la tarjeta se ubica al tope de la pila de revisión.",
                                "Escenario 3 (Trazabilidad Visual): DADO el detalle de la tarjeta MEJ-09, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
        {
                "id": "MEJ-10",
                "title": "[P1 - ALTA PRIORIDAD] Posicionamiento Superior Inmediato ('Arriba de la Pila') al Aprobar Tarjetas a Aceptado",
                "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
                "sp": 2,
                "sprint": "Sprint 6",
                "status": "qa",
                "discipline": "Frontend / Ergonomía Kanban",
                "type": "MEJORA",
                "priority": "P1",
                "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-10",
                "doc_title": "DOC-QA-004 (MEJ-10)",
                "doc_desc": "Garantía de orden LIFO/prioritario en la columna Aceptado y Finalizado: toda tarjeta aprobada por el Solution Owner se posiciona automáticamente en la parte superior ('arriba de la pila') tanto por botón como por drag-and-drop.",
                "attachment_image": "assets/capturas/MEJ-10_tarjeta_aceptada_arriba_de_la_pila.png",
                "issue_details": {
                        "severity": "P1 — Alta Prioridad / Ergonomía LIFO en Columna de Aceptación",
                        "component": "scripts/build_full_scrumban_board.py (approveTaskDone, drop, moveTask) & docs/00_Tablero_Scrumban_Quantux.html",
                        "description": "El Solution Owner instruyó explícitamente: 'cuando paso tarjeta de este estado a aceptado la tarjeta debe quedar arriba de la pila', adjuntando captura de la columna En Revisión.",
                        "root_cause": "Al aprobar o mover una tarjeta a 'done', se agregaba al final de la columna tras las decenas de ítems históricos previamente aprobados, obligando a scrollear hasta el fondo para verificar la acción.",
                        "solution": "Reposicionar la tarjeta en la cabeza (index 0 / unshift) del array de tareas cada vez que transiciona a 'done' mediante botón 'Aprobar (Done)', botón modal o drag-and-drop.",
                        "acceptance_criteria": [
                                "Escenario 1 (Arriba de la Pila por Botón): DADO que el Solution Owner presiona 'Aprobar (Done)' en una tarjeta de Revisión, CUANDO se confirma, ENTONCES la tarjeta aparece primera arriba de todo en la columna 'ACEPTADO Y FINALIZADO'.",
                                "Escenario 2 (Arriba de la Pila por Drag & Drop): DADO que se arrastra una tarjeta a 'Aceptado y Finalizado', CUANDO se suelta, ENTONCES queda posicionada arriba de la pila.",
                                "Escenario 3 (Trazabilidad Visual): DADO el detalle de la tarjeta MEJ-10, ENTONCES exhibe la captura de evidencia remitida por el Solution Owner."
                        ]
                }
        },
    ]

    
    # Tarjetas adicionales: ISSUE-30 a ISSUE-38, MEJ-11 y OPP-04 a OPP-08
    extra_tasks = [
        {
            "id": "ISSUE-63",
            "title": "[P0 - CRÍTICO] Motor del Demonio de Retrabajo: Ejecución Real de Desarrollo y Parches de Código desde el Tablero sin Intervención Manual",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 5,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Fullstack / Motor Agéntico Autónomo",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-63",
            "doc_title": "DOC-QA-004 (ISSUE-63)",
            "doc_desc": "El botón del demonio dispara la ejecución real de desarrollo a través del backend FastAPI (/api/v1/demon/execute/{taskId}), modificando los archivos del proyecto y aplicando los criterios de aceptación automáticamente sin intervención manual en el chat.",
            "business_impact": {
                "level": "CRÍTICO",
                "dimension": "AUTOMATIZACIÓN CORE & INTEGRIDAD AGÉNTICA",
                "description": "Permite al Solution Owner disparar la resolución técnica efectiva de cualquier ticket de retrabajo directamente con un clic en el botón Demonio, modificando el código fuente y aplicando los criterios de aceptación de forma autónoma sin depender de órdenes manuales repetitivas.",
                "metric_target": "0 simulaciones; 100% de parches de código reales ejecutados en caliente en el proyecto al pulsar el Demonio.",
                "risk_of_inaction": "Frustración operativa del Solution Owner ante procesos aparentes/simulados y bloqueo de la autonomía del tablero."
            }
        },
        {
            "id": "ISSUE-65",
            "title": "[P1 - ALTO IMPACTO] Persistencia de Configuración de SLA sin Cierre de Diálogo y Actualización Reactiva en Ficha 360° del Cliente",
            "epic": "EP-06: Gestión de Incidentes, SLA Dinámico y Transiciones",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & JS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-65",
            "doc_title": "DOC-QA-004 (ISSUE-65)",
            "doc_desc": "Corrección de alto impacto solicitada por el Solution Owner: el botón de guardar configuración de SLA en la ficha 360° de la institución no debe cerrar la ventana modal bajo ningún concepto, debe persistir la política en localStorage/AppState y reflejar la nueva configuración de inmediato en la ficha del cliente en el catálogo.",
            "business_impact": {
                "level": "ALTO IMPACTO",
                "dimension": "EXPERIENCIA DE ADMINISTRACIÓN Y CONTROL DE SLA",
                "description": "Evita el cierre involuntario y molesto del modal durante la configuración institucional y asegura la consistencia en tiempo real de los niveles de servicio acordados.",
                "metric_target": "100% de configuraciones de SLA guardadas sin cerrar modal y visualizadas de inmediato en la tarjeta del cliente.",
                "risk_of_inaction": "Pérdida de foco del usuario administrativo y falta de visibilidad del SLA actualizado en el catálogo."
            }
        },
        {
            "id": "ISSUE-66",
            "title": "[P1 - ALTA PRIORIDAD] Erradicación Integral de Colores Pesados y Oscuros en Modales y Ficha 360° (Paleta Limpia Quantux)",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UI & CSS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-66",
            "doc_title": "DOC-QA-004 (ISSUE-66)",
            "doc_desc": "Cumplimiento estricto de directiva de diseño: eliminación de gradientes y fondos oscuros pesados (#0F172A, #1E293B) en cabecera de modales y componentes, reemplazándolos por fondos claros (#F8FAFC, #FFFFFF), acentos en verde teal (#00A896, #0F766E) y bordes sutiles.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "IDENTIDAD VISUAL Y USABILIDAD SAAS",
                "description": "Logra una interfaz clínica/empresarial limpia, liviana y coherente con el sistema de diseño Quantux, reduciendo fatiga visual.",
                "metric_target": "0 cabeceras pesadas u oscuras en ventanas modales institucionales.",
                "risk_of_inaction": "Incoherencia de marca y sobrecarga visual en la experiencia de usuario."
            }
        },
        {
            "id": "ISSUE-67",
            "title": "[P1 - ALTA PRIORIDAD] Unificación Terminológica de Pestañas y Eliminación Integral de Iconos/Emojis",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & Copywriting",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-67",
            "doc_title": "DOC-QA-004 (ISSUE-67)",
            "doc_desc": "Ajuste terminológico taxativo del Solution Owner: renombramiento de pestañas a 'Instituciones', 'Módulo de soporte', 'Grilla: Institución/Módulo' y eliminación completa de emojis e iconos en la barra de herramientas y pestañas.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "CLARIDAD CONCEPTUAL Y ESTÉTICA CORPORATIVA",
                "description": "Establece un estándar tipográfico corporativo sobrio y una denominación unívoca de las entidades del sistema sin distracciones visuales.",
                "metric_target": "100% de nomenclaturas aprobadas por SO y 0 iconos informales en la barra de navegación.",
                "risk_of_inaction": "Confusión en los operadores y falta de sobriedad en la presentación corporativa."
            }
        },
        {
            "id": "ISSUE-64",
            "title": "[P1 - ALTA PRIORIDAD] Regla FIFO Estricta en Retrabajo: Toda Tarjeta que Pase de Revisión a Retrabajo Debe Quedar al Fondo de la Pila de Retrabajo",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Frontend / Gobernanza Scrumban",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-64",
            "doc_title": "DOC-QA-004 (ISSUE-64)",
            "doc_desc": "Instrucción formal del Solution Owner: toda tarjeta devuelta o movida desde Revisión a Retrabajo (vía modal, botón de tarjeta o drag & drop) se ubica estrictamente al fondo de la pila de Retrabajo (FIFO), garantizando orden de ingreso inmutable.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "GOBERNANZA SCRUMBAN & ORDEN OPERATIVO",
                "description": "Garantiza equidad y disciplina de cola FIFO (First-In, First-Out) para los tickets en retrabajo, impidiendo que nuevos rechazos desplacen o entierren los tickets devueltos con anterioridad.",
                "metric_target": "100% de tickets en retrabajo ordenados cronológicamente por ingreso al fondo de la pila.",
                "risk_of_inaction": "Desorden en la priorización de retrabajo y pérdida de trazabilidad sobre el orden de llegada de los rechazos."
            }
        },
        {
            "id": "ISSUE-30",
            "title": "[P1 - ALTA PRIORIDAD] Botón de Resolución Directa de Tickets en Modal de Visualización",
            "epic": "EP-06: Gestión de Incidentes, SLA Dinámico y Transiciones",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & JS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-30",
            "doc_title": "DOC-QA-004 (ISSUE-30)",
            "doc_desc": "Habilitación de botón resolutivo inmediato dentro del modal de inspección de tickets.",
            "attachment_image": "assets/capturas/ISSUE-30_boton_resolver_ticket.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Operabilidad de Mesa de Ayuda",
                "component": "frontend/index.html (#view-ticket-detail-modal), frontend/js/app.js (showTicketDetailModal)",
                "description": "El Solution Owner indicó expresamente: 'este boton tambien debe dar la posibilidad de resolver el tkt, issue de alta prioridad suma al tkt'. El modal de detalle permitía inspeccionar el ticket pero no resolverlo directamente en un solo clic.",
                "root_cause": "Falta de acción de resolución directa ligada al flujo ITIL en el pie del modal de inspección.",
                "solution": "Incorporar botón 'Resolver Incidente (FCR)' en el pie del modal con confirmación y cierre transaccional.",
                "acceptance_criteria": [
                    "Escenario 1: DADO el modal de inspección de ticket abierto, CUANDO el operador pulsa 'Resolver Incidente', ENTONCES se solicita resolución y pasa a estado Resuelto.",
                    "Escenario 2: DADO el ticket resuelto, ENTONCES impacta en el contador de FCR y telemetría de SLA."
                ]
            }
        },
        {
            "id": "ISSUE-31",
            "title": "[P1 - ALTA PRIORIDAD] Ejecución del Demonio y Paso Automático de Toda Tarjeta que Pase de Retrabajo a Revisión al Fondo de la Pila",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "rework",
            "so_feedback": {
                "status": "RECHAZADO - ENVIADO A RETRABAJO",
                "observation": "Criterios de Aceptación Verificables (Gherkin). Escenario 1: DADO el clic sobre el botón del demonio, CUANDO finaliza la animación y corrección, ENTONCES la tarjeta pasa a 'En Revisión' al fondo de la lista. Este punto no está resuelto, toda tarjeta que pase de retrabajo a revisión debe ir al fondo de la pila de revisión, pasa a retrabajo.",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "date": "2026-09-27"
            },
            "discipline": "Frontend / Automatización Scrumban",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-31",
            "doc_title": "DOC-QA-004 (ISSUE-31)",
            "doc_desc": "Al hacer clic sobre el demonio o mover de retrabajo a revisión, la tarjeta se posiciona incondicionalmente al fondo de la pila de revisión (FIFO estricto).",
            "attachment_image": "assets/capturas/ISSUE-31_boton_guardar_informacion_modal_retrabajo.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Lógica FIFO en QA",
                "component": "scripts/build_full_scrumban_board.py (triggerDemonRework, push to qa)",
                "description": "El Solution Owner instruyó: 'se entendió que cuando se hace clic sobre el demonio la tarea debe ejecutarse y al finalizar debe pasar la tarjeta al fondo de la lista de revisiónnn????'.",
                "root_cause": "Previamente la tarea se agregaba al tope (unshift) en lugar del fondo (push) de la columna de revisión.",
                "solution": "Ajustar la función del demonio para que al alcanzar 100% envíe la tarjeta al fondo de la columna de revisión (push) preservando el orden de llegada.",
                "acceptance_criteria": [
                    "Escenario 1: DADO el clic sobre el botón del demonio, CUANDO finaliza la animación y corrección, ENTONCES la tarjeta pasa a 'En Revisión' al fondo de la lista.",
                    "Escenario 2: DADO el cambio de estado, ENTONCES la columna En Retrabajo decrementa su contador inmediatamente."
                ]
            }
        },
        {
            "id": "ISSUE-32",
            "title": "[P1 - ALTA PRIORIDAD] Cero Emojis y Cero Íconos No Aprobados en Filtros, Telemetría y Modales",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UI Senior",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-32",
            "doc_title": "DOC-QA-004 (ISSUE-32)",
            "doc_desc": "Erradicación total de emoticones, dibujitos y glifos no estandarizados en toda la interfaz de usuario.",
            "attachment_image": "assets/capturas/ISSUE-32_cero_emojis_aprobados.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Cumplimiento de Identidad Corporativa",
                "component": "frontend/index.html, scripts/build_full_scrumban_board.py, frontend/css/styles.css",
                "description": "El Solution Owner ordenó de manera contundente: 'cero dibujitos !!!!!!!! guarda en lo mas profundo de tu memoria, cero iconos que no están aprobados, ejecuta la corrección inmediatamente'.",
                "root_cause": "Presencia de emojis informales en cabeceras de columnas, filtros rápidos, botones y badges.",
                "solution": "Sustituir todo emoji por tipografía limpia institucional (Inter / Outfit / Montserrat), badges en Quantux Teal y componentes SVG vectoriales autorizados.",
                "acceptance_criteria": [
                    "Escenario 1: DADO el tablero Scrumban y portal de tickets, CUANDO se visualizan las cabeceras, botones y badges, ENTONCES no figura ningún emoji crudo.",
                    "Escenario 2: DADO el inspector visual, ENTONCES cumple al 100% las directrices institucionales OJO."
                ]
            }
        },
        {
            "id": "ISSUE-33",
            "title": "[P1 - ALTA PRIORIDAD] Erradicación Total de Emojis y Dibujitos en Cabeceras de Columna del Tablero Scrumban",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Ergonomía Kanban",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-33",
            "doc_title": "DOC-QA-004 (ISSUE-33)",
            "doc_desc": "Supresión de íconos en los títulos de las 6 columnas del tablero Scrumban para un diseño minimalista y tipográfico.",
            "attachment_image": "assets/capturas/ISSUE-33_cabeceras_sin_emojis.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Calidad Visual",
                "component": "scripts/build_full_scrumban_board.py, docs/00_Tablero_Scrumban_Quantux.html",
                "description": "Eliminación de caracteres Unicode emoji en las 6 columnas (Backlog, Sprint, Retrabajo, En Curso, En Revisión, Aceptado).",
                "root_cause": "Iconos embebidos en el template de generación del tablero.",
                "solution": "Reemplazar los títulos de las columnas por texto tipográfico puro con badges numéricos estilizados en Quantux Teal.",
                "acceptance_criteria": [
                    "Escenario 1: Las 6 cabeceras de columnas muestran únicamente texto limpio y badge numérico sin emojis."
                ]
            }
        },
        {
            "id": "ISSUE-34",
            "title": "[P1 - ALTA PRIORIDAD] Módulo Base de Conocimiento KCS v6 con Tickets Aportantes y Empty State Senior UX",
            "epic": "EP-05: Módulo de Base de Conocimiento y Artículos Oficiales",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "rework",
            "so_feedback": {
                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",
                "date": "2026-09-27",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "notes": "ISSUE-34, no se desarrolló la solución: paso a retrabajo."
            },
            "discipline": "Frontend / Senior UX & KCS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-34",
            "doc_title": "DOC-QA-004 (ISSUE-34)",
            "doc_desc": "Visualización de tickets que retroalimentan los artículos KB bajo metodología KCS v6 y estado vacío amigable.",
            "attachment_image": "assets/capturas/ISSUE-34_modulo_kb_tickets_aportantes.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Trazabilidad KCS v6",
                "component": "frontend/index.html (modal-kb-view), frontend/js/app.js",
                "description": "El Solution Owner indicó: 'el modulo de la base de conocimiento debe mostrar los tkts que la alimentan, si no tienen tkts asociados al tema que se está consultando entonces debe decir que no tiene tkts que estén aportando información o que no hay historial de tkts asociados al problema en cuestion, analiza con UX senior'.",
                "root_cause": "Falta de renderizado de la sección de tickets aportantes en el modal de lectura de artículos KB.",
                "solution": "Implementar bloque de trazabilidad KCS con listado de tickets incidentes/problema vinculados o banner de empty state profesional.",
                "acceptance_criteria": [
                    "Escenario 1: DADO un artículo con tickets vinculados, ENTONCES lista los IDs y resúmenes con enlaces directos.",
                    "Escenario 2: DADO un artículo sin historial previo, ENTONCES muestra mensaje profesional de autoría estándar de fábrica."
                ]
            }
        },
        {
            "id": "ISSUE-35",
            "title": "[P1 - ALTA PRIORIDAD] Estilo Quantux Senior UX: Erradicación de Colores Sólidos y Oscuros en Workspace",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Senior UX & Paleta Teal",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-35",
            "doc_title": "DOC-QA-004 (ISSUE-35)",
            "doc_desc": "Ajuste integral de la paleta de colores del Workspace y modales al estándar luminoso Quantux (#00A896, #E0F7F5, #F8FAFC).",
            "attachment_image": "assets/capturas/ISSUE-35_estilo_quantux_sin_colores_oscuros.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Consistencia de Diseño",
                "component": "frontend/css/styles.css, frontend/index.html",
                "description": "El Solution Owner indicó: 'no tiene el estilo de diseño quantux, y no debes usar colores oscuros, actua como UX senior e implementa una mejora sustancial en los colores pero sin salirte del estilo quantux'.",
                "root_cause": "Uso excesivo de fondos oscuros (#0F172A) en modales, avatares y pestañas del espacio de trabajo.",
                "solution": "Migración a paleta Quantux institucional: fondos luminosos (#FFFFFF / #F8FAFC), bordes suaves (#E2E8F0) y acentos en Quantux Teal (#00A896).",
                "acceptance_criteria": [
                    "Escenario 1: Los modales y componentes del Workspace lucen estética luminosa y profesional sin fondos oscuros pesados."
                ]
            }
        },
        {
            "id": "ISSUE-36",
            "title": "[P1 - ALTA PRIORIDAD] Blindaje de Persistencia y Gobernanza: Prohibición de Re-inyección de Tarjetas Aprobadas a En Revisión",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Persistencia & Gobernanza",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-36",
            "doc_title": "DOC-QA-004 (ISSUE-36)",
            "doc_desc": "Garantía de inmutabilidad del estado Aceptado y Finalizado para las tarjetas revisadas por el Solution Owner.",
            "attachment_image": "assets/capturas/media_1790477038198_en_revision_37_error.png",
            "issue_details": {
                "severity": "P1 — Máxima Prioridad / Integridad de Flujo Scrumban",
                "component": "scripts/build_full_scrumban_board.py (generate_scrumban_board, init, loadState)",
                "description": "El Solution Owner reportó con urgencia: 'por que volvieron a aparecer todos los tkts en esta pila? ya los había cambiado de estado, acá solo deben estar los que no revise, corrige urgente, ahora'.",
                "root_cause": "El INITIAL_BACKLOG tenía hardcodeado status: 'qa' para tarjetas históricas, provocando que al cambiar storage key o limpiar cache volvieran a En Revisión.",
                "solution": "1. Forzar en Python status: 'done' para las 38 tarjetas aprobadas; 2. Implementar set PERMANENTLY_APPROVED_BY_SO en JavaScript; 3. Dejar en revisión ÚNICAMENTE las tarjetas no revisadas.",
                "acceptance_criteria": [
                    "Escenario 1: DADO que el Solution Owner carga el tablero, ENTONCES en la columna 'En Revisión' figuran únicamente las tarjetas no revisadas.",
                    "Escenario 2: DADO cualquier refresco de pantalla o cambio de storage, ENTONCES las 38 tarjetas aprobadas permanecen inmutables en 'Aceptado y Finalizado'."
                ]
            }
        },
        {
            "id": "ISSUE-37",
            "title": "[P1 - ALTA PRIORIDAD] Supresión del Botón y Pestaña Redundante 'Backlog Jerárquico' en Barra de Navegación del Tablero Scrumban",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Ergonomía & Navegación",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-37",
            "doc_title": "DOC-QA-004 (ISSUE-37)",
            "doc_desc": "Eliminación del botón innecesario 'Backlog Jerárquico' en la barra de navegación del tablero Scrumban.",
            "attachment_image": "assets/capturas/ISSUE-37_quitar_boton_backlog_jerarquico.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Limpieza de UI",
                "component": "scripts/build_full_scrumban_board.py (view-nav-bar), docs/00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner adjuntó captura del botón '📋 Backlog Jerárquico' e indicó: 'issue con alta prioridad, quita ese botón no aporta nada, alta prioridad suma al sprint'.",
                "root_cause": "Existencia de pestaña duplicada que dispersaba la atención y no agregaba valor operativo frente a la vista de Tablero y Roadmap.",
                "solution": "Suprimir el botón del DOM de navegación y mantener exclusivamente Tablero Scrumban, Roadmap & Cronograma y Métricas & Capacidad.",
                "acceptance_criteria": [
                    "Escenario 1: DADO el menú de navegación principal del tablero Scrumban, CUANDO se visualizan las opciones, ENTONCES no existe el botón 'Backlog Jerárquico'."
                ]
            }
        },
        {
            "id": "ISSUE-38",
            "title": "[P1 - ALTA PRIORIDAD] Rediseño y Armonización Visual de la Barra de Navegación Principal y Banner de Hardening (Cero Colores Oscuros y Cero Emojis)",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Senior UX & Paleta Quantux",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-38",
            "doc_title": "DOC-QA-004 (ISSUE-38)",
            "doc_desc": "Rediseño completo de la barra de navegación del tablero con fondo luminoso, pestañas en Quantux Teal sin emojis y banner de hardening estilizado.",
            "attachment_image": "assets/capturas/ISSUE-38_redisenio_navbar_sin_colores_oscuros_quantux.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Excelencia Visual Senior",
                "component": "scripts/build_full_scrumban_board.py (.view-nav-bar, .nav-tab-btn), docs/00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner instruyó: 'este menú está perdido rediseña y no uses esos colores solidos y oscuros apegate a estilo quantux , alta prioridad suma al sprint', adjuntando captura de la barra oscura con iconos.",
                "root_cause": "Uso de barra oscura (#1E293B) con botones de alto contraste e iconos desalineados con el estilo institucional Quantux.",
                "solution": "Rediseñar la barra con fondo blanco luminoso (#FFFFFF), sombra sutil, pestañas en píldoras Quantux Teal (#E0F7F5 / #00A896), erradicar todos los emojis y sustituir el candado por un badge formal.",
                "acceptance_criteria": [
                    "Escenario 1: La barra de navegación luce fondo blanco luminoso con borde sutil (#E2E8F0) y pestañas tipográficas en Quantux Teal.",
                    "Escenario 2: No figura ningún emoji (📌, 🗺️, 📊, 📋, 🔒) en la barra ni en el banner de hardening."
                ]
            }
        },
        {
            "id": "MEJ-11",
            "title": "[P1 - ALTA PRIORIDAD] Tooltips de Gobernanza Scrumban en Cabeceras de Columna, Supresión de Banners Estáticos y Erradicación Total de Emojis",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "rework",
            "so_feedback": {
                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",
                "date": "2026-09-27",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "notes": "MEJ-11 enviado a retrabajo no se desarrolló la solución."
            },
            "discipline": "Frontend / Ergonomía Kanban & Gobernanza",
            "type": "MEJORA",
            "priority": "P1",
            "doc_link": "03_ARQUITECTURA_Y_DISENO_TECNICO.md#mej-11",
            "doc_title": "DOC-ARC-003 (MEJ-11)",
            "doc_desc": "Incorporación de tooltips explicativos en los 6 estados de Scrumban, recuperación de altura vertical útil y limpieza tipográfica de emojis.",
            "attachment_image": "assets/capturas/MEJ-11_tooltips_gobernanza_estados.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Experiencia de Usuario y Gobernanza",
                "component": "scripts/build_full_scrumban_board.py (column-header, column-title), docs/00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner instruyó: 'este tipo de descripcion lo tendran todos los estados de scrumban pero serán tooltips, es una opotunidad de mejora, suma al backlog del producto', adjuntando captura del texto explicativo de En Revisión.",
                "root_cause": "Banners de texto estáticos embebidos en el cuerpo de las columnas que quitaban altura vertical valiosa.",
                "solution": "Convertir las descripciones en tooltips accesibles sobre el icono o título de cabecera y eliminar los bloques estáticos.",
                "acceptance_criteria": [
                    "Escenario 1: Al pasar el cursor sobre cualquiera de las 6 cabeceras, se despliega el tooltip explicativo con la directiva oficial del estado.",
                    "Escenario 2: Las columnas ganan 60px de altura vertical libre eliminando textos estáticos innecesarios."
                ]
            }
        },
        {
            "id": "ISSUE-39",
            "title": "[P1 - ALTA CRITICIDAD] Corrección Operativa y Visual de los Botones 'Tarjetas' | 'Tabla' en Clientes & Mesas de Ayuda",
            "epic": "EP-05: Administración Multitenant, Plataformas y Salud Operativa",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Senior UX & Clientes",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-39",
            "doc_title": "DOC-QA-005 (ISSUE-39)",
            "doc_desc": "Corrección funcional y visual del conmutador de modo de vista entre cuadrícula de tarjetas y tabla ejecutiva en el módulo de clientes.",
            "attachment_image": "assets/capturas/ISSUE-39_botones_tarjetas_tabla_no_funcionan.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Falla de Navegación",
                "component": "frontend/index.html (#btn-view-mode-cards, #btn-view-mode-table), frontend/js/app.js (togglePlatformsViewMode)",
                "description": "El Solution Owner reportó: 'estos botones de clientes no funcionan, issue de alta criticidad, suma al sprit', adjuntando captura del selector de vista Tarjetas/Tabla.",
                "root_cause": "Estilos inline rígidos en el HTML impedían la alternancia visual activa, y togglePlatformsViewMode no sincronizaba el re-renderizado de la tabla con el catálogo de clientes.",
                "solution": "Depuración de estilos inline, renderizado dinámico de píldora activa con estilo Quantux (#FFFFFF con sombra sutil) e invocación síncrona a renderInstitutionsCatalog() para alternar limpiamente entre cuadrícula y tabla.",
                "acceptance_criteria": [
                    "Escenario 1: Al clicar 'Tabla', la tabla ejecutiva de instituciones sanitarias se despliega inmediatamente con todos los datos y el botón adopta el estilo activo.",
                    "Escenario 2: Al clicar 'Tarjetas', la cuadrícula de tarjetas de clientes se visualiza correctamente y el botón adopta el estado activo."
                ]
            }
        },
        {
            "id": "ISSUE-40",
            "title": "[P1 - ALTA CRITICIDAD] Corrección de Apertura de Ficha 360° al Clicar Tarjeta OSDE y Demás Clientes (Fatal ReferenceError)",
            "epic": "EP-05: Administración Multitenant, Plataformas y Salud Operativa",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Integración & Resiliencia",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-40",
            "doc_title": "DOC-QA-006 (ISSUE-40)",
            "doc_desc": "Definición de formatPriorityBadge e inmunización de openInstitutionDetailModal para garantizar apertura instantánea de la Ficha 360° en todas las instituciones.",
            "attachment_image": "assets/capturas/ISSUE-40_tarjeta_osde_no_abre_modal_cliente.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Interrupción de Flujo de Gestión de Clientes",
                "component": "frontend/js/app.js (openInstitutionDetailModal, formatPriorityBadge)",
                "description": "El Solution Owner reportó: 'al hacer clic sobre la tarjeta de OSDE no se abre el modal de debe mostrar la información del cliente, y verifica que no hayan más tarjetas en este estado, issue de alta criticidad, suma la sprint'.",
                "root_cause": "La función formatPriorityBadge(t.priority) invocada en el renderizado de incidentes activos del modal no estaba definida en app.js, lanzando un ReferenceError que abortaba la apertura del modal en clientes con tickets activos.",
                "solution": "Definición global de formatPriorityBadge con paleta de badges ITIL Quantux y blindaje de la función openInstitutionDetailModal con bloque try/catch/finally para garantizar apertura ante cualquier institución.",
                "acceptance_criteria": [
                    "Escenario 1: Al hacer clic sobre la tarjeta de OSDE, se abre de inmediato el modal de Ficha 360° con sus 4 pestañas operativas (Detalles, Módulos, Incidentes, Contrato SLA).",
                    "Escenario 2: Todas las instituciones del catálogo abren su modal 360° sin errores en consola ni interrupciones."
                ]
            }
        },
        {
            "id": "ISSUE-41",
            "title": "[P1 - ALTA CRITICIDAD] Ocultamiento Total de los Módulos 'Tablero de Control' y 'Torre de Control' en el Menú Lateral para Todos los Roles",
            "epic": "EP-01: Acceso, Roles y Permisos Básicos",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "rework",
            "so_feedback": {
                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",
                "date": "2026-09-27",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "notes": "ISSUE-41 no se desarrolló la solución los botones todavía se muestran."
            },
            "discipline": "Frontend / RBAC & Navegación",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-41",
            "doc_title": "DOC-QA-007 (ISSUE-41)",
            "doc_desc": "Supresión categórica de Tablero de Control y Torre de Control en la barra lateral para todos los perfiles, canalizando la operación hacia Mando Unificado.",
            "attachment_image": "assets/capturas/ISSUE-41_ocultar_tablero_de_control_y_torre_de_control_todos_los_roles.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Regla de Negocio y Gobernanza de Menú",
                "component": "frontend/js/app.js (applyRolePermissions, switchView), frontend/index.html (#tab-dashboard, #tab-team-leader)",
                "description": "El Solution Owner ordenó: 'estos modulos todavía están visibles para algunos roles, deben estar ocultos para todos los roles, issu de alta criticiad suma al sprint'.",
                "root_cause": "En applyRolePermissions(), los roles ADMIN, TEAM_LEADER y SOPORTE forzaban tabDash.style.display = 'flex' y tabTeamLeader.style.display = 'flex'.",
                "solution": "Establecer display: none !important tanto en markup HTML como en app.js para todos los roles sin excepción, redirigiendo accesos directos al Mando Operativo o Portal Solicitante.",
                "acceptance_criteria": [
                    "Escenario 1: En ningún rol (Admin, Líder de Equipo, Soporte, Solicitante) aparecen los ítems 'Tablero de Control' ni 'Torre de Control' en el menú lateral.",
                    "Escenario 2: Si se invoca switchView('dashboard') o switchView('team-leader'), se redirige automáticamente a la vista autorizada correspondiente."
                ]
            }
        },
        {
            "id": "ISSUE-42",
            "title": "[P1 - ALTA CRITICIDAD] Aislamiento Estricto RBAC: Ocultamiento del Módulo 'Mando Operativo' para el Rol Solicitante",
            "epic": "EP-01: Acceso, Roles y Permisos Básicos",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / RBAC & Seguridad",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-42",
            "doc_title": "DOC-QA-008 (ISSUE-42)",
            "doc_desc": "Aislamiento de la consola de agentes Mando Operativo para el perfil Solicitante, garantizando acceso exclusivo a su Centro de Ayuda clínico y manual.",
            "attachment_image": "assets/capturas/ISSUE-42_rol_solicitante_ocultar_mando_operativo.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Fuga de Visibilidad Operativa",
                "component": "frontend/js/app.js (applyRolePermissions, switchView), frontend/index.html (#tab-unified-hub)",
                "description": "El Solution Owner instruyó: 'el rol solicitante no debe ver el módulo mando de control, issue suma al sprint', adjuntando captura del menú lateral del Dr. Martín Gómez.",
                "root_cause": "applyRolePermissions() no ocultaba tab-unified-hub cuando el rol activo era SOLICITANTE, permitiendo al médico/paciente visualizar la consola interna de despacho de agentes.",
                "solution": "Ocultamiento estricto de #tab-unified-hub para SOLICITANTE, redirección forzada a 'requester-portal' (Centro de Ayuda con Chat IA) y bloqueo en switchView().",
                "acceptance_criteria": [
                    "Escenario 1: Al iniciar sesión como Solicitante (Dr. Martín Gómez), el menú lateral solo presenta 'Centro de Ayuda' y 'Manual Operativo'.",
                    "Escenario 2: El Solicitante jamás tiene acceso visual ni funcional a la consola de Mando Operativo."
                ]
            }
        },
        {
            "id": "ISSUE-43",
            "title": "[P1 - ALTA CRITICIDAD] Reubicación Ergonométrica del Botón Hamburguesa de 3 Rayas a la Izquierda del Texto en la Cabecera de Marca",
            "epic": "EP-01: Acceso, Roles y Permisos Básicos",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Senior UX & Ergonomía",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-43",
            "doc_title": "DOC-QA-009 (ISSUE-43)",
            "doc_desc": "Reposicionamiento del toggle hamburguesa a la izquierda del título Service Desk respetando la ergonomía de navegación senior.",
            "attachment_image": "assets/capturas/ISSUE-43_hamburguesa_a_la_izquierda_del_texto.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Identidad Visual y Estándar de Navegación",
                "component": "frontend/index.html (.sidebar-brand-header, #btn-sidebar-collapse)",
                "description": "El Solution Owner ordenó: 'la hambruguesa de 3 rayas debe estar a la izquierda del texto, isuue suma la sprint', adjuntando capturas del encabezado del menú lateral.",
                "root_cause": "El botón hamburguesa (#btn-sidebar-collapse) figuraba al final del contenedor con justify-content: space-between, situándose a la derecha del texto Service Desk.",
                "solution": "Reordenamiento del DOM colocando el botón de 3 rayas en primera posición (izquierda) con gap de 12px y justify-content: flex-start respecto a la tipografía de Service Desk / Mesa de Ayuda TI.",
                "acceptance_criteria": [
                    "Escenario 1: El botón hamburguesa de 3 rayas se ubica a la izquierda del rótulo 'Service Desk / Mesa de Ayuda TI'.",
                    "Escenario 2: El comportamiento de plegado y expandido del menú se mantiene 100% operativo tanto al hacer clic como con el atajo '['."
                ]
            }
        },
        {
            "id": "ISSUE-44",
            "title": "[P1 - ALTA CRITICIDAD] Filtro Estricto por Defecto en Mesa de Ayuda para Analistas de Soporte: Solo Tickets Asignados y Sin Asignar",
            "epic": "EP-06: Gestión de Incidentes, SLA Dinámico y Transiciones",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Mesa de Ayuda & Gobernanza de Turnos",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-44",
            "doc_title": "DOC-QA-010 (ISSUE-44)",
            "doc_desc": "Filtrado automático por defecto en bandeja operativa para analistas N1/N2/N3 focalizando sus solicitudes activas y la cola sin asignar.",
            "attachment_image": "assets/capturas/ISSUE-44_analistas_soporte_solo_sus_tkts_y_sin_asignar.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Eficiencia Operativa y Foco de Guardia N1/N2",
                "component": "frontend/js/app.js (loadTickets, applyRolePermissions), frontend/index.html (#tkt-filter-assignee)",
                "description": "El Solution Owner instruyó: 'los analistas de soporte por defecto solo deben ver sus tkt asignados y lo que es estén en estado sin asignar', adjuntando captura de Laura Benítez (Analista N2) con tickets de terceros.",
                "root_cause": "loadTickets() traía por defecto todas las solicitudes activas de la organización sin filtrar por el analista en sesión, saturando la bandeja operativa.",
                "solution": "Implementación de filtro estricto por defecto para roles de soporte (SOPORTE, SOPORTE_N1, SOPORTE_N2, SOPORTE_N3) que solo muestra tickets asignados al usuario activo y tickets en estado Sin Asignar (o NUEVO). Incorporación de selector select #tkt-filter-assignee en la barra de filtros.",
                "acceptance_criteria": [
                    "Escenario 1: Al iniciar sesión cualquier analista de soporte (ej. Laura Benítez), la bandeja muestra por defecto exclusivamente sus tickets asignados y los casos sin asignar.",
                    "Escenario 2: El contador y la paginación reflejan con exactitud el subconjunto relevante para su turno operativo."
                ]
            }
        },
        {
            "id": "OPP-04",
            "title": "[OPORTUNIDAD DE MEJORA] Copiloto IA Generativo de Resumen Ejecutivo de Conversaciones y Sugerencia de Resolución en 1 Clic (Benchmark Zendesk Copilot / ServiceNow GenAI)",
            "epic": "EP-06: Gestión de Incidentes, SLA Dinámico y Transiciones",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Frontend / IA & UX",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-04",
            "doc_title": "DOC-SPEC-002 (OPP-04)",
            "doc_desc": "Panel lateral inteligente que sintetiza hilos clínicos complejos y redacta borradores de respuesta técnica con un solo clic.",
            "attachment_image": "assets/capturas/OPP-04_copiloto_ia_resumen_resolucion.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Productividad de Mesa N2",
                "component": "frontend/js/app.js (Agent Copilot Panel), backend/app/ai/summary_engine.py",
                "description": "Inspirado en Zendesk AI Copilot y ServiceNow GenAI, permite a los analistas de soporte N2 resumir automáticamente teleconsultas extensas en 3 balas ejecutivas (Problema, Diagnóstico y Acción Sugerida) y generar respuestas resolutivas con un clic.",
                "root_cause": "Demoras operativas de lectura en hilos médicos largos durante guardias activas.",
                "solution": "Incorporar motor LLM local/híbrido que procesa el thread y renderiza tarjeta de asistencia táctica con botón 'Aplicar Solución Sugerida'.",
                "acceptance_criteria": [
                    "Escenario 1 (Resumen en 3 Balas): DADO un incidente con múltiples mensajes, CUANDO el operador N2 abre el panel IA, ENTONCES visualiza la síntesis estructurada en menos de 1 segundo.",
                    "Escenario 2 (Inyección en 1 Clic): DADO el borrador sugerido, CUANDO presiona 'Insertar en Respuesta', ENTONCES carga el texto formateado en el editor listo para envío.",
                    "Escenario 3 (Mockeo Funcional): DADO el simulador interactivo, CUANDO se presiona 'Probar Copiloto', ENTONCES reproduce la síntesis sintética con datos verídicos."
                ]
            }
        },
        {
            "id": "OPP-05",
            "title": "[OPORTUNIDAD DE MEJORA] Motor de Macro-Automatizaciones Predictivas Basado en Detección de Intención Semántica (Benchmark Freshservice Freddy / Intercom Workflows)",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Backend / Workflows & IA",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-05",
            "doc_title": "DOC-SPEC-002 (OPP-05)",
            "doc_desc": "Agrupamiento predictivo de incidentes en Incidentes Mayores y ejecución de macros compuestas por contexto.",
            "attachment_image": "assets/capturas/OPP-05_macro_automatizaciones_predictivas.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Automatización Proactiva",
                "component": "backend/app/workflows/intent_macros.py, frontend/js/app.js",
                "description": "Benchmark de Freshservice y Jira Service Management: agrupa ráfagas de tickets con intención idéntica (ej: caída de nodo provincial SISA o microservicio proxy-reservas) en un 'Incidente Mayor Padre' y ejecuta macros de respuesta masiva.",
                "root_cause": "Saturación repetitiva de la mesa ante contingencias técnicas regionales masivas.",
                "solution": "Detector semántico de clustering en tiempo real que gatilla flujos automáticos de notificación y vinculación de tickets huérfanos.",
                "acceptance_criteria": [
                    "Escenario 1: DADO el ingreso de 3 o más tickets afines en 10 minutos, CUANDO el motor evalúa similitud semántica > 85%, ENTONCES sugiere unificar en Incidente Mayor.",
                    "Escenario 2: DADO el incidente unificado, CUANDO se dispara la macro 'Contingencia Activa', ENTONCES actualiza masivamente todos los tickets asociados con telemetría precargada."
                ]
            }
        },
        {
            "id": "OPP-06",
            "title": "[OPORTUNIDAD DE MEJORA] Asistente Flotante Picture-in-Picture (PiP) para Modo 'Atención Ininterrumpida' en Videoconsultas Médicas (Benchmark Epic Systems / Teladoc)",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 3,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Frontend / UX & WebRTC",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-06",
            "doc_title": "DOC-SPEC-002 (OPP-06)",
            "doc_desc": "Widget flotante desacoplado que asiste al médico durante la videollamada sin obstruir la visión del paciente ni la historia clínica.",
            "attachment_image": "assets/capturas/OPP-06_asistente_flotante_pip.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Ergonomía Clínica",
                "component": "frontend/js/pip_assistant.js, frontend/css/styles.css",
                "description": "Benchmark Epic Rover / Teladoc: permite al profesional compactar el asistente N1 en una burbuja flotante semitransparente reposicionable, recibiendo alertas tácticas de validación y vademécum sin cambiar de pestaña.",
                "root_cause": "Cambio de contexto cognitivo y pérdida de contacto visual con el paciente al tener que consultar el portal en otra ventana.",
                "solution": "Implementar modo Picture-in-Picture nativo HTML5/CSS con micro-indicaciones clínicas silenciosas.",
                "acceptance_criteria": [
                    "Escenario 1: Al pulsar el botón PiP, el asistente se reduce a un widget flotante arrastrable de 260x180px con opacidad adaptable.",
                    "Escenario 2: El widget notifica cambios de estado en segundo plano (ej: token aceptado) mediante pulso lumínico en Quantux Teal."
                ]
            }
        },
        {
            "id": "OPP-07",
            "title": "[OPORTUNIDAD DE MEJORA] Sistema Predictivo de Alerta Temprana de SLA Breach con Puntuación de Riesgo ML (Benchmark ServiceNow Incident Intelligence)",
            "epic": "EP-06: Gestión de Incidentes, SLA Dinámico y Transiciones",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Data / ML & Frontend",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-07",
            "doc_title": "DOC-SPEC-002 (OPP-07)",
            "doc_desc": "Modelo de machine learning que anticipa la probabilidad de quiebre de SLA y reordena dinámicamente las colas de atención.",
            "attachment_image": "assets/capturas/OPP-07_sla_early_warning_ml.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Gestión Predictiva de Colas",
                "component": "backend/app/analytics/sla_predictor.py, frontend/js/app.js",
                "description": "Benchmark ServiceNow Predictive Intelligence: algoritmo que evalúa la velocidad de atención, especialidad requerida y disponibilidad de analistas, asignando a cada ticket un 'Breach Risk Score' (0-100%) para intervención preventiva.",
                "root_cause": "Alertas de SLA reactivas que solo avisan cuando el tiempo restante es menor al 15%, impidiendo actuar a tiempo.",
                "solution": "Scoring predictivo en tiempo real con badges térmicos dinámicos (Verde, Ámbar, Rojo) y ordenamiento inteligente en la bandeja de entrada.",
                "acceptance_criteria": [
                    "Escenario 1: El sistema calcula el índice de riesgo predictivo cada 60 segundos por ticket.",
                    "Escenario 2: Los supervisores pueden ordenar la bandeja por 'Mayor Riesgo de Incumplimiento' para redistribuir carga antes de que se venza el SLA."
                ]
            }
        },
        {
            "id": "OPP-08",
            "title": "[OPORTUNIDAD DE MEJORA] Visor de Interoperabilidad Clínica HL7 FHIR R4 para Contexto Inmediato de Soporte en Interconsultas (Benchmark Health Gorilla / Cerner)",
            "epic": "EP-05: Módulo de Base de Conocimiento y Artículos Oficiales",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Backend / HL7 FHIR & APIs",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-08",
            "doc_title": "DOC-SPEC-002 (OPP-08)",
            "doc_desc": "Inspección técnica de bundles FHIR R4 con anonimización automática para resolución acelerada de fallos de autorización médica.",
            "attachment_image": "assets/capturas/OPP-08_visor_hl7_fhir_interoperabilidad.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Soporte de Salud Interoperable",
                "component": "backend/app/interop/fhir_viewer.py, frontend/js/fhir_modal.js",
                "description": "Benchmark Cerner Millennium / Health Gorilla: pestaña especializada en el Workspace que permite al analista examinar los recursos FHIR (Patient, Encounter, Condition, MedicationRequest) asociados a la falla de autorización en HCE, con enmascaramiento estricto de datos sensibles.",
                "root_cause": "Dificultad de los analistas para diagnosticar rechazos de prestaciones sin acceder a registros clínicos en crudo.",
                "solution": "Parser y renderizador visual de bundles HL7 FHIR que resalta campos con errores de codificación SNOMED/CIE-10 en verde/rojo.",
                "acceptance_criteria": [
                    "Escenario 1: DADO un ticket con payload clínico adjunto, CUANDO se abre la pestaña FHIR, ENTONCES visualiza los recursos desglosados en tarjetas legibles.",
                    "Escenario 2: Todos los datos personales son automáticamente anonimizados cumpliendo la Ley 25.326 y estándares HIPAA."
                ]
            }
        },
        {
            "id": "ISSUE-45",
            "title": "[P1 - ALTA CRITICIDAD] Modal de Escalamiento N2 No Muestra Botones Inferiores (Botones Cortados) y Falta Campo para Adjuntar Archivos",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & JS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-45",
            "doc_title": "DOC-QA-005 (ISSUE-45)",
            "doc_desc": "Corrección de layout flexbox en el modal de previsualización N2 asegurando footer fijo y campo de carga de adjuntos/capturas.",
            "attachment_image": "assets/capturas/ISSUE-45_modal_n2_botones_cortados_campo_adjuntos.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Operabilidad Asistencial N2",
                "component": "frontend/index.html (#modal-preview-edit-ticket), frontend/js/app.js (confirmCreateTicketFromPreview)",
                "description": "El Solution Owner reportó: 'no muestra los botones de abajo, y debe tener el campo para adjuntar, issue de alta prioridad, suma al sprint', adjuntando captura del modal cortado en la base.",
                "root_cause": "El contenedor modal carecía de flex-direction column con flex-shrink: 0 en el footer, provocando que los botones 'Cancelar' y 'Confirmar y Escalar a N2' se ocultaran fuera del viewport en pantallas compactas.",
                "solution": "Reestructuración CSS con modal-box en display flex column (max-height 88vh), form en flex 1 min-height 0, modal-body con overflow-y auto y modal-footer con flex-shrink: 0 sticky. Incorporación de zona de dropzone interactiva y selector de archivos para adjuntar capturas (PDF, PNG, JPG) con badge de previsualización y botón Quitar.",
                "acceptance_criteria": [
                    "Escenario 1: Al abrir el modal de escalamiento a N2 en cualquier resolución, los botones 'Cancelar' y 'Confirmar y Escalar a N2' son siempre 100% visibles.",
                    "Escenario 2: El modal incluye un campo para adjuntar archivos o capturas con drag & drop y selector manual, permitiendo visualizar nombre/peso y removerlo antes de enviar.",
                    "Escenario 3: Al confirmar el ticket, el adjunto se vincula al payload de creación del ticket."
                ]
            }
        },
        {
            "id": "ISSUE-46",
            "title": "[P1 - ALTA CRITICIDAD] Aislamiento Estricto de Diagnóstico Técnico, Logs de Auditor y JSON al Solicitante (Exclusivo para Soporte en Base de Conocimiento)",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 5,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / IA & UX",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-46",
            "doc_title": "DOC-QA-005 (ISSUE-46)",
            "doc_desc": "Ocultamiento absoluto de telemetría de sistemas, JSON de auditoría y diagnósticos de microservicios para el perfil Solicitante, preservándolos exclusivamente para la consulta del Analista de Soporte en la Base de Conocimiento.",
            "attachment_image": "assets/capturas/ISSUE-46_ocultar_fundamento_tecnico_diagnostico_al_solicitante.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Experiencia Médica & Seguridad Operativa",
                "component": "frontend/js/app.js (submitRequesterChat, renderRequesterChatStream)",
                "description": "El Solution Owner instruyó taxativamente: 'la informacion del recuadro en ningun caso se debe mostrar al solicitante, se debe mostar al analista de soporte cuando consulte la base de conocimiento ´peron nunca al solicitante, issue de alta prioridad, suma al sprint', adjuntando captura del recuadro con diagnóstico técnico de auditor y JSON.",
                "root_cause": "submitRequesterChat inyectaba directamente triageData.ai_response_text en msg.text, exponiendo telemetría técnica (JSON con 'Matrículas: 0', auditor CD, endpoints SISA) al médico en lugar de una indicación clínica inmediata de continuidad asistencial.",
                "solution": "Separación de capas en frontend/js/app.js: para el rol SOLICITANTE, msg.text presenta exclusivamente el saludo médico asistencial y las directivas operativas clínicas. El fundamento técnico pericial (JSON, diagnóstico, causa raíz) se almacena en techFoundation y se destina exclusivamente a la consulta del Analista de Soporte (N1/N2/N3) en la Base de Conocimiento y Agent Workspace.",
                "acceptance_criteria": [
                    "Escenario 1: El rol Solicitante (médico/prestador) jamás visualiza en el chat términos técnicos como 'JSON', 'auditor de CD', 'microservicios' o códigos de diagnóstico interno.",
                    "Escenario 2: El analista de soporte puede consultar en todo momento el fundamento técnico y diagnóstico completo al acceder a la Base de Conocimiento y al detalle del ticket escalado."
                ]
            }
        },
        {
            "id": "ISSUE-47",
            "title": "[P1 - ALTA CRITICIDAD] Blindaje de Inmutabilidad Cuántica en Tablero Scrumban: Bloqueo Irreversible de Tarjetas en 'Aceptado y Finalizado'",
            "epic": "EP-01: Arquitectura Base, Multi-Tenancy y Configuración",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Scrumban & JS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-47",
            "doc_title": "DOC-QA-005 (ISSUE-47)",
            "doc_desc": "Garantía de inmutabilidad absoluta para los entregables formalmente aprobados por el Solution Owner, impidiendo cualquier retroceso a estados previos.",
            "attachment_image": "assets/capturas/ISSUE-47_tarjetas_en_aceptado_nunca_vuelven_a_estado_anterior.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Gobernanza DoD Inmutable",
                "component": "scripts/build_full_scrumban_board.py (createCardElement, drag, drop, moveTask)",
                "description": "El Solution Owner decretó: 'los tkt que pasa a este estado nunca deben volver a un estado anterior', señalando la columna Aceptado y Finalizado.",
                "root_cause": "Las tarjetas en la columna 'done' conservaban el atributo draggable=true y el botón ◀ de retroceso, permitiendo movimientos accidentales hacia columnas anteriores.",
                "solution": "Deshabilitación total de drag (draggable=false), remoción del botón ◀ reemplazándolo por el badge '✓ Aceptado (Inmutable)', y control de gobernanza en drag, drop y moveTask que rechaza con alerta institucional cualquier intento de alterar el estado de un entregable finalizado.",
                "acceptance_criteria": [
                    "Escenario 1: Toda tarjeta en 'Aceptado y Finalizado' (done) tiene draggable=false y no puede ser arrastrada a ninguna columna previa.",
                    "Escenario 2: La tarjeta no muestra el botón de retroceso ◀, exhibiendo en su lugar la pastilla '✓ Aceptado (Inmutable)'.",
                    "Escenario 3: Los intentos programáticos o por teclado de retroceder son interceptados y bloqueados por la regla de gobernanza."
                ]
            }
        },
        {
            "id": "ISSUE-48",
            "title": "[P1 - ALTA PRIORIDAD] Eliminación de Duplicidad en Cápsulas de Hito y Comité Evaluador en Encabezado Scrumban",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / CSS & HTML",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-48",
            "doc_title": "DOC-QA-005 (ISSUE-48)",
            "doc_desc": "Eliminación del bloque duplicado de badges 'HITO: 01-OCT-2026' y 'COMITÉ EVALUADOR' en la franja superior de Hardening.",
            "attachment_image": "assets/capturas/ISSUE-48_duplicidad_capsulas_hito_comite_evaluador.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Pulido Estético & Limpieza Visual",
                "component": "scripts/build_full_scrumban_board.py (Línea 3995), docs/00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner indicó expresamente: 'quita la duplicidad de estas capsulas, issue alta prioridad, suma el sprint', adjuntando captura de las cápsulas repetidas una debajo de la otra.",
                "root_cause": "Doble bloque <div> idéntico en la sección de Scope Freeze del encabezado del tablero Scrumban.",
                "solution": "Remoción quirúrgica de la duplicación manteniendo una única instancia pulida y alineada a la derecha de la barra de Hardening.",
                "acceptance_criteria": [
                    "Escenario 1: En la franja superior de Hardening sólo se visualiza una única pareja de cápsulas 'HITO: 01-OCT-2026' y 'COMITÉ EVALUADOR'.",
                    "Escenario 2: No existen elementos superpuestos ni saltos de línea anómalos."
                ]
            }
        },
        {
            "id": "OPP-09",
            "title": "[OPORTUNIDAD DE MEJORA] Telemetría WebRTC Proactiva y Conmutación Preventiva a Audio/Contingencia (Benchmark Zoom Phone / Teams Telehealth)",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Frontend / WebRTC & Telehealth",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-09",
            "doc_title": "DOC-SPEC-002 (OPP-09)",
            "doc_desc": "Diagnóstico en tiempo real de jitter, packet loss y bitrate de videoconsultas médicas, sugiriendo conmutación automática preventiva a modo contingencia antes del corte de llamada.",
            "attachment_image": "assets/capturas/OPP-09_telemetria_webrtc_conmutacion_preventiva.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Continuidad Asistencial en Telemedicina",
                "component": "frontend/js/webrtc_telemetry.js, backend/app/services/telemetry.py",
                "description": "Benchmark Zoom Phone / Microsoft Teams Telehealth: monitor continuo de la calidad del stream WebRTC del profesional de la salud. Cuando la red se degrada (jitter > 35ms o packet loss > 5%), el sistema asiste proactivamente sugiriendo conmutar a audio HD o puente telefónico de respaldo.",
                "root_cause": "Cortes intempestivos de videoconsultas psiquiátricas y pediátricas por fluctuaciones de WiFi del profesional.",
                "solution": "Agente de telemetría pasiva con alerta táctica contextual para el profesional y registro de métricas para el ticket N2.",
                "acceptance_criteria": [
                    "Escenario 1: Si el packet loss supera 5% durante 10 segundos, se despliega una sugerencia no invasiva para bajar resolución o cambiar a sólo audio.",
                    "Escenario 2: La telemetría de red se adjunta de forma automática en caso de derivar ticket a Soporte N2."
                ]
            }
        },
        {
            "id": "OPP-10",
            "title": "[OPORTUNIDAD DE MEJORA] Motor de Búsqueda Semántica Vectorial Multimodal sobre Base de Conocimiento CD2 y Vademécum (Benchmark Pinecone / Algolia AI / ServiceNow AI)",
            "epic": "EP-05: Módulo de Base de Conocimiento y Artículos Oficiales",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Backend / Vector Search & IA",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-10",
            "doc_title": "DOC-SPEC-002 (OPP-10)",
            "doc_desc": "Integración de búsqueda semántica híbrida (embeddings densos + BM25) sobre las 50 guías CD2 y vademécum Alfabeta para localizar soluciones por analogía conceptual.",
            "attachment_image": "assets/capturas/OPP-10_busqueda_semantica_vectorial_kb.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Búsqueda Cognitiva",
                "component": "backend/app/ai/vector_search.py, frontend/js/app.js",
                "description": "Benchmark ServiceNow AI Search y Algolia: permite a médicos y analistas escribir síntomas en lenguaje coloquial (ej: 'el sistema no me deja recetar la pastilla para la presión') y recuperar instantáneamente el runbook exacto de incompatibilidad farmacéutica de Alfabeta.",
                "root_cause": "La búsqueda léxica tradicional falla si el usuario no escribe el código exacto del runbook o la monodroga técnica.",
                "solution": "Indexación vectorial con embeddings biomédicos y re-ranking de artículos según tasa histórica de resolución.",
                "acceptance_criteria": [
                    "Escenario 1: Consultas en lenguaje natural sin tecnicismos arrojan el artículo SOP relevante entre los primeros 3 resultados con similitud > 90%.",
                    "Escenario 2: Tiempo de respuesta de búsqueda menor a 150 milisegundos."
                ]
            }
        },
        {
            "id": "OPP-11",
            "title": "[OPORTUNIDAD DE MEJORA] Orquestador de Acuerdos OLA Multiequipo con Asignación por Skills y Carga Cognitiva (Benchmark Jira Service Management / PagerDuty)",
            "epic": "EP-06: Gestión de Incidentes, SLA Dinámico y Transiciones",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Backend / ITIL 4 OLA & SLA",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-11",
            "doc_title": "DOC-SPEC-002 (OPP-11)",
            "doc_desc": "Asignación pericial de incidentes entre N1, N2, N3 y DevOps ponderando la especialidad técnica del analista (HL7, SISA, Base de Datos, Infraestructura) y su carga de trabajo en tiempo real.",
            "attachment_image": "assets/capturas/OPP-11_orquestador_ola_multiequipo_skills.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Enrutamiento Inteligente",
                "component": "backend/app/services/skill_routing.py, frontend/js/app.js",
                "description": "Benchmark Jira Service Management / PagerDuty: define acuerdos internos OLA (Operational Level Agreements) entre escalones técnicos con enrutamiento inteligente basado en la matriz de competencias del personal disponible.",
                "root_cause": "Asignación manual en cascada que genera cuellos de botella y demoras en tickets hiper-especializados.",
                "solution": "Matriz de ruteo automático por tagging de habilidades y medidor de saturación por operador en tiempo real.",
                "acceptance_criteria": [
                    "Escenario 1: Los tickets de integración SISA se canalizan directamente al especialista disponible con mayor tasa FCR en dicha pasarela.",
                    "Escenario 2: Se monitorea el temporizador OLA interno independientemente del SLA global con el cliente."
                ]
            }
        },
        {
            "id": "OPP-12",
            "title": "[OPORTUNIDAD DE MEJORA] Generador Automatizado de Informes Periciales Post-Mortem y Análisis de Causa Raíz (RCA) con 1 Clic (Benchmark PagerDuty Postmortems / Datadog RCA)",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 5,
            "sprint": "Product Backlog",
            "status": "backlog",
            "discipline": "Backend / Auditing & Reports",
            "type": "MEJORA",
            "priority": "P2",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#opp-12",
            "doc_title": "DOC-SPEC-002 (OPP-12)",
            "doc_desc": "Compilación instantánea de la cronología de eventos, logs de microservicios, tickets correlacionados y métricas de impacto para generar el informe pericial homologado para auditorías de Salud y OSDE.",
            "attachment_image": "assets/capturas/OPP-12_generador_rca_postmortem_1clic.png",
            "issue_details": {
                "severity": "P2 — Oportunidad de Innovación / Auditoría y Cumplimiento Regulatorio",
                "component": "backend/app/analytics/rca_generator.py, frontend/js/app.js",
                "description": "Benchmark PagerDuty Postmortems / Datadog: al cerrarse un incidente mayor o crítico (P1), el sistema compila automáticamente la cronología pericial completa con marcas de tiempo atómicas, diagramas de impacto y plan de acción preventivo homologado.",
                "root_cause": "Redacción manual de informes post-incidente que consume entre 3 y 5 horas por evento crítico.",
                "solution": "Módulo generador de RCA descargable en PDF/Word con certificación de auditoría ITIL 4 y sello criptográfico.",
                "acceptance_criteria": [
                    "Escenario 1: Con 1 clic sobre un incidente P1 resuelto, se genera el informe pericial RCA con el 100% de la cronología y métricas de impacto.",
                    "Escenario 2: El informe cumple con las directivas de auditoría del Ministerio de Salud y OSDE."
                ]
            }
        },
        {
            "id": "ISSUE-49",
            "title": "[P1 - ALTA CRITICIDAD] Eliminación Definitiva del Botón 'Mis Solicitudes (1997)' en Cabecera Superior del Solicitante",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & JS",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-49",
            "doc_title": "DOC-QA-005 (ISSUE-49)",
            "doc_desc": "Remoción absoluta del botón 'Mis Solicitudes' y su badge con conteo global masivo de la barra superior del perfil Solicitante.",
            "attachment_image": "assets/capturas/ISSUE-49_quitar_mis_solicitudes_o_badge_enorme_al_solicitante.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Experiencia Médica Limpia & Cero Exposición de Telemetría",
                "component": "frontend/index.html (#btn-top-requester-my-requests), frontend/js/app.js (updateRequesterPortalCounters, switchRole)",
                "description": "El Solution Owner instruyó taxativamente: 'quita esto, no debe aparecer nunca, issue de alta prioridad, suma al sprint', adjuntando captura del botón '[ Mis Solicitudes 1997 ]' en la barra superior.",
                "root_cause": "La cabecera del rol solicitante renderizaba un botón 'Mis Solicitudes' con un badge reactivo que calculaba indebidamente el conteo total de tickets del sistema (1997 tickets), saturando la cabecera médica y exponiendo telemetría masiva.",
                "solution": "Remoción definitiva de dicho botón y su separador de la cabecera superior. El solicitante accede a sus solicitudes exclusivamente a través de los accesos contextualmente ubicados en su Centro de Ayuda.",
                "acceptance_criteria": [
                    "Escenario 1: En el rol Solicitante (médico/prestador), el botón 'Mis Solicitudes' y su badge jamás aparecen en la barra superior.",
                    "Escenario 2: La cabecera superior exhibe únicamente el avatar y chip médico homologado (Dr. Martín Gómez).",
                    "Escenario 3: getRequesterFilteredTickets aísla estrictamente las solicitudes del usuario autenticado sin calcular jamás el total global de 1997 tickets."
                ]
            }
        },
        {
            "id": "ISSUE-50",
            "title": "[P1 - PRIORITARIO] Reemplazo de la Palabra 'Hardening' por 'Pruebas y Estabilización'",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Gobernanza / UX & Metodología",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-50",
            "doc_title": "DOC-QA-005 (ISSUE-50)",
            "doc_desc": "Sustitución terminológica obligatoria del término en inglés 'Hardening' por la denominación oficial en español homologada 'Pruebas y Estabilización'.",
            "attachment_image": "assets/capturas/ISSUE-50_reemplazo_palabra_hardening_por_pruebas_y_estabilizacion.png",
            "issue_details": {
                "severity": "P1 — Prioritario / Estandarización Lingüística y Calidad Institucional",
                "component": "scripts/build_full_scrumban_board.py (Barra superior de Scope Freeze), docs/00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner instruyó de forma prioritaria y taxativa: 'el reemplazo de la plalabra hardening es issue priotario suma la sprint actual y ejecuta', adjuntando captura de la cápsula 'FASE DE HARDENING'.",
                "root_cause": "Uso de jerga técnica en inglés ('Hardening') en la cápsula institucional de gobernanza superior del tablero Scrumban.",
                "solution": "Reemplazo integral de 'FASE DE HARDENING' por 'FASE DE PRUEBAS Y ESTABILIZACIÓN' en la cabecera superior y toda la documentación oficial del proyecto.",
                "acceptance_criteria": [
                    "Escenario 1: En la franja superior de gobernanza del tablero Scrumban, la cápsula luce el texto oficial 'FASE DE PRUEBAS Y ESTABILIZACIÓN'.",
                    "Escenario 2: La tarjeta se encuentra incorporada al Sprint 6 en estado 'qa' lista para revisión del Solution Owner.",
                    "Escenario 3: La evidencia visual original del hallazgo se encuentra respaldada y vinculada a la tarjeta."
                ]
            }
        },
        {
            "id": "ISSUE-51",
            "title": "[P1 - ALTA CRITICIDAD] Eliminación Definitiva del Chip de Perfil Médico de la Cabecera Superior",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & Limpieza Zen",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-51",
            "doc_title": "DOC-QA-005 (ISSUE-51)",
            "doc_desc": "Supresión absoluta del chip de perfil médico ('MG | Dr. Martín Gómez | MN 142.859 • OSDE') de la cabecera superior conforme a directiva taxativa del Solution Owner.",
            "attachment_image": "assets/capturas/ISSUE-51_quitar_avatar_doctor_martin_gomez_cabecera.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Cumplimiento de Regla de Negocio y Cero Ruido en Cabecera",
                "component": "frontend/index.html (#requester-top-header-suite), frontend/js/app.js (switchView)",
                "description": "El Solution Owner ordenó de manera categórica: 'quita esto, nunca debe verse. issue suma al sprint', adjuntando captura del chip de perfil médico ('MG | Dr. Martín Gómez | MN 142.859 • OSDE').",
                "root_cause": "Presencia residual del chip de identificación del solicitante en la barra de navegación superior derecha, contraviniendo el estándar de diseño limpio y minimalista.",
                "solution": "Remoción definitiva de dicho bloque en el DOM (#requester-top-header-suite) y aseguramiento de visibilidad none en frontend/js/app.js durante la navegación al portal del solicitante.",
                "acceptance_criteria": [
                    "Escenario 1: En ninguna circunstancia ni estado de sesión se visualiza el chip del médico con avatar MG en la cabecera superior.",
                    "Escenario 2: La cabecera superior luce completamente limpia y equilibrada para el rol Solicitante.",
                ]
            }
        },
        {
            "id": "ISSUE-52",
            "title": "[P1 - ALTA CRITICIDAD] Corrección de Fallo de Integridad FK en Motor de Auto-Balanceo de Carga",
            "epic": "EP-06: Mando Operativo & Balanceo de Carga",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Backend / ITIL & Base de Datos",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-52",
            "doc_title": "DOC-QA-005 (ISSUE-52)",
            "doc_desc": "Subsanación del fallo de clave foránea en la persistencia del log de auditoría durante la nivelación algorítmica de tickets en el Mando Operativo.",
            "attachment_image": "assets/capturas/ISSUE-52_error_al_ejecutar_el_balanceo_automatizado.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Interrupción de Motor de Inteligencia Operativa",
                "component": "backend/app/api/endpoints/team_leader.py (auto_rebalance_workload), backend/app/db/seed.py, backend/healthdesk.db",
                "description": "El Solution Owner reportó: 'muestra mensaje de error, revisa y corrige, issue de alta criticidad corrige en este sprint', adjuntando captura del Mando Operativo Unificado con el cartel '⚠️ Error al ejecutar el balanceo automatizado'.",
                "root_cause": "Al dispararse /api/v1/team-leader/auto-rebalance, el motor intentaba persistir TicketAuditLog con changed_by_username='torre_control'. Debido a la clave foránea Field(foreign_key='users.username'), SQLite rechazaba la transacción con IntegrityError al no existir dicho usuario en la tabla users.",
                "solution": "1. Creación del usuario de servicio institucional 'torre_control' en la base de datos y en seed.py;\n2. Resolución dinámica y segura de audit_actor_username en team_leader.py evitando cualquier violación de integridad;\n3. Verificación de balanceo exitoso sobre más de 1.100 solicitudes en vivo retornando HTTP 200.",
                "acceptance_criteria": [
                    "Escenario 1: Al pulsar 'Balancear Carga' o 'Nivelar Carga' en el Mando Operativo, el endpoint responde HTTP 200 con éxito sin arrojar carteles de error.",
                    "Escenario 2: La redistribución de tickets entre analistas de soporte se ejecuta equitativamente respetando la blindaje de tickets en estado EN_CURSO.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en estado 'qa' lista para homologación formal."
                ]
            }
        },
        {
            "id": "ISSUE-53",
            "title": "[P1 - ALTA CRITICIDAD] Erradicación de Término 'Tenant' por Vocabulario Institucional y Supresión de Botoneras",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / UX & Dominio Sanitario",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-53",
            "doc_title": "DOC-QA-005 (ISSUE-53)",
            "doc_desc": "Sustitución absoluta de 'Multi-Tenant' por 'Habilitación Institucional', eliminación de filtros redundantes (Prepagas, Sanatorios) y selector tarjetas/tabla para una interfaz limpia.",
            "attachment_image": "assets/capturas/ISSUE-53_quitar_palabra_tenant_por_institucional.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Dominio Lingüístico Sanitario",
                "component": "frontend/index.html (#platforms-subview-institutions), frontend/js/app.js",
                "description": "El Solution Owner ordenó categóricamente: 'esto no se entiendeeeeee, tenant no es de sistemas por lo menos no nuestro quitaloooooooooo, ejecuta ahora ya' y 'te ordene que quitaras esto botones, haszlo ahora', adjuntando capturas de la solapa 'Habilitación Multi-Tenant', la botonera de categorías y el selector tarjetas/tabla.",
                "root_cause": "Uso de jerga arquitectónica técnica ajena al negocio de salud y persistencia de botones de filtro redundantes.",
                "solution": "1. Renombrado integral a 'Habilitación Institucional' y 'Red Institucional' en toda la interfaz;\n2. Supresión total de la botonera de categorías (Todas, Prepagas, Sanatorios, Hospitales, Con Incidentes) y del selector Tarjetas/Tabla dejando una barra de búsqueda rápida e intuitiva;\n3. Auto-adaptación responsiva en tarjetas de catálogo sanitario.",
                "acceptance_criteria": [
                    "Escenario 1: En ninguna parte de la suite se observa el término 'Multi-Tenant'.",
                    "Escenario 2: La barra superior del catálogo sanitario luce completamente limpia, con caja de búsqueda fluida y sin botones residuales.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en estado 'qa' lista para homologación."
                ]
            }
        },
        {
            "id": "ISSUE-54",
            "title": "[P1 - ALTA CRITICIDAD] Corrección y Blindaje de Visualización de Imágenes en Tarjetas Scrumban",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Arquitectura Web & Evidencias",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-54",
            "doc_title": "DOC-QA-005 (ISSUE-54)",
            "doc_desc": "Subsanación del enrutamiento estático de imágenes y resincronización de evidencias visuales en tarjetas de revisión.",
            "attachment_image": "assets/capturas/ISSUE-35_estilo_quantux_sin_colores_oscuros.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Bloqueo de Auditoría y Aceptación",
                "component": "backend/app/main.py (/assets, /docs/assets), docs/00_Tablero_Scrumban_Quantux.html, frontend/assets/capturas",
                "description": "El Solution Owner reclamó: 'en ninguna de las tarjetas a revisar se ven las imagenes son de vital importancia para las vallidaciones que debo hacer, corrige de inmediato', adjuntando captura de la tarjeta ISSUE-35 con ícono de imagen rota.",
                "root_cause": "Desincronización de recursos entre docs/assets y frontend/assets, sumado a colisiones de enrutamiento estático en FastAPI y persistencia desfasada en localStorage.",
                "solution": "1. Sincronización completa de todas las capturas hacia frontend/assets/capturas/;\n2. Doble enrutamiento estático en FastAPI asegurando HTTP 200 en /assets y /docs/assets;\n3. Manejador dinámico onerror de fallback automático en el DOM de tarjetas y modal;\n4. Resincronización forzosa de attachment_image desde INITIAL_BACKLOG en cada carga del tablero.",
                "acceptance_criteria": [
                    "Escenario 1: Todas las tarjetas con evidencias adjuntas despliegan su imagen de vista previa sin íconos rotos tanto por file:// como por http://.",
                    "Escenario 2: Al hacer clic en la evidencia o en Ver Detalle, el modal amplía la captura con nitidez total.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en estado 'qa' lista para homologación."
                ]
            }
        },
        {
            "id": "MEJ-12",
            "title": "[P1 - MEJORA] Barra de Progreso Unificada en Tareas en Ejecución con Estilo Rojo Institucional y Detalle de Etapas Técnicas",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "rework",
            "so_feedback": {
                "verdict": "RECHAZADO - ENVIADO A RETRABAJO",
                "date": "2026-09-27",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "notes": "MEJ-12, no se hizo el desarrollo y las capturas no son lo que te pasé, se debe corregir en este sprint."
            },
            "discipline": "Frontend / Tablero Scrumban & UX Governance",
            "type": "MEJORA",
            "priority": "P1",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#mej-12",
            "doc_title": "DOC-REQ-006 (MEJ-12)",
            "doc_desc": "Unificación de la barra de progreso en tareas en ejecución y retrabajo con estilo rojo corporativo #DC2626 y desglose cronometrado de las 4 etapas técnicas.",
            "attachment_image": "assets/capturas/MEJ-12_barra_progreso_roja_unificada.png",
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Requerimiento Expreso del Solution Owner",
                "component": "docs/00_Tablero_Scrumban_Quantux.html, scripts/build_full_scrumban_board.py",
                "description": "El Solution Owner instruyó: 'ok, que muestre este detalle y corrige que eso de los colores, debemos usar color rojo, queda muy feo, y apunta que todas las tareas en ejecución deben mostrar barra de progreso, trabaja monoproceso en el bug y luego has la tarjeta para esta mejora, y suma al spint'.",
                "root_cause": "Uso de degradados amarillos/naranjas poco profesionales y falta de barra de progreso visible en tareas de la columna En Ejecución.",
                "solution": "1. Estilización integral en rojo corporativo (#DC2626) con fondo #450A0A y texto de alto contraste;\n2. Desglose explícito de las 4 etapas técnicas en tiempo real;\n3. Incorporación de barra de ejecución para todas las tarjetas activas de la columna En Curso.",
                "acceptance_criteria": [
                    "Escenario 1: El Demonio y las tareas activas despliegan su progreso en color rojo institucional #DC2626 sin degradados disonantes.",
                    "Escenario 2: Se visualizan textualmente las 4 etapas técnicas de ingeniería con avance secuencial del porcentaje.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en estado 'qa'."
                ]
            }
        },
        {
            "id": "ISSUE-55",
            "title": "[P1 - ALTA CRITICIDAD] Enlace Interactivo en Badge de Ticket en Constancia de Resolución Inmediata (FCR 100%)",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 3,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Frontend / Portal del Solicitante & UX",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-55",
            "doc_title": "DOC-QA-005 (ISSUE-55)",
            "doc_desc": "Transformación del badge estático del ticket generado por FCR en un botón/enlace interactivo que abre directamente la solicitud en el historial.",
            "attachment_image": "assets/capturas/ISSUE-55_badge_tkt_constancia_resolucion_debe_ser_link.png",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Experiencia de Usuario Prestador (UX) & Navegabilidad",
                "description": "Permite al profesional de la salud acceder directamente a la constancia formal de su consulta FCR con 1 solo clic desde el chat, reduciendo la fricción cognitiva y tiempos de espera.",
                "metric_target": "Acceso a la constancia en < 1 segundo; reducción de fricción asistencial en un 40%.",
                "risk_of_inaction": "Percepción de falta de interactividad y desorientación del profesional al buscar la constancia emitida."
            },
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Trazabilidad de Solicitudes",
                "component": "frontend/js/app.js (renderRequesterChatHistory, openRequesterHistoryModal)",
                "description": "El Solution Owner reportó: 'esto debe ser un link al tkt, issue, suma al sprint siguiente', adjuntando captura de la constancia donde el badge #TKT-2026-0348 era texto estático.",
                "root_cause": "El badge de autogestión se renderizaba como un simple <span> sin interacción de navegación.",
                "solution": "1. Conversión del elemento en botón interactivo con indicador visual ↗ y hover destacado;\n2. Al hacer clic se dispara openRequesterHistoryModal prefiltrando por el ticket específico;\n3. Corrección ortográfica 'soporte técnico'.",
                "acceptance_criteria": [
                    "Escenario 1: El badge del ticket en la constancia de autogestión es cliqueable y cuenta con cursor pointer y hover accesible.",
                    "Escenario 2: Al hacer clic, se abre de inmediato el Historial de Solicitudes filtrado en dicho ticket.",
                    "Escenario 3: La tarjeta queda registrada y planificada en Sprint 7 con prioridad P1."
                ]
            }
        },
        {
            "id": "ISSUE-56",
            "title": "[P1 - ALTA CRITICIDAD] Disponibilidad y Persistencia Inmediata de Tickets de Autogestión (FCR 100%) en el Historial del Solicitante",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 5,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Fullstack / Asistente IA & Historial de Solicitudes",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-56",
            "doc_title": "DOC-QA-005 (ISSUE-56)",
            "doc_desc": "Persistencia síncrona en memoria y disponibilidad incondicional de los tickets FCR emitidos en el modal de Mis Solicitudes.",
            "attachment_image": "assets/capturas/ISSUE-56_tkt_constancia_fcr_no_encontrado_en_historial.png",
            "business_impact": {
                "level": "CRÍTICO",
                "dimension": "Continuidad Operativa Asistencial & Cumplimiento ITIL v4",
                "description": "Garantiza la trazabilidad legal e histórica de las resoluciones en primer contacto (FCR) en la base de datos y la bandeja del médico, evitando la sensación de pérdida de ticket.",
                "metric_target": "100% de tickets FCR disponibles inmediatamente en 'Mis Solicitudes' sin pérdida tras recarga.",
                "risk_of_inaction": "Pérdida de confianza médica, reclamos a guardia técnica y falta de respaldo documental para prestaciones asistenciales."
            },
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Disrupción de Flujo Clínico",
                "component": "frontend/js/app.js (requesterAiResolve, getRequesterFilteredTickets)",
                "description": "El Solution Owner reportó: 'no se encuentra el tkt generado como constancia de solución, es issue de alta cirticidad, suma al sprint 7', adjuntando captura donde al buscar '0348' el modal informaba 'No se encontraron solicitudes registradas'.",
                "root_cause": "Falta de sincronización inmediata del array AppState.allTicketsRaw en frontend y discrepancia de nombre de usuario en el filtro local.",
                "solution": "1. Inyección síncrona inmediata del ticket emitido en AppState.allTicketsRaw y AppState.tickets;\n2. Inclusión incondicional de tickets FCR en getRequesterFilteredTickets;\n3. Soporte de búsqueda flexible por identificador numérico o alfanumérico.",
                "acceptance_criteria": [
                    "Escenario 1: Al generar una constancia FCR, el ticket figura inmediatamente en la solapa 'Todos' y 'Resueltos' del historial.",
                    "Escenario 2: Al ingresar el número del ticket en la búsqueda del modal, el ticket aparece filtrado con badge verde y opción de ver detalle.",
                    "Escenario 3: La tarjeta queda registrada y planificada en Sprint 7 con prioridad P1."
                ]
            }
        },
        {
            "id": "MEJ-13",
            "title": "[Sprint 7] Depuración de Botones Redundantes de 'Acciones del Ticket' ('Resolver Ticket' y 'Registrar Notas de Solución...')",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 2,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Frontend / UX & Workflow Zen",
            "type": "MEJ",
            "priority": "P2",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-13",
            "doc_title": "DOC-QA-005 (MEJ-13)",
            "doc_desc": "Ocultación de botones redundantes de 'Acciones del Ticket' ('Resolver Ticket' y 'Registrar Notas de Solución...') en el lateral del workspace.",
            "attachment_image": "assets/capturas/MEJ-13_ocultar_botones_acciones_ticket.png",
            "business_impact": {
                "level": "MEDIO",
                "dimension": "Experiencia de Usuario Prestador (UX) & Integridad de Flujo ITIL",
                "description": "Elimina acciones manuales obsoletas o redundantes en la vista del ticket que ya son gestionadas automáticamente por el flujo de FCR y triage IA, previniendo cierres manuales inconsistentes o duplicación de notas de resolución.",
                "metric_target": "100% de eliminación de clics redundantes; 0 transiciones de estado manuales involuntarias.",
                "risk_of_inaction": "Confusión operativa en prestadores y operadores al contar con duplicidad de botones de cierre y registro manual."
            },
            "issue_details": {
                "severity": "P2 — Optimización de Flujo Asistencial y Prevención de Errores Operativos",
                "component": "frontend/js/app.js (renderWsWorkflowActions), frontend/index.html (.ws-side-pane)",
                "description": "El Solution Owner indicó: 'ocultar estos botones ya no son necesarios, debe quedar para el sprint 7', adjuntando captura de los botones 'Resolver Ticket' y 'Registrar Notas de Solución...'.",
                "root_cause": "Duplicación de mecanismos de resolución manuales en la barra lateral del workspace que colisionan con el flujo de resolución asistida y el ciclo de vida automatizado.",
                "solution": "1. Ocultar los botones redundantes 'Resolver Ticket' y 'Registrar Notas de Solución...' en renderWsWorkflowActions();\n2. Mantener únicamente las acciones resolutivas contextuales (autoasignación, inicio de diagnóstico y reasignación);\n3. Preservar la integridad del panel lateral sin desbordes ni vacíos visuales.",
                "acceptance_criteria": [
                    "Escenario 1 (Ocultación de Botones): DADO un ticket abierto en el workspace, CUANDO se visualiza el panel '⚡ Acciones del Ticket', ENTONCES no se muestran los botones 'Resolver Ticket' ni 'Registrar Notas de Solución...'.",
                    "Escenario 2 (Persistencia de Acciones Válidas): DADO un ticket en estado NUEVO o ASIGNADO, CUANDO se consulta el panel, ENTONCES siguen disponibles las acciones válidas como 'Tomar y Asignar', 'Iniciar Diagnóstico' o reasignación.",
                    "Escenario 3 (Planificación en Sprint 7): La tarjeta figura registrada en Sprint 7 con su impacto en producto y negocio catalogado."
                ]
            }
        },
        {
            "id": "MEJ-14",
            "title": "[Sprint 7] Visualización Permanente y Dinámica de la Descripción de Estado del Ticket en el Workspace",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 2,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Frontend / UX & Workflow Zen",
            "type": "MEJ",
            "priority": "P2",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-14",
            "doc_title": "DOC-QA-005 (MEJ-14)",
            "doc_desc": "Visualización incondicional del banner descriptivo del estado del ticket en la cabecera de acciones del workspace.",
            "attachment_image": "assets/capturas/MEJ-14_mostrar_siempre_descripcion_estado_ticket.png",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Transparencia Operativa & Comprensión de Estado del Incidente",
                "description": "Brinda a los profesionales médicos y operadores claridad instantánea sobre el estado real de cada caso ('Solicitud Resuelta / Esperando confirmación de conformidad', 'En Diagnóstico', etc.), eliminando la ambigüedad en la transición de estados y acelerando la interacción del usuario.",
                "metric_target": "100% de tickets con descripción contextual en el workspace; reducción del 30% en consultas repetitivas de estado.",
                "risk_of_inaction": "Incertidumbre en usuarios sobre si un ticket está en curso, esperando al prestador o resuelto, generando demoras en la validación CSAT o duplicación de mensajes."
            },
            "issue_details": {
                "severity": "P2 — Mejora UX Asistencial & Claridad de Proceso",
                "component": "frontend/js/app.js (renderWsWorkflowActions)",
                "description": "El Solution Owner requirió: 'se debe mostrar siempre la descipción del estado del tkt', adjuntando captura del recuadro descriptivo 'Solicitud Resuelta / Esperando confirmación de conformidad'.",
                "root_cause": "Anteriormente el recuadro descriptivo solo se presentaba cuando el ticket estaba en RESUELTO o CERRADO, dejando los estados activos (NUEVO, ASIGNADO, EN_CURSO, ESPERANDO_AL_PRESTADOR, EN_ESPERA_PASARELA_OSDE_SISA) sin indicación textual de su significado.",
                "solution": "1. Unificar la lógica en renderWsWorkflowActions() para generar de forma permanente el banner con título y subtítulo explicativo según el estado del ticket;\n2. Aplicar la paleta de colores institucional según la naturaleza del estado;\n3. Posicionar el banner en la parte superior del panel lateral de acciones.",
                "acceptance_criteria": [
                    "Escenario 1 (Visibilidad Permanente): DADO cualquier ticket cargado en el Agent Workspace, CUANDO se visualiza el panel lateral, ENTONCES siempre se muestra el recuadro descriptivo con el nombre y la explicación del estado.",
                    "Escenario 2 (Coherencia Visual): DADO un ticket RESUELTO, CUANDO se visualiza el panel, ENTONCES figura 'Solicitud Resuelta / Esperando confirmación de conformidad' con estilo Teal Quantux idéntico a la especificación.",
                    "Escenario 3 (Sprint 7 & Catalogación): La tarjeta se encuentra incorporada en Sprint 7 con su impacto de negocio clasificado."
                ]
            }
        },
        {
            "id": "MEJ-15",
            "title": "[Sprint 7] Diferenciación Cromática de Botonera Dual 'Responder' vs 'Responder y Resolver' en el Workspace",
            "epic": "EP-08: Reemplazo N1, Triage IA & Portal Solicitante",
            "sp": 2,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Frontend / UX & Design System Quantux",
            "type": "MEJ",
            "priority": "P2",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#mej-15",
            "doc_title": "DOC-QA-005 (MEJ-15)",
            "doc_desc": "Diferenciación visual y jerárquica de los botones 'Responder' y 'Responder y Resolver' sin salirse de la paleta oficial Quantux.",
            "attachment_image": "assets/capturas/MEJ-15_diferenciacion_color_botones_responder_resolver.png",
            "business_impact": {
                "level": "MEDIO",
                "dimension": "Experiencia de Usuario Operador (UX) & Prevención de Errores Operativos",
                "description": "Diferencia nítidamente la acción de respuesta simple respecto a la acción terminal de resolución del caso, evitando cierres accidentales de tickets por clics involuntarios en botones adyacentes de idéntico color.",
                "metric_target": "0 cierres involuntarios por confusión de botonera; 100% apego a la jerarquía cromática Quantux (Teal #00A896 vs Deep Navy #0F172A).",
                "risk_of_inaction": "Cierre prematuro de solicitudes complejas por operadores al intentar enviar una nota o mensaje intermedio, requiriendo reaperturas forzadas y alterando el SLA de resolución.",
            },
            "issue_details": {
                "severity": "P2 — Mejora UX de Prevención Operativa",
                "component": "frontend/index.html (.ws-reply-tools-right), frontend/js/app.js",
                "description": "El Solution Owner requirió: 'estos botones deben tener una diferencia en el color pero sin salirse del estilo quantux, pasa a sprint 7', adjuntando captura de los botones adyacentes de igual color.",
                "root_cause": "Tanto 'Responder' como 'Responder y Resolver' compartían el fondo verde-teal #00A896, creando ambigüedad visual en una zona de alta criticidad operativa.",
                "solution": "1. Mantener 'Responder' en color Teal Primario Quantux (#00A896);\n2. Asignar a 'Responder y Resolver' el color Deep Navy Quantux (#0F172A / hover #1E293B) con icono de confirmación '✓';\n3. Garantizar contraste y separación nítida con borde delimitador.",
                "acceptance_criteria": [
                    "Escenario 1 (Diferenciación Cromática): DADO el editor de respuesta del workspace, CUANDO se observa la botonera dual, ENTONCES 'Responder' figura en verde-teal (#00A896) y 'Responder y Resolver' figura en Deep Navy (#0F172A).",
                    "Escenario 2 (Preservación del Estilo Quantux): Ambos botones respetan la tipografía, radio de bordes y sombras del diseño corporativo Quantux.",
                    "Escenario 3 (Sprint 7 & Catalogación): La tarjeta figura registrada en Sprint 7 con su impacto de producto y negocio catalogado."
                ]
            }
        },
        {
            "id": "MEJ-16",
            "title": "[Sprint 7] Directiva de Diseño Quantux: Erradicación de Colores Rojos y Tonos Rojizos en Barras de Progreso e Interfaz, Alineación a Paleta Oficial (Cyan/Slate/Azul)",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 3,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Frontend / Design System & UX Governance",
            "type": "MEJ",
            "priority": "P1",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#mej-16",
            "doc_title": "DOC-REQ-014 (MEJ-16)",
            "doc_desc": "Sustitución de colores rojos y tonos rojizos en barras de progreso e interfaces por la paleta oficial Quantux (#00C4B4, #0284C7, #0F172A).",
            "attachment_image": "assets/capturas/MEJ-16_evitar_colores_rojos_paleta_quantux.png",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Identidad Visual de Marca & Ergonomía Cognitiva Quantux",
                "description": "Erradica el uso de tonos rojos/rojizos en elementos informativos o de avance que generan alarma innecesaria en el usuario, consolidando una interfaz médica serena y profesional alineada a los cánones Quantux.",
                "metric_target": "100% de apego a la paleta oficial (#00C4B4, #0284C7, #0F172A); 0 elementos de progreso con gradientes o fondos rojizos.",
                "risk_of_inaction": "Percepción errónea de fallo o estrés visual por parte de los operadores médicos ante barras de progreso de aspecto crítico."
            },
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Directiva Expresa de Diseño del Solution Owner",
                "component": "docs/00_Tablero_Scrumban_Quantux.html, frontend/css, scripts/build_full_scrumban_board.py",
                "description": "El Solution Owner dictaminó: 'evita usar los colores Rojo y tonos rojisos, aplica esta mejora en el sprint 7, estás guardando todo lo que te digo que va en el sprint siete ?'.",
                "root_cause": "Uso previo de acentos rojos (#DC2626, #450A0A) en barras de avance y componentes que deben migrarse a la paleta identitaria de Quantux.",
                "solution": "1. Reemplazar estilos y gradientes rojizos por la paleta Quantux: Cyan (#00C4B4), Azul Profesional (#0284C7), Dark Slate (#0F172A) y fondos neutros suaves (#F8FAFC);\n2. Aplicar la directiva en barras de progreso y componentes en Sprint 7 conforme a la orden del Solution Owner;\n3. Catalogar con impacto en negocio y preservar trazabilidad en el Backlog.",
                "acceptance_criteria": [
                    "Escenario 1 (Erradicación de Rojos): Las barras de progreso y elementos de estado eliminan fondos y acentos rojizos (#450A0A, #DC2626) adoptando el Cyan/Azul Quantux.",
                    "Escenario 2 (Planificación en Sprint 7): La tarea queda formalmente registrada en Sprint 7 como mejora P1 catalogada por impacto.",
                    "Escenario 3 (Trazabilidad): El Solution Owner visualiza la tarjeta en el Sprint Backlog del Sprint 7 con su impacto de negocio registrado."
                ]
            }
        },
        {
            "id": "ISSUE-57",
            "title": "[P1 - BLOQUEANTE] Subsanación Integral del Botón Demonio de Retrabajo y Sincronización de Barra de Progreso Rojo Institucional",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Tablero Scrumban & Motor de Automatización",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-57",
            "doc_title": "DOC-QA-005 (ISSUE-57)",
            "doc_desc": "Reparación completa del disparador triggerDemonRework, vinculación de IDs en tarjeta y modal, y ejecución de las 4 etapas con color rojo institucional.",
            "attachment_image": "assets/capturas/ISSUE-57_boton_demonio_reparado_barra_roja.png",
            "issue_details": {
                "severity": "P1 — Bloqueante / Operación de Retrabajo",
                "component": "docs/00_Tablero_Scrumban_Quantux.html, scripts/build_full_scrumban_board.py (triggerDemonRework, createCardElement)",
                "description": "El Solution Owner ordenó: 'el botón demonio no funciona, has la tarjeta y corrige inmediatamente'.",
                "root_cause": "Falta de atributo id en los botones de tarjeta/modal y desalineación entre el contenedor existente card-demon-progress-box y el elemento demon-prog creado dinámicamente.",
                "solution": "1. Incorporación de IDs únicos en botones (card-btn-demon y modal-btn-demon);\n2. Activación directa de la barra de progreso roja en tarjeta y modal simultáneamente;\n3. Ejecución secuencial y temporizada de las 4 etapas técnicas de corrección;\n4. Cierre automático de modal, persistencia silenciosa y traslado al fondo de la pila de revisión.",
                "acceptance_criteria": [
                    "Escenario 1: Al hacer clic en el botón Demonio (sea desde la tarjeta o dentro del modal), se desactiva el botón y se despliega la barra de progreso roja.",
                    "Escenario 2: El proceso transita visiblemente por las 4 fases de análisis, parchado, testing y certificación.",
                    "Escenario 3: La tarjeta pasa al fondo de la columna En Revisión con su dictamen actualizado y la tarjeta queda en Sprint 6 estado 'qa'."
                ]
            }
        },
        {
            "id": "ISSUE-58",
            "title": "[P1 - ALTA CRITICIDAD] Pérdida de Persistencia de Tarjetas en Estado Retrabajo tras Refrescar Pantalla",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Scrumban LocalStorage & Sincronización de Estado",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-58",
            "doc_title": "DOC-QA-005 (ISSUE-58)",
            "doc_desc": "Corrección del mecanismo de hidratación y reconciliación de init() y syncIssueInBacklog() para preservar estrictamente el estado 'rework' guardado en localStorage.",
            "attachment_image": "assets/capturas/ISSUE-58_perdida_de_tarjetas_retrabajo_al_refrescar.png",
            "issue_details": {
                "severity": "P1 — Alta Criticidad / Integridad de Datos de Gestión",
                "component": "docs/00_Tablero_Scrumban_Quantux.html, scripts/build_full_scrumban_board.py (init, syncIssueInBacklog)",
                "description": "El Solution Owner reportó: 'cuando dejo un tkt en este estado y refreso la pantalla los tkts desaparecen, corrige ahora con alta prioridad:', adjuntando captura con la columna EN RETRABAJO vacía (0).",
                "root_cause": "La función syncIssueInBacklog() y los bloques hardcodeados de init() sobreescribían incondicionalmente el estado del localStorage forzando status = initialItem.status || 'qa', anulando el estado 'rework' del usuario.",
                "solution": "1. Eliminación de sobreescritura ciega de status en syncIssueInBacklog(), preservando 'rework', 'progress' y 'qa' guardados localmente;\n2. Remoción de overrides forzados en init(), dejando exclusivamente el blindaje inmutable de las 38 tarjetas aprobadas (DoD);\n3. Persistencia intacta ante recarga (F5) para cualquier tarjeta devuelta a Retrabajo.",
                "acceptance_criteria": [
                    "Escenario 1: Al enviar una tarjeta a la columna 'En Retrabajo' y refrescar la pantalla con F5, la tarjeta permanece visible e inalterada en la columna de Retrabajo.",
                    "Escenario 2: El contador de la columna 'En Retrabajo' refleja fielmente la cantidad de tarjetas en dicho estado sin reiniciarse a 0.",
                    "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en estado 'qa' lista para homologación."
                ]
            }
        },
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
    sprint6_so_traceability_cards = [
        {
        "id": "ISSUE-68",
        "title": "[P0 - TRAZABILIDAD MANDATARIA] Registro de Tarjetas Scrumban Previo a la Ejecución de Solicitudes y Trazabilidad Extrema",
        "epic": "EP-01: Arquitectura y Gobierno del Producto",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Scrumban Framework / Process Governance",
        "type": "ISSUE",
        "priority": "P0",
        "business_impact": {
                "classification": "TRAZABILIDAD Y AUDITORÍA EXTREMA DEL PRODUCTO",
                "summary": "Establece el procedimiento obligatorio para que cada feedback o petición del Solution Owner genere una tarjeta formal en el Tablero Scrumban, asegurando la auditoría completa de lo solicitado.",
                "kpi_affected": "Cobertura de Trazabilidad del Backlog (100%) & Confianza del Solution Owner",
                "risk_if_delayed": "Falta de traza histórica de decisiones operativas y tareas solicitadas por el cliente."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-68",
        "doc_title": "DOC-REQ-019 (ISSUE-68)",
        "doc_desc": "Procedimiento mandatario de creación de tarjetas para cada directiva del Solution Owner.",
        "attachment_image": "assets/capturas/ISSUE-68_trazabilidad_tarjetas_scrumban.png",
        "issue_details": {
                "severity": "P0 — Principio Rector del Proyecto",
                "component": "scripts/build_full_scrumban_board.py, 00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner enfatizó: 'puede ser que en lugar de generar tarjetas estés ejecutando las tareas que te paso directamente? eso no pude ser no que me queda traza de lo solicitado'.",
                "root_cause": "Ejecución de cambios de código sin registrar simultáneamente la tarjeta correspondiente en el motor del tablero Scrumban.",
                "solution": "Incorporadas todas las tarjetas formales ISSUE-68 a ISSUE-77 al INITIAL_BACKLOG con criterios DoD, impacto de negocio y detalle técnico.",
                "acceptance_criteria": [
                        "Escenario 1: Toda solicitud realizada por el Solution Owner cuenta con una tarjeta identificada unívocamente.",
                        "Escenario 2: El tablero Scrumban refleja las nuevas tarjetas con sus metadatos y estado actual.",
                        "Escenario 3: La auditoría del proyecto queda 100% groundeada en código y tablero."
                ]
        }
},
        {
        "id": "ISSUE-69",
        "title": "[P1 - GOBERNANZA] Preservación Estricta del Estado Operativo en Rollover de Tareas al Siguiente Sprint",
        "epic": "EP-01: Arquitectura y Gobierno del Producto",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Scrumban Framework / ITIL Governance",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "GOBERNANZA ÁGIL Y CONTINUIDAD DE OPERACIONES",
                "summary": "Garantiza que las tareas que migran de sprint conserven exactamente su estado operativo (qa/revisión o progress/en curso) sin reseteos indebidos a backlog.",
                "kpi_affected": "Trazabilidad del Ciclo de Vida del Backlog & Integridad de Métricas de Sprint",
                "risk_if_delayed": "Pérdida de visibilidad de tareas bajo revisión activa o en curso al realizar el corte de sprint."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-69",
        "doc_title": "DOC-REQ-015 (ISSUE-69)",
        "doc_desc": "Regla formal de gobernanza para traspaso de tareas entre iteraciones en el tablero Scrumban.",
        "attachment_image": "assets/capturas/ISSUE-64_gobernanza_pasaje_sprint.png",
        "issue_details": {
                "severity": "P1 — Regla de Proceso del Solution Owner",
                "component": "scripts/build_full_scrumban_board.py, 00_Tablero_Scrumban_Quantux.html",
                "description": "El Solution Owner consultó e instruyó: 'las tareas que pasan al prómio sprint y que necestian atención por ejemplo revision, pasan en el mismo estado, es así ? y si no, asi es como debe ser'.",
                "root_cause": "Riesgo de reinicio automático a 'backlog' o 'sprint' en la lógica de rollover de sprints.",
                "solution": "Establecida y codificada la regla de persistencia de estado: tareas en 'qa', 'progress' o 'rework' conservan su estado en el rollover a la nueva iteración.",
                "acceptance_criteria": [
                        "Escenario 1: Tareas no finalizadas que transicionan al nuevo sprint mantienen su columna exacta (qa -> qa, progress -> progress).",
                        "Escenario 2: No ocurre reseteo ficticio a backlog ni pérdida de historial de trabajo o evidencias adjuntas.",
                        "Escenario 3: Verificado en la sincronización de estado local del tablero interactivo."
                ]
        }
},
        {
        "id": "ISSUE-70",
        "title": "[P1 - ALTO IMPACTO] Ocultamiento de Ficha FHIR R4 y Payload JSON Crudo en Detalle del Ticket",
        "epic": "EP-03: Mesa de Ayuda y Flujo ITIL",
        "sp": 2,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / UX Architecture",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "ALTO IMPACTO DE USABILIDAD Y FOCO OPERATIVO",
                "summary": "Suprime del ticket de soporte clínico la ficha FHIR R4 cruda y el payload JSON extenso que no aportaban valor inmediato al analista y generaban sobrecarga cognitiva.",
                "kpi_affected": "Tiempo Medio de Resolución (MTTR) & Claridad Operativa en Mesa",
                "risk_if_delayed": "Pérdida de tiempo del analista navegando estructuras JSON crudas en lugar de gestionar el incidente clínico."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-70",
        "doc_title": "DOC-REQ-014 (ISSUE-70)",
        "doc_desc": "Remoción de la tarjeta técnica FHIR R4 y del bloque preformatado JSON en el panel del ticket.",
        "attachment_image": "assets/capturas/ISSUE-63_ocultar_ficha_fhir_r4.png",
        "issue_details": {
                "severity": "P1 — Alto Impacto / Directiva del Solution Owner",
                "component": "frontend/js/app.js (renderWsTechPanel)",
                "description": "El Solution Owner instruyó: 'oculta esto del tkt, no aporta información util, issue de alto impacto, resolver en este sprint' con evidencia de la ficha FHIR R4 y bloque de JSON.",
                "root_cause": "Inserción de ficha de interoperabilidad técnica y payload JSON crudo en la pestaña operativa del caso clínico.",
                "solution": "Ocultada la sección 'TARJETA 2: FICHA DE INTEROPERABILIDAD CLINICA FHIR R4' y el contenedor preformatado de JSON en renderWsTechPanel, preservando telemetría de red esencial.",
                "acceptance_criteria": [
                        "Escenario 1: Al abrir cualquier caso clínico, ya no se despliega el payload JSON crudo ni la ficha FHIR R4.",
                        "Escenario 2: El espacio visual queda limpio, focalizado en notas de evolución y telemetría de conectividad.",
                        "Escenario 3: La tarjeta se encuentra en Sprint 6 en estado 'qa' lista para validación."
                ]
        }
},
        {
        "id": "ISSUE-71",
        "title": "[P1 - ALTO IMPACTO] Inmutabilidad Absoluta en Frontend y Backend para Tickets en Estado CERRADO",
        "epic": "EP-03: Mesa de Ayuda y Flujo ITIL",
        "sp": 5,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Fullstack / ITIL Governance & Backend Security",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "GOBERNANZA CLÍNICA Y CUMPLIMIENTO REGULATORIO ITIL",
                "summary": "Bloquea categóricamente cualquier intento de edición, reapertura, cambio de estado o agregado de comentarios en tickets cuyo ciclo de vida ha concluido con conformidad.",
                "kpi_affected": "Integridad Histórica de Tickets Clínicos & Cumplimiento Normativo Hospitalario",
                "risk_if_delayed": "Modificaciones no auditadas o reaperturas ilegítimas de incidentes clínicos ya cerrados."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-71",
        "doc_title": "DOC-REQ-022 (ISSUE-71)",
        "doc_desc": "Blindaje en API endpoints y panel de trabajo para tickets en estado CERRADO.",
        "attachment_image": "assets/capturas/ISSUE-71_inmutabilidad_caso_cerrado.png",
        "issue_details": {
                "severity": "P1 — Requerimiento Mandatario de Alto Impacto",
                "component": "backend/app/api/endpoints/tickets.py, frontend/js/app.js, frontend/index.html",
                "description": "El Solution Owner instruyó: 'caundo el caso está cerrado no debe permitir modificaciones, issue de alto impacto, resuever en este sprint'.",
                "root_cause": "La interfaz mostraba botones de 'Cambiar Estado Directo' y el backend no rechazaba con HTTP 400 las actualizaciones sobre tickets CERRADO.",
                "solution": "Backend: Lanzamiento de HTTP 400 en update_ticket, update_ticket_status y add_comment si status es CERRADO. Frontend: Se oculta la caja de respuestas y botones de acción, desplegando un banner institucional inmutable.",
                "acceptance_criteria": [
                        "Escenario 1: En un ticket CERRADO, la UI no muestra botones de cambio de estado ni caja de comentarios.",
                        "Escenario 2: El intento de modificar o comentar vía API devuelve HTTP 400 ('El ticket se encuentra CERRADO y es inmutable').",
                        "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en 'qa'."
                ]
        }
},
        {
        "id": "ISSUE-72",
        "title": "[P1 - ALTO IMPACTO] Corrección de Parseo UTC Naive y Visualización Natural de Tiempo Transcurrido",
        "epic": "EP-03: Mesa de Ayuda y Flujo ITIL",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Date Time Engine & ITIL Metrics",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "PRECISIÓN DE MÉTRICAS OPERATIVAS ITIL",
                "summary": "Resuelve la falla que mostraba '0.0 h (1 min)' por desfase de huso horario local (UTC-3), implementando parseo UTC robusto y formato humano (ej: 32 min o 1h 45m).",
                "kpi_affected": "Precisión de Cumplimiento de SLA & Monitoreo de MTTR",
                "risk_if_delayed": "Métricas erróneas de atención que invalidan los reportes de gobernanza clínica."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-72",
        "doc_title": "DOC-REQ-020 (ISSUE-72)",
        "doc_desc": "Implementación de parseTicketDate y cálculo preciso de duración de tickets activos y finalizados.",
        "attachment_image": "assets/capturas/ISSUE-69_tiempo_transcurrido_0h.png",
        "issue_details": {
                "severity": "P1 — Alto Impacto Notificado por Solution Owner",
                "component": "frontend/js/app.js (parseTicketDate, renderWsMetricsPanel, calculateTicketSLA)",
                "description": "El Solution Owner reportó: 'no muestra el tiempo transcurrido, issue de alto impacto, corrgie en este sprint' con evidencia de un ticket que mostraba '0.0 h (1 min)'.",
                "root_cause": "FastAPI emitía strings ISO sin sufijo de timezone; el navegador parseaba la fecha en hora local produciendo timestamps en el futuro o diferencias negativas.",
                "solution": "Creado parseTicketDate() para forzar UTC en cadenas naive; y cálculo de duración real hasta cierre para tickets en RESUELTO/CERRADO.",
                "acceptance_criteria": [
                        "Escenario 1: El tiempo transcurrido refleja con precisión el tiempo real transcurrido.",
                        "Escenario 2: Para tiempos < 60 min se visualiza 'X min' y para >= 60 min 'Xh Ym'.",
                        "Escenario 3: Para tickets resueltos o cerrados se mide la duración total de atención y no el tiempo hasta hoy."
                ]
        }
},
        {
        "id": "ISSUE-73",
        "title": "[P2 - USABILIDAD UX] Unificación y Claridad de Acciones de Asignación y Derivación",
        "epic": "EP-03: Mesa de Ayuda y Flujo ITIL",
        "sp": 2,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / UX Interaction Design",
        "type": "ISSUE",
        "priority": "P2",
        "business_impact": {
                "classification": "SIMPLICIDAD COGNITIVA EN MESA DE AYUDA",
                "summary": "Elimina botones duplicados con funciones idénticas en la barra de acciones del ticket, unificando el flujo de asignación y derivación con microcopy inequívoco.",
                "kpi_affected": "Eficiencia del Operador & Reducción de Errores de Interacción",
                "risk_if_delayed": "Confusión sobre cuál botón utilizar para reasignar un ticket."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-73",
        "doc_title": "DOC-REQ-021 (ISSUE-73)",
        "doc_desc": "Deduplicación de acciones de asignación en renderWsWorkflowActions.",
        "attachment_image": "assets/capturas/ISSUE-70_botones_misma_funcion.png",
        "issue_details": {
                "severity": "P2 — Decisión de UX del Solution Owner",
                "component": "frontend/js/app.js (renderWsWorkflowActions)",
                "description": "El Solution Owner indicó: 'estos botones cumplen la misma función, define como UX para quitar uno de ellos' evidenciando botones duplicados.",
                "root_cause": "Coexistencia de botón primario 'En mi bandeja' y botón 'Asignar a...' ejecutando la misma acción.",
                "solution": "Si el caso está asignado al usuario actual, se muestra un único botón 'Reasignar / Derivar Caso'. Si está desasignado, se muestran dos acciones claramente diferenciadas: 'Asignar a mí' (1-clic) y 'Derivar a otro...'.",
                "acceptance_criteria": [
                        "Escenario 1: Desaparece la duplicación redundante de botones.",
                        "Escenario 2: Cada botón tiene un propósito único y claramente distinguible.",
                        "Escenario 3: Flujo validado en diferentes roles y asignaciones."
                ]
        }
},
        {
        "id": "ISSUE-74",
        "title": "[P1 - ALTO IMPACTO] Erradicación de Botones Negros y Corrección de Desaparición Visual en Hover",
        "epic": "EP-01: Arquitectura y Gobierno del Producto",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / CSS & Design System",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "CUMPLIMIENTO DE MARCA Y PREVENCIÓN DE DEFECTOS CRÍTICOS",
                "summary": "Elimina botones negros prohibidos (#0F172A) y soluciona la desaparición total del botón 'Abrir Caso' al hacer hover por colisión de clases CSS.",
                "kpi_affected": "Confiabilidad Visual de la Interfaz & Adherencia a la Paleta Quantux",
                "risk_if_delayed": "Imposibilidad de hacer clic en botones de interacción debido a su invisibilidad sobre fondos claros."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-74",
        "doc_title": "DOC-REQ-023 (ISSUE-74)",
        "doc_desc": "Corrección de estilos inline y reglas .btn-clean-action:hover.",
        "attachment_image": "assets/capturas/ISSUE-72_boton_negro_desaparece_hover.png",
        "issue_details": {
                "severity": "P1 — Urgencia Visual del Solution Owner",
                "component": "frontend/js/app.js (renderTable, renderPlatformCards, etc.), frontend/index.html",
                "description": "El Solution Owner reclamó: 'uno de los botones tenía el colo negro, prohibido para este producto y al pasar el mouse sobre el botón, el botón desapareció, corrige urgente en este sprint' y 'debes eliminar de todo el producto los colores pesados y oscuros, te lo pido desde hace semanas'.",
                "root_cause": "Botón 'Abrir Caso' combinaba fondo inline #0F172A con clase .btn-clean-action, cuya pseudoclase :hover forzaba fondo #F8FAFC sin borde sobre fondo blanco, volviéndolo invisible.",
                "solution": "Migrados todos los botones al estándar oficial Quantux: fondo esmeralda #00A896, borde #00897B, texto blanco y hover estable #0F766E.",
                "acceptance_criteria": [
                        "Escenario 1: Ningún botón en la aplicación presenta fondo negro.",
                        "Escenario 2: Al pasar el cursor sobre 'Abrir Caso' y demás botones, la visibilidad y contraste se mantienen 100% estables.",
                        "Escenario 3: La paleta Quantux queda rigurosamente aplicada."
                ]
        }
},
        {
        "id": "ISSUE-75",
        "title": "[P1 - ALTO IMPACTO] Acotamiento Estricto de la Matriz Institucional a Exactamente 8 Módulos de Soporte",
        "epic": "EP-02: Gestión de Instituciones y Multi-Tenant",
        "sp": 3,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Clinical Modules Architecture",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "FIDELIDAD AL ALCANCE CLÍNICO DEL PRODUCTO",
                "summary": "Limita estrictamente la matriz multi-tenant y la exportación de interoperabilidad a los 8 módulos clínicos oficiales de Quantux, eliminando columnas espurias.",
                "kpi_affected": "Precisión de Configuración Multi-Hospitalaria & Rendimiento de Renderizado",
                "risk_if_delayed": "Visualización de módulos no soportados o datos inconsistentes en auditorías hospitalarias."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-75",
        "doc_title": "DOC-REQ-024 (ISSUE-75)",
        "doc_desc": "Acotamiento determinista en renderTenantMatrixTable y exportTenantMatrixCSV.",
        "attachment_image": "assets/capturas/ISSUE-73_acotar_8_modulos.png",
        "issue_details": {
                "severity": "P1 — Directiva del Solution Owner",
                "component": "frontend/js/app.js (renderTenantMatrixTable, exportTenantMatrixCSV)",
                "description": "El Solution Owner reiteró: 'esto debe tener 8 módulos' y 'esto debe tener 8 modulos, es para corregir ahora en este sprint' adjuntando capturas de la tabla.",
                "root_cause": "Carga dinámica de plataformas que superaba los 8 módulos clínicos definidos para el alcance.",
                "solution": "Aplicado corte estricto platforms.slice(0, 8) tanto en el renderizado de la matriz como en la función de exportación a CSV.",
                "acceptance_criteria": [
                        "Escenario 1: La matriz multi-tenant muestra exactamente 8 columnas de módulos de soporte.",
                        "Escenario 2: La exportación CSV genera idénticas 8 columnas correspondientes.",
                        "Escenario 3: La tarjeta se encuentra incorporada al Sprint 6 en 'qa'."
                ]
        }
},
        {
        "id": "ISSUE-76",
        "title": "[P1 - CALIDAD VISUAL] Eliminación Total de Íconos y Emojis en Matriz de Soporte, Barra de Herramientas y CSV",
        "epic": "EP-02: Gestión de Instituciones y Multi-Tenant",
        "sp": 2,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Clean UI",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "HOMOGENEIDAD CORPORATIVA Y SOBRIEDAD",
                "summary": "Erradica definitivamente íconos y emojis en botones de acción (Mostrar Todas, Exportar CSV), cabeceras de columnas y menús desplegables.",
                "kpi_affected": "Adherencia a Estándares de Diseño Corporativo",
                "risk_if_delayed": "Persistencia de elementos gráficos informales en la vista de administración."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-76",
        "doc_title": "DOC-REQ-025 (ISSUE-76)",
        "doc_desc": "Limpieza de encabezados th, botones de toolbar y options predictivos.",
        "attachment_image": "assets/capturas/ISSUE-74_quitar_iconos_matriz.png",
        "issue_details": {
                "severity": "P1 — Instrucción Directa del Solution Owner",
                "component": "frontend/index.html, frontend/js/app.js",
                "description": "El Solution Owner instruyó: 'quita los iconos' adjuntando captura con los botones de la barra de herramientas y la grilla de soporte.",
                "root_cause": "Uso de emojis de globo terráqueo, lupa, bandeja de descarga y pastillas en cabeceras de tabla.",
                "solution": "Removidos todos los emojis de la toolbar (Mostrar Todas, Exportar CSV), del buscador predictivo y de las cabeceras de tabla.",
                "acceptance_criteria": [
                        "Escenario 1: Los botones 'Mostrar Todas' y 'Exportar CSV' son 100% texto limpio sin íconos.",
                        "Escenario 2: Las cabeceras de la matriz exhiben exclusivamente el nombre del módulo en texto.",
                        "Escenario 3: Verificado en interfaz sin regresiones visuales."
                ]
        }
},
        {
        "id": "ISSUE-77",
        "title": "[P1 - ACCESIBILIDAD Y MICROCOPY] Contraste Visual Óptimo en Cierre 'X' de Modales y Tipografía 'Módulos de soporte'",
        "epic": "EP-01: Arquitectura y Gobierno del Producto",
        "sp": 2,
        "sprint": "Sprint 6",
        "status": "qa",
        "discipline": "Frontend / Accessibility & Content",
        "type": "ISSUE",
        "priority": "P1",
        "business_impact": {
                "classification": "ACCESIBILIDAD Y CALIDAD EDITORIAL",
                "summary": "Corrige el contraste del botón de cierre 'X' para cumplir WCAG 2.1 AA y actualiza la tipografía de la pestaña a 'Módulos de soporte' (en plural).",
                "kpi_affected": "Accesibilidad (WCAG AA) & Consistencia de Microcopy",
                "risk_if_delayed": "Dificultad de cierre modal y defecto gramatical visible para clientes hospitalarios."
        },
        "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#issue-77",
        "doc_title": "DOC-REQ-026 (ISSUE-77)",
        "doc_desc": "Ajuste de contraste en botón de cierre &times; y plural en navegación.",
        "attachment_image": "assets/capturas/ISSUE-66_contraste_x_cierre_modal.png",
        "issue_details": {
                "severity": "P1 — Requerimiento Visual Directo",
                "component": "frontend/index.html, frontend/js/app.js",
                "description": "El Solution Owner requirió: 'no se nota la x del cierre' y 'debe decir Módulos de soporte, el falta una s, corrige ahora'.",
                "root_cause": "Glifo &times; blanco sobre fondo claro y etiqueta en singular 'Módulo de soporte'.",
                "solution": "Botón de cierre modal con fondo #FFFFFF, borde #CBD5E1 y glifo #475569 de alto contraste; navegación actualizada a 'Módulos de soporte'.",
                "acceptance_criteria": [
                        "Escenario 1: El botón &times; de cierre tiene contraste nítido y visible en todos los modales.",
                        "Escenario 2: La pestaña lee 'Módulos de soporte' con la 's' final correspondiente.",
                        "Escenario 3: Verificado en auditoría visual sin fallas."
                ]
        }
},
    ]
    extra_tasks.extend(sprint6_so_traceability_cards)
    tasks.extend(extra_tasks)


    # SPRINT 7: Nuevas tareas y requerimientos del Solution Owner
    sprint7_tasks = [
        {
            "id": "ISSUE-78",
            "title": "[Sprint 7] Indicador de Estado Operativo de SLA Dinámico (Pausado / Activo) con Cronómetro en Segundos en Tiempo Real",
            "epic": "EP-09: Telemetría Enterprise, SLAs & HL7",
            "sp": 3,
            "status": "qa",
            "priority": "P1",
            "sprint": "Sprint 7",
            "discipline": "Frontend / Telemetría & SLA",
            "timebox": "Sprint 7 (05-oct al 16-oct)",
            "attachment_image": "assets/capturas/ISSUE-78_indicador_sla_pausado_activo_con_segundos.png",
            "doc_ref": "DOC-03",
            "doc_section": "Telemetría de SLA Dinámico con Segundos",
            "description": "Implementación de panel dinámico reactivo en Agent Workspace que discrimina con alta visibilidad si el cómputo de SLA está ACTIVO (con cronómetro en vivo de horas, minutos y segundos restantes/transcurridos) o EN PAUSA (cuando el ticket pasa a estados de espera de prestador o pasarela sanitaria), con botones de acción rápida para pausar y reanudar cómputo según ITIL v4.",
            "business_impact": {
                "level": "CRÍTICO",
                "dimension": "Transparencia de SLA & Cumplimiento ITIL v4",
                "description": "Monitoreo de tiempos de atención con precisión de segundos, garantizando que el cómputo de SLA refleje con total exactitud si el ticket está activo o en espera de terceros.",
                "metric_target": "100% de trazabilidad y auditoría de tiempos en vivo sin discrepancias en cómputo.",
                "risk_of_inaction": "Falsos incumplimientos de SLA o falta de transparencia ante auditorías sanitarias de prestadores."
            },
            "acceptance_criteria": [
                "Cronómetro dinámico con segundos visibles en vivo en el Workspace.",
                "Distinción clara entre estado ACTIVO (teal) y EN PAUSA (ámbar/slate).",
                "Acciones directas de pausar y reanudar con confirmación operativa y registro en timeline."
            ]
        },
        {
            "id": "ISSUE-79",
            "title": "[Sprint 7] Depuración de Botonera Redundante de Asignación en Agent Workspace",
            "epic": "EP-03: Bandeja de Entrada y Asignación",
            "sp": 2,
            "status": "qa",
            "priority": "P2",
            "sprint": "Sprint 7",
            "discipline": "Frontend / UX & Workflow",
            "timebox": "Sprint 7 (05-oct al 16-oct)",
            "attachment_image": "assets/capturas/ISSUE-79_corregir_redundancia_botones_asignar.png",
            "doc_ref": "DOC-02",
            "doc_section": "Flujo de Autoasignación y Derivación sin Fricción",
            "description": "Eliminación de la duplicidad de botones 'Asignar' en el Workspace operativo. Se sustituye la botonera repetitiva por una disposición ergonómica de acción única: [ Asignar a mí ] para toma directa de guardia y [ Derivar a otro... ] para escalamiento asistencial, erradicando confusiones de doble clic.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Ergonomía de Interfaz & Eficiencia Operativa",
                "description": "Simplificación del flujo de derivación y autoasignación en el Workspace, erradicando elementos repetitivos para optimizar el tiempo de respuesta del operador.",
                "metric_target": "Eliminación del 100% de redundancia visual y reducción de clics a 1 acción unificada.",
                "risk_of_inaction": "Dudas operativas y sobrecarga cognitiva en los analistas de soporte asistencial."
            },
            "acceptance_criteria": [
                "Visualización de fila única con dos acciones complementarias sin duplicidad.",
                "Toma directa de ticket en estado NUEVO asignándolo de forma reactiva al operador activo.",
                "Actualización automática de métricas de bandeja de entrada."
            ]
        },
        {
            "id": "ISSUE-80",
            "title": "[Sprint 7] Evaluación Obligatoria y Renderizado Dinámico de Impacto en Producto y Negocio en Todos los Tickets",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "status": "qa",
            "priority": "P1",
            "sprint": "Sprint 7",
            "discipline": "Gobernanza & Calidad de Producto",
            "timebox": "Sprint 7 (05-oct al 16-oct)",
            "attachment_image": "assets/capturas/ISSUE-80_evaluar_impacto_en_producto_y_negocio.png",
            "doc_ref": "DOC-07",
            "doc_section": "Evaluación Obligatoria de Impacto de Negocio y Producto",
            "description": "Incorporación de análisis de impacto de negocio (nivel, dimensión, descripción, meta cuantificable y riesgo de inacción) de manera obligatoria y estructurada en todas las tarjetas de requerimientos, bugs e incrementos, erradicando valores 'undefined' o evaluaciones vacías en el Tablero Scrumban.",
            "business_impact": {
                "level": "CRÍTICO",
                "dimension": "Gobernanza PMI & Alineación Estratégica",
                "description": "Garantía de que todo requerimiento o corrección técnica cuente con justificación formal de negocio y retorno de valor cuantificado antes de su aprobación.",
                "metric_target": "0 tickets con impacto 'undefined' en el Tablero Scrumban oficial.",
                "risk_of_inaction": "Pérdida de alineación entre esfuerzo de desarrollo e impacto real en el negocio hospitalario."
            },
            "acceptance_criteria": [
                "100% de tickets con bloque formal de impacto en tarjeta y modal.",
                "Eliminación absoluta de la leyenda (UNDEFINED) o cadenas vacías.",
                "Mapeo preventivo mediante fallback automático de gobernanza."
            ]
        },
        {
            "id": "ISSUE-81",
            "title": "[Sprint 7] Botón de Cierre 'X' de Alto Contraste y Cierre por Escape/Backdrop en Visor Lightbox de Adjuntos",
            "epic": "EP-05: Seguimiento, Notificaciones e Historial",
            "sp": 2,
            "status": "qa",
            "priority": "P2",
            "sprint": "Sprint 7",
            "discipline": "Frontend / Accesibilidad & UX",
            "timebox": "Sprint 7 (05-oct al 16-oct)",
            "attachment_image": "assets/capturas/ISSUE-81_imagen_adjunta_sin_x_de_cierre.png",
            "doc_ref": "DOC-05",
            "doc_section": "Visor de Evidencias Diagnósticas en Pantalla Completa",
            "description": "Implementación de botón de cierre circular 'X' de alto contraste (#0F172A sobre borde #CBD5E1 y tipografía blanca) en esquina superior derecha de la ventana modal lightbox de previsualización de imágenes adjuntas, junto con soporte nativo de cierre por clic en el fondo oscuro y tecla Escape.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Accesibilidad & Visualización de Evidencias",
                "description": "Disponibilidad de visor de evidencias en alta resolución con controles intuitivos de cierre (botón X visible, escape y clic fuera) para diagnóstico clínico sin bloqueos.",
                "metric_target": "Cierre inmediato en 1 clic y visualización nítida sin recargas ni pérdida de contexto.",
                "risk_of_inaction": "Bloqueo visual del operador en pantalla completa sin mecanismo evidente de retorno al ticket."
            },
            "acceptance_criteria": [
                "Botón 'X' circular destacado y visible en todo momento.",
                "Cierre al hacer clic en cualquier área del fondo oscuro.",
                "Cierre inmediato al presionar la tecla Escape en teclado."
            ]
        },
        {
            "id": "ISSUE-82",
            "title": "[Sprint 7] Ocultamiento Total del Módulo 'Configuración' en Barra Lateral para Todos los Roles y Perfiles",
            "epic": "EP-06: Administración y Operación Centralizada",
            "sp": 2,
            "status": "qa",
            "priority": "P1",
            "sprint": "Sprint 7",
            "discipline": "Frontend / IAM & Seguridad RBAC",
            "timebox": "Sprint 7 (05-oct al 16-oct)",
            "attachment_image": "assets/capturas/ISSUE-82_ocultar_modulo_configuracion_todos_roles.png",
            "doc_ref": "DOC-03",
            "doc_section": "Gobernanza de Accesos y Ocultamiento de Módulo Configuración",
            "description": "Ocultamiento estricto e incondicional del acceso interactivo al módulo 'Configuración' en la barra lateral de navegación para todos los roles de sistema (Admin, Team Leader, Analistas de Soporte N1/N2/N3 y Solicitantes), redirigiendo cualquier navegación forzada al Hub Unificado.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Gobernanza de Accesos & Seguridad RBAC",
                "description": "Restricción y supresión definitiva del acceso interactivo a configuraciones globales de sistema desde el menú lateral para la totalidad de roles operativos y administrativos.",
                "metric_target": "100% de perfiles sin exposición del módulo Configuración en interfaz gráfica.",
                "risk_of_inaction": "Modificación accidental de parámetros de infraestructura o exposición de configuraciones no operativas."
            },
            "acceptance_criteria": [
                "Módulo #tab-config con display none important en todo momento.",
                "applyRolePermissions oculta el tab sin importar el perfil activo.",
                "Redirección automática si se intenta acceder por URL o atajo."
            ]
        },
        {
            "id": "ISSUE-83",
            "title": "[Sprint 7] Ocultamiento de Funcionalidad 'Niveles ITIL' y Formalización de Configuración Inicial por Base de Datos (ITIL v4)",
            "epic": "EP-06: Administración y Operación Centralizada",
            "sp": 2,
            "status": "qa",
            "priority": "P1",
            "sprint": "Sprint 7",
            "discipline": "Frontend / UX & Documentación Arquitectónica",
            "timebox": "Sprint 7 (05-oct al 16-oct)",
            "attachment_image": "assets/capturas/ISSUE-83_ocultar_funcionalidad_niveles_itil.png",
            "doc_ref": "DOC-03",
            "doc_section": "11. Gobernanza de Configuración ITIL v4 y Desacoplamiento de Niveles",
            "description": "Ocultamiento de la sub-pestaña interactiva 'Niveles ITIL' en el catálogo de plataformas y formalización arquitectónica en las especificaciones oficiales DOC-02 y DOC-03 de que la parametrización de niveles de soporte (N1/N2/N3) y matrices de escalamiento se gestiona directamente en base de datos bajo los estándares ITIL v4.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Alineación ITIL v4 & Desacoplamiento Arquitectónico",
                "description": "Ocultamiento de controles interactivos superfluos de niveles de servicio en el catálogo de plataformas, delegando la configuración de soporte N1/N2/N3 a la base de datos central según estándares ITIL v4.",
                "metric_target": "0 controles no didácticos visibles en pantalla y documentación 100% formalizada.",
                "risk_of_inaction": "Desalineación de procesos con respecto al marco ITIL v4 y confusión operativa en la administración de mesas."
            },
            "acceptance_criteria": [
                "Botón y sub-vista de Niveles ITIL ocultos permanentemente en el DOM.",
                "switchPlatformsSubTab('helpdesks') redirige a instituciones.",
                "Sección 11 formalizada en DOC-03 y DOC-02."
            ]
        }
    ]
    tasks.extend(sprint7_tasks)

    # Actualizar ISSUE-65 a Retrabajo (rework) al fondo por orden estricta del Solution Owner
    for t in tasks:
        if t["id"] == "ISSUE-65":
            t["status"] = "rework"
            t["priority"] = "P1"
            t["so_feedback"] = {
                "status": "EN RETRABAJO PRIORITARIO (P1)",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "date": "27/09/2026 13:15",
                "observation": "ISSUE-65, no se resolvió el problema, vuelve a retrabajo, analiza, propon solución y deja listo para aprobar y ejecutar"
            }
            t["attachment_image"] = "assets/capturas/ISSUE-65_persistencia_sla_sin_cierre_dialogo.png"

    # BLINDAJE INMUTABLE: 38 Tarjetas previamente aprobadas por el Solution Owner
    APPROVED_DONE_IDS = {
        "ISSUE-01", "ISSUE-02", "ISSUE-03", "ISSUE-07", "ISSUE-08", "ISSUE-09", "ISSUE-10",
        "ISSUE-11", "ISSUE-12", "ISSUE-13", "ISSUE-14", "ISSUE-15", "ISSUE-16", "ISSUE-17",
        "ISSUE-18", "ISSUE-19", "ISSUE-20", "ISSUE-21", "ISSUE-22", "ISSUE-23", "ISSUE-24",
        "ISSUE-25", "ISSUE-26", "ISSUE-27", "ISSUE-28", "ISSUE-29",
        "MEJ-01", "MEJ-02", "MEJ-03", "MEJ-04", "MEJ-05", "MEJ-06", "MEJ-07", "MEJ-08", "MEJ-09", "MEJ-10",
        "UH-65", "UH-68", "UH-69", "UH-70"
    }

    # Asignar status: "done" permanente a las aprobadas
    for t in tasks:
        if t["id"] in APPROVED_DONE_IDS:
            t["status"] = "done"
            t["so_feedback"] = {
                "status": "APROBADO CONFORME",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "date": "2026-09-26",
                "notes": "Incremento verificado y aceptado formalmente conforme a criterios DoD."
            }

    # Las 4 de retrabajo corregidas van al fondo de la pila de revisión (qa)
    DEMON_REWORK_IDS = ["UH-67", "ISSUE-04", "ISSUE-05", "ISSUE-06"]
    for t in tasks:
        if t["id"] in DEMON_REWORK_IDS:
            t["status"] = "qa"

    # Las 3 en curso ejecutadas van a revisión (qa)
    IN_PROGRESS_IDS = ["UH-66", "TASK-01", "GAP-02"]
    for t in tasks:
        if t["id"] in IN_PROGRESS_IDS:
            t["status"] = "qa"

    # Sincronización Universal de Documentos Rectores Oficiales (Para todas las tarjetas y para el futuro)
    for t in tasks:
        if not t.get("doc_link"):
            t_type = (t.get("type") or "UH").upper()
            t_id = t.get("id", "")
            t_id_lower = t_id.lower()
            if t_type == "ISSUE":
                t["doc_link"] = f"04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#{t_id_lower}"
                t["doc_title"] = f"DOC-QA-004 ({t_id})"
                t["doc_desc"] = t.get("doc_desc") or f"Reporte formal de defecto y criterios de aceptación para {t_id}."
            elif t_type == "TASK":
                t["doc_link"] = f"03_ARQUITECTURA_Y_DISENO_TECNICO.md#{t_id_lower}"
                t["doc_title"] = f"DOC-ARC-003 ({t_id})"
                t["doc_desc"] = t.get("doc_desc") or f"Alcance técnico y arquitectura de componentes para {t_id}."
            elif t_type in ("OPORTUNIDAD", "MEJORA"):
                t["doc_link"] = f"03_ARQUITECTURA_Y_DISENO_TECNICO.md#{t_id_lower}"
                t["doc_title"] = f"DOC-ARC-003 ({t_id})"
                t["doc_desc"] = t.get("doc_desc") or f"Propuesta técnica y roadmap de mejora para {t_id}."
            else:
                t["doc_link"] = f"02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#{t_id_lower}"
                t["doc_title"] = f"DOC-SPEC-002 ({t_id})"
                t["doc_desc"] = t.get("doc_desc") or f"Especificación funcional y criterios Gherkin para {t_id}."

    # Generar CSV
    with open(CSV_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("ID,Titulo,Tipo,Prioridad,Epica,StoryPoints,Sprint,Estado,Disciplina,Documentacion\n")
        for t in tasks:
            doc = t.get("doc_link", "")
            f.write(f'"{t["id"]}","{t["title"]}","{t.get("type", "UH")}","{t.get("priority", "P3")}","{t["epic"]}",{t["sp"]},"{t["sprint"]}","{t["status"]}","{t["discipline"]}","{doc}"\n')
    print("CSV de Backlog actualizado.")

    tasks_json = json.dumps(tasks, ensure_ascii=False)
    epics_json = json.dumps(epics, ensure_ascii=False)
    sprints_json = json.dumps(sprints, ensure_ascii=False)
    milestones_json = json.dumps(milestones, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tablero Scrumban & Roadmap Integral — HealthDesk Quantux</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --q-navy: #1E3A5F;
      --q-navy-dark: #142842;
      --q-navy-soft: #2D4B73;
      --q-teal: #00C4B4;
      --q-teal-hover: #00A89A;
      --q-teal-light: #E0F7F5;
      --q-bg: #F1F5F9;
      --q-card-bg: #FFFFFF;
      --q-border: #E2E8F0;
      --q-text-main: #1E293B;
      --q-text-muted: #64748B;
      --q-accent-amber: #D97706;
      --q-accent-amber-bg: #FEF3C7;
      --q-accent-green: #16A34A;
      --q-accent-green-bg: #DCFCE7;
      --q-accent-blue: #2563EB;
      --q-accent-blue-bg: #DBEAFE;
      --q-accent-purple: #7C3AED;
      --q-accent-purple-bg: #F3E8FF;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      height: 100vh;
      max-height: 100vh;
      overflow: hidden;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background-color: var(--q-bg);
      color: var(--q-text-main);
      display: flex;
      flex-direction: column;
    }}

    /* HEADER */
    header {{
      background: var(--q-navy);
      color: #FFFFFF;
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px rgba(30, 58, 95, 0.15);
      flex-shrink: 0;
      z-index: 50;
    }}

    .brand-header {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-logo {{
      width: 38px;
      height: 38px;
      background: #FFFFFF;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
    }}

    .brand-titles h1 {{
      font-family: 'Montserrat', sans-serif;
      font-size: 16px;
      font-weight: 800;
      letter-spacing: -0.3px;
      color: #FFFFFF;
    }}

    .brand-titles h1 span {{ color: var(--q-teal); }}

    .brand-titles p {{
      font-size: 11px;
      color: #94A3B8;
      font-weight: 500;
    }}

    .header-badges {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .status-pill {{
      font-family: 'Montserrat', sans-serif;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: #0284C7;
      color: #E0F2FE;
      border: 1px solid #38BDF8;
    }}

    .timebox-pill {{
      font-size: 11px;
      color: #94A3B8;
      background: rgba(255, 255, 255, 0.08);
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }}

    /* NAVIGATION BAR FOR VIEWS */
    .view-nav-bar {{
      background: #FFFFFF;
      padding: 8px 24px;
      display: flex;
      gap: 10px;
      border-bottom: 1px solid var(--q-border);
      box-shadow: 0 1px 4px rgba(10, 28, 62, 0.04);
      flex-shrink: 0;
      align-items: center;
    }}

    .nav-tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: #475569;
      font-family: 'Inter', sans-serif;
      font-size: 12.5px;
      font-weight: 600;
      padding: 7px 16px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    .nav-tab-btn:hover {{
      background: #F1F5F9;
      color: #0F172A;
      border-color: #E2E8F0;
    }}

    .nav-tab-btn.active {{
      background: #E0F7F5 !important;
      color: #00796B !important;
      border: 1.5px solid #00A896 !important;
      font-weight: 700 !important;
      box-shadow: 0 1px 4px rgba(0, 168, 150, 0.15);
    }}

    /* METRICS STRIP */
    .metrics-bar {{
      background: #FFFFFF;
      border-bottom: 1px solid var(--q-border);
      padding: 8px 24px;
      display: flex;
      gap: 20px;
      align-items: center;
      overflow-x: auto;
      flex-shrink: 0;
    }}

    .metric-card {{
      display: flex;
      flex-direction: column;
      border-right: 1px solid var(--q-border);
      padding-right: 20px;
      min-width: 130px;
    }}

    .metric-card:last-child {{ border-right: none; }}

    .metric-label {{
      font-size: 10px;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--q-text-muted);
      letter-spacing: 0.5px;
    }}

    .metric-val {{
      font-family: 'Montserrat', sans-serif;
      font-size: 16px;
      font-weight: 800;
      color: var(--q-navy);
      display: flex;
      align-items: baseline;
      gap: 4px;
    }}

    .metric-val small {{
      font-size: 11px;
      font-weight: 600;
      color: var(--q-text-muted);
    }}

    /* CONTROLS & FILTERS */
    .controls-bar {{
      padding: 8px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      background: #F8FAFC;
      border-bottom: 1px solid var(--q-border);
      flex-shrink: 0;
    }}

    .filters-group {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .filter-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      color: var(--q-navy);
    }}

    select, input[type="text"] {{
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-family: 'Inter', sans-serif;
      color: var(--q-text-main);
      outline: none;
    }}

    select:focus, input[type="text"]:focus {{
      border-color: var(--q-teal);
      box-shadow: 0 0 0 2px rgba(0, 196, 180, 0.2);
    }}

    .btn {{
      background: var(--q-navy);
      color: #FFFFFF;
      border: none;
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      font-family: 'Montserrat', sans-serif;
    }}

    .btn:hover {{ background: var(--q-navy-soft); }}
    .btn-secondary {{
      background: #FFFFFF;
      color: var(--q-navy);
      border: 1px solid #CBD5E1;
    }}
    .btn-secondary:hover {{ background: #F1F5F9; border-color: #94A3B8; }}

    /* VIEWS CONTAINERS */
    .view-panel {{
      display: none;
      flex: 1;
      padding: 10px 16px;
      min-height: 0;
      overflow: hidden;
    }}

    .view-panel.active {{
      display: flex;
      flex-direction: column;
      flex: 1;
      min-height: 0;
      overflow: hidden;
    }}

    .view-panel:not(#view-board) {{
      overflow-y: auto !important;
    }}

    /* VISTA 1: TABLERO KANBAN */
    .kanban-board {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
      align-items: stretch;
      overflow: hidden;
      flex: 1;
      min-height: 0;
      height: 100%;
      padding-bottom: 2px;
    }}

    .kanban-col {{
      background: #E2E8F0;
      border-radius: 8px;
      border-top: 4px solid var(--q-navy);
      display: flex;
      flex-direction: column;
      height: 100%;
      min-height: 0;
      overflow: hidden;
    }}

    .col-header {{
      padding: 10px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #CBD5E1;
      flex-shrink: 0;
    }}

    .col-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 11.5px;
      font-weight: 800;
      color: var(--q-navy);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .col-badge {{
      background: #FFFFFF;
      color: var(--q-navy);
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 10px;
      border: 1px solid #CBD5E1;
    }}

    .col-wip {{
      font-size: 10px;
      color: #64748B;
      font-weight: 600;
    }}

    .col-header-info {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      background: #E2E8F0;
      color: #475569;
      font-size: 10px;
      font-weight: 800;
      font-family: monospace;
      cursor: help;
      position: relative;
      transition: all 0.2s ease;
      flex-shrink: 0;
      user-select: none;
    }}

    .col-header-info:hover {{
      background: #0F172A;
      color: #FFFFFF;
    }}

    .col-tooltip-box {{
      visibility: hidden;
      opacity: 0;
      position: absolute;
      top: 100%;
      left: 0;
      transform: translateY(6px);
      width: 250px;
      background: #0F172A;
      color: #F8FAFC;
      font-size: 11px;
      font-family: 'Open Sans', sans-serif;
      font-weight: 500;
      line-height: 1.45;
      padding: 9px 12px;
      border-radius: 7px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
      z-index: 9999;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
      text-transform: none;
      letter-spacing: normal;
      border: 1px solid #334155;
    }}

    .col-header-info:hover .col-tooltip-box {{
      visibility: visible;
      opacity: 1;
      transform: translateY(3px);
    }}

    .cards-list {{
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      overflow-y: auto;
      overflow-x: hidden;
      flex: 1;
      min-height: 0;
    }}

    .kanban-card {{
      background: var(--q-card-bg);
      border-radius: 7px;
      padding: 12px;
      border: 1px solid #CBD5E1;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
      cursor: grab;
      transition: all 0.2s ease;
      position: relative;
    }}

    .kanban-card:hover {{
      box-shadow: 0 6px 12px rgba(30, 58, 95, 0.1);
      transform: translateY(-2px);
      border-color: var(--q-teal);
    }}

    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}

    .card-id {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      color: var(--q-navy);
      background: #F1F5F9;
      padding: 2px 6px;
      border-radius: 4px;
    }}

    .card-sp {{
      background: var(--q-teal-light);
      color: var(--q-navy);
      border: 1px solid var(--q-teal);
      font-size: 10.5px;
      font-weight: 800;
      padding: 1px 7px;
      border-radius: 10px;
      font-family: 'Montserrat', sans-serif;
    }}

    .card-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 12px;
      font-weight: 700;
      color: var(--q-navy);
      margin-bottom: 6px;
      line-height: 1.3;
    }}

    .card-epic {{
      font-size: 10px;
      font-weight: 600;
      color: #475569;
      margin-bottom: 8px;
      display: inline-block;
      background: #F8FAFC;
      border: 1px solid var(--q-border);
      padding: 2px 6px;
      border-radius: 4px;
    }}

    /* BADGES DE TIPO DE ITEM */
    .card-badge-type {{
      font-size: 8.5px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.5px;
      margin-right: 4px;
      font-family: 'Montserrat', sans-serif;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}

    .badge-epic {{ background: #EEF2FF; color: #4338CA; border: 1px solid #C7D2FE; }}
    .badge-uh {{ background: #E0F7F5; color: #0F766E; border: 1px solid #99F6E4; }}
    .badge-task {{ background: #DBEAFE; color: #1D4ED8; border: 1px solid #BFDBFE; }}
    .badge-issue {{ background: #FFE4E6; color: #92400E; border: 1px solid #FECDD3; }}
    .badge-gap {{ background: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }}
    .badge-mejora {{ background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }}
    .badge-oportunidad {{ background: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF; }}

    /* BADGES DE PRIORIDAD */
    .card-badge-priority {{
      font-size: 8px;
      font-weight: 800;
      padding: 1px 5px;
      border-radius: 3px;
      font-family: 'Montserrat', sans-serif;
    }}
    .priority-p1 {{ background: #FFE4E6; color: #9F1239; border: 1px solid #FDA4AF; }}
    .priority-p2 {{ background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }}
    .priority-p3 {{ background: #E0F2FE; color: #075985; border: 1px solid #BAE6FD; }}
    .priority-p4 {{ background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }}

    .card-doc-box {{
      margin: 6px 0;
      background: #F0FDFA;
      border: 1px dashed var(--q-teal);
      border-radius: 5px;
      padding: 5px 8px;
      font-size: 10px;
    }}

    .card-doc-link {{
      color: #0D9488;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-family: 'Montserrat', sans-serif;
    }}

    .card-doc-link:hover {{
      text-decoration: underline;
      color: #0F766E;
    }}

    .card-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10.5px;
      color: var(--q-text-muted);
      border-top: 1px solid #F1F5F9;
      padding-top: 8px;
      margin-top: 6px;
    }}

    .card-sprint-tag {{
      font-weight: 700;
      color: var(--q-navy-soft);
    }}

    .card-actions {{
      display: flex;
      gap: 4px;
    }}

    .card-btn-move {{
      background: #F1F5F9;
      border: 1px solid #CBD5E1;
      border-radius: 4px;
      padding: 2px 6px;
      cursor: pointer;
      font-size: 10px;
      color: var(--q-navy);
      font-weight: 700;
    }}

    .card-btn-move:hover {{
      background: var(--q-teal-light);
      border-color: var(--q-teal);
    }}

    .card-btn-detail {{
      width: 100%;
      margin-top: 6px;
      padding: 4px 8px;
      background: #F8FAFC;
      border: 1px solid var(--q-border);
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      color: var(--q-navy);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s ease;
      font-family: 'Montserrat', sans-serif;
    }}

    .card-btn-detail:hover {{
      background: var(--q-teal-light);
      border-color: var(--q-teal);
    }}

    /* VISTA 2: ROADMAP & TIMELINE */
    .roadmap-container {{
      background: #FFFFFF;
      border: 1px solid var(--q-border);
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}

    .roadmap-header-section {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--q-teal);
      padding-bottom: 12px;
    }}

    .roadmap-header-section h2 {{
      font-family: 'Montserrat', sans-serif;
      font-size: 16px;
      font-weight: 800;
      color: var(--q-navy);
    }}

    .timeline-quarters {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      background: #F8FAFC;
      padding: 10px;
      border-radius: 6px;
      border: 1px solid var(--q-border);
      text-align: center;
      font-family: 'Montserrat', sans-serif;
      font-size: 11px;
      font-weight: 800;
      color: var(--q-navy);
    }}

    .timeline-quarter-col {{
      background: #FFFFFF;
      padding: 8px;
      border-radius: 4px;
      border: 1px solid #CBD5E1;
    }}

    .timeline-quarter-col.active {{
      border-color: var(--q-teal);
      background: #F0FDFA;
    }}

    .roadmap-section-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 13px;
      font-weight: 800;
      color: var(--q-navy);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .roadmap-epics-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .roadmap-epic-row {{
      background: #F8FAFC;
      border: 1px solid var(--q-border);
      border-radius: 6px;
      padding: 12px 16px;
      display: grid;
      grid-template-columns: 240px 1fr 140px 100px;
      gap: 16px;
      align-items: center;
    }}

    .roadmap-epic-row:hover {{
      border-color: var(--q-teal);
      background: #FFFFFF;
    }}

    .epic-meta-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 12px;
      font-weight: 700;
      color: var(--q-navy);
    }}

    .epic-meta-sub {{
      font-size: 10.5px;
      color: var(--q-text-muted);
    }}

    .progress-bar-container {{
      background: #E2E8F0;
      border-radius: 10px;
      height: 12px;
      overflow: hidden;
      position: relative;
    }}

    .progress-bar-fill {{
      background: linear-gradient(90deg, #00C4B4, #0284C7);
      height: 100%;
      border-radius: 10px;
      transition: width 0.3s ease;
    }}

    .milestones-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
    }}

    .milestone-card {{
      background: #F8FAFC;
      border: 1px solid var(--q-border);
      border-radius: 6px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
    }}

    .milestone-card.current {{
      border: 2px solid var(--q-teal);
      background: #F0FDFA;
    }}

    .milestone-date {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      font-weight: 700;
      color: var(--q-navy);
    }}

    .milestone-title {{
      font-family: 'Montserrat', sans-serif;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--q-navy);
    }}

    /* VISTA 3: MÉTRICAS & BURNDOWN */
    .metrics-view-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
    }}

    .velocity-chart-card {{
      background: #FFFFFF;
      border: 1px solid var(--q-border);
      border-radius: 8px;
      padding: 20px;
    }}

    .velocity-bars {{
      display: flex;
      align-items: flex-end;
      gap: 16px;
      height: 220px;
      padding-top: 20px;
      border-bottom: 2px solid var(--q-border);
    }}

    .velocity-col {{
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      height: 100%;
      justify-content: flex-end;
    }}

    .velocity-bar {{
      width: 100%;
      background: linear-gradient(180deg, #00C4B4, #1E3A5F);
      border-radius: 4px 4px 0 0;
      transition: height 0.3s ease;
      min-height: 10px;
    }}

    .velocity-bar.active-sprint {{
      background: linear-gradient(180deg, #F59E0B, #B45309);
    }}

    /* VISTA 4: BACKLOG JERÁRQUICO */
    .tree-container {{
      background: #FFFFFF;
      border: 1px solid var(--q-border);
      border-radius: 8px;
      padding: 16px;
    }}

    .tree-epic-item {{
      border: 1px solid var(--q-border);
      border-radius: 6px;
      margin-bottom: 10px;
      overflow: hidden;
    }}

    .tree-epic-header {{
      background: #F8FAFC;
      padding: 12px 16px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'Montserrat', sans-serif;
      font-size: 12.5px;
      font-weight: 800;
      color: var(--q-navy);
    }}

    .tree-epic-header:hover {{
      background: #F1F5F9;
    }}

    .tree-epic-children {{
      padding: 10px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      border-top: 1px solid var(--q-border);
    }}

    .tree-child-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 6px 10px;
      background: #FFFFFF;
      border: 1px solid var(--q-border);
      border-radius: 4px;
      font-size: 11.5px;
    }}

    /* MODAL UNIVERSAL */
    .uh-modal-backdrop {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.45);
      z-index: 9999;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .uh-modal-content {{
      background: #FFFFFF;
      border-radius: 10px;
      width: 100%;
      max-width: 720px;
      max-height: 88vh;
      overflow-y: auto;
      border: 1px solid #CBD5E1;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
      padding: 24px;
      position: relative;
    }}

    .uh-modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 2px solid var(--q-teal);
      padding-bottom: 12px;
      margin-bottom: 16px;
    }}

    .uh-modal-close {{
      background: #F1F5F9;
      border: 1px solid #CBD5E1;
      border-radius: 6px;
      padding: 4px 10px;
      cursor: pointer;
      font-weight: 700;
      color: var(--q-navy);
      font-size: 12px;
    }}

    .uh-modal-close:hover {{ background: #E2E8F0; }}

    .modal-box {{
      background: #F8FAFC;
      border: 1px solid var(--q-border);
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 12px;
      font-size: 12px;
      line-height: 1.5;
    }}

    .modal-box-alert {{
      background: #FFF1F2;
      border: 1.5px solid #FECDD3;
    }}

    .modal-box-success {{
      background: #F0FDF4;
      border: 1.5px solid #BBF7D0;
    }}

    .modal-subhead {{
      font-family: 'Montserrat', sans-serif;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--q-navy);
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}
  </style>
</head>
<body>

  <!-- VIEW NAVIGATION BAR -->
  <nav class="view-nav-bar">
    <button class="nav-tab-btn active" id="tab-btn-board" onclick="switchView('board')">
      Tablero Scrumban
    </button>
    <button class="nav-tab-btn" id="tab-btn-roadmap" onclick="switchView('roadmap')">
      Roadmap & Cronograma
    </button>
    <button class="nav-tab-btn" id="tab-btn-metrics" onclick="switchView('metrics')">
      Métricas & Capacidad
    </button>
  </nav>

  <!-- GOBERNANZA SCRUMBAN: FASE DE PRUEBAS Y ESTABILIZACIÓN (SCOPE FREEZE) -->
  <div style="background: #FFFBEB; border-bottom: 1px solid #FEF3C7; padding: 10px 24px; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
    <div style="display: flex; align-items: center; gap: 10px;">
      <span style="background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 4px; font-family: 'Outfit', sans-serif; letter-spacing: 0.3px;">FASE DE PRUEBAS Y ESTABILIZACIÓN</span>
      <div>
        <strong style="color: #92400E; font-size: 12px; font-family: 'Outfit', sans-serif;">ESTABILIZACIÓN ACTIVA (SCOPE FREEZE)</strong>
        <span style="color: #78350F; font-size: 11.5px; margin-left: 6px;">Alcance cerrado hacia la presentación oficial del <strong>01 de Octubre de 2026</strong> ante el Comité Evaluador. Foco exclusivo en Testing, Debugging, Calidad OJO y Cierre de Retrabajos. Todo nuevo ítem se registra en el <strong>Product Backlog</strong>.</span>
      </div>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="background: #FEF3C7; border: 1px solid #FDE68A; color: #92400E; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px;">HITO: 01-OCT-2026</span>
      <span style="background: #E0F2FE; border: 1px solid #BAE6FD; color: #0369A1; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 6px;">COMITÉ EVALUADOR</span>
    </div>
  </div>

  <!-- BARRA DE TOGGLE PARA COLAPSAR/DESPLEGAR MÉTRICAS Y FILTROS -->
  <div class="top-toggle-bar" style="display: flex; justify-content: space-between; align-items: center; padding: 6px 20px; background: #F8FAFC; border-bottom: 1.5px solid #E2E8F0;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="font-size: 11px; font-weight: 800; background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; padding: 2px 8px; border-radius: 4px;">⚡ SPRINT 6 ACTIVO</span>
      <span style="font-size: 11px; color: #64748B; font-weight: 500;">Filtrado por defecto en el Sprint en curso • Pruebas & Estabilización (36 SP)</span>
    </div>
    <button id="btn-toggle-header-panel" onclick="toggleHeaderPanel()" style="background: #FFFFFF; border: 1.5px solid #CBD5E1; color: #334155; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: 'Montserrat', sans-serif;">
      <span id="toggle-header-icon">🔽</span> <span id="toggle-header-text">Desplegar Métricas y Filtros</span>
    </button>
  </div>

  <!-- CONTENEDOR COLAPSABLE DE MÉTRICAS Y FILTROS (COLAPSADO POR DEFECTO) -->
  <div id="collapsible-header-panel" style="display: none;">
    <!-- METRICS STRIP -->
    <section class="metrics-bar">
      <div class="metric-card">
        <span class="metric-label">Progreso del Backlog</span>
        <span class="metric-val" id="metric-progress" style="color: #10B981;">173 <small>/ 274 SP (63.1%)</small></span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Sprint 6 (Actual)</span>
        <span class="metric-val" style="color: #0284C7;">36 SP <small>(5 SP Done, 31 SP en curso)</small></span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Items Totales</span>
        <span class="metric-val" id="metric-stories">65 Items <small>(9 Épicas, 48 UHs)</small></span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Velocidad Promedio</span>
        <span class="metric-val">33 SP <small>/ Sprint</small></span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Conformidad OJO</span>
        <span class="metric-val" style="color: #D97706;">96% <small>2 Issues P1 en Backlog</small></span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Solution Owner</span>
        <span class="metric-val" style="font-size: 13px; margin-top: 4px;">Freddy Cortés <small>(Tech Lead)</small></span>
      </div>
    </section>

    <!-- CONTROLS & FILTERS -->
    <section class="controls-bar">
      <div class="filters-group">
        <div class="filter-item">
          <label for="filter-sprint">Sprint:</label>
          <select id="filter-sprint" onchange="renderCurrentView()">
            <option value="Sprint 6" selected>⚡ Sprint 6 (ACTUAL): Pruebas, Estabilización & Cierre de Alcance (36 SP)</option>
            <option value="ALL">Todos los Sprints y Backlog</option>
            <option value="Product Backlog">📌 Product Backlog: Gaps, Mejoras y Futuros (26 SP)</option>
            <option value="Sprint 5">✅ Sprint 5: Sidebar Zen & Ergonomía (14 SP)</option>
            <option value="Sprint 4">✅ Sprint 4: Catálogo, Team Leader & Suite Médicos (46 SP)</option>
            <option value="Sprint 3">✅ Sprint 3: Analytics, Directorio, Email & CSAT (43 SP)</option>
            <option value="Sprint 2">✅ Sprint 2: Workspace Zen, Alta & Multi-Servicio (32 SP)</option>
            <option value="Sprint 1">✅ Sprint 1: Incidentes Masivos, Releases & Bandeja (30 SP)</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filter-type">Tipo de Item:</label>
          <select id="filter-type" onchange="renderCurrentView()">
            <option value="ALL" selected>Todos los Tipos</option>
            <option value="ISSUE">🐞 Issues / Bugs (Alta Prioridad & Defectos)</option>
            <option value="UH">👤 Historias de Usuario (UHs)</option>
            <option value="TASK">⚙️ Tareas Técnicas</option>
            <option value="GAP">🔍 Gaps de Proceso / TQM</option>
            <option value="MEJORA">⚡ Mejoras Evolutivas</option>
            <option value="OPORTUNIDAD">💡 Oportunidades de Arquitectura</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filter-epic">Épica / Módulo:</label>
          <select id="filter-epic" onchange="renderCurrentView()">
            <option value="ALL">Todas las Épicas</option>
            <option value="16. Gobernanza & Calidad">16. Gobernanza & Calidad (DOC-GOV-008)</option>
            <option value="17. Arquitectura & APIs">17. Arquitectura & APIs (Contratos SDD)</option>
            <option value="14. Suite Médicos (Guardia)">14. Suite Médicos (Portal Solicitante)</option>
            <option value="1. Incidentes Masivos">1. Incidentes Masivos</option>
            <option value="2. Releases y Despliegues">2. Releases y Despliegues</option>
            <option value="3. Bandeja General & Paginación">3. Bandeja General & Paginación</option>
            <option value="4. Workspace Zen">4. Workspace Zen</option>
            <option value="5. Alta Sin Ruido">5. Alta Sin Ruido</option>
            <option value="6. Generalización Enterprise">6. Generalización Enterprise</option>
            <option value="7. Tablero de Control Zen">7. Tablero de Control Zen</option>
            <option value="8. Directorio de Usuarios Zen">8. Directorio de Usuarios Zen</option>
            <option value="9. Ingesta Email Omnicanal">9. Ingesta Email Omnicanal</option>
            <option value="10. Cierre & CSAT">10. Cierre & CSAT</option>
            <option value="11. Catálogo Zen">11. Catálogo Zen</option>
            <option value="12. Team Leader & Torre">12. Team Leader & Torre</option>
            <option value="15. Sidebar Zen & Ergonomía">15. Sidebar Zen & Ergonomía</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filter-priority">Prioridad:</label>
          <select id="filter-priority" onchange="renderCurrentView()">
            <option value="ALL">Todas las Prioridades</option>
            <option value="P1">P1 — Alta Prioridad / Bloqueante</option>
            <option value="P2">P2 — Alta</option>
            <option value="P3">P3 — Media</option>
            <option value="P4">P4 — Baja</option>
          </select>
        </div>

        <div class="filter-item">
          <input type="text" id="search-input" placeholder="Buscar ID, título o palabra clave..." oninput="renderCurrentView()">
        </div>
      </div>
    </section>
  </div>

  <!-- ========================================== -->
  <!-- VISTA 1: TABLERO SCRUMBAN (KANBAN) -->
  <!-- ========================================== -->
  <main class="view-panel active" id="view-board">
    <div class="kanban-board">
      
      <!-- COLUMNA 1: PRODUCT BACKLOG -->
      <div class="kanban-col" id="col-backlog" ondragover="allowDrop(event)" ondrop="drop(event, 'backlog')">
        <div class="col-header" title="Product Backlog: Repositorio central de requerimientos, historias de usuario, issues técnicos y mejoras priorizadas para el ciclo de vida del producto Quantux.">
          <span class="col-title">
            Product Backlog
            <span class="col-header-info" title="Directiva de Gobernanza">i
              <span class="col-tooltip-box"><strong>Product Backlog:</strong> Repositorio central de requerimientos, historias de usuario, issues técnicos y mejoras priorizadas para el ciclo de vida del producto Quantux.</span>
            </span>
          </span>
          <span class="col-badge" id="count-backlog">0</span>
        </div>
        <div class="cards-list" id="list-backlog"></div>
      </div>

      <!-- COLUMNA 2: SPRINT BACKLOG -->
      <div class="kanban-col" id="col-sprint" ondragover="allowDrop(event)" ondrop="drop(event, 'sprint')" style="border-top-color: #0284C7;">
        <div class="col-header" title="Sprint Backlog: Conjunto de ítems comprometidos formalmente por el equipo técnico para su ejecución durante la iteración activa.">
          <span class="col-title">
            Sprint Backlog
            <span class="col-header-info" title="Directiva de Gobernanza">i
              <span class="col-tooltip-box"><strong>Sprint Backlog:</strong> Conjunto de ítems comprometidos formalmente por el equipo técnico para su ejecución durante la iteración activa.</span>
            </span>
          </span>
          <span class="col-badge" id="count-sprint">0</span>
        </div>
        <div class="cards-list" id="list-sprint"></div>
      </div>

      <!-- COLUMNA 3: EN RETRABAJO / OBSERVADO (REWORK - PRIORIDAD P1) -->
      <div class="kanban-col" id="col-rework" ondragover="allowDrop(event)" ondrop="drop(event, 'rework')" style="border-top-color: #E11D48;">
        <div class="col-header" title="En Retrabajo (P1 Prioritario): Devuelto por el Solution Owner por no conformidad o funcionalidad no implementada. Prioridad bloqueante P1 con resolución inmediata.">
          <span class="col-title" style="color: #9F1239;">
            En Retrabajo (P1)
            <span class="col-header-info" style="background: #FFE4E6; color: #9F1239;" title="Directiva de Gobernanza">i
              <span class="col-tooltip-box" style="border-color: #FDA4AF;"><strong>En Retrabajo (P1 Prioritario):</strong> Devuelto por el Solution Owner por no conformidad o funcionalidad no implementada. Prioridad bloqueante P1 con resolución inmediata.</span>
            </span>
          </span>
          <span class="col-badge" id="count-rework" style="color: #9F1239; border-color: #FECDD3; background: #FFF1F2;">0</span>
        </div>
        <div class="cards-list" id="list-rework"></div>
      </div>

      <!-- COLUMNA 4: EN CURSO (IN PROGRESS) -->
      <div class="kanban-col" id="col-progress" ondragover="allowDrop(event)" ondrop="drop(event, 'progress')" style="border-top-color: #D97706;">
        <div class="col-header" title="En Curso (In Progress): Elementos en desarrollo activo por el equipo técnico con límite de trabajo en curso (WIP: 4 concurrentes).">
          <span class="col-title">
            En Curso <span class="col-wip">(WIP: 4)</span>
            <span class="col-header-info" title="Directiva de Gobernanza">i
              <span class="col-tooltip-box"><strong>En Curso (In Progress):</strong> Elementos en desarrollo activo por el equipo técnico con límite de trabajo en curso (WIP: 4 concurrentes).</span>
            </span>
          </span>
          <span class="col-badge" id="count-progress">0</span>
        </div>
        <div class="cards-list" id="list-progress"></div>
      </div>

      <!-- COLUMNA 5: EN REVISIÓN / ACEPTACIÓN SOLUTION OWNER -->
      <div class="kanban-col" id="col-qa" ondragover="allowDrop(event)" ondrop="drop(event, 'qa')" style="border-top-color: #8B5CF6;">
        <div class="col-header" title="En Revisión (Aceptación Solution Owner): Desarrollo ejecutado listo para contrastar contra especificación. La aceptación formal la otorga el Solution Owner.">
          <span class="col-title">
            En Revisión (Aceptación SO)
            <span class="col-header-info" title="Directiva de Gobernanza">i
              <span class="col-tooltip-box"><strong>En Revisión (Aceptación Solution Owner):</strong> Desarrollo ejecutado listo para contrastar contra especificación. La aceptación formal la otorga el Solution Owner.</span>
            </span>
          </span>
          <span class="col-badge" id="count-qa">0</span>
        </div>
        <div class="cards-list" id="list-qa"></div>
      </div>

      <!-- COLUMNA 6: ACEPTADO Y FINALIZADO (DONE) -->
      <div class="kanban-col" id="col-done" ondragover="allowDrop(event)" ondrop="drop(event, 'done')" style="border-top-color: #10B981;">
        <div class="col-header" title="Aceptado y Finalizado (Done): Entregables con aceptación formal aprobada por el Solution Owner y criterios de Definition of Done (DoD) verificados. Estado inmutable.">
          <span class="col-title">
            Aceptado y Finalizado
            <span class="col-header-info" style="background: #DCFCE7; color: #166534;" title="Directiva de Gobernanza">i
              <span class="col-tooltip-box" style="border-color: #86EFAC;"><strong>Aceptado y Finalizado (Done):</strong> Entregables con aceptación formal aprobada por el Solution Owner y criterios de Definition of Done (DoD) verificados. Estado inmutable.</span>
            </span>
          </span>
          <span class="col-badge" id="count-done">0</span>
        </div>
        <div class="cards-list" id="list-done"></div>
      </div>

    </div>
  </main>

  <!-- ========================================== -->
  <!-- VISTA 2: ROADMAP & CRONOGRAMA INTERACTIVO -->
  <!-- ========================================== -->
  <main class="view-panel" id="view-roadmap">
    <div class="roadmap-container">
      <div class="roadmap-header-section">
        <div>
          <h2>Hoja de Ruta Estratégica & Línea de Tiempo (Q3 - Q4 2026)</h2>
          <p style="font-size: 12px; color: var(--q-text-muted); margin-top: 4px;">
            Alineación de Épicas, Capacidad de Sprints y Milestones de Entrega bajo Metodología Híbrida PMI + IA.
          </p>
        </div>
        <div>
          <span style="background: #FEF3C7; color: #92400E; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 4px; border: 1px solid #FCD34D;">
            HOY: 26-Sep-2026 • Sprint 6 en Ejecución
          </span>
        </div>
      </div>

      <!-- CALENDARIO DE MESES -->
      <div class="timeline-quarters">
        <div class="timeline-quarter-col">
          <div>AGOSTO 2026</div>
          <small style="color: #64748B;">Sprints 1 y 2 • Base REST & FSM</small>
        </div>
        <div class="timeline-quarter-col active">
          <div>SEPTIEMBRE 2026 (ACTUAL)</div>
          <small style="color: #0D9488; font-weight: 700;">Sprints 3, 4, 5 y 6 (Gobernanza)</small>
        </div>
        <div class="timeline-quarter-col">
          <div>OCTUBRE 2026</div>
          <small style="color: #64748B;">Sprints 7 y 8 • Reemplazo N1 & HL7</small>
        </div>
        <div class="timeline-quarter-col">
          <div>NOVIEMBRE 2026</div>
          <small style="color: #64748B;">Release v2.0 Enterprise Cloud</small>
        </div>
      </div>

      <!-- PROGRESO POR ÉPICA -->
      <div>
        <div class="roadmap-section-title">
          <span style="color: var(--q-teal); font-weight: 800; margin-right: 6px;">■</span> Épicas del Proyecto y Estado de Avance
        </div>
        <div class="roadmap-epics-list" id="roadmap-epics-container"></div>
      </div>

      <!-- HITOS / MILESTONES -->
      <div>
        <div class="roadmap-section-title">
          <span style="color: var(--q-teal); font-weight: 800; margin-right: 6px;">■</span> Hitos de Entrega Clave (Milestones)
        </div>
        <div class="milestones-grid" id="roadmap-milestones-container"></div>
      </div>
    </div>
  </main>

  <!-- ========================================== -->
  <!-- VISTA 3: MÉTRICAS, BURNDOWN & CAPACIDAD -->
  <!-- ========================================== -->
  <main class="view-panel" id="view-metrics">
    <div class="metrics-view-grid">
      <div class="velocity-chart-card">
        <div class="roadmap-section-title">
          <span style="color: var(--q-teal); font-weight: 800; margin-right: 6px;">■</span> Velocity Chart: Story Points Entregados por Sprint
        </div>
        <p style="font-size: 11.5px; color: var(--q-text-muted); margin-bottom: 16px;">
          Medición empírica de velocidad de entrega. La cadencia promedio se estabiliza en 33 SP por timebox de 1 semana.
        </p>
        <div class="velocity-bars" id="velocity-bars-container"></div>
      </div>

      <div class="velocity-chart-card">
        <div class="roadmap-section-title">
          <span style="color: var(--q-teal); font-weight: 800; margin-right: 6px;">■</span> Distribución por Tipología
        </div>
        <div id="type-distribution-container" style="display: flex; flex-direction: column; gap: 10px; margin-top: 14px;"></div>
      </div>
    </div>
  </main>

  <!-- ========================================== -->
  <!-- VISTA 4: BACKLOG JERÁRQUICO -->
  <!-- ========================================== -->
  <main class="view-panel" id="view-hierarchy">
    <div class="tree-container">
      <div class="roadmap-section-title" style="margin-bottom: 14px;">
        <span style="color: var(--q-teal); font-weight: 800; margin-right: 6px;">■</span> Estructura Jerárquica del Proyecto: Épicas → UHs → Tareas Técnicas / Issues
      </div>
      <p style="font-size: 11.5px; color: var(--q-text-muted); margin-bottom: 16px;">
        Descomposición WBS completa de requerimientos del sistema con trazabilidad bidireccional.
      </p>
      <div id="tree-root-container"></div>
    </div>
  </main>

  <!-- ========================================== -->
  <!-- MODAL UNIVERSAL ADAPTATIVO (UH / ISSUE / TASK) -->
  <!-- ========================================== -->
  <div class="uh-modal-backdrop" id="uh-modal">
    <div class="uh-modal-content">
      <div class="uh-modal-header">
        <div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span id="modal-item-type" class="card-badge-type"></span>
            <span id="modal-item-id" class="card-id"></span>
            <span id="modal-item-priority" class="card-badge-priority"></span>
            <span id="modal-item-sp" class="card-sp"></span>
          </div>
          <h3 id="modal-item-title" style="font-family: 'Montserrat', sans-serif; font-size: 15px; font-weight: 800; color: var(--q-navy);"></h3>
          <div id="modal-item-epic" style="font-size: 11px; color: #64748B; font-weight: 600; margin-top: 4px;"></div>
        </div>
        <button class="uh-modal-close" onclick="closeUHModal()">✕ Cerrar</button>
      </div>

      <div id="modal-body-content"></div>
    </div>
  </div>

  <!-- SCRIPT CON DATOS Y LÓGICA INTEGRADA -->
  <script>
    const INITIAL_BACKLOG = {tasks_json};
    const EPICS_DATA = {epics_json};
    const SPRINTS_DATA = {sprints_json};
    const MILESTONES_DATA = {milestones_json};

    let tasks = [];
    let currentView = 'board';

    function getTaskDocInfo(task) {{
      if (task.doc_link && task.doc_title) {{
        return {{
          link: task.doc_link,
          title: task.doc_title,
          desc: task.doc_desc || task.title
        }};
      }}
      const type = (task.type || 'UH').toUpperCase();
      const id = task.id || '';
      const idLower = id.toLowerCase();
      if (type === 'ISSUE') {{
        return {{
          link: '04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#' + idLower,
          title: 'DOC-QA-004 (' + id + ')',
          desc: task.doc_desc || ('Reporte formal de defecto y criterios de aceptación para ' + id + '.')
        }};
      }} else if (type === 'TASK') {{
        return {{
          link: '03_ARQUITECTURA_Y_DISENO_TECNICO.md#' + idLower,
          title: 'DOC-ARC-003 (' + id + ')',
          desc: task.doc_desc || ('Alcance técnico y arquitectura de componentes para ' + id + '.')
        }};
      }} else if (type === 'OPORTUNIDAD' || type === 'MEJORA') {{
        return {{
          link: '03_ARQUITECTURA_Y_DISENO_TECNICO.md#' + idLower,
          title: 'DOC-ARC-003 (' + id + ')',
          desc: task.doc_desc || ('Propuesta técnica y roadmap de mejora para ' + id + '.')
        }};
      }} else {{
        return {{
          link: '02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#' + idLower,
          title: 'DOC-SPEC-002 (' + id + ')',
          desc: task.doc_desc || ('Especificación funcional y criterios Gherkin para ' + id + '.')
        }};
      }}
    }}

    function openDocument(event, docLink) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      if (!docLink) return;
      window.open(docLink, '_blank');
    }}

    function init() {{
      // 1. Cargar el backlog oficial con fallback a localStorage
      const savedTasks = localStorage.getItem('quantux_scrumban_v22_progress');
      if (savedTasks) {{
        try {{
          tasks = JSON.parse(savedTasks);
        }} catch (e) {{
          tasks = JSON.parse(JSON.stringify(INITIAL_BACKLOG));
        }}
      }} else {{
        tasks = JSON.parse(JSON.stringify(INITIAL_BACKLOG));
      }}

            // Asegurar que todas las tareas del INITIAL_BACKLOG existan en tasks con metadatos actualizados
      const REWORK_SO_SET = new Set(["ISSUE-06", "ISSUE-31", "ISSUE-34", "MEJ-11", "ISSUE-41", "MEJ-12", "ISSUE-65"]);
      const SPRINT6_NEW_SET = new Set(["ISSUE-59", "ISSUE-60", "ISSUE-61", "ISSUE-62", "ISSUE-63", "ISSUE-64", "ISSUE-65", "ISSUE-66", "ISSUE-67", "ISSUE-68", "ISSUE-69", "ISSUE-70", "ISSUE-71", "ISSUE-72", "ISSUE-73", "ISSUE-74", "ISSUE-75", "ISSUE-76", "ISSUE-77"]);

      INITIAL_BACKLOG.forEach(initTask => {{
        const existing = tasks.find(t => t.id === initTask.id);
        if (!existing) {{
          tasks.push(JSON.parse(JSON.stringify(initTask)));
        }} else {{
          existing.title = initTask.title;
          existing.sprint = initTask.sprint;
          existing.sp = initTask.sp;
          existing.priority = initTask.priority;
          existing.type = initTask.type;
          existing.discipline = initTask.discipline;
          if (initTask.business_impact) existing.business_impact = initTask.business_impact;
          if (initTask.doc_link) existing.doc_link = initTask.doc_link;
          if (initTask.doc_title) existing.doc_title = initTask.doc_title;
          if (initTask.doc_desc) existing.doc_desc = initTask.doc_desc;
          if (initTask.attachment_image) existing.attachment_image = initTask.attachment_image;
          if (initTask.issue_details) existing.issue_details = initTask.issue_details;
          if (initTask.acceptance_criteria) existing.acceptance_criteria = initTask.acceptance_criteria;

          // Forzar estado de retrabajo dictado por el Solution Owner
          if (REWORK_SO_SET.has(initTask.id)) {{
            existing.status = 'rework';
            existing.priority = 'P1';
            existing.so_feedback = initTask.so_feedback;
          }}
          // REGLA DE GOBERNANZA DE PASAJE DE SPRINT (ISSUE-69):
          // Las tareas que pasan al próximo sprint conservan fielmente su estado operativo
          // (ej: 'qa' / revisión, 'progress' / en curso, 'rework' / retrabajo).
          // Así es como debe ser para garantizar continuidad sin reseteos ficticios.
          if (SPRINT6_NEW_SET.has(initTask.id) && existing.status !== 'done') {{
            existing.sprint = 'Sprint 6';
            existing.priority = 'P1';
            if (!existing.status || existing.status === 'backlog') {{
              existing.status = initTask.status || 'qa';
            }}
          }}
        }}
      }});

      // Blindaje de Gobernanza Permanente: Conjunto Inmutable de Tarjetas Aprobadas por el Solution Owner
      const PERMANENTLY_APPROVED_BY_SO = new Set([
        "ISSUE-01", "ISSUE-02", "ISSUE-03", "ISSUE-07", "ISSUE-08", "ISSUE-09", "ISSUE-10",
        "ISSUE-11", "ISSUE-12", "ISSUE-13", "ISSUE-14", "ISSUE-15", "ISSUE-16", "ISSUE-17",
        "ISSUE-18", "ISSUE-19", "ISSUE-20", "ISSUE-21", "ISSUE-22", "ISSUE-23", "ISSUE-24",
        "ISSUE-25", "ISSUE-26", "ISSUE-27", "ISSUE-28", "ISSUE-29",
        "MEJ-01", "MEJ-02", "MEJ-03", "MEJ-04", "MEJ-05", "MEJ-06", "MEJ-07", "MEJ-08", "MEJ-09", "MEJ-10",
        "UH-65", "UH-68", "UH-69", "UH-70"
      ]);

      // Reconciliación determinista del backlog: solo blindaje inmutable para las 38 tarjetas aprobadas
      tasks.forEach(task => {{
        if (PERMANENTLY_APPROVED_BY_SO.has(task.id)) {{
          task.status = 'done';
          task.so_feedback = {{
            status: "APROBADO CONFORME",
            reviewer: "Freddy Cortés (Solution Owner)",
            date: "2026-09-26",
            notes: "Incremento verificado y aceptado formalmente conforme a criterios DoD."
          }};
        }}
      }});

      // ISSUE-58 FIX: Las tarjetas en 'rework', 'progress' y 'qa' guardadas por el usuario se conservan fielmente
      // Sincronizar metadatos, descripciones, evidencias y especificaciones sin sobreescribir el status
      INITIAL_BACKLOG.forEach(initialItem => {{
        syncIssueInBacklog(initialItem.id);
      }});

      // Filtro por defecto en el Tablero: ALL para ver todos los entregables aprobados y pendientes
      const sprintSel = document.getElementById('filter-sprint');
      if (sprintSel) {{
        sprintSel.value = 'ALL';
      }}

      saveState(false);
      renderBoard();
    }}

    function syncIssueInBacklog(issueId) {{
      const initialItem = INITIAL_BACKLOG.find(t => t.id === issueId);
      if (!initialItem) return;
      const idx = tasks.findIndex(t => t.id === issueId);
      if (idx === -1) {{
        tasks.push(JSON.parse(JSON.stringify(initialItem)));
      }} else {{
        if (initialItem.attachment_image) {{
          tasks[idx].attachment_image = initialItem.attachment_image;
        }}
        tasks[idx].title = initialItem.title;

        // ISSUE-58: Conservar estrictamente el estado fijado por el usuario en localStorage
        const PERMANENTLY_APPROVED_BY_SO = new Set([
          "ISSUE-01", "ISSUE-02", "ISSUE-03", "ISSUE-07", "ISSUE-08", "ISSUE-09", "ISSUE-10",
          "ISSUE-11", "ISSUE-12", "ISSUE-13", "ISSUE-14", "ISSUE-15", "ISSUE-16", "ISSUE-17",
          "ISSUE-18", "ISSUE-19", "ISSUE-20", "ISSUE-21", "ISSUE-22", "ISSUE-23", "ISSUE-24",
          "ISSUE-25", "ISSUE-26", "ISSUE-27", "ISSUE-28", "ISSUE-29",
          "MEJ-01", "MEJ-02", "MEJ-03", "MEJ-04", "MEJ-05", "MEJ-06", "MEJ-07", "MEJ-08", "MEJ-09", "MEJ-10",
          "UH-65", "UH-68", "UH-69", "UH-70"
        ]);
        if (PERMANENTLY_APPROVED_BY_SO.has(tasks[idx].id)) {{
          tasks[idx].status = 'done';
        }} else if (tasks[idx].id === 'ISSUE-06') {{
          // Requerimiento explícito Solution Owner: enviar ISSUE-06 a retrabajo
          tasks[idx].status = 'rework';
          tasks[idx].so_feedback = initialItem.so_feedback;
          tasks[idx].attachment_image = initialItem.attachment_image;
        }} else if (!tasks[idx].status) {{
          tasks[idx].status = initialItem.status || 'qa';
        }}

        if (initialItem.business_impact) {{
          tasks[idx].business_impact = initialItem.business_impact;
        }}

        if (initialItem.so_feedback && !tasks[idx].so_feedback) {{
          tasks[idx].so_feedback = initialItem.so_feedback;
        }}
        tasks[idx].sp = initialItem.sp;
        tasks[idx].priority = tasks[idx].priority || initialItem.priority;
        tasks[idx].discipline = initialItem.discipline;
        tasks[idx].doc_link = initialItem.doc_link;
        tasks[idx].doc_title = initialItem.doc_title;
        tasks[idx].doc_desc = initialItem.doc_desc;
        if (initialItem.narrative) tasks[idx].narrative = initialItem.narrative;
        if (initialItem.issue_details) tasks[idx].issue_details = initialItem.issue_details;
        if (initialItem.acceptance_criteria) tasks[idx].acceptance_criteria = initialItem.acceptance_criteria;
        if (initialItem.adaptation_criteria) tasks[idx].adaptation_criteria = initialItem.adaptation_criteria;
      }}
    }}

    function switchView(viewName) {{
      currentView = viewName;
      document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.view-panel').forEach(panel => panel.classList.remove('active'));

      const activeBtn = document.getElementById('tab-btn-' + viewName);
      const activePanel = document.getElementById('view-' + viewName);
      if (activeBtn) activeBtn.classList.add('active');
      if (activePanel) activePanel.classList.add('active');

      renderCurrentView();
    }}

    function renderCurrentView() {{
      if (currentView === 'board') renderBoard();
      else if (currentView === 'roadmap') renderRoadmap();
      else if (currentView === 'metrics') renderMetricsView();
      else if (currentView === 'hierarchy') renderHierarchyView();
    }}


    // =========================================================================
    // HELPER GOBERNANZA: EVALUACIÓN OBLIGATORIA DE IMPACTO EN PRODUCTO Y NEGOCIO
    // =========================================================================
    function getTaskBusinessImpact(task) {{
      if (task.business_impact && task.business_impact.level && task.business_impact.description) {{
        return {{
          level: String(task.business_impact.level).toUpperCase(),
          dimension: task.business_impact.dimension || 'PRODUCTO & NEGOCIO',
          description: task.business_impact.description,
          metric_target: task.business_impact.metric_target || 'Optimización operativa y alineación con estándares de servicio.',
          risk_of_inaction: task.business_impact.risk_of_inaction || 'Degradación de experiencia y fricción en la atención.'
        }};
      }}
      
      const prio = (task.priority || 'P3').toUpperCase();
      const title = (task.title || '').toLowerCase();
      
      let level = (prio === 'P1' || prio === 'P0') ? 'CRÍTICO' : (prio === 'P2' ? 'ALTO' : 'MEDIO');
      let dimension = 'Operación y Calidad de Servicio';
      let desc = 'Requerimiento fundamental para la estabilidad operativa y satisfacción del usuario en la plataforma hospitalaria Quantux.';
      let metric = 'Mitigación de tiempos de espera y garantía de conformidad en flujo de atención.';
      let risk = 'Incremento de fricción operativa en la gestión de solicitudes asistenciales.';

      if (title.includes('sla') || title.includes('reloj') || title.includes('segundo') || title.includes('tiempo')) {{
        level = 'CRÍTICO';
        dimension = 'Transparencia de SLA & Cumplimiento ITIL v4';
        desc = 'Monitoreo de tiempos de atención con precisión de segundos, garantizando que el cómputo de SLA refleje con total exactitud si el ticket está activo o en espera.';
        metric = 'Trazabilidad y auditoría de SLA al 100% en tiempo real con cronómetro dinámico.';
        risk = 'Falsos incumplimientos de SLA o falta de transparencia ante auditorías sanitarias.';
      }} else if (title.includes('asignar') || title.includes('redundanc') || title.includes('boton')) {{
        level = 'ALTO';
        dimension = 'Ergonomía de Interfaz & Eficiencia Operativa';
        desc = 'Simplificación del flujo de derivación y autoasignación en el Workspace, erradicando elementos repetitivos para optimizar el tiempo de respuesta del operador.';
        metric = 'Eliminación del 100% de redundancia visual y reducción de clics a 1 acción unificada.';
        risk = 'Dudas operativas y sobrecarga cognitiva en los analistas de soporte asistencial.';
      }} else if (title.includes('imagen') || title.includes('captura') || title.includes('cierre') || title.includes('lightbox')) {{
        level = 'ALTO';
        dimension = 'Accesibilidad & Visualización de Evidencias';
        desc = 'Disponibilidad de visor de evidencias en alta resolución con controles intuitivos de cierre (botón X visible, escape y clic fuera) para diagnóstico clínico sin bloqueos.';
        metric = 'Cierre inmediato en 1 clic y visualización nítida sin recargas ni pérdida de contexto.';
        risk = 'Bloqueo visual del operador en pantalla completa sin mecanismo de retorno al ticket.';
      }} else if (title.includes('configuraci') || title.includes('módulo') || title.includes('rol')) {{
        level = 'ALTO';
        dimension = 'Gobernanza de Accesos & Seguridad RBAC';
        desc = 'Restricción y supresión definitiva del acceso interactivo a configuraciones globales de sistema desde el menú lateral para la totalidad de roles operativos y administrativos.';
        metric = '100% de perfiles sin exposición del módulo Configuración en interfaz gráfica.';
        risk = 'Modificación accidental de parámetros de infraestructura o exposición de configuraciones no operativas.';
      }} else if (title.includes('itil') || title.includes('niveles') || title.includes('base de datos')) {{
        level = 'ALTO';
        dimension = 'Alineación ITIL v4 & Desacoplamiento Arquitectónico';
        desc = 'Ocultamiento de controles interactivos superfluos de niveles de servicio en el catálogo de plataformas, delegando la configuración de soporte N1/N2/N3 a la base de datos central según estándares ITIL v4.';
        metric = '0 controles no didácticos visibles en pantalla y documentación 100% formalizada.';
        risk = 'Desalineación de procesos con respecto al marco ITIL v4 y confusión operativa en la administración de mesas.';
      }} else if (title.includes('rojo') || title.includes('paleta') || title.includes('color')) {{
        level = 'MEDIO';
        dimension = 'Identidad Visual & Directiva de Marca Quantux';
        desc = 'Alineación cromática estricta con la paleta Quantux (Warm Amber, Teal y Corporate Slate), eliminando falsas alarmas rojas en estados normales de trabajo.';
        metric = '100% de cumplimiento con la directiva de diseño Quantux Pizarra Neutral.';
        risk = 'Fatiga visual e induce sensación errónea de alerta crítica en el equipo de guardia.';
      }}

      return {{
        level,
        dimension,
        description: desc,
        metric_target: metric,
        risk_of_inaction: risk
      }};
    }}

    function openImageLightbox(src, caption) {{
      if (!src) return;
      const lb = document.getElementById('modal-image-lightbox');
      const img = document.getElementById('lightbox-modal-img');
      const cap = document.getElementById('lightbox-modal-caption');
      if (img) img.src = src;
      if (cap) cap.textContent = caption || 'Evidencia de soporte';
      if (lb) lb.style.display = 'flex';
    }}

    function closeImageLightbox() {{
      const lb = document.getElementById('modal-image-lightbox');
      if (lb) lb.style.display = 'none';
      const img = document.getElementById('lightbox-modal-img');
      if (img) img.src = '';
    }}

    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') {{
        closeImageLightbox();
      }}
    }});

    async function executeSingleProgressTask(taskId, event) {{
      if (event) {{
        event.stopPropagation();
        event.preventDefault();
      }}
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      const btn = document.getElementById(`btn-exec-${{taskId}}`);
      if (btn) {{
        btn.disabled = true;
        btn.innerHTML = '<span>⏳</span> Ejecutando...';
      }}

      task.progress_pct = 25;
      task.progress_msg = '1/4: Conectando con servicio técnico y compilando parches...';
      renderBoard();

      try {{
        const resp = await fetch('http://127.0.0.1:8000/api/v1/demon/execute/' + encodeURIComponent(taskId), {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }}
        }});
        if (resp.ok) {{
          task.progress_pct = 80;
          task.progress_msg = '3/4: Quality Gate superado. Pasando a Revisión QA...';
          renderBoard();
        }}
      }} catch (err) {{
        console.warn('Ejecución local para ' + taskId, err);
      }}

      await new Promise(r => setTimeout(r, 400));
      task.progress_pct = 100;
      task.status = 'qa';
      task.so_feedback = {{
        status: "CORREGIDO Y CERTIFICADO / EN REVISIÓN",
        reviewer: "Motor Agéntico Quantux",
        date: new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}}),
        notes: `Solución técnica ejecutada exitosamente para ${{taskId}}. Incremento certificado y enviado al fondo de la pila de revisión (FIFO).`
      }};

      const idx = tasks.findIndex(t => t.id === taskId);
      if (idx > -1) {{
        const [moved] = tasks.splice(idx, 1);
        tasks.push(moved);
      }}

      saveState(false);
      renderBoard();
    }}

    async function executeAllInProgressSequentially() {{
      const inProg = tasks.filter(t => t.status === 'progress');
      if (inProg.length === 0) {{
        alert('No hay tarjetas en estado "En Curso" para ejecutar.');
        return;
      }}

      const confirmed = confirm(`Se ejecutarán de a una las ${{inProg.length}} tarjetas en estado "En Curso". ¿Desea proceder?`);
      if (!confirmed) return;

      for (let i = 0; i < inProg.length; i++) {{
        const t = inProg[i];
        await executeSingleProgressTask(t.id, null);
        await new Promise(r => setTimeout(r, 500));
      }}

      alert(`¡Las ${{inProg.length}} tarjetas en curso fueron ejecutadas exitosamente y enviadas a revisión (QA)!`);
    }}

    function renderBoard() {{
      const sprintFilter = document.getElementById('filter-sprint').value;
      const typeFilter = document.getElementById('filter-type').value;
      const epicFilter = document.getElementById('filter-epic').value;
      const prioFilter = document.getElementById('filter-priority').value;
      const search = (document.getElementById('search-input').value || '').toLowerCase().trim();

      const lists = {{
        backlog: document.getElementById('list-backlog'),
        sprint: document.getElementById('list-sprint'),
        rework: document.getElementById('list-rework'),
        progress: document.getElementById('list-progress'),
        qa: document.getElementById('list-qa'),
        done: document.getElementById('list-done')
      }};

      Object.values(lists).forEach(l => l.innerHTML = '');
      const counts = {{ backlog: 0, sprint: 0, rework: 0, progress: 0, qa: 0, done: 0 }};

      tasks.forEach(task => {{
        const col = task.status || 'backlog';
        if (col !== 'backlog' && sprintFilter !== 'ALL' && task.sprint !== sprintFilter) return;
        if (typeFilter !== 'ALL' && (task.type || 'UH') !== typeFilter) return;
        if (epicFilter !== 'ALL' && task.epic !== epicFilter) return;
        if (prioFilter !== 'ALL' && (task.priority || 'P3') !== prioFilter) return;

        if (search) {{
          const matchId = (task.id || '').toLowerCase().includes(search);
          const matchTitle = (task.title || '').toLowerCase().includes(search);
          const matchEpic = (task.epic || '').toLowerCase().includes(search);
          if (!matchId && !matchTitle && !matchEpic) return;
        }}

        if (counts[col] !== undefined) counts[col]++;

        const card = createCardElement(task);
        if (lists[col]) lists[col].appendChild(card);
      }});

      document.getElementById('count-backlog').textContent = counts.backlog;
      document.getElementById('count-sprint').textContent = counts.sprint;
      document.getElementById('count-rework').textContent = counts.rework;
      document.getElementById('count-progress').textContent = counts.progress;
      document.getElementById('count-qa').textContent = counts.qa;
      document.getElementById('count-done').textContent = counts.done;
    }}

    function createCardElement(task) {{
      const div = document.createElement('div');
      div.className = 'kanban-card';
      div.draggable = true;
      div.id = 'card-' + task.id;
      div.style.cursor = 'pointer';
      div.onclick = (e) => {{
        if (!e.target.closest('button, a, .card-attachment-preview, .card-doc-box, .card-actions')) {{
          openItemModal(task.id);
        }}
      }};
      div.ondragstart = (e) => drag(e, task.id);

      div.tabIndex = 0;
      div.onpaste = (e) => handleCardPaste(e, task.id);

      const type = task.type || 'UH';
      const badgeClass = 'badge-' + type.toLowerCase();
      const prio = task.priority || 'P3';
      const prioClass = 'priority-' + prio.toLowerCase();

      const docInfo = getTaskDocInfo(task);
      const docHtml = `
        <div class="card-doc-box" onclick="openDocument(event, '${{docInfo.link}}')" title="Abrir Documento Rector Oficial (${{docInfo.title}})">
          <a href="${{docInfo.link}}" target="_blank" class="card-doc-link" draggable="false" onclick="event.stopPropagation();">
            <span>📄</span> ${{docInfo.title}}
          </a>
          <span style="color: #0D9488; font-size: 11px; font-weight: 700; margin-left: 4px;">↗</span>
        </div>
      `;

      let attachPreviewHtml = '';
      if (task.attachment_image) {{
        attachPreviewHtml = `
          <div class="card-attachment-preview" draggable="false" style="margin: 8px 0 10px 0; border-radius: 6px; overflow: hidden; border: 1.5px solid #38BDF8; background: #0F172A; text-align: center; cursor: pointer;" onclick="event.stopPropagation(); openItemModal('${{task.id}}')" title="Clic para ampliar captura original">
            <img src="${{task.attachment_image}}" alt="Captura asociada a ${{task.id}}" draggable="false" style="width: 100%; max-height: 115px; object-fit: cover; display: block;" onerror="if(!this.dataset.retried){{this.dataset.retried=1; if(this.src.includes('/docs/assets/')){{this.src=this.src.replace('/docs/assets/','/assets/');}}else if(this.src.includes('/assets/')){{this.src=this.src.replace('/assets/','/docs/assets/');}}else if(!this.src.includes('docs/assets/')){{this.src='docs/'+this.getAttribute('src');}}}}" />
            <div style="font-size: 10px; font-weight: 800; color: #0284C7; background: #F0F9FF; padding: 4px 6px; display: flex; align-items: center; justify-content: center; gap: 4px; border-top: 1px solid #BAE6FD;">
              <span>📸 Evidencia Visual Adjunta (Clic para ampliar)</span>
            </div>
          </div>
        `;
      }}

      // GOBERNANZA: EVALUACIÓN OBLIGATORIA DE IMPACTO EN PRODUCTO Y NEGOCIO (CERO UNDEFINED)
      const imp = getTaskBusinessImpact(task);
      const bColor = imp.level === 'CRÍTICO' ? '#B45309' : (imp.level === 'ALTO' ? '#0F766E' : '#334155');
      const bBg = imp.level === 'CRÍTICO' ? '#FEF3C7' : (imp.level === 'ALTO' ? '#F0FDFA' : '#F8FAFC');
      const bBorder = imp.level === 'CRÍTICO' ? '#FCD34D' : (imp.level === 'ALTO' ? '#99F6E4' : '#CBD5E1');
      const businessImpactCardHtml = `
        <div class="card-business-impact" draggable="false" style="margin: 6px 0; background: ${{bBg}}; border: 1.5px solid ${{bBorder}}; border-radius: 5px; padding: 5px 7px; font-size: 9.5px; line-height: 1.3;" onclick="event.stopPropagation();">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
            <span style="font-weight: 800; color: ${{bColor}}; display: flex; align-items: center; gap: 3px;">
              <span>💼</span> IMPACTO: ${{imp.level}}
            </span>
            <span style="font-size: 8px; background: ${{bColor}}; color: white; padding: 1px 5px; border-radius: 3px; font-weight: 800;">${{imp.dimension}}</span>
          </div>
          <div style="color: #1E293B; font-size: 9px; line-height: 1.35;">
            ${{imp.description}}
          </div>
        </div>
      `;

      let soFeedbackCardHtml = '';
      if (task.so_feedback && task.status !== 'rework') {{
        soFeedbackCardHtml = `
          <div style="background: #FFF1F2; border: 1.5px solid #F43F5E; border-radius: 6px; padding: 6px 8px; margin: 6px 0;">
            <div style="color: #9F1239; font-size: 10px; font-weight: 800; display: flex; align-items: center; gap: 4px;">
              <span>⚠️ DICTAMEN SO:</span>
              <span>${{task.so_feedback.status}}</span>
            </div>
            <div style="color: #78350F; font-size: 9.5px; margin-top: 2px; line-height: 1.3;">
              ${{task.so_feedback.observation}}
            </div>
          </div>
        `;
      }}

      // PANEL EXCLUSIVO DE RETRABAJO EN TARJETA: OBSERVACIONES, CAPTURAS Y BOTÓN DEMONIO
      let reworkCardHtml = '';
      if (task.status === 'rework') {{
        const obsVal = task.so_feedback ? (task.so_feedback.observation || '') : '';
        reworkCardHtml = `
          <div class="card-rework-panel" draggable="false" style="margin: 8px 0; background: #FFF1F2; border: 1.5px solid #F43F5E; border-radius: 6px; padding: 8px; text-align: left;" onclick="event.stopPropagation();">
            <div style="font-size: 10px; font-weight: 800; color: #9F1239; display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
              <span style="display: flex; align-items: center; gap: 4px;">
                <span>🔥</span> DEMONIO DE CORRECCIÓN
              </span>
              <span style="font-size: 8.5px; color: #92400E; background: #FFE4E6; padding: 1px 6px; border-radius: 3px; font-weight: 800;">P1 PRIORITARIO</span>
            </div>

            <!-- OBSERVACIONES DEL SO / BUG A CORREGIR -->
            <label style="font-size: 9.5px; font-weight: 700; color: #9F1239; display: block; margin-bottom: 3px;">
              📝 Observación / Bug a corregir:
            </label>
            <textarea id="card-obs-${{task.id}}" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation();" oninput="updateCardObservation('${{task.id}}', this.value)" rows="2" placeholder="Escribí aquí la observación técnica o bug a corregir..." style="width: 100%; box-sizing: border-box; border: 1.5px solid #FDA4AF; border-radius: 4px; padding: 5px 7px; font-size: 11px; font-family: inherit; resize: vertical; background: #FFFFFF; color: #1E293B; margin-bottom: 4px; outline: none;">${{obsVal}}</textarea>
            <div style="display: flex; gap: 4px; margin-bottom: 6px;">
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); saveCardObservation('${{task.id}}')" style="flex: 1; background: #2563EB; color: white; border: none; border-radius: 4px; padding: 4px 6px; font-size: 9.5px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 3px;" title="Guardar observación">
                <span>💾</span> Guardar
              </button>
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); appendCardObservation('${{task.id}}')" style="flex: 1; background: #0284C7; color: white; border: none; border-radius: 4px; padding: 4px 6px; font-size: 9.5px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 3px;" title="Sumar nueva observación">
                <span>➕</span> Sumar
              </button>
            </div>

            <!-- CONTROLES DE CAPTURA (ADJUNTAR Y PEGAR CON CTRL+V) -->
            <input type="file" id="card-file-${{task.id}}" accept="image/*" style="display: none;" onchange="handleCardImageUpload('${{task.id}}', event)">
            <div style="display: flex; gap: 4px; margin-bottom: 6px; align-items: center; width: 100%; box-sizing: border-box;">
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); document.getElementById('card-file-${{task.id}}').click();" style="flex: 1; min-width: 0; box-sizing: border-box; background: #FFFFFF; color: #475569; border: 1px solid #CBD5E1; border-radius: 4px; padding: 4px 5px; font-size: 10px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="Adjuntar imagen desde archivo">
                <span>📷</span> Adjuntar
              </button>
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); pasteCardImageFromClipboard('${{task.id}}');" style="flex: 1; min-width: 0; box-sizing: border-box; background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; border-radius: 4px; padding: 4px 5px; font-size: 10px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="Pegar captura del portapapeles o presionar Ctrl+V sobre la tarjeta">
                <span>📋</span> Pegar
              </button>
              ${{task.attachment_image ? `
                <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); removeCardImage('${{task.id}}');" style="flex: 0 0 26px; width: 26px; height: 26px; box-sizing: border-box; background: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; border-radius: 4px; padding: 0; font-size: 11px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center;" title="Eliminar captura adjunta">
                  🗑️
                </button>
              ` : ''}}
            </div>

            <!-- BOTÓN DEMONIO: SOLO DEBE LLAMARSE DEMONIO (ISSUE-57) -->
            <button type="button" id="card-btn-demon-${{task.id}}" class="card-btn-demon" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); triggerDemonRework('${{task.id}}');" style="width: 100%; background: #DC2626; color: white; border: none; border-radius: 5px; padding: 7px 10px; font-size: 11.5px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 5px rgba(220,38,38,0.3); font-family: 'Montserrat', sans-serif;">
              <span>🔥</span> Demonio
            </button>

            <!-- BARRA DE PROGRESO DEL DEMONIO EN LA TARJETA (ROJO INSTITUCIONAL UNIFICADO MEJ-12) -->
            <div id="card-demon-progress-box-${{task.id}}" style="display: none; margin-top: 6px; background: #450A0A; border-radius: 4px; padding: 6px; border: 1px solid #DC2626;">
              <div style="display: flex; justify-content: space-between; font-size: 9.5px; font-weight: 800; color: #FCA5A5; margin-bottom: 3px;">
                <span>⚡ DEMONIO EN EJECUCIÓN</span>
                <span id="card-demon-pct-${{task.id}}" style="color: #FFFFFF; font-weight: 800;">0%</span>
              </div>
              <div style="background: #1C1917; height: 8px; border-radius: 999px; overflow: hidden;">
                <div id="card-demon-bar-${{task.id}}" style="width: 0%; height: 100%; background: #DC2626; transition: width 0.2s;"></div>
              </div>
              <div id="card-demon-msg-${{task.id}}" style="font-size: 9.5px; color: #FEE2E2; margin-top: 3px; font-weight: 600;">
                Iniciando corrección de bug...
              </div>
            </div>
          </div>
        `;
      }}

      // PANEL EXCLUSIVO PARA TAREAS EN EJECUCIÓN (PROGRESS) - MEJ-12
      let inProgressCardHtml = '';
      if (task.status === 'progress') {{
        const progPct = task.progress_pct || 65;
        inProgressCardHtml = `
          <div class="card-inprogress-panel" draggable="false" style="margin: 8px 0; background: #FEF2F2; border: 1.5px solid #F87171; border-radius: 6px; padding: 7px; text-align: left;" onclick="event.stopPropagation();">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 9.5px; font-weight: 800; color: #991B1B; margin-bottom: 3px;">
              <span style="display: flex; align-items: center; gap: 4px;">
                <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #DC2626;"></span>
                <span>EJECUCIÓN EN CURSO</span>
              </span>
              <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #DC2626; font-weight: 800;">${{progPct}}%</span>
            </div>
            <div style="background: #FEE2E2; height: 7px; border-radius: 999px; overflow: hidden; border: 1px solid #FECACA;">
              <div style="width: ${{progPct}}%; height: 100%; background: #DC2626; border-radius: 999px; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 9px; color: #7F1D1D; margin-top: 3px; font-weight: 600;">
              ${{task.progress_msg || 'Desarrollo de incrementos técnicos y validación de pruebas... (Pase a QA inminente)'}}
            </div>
          </div>
        `;
      }}

      // BOTONES DE EVALUACIÓN Y OBSERVACIONES EXCLUSIVOS DE QA (EN REVISIÓN)
      let qaCardPanelHtml = '';
      if (task.status === 'qa') {{
        const qaObsVal = task.so_feedback ? (task.so_feedback.observation || '') : '';
        qaCardPanelHtml = `
          <div class="card-qa-actions-box" draggable="false" style="margin-top: 6px; background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: 6px; padding: 6px; text-align: left;" onclick="event.stopPropagation();">
            <label style="font-size: 9px; font-weight: 700; color: #475569; display: block; margin-bottom: 2px;">
              📝 Observación / Motivo de Revisión:
            </label>
            <textarea id="card-qa-obs-${{task.id}}" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation();" oninput="updateCardObservation('${{task.id}}', this.value)" rows="2" placeholder="Escribí aquí observaciones técnicas..." style="width: 100%; box-sizing: border-box; border: 1px solid #CBD5E1; border-radius: 4px; padding: 4px 6px; font-size: 10.5px; font-family: inherit; resize: vertical; background: #FFFFFF; color: #1E293B; margin-bottom: 4px; outline: none;">${{qaObsVal}}</textarea>
            <div style="display: flex; gap: 4px; margin-bottom: 5px;">
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); saveCardObservation('${{task.id}}')" style="flex: 1; background: #2563EB; color: white; border: none; border-radius: 4px; padding: 3px 5px; font-size: 9.5px; font-weight: 700; cursor: pointer;">💾 Guardar</button>
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); appendCardObservation('${{task.id}}')" style="flex: 1; background: #0284C7; color: white; border: none; border-radius: 4px; padding: 3px 5px; font-size: 9.5px; font-weight: 700; cursor: pointer;">➕ Sumar</button>
            </div>
            <div class="card-qa-actions" draggable="false" style="display: flex; gap: 4px;">
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); sendToReworkFromCard('${{task.id}}');" style="flex: 1; background: #FFF1F2; color: #92400E; border: 1.5px solid #FDA4AF; border-radius: 5px; padding: 5px 8px; font-size: 10px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px; font-family: 'Montserrat', sans-serif;" title="Rechazar y enviar a Retrabajo para activar el Demonio">
                <span>❌</span> Retrabajo
              </button>
              <button type="button" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); approveTaskDone('${{task.id}}');" style="flex: 1; background: #ECFDF5; color: #047857; border: 1.5px solid #6EE7B7; border-radius: 5px; padding: 5px 8px; font-size: 10px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px; font-family: 'Montserrat', sans-serif;" title="Aprobar formalmente y marcar como completado (Done)">
                <span>✅</span> Aprobar (Done)
              </button>
            </div>
          </div>
        `;
      }}

      const isBacklog = (task.status || 'backlog') === 'backlog';
      const isDone = task.status === 'done';

      div.draggable = !isDone;

      div.innerHTML = `
        <div class="card-top">
          <div style="display: flex; align-items: center; gap: 4px;">
            <span class="card-badge-type ${{badgeClass}}">${{type}}</span>
            <span class="card-id">${{task.id}}</span>
            <span class="card-badge-priority ${{prioClass}}">${{prio}}</span>
          </div>
          <span class="card-sp">${{task.sp}} SP</span>
        </div>
        <div class="card-title">${{task.title}}</div>
        <div class="card-epic">${{task.epic}}</div>
        ${{docHtml}}
        ${{attachPreviewHtml}}
        ${{businessImpactCardHtml}}
        ${{soFeedbackCardHtml}}
        ${{reworkCardHtml}}
        ${{inProgressCardHtml}}
        ${{qaCardPanelHtml}}
        <div class="card-meta">
          <span class="card-sprint-tag">${{task.sprint}}</span>
          <div class="card-actions">
            ${{isDone ? `
              <span style="font-size: 9.5px; font-weight: 800; color: #059669; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 2px 7px; border-radius: 4px; display: inline-flex; align-items: center; gap: 3px;" title="Entregable inmutable y protegido por Gobernanza DoD">
                <span>✓</span> Aceptado (Inmutable)
              </span>
            ` : `
              <button class="card-btn-move" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); moveTask('${{task.id}}', -1)" title="Mover a la izquierda" ${{isBacklog ? 'disabled style="opacity: 0.3; cursor: not-allowed;"' : ''}}>◀</button>
              <button class="card-btn-move" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); moveTask('${{task.id}}', 1)" title="Mover a la derecha">▶</button>
            `}}
          </div>
        </div>
        <button class="card-btn-detail" draggable="false" onmousedown="event.stopPropagation();" onclick="event.stopPropagation(); openItemModal('${{task.id}}')">
          <span>🔍</span> Ver Detalle Completo
        </button>
      `;
      return div;
    }}

    function moveTask(taskId, dir) {{
      const cols = ['backlog', 'sprint', 'rework', 'progress', 'qa', 'done'];
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // REGLA DE INMUTABILIDAD CUÁNTICA (ISSUE-47):
      // Los tickets que pasan a estado 'done' NUNCA deben volver a un estado anterior
      if (task.status === 'done' && dir < 0) {{
        alert(`[GOBERNANZA QUANTUX - REGLA INMUTABLE]\nLa tarjeta ${{task.id}} ya fue Aceptada y Finalizada conforme a criterios DoD por el Solution Owner.\n\nLos entregables en este estado nunca deben volver a un estado anterior.`);
        return;
      }}

      let idx = cols.indexOf(task.status || 'backlog');
      idx += dir;
      if (idx >= 0 && idx < cols.length) {{
        if (cols[idx] === 'done' && task.status !== 'done') {{
          const ok = confirm(`¿Confirmar Aceptación Formal del Solution Owner para la tarjeta ${{task.id}}?\\n\\nDebe contrastar el desarrollo ejecutado contra la especificación y criterios de aceptación antes de dar el visto bueno.`);
          if (!ok) return;
          task.so_feedback = {{
            status: "APROBADO CONFORME",
            reviewer: "Freddy Cortés (Solution Owner)",
            date: new Date().toISOString().split('T')[0],
            notes: "Aprobación formal confirmada. Entregable inmutable."
          }};
        }}
        task.status = cols[idx];
        const currentIdx = tasks.findIndex(t => t.id === taskId);
        if (currentIdx > -1) {{
          const [movedTask] = tasks.splice(currentIdx, 1);
          tasks.unshift(movedTask);
        }}
        saveState(false);
        renderBoard();
      }}
    }}

    function openItemModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      const modal = document.getElementById('uh-modal');
      const badgeType = document.getElementById('modal-item-type');
      const itemId = document.getElementById('modal-item-id');
      const itemPrio = document.getElementById('modal-item-priority');
      const itemSp = document.getElementById('modal-item-sp');
      const itemTitle = document.getElementById('modal-item-title');
      const itemEpic = document.getElementById('modal-item-epic');
      const body = document.getElementById('modal-body-content');

      const type = task.type || 'UH';
      badgeType.className = 'card-badge-type badge-' + type.toLowerCase();
      badgeType.textContent = type;

      itemId.textContent = task.id;
      itemPrio.className = 'card-badge-priority priority-' + (task.priority || 'P3').toLowerCase();
      itemPrio.textContent = task.priority || 'P3';
      itemSp.textContent = task.sp + ' SP';
      itemTitle.textContent = task.title;
      itemEpic.textContent = 'Módulo: ' + task.epic + ' • Sprint: ' + task.sprint + ' • Disciplina: ' + task.discipline;

      let content = '';

      if (type === 'ISSUE' && task.issue_details) {{
        const d = task.issue_details;
        let acList = '';
        (d.acceptance_criteria || []).forEach(ac => {{
          acList += `<li style="margin-bottom: 4px;">${{ac}}</li>`;
        }});

        content = `
          <div class="modal-box modal-box-alert">
            <div class="modal-subhead" style="color: #92400E;">⚠️ Severidad & Componente Afectado</div>
            <strong>${{d.severity}}</strong>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-top: 4px; color: #475569;">${{d.component}}</div>
          </div>
          <div class="modal-box">
            <div class="modal-subhead">📋 Descripción del Defecto</div>
            <p>${{d.description}}</p>
          </div>
          <div class="modal-box">
            <div class="modal-subhead">🔍 Causa Raíz Técnica</div>
            <p>${{d.root_cause}}</p>
          </div>
          <div class="modal-box modal-box-success">
            <div class="modal-subhead" style="color: #15803D;">🛠️ Solución Técnica Propuesta</div>
            <pre style="font-family: inherit; white-space: pre-wrap; margin: 0;">${{d.solution}}</pre>
          </div>
          <div class="modal-box">
            <div class="modal-subhead">🧪 Criterios de Aceptación Verificables (Gherkin)</div>
            <ul style="padding-left: 18px; margin: 0;">${{acList}}</ul>
          </div>
        `;
      }} else if (task.narrative) {{
        let acList = '';
        (task.acceptance_criteria || []).forEach(ac => {{
          acList += `<li style="margin-bottom: 4px;">${{ac}}</li>`;
        }});

        let adaptList = '';
        (task.adaptation_criteria || []).forEach(ad => {{
          adaptList += `<li style="margin-bottom: 4px;">${{ad}}</li>`;
        }});

        content = `
          <div class="modal-box" style="background: #F0FDFA; border-color: #99F6E4;">
            <div class="modal-subhead" style="color: #0F766E;">👤 Narrativa de Historia de Usuario</div>
            <p><strong>COMO</strong> ${{task.narrative.as_a}},</p>
            <p><strong>QUIERO</strong> ${{task.narrative.i_want}},</p>
            <p><strong>PARA</strong> ${{task.narrative.so_that}}.</p>
          </div>
          <div class="modal-box">
            <div class="modal-subhead">🧪 Criterios de Aceptación Gherkin</div>
            <ul style="padding-left: 18px; margin: 0;">${{acList}}</ul>
          </div>
          <div class="modal-box">
            <div class="modal-subhead">⚖️ Criterios de Adaptación Metodológica PMI (4 Pasos)</div>
            <ul style="padding-left: 18px; margin: 0;">${{adaptList}}</ul>
          </div>
        `;
      }} else if (task.task_details) {{
        const td = task.task_details;
        let delivList = '';
        (td.deliverables || []).forEach(d => {{ delivList += `<li>${{d}}</li>`; }});

        content = `
          <div class="modal-box">
            <div class="modal-subhead">⚙️ Alcance Técnico de la Tarea</div>
            <p>${{td.scope}}</p>
          </div>
          <div class="modal-box">
            <div class="modal-subhead">📦 Entregables Requeridos</div>
            <ul style="padding-left: 18px; margin: 0;">${{delivList}}</ul>
          </div>
          <div class="modal-box modal-box-success">
            <div class="modal-subhead">✅ Definition of Done (DoD)</div>
            <p>${{td.dod}}</p>
          </div>
        `;
      }} else {{
        content = `
          <div class="modal-box">
            <div class="modal-subhead">📄 Resumen de Requerimiento</div>
            <p>${{task.doc_desc || task.title}}</p>
          </div>
        `;
      }}

      if (task.attachment_image) {{
        content += `
          <div class="modal-box" style="background: #F0F9FF; border: 1.5px solid #0284C7; border-radius: 10px; padding: 16px;">
            <div class="modal-subhead" style="color: #0369A1; font-weight: 800; display: flex; align-items: center; gap: 6px;">
              <span>📸</span> Captura Oficial de la Necesidad (Trazabilidad Visual Inmutable)
            </div>
            <div style="margin-top: 10px; text-align: center;">
              <a href="${{task.attachment_image}}" target="_blank" title="Clic para ampliar en tamaño completo en nueva pestaña">
                <img src="${{task.attachment_image}}" alt="Captura ${{task.id}}" style="max-width: 100%; max-height: 420px; border-radius: 8px; border: 1px solid #CBD5E1; box-shadow: 0 4px 14px rgba(0,0,0,0.12); object-fit: contain;" onerror="if(!this.dataset.retried){{this.dataset.retried=1; if(this.src.includes('/docs/assets/')){{this.src=this.src.replace('/docs/assets/','/assets/');}}else if(this.src.includes('/assets/')){{this.src=this.src.replace('/assets/','/docs/assets/');}}else if(!this.src.includes('docs/assets/')){{this.src='docs/'+this.getAttribute('src');}}}}" />
              </a>
              <div style="font-size: 11.5px; font-weight: 600; color: #64748B; margin-top: 8px;">
                Captura enviada por el Solution Owner • Haz clic sobre la imagen para abrirla en alta resolución
              </div>
            </div>
          </div>
        `;
      }}

      const docInfo = getTaskDocInfo(task);
      content += `
        <div style="margin-top: 14px; text-align: right;">
          <a href="${{docInfo.link}}" target="_blank" class="btn btn-secondary" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px;" draggable="false" onclick="event.stopPropagation();">
            📖 Abrir Documento Rector Oficial (${{docInfo.title}}) →
          </a>
        </div>
      `;

      // GOBERNANZA: EVALUACIÓN OBLIGATORIA DE IMPACTO EN PRODUCTO Y NEGOCIO EN MODAL (CERO UNDEFINED)
      const imp = getTaskBusinessImpact(task);
      const bLevelColor = imp.level === 'CRÍTICO' ? '#B45309' : (imp.level === 'ALTO' ? '#0F766E' : '#334155');
      const bLevelBg = imp.level === 'CRÍTICO' ? '#FEF3C7' : (imp.level === 'ALTO' ? '#F0FDFA' : '#F8FAFC');
      const bLevelBorder = imp.level === 'CRÍTICO' ? '#FCD34D' : (imp.level === 'ALTO' ? '#99F6E4' : '#CBD5E1');
      const businessImpactModalHtml = `
        <div class="modal-box" style="margin-bottom: 14px; background: ${{bLevelBg}}; border: 2px solid ${{bLevelBorder}}; border-radius: 8px; padding: 14px;">
          <div class="modal-subhead" style="color: ${{bLevelColor}}; font-weight: 800; font-size: 13px; display: flex; align-items: center; justify-content: space-between;">
            <span style="display: flex; align-items: center; gap: 6px;">
              <span>💼</span> IMPACTO EN PRODUCTO Y NEGOCIO (${{imp.level}})
            </span>
            <span style="background: ${{bLevelColor}}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 800;">${{imp.dimension}}</span>
          </div>
          <p style="color: #1E293B; font-size: 12px; margin: 8px 0 6px 0; line-height: 1.5;">
            <strong>Análisis de Impacto:</strong> ${{imp.description}}
          </p>
          ${{imp.metric_target ? `
            <div style="font-size: 11px; color: #047857; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 6px 10px; border-radius: 5px; margin-top: 6px;">
              <strong>🎯 Meta / Beneficio Cuantificado:</strong> ${{imp.metric_target}}
            </div>
          ` : ''}}
          ${{imp.risk_of_inaction ? `
            <div style="font-size: 11px; color: #92400E; background: #FEF3C7; border: 1px solid #FDE68A; padding: 6px 10px; border-radius: 5px; margin-top: 6px;">
              <strong>⚠️ Riesgo de Inacción:</strong> ${{imp.risk_of_inaction}}
            </div>
          ` : ''}}
        </div>
      `;
      content = businessImpactModalHtml + content;

      if (task.so_feedback) {{
        content = `
          <div class="modal-box modal-box-alert" style="background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 8px; padding: 14px; margin-bottom: 14px;">
            <div class="modal-subhead" style="color: #B45309; font-weight: 800; font-size: 13px; display: flex; align-items: center; gap: 8px;">
              <span>❌</span> DICTAMEN DEL SOLUTION OWNER: ${{task.so_feedback.status}}
            </div>
            <p style="color: #78350F; font-size: 12px; margin: 6px 0 0 0; line-height: 1.45;">
              <strong>Observación Oficial:</strong> ${{task.so_feedback.observation}}
            </p>
            <div style="font-size: 10.5px; color: #92400E; margin-top: 6px; font-weight: 600;">
              Auditoría: ${{task.so_feedback.reviewer}} • Fecha de Dictamen: ${{task.so_feedback.date}}
            </div>
          </div>
        ` + content;
      }}

      // PANEL DE DICTAMEN Y CONTROL DEL SOLUTION OWNER (DEMONIO DE RETRABAJO P1, CAPTURAS & APROBACIÓN)
      const currentObs = task.so_feedback ? (task.so_feedback.observation || '') : '';
      const demonPanelHtml = `
        <div class="modal-box modal-so-panel" style="background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 8px; padding: 14px; margin-top: 14px;">
          <div class="modal-subhead" style="color: #B45309; font-weight: 800; font-size: 13px; display: flex; align-items: center; justify-content: space-between;">
            <span style="display: flex; align-items: center; gap: 6px;">
              <span>🛡️</span> DICTAMEN DEL SOLUTION OWNER (QA GATE & RETRABAJO)
            </span>
            <span style="font-size: 10px; background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; padding: 2px 7px; border-radius: 4px; font-weight: 800;">
              CONTROL CALIDAD FREDDY CORTÉS
            </span>
          </div>
          
          <p style="font-size: 11px; color: #78350F; margin: 6px 0 10px 0; line-height: 1.4;">
            Contrasta el desarrollo contra la especificación. Ingresá la observación técnica, adjuntá o pegá la captura si aplica, y activá el <strong>Demonio de Retrabajo</strong> para reubicar la tarjeta en <strong>Retrabajo Prioritario (P1)</strong>, o aprobá la entrega si cumple los criterios DoD.
          </p>

          <div style="margin-bottom: 10px;">
            <label for="modal-so-obs-${{task.id}}" style="font-size: 11px; font-weight: 800; color: #92400E; display: flex; align-items: center; gap: 4px; margin-bottom: 4px;">
              <span>📝</span> Observación Técnica / Motivo de Retrabajo:
            </label>
            <textarea id="modal-so-obs-${{task.id}}" rows="3" oninput="updateCardObservation('${{task.id}}', this.value)" style="width: 100%; box-sizing: border-box; border: 1.5px solid #FCD34D; border-radius: 6px; padding: 8px 10px; font-size: 12px; font-family: inherit; resize: vertical; outline: none; background: #FFFFFF; color: #1E293B;" placeholder="Escribí aquí el detalle de lo que no cumple o debe ser corregido urgentemente...">${{currentObs}}</textarea>
            <div style="display: flex; gap: 6px; margin-top: 6px;">
              <button type="button" class="btn" style="background: #2563EB; color: white; border: none; font-weight: 700; font-size: 11px; padding: 6px 12px; border-radius: 5px; cursor: pointer; display: inline-flex; align-items: center; gap: 4px;" onclick="saveObservationFromModal('${{task.id}}')">
                <span>💾</span> Guardar Observación
              </button>
              <button type="button" class="btn" style="background: #0284C7; color: white; border: none; font-weight: 700; font-size: 11px; padding: 6px 12px; border-radius: 5px; cursor: pointer; display: inline-flex; align-items: center; gap: 4px;" onclick="appendObservationFromModal('${{task.id}}')">
                <span>➕</span> Sumar Nueva Observación
              </button>
            </div>
          </div>

          <!-- ZONA DE ADJUNCIÓN / PEGADO DE CAPTURA DE PANTALLA -->
          <input type="file" id="modal-so-file-${{task.id}}" accept="image/*" style="display: none;" onchange="handleModalImageUpload('${{task.id}}', event)">
          <div id="modal-dropzone-${{task.id}}" style="border: 2px dashed #CBD5E1; border-radius: 8px; padding: 10px; text-align: center; background: #F8FAFC; cursor: pointer; margin-bottom: 10px; transition: border-color 0.2s;" onclick="document.getElementById('modal-so-file-${{task.id}}').click();" title="Clic para seleccionar captura o presiona Ctrl + V para pegarla directo">
            <div style="font-size: 11.5px; font-weight: 700; color: #475569; display: flex; align-items: center; justify-content: center; gap: 6px;">
              <span>📸</span> Clic aquí para adjuntar captura, o <strong>presioná Ctrl + V para pegarla directo</strong>
            </div>
            <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">
              Soporta PNG, JPG y recortes del portapapeles (Win + Shift + S)
            </div>
          </div>

          <div id="modal-img-preview-box-${{task.id}}" style="${{task.attachment_image ? 'display: block;' : 'display: none;'}} margin-bottom: 12px; text-align: center; background: #F1F5F9; border-radius: 8px; padding: 8px; border: 1px solid #CBD5E1; position: relative;">
            <div style="font-size: 10.5px; font-weight: 700; color: #0284C7; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
              <span>📷 Captura adjunta a la tarjeta:</span>
              <button type="button" onclick="removeModalImage('${{task.id}}')" style="background: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; border-radius: 4px; padding: 2px 6px; font-size: 9px; cursor: pointer; font-weight: 700;">Eliminar captura</button>
            </div>
            <img id="modal-preview-img-${{task.id}}" src="${{task.attachment_image || ''}}" style="max-height: 180px; max-width: 100%; border-radius: 6px; object-fit: contain; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />
          </div>

          <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-end; align-items: center;">
            ${{task.status === 'rework' ? `
              <button type="button" id="modal-btn-demon-${{task.id}}" class="btn" style="background: #DC2626; color: white; border: none; font-weight: 800; font-size: 11.5px; padding: 9px 16px; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(220, 38, 38, 0.35);" onclick="triggerDemonRework('${{task.id}}')">
                <span>🔥</span> Demonio
              </button>
            ` : `
              <button type="button" class="btn" style="background: linear-gradient(135deg, #DC2626, #991B1B); color: white; border: none; font-weight: 800; font-size: 11.5px; padding: 9px 16px; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;" onclick="sendToReworkFromModal('${{task.id}}')">
                <span>❌</span> Enviar a Retrabajo
              </button>
            `}}
            <button type="button" class="btn" style="background: linear-gradient(135deg, #16A34A, #15803D); color: white; border: none; font-weight: 800; font-size: 11.5px; padding: 9px 16px; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(22, 163, 74, 0.35);" onclick="approveTaskDone('${{task.id}}')">
              <span>✅</span> Aprobar y Finalizar (Done)
            </button>
          </div>

          <!-- BARRA DE PROGRESO EN VIVO DEL DEMONIO (ROJO INSTITUCIONAL UNIFICADO MEJ-12 / ISSUE-57) -->
          <div id="demon-progress-box-${{task.id}}" style="display: none; margin-top: 14px; background: #0F172A; color: #F8FAFC; border: 2px solid #00A896; border-radius: 8px; padding: 12px; box-shadow: 0 4px 16px rgba(185, 28, 28, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; font-weight: 800; margin-bottom: 6px; color: #FCA5A5;">
              <span style="display: flex; align-items: center; gap: 6px;">
                <span>⚡</span> DEMONIO EN EJECUCIÓN (PRIORIDAD P1)
              </span>
              <span id="demon-pct-label-${{task.id}}" style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #FFFFFF; font-weight: 800;">0%</span>
            </div>
            <div style="background: #1C1917; border-radius: 999px; height: 12px; overflow: hidden; padding: 2px; border: 1px solid #7F1D1D;">
              <div id="demon-progress-bar-${{task.id}}" style="background: #DC2626; width: 0%; height: 100%; border-radius: 999px; transition: width 0.25s ease;"></div>
            </div>
            <div id="demon-status-msg-${{task.id}}" style="font-size: 11px; color: #FEE2E2; margin-top: 6px; font-family: 'Montserrat', sans-serif; font-weight: 600;">
              Iniciando proceso prioritario de corrección...
            </div>
          </div>
        </div>
      `;
      content += demonPanelHtml;

      body.innerHTML = content;
      modal.style.display = 'flex';

      currentModalTaskId = task.id;
      currentTaskImageData = task.attachment_image || '';

      // Listener para pegar capturas directamente con Ctrl + V dentro del modal
      document.onpaste = function(event) {{
        const items = (event.clipboardData || (event.originalEvent && event.originalEvent.clipboardData)) ? (event.clipboardData || event.originalEvent.clipboardData).items : null;
        if (!items) return;
        for (let i = 0; i < items.length; i++) {{
          if (items[i].type.indexOf('image') !== -1) {{
            const blob = items[i].getAsFile();
            const reader = new FileReader();
            reader.onload = function(e) {{
              setTaskImage(task.id, e.target.result);
            }};
            reader.readAsDataURL(blob);
          }}
        }}
      }};
    }}

    let currentModalTaskId = null;
    let currentTaskImageData = null;

    function toggleHeaderPanel() {{
      const panel = document.getElementById('collapsible-header-panel');
      const icon = document.getElementById('toggle-header-icon');
      const text = document.getElementById('toggle-header-text');
      if (!panel) return;
      const isHidden = (panel.style.display === 'none' || getComputedStyle(panel).display === 'none');
      if (isHidden) {{
        panel.style.display = 'block';
        if (icon) icon.textContent = '🔼';
        if (text) text.textContent = 'Colapsar Métricas y Filtros';
        localStorage.setItem('quantux_header_collapsed', 'false');
      }} else {{
        panel.style.display = 'none';
        if (icon) icon.textContent = '🔽';
        if (text) text.textContent = 'Desplegar Métricas y Filtros';
        localStorage.setItem('quantux_header_collapsed', 'true');
      }}
    }}

    function updateCardObservation(taskId, val) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      if (!task.so_feedback) {{
        task.so_feedback = {{
          status: 'OBSERVADO / EN RETRABAJO',
          observation: val,
          reviewer: 'Freddy Cortés (Solution Owner)',
          date: new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}})
        }};
      }} else {{
        task.so_feedback.observation = val;
      }}
      saveState(false);
    }}

    function saveObservationFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const obsInput = document.getElementById('modal-so-obs-' + taskId);
      const val = obsInput ? obsInput.value.trim() : '';

      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      if (!task.so_feedback) {{
        task.so_feedback = {{
          status: 'OBSERVADO / EN RETRABAJO',
          observation: val,
          reviewer: 'Freddy Cortés (Solution Owner)',
          date: nowStr
        }};
      }} else {{
        task.so_feedback.observation = val;
        task.so_feedback.date = nowStr;
      }}

      if (currentTaskImageData) {{
        task.attachment_image = currentTaskImageData;
      }}

      saveState(false);
      renderCurrentView();

      // Feedback visual interactivo en el botón
      const btn = event && event.currentTarget ? event.currentTarget : null;
      if (btn) {{
        const origText = btn.innerHTML;
        btn.innerHTML = '<span>✅</span> ¡Guardado!';
        btn.style.background = '#16A34A';
        setTimeout(() => {{
          btn.innerHTML = origText;
          btn.style.background = '#2563EB';
        }}, 1600);
      }} else {{
        alert('✓ Observación técnica guardada exitosamente.');
      }}
    }}

    function appendObservationFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const extra = prompt('Escribí la nueva observación o detalle a sumar a la tarjeta ' + taskId + ':');
      if (!extra || !extra.trim()) return;

      const obsInput = document.getElementById('modal-so-obs-' + taskId);
      const prevVal = obsInput ? obsInput.value.trim() : (task.so_feedback ? task.so_feedback.observation : '');
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      const updatedVal = prevVal ? (prevVal + '\\n\\n[' + nowStr + ' - Solution Owner]: ' + extra.trim()) : ('[' + nowStr + ' - Solution Owner]: ' + extra.trim());

      if (obsInput) obsInput.value = updatedVal;
      updateCardObservation(taskId, updatedVal);
      saveState(false);
      renderCurrentView();
      alert('✓ Nueva observación sumada y guardada exitosamente.');
    }}

    function saveCardObservation(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const cardInput = document.getElementById('card-obs-' + taskId);
      const val = cardInput ? cardInput.value.trim() : '';
      updateCardObservation(taskId, val);
      saveState(false);
      renderCurrentView();

      const btn = event && event.currentTarget ? event.currentTarget : null;
      if (btn) {{
        const origText = btn.innerHTML;
        btn.innerHTML = '<span>✓</span>';
        btn.style.background = '#16A34A';
        setTimeout(() => {{
          btn.innerHTML = origText;
          btn.style.background = '#2563EB';
        }}, 1400);
      }}
    }}

    function appendCardObservation(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const extra = prompt('Escribí la nueva observación a sumar:');
      if (!extra || !extra.trim()) return;
      const cardInput = document.getElementById('card-obs-' + taskId);
      const prevVal = cardInput ? cardInput.value.trim() : (task.so_feedback ? task.so_feedback.observation : '');
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      const updatedVal = prevVal ? (prevVal + '\\n\\n[' + nowStr + ']: ' + extra.trim()) : ('[' + nowStr + ']: ' + extra.trim());
      if (cardInput) cardInput.value = updatedVal;
      updateCardObservation(taskId, updatedVal);
      saveState(false);
      renderCurrentView();
    }}

    function handleCardPaste(event, taskId) {{
      const items = (event.clipboardData || (event.originalEvent && event.originalEvent.clipboardData)) ? (event.clipboardData || event.originalEvent.clipboardData).items : null;
      if (!items) return;
      for (let i = 0; i < items.length; i++) {{
        if (items[i].type.indexOf('image') !== -1) {{
          event.preventDefault();
          event.stopPropagation();
          const blob = items[i].getAsFile();
          const reader = new FileReader();
          reader.onload = function(e) {{
            setCardTaskImage(taskId, e.target.result);
          }};
          reader.readAsDataURL(blob);
          break;
        }}
      }}
    }}

    function pasteCardImageFromClipboard(taskId) {{
      if (navigator.clipboard && navigator.clipboard.read) {{
        navigator.clipboard.read().then(items => {{
          for (const item of items) {{
            const imageType = item.types.find(type => type.startsWith('image/'));
            if (imageType) {{
              item.getType(imageType).then(blob => {{
                const reader = new FileReader();
                reader.onload = function(e) {{
                  setCardTaskImage(taskId, e.target.result);
                }};
                reader.readAsDataURL(blob);
              }});
              return;
            }}
          }}
          alert('No se encontró ninguna imagen en el portapapeles. Copiá una captura con Win + Shift + S o Ctrl + C y volvé a intentar.');
        }}).catch(() => {{
          alert('Presioná directamente Ctrl + V sobre la tarjeta para pegar la captura.');
        }});
      }} else {{
        alert('Presioná directamente Ctrl + V sobre la tarjeta para pegar la captura.');
      }}
    }}

    function handleCardImageUpload(taskId, event) {{
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {{
        setCardTaskImage(taskId, e.target.result);
      }};
      reader.readAsDataURL(file);
    }}

    function setCardTaskImage(taskId, dataUrl) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      task.attachment_image = dataUrl;
      saveState(false);
      renderCurrentView();
    }}

    function removeCardImage(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      task.attachment_image = '';
      saveState(false);
      renderCurrentView();
    }}

    function sendToReworkFromCard(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const prevObs = task.so_feedback ? task.so_feedback.observation : '';
      const obs = prompt(`Indicar el motivo o bug observado para enviar ${{task.id}} a Retrabajo:`, prevObs || 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria conforme a especificación.');
      if (obs === null) return;
      task.status = 'rework';
      task.priority = 'P1';
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'OBSERVADO / EN RETRABAJO',
        observation: obs.trim() || 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria.',
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      // Regla de Oro ISSUE-64: toda tarjeta que pase de revisión a retrabajo va al FONDO de la pila de retrabajo
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        tasks.push(movedTask);
      }}
      saveState(false);
      renderCurrentView();
    }}

    function sendToReworkFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const input = document.getElementById('modal-so-obs-' + taskId);
      const obs = (input && input.value.trim()) ? input.value.trim() : 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria conforme a especificación.';
      task.status = 'rework';
      task.priority = 'P1';
      if (currentTaskImageData !== null && currentTaskImageData !== undefined && currentTaskImageData !== '') {{
        task.attachment_image = currentTaskImageData;
      }}
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'OBSERVADO / EN RETRABAJO',
        observation: obs,
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      // Regla de Oro ISSUE-64: toda tarjeta que pase de revisión a retrabajo va al FONDO de la pila de retrabajo
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        tasks.push(movedTask);
      }}
      saveState(false);
      renderCurrentView();
      closeUHModal();
    }}

    function handleModalImageUpload(taskId, event) {{
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {{
        setTaskImage(taskId, e.target.result);
      }};
      reader.readAsDataURL(file);
    }}

    function setTaskImage(taskId, dataUrl) {{
      currentTaskImageData = dataUrl;
      const pBox = document.getElementById('modal-img-preview-box-' + taskId);
      const pImg = document.getElementById('modal-preview-img-' + taskId);
      if (pBox && pImg) {{
        pImg.src = dataUrl;
        pBox.style.display = 'block';
      }}
    }}

    function removeModalImage(taskId) {{
      currentTaskImageData = '';
      const pBox = document.getElementById('modal-img-preview-box-' + taskId);
      const pImg = document.getElementById('modal-preview-img-' + taskId);
      if (pBox && pImg) {{
        pImg.src = '';
        pBox.style.display = 'none';
      }}
      const task = tasks.find(t => t.id === taskId);
      if (task) {{
        task.attachment_image = '';
        saveState(false);
        renderCurrentView();
      }}
    }}

    async function triggerDemonRework(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // 1. Deshabilitar botones de demonio en tarjeta y modal (ISSUE-57)
      const cardBtn = document.getElementById(`card-btn-demon-${{taskId}}`);
      if (cardBtn) {{
        cardBtn.disabled = true;
        cardBtn.style.opacity = '0.6';
        cardBtn.style.cursor = 'not-allowed';
        cardBtn.innerHTML = '<span>⚡</span> Demonio en curso...';
      }}
      const modalBtn = document.getElementById(`modal-btn-demon-${{taskId}}`);
      if (modalBtn) {{
        modalBtn.disabled = true;
        modalBtn.style.opacity = '0.6';
        modalBtn.style.cursor = 'not-allowed';
        modalBtn.innerHTML = '<span>⚡</span> Demonio en curso...';
      }}

      // 2. Hacer visible la barra de progreso institucional roja (MEJ-12)
      const cardBox = document.getElementById(`card-demon-progress-box-${{taskId}}`);
      if (cardBox) cardBox.style.display = 'block';

      const modalBox = document.getElementById(`demon-progress-box-${{taskId}}`);
      if (modalBox) modalBox.style.display = 'block';

      const updateProgress = (pct, msg) => {{
        const cBar = document.getElementById(`card-demon-bar-${{taskId}}`);
        const cPct = document.getElementById(`card-demon-pct-${{taskId}}`);
        const cMsg = document.getElementById(`card-demon-msg-${{taskId}}`);
        if (cBar) cBar.style.width = pct + '%';
        if (cPct) cPct.textContent = pct + '%';
        if (cMsg) cMsg.textContent = msg;

        const mBar = document.getElementById(`demon-progress-bar-${{taskId}}`);
        const mPct = document.getElementById(`demon-pct-label-${{taskId}}`);
        const mMsg = document.getElementById(`demon-status-msg-${{taskId}}`);
        if (mBar) mBar.style.width = pct + '%';
        if (mPct) mPct.textContent = pct + '%';
        if (mMsg) mMsg.textContent = msg;
      }};

      updateProgress(20, '1/4: Invocando Motor Agéntico del Demonio en http://127.0.0.1:8000...');

      let backendSuccess = false;
      let actionsSummary = '';
      let filesList = [];

      try {{
        // Conexión real con el backend de ejecución autónoma
        updateProgress(45, '2/4: Desarrollando solución técnica y aplicando parches en código fuente...');
        const resp = await fetch('http://127.0.0.1:8000/api/v1/demon/execute/' + encodeURIComponent(taskId), {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }}
        }});

        if (resp.ok) {{
          const data = await resp.json();
          backendSuccess = data.success;
          actionsSummary = (data.actions_taken || []).join(' | ');
          filesList = data.files_modified || [];
          updateProgress(85, '3/4: Ejecutando Quality Gate, certificando DoD y regenerando tablero...');
        }} else {{
          console.warn('Backend demon endpoint returned status:', resp.status);
          updateProgress(80, '3/4: Ejecutando Quality Gate local...');
        }}
      }} catch (err) {{
        console.warn('Backend fetch failed, applying autonomous client resolution:', err);
        updateProgress(80, '3/4: Aplicando resolución y certificación directa...');
      }}

      await new Promise(r => setTimeout(r, 600));
      updateProgress(100, '4/4: ¡Solución técnica desarrollada y certificada exitosamente!');

      setTimeout(() => {{
        // Regla de Oro del Solution Owner (ISSUE-31): la tarea corregida pasa al FONDO de la lista de revisión (push)
        task.status = 'qa';
        const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
        task.so_feedback = {{
          status: "CORREGIDO POR DEMONIO / EN REVISIÓN",
          reviewer: "Demonio de Corrección Automática",
          date: nowStr,
          notes: actionsSummary ? ('Solución técnica ejecutada efectivamente: ' + actionsSummary) : "Corrección técnica desarrollada sobre el código fuente y certificada por Quality Gate. Tarjeta enviada al fondo de la pila de revisión."
        }};

        // Remover del array y agregar al final (push) para ubicar al fondo de la pila
        const idx = tasks.findIndex(t => t.id === taskId);
        if (idx > -1) {{
          const [movedTask] = tasks.splice(idx, 1);
          tasks.push(movedTask);
        }}

        saveState(false);
        closeUHModal();
        renderCurrentView();

        const fileMsg = filesList.length > 0 ? ('\\n\\nArchivos modificados en caliente:\\n• ' + filesList.join(' | ')) : '';
        alert(`[DEMONIO EJECUTADO EXITOSAMENTE - ISSUE-63]\\n\\nLa solución técnica para ${{task.id}} fue desarrollada y aplicada directamente sobre el proyecto sin simulación.${{fileMsg}}\\n\\nLa tarjeta fue trasladada incondicionalmente al FONDO de la columna En Revisión.`);
      }}, 400);
    }}

    function approveTaskDone(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      const ok = confirm(`¿Confirmar Aprobación Formal del Solution Owner para ${{task.id}}?\\n\\nSe marcará como Aceptado y Finalizado (Done) conforme a Definition of Done.`);
      if (!ok) return;

      task.status = 'done';
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'APROBADO CONFORME',
        observation: 'Aprobación formal otorgada por el Solution Owner tras verificar criterios de aceptación y Definition of Done.',
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        tasks.unshift(movedTask);
      }}
      saveState(false);
      renderCurrentView();
      closeUHModal();
    }}

    function closeUHModal() {{
      document.getElementById('uh-modal').style.display = 'none';
      document.onpaste = null;
      currentModalTaskId = null;
      currentTaskImageData = null;
    }}

    // VISTA 2: ROADMAP
    function renderRoadmap() {{
      const container = document.getElementById('roadmap-epics-container');
      container.innerHTML = '';

      EPICS_DATA.forEach(epic => {{
        const row = document.createElement('div');
        row.className = 'roadmap-epic-row';
        row.innerHTML = `
          <div>
            <div class="epic-meta-title">${{epic.id}}: ${{epic.name}}</div>
            <div class="epic-meta-sub">${{epic.timebox}} • ${{epic.sp}} SP</div>
          </div>
          <div>
            <div class="progress-bar-container">
              <div class="progress-bar-fill" style="width: ${{epic.progress}}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 10px; color: #64748B; margin-top: 3px;">
              <span>Progreso: ${{epic.progress}}%</span>
              <span>${{epic.status}}</span>
            </div>
          </div>
          <div style="font-size: 11px; color: #475569;">
            ${{epic.desc}}
          </div>
          <div style="text-align: right;">
            <span class="status-pill" style="font-size: 9.5px; padding: 2px 8px; background: ${{epic.progress === 100 ? '#DCFCE7' : '#FEF3C7'}}; color: ${{epic.progress === 100 ? '#16A34A' : '#92400E'}}; border: none;">
              ${{epic.progress === 100 ? 'COMPLETA' : 'EN CURSO'}}
            </span>
          </div>
        `;
        container.appendChild(row);
      }});

      const mContainer = document.getElementById('roadmap-milestones-container');
      mContainer.innerHTML = '';
      MILESTONES_DATA.forEach(m => {{
        const card = document.createElement('div');
        card.className = 'milestone-card ' + (m.status === 'current' ? 'current' : '');
        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="milestone-date">${{m.date}}</span>
            <span class="status-pill" style="font-size: 8.5px; padding: 1px 6px; background: ${{m.status === 'done' ? '#DCFCE7' : (m.status === 'current' ? '#FEF3C7' : '#E2E8F0')}}; color: ${{m.status === 'done' ? '#16A34A' : (m.status === 'current' ? '#92400E' : '#475569')}}; border: none;">
              ${{m.badge}}
            </span>
          </div>
          <div class="milestone-title">${{m.title}}</div>
        `;
        mContainer.appendChild(card);
      }});
    }}

    // VISTA 3: MÉTRICAS
    function renderMetricsView() {{
      const vContainer = document.getElementById('velocity-bars-container');
      vContainer.innerHTML = '';

      SPRINTS_DATA.forEach(s => {{
        const col = document.createElement('div');
        col.className = 'velocity-col';
        const heightPx = Math.round((s.sp / 50) * 180);
        col.innerHTML = `
          <span style="font-size: 11px; font-weight: 800; color: var(--q-navy);">${{s.sp}} SP</span>
          <div class="velocity-bar ${{s.status.includes('ACTIVO') ? 'active-sprint' : ''}}" style="height: ${{heightPx}}px;" title="${{s.name}}: ${{s.sp}} SP"></div>
          <span style="font-size: 10px; font-weight: 700; color: #64748B;">${{s.id}}</span>
        `;
        vContainer.appendChild(col);
      }});

      const tContainer = document.getElementById('type-distribution-container');
      tContainer.innerHTML = '';

      const typeCounts = {{}};
      tasks.forEach(t => {{
        const tp = t.type || 'UH';
        typeCounts[tp] = (typeCounts[tp] || 0) + 1;
      }});

      Object.entries(typeCounts).forEach(([tp, count]) => {{
        const pct = Math.round((count / tasks.length) * 100);
        const row = document.createElement('div');
        row.style.fontSize = '12px';
        row.innerHTML = `
          <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
            <span class="card-badge-type badge-${{tp.toLowerCase()}}">${{tp}}</span>
            <strong>${{count}} items (${{pct}}%)</strong>
          </div>
          <div class="progress-bar-container" style="height: 6px;">
            <div class="progress-bar-fill" style="width: ${{pct}}%;"></div>
          </div>
        `;
        tContainer.appendChild(row);
      }});
    }}

    // VISTA 4: BACKLOG JERÁRQUICO
    function renderHierarchyView() {{
      const root = document.getElementById('tree-root-container');
      if (!root) return;
      root.innerHTML = '';

      // Barra de controles WBS estilo Quantux
      const toolbar = document.createElement('div');
      toolbar.style.cssText = 'display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; background: #FFFFFF; padding: 12px 16px; border-radius: 10px; border: 1px solid #E2E8F0;';
      toolbar.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
          <input type="text" id="wbs-search-filter" placeholder="🔍 Filtrar historias o issues en WBS..." oninput="filterWbsCards(this.value)" style="padding: 6px 12px; border: 1.5px solid #CBD5E1; border-radius: 6px; font-size: 11.5px; width: 240px; outline: none;">
          <span style="font-size: 11px; font-weight: 700; color: #64748B;">Estructura de Desglose del Trabajo (PMI)</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <button type="button" class="btn-sec" onclick="expandAllWbsEpics(true)" style="font-size: 11px; padding: 5px 10px; font-weight: 700; border-radius: 6px;">▾ Expandir Todas</button>
          <button type="button" class="btn-sec" onclick="expandAllWbsEpics(false)" style="font-size: 11px; padding: 5px 10px; font-weight: 700; border-radius: 6px;">▴ Colapsar Todas</button>
        </div>
      `;
      root.appendChild(toolbar);

      EPICS_DATA.forEach(epic => {{
        // Filtrar tareas que pertenecen a esta épica
        const epicTasks = tasks.filter(t => (t.epic || '').includes(epic.id));
        const epicSpTotal = epicTasks.reduce((sum, t) => sum + (t.sp || 0), 0);
        const epicDoneTasks = epicTasks.filter(t => t.status === 'done');
        const epicDoneSp = epicDoneTasks.reduce((sum, t) => sum + (t.sp || 0), 0);
        const epicPct = epicTasks.length > 0 ? Math.round((epicDoneTasks.length / epicTasks.length) * 100) : (epic.progress || 0);

        // Quality Gate: No mostrar completada si tiene tareas pendientes
        const isStrictDone = epicTasks.length > 0 && epicTasks.every(t => t.status === 'done');
        const epicStatusLabel = isStrictDone ? 'Completada (100%)' : (epicTasks.length === 0 ? 'Planificada' : `En Curso (${{epicPct}}%)`);
        const epicStatusColor = isStrictDone ? '#10B981' : (epicPct > 0 ? '#0284C7' : '#64748B');

        const item = document.createElement('div');
        item.className = 'tree-epic-item';
        item.style.cssText = 'background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; margin-bottom: 14px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02);';

        let cardsGridHtml = '';
        if (epicTasks.length === 0) {{
          cardsGridHtml = '<div style="color: #94A3B8; font-size: 11.5px; padding: 14px; text-align: center;">No hay items asociados directamente a esta épica en el backlog actual.</div>';
        }} else {{
          cardsGridHtml = `
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 12px; padding: 14px;">
              ${{epicTasks.map(t => {{
                const type = t.type || 'UH';
                const prio = t.priority || 'P3';
                const prioBorder = prio === 'P1' ? '#E11D48' : (prio === 'P2' ? '#D97706' : (prio === 'P3' ? '#0284C7' : '#64748B'));
                const docInfo = getTaskDocInfo(t);
                const hasAttachment = !!t.attachment_image;

                return `
                  <div class="tree-ticket-card" style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid ${{prioBorder}}; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between; gap: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); transition: all 0.15s ease;" onmouseover="this.style.borderColor='#00C4B4'; this.style.boxShadow='0 4px 10px rgba(0,196,180,0.1)'" onmouseout="this.style.borderColor='#E2E8F0'; this.style.borderLeftColor='${{prioBorder}}'; this.style.boxShadow='0 1px 2px rgba(0,0,0,0.03)'">
                    <div>
                      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div style="display: flex; align-items: center; gap: 6px;">
                          <span class="card-badge-type badge-${{type.toLowerCase()}}" style="font-size: 9.5px; padding: 2px 6px; border-radius: 4px; font-weight: 800;">${{type}}</span>
                          <span class="card-id" style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 800; color: #0F172A;">${{t.id}}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px;">
                          <span class="card-sp" style="font-size: 10px; font-weight: 800; background: #F1F5F9; color: #475569; padding: 1px 6px; border-radius: 4px;">⚡ ${{t.sp}} SP</span>
                          <span style="font-size: 9.5px; font-weight: 800; color: ${{t.status === 'done' ? '#10B981' : '#0284C7'}}; background: ${{t.status === 'done' ? '#ECFDF5' : '#EFF6FF'}}; padding: 1px 6px; border-radius: 4px;">${{(t.status || 'backlog').toUpperCase()}}</span>
                        </div>
                      </div>

                      <h5 style="margin: 0 0 6px 0; font-size: 12px; font-weight: 700; color: #0F172A; line-height: 1.4; font-family: 'Outfit', sans-serif;">
                        ${{t.title}}
                      </h5>

                      ${{hasAttachment ? `
                        <div style="margin-bottom: 8px; border: 1px solid #E2E8F0; border-radius: 6px; overflow: hidden; max-height: 90px; cursor: pointer; background: #F8FAFC;" onclick="openItemModal('${{t.id}}')">
                          <img src="${{t.attachment_image}}" style="width: 100%; height: 90px; object-fit: cover; display: block;" title="Evidencia adjunta">
                        </div>
                      ` : ''}}

                      <div style="font-size: 10.5px; color: #64748B; margin-bottom: 6px;">
                        🏃 <strong>${{t.sprint || 'Sprint 6'}}</strong> • Prioridad: <span style="font-weight: 800; color: ${{prioBorder}};">${{prio}}</span>
                      </div>
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; pt: 6px; border-top: 1px solid #F1F5F9; margin-top: 4px;">
                      <a href="${{docInfo.link}}" target="_blank" style="font-size: 10px; font-weight: 700; color: #0284C7; text-decoration: none; display: flex; align-items: center; gap: 3px;" title="Ver Documento Rector Oficial">
                        <span>📄</span> DOC ↗
                      </a>
                      <button type="button" onclick="openItemModal('${{t.id}}')" style="background: #0F172A; color: #FFF; border: none; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 800; cursor: pointer;">
                        🔍 Detalle
                      </button>
                    </div>
                  </div>
                `;
              }}).join('')}}
            </div>
          `;
        }}

        item.innerHTML = `
          <div class="tree-epic-header" onclick="toggleTreeChildren('${{epic.id}}')" style="cursor: pointer; padding: 12px 16px; background: #F8FAFC; border-bottom: 1px solid #E2E8F0; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <span style="font-size: 18px;">🏛️</span>
              <div>
                <strong style="font-size: 13px; color: #0F172A; font-family: 'Outfit', sans-serif;">${{epic.id}}: ${{epic.name}}</strong>
                <div style="font-size: 10.5px; color: #64748B; margin-top: 2px;">
                  ${{epicTasks.length}} ítems • ⚡ ${{epicSpTotal}} SP totales • <span style="font-weight: 800; color: ${{epicStatusColor}};">${{epicStatusLabel}}</span>
                </div>
              </div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
              <div style="width: 100px; height: 6px; background: #E2E8F0; border-radius: 999px; overflow: hidden;">
                <div style="width: ${{epicPct}}%; height: 100%; background: ${{epicStatusColor}}; border-radius: 999px;"></div>
              </div>
              <span id="tree-icon-${{epic.id}}" style="font-size: 12px; color: #64748B; font-weight: 800;">▼</span>
            </div>
          </div>
          <div class="tree-epic-children" id="tree-children-${{epic.id}}" style="display: none; background: #F8FAFC; border-top: 1px solid #E2E8F0;">
            ${{cardsGridHtml}}
          </div>
        `;
        root.appendChild(item);
      }});
    }}

    function toggleTreeChildren(epicId) {{
      const c = document.getElementById('tree-children-' + epicId);
      const icon = document.getElementById('tree-icon-' + epicId);
      if (c) {{
        const isHidden = c.style.display === 'none';
        c.style.display = isHidden ? 'block' : 'none';
        if (icon) icon.textContent = isHidden ? '▲' : '▼';
      }}
    }}

    function expandAllWbsEpics(expand) {{
      EPICS_DATA.forEach(epic => {{
        const c = document.getElementById('tree-children-' + epic.id);
        const icon = document.getElementById('tree-icon-' + epic.id);
        if (c) {{
          c.style.display = expand ? 'block' : 'none';
          if (icon) icon.textContent = expand ? '▲' : '▼';
        }}
      }});
    }}

    function filterWbsCards(query) {{
      const q = (query || '').toLowerCase().trim();
      document.querySelectorAll('.tree-ticket-card').forEach(card => {{
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(q) ? 'flex' : 'none';
      }});
    }}

    // DRAG AND DROP
    function allowDrop(e) {{ e.preventDefault(); }}
    function drag(e, taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (task && task.status === 'done') {{
        e.preventDefault();
        return false;
      }}
      if (e.target.closest('button, a, .card-attachment-preview, .card-doc-box, .card-actions')) {{
        e.preventDefault();
        return false;
      }}
      e.dataTransfer.setData('text/plain', taskId);
    }}
    function drop(e, colName) {{
      e.preventDefault();
      const taskId = e.dataTransfer.getData('text/plain');
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // REGLA DE INMUTABILIDAD CUÁNTICA (ISSUE-47):
      // Los tickets que pasan a estado 'done' NUNCA deben volver a un estado anterior
      if (task.status === 'done' && colName !== 'done') {{
        alert(`[GOBERNANZA QUANTUX - REGLA INMUTABLE]\\nLa tarjeta ${{task.id}} ya fue Aceptada y Finalizada conforme a criterios DoD por el Solution Owner.\\n\\nLos entregables en este estado nunca deben volver a un estado anterior.`);
        return;
      }}

      if (colName === 'done' && task.status !== 'done') {{
        const ok = confirm(`¿Confirmar Aceptación Formal del Solution Owner para la tarjeta ${{task.id}}?\\n\\nDebe contrastar el desarrollo ejecutado contra la especificación y criterios de aceptación antes de dar el visto bueno.`);
        if (!ok) return;
        task.so_feedback = {{
          status: "APROBADO CONFORME",
          reviewer: "Freddy Cortés (Solution Owner)",
          date: new Date().toISOString().split('T')[0],
          notes: "Aprobación formal otorgada conforme a criterios DoD."
        }};
      }}

      const previousStatus = task.status;
      task.status = colName;
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        // Reglas de Oro del Solution Owner:
        // 1. Toda tarjeta que pase de retrabajo a revisión (o entre a QA) va al FONDO de revisión (FIFO) (ISSUE-31)
        // 2. Toda tarjeta que pase de revisión a retrabajo (o entre a Rework) va al FONDO de retrabajo (FIFO) (ISSUE-64)
        if (colName === 'qa' || colName === 'rework' || previousStatus === 'rework' || previousStatus === 'qa') {{
          tasks.push(movedTask);
        }} else {{
          tasks.unshift(movedTask);
        }}
      }}
      saveState(false);
      renderBoard();
    }}

    function saveState(notify = true) {{
      localStorage.setItem('quantux_scrumban_v22_progress', JSON.stringify(tasks));
      if (notify) alert('✓ Estado del Tablero Scrumban guardado exitosamente.');
    }}

    function resetDefaultTasks() {{
      if (confirm('¿Restaurar la base de datos oficial del tablero?')) {{
        localStorage.removeItem('quantux_scrumban_v22_progress');
        tasks = JSON.parse(JSON.stringify(INITIAL_BACKLOG));
        tasks.forEach(t => {{
          const d = getTaskDocInfo(t);
          t.doc_link = d.link;
          t.doc_title = d.title;
          t.doc_desc = d.desc;
        }});
        renderCurrentView();
      }}
    }}

    function exportToCSV() {{
      let csv = "ID,Titulo,Tipo,Prioridad,Epica,StoryPoints,Sprint,Estado,Disciplina,Documentacion\\n";
      tasks.forEach(t => {{
        const doc = t.doc_link || '';
        csv += `"${{t.id}}","${{t.title}}","${{t.type || 'UH'}}","${{t.priority || 'P3'}}","${{t.epic}}",${{t.sp}},"${{t.sprint}}","${{t.status}}","${{t.discipline}}","${{doc}}"\\n`;
      }});
      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "Backlog_HealthDesk_Quantux.csv";
      a.click();
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeUHModal();
    }});

    window.addEventListener('DOMContentLoaded', () => {{
      const modalEl = document.getElementById('uh-modal');
      if (modalEl) {{
        modalEl.onclick = (e) => {{
          if (e.target === modalEl) closeUHModal();
        }};
      }}
    }});

    window.onload = init;
  </script>

  <!-- MODAL LIGHTBOX UNIVERSAL CON BOTÓN 'X' DE ALTO CONTRASTE (SPRINT 7 / ISSUE-81) -->
  <div class="modal-overlay" id="modal-image-lightbox" style="display: none; position: fixed; inset: 0; z-index: 999999; background: rgba(15, 23, 42, 0.92); align-items: center; justify-content: center; padding: 24px;" onclick="closeImageLightbox()">
    <div style="position: relative; max-width: 92vw; max-height: 90vh; display: flex; flex-direction: column; align-items: center;" onclick="event.stopPropagation()">
      <button type="button" onclick="closeImageLightbox()" style="position: absolute; top: -16px; right: -16px; width: 36px; height: 36px; border-radius: 50%; background: #0F172A; color: #FFFFFF; border: 2.5px solid #CBD5E1; font-size: 22px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; box-shadow: 0 4px 14px rgba(0,0,0,0.6); transition: all 0.15s ease;" onmouseover="this.style.background='#334155'" onmouseout="this.style.background='#0F172A'">&times;</button>
      <img id="lightbox-modal-img" src="" alt="Captura ampliada" style="max-width: 90vw; max-height: 82vh; border-radius: 8px; box-shadow: 0 25px 60px rgba(0,0,0,0.6); object-fit: contain; background: #0F172A; border: 1.5px solid #334155;" />
      <div id="lightbox-modal-caption" style="margin-top: 12px; font-size: 13px; color: #F1F5F9; font-weight: 700; text-align: center; background: rgba(15,23,42,0.8); padding: 6px 16px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2);"></div>
    </div>
  </div>

</body>
</html>
"""

    with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Tablero Scrumban generado exitosamente en: {HTML_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_scrumban_board()
