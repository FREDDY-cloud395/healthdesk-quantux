# 📑 DOCUMENTO 8: MARCO DE TRABAJO PMI + IA, PROCESO DE ADAPTACIÓN Y ASEGURAMIENTO DE CALIDAD
**Código:** DOC-GOV-008 (Versión 1.2 Oficial - Cierre Sprint 6 & Apertura Sprint 7)  
**Proyecto:** HealthDesk Quantux — Sistema Centralizado de Gestión de Tickets de Soporte  
**Organización:** Quantux Salud  
**Solution Owner:** Freddy Cortés (Analista Funcional)  
**Fecha de Línea Base:** 26 de Septiembre de 2026 | **Fecha de Versión 1.2:** 27 de Septiembre de 2026  
**Comité Evaluador:**  
• Paula Sbarbati (Referente Funcional)  
• Diego Martínez (Facilitador Técnico)  
• Carolina Brizuela (Capital Humano)  
• Nicolás Sánchez (Gerencia General)  

---

### Control de Versiones y Distribución
| Versión | Fecha | Responsable | Detalle de Modificaciones / Estado |
| :--- | :--- | :--- | :--- |
| **v1.0** | 26/09/2026 | Freddy Cortés | **Versión Oficial de Gobernanza PMI + IA:** Adaptación Metodológica, Delimitación de Roles y Gestión de Mejoras/Gaps en Scrumban. |
| **v1.1** | 26/09/2026 | Freddy Cortés | **Fase de Hardening, Pre-commit Quality Gates, Política de Scope Freeze y Blindaje de Tiempos hacia la Demo del 01-Oct-2026.** |
| **v1.2** | 27/09/2026 | Freddy Cortés | **Cierre Formal Sprint 6 (93 tareas en Done), Protocolo Notarial Siete Llaves, Apertura Sprint 7 (13 tareas) y Gobernanza Multi-Entorno Cloud.** |

---

### 1. Diagnóstico Operativo: El Colapso de la "Instrucción Directa" en Modelos de IA

#### 1.1. La Brecha entre Lenguaje Natural y Ejecución Técnica
El desarrollo de productos digitales asistido por Inteligencia Artificial (LLMs y Agentes de Código) suele iniciarse bajo la premisa errónea de que la IA actúa como un colaborador humano senior capaz de interpretar intenciones tácitas. Cuando se opera mediante **"pasaje libre de instrucciones"**, el flujo se degrada inevitablemente:
1. **Deriva y Saturación de Contexto (*Context Drift*):** Los LLMs tienen una memoria de trabajo acotada a su ventana de contexto. Al enviar instrucciones sucesivas en chat, las restricciones iniciales se diluyen, priorizando los últimos tokens y perdiendo la arquitectura global.
2. **Alucinación de Decisiones Arquitectónicas:** Ante instrucciones como *"haz el módulo de gestión con X detalle"*, la IA llena los cientos de vacíos no especificados asumiendo patrones por probabilidad estadística, generando código inconexo con el resto de las capas.
3. **Autovalidación Ilusoria:** La IA carece de noción de verdad operativa fuera de las pruebas de ejecución. Una respuesta que "parece correcta" textualmente suele contener roturas de tipado, estados de carrera o inconsistencias de base de datos.
4. **Acoplamiento Cognitivo (Diseñar y Codificar al mismo tiempo):** Exigir al modelo que defina los requisitos, diseñe los contratos de interfaz y escriba el código en un único turno satura su capacidad de razonamiento.

#### 1.2. El Principio de Corrección: Spec-Driven & Contract-First
Para erradicar la pérdida de calidad, la interacción pasa de ser una conversación informal a un **flujo formal de ingeniería gobernado por el marco de adaptación del PMI (PMBOK® 7ª Edición)**, donde el software solo se construye contra especificaciones aprobadas y pruebas ejecutables.

---

### 2. Marco PMI: Los Cuatro Pasos del Proceso de Adaptación (*Tailoring*) con IA

