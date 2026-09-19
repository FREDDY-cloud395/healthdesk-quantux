# Registro de Cambios y Versiones (Changelog)

Todos los cambios notables en este proyecto están documentados en este archivo siguiendo los lineamientos de [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y respetando [Versionado Semántico (SemVer 2.0.0)](https://semver.org/lang/es/).

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
  - **M13: Copilot N1 Resolutivo & Telemetría Zero-Question:** Asistente cognitivo de resolución guiada y captura automática de contexto.
  - **M14: Suite Médica Asistencial:** Botón de emergencia 1-toque ("Paciente en Box"), protocolos de contingencia offline con recetario descargable y dictado de audio-ticket asistido por IA (`UH-74` a `UH-77`).
  - **M15: Sidebar Zen Dinámico:** Modo colapsable a 64px estilo Windows 11 Fluent / Task Manager con persistencia en `localStorage`, sub-árbol con contadores en vivo y RBAC contextual (`UH-78` a `UH-80`).
- **Portal de Solicitante & Triage Asistencial IA:**
  - Chat conversacional multi-turno con diagnóstico de causa raíz y pasos técnicos inmediatos.
  - Dictado por voz en consultorio integrado con Web Speech API.
  - Bypass express directo a guardia de soporte y autogestión con deflexión inmutable (`[✓ Quedó Resuelto]`).
- **Certificación de Calidad QA Automatizada (100% Exitoso):**
  - Suite E2E de 73 pruebas automatizadas cubriendo todas las capas (Frontend, Maestros, ITIL FSM, CSV, KB, Team Leader, Releases, Triage IA).
  - 0 Errores de sintaxis JavaScript y preflight check 100% aprobado.
