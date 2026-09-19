# Especificación de Contratos de API REST — HealthDesk Quantux v4
**Quantux Salud — Plataforma de Soporte Clínico Multi-Institucional**  
*Versión de la Especificación: 4.0.0-DEV*  
*Base URL:* `http://localhost:8000/api/v1` (o proxy `/api/v1`)  
*Documentación Interactiva (Swagger/OpenAPI):* `http://localhost:8000/docs`

---

## 1. Principios de Arquitectura y Estándares

1. **Protocolo:** RESTful sobre HTTP/1.1 y HTTP/2 con serialización en formato `application/json`.
2. **Validación de Datos:** Modelos de Pydantic v2 en todas las entradas y salidas (`response_model`).
3. **Manejo Uniforme de Errores:** Errores controlados mediante `HTTPException` devolviendo un envelope estándar:
   ```json
   {
     "detail": "Mensaje descriptivo del error o causa de rechazo"
   }
   ```
4. **Fechas y Tiempos:** Formato ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ` o con milisegundos).
5. **Máquina de Estados Finita (FSM):** Ciclo de vida estricto para tickets:  
   `NUEVO` &rarr; `ASIGNADO` &rarr; `EN_CURSO` &rarr; `RESUELTO` &rarr; `CERRADO`.  
   *Inmutabilidad:* Un ticket en estado `CERRADO` rechaza cualquier modificación ulterior.
6. **Auditoría Inmutable (Caja Negra):** Todo cambio de estado, asignación o resolución genera un registro inmutable en `ticket_audit_logs`.
7. **Notificaciones Multi-Destinatario:** Notificaciones por email con registro en `email_notification_logs` para involucrados (solicitante, soporte y guardia en incidentes P1).

---

## 2. Tipos de Datos y Enums Globales

```typescript
// Roles de Usuario
type UserRole = "ADMIN" | "TEAM_LEADER" | "SOPORTE" | "SOLICITANTE";

// Niveles de Soporte ITIL
type SupportLevel = "N1" | "N2" | "N3";

// Estados del Ciclo de Vida del Ticket (FSM)
type TicketStatus = "NUEVO" | "ASIGNADO" | "EN_CURSO" | "RESUELTO" | "CERRADO";

// Tipo de Ticket
type TicketType = "INCIDENTE" | "CONSULTA" | "REQUERIMIENTO";

// Niveles de Impacto y Urgencia
type ImpactLevel = "BAJO" | "MEDIO" | "ALTO" | "CRITICO";
type UrgencyLevel = "BAJO" | "MEDIO" | "ALTA" | "CRITICA";

// Prioridades Calculadas (Matriz ITIL P = Impacto x Urgencia)
type PriorityLevel = "P1" | "P2" | "P3" | "P4" | "P5";

// Estados de Software Release
type ReleaseStatus = "PLANIFICADA" | "EN_DESARROLLO" | "TESTING" | "DESPLEGADA" | "CANCELADA";
```

### Matriz de Cálculo de Prioridad (ITIL) y SLAs Base
| Impacto | Urgencia | Prioridad | SLA Respuesta | SLA Resolución |
|---|---|---|---|---|
| CRITICO | CRITICA | **P1** (Crítica) | &le; 15 min | &le; 60 min (1 h) |
| ALTO / CRITICO | ALTA / CRITICA | **P2** (Alta) | &le; 30 min | &le; 120 min (2 h) |
| MEDIO | MEDIO | **P3** (Media) | &le; 60 min | &le; 240 min (4 h) |
| BAJO | MEDIO | **P4** (Baja) | &le; 120 min | &le; 480 min (8 h) |
| BAJO | BAJO | **P5** (Mínima) | &le; 240 min | &le; 1440 min (24 h) |

---

## 3. Contratos por Dominio

---

### 3.1. Autenticación y Perfil de Usuario (`/api/v1/auth`)

#### `POST /api/v1/auth/login`
Autentica al usuario mediante sus credenciales institucionales o simula el acceso por rol para pruebas de aceptación (UH-01).

- **Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "username": "soporte",
    "password": "quantux123",        // Opcional, por defecto "quantux123"
    "selected_role": "SOPORTE"       // Opcional: "ADMIN" | "TEAM_LEADER" | "SOPORTE" | "SOLICITANTE"
  }
  ```