El proceso de adaptación (*Tailoring*) definido por el Project Management Institute se aplica al ecosistema de Quantux asistido por IA mediante cuatro pasos inmutables:

```
┌────────────────────────────────────────────────────────────────────────┐
│  PASO 1: SELECCIONAR EL ENFOQUE DE DESARROLLO INICIAL                  │
│  Enfoque Híbrido Estricto: Predictivo en Contratos + Ágil en Sprints  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│  PASO 2: ADAPTAR PARA LA ORGANIZACIÓN (QUANTUX SALUD)                 │
│  Gobernanza Institucional, Repositorio de Reglas y Restricciones OJO   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│  PASO 3: ADAPTAR PARA EL PROYECTO (HEALTHDESK QUANTUX)                 │
│  Atomicidad de Tareas, TDD, Gatekeepers Ejecutables y Scrumban Board   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│  PASO 4: IMPLEMENTAR LA MEJORA CONTINUA (ONGOING IMPROVEMENT)         │
│  Gestión de Mejoras/Gaps en Product Backlog + Refinamiento de Reglas  │
└────────────────────────────────────────────────────────────────────────┘
```

#### Paso 1: Seleccionar el Enfoque de Desarrollo Inicial
* **Enfoque Híbrido Estricto:**
  * **Fase Predictiva (Upfront Contracts):** Ningún componente se programa sin contar con modelos de datos (DDL), contratos de API (OpenAPI/schemas) y criterios de aceptación formalizados en lenguaje Gherkin (*Dado / Cuando / Entonces*).
  * **Fase Adaptativa (AI Sprints):** Ciclos de micro-desarrollo atómicos (15 a 30 minutos por funcionalidad) dentro del marco Scrumban, permitiendo reajustes inmediatos según los resultados de las pruebas.

#### Paso 2: Adaptar para la Organización
* **Alineación con Quantux Salud:**
  * **Estandarización de Contexto de IA:** Inyección mandatoria de directrices institucionales (`GEMINI.md`, `AGENTS.md`, `PROMPT_RESTRICCIONES_OPERATIVAS_QUANTUX.md`).
  * **Políticas Negativas Inquebrantables ("OJO"):** Prohibición terminante de terminología clínica asistencial («bypass», «guardia»), prohibición de tarjetas flotantes (*cards*), exclusividad de la paleta corporativa Quantux (pizarra neutral, fondos claros `#FFFFFF`/`#F8FAFC`, cero rojos, cero azules oscuros).
  * **Seguridad y Privacidad de Datos:** Tratamiento riguroso de identidades y datos sensibles conforme a regulaciones de salud.

#### Paso 3: Adaptar para el Proyecto
* **Ingeniería Específica de HealthDesk:**
  * **Desglose Atómico de Historias de Usuario (UH):** Cada requerimiento se fragmenta en la mínima unidad funcional indivisible para evitar que la IA pierda contexto.
  * **Compuertas de Software Automatizadas (*Automated Quality Gates*):** Obligatoriedad de ejecución de scripts de auditoría (`validate_ojo_compliance.py`, suites de tests DOM) antes de entregar cualquier bloque al Solution Owner.
  * **Trazabilidad 100%:** Cada archivo modificado o creado debe responder a un ID formal de requerimiento (UH, GAP, MEJ, OM).

#### Paso 4: Implementar la Mejora Continua
* **Bucle Sistemático de Aprendizaje:**
  * Si la IA comete un error, la solución no es insistir en el chat, sino **incorporar la regla correctiva en el archivo permanente de directrices** para inmunizar futuros desarrollos.
  * **Gestión Visual del Backlog:** Todo hallazgo, deuda técnica, oportunidad de mejora o gap se canaliza visualmente a través del Tablero Scrumban.

---

### 3. Métodos de Aseguramiento de la Calidad (QA) de Alto Rendimiento

Para garantizar calidad de nivel industrial, se implementan tres métodos complementarios:

