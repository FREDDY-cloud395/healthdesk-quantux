# 📘 DOCUMENTO DE ARQUITECTURA DE SOFTWARE Y DISEÑO TÉCNICO
**Código Documental:** DOC-ARC-003 (Versión 2.0 Definitiva Integral)  
**Proyecto:** HealthDesk Quantux — Sistema Centralizado de Gestión de Tickets de Soporte  
**Organización:** Quantux Salud  
**Solution Owner / Líder Funcional:** Freddy Cortés (Analista Funcional)  
**Facilitador Técnico:** Diego Martínez  
**Fecha de Emisión:** 28 de Agosto de 2026  
**Comité Evaluador de Aceptación y Gobernanza:**
• Paula Sbarbati (Referente Funcional)  
• Diego Martínez (Facilitador Técnico)  
• Carolina Brizuela (Capital Humano)  
• Nicolás Sánchez (Gerencia General)  

---

## 1. STACK TECNOLÓGICO Y FUNDAMENTACIÓN DE NEGOCIO

| Capa y Tecnología | Rol Funcional en la Operación | Justificación Técnica y Beneficio para el Negocio |
| :--- | :--- | :--- |
| **Frontend UI**<br>`HTML5 / Modern JS / CSS Quantux` | **La Pantalla Web Centralizada** que operan profesionales de la salud, solicitantes y operadores de soporte. | **Cero Instalación y Despliegue Inmediato:** Abre al instante en cualquier navegador de consultorio o tablet asistencial sin requerir permisos de Administrador de IT. Diseño Cockpit en 3 columnas que evita la dispersión de pestañas. |
| **Backend API**<br>`FastAPI / Python 3.11+` | **El Cerebro y Recepcionista** que procesa tickets, calcula prioridades y aplica reglas. | **Velocidad y Confiabilidad:** Tiempo de respuesta inferior a 10 ms (vital para incidentes críticos asistenciales). Genera automáticamente documentación interactiva (`/docs`) que permite auditar y validar cada función sin cajas negras. |
| **Validador de Reglas**<br>`Pydantic v2` | **El Inspector de Control de Calidad** que audita cada dato antes de ingresar al sistema. | **Cero Datos Corruptos y Cierre Exigido:** Rechaza tickets sin plataforma o urgencia válida. Impide taxativamente que un operador pase un ticket a "Resuelto" sin documentar la solución técnica obligatoria (≥ 8 caracteres). |
| **Persistencia Relacional**<br>`SQLite 3 + SQLModel ORM` | **El Archivador Digital Seguro** donde residen los tickets y la auditoría. | **Cero Costo en MVP + Escalabilidad a PostgreSQL:** Elimina costos de servidores de base de datos para las 5 semanas. Programado bajo estándar SQLModel; si el volumen crece a 100.000 tickets, se migra a PostgreSQL sin cambiar una sola línea funcional. |

---

## 2. GUÍA DE ARGUMENTACIÓN Y DEFENSA ANTE EL COMITÉ DIRECTIVO

### Pregunta 1: "¿Por qué no arrancamos con un sistema en la nube pesada desde el día 1?"
* **Defensa Funcional:** *"Porque el objetivo de este MVP es validar el circuito operativo de 5 pasos en 5 semanas sin incurrir en costos de infraestructura ni trabas burocráticas de IT. La arquitectura modular desacoplada nos permite pasar a cualquier nube corporativa (GCP/AWS/Azure) cuando la operación lo requiera, reutilizando el 100% del código de negocio."*

### Pregunta 2: "¿Cómo evitamos que soporte cierre tickets 'en el aire' sin resolver el problema real?"
* **Defensa Funcional:** *"El motor de reglas (Pydantic + FSM) bloquea técnicamente el paso al estado 'Resuelto' si el campo de solución técnica no está completo o tiene menos de 8 caracteres. Además, exige marcar si es solución definitiva o provisoria (Workaround) y la Caja Negra de auditoría registra la identidad del operador y la hora exacta."*

### Pregunta 3: "¿Cómo garantizamos la confidencialidad entre el Solicitante y el Soporte Interno?"
* **Defensa Funcional:** *"El modelo de datos y la API incorporan un flag nativo (`is_internal`). Los comentarios públicos son visibles para profesionales de la salud e instituciones, mientras que las notas técnicas de diagnóstico quedan estrictamente restringidas a los roles de Soporte y Administrador."*

---

