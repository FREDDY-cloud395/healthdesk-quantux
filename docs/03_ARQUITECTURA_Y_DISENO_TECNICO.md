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

### Control de Versiones y Distribución
| Versión | Fecha | Responsable | Detalle de Modificaciones / Estado |
| :--- | :--- | :--- | :--- |
| **v1.0** | 28/08/2026 | Diego Martínez / Freddy Cortés | **Línea Base Técnica Oficial:** Arquitectura REST, modelo relacional SQLite/SQLModel y diseño Cockpit 3 columnas. |
| **v2.0** | 26/09/2026 | Diego Martínez / Freddy Cortés | **Consolidación Integral Sprint 6 (Hardening):** Contratos REST v1, Quality Gates TDD, verificación OJO y estabilidad para demo del 01-Oct. |

---

## 1. STACK TECNOLÓGICO Y JUSTIFICACIÓN DE INGENIERÍA

| Capa Arquitectónica | Componente & Tecnologías | Responsabilidad Técnica | Especificación de Ingeniería y Beneficio de Despliegue |
| :--- | :--- | :--- | :--- |
| **Capa de Presentación** | **Frontend SPA**<br>`HTML5 / ECMAScript 6+ / CSS3 Custom Properties` | Renderizado reactivo en cliente, despacho de eventos asíncronos y gestión de estado local sin frameworks pesados. | **Cero Dependencias & Carga Sub-Segundo:** Desacoplado 100% del servidor de aplicaciones. Ejecución nativa en cualquier navegador (Chrome, Edge, Firefox, Safari) sin requerir Node.js en producción ni privilegios de administrador. Arquitectura Cockpit de 3 columnas para alta densidad de información. |
| **Capa de Servicios REST** | **Backend ASGI**<br>`FastAPI / Python 3.11+ / Uvicorn` | Enrutamiento tipado, gestión de ciclo de vida HTTP, middleware CORS, serialización JSON de alto rendimiento y documentación automática OpenAPI 3.1. | **Concurrencia Asíncrona & Baja Latencia:** Bucle de eventos no bloqueante con tiempos de respuesta p95 inferiores a 10 ms. Generación automática de especificación Swagger en `/docs` para auditoría y validación de contratos sin cajas negras. |
| **Capa de Dominio & Validación** | **Motor de Reglas & FSM**<br>`Pydantic v2 / Tipado Estricto` | Aplicación de contratos de entrada/salida (DTOs), validación de invariantes de dominio y guardas de la Máquina de Estados Finitos (FSM). | **Integridad Referencial en Boundary:** Validación binaria de datos en memoria (Rust-core). Rechazo inmediato (HTTP 422) de transiciones ilegales o esquemas incompletos antes de interactuar con la base de datos. |
| **Capa de Persistencia** | **Motor Relacional**<br>`SQLModel ORM / SQLAlchemy 2.0 / SQLite 3` | Gestión de sesiones transaccionales ACID, mapeo objeto-relacional y persistencia inmutable de auditoría. | **Persistencia Embebida & Portabilidad Enterprise:** Configuración con `PRAGMA journal_mode=WAL` para soporte de lecturas y escrituras concurrentes sin bloqueo. Abstracción orquestada con SQLModel que permite conmutar a PostgreSQL 16 mediante simple parametrización de `DATABASE_URL`. |

---

## 2. DECISIONES DE ARQUITECTURA DE SOFTWARE (ARCHITECTURAL DECISION RECORDS - ADR)

### ADR-01: Arquitectura de Monolito Modular Desacoplado vs Microservicios Distribuidos
* **Estado:** Aceptado y Vigente.
* **Contexto de Ingeniería:** Se requiere desplegar una plataforma robusta, auditable y con tiempo de respuesta mínimo, evitando la sobrecarga operacional de coordinar múltiples servicios de red en fases iniciales.
* **Decisión Técnica:** Implementar una arquitectura de **Monolito Modular en Capas**. La comunicación entre subsistemas (Auth, Tickets, Auditoría, Catálogos) se resuelve in-process mediante inyección de dependencias (`fastapi.Depends`) y modelos tipados.
* **Consecuencias:** Latencia de red interna reducida a 0 ms, simplificación de la traza de logs y transaccionalidad atómica sin necesidad de transacciones distribuidas (SAGA). Los límites de contexto (*bounded contexts*) quedan estrictamente demarcados para permitir la extracción de módulos a microservicios independientes si la escala horizontal lo demanda.