#### 3.1. Spec-Driven Development (SDD) & Contract-First
* **La Especificación como Única Fuente de Verdad:** Antes de abrir un archivo de código (`.py`, `.js`, `.html`), la IA debe generar el artefacto de especificación detallando esquema de entrada, mutaciones, salida esperada y manejo de excepciones.
* **Aprobación Previa:** La fase de desarrollo no inicia hasta que el Solution Owner aprueba explícitamente la especificación.

#### 3.2. Test-Driven Development (TDD / ATDD) Asistido por IA
* **Ciclo Red-Green-Refactor Determinista:**
  1. El Solution Owner define los Criterios de Aceptación.
  2. La IA redacta la prueba unitaria o de integración correspondiente.
  3. La prueba **se ejecuta en el CLI (`run_command`) y debe fallar (RED)**, demostrando que evalúa la ausencia del comportamiento.
  4. La IA genera el código mínimo indispensable para satisfacer la prueba.
  5. La prueba se vuelve a ejecutar en el CLI hasta **pasar al 100% sin advertencias (GREEN)**.
  6. Se entrega el resultado adjuntando el log del terminal como evidencia objetiva.

#### 3.3. Validación en Doble Bucle (*Dual-Loop Validation*)
* **Bucle Mecánico / Sintáctico (Responsabilidad de la IA):**
  * Verificación de tipado estricto, análisis estático de código, linters, compilación y suite de pruebas unitarias. La IA no puede solicitar revisión humana si este bucle no está 100% en verde.
* **Bucle Semántico / De Negocio (Responsabilidad del Solution Owner):**
  * Validación funcional, ergonomía operativa, alineación estratégica con los 14 clientes institucionales y aprobación formal para despliegue.

---

### 4. Matriz de Límites y Responsabilidades: Solution Owner (Humano) vs. Agente de IA

La interacción hombre-máquina queda formalmente delimitada para evitar solapamientos y pérdida de control:

| Dimensión | **Solution Owner / Líder de Proyecto (Freddy Cortés - Humano)** | **Agente de IA (Antigravity / Co-piloto Técnico)** |
| :--- | :--- | :--- |
| **Definición de Alcance** | • Dueño absoluto del "Qué" y del "Por qué".<br>• Prioriza requerimientos y establece objetivos de negocio.<br>• Define los Criterios de Aceptación y el DoD (*Definition of Done*). | • **Límite Infranqueable:** No puede inventar requerimientos, ni alterar prioridades, ni asumir alcance no documentado.<br>• **Rol:** Proponer opciones técnicas y advertir riesgos de implementación. |
| **Diseño y Arquitectura** | • Aprueba los Contratos de Interfaz, DDL de base de datos y decisiones de diseño (ADRs). | • **Límite:** No puede cambiar esquemas ni contratos sin aprobación.<br>• **Rol:** Redactar borradores de especificación y mockups visuales alineados a las restricciones OJO. |
| **Construcción de Código** | • Autoriza el pase a fase de codificación tras validar la especificación. | • **Rol:** Escribir código limpio, modular y estrictamente subordinado a los contratos aprobados.<br>• Aplicar TDD riguroso. |
| **Control de Calidad (QA)** | • Valida la calidad semántica, la experiencia de usuario (UX) y el valor entregado.<br>• Aprueba el pase a producción. | • **Límite:** Prohibido autodeclarar victoria con frases como "funciona perfectamente".<br>• **Rol:** Ejecutar validadores automáticos en CLI y aportar logs de evidencia verificables. |
| **Gobernanza y Backlog** | • Administra y autoriza la transición de tarjetas entre columnas del Tablero Scrumban. | • **Rol:** Registrar de forma inmediata cualquier gap o mejora identificada como tarjeta en el **Product Backlog**, vinculando la documentación técnica. |

---

### 5. Regla Suprema Operativa: Gestión de Mejoras, Oportunidades y Gaps en el Tablero Scrumban

Queda establecida como política de gobernanza obligatoria la siguiente directriz para toda evolución del producto HealthDesk Quantux:

#### 5.1. Prohibición de Desarrollos "Al Vuelo"
Queda terminantemente prohibido a la IA y a cualquier colaborador técnico iniciar el desarrollo de una mejora, optimización o corrección sin que exista previamente su correspondiente tarjeta formalizada en la columna **Product Backlog** del Tablero Scrumban (`docs/00_Tablero_Scrumban_Quantux.html` y `docs/Backlog_HealthDesk_Quantux.csv`).

#### 5.2. Requisitos Mandatorios de Cada Tarjeta en el Backlog
Cada tarjeta incorporada debe contar con los siguientes metadatos ineludibles:
1. **Identificador Único y Tipología:**
   * `[GAP-XX]`: Para discrepancias funcionales, ausencias de especificación o defectos estructurales.
   * `[MEJ-XX]`: Para mejoras evolutivas sobre componentes o funcionalidades existentes.
   * `[OM-XX]`: Para oportunidades de mejora proactivas (rendimiento, seguridad, automatización).
2. **Estimación y Disciplina:** Story Points (SP) estimados y disciplina responsable (Backend, Frontend, DevOps, QA, AF).
3. **Documentación Completa o Enlace Directo (`doc_link`):**
   * La tarjeta debe incluir la descripción exhaustiva de la necesidad O el enlace directo al archivo de especificación en la suite documental (`docs/08_...`, `docs/API_CONTRACTS.md`, etc.).
   * Ninguna tarjeta puede ser ambigua o carecer de referencia documental.
4. **Criterios de Aceptación Verificables:** Definición clara de las condiciones que certificarán su pase a `Done`.

#### 5.3. Flujo Operativo Estrictamente "Pull"
```
[ Product Backlog ] ──(Priorización del Solution Owner)──> [ Sprint Backlog ]
                                                                 │
                                                    (Aprobación de Spec + TDD)
                                                                 │
                                                                 ▼
[ Done (Aprobación SO) ] <──(QA Automatizado + Criterios)── [ In Progress ]
```

1. **Ingreso a Product Backlog:** Todo gap, mejora u oportunidad se documenta y se coloca en la columna `Product Backlog` (`status: "backlog"`).
2. **Refinamiento y Priorización:** El Solution Owner evalúa el Backlog y decide qué tarjeta pasa a `Sprint Backlog`.
3. **Especificación y Pruebas:** Se genera/revisa la especificación y se escriben las pruebas que fallan.
4. **Desarrollo (In Progress):** La IA ejecuta el código mínimo atómico hasta satisfacer las pruebas.
5. **Compuerta de Calidad (QA):** Ejecución de tests automatizados y validación de restricciones OJO.
6. **Aceptación Final (Done):** El Solution Owner valida la solución en funcionamiento y autoriza el cierre.

---

### 6. Catálogo y Especificación Detallada de las Historias de Usuario (UH) del Product Backlog

A continuación se especifica la ficha técnica completa de cada una de las 5 iniciativas registradas en la columna **Product Backlog** del Tablero Scrumban, estructuradas bajo el estándar oficial de Historias de Usuario con sus Criterios de Aceptación (Gherkin) y sus Criterios de Adaptación Metodológica (Tailoring PMI):

---

#### 6.1. `GAP-01`: Formalización del Marco PMI + IA y Protocolo de Calidad en Suite Documental
* **Identificador:** `GAP-01` | **Tipo:** GAP de Proceso | **Estimación:** 5 Story Points | **Disciplina:** Analista Funcional / Gobernanza
* **Documentación Enlazada:** `docs/08_MARCO_DE_TRABAJO_PMI_IA_Y_GOBERNANZA_CALIDAD.md` y `docs/01_PLAN_DE_GESTION_DEL_PROYECTO.md`

* **Narrativa de la Historia de Usuario:**
  * **COMO** Solution Owner de HealthDesk Quantux,
  * **NECESITO** formalizar la integración de los 4 pasos del proceso de adaptación del PMI (PMBOK® 7ª Edición) con el ciclo de desarrollo asistido por IA generativa en la suite documental del producto,
  * **PARA** erradicar la degradación de calidad por instrucciones en lenguaje natural libre, evitar la deriva de contexto (*context drift*) y asegurar que cada desarrollo esté respaldado contractualmente.