## 3. ARQUITECTURA DE SOFTWARE EN CAPAS (LAYERED ARCHITECTURE)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. CAPA DE PRESENTACIÓN (FRONTEND COCKPIT)                                              │
│    • Interfaz SPA en Pantalla Única (3 Columnas: Filtros/Bandeja, Detalle, Acciones)    │
│    • Selector Rápido de Contexto de Rol (Solicitante, Operador de Soporte, Admin)      │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP / JSON
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ 2. CAPA DE SERVICIOS REST & CONTROLADORES (API GATEWAY)                                 │
│    • Enrutamiento modular: /auth, /tickets, /platforms, /institutions, /users          │
│    • Middleware CORS y documentación OpenAPI interactiva (/docs)                       │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ DTOs / Schemas Tipados
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ 3. CAPA DE DOMINIO, LÓGICA DE NEGOCIO Y MOTOR FSM                                      │
│    • Motor de Transición de Estados FSM (NUEVO ➔ ASIGNADO ➔ EN_CURSO ➔ RESUELTO ➔ CERRADO)│
│    • Algoritmo de Prioridad P = I × U (Matriz Bidimensional Impacto × Urgencia)        │
│    • Validación de notas obligatorias y control RBAC por rol                           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ SQLModel / SQLAlchemy ORM
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ 4. CAPA DE PERSISTENCIA Y ACCESO A DATOS (DATA ACCESS LAYER)                           │
│    • Transacciones ACID y normalización 3FN sobre SQLite 3 (healthdesk.db)             │
│    • Abstracción lista para migración transparente a PostgreSQL / SQL Server           │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Inserción Inmutable
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│ 5. SUBSISTEMA DE AUDITORÍA Y TRAZABILIDAD (AUDIT & COMPLIANCE)                         │
│    • Registro automático de eventos en ticket_audit_log (Fecha, Usuario, Campo, Delta) │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. CIRCUITO DE 5 PASOS DEL CICLO DE VIDA DEL TICKET

```
[ PASO 1: REGISTRAR ] ──► [ PASO 2: ASIGNAR ] ──► [ PASO 3: GESTIONAR ] ──► [ PASO 4: RESOLVER ] ──► [ PASO 5: CERRAR ]
   Estado: NUEVO            Estado: ASIGNADO        Estado: EN CURSO         Estado: RESUELTO         Estado: CERRADO
  Calcula P1 a P5          Asigna Responsable     Diagnóstico técnico      Solución obligatoria     Conformidad final
   según P = I × U          y Nivel N1/N2/N3       y Notas Internas         (≥ 8 caracteres)         e inmutabilidad
```

---

## 5. CATÁLOGO COMPLETO DE ENDPOINTS REST (CONTRATOS DE INTEGRACIÓN)

| Verbo | Ruta del Endpoint | Parámetros / Request Payload | HTTP Status | Regla de Negocio / Efecto en el Sistema |
| :---: | :--- | :--- | :---: | :--- |
| `POST` | `/api/v1/auth/login` | `{ username, selected_role }` | `200 / 401 / 403` | Valida credenciales. Si coincide el rol, devuelve perfil y `landing_view`. |
| `GET` | `/api/v1/auth/switch-role/{role}` | Path: `role` (SOLICITANTE/SOPORTE/ADMIN) | `200 / 404` | Alterna en 1 clic el rol activo del usuario para pruebas y operación del Cockpit. |
| `GET` | `/api/v1/platforms` | Ninguno | `200 OK` | Retorna el catálogo oficial de las **9 plataformas de salud** de Quantux activas. |
| `GET` | `/api/v1/institutions` | Ninguno | `200 OK` | Retorna el listado oficial de los **14 clientes institucionales** habilitados. |
| `GET` | `/api/v1/calculate-priority` | Query: `impact, urgency` | `200 OK` | Calcula en tiempo real la prioridad P1..P5 mediante la matriz $P = I \times U$. |
| `GET` | `/api/v1/tickets` | Query: `status, platform, inst, search` | `200 OK` | Lista los tickets de la bandeja aplicando filtros y ordenando por prioridad (P1➔P5). |
| `GET` | `/api/v1/tickets/{id}` | Path: `id` (TICK-YYYYMM-XXXX) | `200 / 404` | Retorna el detalle completo del ticket, sus mensajes/notas y la traza de auditoría. |
| `POST` | `/api/v1/tickets` | **Paso 1 (Registrar):** `{ title, description, platform_code, institution_code, impact, urgency }` | `200 / 400` | Crea ticket en estado `NUEVO`, genera ID correlativo y primer registro de auditoría. |
| `PATCH` | `/api/v1/tickets/{id}/assign` | **Paso 2 (Asignar):** `{ assignee_username, support_level, reason }` | `200 / 400` | Asigna operador. Si estaba en `NUEVO`, transiciona automáticamente a `ASIGNADO`. |
| `PATCH` | `/api/v1/tickets/{id}/status` | **Paso 3 (Gestionar):** `{ new_status, reason, changed_by }` | `200 / 400` | Valida la FSM y avanza el estado operativo (ej. a `EN_CURSO` o pausa temporal). |
| `POST` | `/api/v1/tickets/{id}/resolve` | **Paso 4 (Resolver):** `{ resolution_notes, is_workaround, resolved_by }` | `200 / 400` | Transiciona a `RESUELTO`. Exige notas $\ge 8$ caracteres y flag de solución temporal. |
| `POST` | `/api/v1/tickets/{id}/close` | **Paso 5 (Cerrar):** `{ closed_by_username, feedback }` | `200 / 400` | Cierre definitivo. Valida estado previo `RESUELTO`. El ticket pasa a ser inmutable. |
| `POST` | `/api/v1/tickets/{id}/comments` | `{ author_username, message, is_internal }` | `200 / 404` | Publica comentario en el hilo o nota privada interna para el equipo de soporte. |
| `GET` | `/api/v1/users/operators` | Ninguno | `200 OK` | Lista los operadores de soporte disponibles para asignación en el Cockpit. |