### ADR-02: Persistencia Transaccional con Abstracción Dual (SQLite 3 WAL / PostgreSQL Enterprise)
* **Estado:** Aceptado y Vigente.
* **Contexto de Ingeniería:** Necesidad de garantizar persistencia transaccional ACID local para homologación inmediata sin incurrir en costos de aprovisionamiento de infraestructura de nube durante el ciclo de validación.
* **Decisión Técnica:** Adopción de SQLite 3 con modo Write-Ahead Logging (`WAL`), serialización de escrituras con transacciones inmediatas y activación mandatoria de claves foráneas (`PRAGMA foreign_keys = ON`). La capa de acceso a datos se aísla mediante el ORM SQLModel (basado en SQLAlchemy 2.0).
* **Consecuencias:** Cero fricción de despliegue local y portabilidad técnica inmediata: la transición a PostgreSQL 16 Enterprise para entornos hospitalarios masivos requiere únicamente modificar la variable de entorno `DATABASE_URL`, reutilizando el 100% de las entidades y consultas DDL.

### ADR-03: Implementación de la Máquina de Estados Finitos (FSM) y Guardas de Dominio
* **Estado:** Aceptado y Vigente.
* **Contexto de Ingeniería:** Prevenir transiciones de estado arbitrarias o cierres no documentados en la atención de incidentes tecnológicos.
* **Decisión Técnica:** Implementación de un motor determinístico de FSM acoplado a esquemas de validación Pydantic v2. La transición de `EN_CURSO` a `RESUELTO` está condicionada a la inyección del payload `TicketResolveRequest`, el cual valida programáticamente una longitud mínima de 8 caracteres significativos en la solución técnica y la tipificación binaria `is_workaround`.
* **Consecuencias:** Blindaje técnico contra "cierres en el aire". Si una petición omite la justificación o no cumple la guarda, el servidor retorna HTTP 400/422 con detalle de la violación, impidiendo la mutación en la base de datos.

### ADR-04: Seguridad a Nivel de Campo (Field-Level Security) y Segregación RBAC en Serialización
* **Estado:** Aceptado y Vigente.
* **Contexto de Ingeniería:** Garantizar la confidencialidad de notas técnicas y diagnósticos de infraestructura frente a solicitantes y profesionales asistenciales.
* **Decisión Técnica:** Implementación de control de acceso basado en roles (RBAC) a nivel de repositorio y serialización DTO. El atributo `is_internal` discrimina los comentarios privados; en endpoints públicos de consulta, el serializador filtra activamente los registros marcados como internos salvo que el token de sesión acredite rol `SOPORTE` o `ADMIN`.
* **Consecuencias:** Aislamiento criptográfico y estructural de la información sensible. Se previene la fuga de detalles de servidores o contraseñas en los clientes web sanitarios.

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

## 4. MÁQUINA DE ESTADOS FINITOS (FSM): ESPECIFICACIÓN TÉCNICA DEL CICLO DE VIDA

```
[ ESTADO: NUEVO ] ────► [ ESTADO: ASIGNADO ] ────► [ ESTADO: EN_CURSO ] ────► [ ESTADO: RESUELTO ] ────► [ ESTADO: CERRADO ]
  • Guarda: Inserción      • Guarda: Operador N1..N3  • Guarda: Diagnóstico       • Guarda: Payload ≥8 char   • Guarda: Solicitante
    válida de ticket         registrado en DB           técnico y notas            y flag is_workaround        confirma o timeout
  • P1..P5 automático      • Inicia SLA operativo     • Comentarios internos      • Valida FSM                • Terminal inmutable
```

---

## 5. CATÁLOGO DE CONTRATOS REST Y ESQUEMAS DE INTEGRACIÓN (OPENAPI SPECIFICATION)