* **Criterios de Aceptación Verificables (Formato Gherkin):**
  * **Escenario 1 (Formalización y Trazabilidad):**
    * **DADO** el ecosistema documental de Quantux en `docs/`,
    * **CUANDO** se audita la gobernanza de ingeniería,
    * **ENTONCES** debe existir el documento oficial `DOC-GOV-008` en formatos Markdown y HTML corporativo, debidamente registrado en el Catálogo de Entregables del Plan de Gestión (`DOC-MGT-001`).
  * **Escenario 2 (Matriz RACI y Delimitación de Roles):**
    * **DADO** el trabajo en pair-programming con el Agente IA,
    * **CUANDO** se consulta la matriz de límites operativos,
    * **ENTONCES** queda explícitamente delimitado que el Solution Owner (Humano) es el único dueño del alcance, valor de negocio y aceptación final, mientras que el Agente IA es un ejecutor técnico subordinado con prohibición de autovalidarse o inventar alcance.
  * **Escenario 3 (Regla Mandatoria de Backlog):**
    * **DADO** un nuevo requerimiento, mejora o corrección de gap,
    * **CUANDO** la IA detecta o propone la necesidad,
    * **ENTONCES** debe quedar registrado como tarjeta en la columna `Product Backlog` del Scrumban antes de tocar una sola línea de código.

* **Criterios de Adaptación Metodológica (Tailoring PMI):**
  * *Paso 1 (Enfoque Inicial):* Modelo Híbrido Estricto — Requerimientos predictivos cerrados + micro-sprints adaptativos de codificación.
  * *Paso 2 (Adaptación Organizacional):* Cumplimiento inquebrantable de la cultura Quantux y restricciones OJO.
  * *Paso 3 (Adaptación al Proyecto):* Desglose atómico en UH con criterios Gherkin verificables y accionables en CLI.
  * *Paso 4 (Mejora Continua):* Gestión visual en columna Product Backlog e incorporación retroactiva en reglas de prompt (`GEMINI.md`).

---

#### 6.2. `MEJ-01`: Automatización de Bucle TDD y Pre-commit Hooks para Validadores OJO
* **Identificador:** `MEJ-01` | **Tipo:** MEJORA Técnica | **Estimación:** 5 Story Points | **Disciplina:** DevOps / QA Automation
* **Documentación Enlazada:** `docs/08_MARCO_DE_TRABAJO_PMI_IA_Y_GOBERNANZA_CALIDAD.md#seccion-3` y `validate_ojo_compliance.py`

* **Narrativa de la Historia de Usuario:**
  * **COMO** Facilitador Técnico y QA Lead de HealthDesk Quantux,
  * **NECESITO** instrumentar un hook de pre-commit y un script de verificación automatizada que ejecute secuencialmente `validate_ojo_compliance.py` y la suite de pruebas del DOM,
  * **PARA** impedir mecánicamente que el Agente IA o cualquier colaborador introduzca cards flotantes, fondos oscuros, tonos rojos prohibidos o jergas clínicas en el repositorio.

* **Criterios de Aceptación Verificables (Formato Gherkin):**
  * **Escenario 1 (Bloqueo Automatizado en Commit / Compuerta):**
    * **DADO** un intento de commit o entrega de código que contenga selectores de clase tipo `.card`, estilos con colores rojos (`#EF4444`, `#DC2626`) o términos clínicos (`guardia`, `asistencial`),
    * **CUANDO** se ejecuta el validador en terminal,
    * **ENTONCES** el proceso finaliza con Exit Code 1, abortando la entrega y detallando archivo, línea y regla violada.
  * **Escenario 2 (Certificación Verde):**
    * **DADO** un código refactorizado y limpio conforme a las pautas de estilo neutral y maquetación en filas de 1px,
    * **CUANDO** se corre el comando de verificación,
    * **ENTONCES** reporta Exit Code 0 ("100% COMPLIANT") y permite continuar el flujo de integración.
  * **Escenario 3 (Automatización del Bucle TDD):**
    * **DADO** un nuevo criterio de aceptación,
    * **CUANDO** se inicia el desarrollo,
    * **ENTONCES** se ejecuta primero la prueba unitaria/E2E demostrando fallo (rojo) antes de escribir la implementación mínima (verde).