---

## 6. MODELO RELACIONAL DE DATOS (DICCIONARIO DE ENTIDADES 3FN)

* **1. `users`:** `id` (PK), `username` (UK), `full_name`, `role` (SOL/SOP/ADM), `is_active`.
* **2. `platforms` (9 Catálogos Oficiales):** `id` (PK), `code` (UK), `name`, `is_active`.
* **3. `institutions` (14 Clientes Institucionales):** `id` (PK), `code` (UK), `name`, `type` (PREPAGA, SANATORIO, OBRA_SOCIAL).
* **4. `tickets` (Tabla Central del Ciclo de Vida):** `id` (PK TICK-YYYYMM-XXXX), `title`, `description`, `platform_code` (FK), `institution_code` (FK), `ticket_type`, `impact`, `urgency`, `priority` (P1..P5), `status` (NUEVO..CERRADO), `requester_username`, `assignee_username`, `support_level` (N1/N2/N3), `resolution_notes`, `is_workaround`, `created_at`, `resolved_at`, `closed_at`.
* **5. `ticket_comments`:** `id` (PK), `ticket_id` (FK), `author_username`, `message`, `is_internal`, `created_at`.
* **6. `ticket_audit_log` (Caja Negra Inmutable):** `id` (PK), `ticket_id` (FK), `changed_by_username`, `field_changed`, `old_value`, `new_value`, `change_reason`, `created_at`.

---

## 7. MÁQUINA DE ESTADOS FINITOS (FSM) Y MATRIZ DE PRIORIDAD

### Matriz de Transiciones de Estado FSM
| Estado Origen | Transición Permitida | Regla de Validación |
| :--- | :--- | :--- |
| **NUEVO** | `ASIGNADO`, `EN_CURSO` | Asigna responsable o autoasignación directa ("Tomar Ticket"). |
| **ASIGNADO** | `EN_CURSO`, `ASIGNADO` | Inicio de diagnóstico o derivación de nivel (N1 ➔ N2 ➔ N3). |
| **EN_CURSO** | `RESUELTO`, `EN_CURSO` | Exige obligatoriamente `resolution_notes` ($\ge 8$ caracteres) y flag `is_workaround`. |
| **RESUELTO** | `CERRADO`, `EN_CURSO` | Conformidad final del solicitante o reapertura técnica justificada. |
| **CERRADO** | *(Ninguna)* | **Estado Terminal:** Registro inmutable para cumplimiento y auditoría clínica. |

### Matriz de Prioridad ($P = I \times U$)
| Urgencia \ Impacto | CRÍTICO | ALTO | MEDIO | BAJO |
| :--- | :---: | :---: | :---: | :---: |
| **CRÍTICA** | **P1** | **P1** | **P2** | **P3** |
| **ALTA** | **P1** | **P2** | **P3** | **P4** |
| **MEDIA** | **P2** | **P3** | **P3** | **P4** |
| **BAJA** | **P3** | **P4** | **P4** | **P5** |
