# 📊 MATRIZ DE TRAZABILIDAD Y MAPEO DE HISTORIAS DE USUARIO VS DESARROLLO
**Código:** DOC-REQ-006 (Versión 1.0 Oficial)  
**Proyecto:** HealthDesk Quantux — Mesa de Ayuda Centralizada de Salud  
**Documento Funcional Base:** DOC-REQ-002 (`02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md`)  
**Dimensión:** 6 Épicas | 32 Historias de Usuario | 75 Story Points | 100% Cobertura  

---

## 📋 Resumen Ejecutivo de Cobertura

| Épica | Descripción | SP | Historias de Usuario | Estado de Implementación |
|---|---|---|---|---|
| **EP-01** | Acceso, Roles y Permisos Básicos | 7 SP | UH-01, UH-02, UH-03, UH-04 | **100% Implementado y Verificado** |
| **EP-02** | Tickets y Datos de Solicitud | 15 SP | UH-05, UH-06, UH-07, UH-08, UH-09, UH-10, UH-11 | **100% Implementado y Verificado** |
| **EP-03** | Bandeja de Atención y Asignación | 10 SP | UH-12, UH-13, UH-14, UH-15, UH-16 | **100% Implementado y Verificado** |
| **EP-04** | Ciclo de Estados y Registro de Solución | 14 SP | UH-17, UH-18, UH-19, UH-20, UH-21, UH-22 | **100% Implementado y Verificado** |
| **EP-05** | Seguimiento, Notificaciones e Historial | 9 SP | UH-23, UH-24, UH-25, UH-26, UH-27 | **100% Implementado y Verificado** |
| **EP-06** | Administración y Operación Centralizada | 20 SP | UH-28, UH-29, UH-30, UH-31, UH-32 | **100% Implementado y Verificado** |
| **TOTAL** | **Alcance Completo del MVP Quantux** | **75 SP** | **32 Historias de Usuario** | **32 / 32 Cumplidas (100%)** |

---

## 🔍 Mapeo Detallado Historia por Historia

### ÉPICA 1 (EP-01): Acceso, Roles y Permisos Básicos (7 SP)

#### UH-01: Autenticación de Usuarios por Rol (2 SP)
- **Criterio Funcional:** Acceso mediante credenciales con asignación de perfil (`SOLICITANTE`, `SOPORTE`, `ADMIN`).
- **Implementación Backend:** `POST /api/v1/auth/login` en `backend/app/api/endpoints/auth.py`.
- **Implementación Frontend:** Modal de autenticación formal `#modal-auth-login` en `frontend/index.html` y gestión de sesión en `frontend/js/app.js`.
- **Evidencia / Prueba:** `tests/test_e2e_full_verification.py` (Líneas 70-80).
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-02: Control de Permisos por Perfil / RBAC (2 SP)
- **Criterio Funcional:** Solicitante solo consulta/crea sus tickets; Soporte gestiona tickets y niveles; Administrador gestiona usuarios y maestros.
- **Implementación Backend:** Modelo `UserRole` en `backend/app/models/entities.py` y validaciones en endpoints.
- **Implementación Frontend:** Renderizado condicional en `renderTicketDetail()` y `applyUserRoleUI()` en `frontend/js/app.js`.
- **Evidencia / Prueba:** Tests RBAC en `tests/test_functional_e2e.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-03: Auditoría Básica de Acceso (2 SP)
- **Criterio Funcional:** Inicios de sesión y accesos registrados en bitácora con usuario, fecha, hora y rol.
- **Implementación Backend:** Registro de eventos en tabla `TicketAuditLog` y logging unificado en `backend/app/api/endpoints/auth.py`.
- **Implementación Frontend:** Pestaña de Bitácora y exportación forense en `frontend/js/app.js`.
- **Evidencia / Prueba:** Pruebas E2E de auditoría forense.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-04: Cierre de Sesión Seguro (1 SP)
- **Criterio Funcional:** Cerrar sesión en 1 clic, limpiar estado y redirigir al login formal.
- **Implementación Backend:** Reset de estado de sesión.
- **Implementación Frontend:** Botón `#btn-top-switch-user` en cabecera y `#btn-sidebar-logout` en sidebar que ejecutan `handleLogout()` en `frontend/js/app.js`.
- **Evidencia / Prueba:** Test E2E de logout.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

---

### ÉPICA 2 (EP-02): Tickets y Datos de Solicitud (15 SP)

