# 📑 DOCUMENTO 1: PLAN DE GESTIÓN DEL PROYECTO
**Código:** DOC-MGT-001 (Versión 1.0 Oficial)
**Proyecto:** HealthDesk Quantux — Sistema Centralizado de Gestión de Tickets de Soporte
**Organización:** Quantux Salud
**Solution Owner:** Freddy Cortés (Analista Funcional)
**Fecha:** 28 de Agosto de 2026
**Comité Evaluador:**
• Paula Sbarbati (Referente Funcional)
• Diego Martínez (Facilitador Técnico)
• Carolina Brizuela (Capital Humano)
• Nicolás Sánchez (Gerencia General)

---

### Control de Versiones y Distribución
| Versión | Fecha | Responsable | Detalle de Modificaciones / Estado |
| :--- | :--- | :--- | :--- |
| **v0.1** | 24/08/2026 | Freddy Cortés | Estructuración inicial del alcance y relevamiento de soporte. |
| **v0.2** | 26/08/2026 | Freddy Cortés | Calibración de roles, matriz de esfuerzo y riesgos preventivos. |
| **v1.0** | 28/08/2026 | Freddy Cortés | **Versión Oficial de Línea Base del MVP.** |
| **v1.1** | 26/09/2026 | Freddy Cortés | **Fase de Hardening, Scope Freeze, Deadline Técnico 28-Sep y Evaluación en Proceso & Calidad.** |

---

### 1. Identificación y Gobernanza del Proyecto

#### 1.1. Ficha del Proyecto
* **Proyecto:** HealthDesk Quantux
* **Solution Owner:** Freddy Cortés (Analista Funcional)
* **Referente Funcional:** Paula Sbarbati
* **Facilitador Técnico:** Diego Martínez
* **Capital Humano:** Carolina Brizuela
* **Gerencia General:** Nicolás Sánchez
* **Duración:** 5 Semanas (5 Sprints semanales)

#### 1.2. Propósito y Contexto Operativo
Quantux Salud opera un ecosistema tecnológico de 9 plataformas digitales que dan soporte a más de 12.000 profesionales de la salud activos, procesan 400.000 recetas mensuales y atienden los requerimientos de 14 clientes institucionales (financiadores, sanatorios y empresas de internación domiciliaria). El proyecto implementa una plataforma centralizada adaptada a la dinámica de soporte de la compañía.

---

### 2. Definición Oficial del MVP

#### MVP • 1/3 (Objetivo, Flujo y Roles)
* **Objetivo:** Demostrar un circuito completo, simple y trazable de atención de tickets.
* **Flujo Operativo de 5 Pasos:**  
  1. Crear ticket → 2. Asignar → 3. Gestionar → 4. Resolver → 5. Cerrar
* **Roles Principales:**
  * **Usuario / Solicitante:** Genera y consulta sus tickets.
  * **Operador de Soporte:** Recibe, gestiona y resuelve.
  * **Administrador:** Configura y supervisa la operación.

#### MVP • 2/3 (Alcance Funcional)
Funcionalidades mínimas necesarias para soportar el flujo end-to-end:
1. **Acceso:** Login + roles y permisos básicos.
2. **Tickets:** Alta, consulta y edición.
3. **Datos:** Título, descripción, categoría, prioridad, solicitante y fecha.
4. **Gestión:** Asignación de responsable / operador de soporte.
5. **Estados:** Nuevo → Asignado → En curso → Resuelto → Cerrado.
6. **Seguimiento:** Comentarios y actualizaciones.
7. **Historial:** Trazabilidad de cambios relevantes.
8. **Bandeja:** Listado, búsqueda y filtros básicos.
9. **Notificaciones:** Avisos básicos por asignación / cambio de estado.
10. **Administración:** Usuarios, categorías y prioridades.

* **Fuera del MVP:** SLA avanzados • automatizaciones complejas • integraciones • dashboards sofisticados • IA / chatbot.