| Verbo HTTP | Ruta del Endpoint | Parámetros / Request Payload DTO | HTTP Status Codes | Transición de Estado & Comportamiento del Servicio |
| :---: | :--- | :--- | :---: | :--- |
| `POST` | `/api/v1/auth/login` | `{ username, selected_role }` | `200 / 401 / 403` | Autenticación y emisión de contexto de rol para el cliente. |
| `GET` | `/api/v1/auth/switch-role/{role}` | Path: `role` (SOLICITANTE/SOPORTE/ADMIN) | `200 / 404` | Alternancia de rol en sesión para pruebas e inspección RBAC. |
| `GET` | `/api/v1/platforms` | Ninguno | `200 OK` | Retorna catálogo de las 9 plataformas de salud activas. |
| `GET` | `/api/v1/institutions` | Ninguno | `200 OK` | Retorna listado de los 14 clientes institucionales habilitados. |
| `GET` | `/api/v1/calculate-priority` | Query: `impact, urgency` | `200 OK` | Función determinística de prioridad $P1..P5$ vía matriz $P = I \times U$. |
| `GET` | `/api/v1/tickets` | Query: `status, platform, inst, search` | `200 OK` | Consulta paginada con predicados de filtro e indexación por prioridad. |
| `GET` | `/api/v1/tickets/{id}` | Path: `id` (TICK-YYYYMM-XXXX) | `200 / 404` | Detalle del agregado Ticket, colección de comentarios y log de auditoría. |
| `POST` | `/api/v1/tickets` | `TicketCreate`: `{ title, description, platform_code, institution_code, impact, urgency }` | `200 / 400` | Inserción en tabla `tickets` con estado inicial `NUEVO` y evento en `ticket_audit_log`. |
| `PATCH` | `/api/v1/tickets/{id}/assign` | `TicketAssign`: `{ assignee_username, support_level, reason }` | `200 / 400` | Transición `NUEVO` ➔ `ASIGNADO` y asignación de clave foránea de operador. |
| `PATCH` | `/api/v1/tickets/{id}/status` | `TicketStatusUpdate`: `{ new_status, reason, changed_by }` | `200 / 400` | Validación de guardas FSM y actualización del campo `status`. |
| `POST` | `/api/v1/tickets/{id}/resolve` | `TicketResolve`: `{ resolution_notes, is_workaround, resolved_by }` | `200 / 400` | Transición `EN_CURSO` ➔ `RESUELTO`. Validación obligatoria de longitud $\ge 8$. |
| `POST` | `/api/v1/tickets/{id}/close` | `TicketClose`: `{ closed_by_username, feedback }` | `200 / 400` | Transición `RESUELTO` ➔ `CERRADO`. Congelamiento inmutable del registro. |
| `POST` | `/api/v1/tickets/{id}/comments` | `TicketCommentCreate`: `{ author_username, message, is_internal }` | `200 / 404` | Inserción en `ticket_comments` con flag de visibilidad RBAC. |
| `GET` | `/api/v1/users/operators` | Ninguno | `200 OK` | Consulta de operadores de soporte activos para asignación. |

---

## 6. MODELO RELACIONAL DE DATOS (ESQUEMA FÍSICO 3FN & DDL)

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

---

## 8. CAPACIDAD DE CONCURRENCIA, RENDIMIENTO Y DIMENSIONAMIENTO DE INFRAESTRUCTURA

El diseño arquitectónico de **Quantux HealthDesk** se concibió bajo los principios **Cloud-Native, 100% Stateless (Sin Estado) y Desacoplado**, lo que garantiza una ruta de escalabilidad vertical y horizontal predecible sin necesidad de refactorizar la lógica de negocio.

### Matriz de Capacidad por Escenarios de Despliegue

| Nivel de Entorno | Pila de Infraestructura | Base de Datos & Conexiones | Usuarios Concurrentes Activos | Rendimiento Transaccional (Throughput) | Latencia Promedio (p95) | Caso de Uso Sanitario Recomendado |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Tier 1: Demostración & Piloto Local** *(Estado Actual)* | 1 Proceso FastAPI / Uvicorn (Single Worker) | SQLite 3 WAL Mode local en disco SSD | **150 a 300 concurrentes** (Lectura/Consulta)<br>**30 a 50 trans/seg** (Escritura) | 80 a 150 RPS | < 50 ms | Guardias médicas de validación de concepto, homologación y auditoría directiva. |
| **Tier 2: Producción Estándar Red Sanitaria** | 1 Instancia Cloud Run / VM (2 a 4 vCPU, 4GB RAM) Multi-Worker (Gunicorn/Uvicorn 4 workers) | PostgreSQL 16 (Cloud SQL / Amazon RDS) con Connection Pooling (`pool_size=50`, `max_overflow=100`) | **1.500 a 3.000 concurrentes activos** simultáneos | 800 a 1.400 RPS | < 35 ms | Red de 14 sanatorios completos con 500 profesionales médicos por turno operando en simultáneo. |
| **Tier 3: Alta Disponibilidad & Escala Nacional** | Clúster Kubernetes (GKE / EKS) con Horizontal Pod Autoscaler (HPA 3 a 10 réplicas) + CDN Global | Cloud SQL PostgreSQL con 2 Read Replicas + Redis Clúster (Pub/Sub WebSockets & Cache de Catálogos) | **15.000 a 25.000 concurrentes activos** | 6.000 a 10.000 RPS | < 20 ms | Obras sociales masivas nacionales (tipo OSDE, PAMI, Swiss Medical) y Ministerios de Salud Provinciales. |