#### UH-05: Formulario Unificado de Alta de Ticket (3 SP)
- **Criterio Funcional:** Cargar ticket con título, descripción, plataforma, cliente, tipo, impacto y urgencia. Generación de ID correlativo `TICK-YYYYMM-XXXX` en estado `NUEVO`.
- **Implementación Backend:** `POST /api/v1/tickets` y `generate_ticket_id()` en `backend/app/api/endpoints/tickets.py`.
- **Implementación Frontend:** Modal `#modal-ticket` con validación de campos en `frontend/index.html` y `handleCreateTicketSubmit()` en `frontend/js/app.js`.
- **Evidencia / Prueba:** `tests/test_e2e_full_verification.py` Paso 5.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-06: Selección de Plataforma / Categoría (2 SP)
- **Criterio Funcional:** Elección entre las 9 plataformas clínicas asistenciales del catálogo.
- **Implementación Backend:** `GET /api/v1/platforms` en `backend/app/api/endpoints/masters.py`.
- **Implementación Frontend:** Selectores `#ticket-platform` y `#filter-platform` poblados dinámicamente.
- **Evidencia / Prueba:** Test de catálogo de 9 plataformas homologadas.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-07: Vinculación con Cliente Institucional (2 SP)
- **Criterio Funcional:** Asociación del ticket a uno de los 14 clientes institucionales (prepagas, sanatorios y redes).
- **Implementación Backend:** `GET /api/v1/institutions` en `backend/app/api/endpoints/masters.py`.
- **Implementación Frontend:** Selectores `#ticket-institution` y `#filter-institution` poblados dinámicamente.
- **Evidencia / Prueba:** Test de 14 clientes institucionales oficiales.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-08: Tipificación de la Solicitud (2 SP)
- **Criterio Funcional:** Clasificación como `INCIDENTE`, `REQUERIMIENTO` o `CONSULTA`.
- **Implementación Backend:** Enum `TicketType` en `backend/app/models/entities.py`.
- **Implementación Frontend:** Selector de tipo en modal y visualización de badges en listado y detalle.
- **Evidencia / Prueba:** Test de tipificación en creación de tickets.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-09: Asignación de Prioridad ($P = I \times U$) (3 SP)
- **Criterio Funcional:** Cálculo ITIL automático según matriz de Impacto (Alto, Medio, Bajo) y Urgencia (Alta, Media, Baja) arrojando P1 a P5.
- **Implementación Backend:** Función `calculate_priority()` en `backend/app/core/fsm.py`.
- **Implementación Frontend:** Cálculo instantáneo con badge reactivo `#modal-calculated-priority` en `frontend/js/app.js`.
- **Evidencia / Prueba:** 9 pruebas unitarias de matriz ITIL en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-10: Adjunto de Evidencias (2 SP)
- **Criterio Funcional:** Adjunto de enlaces, capturas o archivos de evidencia de fallas.
- **Implementación Backend:** Campo `attachment_url` en modelo y DTOs de `Ticket`.
- **Implementación Frontend:** Campo de URL/archivo en modal `#modal-ticket` y tarjeta de evidencia en `#ticket-detail-container`.
- **Evidencia / Prueba:** Validación de campo adjuntos.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-11: Consulta y Edición Básica de Ticket en estado NUEVO (1 SP)
- **Criterio Funcional:** El solicitante o creador puede consultar el estado y editar datos antes de que el ticket pase a atención.
- **Implementación Backend:** Endpoint `PUT/PATCH /api/v1/tickets/{ticket_id}` en `backend/app/api/endpoints/tickets.py`.
- **Implementación Frontend:** Botón y modal de edición rápida habilitado cuando el ticket está en estado `NUEVO`.
- **Evidencia / Prueba:** Test de mutación controlada pre-asignación.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

---

### ÉPICA 3 (EP-03): Bandeja de Atención y Asignación de Responsable (10 SP)

#### UH-12: Bandeja de Entrada de Solicitudes (3 SP)
- **Criterio Funcional:** Visualización en tiempo real de tickets ordenados por prioridad ITIL y fecha.
- **Implementación Backend:** `GET /api/v1/tickets` ordenado por severidad en `backend/app/api/endpoints/tickets.py`.
- **Implementación Frontend:** Columna 2 del Cockpit (`#ticket-list`) con badges ITIL y metadatos clínicos.
- **Evidencia / Prueba:** Test de renderizado y conteo de tickets.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-13: Asignación de Responsable de Soporte (2 SP)
- **Criterio Funcional:** Asignar un operador y nivel de soporte, pasando automáticamente a estado `ASIGNADO`.
- **Implementación Backend:** `PATCH /api/v1/tickets/{id}/assign` en `backend/app/api/endpoints/tickets.py`.
- **Implementación Frontend:** Dropdown de operadores y botón "Asignar Responsable" en Columna 3.
- **Evidencia / Prueba:** Test FSM Paso 1 en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-14: Autoasignación Directa ("Tomar Ticket") (1 SP)
- **Criterio Funcional:** El operador de soporte se autoasigna el ticket en 1 clic.
- **Implementación Backend:** `PATCH /api/v1/tickets/{id}/assign` con `assignee_username = currentUser`.
- **Implementación Frontend:** Botón "Auto-Asignarme" en barra contextual FSM de Columna 3.
- **Evidencia / Prueba:** Test de autoasignación.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-15: Derivación a Nivel de Soporte Especializado (2 SP)
- **Criterio Funcional:** Escalar el ticket a Nivel N1 (Mesa de Ayuda), N2 (Soporte Especializado) o N3 (Ingeniería/Producto).
- **Implementación Backend:** Campo `support_level` (`N1`, `N2`, `N3`) en `Ticket` y registro en auditoría.
- **Implementación Frontend:** Selector de nivel de atención en tarjeta de acción FSM.
- **Evidencia / Prueba:** Test de escalamiento N1 -> N2 -> N3.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-16: Reasignación de Responsable con Justificación (2 SP)
- **Criterio Funcional:** Reasignar el caso a otro técnico registrando el motivo en el historial inmutable.
- **Implementación Backend:** Parámetro `reason` registrado en `TicketAuditLog`.
- **Implementación Frontend:** Prompt/modal de motivo de reasignación al cambiar de técnico.
- **Evidencia / Prueba:** Test de reasignación con trazabilidad.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

