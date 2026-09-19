# Registro de Cambios y Versiones (Changelog)

Todos los cambios notables en este proyecto están documentados en este archivo siguiendo los lineamientos de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y respetando [Versionado Semántico (SemVer 2.0.0)](https://semver.org/lang/es/).

## [4.0.0-DEV] - 2026-09-19 (Cierre de Versión v4 • Portal Solicitante IA & Executive Donut Charts)

### 🩺 Portal de Solicitante & Triage Asistencial IA
- **Chat Conversacional Multi-Turno:** Flujo interactivo persistente asistido por IA (`/api/v1/ai/triage`), búsqueda semántica en base de conocimientos, diagnóstico de causa raíz y pasos técnicos inmediatos.
- **Dictado por Voz en Consultorio:** Integración nativa con Web Speech API para dictar problemas mientras el profesional atiende, reflejando el texto en tiempo real.
- **Bypass Express Sin Chat:** Botón destacado `+ Crear Ticket Rápido` y enlace directo para derivar incidencias críticas a guardia de soporte en un solo paso.
- **Historial Discreto y Ocultamiento de Bandeja:** Cumplimiento de la directiva de diseño: ocultamiento total de la mesa de ayuda para solicitantes, brindando acceso a solicitudes previas exclusivamente mediante un link sutil (`Mis solicitudes anteriores (N)`) que abre un modal con pestañas y buscador.
- **Autogestión y Deflexión Inmutable:** Botón `[✓ Quedó Resuelto]` que registra la resolución por autogestión en la base de datos vía `/api/v1/ai/resolve-incident`.

### 📊 Tablero de Control & Optimización Visual
- **Donut Charts SVG en Tonos Pastel:** Gráficos de torta con paleta suave pastel, links navegables a la bandeja y cero saturación visual.
- **Aprovechamiento Integral del Espacio:** Inyección de tabla de incidentes activos en seguimiento debajo de los gráficos del Dashboard.
- **Iconografía Unificada:** Todos los íconos estandarizados bajo el patrón SVG Outline de 18px (`stroke-width="2"`), erradicando emojis en botones de acción.

---

## [4.0.0-PROD] - 2026-09-19 (Enterprise Zen Edition & Full Modular Certification)

### 🌟 Release Oficial Enterprise v4.0.0
- **15 Módulos y 48 Historias de Usuario Certificadas (`UH-33` a `UH-80`):**
  - **M1: Incidentes Masivos:** Relación jerárquica padre/hijos con resolución y cierre automatizado en cascada (`UH-33` a `UH-35`).
  - **M2: Software Releases & Despliegues:** Catálogo de releases (`/api/v1/releases`) y cierre automático de tickets al desplegar a producción (`UH-36`, `UH-37`).
  - **M3: Bandeja General Zen & Ergonomía:** Paginación dinámica (10/25/50), filtro destacado "⚡ Sin Asignar" y supresión de tintes rojizos en hover con micro-animaciones en *Soft Ice Blue* (`#F0F7FF`) (`UH-38` a `UH-41`).
  - **M4: Workspace Zen del Caso:** Modal y panel compacto de 48px, acordeones colapsables para datos técnicos densos (JSON/XML/IPs), indicador SLA ergonómico y notas colapsables (`UH-42` a `UH-47`).
  - **M5: Flujo de Alta Reorganizado:** Sustitución de las 8 macro-tarjetas por Segmented Controls compactos de 1 línea, smart defaults para organizaciones y acordeón de opciones técnicas (`UH-48` a `UH-51`).
  - **M6: Generalización Enterprise Multi-Servicio:** Catálogo universal ampliado a 29 plataformas (APIs, Infraestructura, Software, Soporte) y neutralización del término restrictivo "asistencial" (`UH-52`, `UH-53`).
  - **M7: Tablero de Control Zen:** 4 North Star KPIs, ranking Top 5 de clientes y servicios, dona interactiva con prefiltrado (`UH-54` a `UH-57`).
  - **M8: Directorio de Usuarios Zen:** Paginación en bloques de 10, fusión de Rol y Nivel ITIL, y Modal interactivo `[ 👤 Perfil ]` con edición de datos, reseteo de clave y auditoría (`UH-58` a `UH-61`).
  - **M9: Ingesta por Email (Email-to-Ticket):** Parseo de correos entrantes, threading bidireccional (`Re: [#TICK-...]`) y auto-reply (`UH-62` a `UH-64`).
  - **M10: Cierre por Solicitante & CSAT Gamificado "Buena Onda":** Separación estricta entre `Resuelto` (Soporte) y `Cerrado` (Solicitante), grilla con 5 emojis reactivos, píldoras de elogios (*Kudos*) y protocolo empático de queja/rescate (`UH-65` a `UH-67`).
  - **M11: Catálogo Zen Multi-Tenant:** Tarjetas con barra de cobertura (ej. 7/11 activos) y Drawer Lateral Ficha 360° con switches de activación y contratos SLA (`UH-68` a `UH-71`).
  - **M12: Torre de Control & Rol Team Leader:** Rol nativo supervisor, balanceador de carga en 1 clic y cola prioritaria de rescate CSAT (`UH-72`, `UH-73`).
  - **M14: Suite Médica Asistencial:** Botón de emergencia 1-toque ("Paciente en Box"), protocolos de contingencia offline con recetario descargable y dictado de audio-ticket asistido por IA (`UH-74` a `UH-77`).
  - **M15: Sidebar Zen Dinámico:** Modo colapsable a 64px estilo Windows 11 Fluent / Task Manager con persistencia en `localStorage`, sub-árbol con contadores en vivo y RBAC contextual (`UH-78` a `UH-80`).
- **Certificación de Calidad QA Automatizada (100% Exitoso):**
  - Suite E2E de 73 pruebas automatizadas cubriendo todas las capas (Frontend, Maestros, ITIL FSM, CSV, KB, Team Leader, Releases, Triage IA).
  - 0 Errores de sintaxis JavaScript y preflight check 100% aprobado.

---

## [3.2.0-PROD] - 2026-09-11 (Official Production Cloud Release & Executive Redesign)

### 🚀 Release Oficial para Despliegue en la Nube
- **Mesa de Ayuda Homologada con Diseño Ejecutivo:**
  - Alineación completa de la vista `Mesa de Ayuda` (`view-tickets`) con la estructura visual y jerarquía del `Directorio de Usuarios`.
  - Header unificado con métricas en tiempo real (`143 Solicitudes`), subtítulo asistencial ITIL y botón destacado de alta rápida.
  - Barra de píldoras de filtrado rápido ITIL (`Todos los Tickets`, `👤 Asignados a Mí`, `⚪ Sin Asignar`, `🚨 Críticos P1`, `🔵 Nivel 1`, `✅ Resueltos / Archivados`) con conteos dinámicos en tiempo real.
  - Franja secundaria de filtros desplegables de precisión (Institución, Plataforma, Nivel ITIL, Estado y Período de Creación).
  - Botón de refresco interactivo `🔄` con rotación suave, invalidación de caché, recarga en tiempo real y toasts de confirmación.
  - Tabla de diseño ejecutivo con encabezado azul marino `#0A1C3E` y texto blanco sticky, bordes gruesos de prioridad en tarjetas y micro-animaciones en hover.
- **Identidad Corporativa y Branding de Soporte:**
  - Emblema oficial en degradado teal/azul con ícono de headset de soporte `🎧` y tipografía corporativa `QUANTUX ServiceDesk - Soporte HealthTech`.
- **Preparación Integral para Cloud Production:**
  - `Dockerfile` multi-worker optimizado para Cloud Run, AWS ECS, Azure Container Apps y Kubernetes.
  - `docker-compose.prod.yml` con healthchecks integrados y persistencia de volúmenes.
  - Soporte de base de datos relacional PostgreSQL / Cloud SQL vía `DATABASE_URL` con fallback automático a SQLite local.
  - Template `.env.production` y scripts de despliegue automatizados (`deploy_cloud.sh`, `deploy_cloud.ps1`, `cloudbuild.yaml`).

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
