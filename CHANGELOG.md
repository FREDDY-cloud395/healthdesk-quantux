# Registro de Cambios y Versiones (Changelog)

Todos los cambios notables en este proyecto están documentados en este archivo siguiendo los lineamientos de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y respetando [Versionado Semántico (SemVer 2.0.0)](https://semver.org/lang/es/).

---

## [3.0.0] - 2026-09-11 (Senior UX & Clean Usability Overhaul Edition)

### ✨ Rediseño Integral de Experiencia de Usuario (Senior UX / UI)
- **Bandeja de Tickets Despejada y Limpia (`.ticket-card-clean`):**
  - Reemplazo de tarjetas sobrecargadas con insignias confusas por un diseño espacioso de 3 líneas jerárquicas.
  - Acento visual de prioridad sutil en el borde izquierdo (`prio-p1` a `prio-p5`) con chips legibles y ordenados.
  - Identificación instantánea de ID, título truncado a 2 líneas, plataforma, institución, tiempo transcurrido y estado del ticket.
- **Detalle de Ticket Estructurado en Pestañas Especializadas:**
  - **Cabecera Ejecutiva:** Título destacado, badges institucionales/plataforma, indicador de SLA con barra de tiempo restante y barra de acciones rápidas contextuales.
  - **💬 Actividad & Notas:** Flujo de conversación limpio tipo chat que separa mensajes del solicitante y notas internas privadas con selector visual y caja de respuesta ergonómica inferior.
  - **📋 Ficha Técnica & Diagnóstico:** Cuadrícula de 2 columnas con tarjetas de información técnica: Solicitante y Contacto, Plataforma y SLAs, Diagnóstico y Evidencias (con preview de adjuntos), y Solución Técnica Registrada.
  - **📜 Historial & Trazabilidad:** Línea de tiempo cronológica inmutable con registro forense de todas las acciones y cambios de estado.
  - **📚 Base de Conocimiento Sugerida:** Sugerencias automáticas de artículos y protocolos homologados según la plataforma afectada, más botón para promover a la KB.
- **Modales de Acción Dedicados (Reducción de Carga Cognitiva):**
  - `Modal Resolver Ticket (#modal-resolve-ticket)`: Captura limpia de causa raíz, procedimiento de solución, flag de workaround y opción de auto-publicación en la KB.
  - `Modal Reasignar Ticket (#modal-reassign-ticket)`: Selector ergonómico de operador y nivel ITIL (N1, N2, N3) con motivo de derivación.
  - `Modal Escalamiento ITIL (#modal-escalate-ticket)`: Flujo guiado para escalamientos entre niveles con visualización de SLA objetivo.
- **Micro-interacciones y Animaciones Fluidas:**
  - Transiciones suaves `fadeInUp` y `slideIn`, feedback háptico/visual en botones de acción y selector intuitivo de pestañas con `aria-selected`.

---

## [2.5.0] - 2026-09-10 (ITIL Tiered Support & Multi-Helpdesk Edition)

### ✨ Novedades & Funcionalidades Principales
- **Estructura Multi-Nivel ITIL (N1, N2, N3):**
  - Implementación del modelo de niveles de soporte:
    - `🔵 Nivel 1 (N1 - Help Desk / Triage)`: Recepción, categorización y resolución de primer contacto.
    - `🟣 Nivel 2 (N2 - Soporte Especializado)`: Especialistas asignados por plataforma médica (Receta Digital, Telemedicina, HCE, LIS, RIS/PACS).
    - `🔴 Nivel 3 (N3 - Ingeniería & Proveedores Críticos)`: Incidencias de infraestructura, base de datos y emergencias asistenciales P1.
- **Configuración de Mesas de Ayuda en UI:**
  - Nueva pestaña de gestión en la vista Configuración (`view-config`) con edición dinámica de SLAs, horarios de cobertura, canales de contacto y asignación de equipos especializados.
- **Flujo de Escalamiento Contextual:**
  - Botones de acción directa en la ficha técnica del ticket (`⚡ Escalar a N2`, `⚡ Escalar a N3`, `↩️ Devolver a N1`).
  - Modal interactivo de confirmación con registro de justificación, cambio de especialista y auditoría inmutable.
- **Filtros ITIL en Cockpit y Directorio:**
  - Selector de nivel ITIL en la barra de herramientas (`#col-filter-level`).
  - Píldoras de filtrado por nivel en el Directorio de Usuarios (`Todos`, `N1`, `N2`, `N3`, `Solicitantes`).

### 🛠️ Mejoras de Estabilidad & Rendimiento
- **Migraciones Automáticas SQLite No Destructivas:**
  - Función `init_db()` en `backend/app/db/session.py` con sentencias `ALTER TABLE` seguras para columnas `support_level`, `attachment_url`, `version`, `changelog`, `view_count` y `source_ticket_id`.
- **Eliminación de Deadlocks de Middleware:**
  - Removido el middleware bloqueante `BaseHTTPMiddleware` en FastAPI sobre Windows para permitir transferencias asíncronas concurrentes instantáneas (< 35 ms).
- **Lanzadores Automáticos Robustos:**
  - Creación de `run_server.py`, `iniciar_healthdesk.bat` e `iniciar_healthdesk.ps1` con liberación automática de puertos huérfanos y apertura inteligente del navegador.
  - Accesos directos en Escritorio (`Desktop`) y raíz de usuario.

---

## [2.0.0] - 2026-09-08 (Knowledge Base Versioning & Responsive Split Cockpit)

### ✨ Novedades
- **Base de Conocimiento (KB) con Versionado Semántico:**
  - Soporte para creación de nuevas versiones de artículos (`v1.0`, `v1.1`, `v2.0`).
  - Historial inmutable de revisiones (`kb_article_history`) con visualización comparativa de cambios.
  - Promoción de tickets resueltos directamente a artículos de la Base de Conocimiento.
- **Rediseño Senior Cockpit & Split Detail:**
  - Vista dividida (Inbox lateral + Ficha técnica central) con soporte responsivo total en móviles y tablets.
  - Header adaptativo con navegación rápida y selector dinámico de cuentas de usuario.

---

## [1.0.0] - 2026-08-30 (Lanzamiento Inicial Quantux HealthDesk)

### ✨ Novedades
- **Gestión Centralizada de Tickets:**
  - Creación, asignación, seguimiento de estado (FSM: `NUEVO`, `ASIGNADO`, `EN_CURSO`, `RESUELTO`, `CERRADO`) y cierre con conformidad.
  - Matriz de prioridad asistencial (P1 Crítico a P5 Informativo) y cálculo de SLA médico.
- **Multi-Institucional & Multi-Plataforma:**
  - Soporte para 14 instituciones prestadoras de salud (OSDE, Swiss Medical, Galeno, etc.) y 9 plataformas médicas.
- **Módulos Ejecutivos Integrados:**
  - Tablero Scrumban, Plan de Gestión, Especificación Funcional y Presentación Ejecutiva.