#### MVP • 3/3 (Demo Objetivo | Historia que debe poder mostrarse)
La demo debe recorrer un caso completo, no funcionalidades aisladas:
* **01. Usuario genera solicitud:** Crea ticket, selecciona categoría/prioridad y describe el problema.
* **02. Soporte recibe y asigna:** El ticket aparece en la bandeja y se asigna a un responsable de soporte.
* **03. Operador gestiona:** Cambia estado, agrega comentarios y registra avances.
* **04. Se registra la solución:** El operador documenta la resolución y marca el ticket como resuelto.
* **05. Cierre + trazabilidad:** Se cierra el ticket y queda disponible el historial completo.
* **Criterio de éxito:** Completar el ciclo de atención con responsables, estados y trazabilidad de forma simple e intuitiva.

---

### 3. Enfoque de Desarrollo y Adaptación Metodológica (Marco PMI + IA)
El proyecto adopta un marco Ágil (Iterativo e Incremental) bajo la modalidad Scrumban estructurado en 5 ciclos semanales con gestión visual de flujo, gobernado formalmente bajo el estándar de adaptación del PMI (PMBOK® 7ª Edición) integrado con IA generativa (Ref: **DOC-GOV-008**):
1. **Paso 1 • Enfoque de Desarrollo Inicial:** Enfoque Híbrido Estricto. Fase de especificación y contratos predictiva (Spec-Driven / OpenAPI / DDL), complementada con micro-sprints adaptativos de desarrollo asistido por IA.
2. **Paso 2 • Adaptación a Quantux (Organización):** Alineación a las directrices institucionales de Quantux (`GEMINI.md`, `AGENTS.md`), restricciones negativas inquebrantables ("OJO") y estándares de interoperabilidad y datos en salud.
3. **Paso 3 • Adaptación al Proyecto:** Desglose atómico de Historias de Usuario, Test-Driven Development (TDD) con ejecución en CLI, y compuertas automáticas de calidad (`validate_ojo_compliance.py`, tests DOM).
4. **Paso 4 • Mejora Continua y Regla Mandatoria de Backlog:** Toda mejora, oportunidad de mejora (OM) o gap técnico/funcional DEBE canalizarse obligatoriamente como una tarjeta en la columna **Product Backlog** del Tablero Scrumban (`00_Tablero_Scrumban_Quantux.html`), conteniendo la documentación completa o su enlace directo (`doc_link`). Queda prohibido el desarrollo "al vuelo" sin tarjeta en el Backlog.

---

### 4. Estructura de Roles y Matriz RACI de Gobernanza
| Actividad / Hito de Gestión | Solution Owner | Ref. Funcional | Fac. Técnico | Cap. Humano | Gerencia Gral. | Agente IA |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Definición de Alcance y Plan de Gestión | **R / A** | C | C | I | I | C |
| Aprobación de Requerimientos y Backlog | **R** | **A** | C | I | I | C |
| Priorización de Mejoras/Gaps en Product Backlog | **R / A** | C | C | I | I | R (Alta) |
| Diseño y Construcción del Incremento (TDD) | **A** | I | C | I | I | **R** |
| Validación de Calidad y Gatekeepers OJO | **A** | I | C | I | I | **R** |
| Validación de la Demo Operativa E2E | **R** | **A** | C | I | I | I |
| Aprobación Final del Proyecto | **R** | C | C | C | **A** | I |

*Referencias: **R** (Responsable de ejecución), **A** (Aprobador final), **C** (Consultado), **I** (Informado).*

---

### 5. Estimación del Esfuerzo y Capacidad del Proyecto

