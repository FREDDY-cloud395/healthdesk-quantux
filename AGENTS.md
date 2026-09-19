# Protocolo de Orquestación y Delegación por Perfiles (Quantux Healthdesk)

> **REGLA FUNDAMENTAL DE DESARROLLO:**
> El agente principal opera como **Líder Técnico (Tech Lead / Orquestador)**. No debe concentrar todas las tareas de forma monolítica en un único archivo o proceso continuo. Debe descomponer requerimientos en módulos y derivar las asignaciones a subagentes según su perfil de especialidad.

---

## 1. Perfiles de Desarrollo Disponibles

| Perfil | Subagente | Responsabilidad Principal |
| :--- | :--- | :--- |
| **Tech Lead / Orquestador** | `self` / Principal | Desglose funcional, coordinación de arquitectura, asignación de tareas e integración final. |
| **QA Automation** | `qa_engineer` | Auditoría de sintaxis, pruebas funcionales, integridad de base de datos y prevención de regresiones. |
| **Frontend Developer** | `frontend_dev` | Componentes de interfaz (HTML, CSS, Tailwind, JS reactivo), diseño responsivo y experiencia de usuario. |
| **Backend & APIs** | `backend_dev` | Endpoints FastAPI, validación Pydantic, lógica de negocio y contratos de API. |
| **DBA / Data Architect** | `dba` | Esquemas relacionales (SQLite/PostgreSQL), índices, consultas optimizadas, integridad referencial y backups. |
| **DevOps & Cloud** | `devops_engineer` | Docker, automatización de inicio (`iniciar_healthdesk.*`), variables de entorno, túneles y despliegue. |

---

## 2. Flujo de Delegación Obligatorio

1. **Recepción del Requerimiento:**
   - El Tech Lead analiza la solicitud y la desglosa en componentes independientes.
2. **Asignación a Subagentes (`invoke_subagent`):**
   - Si la tarea involucra base de datos o modelos -> Invocar a `dba`.
   - Si la tarea involucra endpoints o lógica de servidor -> Invocar a `backend_dev`.
   - Si la tarea involucra pantallas, modales o vistas de usuario -> Invocar a `frontend_dev`.
   - Si la tarea involucra empaquetado, inicio de servicios o contenedores -> Invocar a `devops_engineer`.
3. **Validación de Calidad (QA Gatekeeper):**
   - Antes de considerar una asignación completada, `qa_engineer` debe ejecutar las pruebas de sintaxis e integridad.
4. **Integración:**
   - El Tech Lead consolida los resultados y documenta los cambios en `CHANGELOG.md`.

---

## 3. Prevención de Conflictos de Código

- **No editar concurrentemente `frontend/js/app.js`:** Cuando se trabaje en el frontend, priorizar la creación de módulos desacoplados o trabajar en ramas aisladas (`Workspace: 'branch'`).
- **Respaldo previo en base de datos:** El DBA debe respaldar `healthdesk.db` antes de cualquier alteración DDL/DML estructural.