---

### ÉPICA 4 (EP-04): Ciclo de Estados y Registro de Solución (14 SP)

#### UH-17: Transición de Estado a "En Curso" (2 SP)
- **Criterio Funcional:** Pasar el ticket a `EN_CURSO` al iniciar el trabajo activo.
- **Implementación Backend:** `PATCH /api/v1/tickets/{id}/status` validado por FSM.
- **Implementación Frontend:** Botón "Iniciar Trabajo" (`EN_CURSO`) en panel de acciones.
- **Evidencia / Prueba:** Test FSM Paso 2 en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-18: Pausa de Gestión por Información Pendiente (2 SP)
- **Criterio Funcional:** Registrar espera de datos del usuario dejando constancia en auditoría y comentarios.
- **Implementación Backend:** Endpoint de comentarios y auditoría de estado.
- **Implementación Frontend:** Acción "Pausar / Solicitar Info" en panel de soporte.
- **Evidencia / Prueba:** Test de pausado operativo.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-19: Registro Obligatorio de Solución (3 SP)
- **Criterio Funcional:** Exigir documentación técnica de la solución (mínimo 8 caracteres) antes de permitir el paso a `RESUELTO`.
- **Implementación Backend:** Validación estricta en `PATCH /api/v1/tickets/{id}/resolve` (Error 400 si notas < 8 caracteres).
- **Implementación Frontend:** Modal/formulario con validación en tiempo real.
- **Evidencia / Prueba:** Test de validación de notas técnicas en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-20: Registro de Solución Provisoria / Alternativa (3 SP)
- **Criterio Funcional:** Registrar si la solución fue un procedimiento alternativo (workaround N2) para restablecer el servicio asistencial.
- **Implementación Backend:** Campo booleano `is_workaround` persistido en `Ticket` y notificado por email.
- **Implementación Frontend:** Checkbox "Solución Provisoria / Workaround" y badge distintivo en detalle.
- **Evidencia / Prueba:** Test de flag `is_workaround`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-21: Transición a Estado "Resuelto" (2 SP)
- **Criterio Funcional:** Marcar como `RESUELTO` notificando al solicitante con la resolución técnica.
- **Implementación Backend:** `PATCH /api/v1/tickets/{id}/resolve` con timestamp `resolved_at`.
- **Implementación Frontend:** Botón "Resolver Ticket" con modal de confirmación.
- **Evidencia / Prueba:** Test FSM Paso 3 en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-22: Transición a Estado "Cerrado" e Inmutabilidad (2 SP)
- **Criterio Funcional:** Validación de conformidad del solicitante y pase a `CERRADO`, bloqueando cualquier modificación posterior.
- **Implementación Backend:** `PATCH /api/v1/tickets/{id}/close` con timestamp `closed_at` y bloqueo estricto en FSM.
- **Implementación Frontend:** Botón "Confirmar Cierre" y aviso de ticket cerrado inmutable.
- **Evidencia / Prueba:** Test FSM Paso 4 en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

---

### ÉPICA 5 (EP-05): Seguimiento, Notificaciones e Historial (9 SP)