* **Criterios de Adaptación Metodológica (Tailoring PMI):**
  * *Paso 1:* Enfoque de Calidad Predictivo mediante compuertas de software (*quality gates*).
  * *Paso 2:* Adaptación a la regla OJO institucional de cero tolerancia a elementos no solicitados.
  * *Paso 3:* Pruebas automatizadas en terminal local sin dependencias en la nube.
  * *Paso 4:* Registro de infracciones en log de auditoría para prevención de reincidencias.

---

#### 6.3. `OM-01`: Trazabilidad Bidireccional de Tickets hacia Contratos OpenAPI y Esquemas DDL
* **Identificador:** `OM-01` | **Tipo:** OPORTUNIDAD DE MEJORA | **Estimación:** 8 Story Points | **Disciplina:** Backend / Arquitectura de Software
* **Documentación Enlazada:** `docs/API_CONTRACTS.md` y `backend/app/main.py`

* **Narrativa de la Historia de Usuario:**
  * **COMO** Arquitecto de Software de HealthDesk Quantux,
  * **NECESITO** vincular cada endpoint de FastAPI (`backend/app/api/endpoints/`) y cada tabla SQLite/PostgreSQL (`backend/app/models/entities.py`) con la especificación contractual unificada en `docs/API_CONTRACTS.md`,
  * **PARA** asegurar consistencia 100% de esquemas, prevenir alucinaciones de modelos Pydantic y permitir la generación automatizada de pruebas de contrato.

* **Criterios de Aceptación Verificables (Formato Gherkin):**
  * **Escenario 1 (Validación de Esquema OpenAPI 3.0):**
    * **DADO** el contrato documentado en `docs/API_CONTRACTS.md`,
    * **CUANDO** se inspecciona el `/openapi.json` generado por FastAPI,
    * **ENTONCES** existe paridad exacta de tipos, parámetros de entrada, respuestas HTTP (200, 400, 404, 422) y esquemas de payload.
  * **Escenario 2 (Trazabilidad DDL en Entidades):**
    * **DADO** el modelo de base de datos de tickets, comentarios y auditoría,
    * **CUANDO** se crean o alteran tablas en SQLite/PostgreSQL,
    * **ENTONCES** los campos corresponden estrictamente a lo pactado sin atributos espurios ni omisiones de restricciones de clave foránea.
  * **Escenario 3 (Prevención de Rompimiento de Integración):**
    * **DADO** un cambio propuesto en la API por parte del asistente IA,
    * **CUANDO** el cambio no cuenta con actualización previa del contrato en `docs/API_CONTRACTS.md`,
    * **ENTONCES** el cambio es rechazado por la compuerta de arquitectura.

* **Criterios de Adaptación Metodológica (Tailoring PMI):**
  * *Paso 1:* Enfoque Spec-Driven Development (SDD) con contratos de interfaz inmutables.
  * *Paso 2:* Protección de datos en salud y trazabilidad de entidades de soporte.
  * *Paso 3:* Verificación mediante esquemas Pydantic deterministas.
  * *Paso 4:* Versionado semántico de contratos ante nuevas capacidades operativas.

---

#### 6.4. `GAP-02`: Blindaje de Integridad de Contexto para Auditorías TQM y Cero Scope Creep
* **Identificador:** `GAP-02` | **Tipo:** GAP Metodológico | **Estimación:** 5 Story Points | **Disciplina:** QA / Metodología de Procesos
* **Documentación Enlazada:** `docs/04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md` y `GEMINI.md`