#### 5.1. Matriz de Dedicación por Disciplina y Sprint
| Perfil / Disciplina | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Sprint 5 | Total Dedicación |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 📋 Análisis Funcional (AF / Solution Owner) | 16 hs | 6 hs | 4 hs | 4 hs | 4 hs | **34 hs** |
| 🎨 Diseño UX / UI | 8 hs | 3 hs | 8 hs | 2 hs | 1 hs | **22 hs** |
| ⚙️ Desarrollo Backend | 2 hs | 18 hs | 6 hs | 8 hs | 2 hs | **36 hs** |
| 💻 Desarrollo Frontend | 2 hs | 2 hs | 16 hs | 10 hs | 2 hs | **32 hs** |
| 🧪 Testing & Calidad (QA) | 3 hs | 5 hs | 4 hs | 10 hs | 12 hs | **34 hs** |
| 📊 Project Management | 8 hs | 4 hs | 3 hs | 4 hs | 8 hs | **27 hs** |
| **TOTAL POR SPRINT** | **39 hs** | **38 hs** | **41 hs** | **38 hs** | **29 hs** | **185 hs** |

#### 5.2. Resumen de Línea Base del Backlog por Épicas (10 Módulos del MVP)
* **EP-01: Acceso, Roles y Permisos Básicos** *(Módulo: Acceso)* → **7 SP** (Sprints 2 y 3)
* **EP-02: Tickets y Datos de Solicitud** *(Módulos: Tickets, Datos)* → **15 SP** (Sprints 2 y 3)
* **EP-03: Bandeja de Entrada y Asignación** *(Módulos: Bandeja, Gestión)* → **10 SP** (Sprints 2, 3 y 4)
* **EP-04: Ciclo de Estados y Registro de Solución** *(Módulo: Estados)* → **14 SP** (Sprints 2 y 4)
* **EP-05: Seguimiento, Notificaciones e Historial** *(Módulos: Seguimiento, Historial, Notif.)* → **9 SP** (Sprint 4)
* **EP-06: Administración y Operación Centralizada** *(Módulos: Administración, Bandeja)* → **20 SP** (Sprints 2 y 3)
* **TOTAL LÍNEA BASE DEL BACKLOG:** **75 Story Points (32 Historias de Usuario)**

---

### 6. Cronograma del Proyecto e Hitos de Entrega
* **Sprint 1 (24-ago al 28-ago):** *Planificación y Especificación de Línea Base.*
  * Entregables: Plan de Gestión y Especificación Funcional aprobados.
* **Sprint 2 (31-ago al 04-sep):** *Backend Core y Persistencia de Datos.*
  * Entregables: Servicios REST, persistencia y circuito de 5 estados operativo.
* **Sprint 3 (07-sep al 11-sep):** *Frontend Cockpit UI y Selector de Roles.*
  * Entregables: Interfaz en 3 columnas y selector rápido de roles.
* **Sprint 4 (14-sep al 18-sep):** *Integración E2E y Auditoría.*
  * Entregables: Circuito completo de 5 pasos integrado con notas e historial.
* **Sprint 5 (21-sep al 25-sep):** *Auditoría Forense TQM, Adaptación Visual y Calidad OJO.*
  * Entregables: Mitigación de gaps visuales, tablero interactivo y compliance pre-commit.
* **Sprint 6 (26-sep al 01-oct):** *Fase de Hardening, Estabilización Final y Presentación al Comité Evaluador.*
  * **Hito Rectivo (Scope Freeze Total):** Bloqueo total de nuevas funcionalidades. Foco exclusivo en Testing, Debugging, Calidad OJO y Cierre de Retrabajos (`UH-67`, `MEJ-08`).
  * **Corte Técnico Definitivo (Hardening Freeze):** **Lunes 28 de Septiembre de 2026 a las 18:00 hs.** A partir de este momento rige un congelamiento absoluto de código para blindar el tiempo de preparación.
  * **Ventana de Preparación y Ensayos del Solution Owner:** **29 y 30 de Septiembre de 2026 (48 hs blindadas e ininterrumpidas)** para ajuste de diapositivas, práctica del storytelling del MVP y simulacro de preguntas del Comité.
  * **Hito de Demostración Formal:** **01 de Octubre de 2026 — Presentación Ejecutiva y Evaluación Final del Producto ante el Comité Evaluador.**