- **Respuestas:**
  - `200 OK`:
    ```json
    {
      "status": "SUCCESS",
      "message": "Autenticación exitosa vía Quantux IAM como SOPORTE",
      "user_id": 6,
      "username": "soporte",
      "full_name": "Laura Benítez",
      "email": "soporte@quantux.com",
      "role": "SOPORTE",
      "landing_view": "cockpit_soporte",
      "iam_provider": "Quantux-IAM-Enterprise",
      "permissions": [
        "tickets:view_all",
        "tickets:work",
        "tickets:internal_notes",
        "tickets:escalate",
        "tickets:resolve",
        "kb:view",
        "metrics:view"
      ]
    }
    ```
  - `400 Bad Request`: `{ "detail": "Debe ingresar su nombre de usuario o correo institucional." }`
  - `401 Unauthorized`: `{ "detail": "Credenciales inválidas: El usuario '...' no está registrado en el sistema." }`
  - `403 Forbidden`: `{ "detail": "Acceso denegado: El usuario ... no posee el rol ADMIN." }`

#### `GET /api/v1/auth/switch-role/{target_role}`
Alterna el perfil de usuario de forma rápida (1 clic) para validación de interfaces y permisos RBAC.

- **Parámetros Path:** `target_role` (`ADMIN`, `TEAM_LEADER`, `SOPORTE`, `SOLICITANTE`)
- **Respuestas:**
  - `200 OK`: Mismo esquema que `LoginResponse`.
  - `400 Bad Request`: `{ "detail": "Rol 'XYZ' no válido." }`

---

### 3.2. Gestión del Ciclo de Vida de Tickets (`/api/v1/tickets`)

#### `GET /api/v1/tickets`
Consulta la lista de tickets con capacidades de filtrado multidimensional y paginación.

- **Query Parameters:**
  - `status` (opcional): Filtro por estado (`NUEVO`, `ASIGNADO`, etc.).
  - `priority` (opcional): Filtro por prioridad (`P1`, `P2`, etc.).
  - `platform_code` (opcional): Código de la plataforma asistencial (`CAT_RECETA`, etc.).
  - `institution_code` (opcional): Código de la institución cliente (`OSDE`, etc.).
  - `assignee_username` (opcional): Nombre de usuario asignado.
  - `requester_username` (opcional): Nombre de usuario solicitante.
  - `limit` (opcional, default: 200, max: 1000): Límite de registros.
  - `offset` (opcional, default: 0): Desplazamiento para paginación.
- **Respuestas:**
  - `200 OK`: `Array<Ticket>`
    ```json
    [
      {
        "id": "TICK-202609-0801",
        "title": "Receta Digital Bloqueada",
        "description": "Error PKI...",
        "platform_code": "CAT_RECETA",
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "CRITICO",
        "urgency": "CRITICA",
        "priority": "P1",
        "status": "NUEVO",
        "requester_username": "solicitante",
        "assignee_username": null,
        "support_level": "N1",
        "attachment_url": null,
        "resolution_notes": null,
        "is_workaround": false,
        "parent_ticket_id": null,
        "is_major_incident": false,
        "release_tag": null,
        "channel": "PORTAL",
        "created_at": "2026-09-19T10:30:00Z",
        "updated_at": "2026-09-19T10:30:00Z"
      }
    ]
    ```

#### `POST /api/v1/tickets`
Registra un nuevo ticket, calcula automáticamente la prioridad según la matriz ITIL y despacha las notificaciones por correo electrónico requeridas.