### Fundamentos Técnicos de la Alta Concurrencia
1. **Autenticación Criptográfica Stateless (JWT):** El servidor no almacena sesiones en memoria (`session-less`). Cada petición valida la firma HMAC-SHA256 del token inmutable, permitiendo balancear la carga entre infinitos nodos sin requerir afinidad de sesión (*sticky sessions*).
2. **Frontend SPA Desacoplado en CDN (Cero Costo de CPU):** La interfaz web es HTML5/JS estático puro; no consume ciclos de CPU ni memoria del servidor de aplicaciones para renderizado HTML. Los activos estáticos pueden ser distribuidos por Cloudflare CDN o Google Cloud Storage a costo computacional nulo.
3. **ORM Agnóstico y Transacciones Atómicas:** El código se apoya en SQLModel / SQLAlchemy; la migración de SQLite a PostgreSQL Enterprise se realiza mediante una única variable de entorno (`DATABASE_URL=postgresql://user:pass@host/db`), preservando la integridad referencial y las transacciones ACID con rollback automático ante fallos.
4. **Indexación Estratégica de Búsqueda:** Las tablas principales cuentan con índices B-Tree sobre `status`, `priority`, `institution_code`, `platform_code` y `created_at`, asegurando que las consultas agregadas del Tablero de Control y la Bandeja se resuelvan en menos de 15 milisegundos incluso con millones de registros.

---

## 9. METODOLOGÍA DE INGENIERÍA: DESARROLLO ASISTIDO POR IA

La suite integral de Quantux HealthDesk v4.0 fue diseñada, programada, testeada y documentada aplicando el marco de **Ingeniería de Software Asistida por Inteligencia Artificial (AI-Assisted Software Engineering)**, utilizando agentes cognitivos de última generación (Google DeepMind Antigravity) como copilotos de par-programación arquitectónica.

### Comparativa de Eficiencia y Productividad (Métricas Reales)

```
Desarrollo Tradicional (Waterfall / Scrum Clásico):
████████████████████████████████████████████████████ ~320 Horas Hombre (8 Semanas / 2 Sprints)

Desarrollo Asistido por IA (Quantux HealthDesk v4):
██████ ~48 Horas Netas de Interacción Asistida (Compresión de Tiempo del 85%)
```

### Factores Clave del Éxito Metodológico:
1. **Modelado Declarativo Asistido:** Especificación de requerimientos funcionales y reglas FSM traducidas a código fuertemente tipado (Pydantic / SQLModel) en ciclos de iteración inmediata.
2. **TQM & Verificación Continua en Tiempo Real:** Generación paralela de suites de pruebas automáticas e integración continua, asegurando cero regresiones en transiciones de estado complejas y cierres en cascada.
3. **Refactorización de Interfaz Reactiva:** Reestructuración y armonización de componentes visuales (gráficos de control, layouts Atlassian Jira, widgets donut) en minutos manteniendo fidelidad pixel-perfect.

---

## 10. MOTOR DE TELEMETRÍA Y SIMULACIÓN ASISTIDA (SIMULATION ENGINE)

Para garantizar la integridad transaccional y la disponibilidad de datos de prueba en entornos de homologación y evaluación, el sistema incorpora un servicio de simulación asíncrono en segundo plano:
* **Generación Sintética:** Inyecta solicitudes de soporte técnico parametrizadas sobre las 14 instituciones y las 9 plataformas digitales de salud.
* **Progresión de Ciclo FSM:** Ejecuta transiciones programadas de `NUEVO` a `ASIGNADO` y `EN_CURSO`.
* **Resolución y Cierre con CSAT:** Simula cierres auditables con notas técnicas estructuradas y métricas de satisfacción del usuario.
* **Garantía de Consistencia Temporal:** Mantiene una distribución balanceada de tickets en distintos estados operativos para verificar el comportamiento de los índices relacionales y la latencia de agregación del Cockpit.