#### 6.1. Desglose Operativo del Sprint 6 (Hardening hacia el 01-Oct)
| Fecha | Foco Operativo | Entregables / Hitos Clave |
| :--- | :--- | :--- |
| **Sábado 26/09 (Hoy)** | Blindaje de Gobernanza y Setup | Supresión de toolbar (`MEJ-08`), Scope Freeze activo en Tablero y definición técnica de retrabajo `UH-67`. |
| **Domingo 27/09** | Cierre de Retrabajos y Revisión SO | Implementación de `UH-67`, revisión de ítems en QA por el Solution Owner y emisión del Dossier Previo al Comité Evaluador. |
| **Lunes 28/09 (18:00 hs)** | **DEADLINE TÉCNICO & HARDENING FREEZE** | Ejecución masiva de suites TDD, compliance OJO 100%, congelamiento total de código y base de datos SQLite respaldada. |
| **Martes 29/09** | Ensayos del Solution Owner (Día 1) | Calibración de diapositivas ejecutivas, narrativa de los 5 pasos del MVP e integración de observaciones tempranas del Comité. |
| **Miércoles 30/09** | Ensayo General / Dry Run (Día 2) | Simulacro de pitch cronometrado (15 min) y preparación de respuestas sobre arquitectura y gobernanza. |
| **Jueves 01/10** | **DÍA D: EVALUACIÓN Y DEMO FINAL** | Demostración operativa en vivo ante Paula Sbarbati, Diego Martínez, Carolina Brizuela y Nicolás Sánchez. |

---

### 7. Catálogo de Entregables del Proyecto
1. **Paquete Documental:**
   * Doc 01: Plan de Gestión del Proyecto (DOC-MGT-001 v1.1).
   * Doc 02: Especificación Funcional y Backlog (DOC-REQ-002 v1.1).
   * Doc 03: Arquitectura y Diseño Técnico (DOC-ARC-003 v2.0).
   * Doc 04: Informe de Pruebas y Evidencias de Calidad (DOC-QA-004 v1.1).
   * Doc 05: Manual Operativo y Guía de Usuario (DOC-OPS-005 v3.0).
   * Doc 06/07: Presentación Ejecutiva y Guión de Demostración (DOC-COM-007 v1.1).
   * Doc 08: Marco de Trabajo PMI + IA y Gobernanza de Calidad (DOC-GOV-008 v1.1).
   * Dossier de Entrega Anticipada para el Comité Evaluador.
   * *Criterio de Aceptación:* Aprobación formal por el Comité Evaluador.
2. **Paquete de Software:**
   * Aplicación Backend con base de datos SQLite transaccional configurada.
   * Frontend de operación Cockpit en pantalla única y Pizarra Neutral Quantux.
   * Dataset de prueba con las 9 plataformas y 14 clientes precargados.
   * *Criterio de Aceptación:* Ejecución funcional sin errores ni dependencias externas.
3. **Paquete de Calidad:**
   * Validación del circuito de estados y reglas de negocio ITIL.
   * Historial de auditoría completo y trazabilidad de cambios.
   * Checklist del caso de demo (5 pasos del MVP).
   * 25 tests unitarios e integrales automatizados con salida Exit Code 0.
   * *Criterio de Aceptación:* Cumplimiento del criterio de éxito del MVP y cero defectos bloqueantes.

---

### 8. Gestión Preventiva de Riesgos del Proyecto
* **R-01: Desvío del Alcance (Nivel: ALTO)**
  * *Riesgo:* Incorporar funcionalidades fuera del MVP.
  * *Mitigación:* Blindaje estricto en los puntos del MVP bajo regla de **Scope Freeze**; todo requerimiento emergente queda registrado en el Product Backlog.
* **R-02: Interfaz Poco Intuitiva (Nivel: ALTO)**
  * *Riesgo:* Dificultad de adopción por operadores de soporte o solicitantes.
  * *Mitigación:* Validar pantallas y usabilidad de forma temprana con el Referente Funcional (Pizarra Neutral, Senior UX, sin saturación visual).
