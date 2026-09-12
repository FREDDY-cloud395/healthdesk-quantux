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

### 3. Enfoque de Desarrollo y Adaptación Metodológica
El proyecto adopta un marco Ágil (Iterativo e Incremental) bajo la modalidad Scrumban estructurado en 5 ciclos semanales con gestión visual de flujo:
1. **Enfoque de Desarrollo:** Ciclo iterativo e incremental en 5 Sprints para validar software funcional utilizable cada semana.
2. **Adaptación a Quantux:** Alineación al modelo operativo de soporte para las plataformas y clientes institucionales.
3. **Adaptación al Proyecto:** Estructuración sobre los 5 pasos del flujo y panel centralizado de operación (Cockpit).
4. **Mejora Continua:** Revisiones periódicas para calibrar y ajustar prioridades de entrega con los referentes.

---

### 4. Estructura de Roles y Matriz RACI de Gobernanza
| Actividad / Hito de Gestión | Solution Owner | Ref. Funcional | Fac. Técnico | Cap. Humano | Gerencia Gral. |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Definición de Alcance y Plan de Gestión | **R / A** | C | C | I | I |
| Aprobación de Requerimientos y Backlog | **R** | **A** | C | I | I |
| Diseño y Construcción del Incremento | **R / A** | I | C | I | I |
| Validación de la Demo Operativa E2E | **R** | **A** | C | I | I |
| Aprobación Final del Proyecto | **R** | C | C | C | **A** |

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
* **Sprint 5 (21-sep al 25-sep):** *Estabilización, QA y Cierre.*
  * Entregables: Dataset de prueba cargado, pruebas completas y **ENTREGA FINAL DEL PROYECTO**.

---

### 7. Catálogo de Entregables del Proyecto
1. **Paquete Documental:**
   * Doc 01: Plan de Gestión del Proyecto.
   * Doc 02: Especificación Funcional y Backlog.
   * Doc 03: Arquitectura y Diseño Técnico.
   * Doc 04: Guía de Demostración Operativa.
   * *Criterio de Aceptación:* Aprobación formal por el Comité Evaluador.
2. **Paquete de Software:**
   * Aplicación Backend con base de datos configurada.
   * Frontend de operación Cockpit en pantalla única.
   * Dataset de prueba con las 9 plataformas y 14 clientes precargados.
   * *Criterio de Aceptación:* Ejecución funcional sin errores ni dependencias externas.
3. **Paquete de Calidad:**
   * Validación del circuito de estados y reglas de negocio.
   * Historial de auditoría completo.
   * Checklist del caso de demo (5 pasos).
   * *Criterio de Aceptación:* Cumplimiento del criterio de éxito del MVP.

---

### 8. Gestión Preventiva de Riesgos del Proyecto
* **R-01: Desvío del Alcance (Nivel: ALTO)**
  * *Riesgo:* Incorporar funcionalidades fuera del MVP.
  * *Mitigación:* Blindaje estricto en los puntos del MVP; lo demás queda formalmente diferido.
* **R-02: Interfaz Poco Intuitiva (Nivel: ALTO)**
  * *Riesgo:* Dificultad de adopción por operadores de soporte o solicitantes.
  * *Mitigación:* Validar pantallas y usabilidad de forma temprana con el Referente Funcional.
* **R-03: Demoras en Integración E2E (Nivel: ALTO)**
  * *Riesgo:* Falla o demora en conectar el circuito de 5 pasos.
  * *Mitigación:* Flujo principal conectado y probado al cierre de la Semana 3.
* **R-04: Modelado Inadecuado (Nivel: MEDIO)**
  * *Riesgo:* Categorías o prioridades no alineadas a las plataformas reales.
  * *Mitigación:* Parametrizar categorías y prioridades con el Referente Funcional.