* **Narrativa de la Historia de Usuario:**
  * **COMO** Auditor de Calidad TQM de Quantux Salud,
  * **NECESITO** un protocolo determinista de verificación de contexto y cotejo de observaciones que audite el 100% de los requerimientos y comentarios del usuario antes de cada entrega,
  * **PARA** erradicar el olvido de especificaciones (*context decay*), evitar el desvío del alcance (*scope creep*) y asegurar que no quede ningún punto de prueba pendiente en `DOC-QA-004`.

* **Criterios de Aceptación Verificables (Formato Gherkin):**
  * **Escenario 1 (Auditoría de Cero Omisiones):**
    * **DADO** el historial completo de solicitudes y observaciones del Solution Owner,
    * **CUANDO** la IA prepara un informe o bloque de código,
    * **ENTONCES** debe contrastar cada requerimiento contra una matriz de cobertura explícita donde ningún punto figure como omitido o no resuelto.
  * **Escenario 2 (Evidencia Ejecutable en `DOC-QA-004`):**
    * **DADO** el documento `docs/04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md`,
    * **CUANDO** se audita el estado del producto,
    * **ENTONCES** debe contener logs reales de terminal, resultados de aserciones y capturas de consola que comprueben la operatividad de cada función.
  * **Escenario 3 (Prohibición de Supuestos No Autorizados):**
    * **DADO** un punto no especificado en el alcance,
    * **CUANDO** la IA enfrenta una bifurcación de diseño,
    * **ENTONCES** debe detenerse y formular la consulta aclaratoria al Solution Owner en lugar de asumir una implementación arbitraria.

* **Criterios de Adaptación Metodológica (Tailoring PMI):**
  * *Paso 1:* Verificación en Doble Bucle (*Dual-Loop Validation*).
  * *Paso 2:* Inmunización de reglas en el archivo de sistema institucional `GEMINI.md`.
  * *Paso 3:* Checklists exhaustivos pre-vuelo con compuertas binarias (PASA / NO PASA).
  * *Paso 4:* Retroalimentación continua al backlog ante cualquier gap de aseguramiento de calidad.

---

#### 6.5. `MEJ-02`: Soporte Nativo de Enlaces Documentales y Modal de UH en Tablero Scrumban
* **Identificador:** `MEJ-02` | **Tipo:** MEJORA de Experiencia | **Estimación:** 3 Story Points | **Disciplina:** Frontend / Experiencia de Usuario
* **Documentación Enlazada:** `docs/00_Tablero_Scrumban_Quantux.html`

* **Narrativa de la Historia de Usuario:**
  * **COMO** Solution Owner y miembro del Comité Evaluador,
  * **NECESITO** visualizar en el tablero Scrumban interactivo (`00_Tablero_Scrumban_Quantux.html`) tanto los badges de tipología (`GAP`, `MEJORA`, `OPORTUNIDAD`) como el enlace directo a la documentación y la posibilidad de desplegar la Historia de Usuario completa con sus criterios de aceptación y adaptación,
  * **PARA** gestionar el Product Backlog con transparencia total, auditar los requerimientos sin salir de la vista operativa y tomar decisiones informadas de priorización para el próximo Sprint.

* **Criterios de Aceptación Verificables (Formato Gherkin):**
  * **Escenario 1 (Visualización de Metadatos y Badges):**
    * **DADO** el tablero Scrumban abierto en el navegador,
    * **CUANDO** se inspecciona la columna `Product Backlog`,
    * **ENTONCES** cada tarjeta exhibe su identificador, Story Points, badge tipológico coloreado según estándar Quantux (Ámbar para GAP, Azul suave para MEJORA, Púrpura suave para OPORTUNIDAD) y caja con link a su documentación.
  * **Escenario 2 (Acceso Inmediato a la Especificación):**
    * **DADO** el enlace `📄 Especificación / Doc` en una tarjeta del backlog,
    * **CUANDO** el usuario hace clic,
    * **ENTONCES** se abre en pestaña nueva el documento correspondiente en la ruta exacta de la suite documental.
  * **Escenario 3 (Modal o Vista Expandible de Narrativa y Criterios):**
    * **DADO** una tarjeta en el backlog,
    * **CUANDO** el usuario hace clic sobre el botón "🔍 Ver UH y Criterios",
    * **ENTONCES** se despliega un modal accesible con la narrativa completa (**Como / Necesito / Para**), los Criterios de Aceptación en formato Gherkin (**Dado / Cuando / Entonces**) y los Criterios de Adaptación PMI.