* **R-03: Demoras en Integración E2E (Nivel: ALTO)**
  * *Riesgo:* Falla o demora en conectar el circuito de 5 pasos.
  * *Mitigación:* Flujo principal conectado, probado y auditado en suite TDD con pre-commit gates activos.
* **R-04: Modelado Inadecuado (Nivel: MEDIO)**
  * *Riesgo:* Categorías o prioridades no alineadas a las plataformas reales.
  * *Mitigación:* Parametrizar categorías y prioridades con el Referente Funcional.
* **R-05: Déficit de Tiempo para Preparación de la Presentación (Nivel: ALTO)**
  * *Riesgo:* Que el Solution Owner llegue a la demo del 01-Oct sin tiempo suficiente para ensayar la narrativa y dominar las transiciones.
  * *Mitigación:* Adelantamiento mandatorio del Deadline Técnico al Lunes 28/09 a las 18:00 hs, reservando el 29 y 30 de Septiembre como ventanas 100% blindadas para preparación y ensayos.

#### 8.1. Matriz de Alerta Temprana de Desvíos (Early Warning System)
| Nivel de Alerta | Condición Disparadora | Momento de Control | Acción de Mitigación Inmediata |
| :---: | :--- | :--- | :--- |
| 🟢 **VERDE** | Tareas de hardening en curso normal; tests pasando al 100%. | Domingo 27/09 14:00 hs | Continuar flujo de estabilización estándar. |
| 🟡 **AMARILLO** | Retrabajo `UH-67` presenta demoras en pruebas o ajustes. | Domingo 27/09 16:00 hs | Simplificación técnica del componente acotada exclusivamente al caso de demo sin tocar lógica profunda. |
| 🔴 **ROJO** | Cualquier fallo técnico que persista pasadas las 14:00 hs del Lunes 28/09. | Lunes 28/09 14:00 hs | **Descope Preventivo Inmediato:** Se mueve el ítem observado al Product Backlog. **Bajo ninguna circunstancia se extiende el deadline técnico de las 18:00 hs.** |

---

### 9. Estrategia de Evaluación del Comité: Enfoque en Proceso de Desarrollo y Calidad
El Comité Evaluador ha determinado priorizar la evaluación del **Proceso de Desarrollo** y el **Aseguramiento de Calidad**, constituyendo este enfoque la principal fortaleza diferencial del proyecto:

1. **Fortalezas en Proceso de Desarrollo (Marco PMI + IA):**
   * **Trazabilidad Integral Bidireccional:** Conexión estricta entre cada Historia de Usuario, su criterio Gherkin en `DOC-SPEC-002`, su tarjeta en el Tablero Scrumban y su commit versionado en Git.
   * **Adaptación Metodológica PMBOK® 7ª Edición:** Gobernanza formal bajo estándar híbrido (`DOC-GOV-008`), delimitación estricta de roles (RACI) y política de no alucinación.
   * **Control Visual en Tiempo Real:** Tablero Scrumban interactivo con 6 columnas, visualización de métricas de velocidad (Velocity Chart) y roadmap sincronizado.
2. **Fortalezas en Calidad y Estabilización Técnica (Hardening):**
   * **Compuertas de Calidad Pre-Commit (Quality Gates):** Hook automatizado en `.git/hooks/pre-commit` que bloquea commits que no superen el 100% de las pruebas o violen restricciones.
   * **Regla OJO y Pizarra Neutral:** Validación automatizada con `validate_ojo_compliance.py` (cero tarjetas rotas, cero colores rojos invasivos, cero terminología clínica en sistemas TI).
   * **Auditoría Forense TQM y Coherencia Visual:** Documento comparativo que certifica la fidelidad visual de la implementación frente a los mockups oficiales.
   * **Cobertura de Pruebas Automatizadas:** 25 tests unitarios y de integración (DOM, backend ITIL, bot gestor y catálogo multi-tenant) ejecutados con éxito permanente.