- **Request Body (`TicketCreateRequest`):**
  ```json
  {
    "title": "Falla en firma digital de recetas",
    "description": "Los certificados emitidos no están respondiendo ante el token USB.",
    "platform_code": "CAT_RECETA",
    "institution_code": "OSDE",
    "ticket_type": "INCIDENTE",         // Default: "INCIDENTE"
    "impact": "CRITICO",                // Default: "MEDIO"
    "urgency": "CRITICA",               // Default: "MEDIO"
    "requester_username": "solicitante",// Default: "solicitante"
    "channel": "PORTAL",                // "PORTAL" | "CHAT_IA" | "CORREO" | "MANUAL"
    "telemetry_data": "{\"browser\": \"Chrome\", \"box\": \"Box 2\"}"
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `Ticket` creado con `id` correlativo generado (ej. `TICK-202609-0802`) y `status: "NUEVO"`.
  - `400 Bad Request`: Si faltan campos requeridos o las instituciones/plataformas son inválidas.

#### `GET /api/v1/tickets/{ticket_id}`
Devuelve el detalle integral del ticket incluyendo comentarios, auditoría inmutable y logs de despacho de correo.

- **Parámetros Path:** `ticket_id` (string)
- **Respuestas:**
  - `200 OK` (`TicketDetailResponse`):
    ```json
    {
      "ticket": { ... },
      "comments": [ ... ],
      "audit_logs": [ ... ],
      "email_logs": [ ... ]
    }
    ```
  - `404 Not Found`: `{ "detail": "Ticket no encontrado." }`

#### `POST /api/v1/tickets/{ticket_id}/assign`
Asigna o deriva el ticket a un operador y nivel de soporte específico. Dispara la transición FSM a `ASIGNADO`.

- **Request Body (`TicketAssignRequest`):**
  ```json
  {
    "assignee_username": "soporte",
    "support_level": "N2",
    "reason": "Derivación a especialista N2 por tokens de firma",
    "changed_by_username": "soporte"
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `Ticket` actualizado.
  - `400 Bad Request`: Si el ticket ya está `CERRADO` o el operador no existe.
  - `404 Not Found`: Ticket no encontrado.

#### `POST /api/v1/tickets/{ticket_id}/status`
Ejecuta una transición manual de estado en el ciclo de vida del ticket sujeta a las reglas de la FSM.

- **Request Body (`TicketStatusUpdateRequest`):**
  ```json
  {
    "new_status": "EN_CURSO",
    "reason": "Iniciando diagnóstico en entorno de pruebas",
    "changed_by_username": "soporte"
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `Ticket` actualizado.
  - `400 Bad Request`: Si la transición viola la FSM o el ticket está `CERRADO`.

#### `POST /api/v1/tickets/{ticket_id}/resolve`
Resuelve formalmente el ticket. Exige un guardrail de resolución técnica (&ge; 8 caracteres). Si el ticket es un Incidente Mayor con hijos vinculados, propaga automáticamente la solución en cascada.

- **Request Body (`TicketResolveRequest`):**
  ```json
  {
    "resolution_notes": "Se realizó failover a servidor secundario y se reanudó la emisión.",
    "is_workaround": true,
    "resolved_by_username": "soporte",
    "git_branch": "fix/token-pki",
    "git_pr": "#142",
    "git_commit": "a3f912b"
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `Ticket` actualizado con `status: "RESUELTO"`.
  - `400 Bad Request`: Si `resolution_notes` tiene menos de 8 caracteres o el ticket está cerrado.

#### `POST /api/v1/tickets/{ticket_id}/close`
Cierre definitivo del ticket realizado exclusivamente por el Solicitante (o Admin con justificación). Recoge métricas CSAT. Si la calificación es &le; 2 estrellas, activa la bandera `requires_service_recovery` para auditoría de calidad.

- **Request Body (`TicketCloseRequest`):**
  ```json
  {
    "closed_by_username": "solicitante",
    "feedback": "Verificado en producción, funcionamiento correcto.",
    "rating_stars": 5,                 // Entero 1 a 5
    "rating_kudos": "Excelente atención y rapidez",
    "rating_feedback": "Muy conforme"
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `Ticket` actualizado con `status: "CERRADO"`.
  - `400 Bad Request`: Si el ticket no estaba resuelto previamente.

#### `POST /api/v1/tickets/ia-resolved`
Registra un caso resuelto de forma autónoma mediante el Asistente Cognitivo IA (Deflexión de Primer Nivel). Genera el ticket directamente en estado `RESUELTO` con canal `CHAT_IA`.

- **Request Body (`IaResolvedTicketRequest`):**
  ```json
  {
    "title": "Consulta Guía de Firma Digital",
    "description": "El profesional consultó procedimiento de habilitación.",
    "category": "Consultorio Digital",
    "platform_code": "CAT_CONSULTORIO_DIGITAL",
    "institution_code": "SWISS_MEDICAL",
    "requester_username": "solicitante",
    "requester_name": "Dr. Martín Gómez",
    "resolution_notes": "Indicación ejecutada con éxito según artículo KB-004",
    "chat_transcript": "Usuario: Hola... IA: Siga estos pasos...",
    "ia_feedback": "Resuelto en Chat IA con éxito"
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `Ticket` registrado.

#### `POST /api/v1/tickets/{ticket_id}/comments` y `GET /api/v1/tickets/{ticket_id}/comments`
Permite añadir comentarios públicos o notas internas privadas (exclusivas de soporte y ocultas para solicitantes).

- **Request Body (`TicketCommentRequest`):**
  ```json
  {
    "author_username": "soporte",
    "message": "Nota interna: Verificando logs en el pod de Kubernetes.",
    "is_internal": true
  }
  ```
- **Respuestas:**
  - `200 OK`: Objeto `TicketComment` persistido.

#### `GET /api/v1/tickets/{ticket_id}/audit`
Devuelve el registro de auditoría cronológico de la caja negra para el ticket.

- **Respuestas:** `200 OK`: `Array<TicketAuditLog>`

#### `GET /api/v1/tickets/{ticket_id}/notifications`
Devuelve el historial completo de notificaciones por email generadas para el ticket.

- **Respuestas:** `200 OK`: `Array<EmailNotificationLog>`

#### `POST /api/v1/tickets/{ticket_id}/copilot-autofix`
Ejecuta el asistente Copilot de autodiagnóstico sobre el ticket, sugiriendo causa raíz y comando o workaround aplicable.

- **Respuestas:**
  - `200 OK`:
    ```json
    {
      "ticket_id": "TICK-202609-0801",
      "autofix_status": "PROPOSED",
      "proposed_action": "Restart Token Auth Service",
      "command": "systemctl restart quantux-auth-token.service",
      "confidence": 0.94
    }
    ```

---

### 3.3. Directorio de Usuarios y Roles (`/api/v1/users`)

#### `GET /api/v1/users`
Lista los usuarios registrados con soporte de filtros.

- **Query Parameters:**
  - `role` (opcional): `ADMIN` | `TEAM_LEADER` | `SOPORTE` | `SOLICITANTE`
  - `support_level` (opcional): `N1` | `N2` | `N3`
- **Respuestas:** `200 OK`: `Array<User>`

#### `GET /api/v1/users/operators`
Lista específicamente a los operadores asignables de la mesa de ayuda (`SOPORTE` y `ADMIN`).

- **Query Parameters:** `level` (opcional): `N1` | `N2` | `N3`
- **Respuestas:** `200 OK`: `Array<User>`

#### `GET /api/v1/users/{user_id}`
Obtiene el perfil completo de un usuario por su identificador numérico.

#### `PUT /api/v1/users/{user_id}` y `PATCH /api/v1/users/{user_id}`
Actualiza campos del perfil de usuario (nombre, email, rol, nivel de soporte, teléfono, etc.).

- **Request Body (`UserUpdateRequest`):**
  ```json
  {
    "full_name": "Carlos Páez",
    "email": "cpaez@quantux.com",
    "role": "SOPORTE",
    "support_level": "N2",
    "phone": "+54 11 5555-0123"
  }
  ```
- **Respuestas:** `200 OK`: Objeto `User` actualizado.

#### `PATCH /api/v1/users/{user_id}/toggle-status`
Habilita o deshabilita a un usuario en el sistema (`is_active = !is_active`).

---

### 3.4. Catálogos Maestros, Acuerdos de Nivel de Servicio (SLA) y Base de Conocimiento (`/api/v1`)

#### `GET /api/v1/platforms` y `POST /api/v1/platforms`
Lista y registra plataformas de software asistencial homologadas (ej. `CAT_RECETA`, `CAT_CONSULTORIO_DIGITAL`, etc.).

#### `GET /api/v1/institutions` y `POST /api/v1/institutions`
Lista y registra instituciones clientes y prestadores de salud (ej. `OSDE`, `SWISS_MEDICAL`, `SANATORIO_FINOCHIETTO`, etc.).

#### `GET /api/v1/calculate-priority`
Calcula la prioridad ITIL y los tiempos comprometidos de SLA en minutos en base al impacto y la urgencia.

- **Query Parameters:**
  - `impact`: `BAJO` | `MEDIO` | `ALTO` | `CRITICO`
  - `urgency`: `BAJO` | `MEDIO` | `ALTA` | `CRITICA`
- **Respuestas:**
  - `200 OK` (`PriorityCalculationResponse`):
    ```json
    {
      "impact": "CRITICO",
      "urgency": "CRITICA",
      "priority": "P1",
      "sla_response_time_minutes": 15,
      "sla_resolution_time_minutes": 60
    }
    ```

#### `GET /api/v1/institutions/{institution_code}/sla`
Obtiene las políticas de SLA vigentes (específicas o heredadas de la directiva `GLOBAL`).

#### `PUT /api/v1/institutions/{institution_code}/sla`
Configura políticas personalizadas de SLA para una institución específica.

- **Request Body:**
  ```json
  {
    "p1_response_min": 10,
    "p1_resolution_min": 45,
    "p2_response_min": 20,
    "p2_resolution_min": 90
  }
  ```

#### `GET /api/v1/sla/policies`
Lista el mapa completo de políticas de SLA configuradas en el sistema.

#### `GET /api/v1/config/helpdesk-levels`
Devuelve la configuración y competencias operativas de las mesas ITIL N1, N2 y N3.

#### `GET /api/v1/metrics/operational`
Devuelve métricas operativas globales para tableros de control y cockpits.

#### `GET /api/v1/articles` y `POST /api/v1/articles`
Endpoints CRUD para la Base de Conocimiento (Knowledge Base). Soporta versionado semántico y categorización por subsistema clínico.

#### `GET /api/v1/articles/{article_id}/history`
Historial de auditoría de versiones del artículo de la Base de Conocimiento.

#### `POST /api/v1/articles/{article_id}/vote`
Registra retroalimentación de utilidad del artículo por parte de médicos o agentes.

---

### 3.5. Torre de Control y Liderazgo de Operaciones (`/api/v1/team-leader`)

#### `GET /api/v1/team-leader/overview`
Provee una visión consolidada en tiempo real para el Team Leader de Guardia:
- Conteo de P1 activos.
- Tickets sin asignar en cola de guardia.
- Alertas de rescate por baja satisfacción CSAT (1-2 estrellas).
- Matriz de carga operativa balanceada por cada operador de soporte.

- **Query Parameters:** `institution_code` (opcional)
- **Respuestas:** `200 OK`

#### `POST /api/v1/team-leader/reassign`
Reasigna un caso de forma directa a otro operador para rebalancear la carga.

- **Request Body:**
  ```json
  {
    "ticket_id": "TICK-202609-0801",
    "assigned_to_username": "cpaez",
    "reason": "Rebalanceo por saturación de guardia",
    "team_leader_username": "cdaneri"
  }
  ```

#### `POST /api/v1/team-leader/rescue/{ticket_id}`
Abre un plan de rescate y service recovery ante una insatisfacción asistencial.

- **Request Body:**
  ```json
  {
    "rescue_notes": "Contacto telefónico directo con la Dirección Médica del Sanatorio",
    "team_leader_username": "cdaneri"
  }
  ```

#### `POST /api/v1/team-leader/auto-rebalance`
Ejecuta el algoritmo heurístico de balanceo automático equitativo entre operadores activos.

---

### 3.6. Ingeniería N3 y Software Releases (`/api/v1/releases`)

#### `GET /api/v1/releases`
Lista las versiones de software planificadas, en desarrollo y desplegadas, incluyendo los tickets vinculados a cada versión.

#### `POST /api/v1/releases`
Crea una nueva versión de software (ej. `v4.1.0-RC1`).

#### `PATCH /api/v1/releases/{release_id}/status`
Actualiza el estado de la versión en el pipeline (`PLANIFICADA` &rarr; `TESTING` &rarr; `DESPLEGADA`).

#### `POST /api/v1/releases/link-ticket`
Vincula un ticket de error o mejora a una versión de software candidata a release.

#### `POST /api/v1/releases/{release_id}/deploy`
Despliega la versión en producción y resuelve de forma automática y sincronizada todos los tickets vinculados a la versión con trazabilidad Git.

---

### 3.7. Asistente Cognitivo IA y Chat Asistencial (`/api/v1/ai`)

#### `POST /api/v1/ai/triage`
Ejecuta el motor de análisis cognitivo N3 sobre el síntoma clínico reportado por el médico, devolviendo diagnóstico predictivo, artículo KB aplicable y dictamen forense.

- **Request Body:**
  ```json
  {
    "query": "No puedo firmar digitalmente la receta electrónica, sale error de token",
    "platform_code": "CAT_RECETA",
    "institution_code": "OSDE",
    "requester_username": "solicitante"
  }
  ```

#### `POST /api/v1/ai/resolve-incident`
Cierra la incidencia vía autogestión asistida cuando el profesional confirma la solución en el chat.

#### `POST /api/v1/ai/escalate-incident`
Escala la conversación a un ticket formal en la Mesa de Ayuda incorporando la transcripción y el dictamen técnico.

#### `POST /api/v1/ai/chat/message` y `GET /api/v1/ai/chat/history/{ticket_id}`
Intercambio de mensajes en vivo en el chat contextual del ticket.

#### `GET /api/v1/ai/deflection-metrics`
Métricas de deflexión asistencial logradas por el asistente de IA sin intervención humana.

---

### 3.8. Gestor de Archivos y Adjuntos Forenses (`/api/v1/files`)

#### `POST /api/v1/files/upload`
Carga de archivos adjuntos (capturas de pantalla de error, logs o certificados).
- **Content-Type:** `multipart/form-data`
- **Límites:** Tamaño máximo de 20 MB. Extensiones permitidas: `.png`, `.jpg`, `.jpeg`, `.pdf`, `.log`, `.txt`, `.csv`, `.json`, `.xml`.
- **Integridad:** Cálculo automático de checksum criptográfico SHA-256.

#### `GET /api/v1/files/ticket/{ticket_id}`
Lista los adjuntos asociados al ticket.

#### `GET /api/v1/files/download/{filename}`
Descarga segura del archivo físico mediante `FileResponse`.

#### `GET /api/v1/files/bot/status`
Estado del servicio de monitorización y limpieza de adjuntos temporales.

---

### 3.9. Monitoreo de Salud (`/health`)

#### `GET /health`
Verifica el estado del servicio, versión de la API y entorno.

- **Respuestas:**
  - `200 OK`:
    ```json
    {
      "status": "healthy",
      "version": "4.0.0-DEV",
      "environment": "Cloud Development (v4.0.0-DEV)",
      "timestamp": "2026-09-19T10:00:00Z"
    }
    ```