* **Criterios de Adaptación Metodológica (Tailoring PMI):**
  * *Paso 1:* Visualización ágil basada en Scrumban con soporte de información en capas (*progressive disclosure*).
  * *Paso 2:* Apego visual a la estética Quantux (Slate, Teal, fondos claros, sin tarjetas flotantes no controladas).
  * *Paso 3:* Ejecución cliente 100% nativa en HTML5/CSS3/Vanilla JS sin dependencias externas.
  * *Paso 4:* Exportación sincronizada a CSV para interoperabilidad con Jira, Trello o Excel.

---

### 7. Gobernanza de Cierre y Aceptación Final

Ninguna tarjeta del Product Backlog podrá ser promovida al estado `Done` sin cumplir con el siguiente protocolo de tres pasos:
1. **Verificación de Criterios de Aceptación:** Ejecución de pruebas demostrables en terminal según los escenarios Gherkin.
2. **Auditoría de Restricciones OJO:** Ejecución obligatoria de `python validate_ojo_compliance.py` con Exit Code 0.
3. **Firma de Conformidad del Solution Owner:** Aprobación explícita por parte del usuario (Freddy Cortés).

---

### 8. Fase de Hardening, Quality Gates Pre-Commit y Scope Freeze (01-Octubre)

Con vistas a la presentación final del **01 de Octubre de 2026** ante el Comité Evaluador, el proyecto ha entrado formalmente en su **Fase de Hardening y Estabilización (Sprint 6)** bajo las siguientes reglas de aseguramiento:

#### 8.1. Política de Scope Freeze (Alcance Cerrado)
* El alcance funcional está 100% cerrado en las 48 UHs de la línea base.
* Toda nueva propuesta, requerimiento accesorio o idea emergente (ej. `ISSUE-19`) se desvía de forma obligatoria a la columna `📋 Product Backlog` con estado `backlog`.
* La labor técnica se circunscribe con exclusividad a:
  1. Cierre de retrabajos observados por el Solution Owner (`UH-67`, `MEJ-08`).
  2. Cobertura de pruebas unitarias y de integración (TDD).
  3. Verificación de cero regresiones en la interfaz y en el backend.

#### 8.2. Calibración de Tiempos y Blindaje para el Solution Owner
* **Deadline Técnico Definitivo (Hardening Freeze):** **Lunes 28 de Septiembre a las 18:00 hs.**
* **Ventana Blindada de Preparación (48 horas):** El **29 y 30 de Septiembre** quedan estrictamente reservados para que el Solution Owner ensaye el pitch, ajuste el guión de 5 pasos y procese cualquier devolución anticipada remitida por el Comité Evaluador.

#### 8.3. Compuertas de Calidad Automatizadas (Pre-Commit Hooks)
En el marco PMI + IA, la calidad no es declarativa sino comprobable mediante código:
* **Quality Gate 1 (Regla OJO y Pizarra Neutral):** Inspección estática del DOM que bloquea cualquier violación estética o de terminología (`validate_ojo_compliance.py`).
* **Quality Gate 2 (Cumplimiento Visual DOM):** Pruebas automatizadas sobre estructura y estilo (`test_dom_visual_compliance.py`).
* **Quality Gate 3 (Integridad Backend & ITIL 4):** Pruebas de integración sobre modelos relacionales y FSM (`test_reemplazo_n1_suite.py`).
* **Quality Gate 4 (Suite de Pruebas Unitarias):** 25 tests cubriendo el bot gestor, catálogos multi-tenant y mejoras operativas.

---
**Documento Oficial aprobado para su integración inmediata a la Suite Documental de HealthDesk Quantux.**