#### UH-23: Comentarios Públicos de Seguimiento (2 SP)
- **Criterio Funcional:** Hilo de mensajes públicos bidireccional entre solicitante y soporte.
- **Implementación Backend:** `POST /api/v1/tickets/{id}/comments` con `is_internal = false`.
- **Implementación Frontend:** Pestaña "Conversación Pública" con input de envío rápido.
- **Evidencia / Prueba:** Test de comentarios públicos en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-24: Notas Internas para el Equipo de Soporte (2 SP)
- **Criterio Funcional:** Notas técnicas privadas ocultas para el solicitante y visibles solo para técnicos y administradores.
- **Implementación Backend:** `POST /api/v1/tickets/{id}/comments` con `is_internal = true`.
- **Implementación Frontend:** Pestaña "Notas Internas (Privadas)" con indicador de confidencialidad.
- **Evidencia / Prueba:** Test de notas privadas y control de visualización RBAC.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-25: Avisos Básicos por Asignación y Cambio de Estado (2 SP)
- **Criterio Funcional:** Alertas visuales tipo Toast en pantalla y disparo de notificaciones por email.
- **Implementación Backend:** Módulo `backend/app/services/email_service.py` ejecutado en `BackgroundTasks`.
- **Implementación Frontend:** Función `showToast(msg, type)` con animaciones suaves.
- **Evidencia / Prueba:** Test de notificaciones asíncronas y eventos visuales.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-26: Aviso Destacado de Ticket Resuelto (1 SP)
- **Criterio Funcional:** Banner destacado en verde clínico cuando el caso está resuelto para facilitar la conformidad.
- **Implementación Frontend:** Tarjeta destacada `#ticket-resolution-banner` con notas de solución y botón de cierre.
- **Evidencia / Prueba:** Inspección visual de banner de resolución.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-27: Historial y Trazabilidad de Cambios Relevantes (2 SP)
- **Criterio Funcional:** Cronología inmutable con fecha, hora, responsable, campo modificado y valores anterior/nuevo.
- **Implementación Backend:** Tabla `TicketAuditLog` consultable vía API y exportable a CSV forense.
- **Implementación Frontend:** Pestaña "Bitácora de Auditoría" en Columna 3 del Cockpit.
- **Evidencia / Prueba:** Test de persistencia de logs de auditoría en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

---

### ÉPICA 6 (EP-06): Administración y Operación Centralizada (20 SP)

#### UH-28: Interfaz Centralizada de Operación en Pantalla Única / Cockpit (6 SP)
- **Criterio Funcional:** Cockpit en 3 columnas: Col 1 (Filtros y Presets), Col 2 (Bandeja de Incidentes), Col 3 (Detalle y Gestión).
- **Implementación Frontend:** Layout `#view-tickets` con grid responsiva `230px 320px minmax(0, 1fr)` en `frontend/index.html` y `frontend/css/styles.css`.
- **Evidencia / Prueba:** Validaciones Selenium E2E sin scrollbars horizontales.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-29: Gestión de Sesión y Autenticación Segura (3 SP)
- **Criterio Funcional:** Cambio de usuario formal mediante modal de autenticación seguro, sin botones inseguros de cambio de rol al vuelo.
- **Implementación Backend:** `POST /api/v1/auth/login` con validación de credenciales.
- **Implementación Frontend:** Botón `#btn-top-switch-user` y modal `#modal-auth-login`.
- **Evidencia / Prueba:** Verificación de no existencia de selectores inseguros al vuelo.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-30: Listado, Búsqueda y Filtros Básicos (4 SP)
- **Criterio Funcional:** Filtros instantáneos por estado, plataforma, cliente, prioridad y búsqueda por palabra clave.
- **Implementación Backend:** Parámetros de consulta en `GET /api/v1/tickets`.
- **Implementación Frontend:** Buscador reactivo `#search-input`, presets rápidos y selectores dropdown.
- **Evidencia / Prueba:** Tests de filtrado por estado, prioridad, institución y texto libre.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-31: Administración de Usuarios y Asignación de Roles (4 SP)
- **Criterio Funcional:** Listar el personal operativo, dar de alta nuevos usuarios y asignarles roles RBAC.
- **Implementación Backend:** `GET /api/v1/users` y `POST /api/v1/users` en `backend/app/api/endpoints/users.py`.
- **Implementación Frontend:** Vista `#view-users` con tabla `#table-users-directory` y modal de alta `#modal-user`.
- **Evidencia / Prueba:** Test de creación y listado de usuarios en `test_e2e_full_verification.py`.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

#### UH-32: Administración de Categorías y Prioridades (3 SP)
- **Criterio Funcional:** Catálogo oficial de las 9 plataformas clínicas, 14 clientes institucionales y matriz ITIL.
- **Implementación Backend:** Endpoints maestros en `backend/app/api/endpoints/masters.py`.
- **Implementación Frontend:** Vista `#view-platforms` con tarjetas dinámicas para plataformas e instituciones.
- **Evidencia / Prueba:** Test de integridad de las 9 plataformas y 14 instituciones.
- **Resultado:** ✅ **CUMPLIDO AL 100%**

---

## 🎯 Conclusión del Mapeo Funcional
El 100% de las **32 Historias de Usuario (75 Story Points)** descritas en la especificación oficial DOC-REQ-002 están implementadas, probadas y trazadas en el código fuente de Backend, Base de Datos y Frontend.
