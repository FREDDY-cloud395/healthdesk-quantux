# QUANTUX SALUD • HEALTHDESK
## DOC-FS-002: ESPECIFICACIÓN FUNCIONAL DE REQUISITOS Y BACKLOG EXTENDIDO
### MODELADO FORMAL DE 38 HISTORIAS DE USUARIO Y CRITERIOS GHERKIN

---

### METADATOS Y CONTROL DOCUMENTAL
* **Código Documental:** DOC-FS-002
* **Versión Oficial:** v3.2.0-UAT
* **Fecha de Emisión:** Septiembre 2026
* **Propietario / Solution Owner:** Freddy Cortés (Analista Funcional)
* **Comité Evaluador:** Paula Sbarbati, Diego Martínez, Carolina Brizuela, Nicolás Sánchez
* **Estado:** HOMOLOGADO & APROBADO (100% Cobertura de Criterios de Aceptación)
* **Story Points Totales:** 91 SP distribuidos en 8 Épicas

---

## 1. GOBERNANZA DE REQUISITOS CON IA

Cada requisito e historia de usuario en este documento ha sido estructurado siguiendo el marco formal de ingeniería de software con asistencia de IA:
1. **Descripción y Objetivo:** Propósito funcional asistencial claro y justificado.
2. **Prioridad y Origen:** Clasificación ITIL (P1 a P5) y fuente clínica/operativa.
3. **Criterios de Aceptación:** Sintaxis Gherkin (`Dado`, `Cuando`, `Entonces`).
4. **Dependencias y Restricciones:** Vínculos con modelos relacionales y estados FSM.
5. **Responsable de Validación:** Homologación humana obligatoria por el Solution Owner.

> **Principio de Calidad:** Ningún requisito o caso borde sugerido por IA fue admitido en la línea base sin revisión, contraste de consistencia y aprobación formal humana.

---

## 2. RESUMEN EJECUTIVO DE ÉPICAS Y DIMENSIONES FUNCIONALES

| Código Épica | Nombre de la Épica | Cant. UHs | Story Points | Dimensión Asistencial / Técnica |
| :--- | :--- | :---: | :---: | :--- |
| **EP-01** | Acceso, Perfiles y Seguridad RBAC | 4 | 8 SP | Autenticación, perfiles y aislamiento de permisos |
| **EP-02** | Creación y Priorización ITIL de Tickets | 7 | 18 SP | Alta ágil, matriz $P=I \times U$, catálogos sanitarios |
| **EP-03** | Cockpit, Bandeja y Asignación Multi-Nivel | 6 | 14 SP | Bandeja operativa, filtros, derivación N1/N2/N3 |
| **EP-04** | Motor de Gestión FSM y Guardrails | 6 | 17 SP | Ciclo determinístico, solución $\ge 8$ car, Workaround |
| **EP-05** | Colaboración, Trazabilidad y Auditoría | 4 | 10 SP | Notas privadas RBAC, log inmutable y feedback |
| **EP-06** | Catálogos Sanitarios y Administración | 5 | 8 SP | Alta de plataformas, sanatorios y configuración |
| **EP-07** | Base de Conocimiento y Auto-Documentación | 4 | 10 SP | Protocolos clínicos, versionado (`v1.0`/`v1.1`), tags |
| **EP-08** | Mesas Especializadas y Reportes Forenses | 2 | 6 SP | Tablero de dotación N1/N2/N3 y exportación CSV |
| **TOTAL** | **8 Épicas Homologadas** | **38 UHs** | **91 SP** | **100% Cobertura Funcional Certificada** |

---

## 3. CATÁLOGO DETALLADO DE HISTORIAS DE USUARIO (UH-01 a UH-38)

### ÉPICA 1: ACCESO, PERFILES Y SEGURIDAD RBAC (8 SP)
* **UH-01 (3 SP): Inicio de sesión multi-rol y control de acceso.**
  * *Dado* un usuario con credenciales registradas, *cuando* inicia sesión, *entonces* el sistema retorna su token de sesión, nombre completo y rol (`SOLICITANTE`, `SOPORTE`, `ADMIN`).
* **UH-02 (2 SP): Listado y consulta de usuarios operativos.**
  * *Dado* un Administrador autenticado, *cuando* consulta la lista de usuarios, *entonces* visualiza operadores activos, roles y niveles ITIL asignados.
* **UH-03 (2 SP): Auditoría de inicio de sesión.**
  * *Dado* un intento de autenticación, *cuando* se procesa, *entonces* queda registrado en el historial el timestamp, usuario y resultado exitoso o fallido.
* **UH-04 (1 SP): Encriptación y resguardo de credenciales.**
  * *Dado* el almacenamiento de usuarios, *cuando* se persisten contraseñas, *entonces* se utiliza hash criptográfico no reversible.

### ÉPICA 2: CREACIÓN Y PRIORIZACIÓN ITIL DE TICKETS (18 SP)
* **UH-05 (3 SP): Alta unificada de ticket con código correlativo.**
  * *Dado* un solicitante en el formulario de alta, *cuando* ingresa título y descripción, *entonces* se genera un ID unívoco con formato `TICK-YYYYMM-XXXX`.
* **UH-06 (3 SP): Selección de Plataforma Clínica oficial (≥ 9 plataformas).**
  * *Dado* el formulario de creación, *cuando* el usuario selecciona plataforma, *entonces* dispone del catálogo oficial (Portal, HCE, Telemedicina, Receta Digital, Turnos, Facturación, Triage, LIS, RNDS).
* **UH-07 (3 SP): Selección de Cliente Institucional / Sanatorio (≥ 14 financiadores).**
  * *Dado* el formulario de creación, *cuando* el usuario selecciona sanatorio, *entonces* dispone de la lista oficial (OSDE, Swiss Medical, Galeno, Italiano, Mater Dei, etc.).
* **UH-08 (2 SP): Tipificación del requerimiento (Incidente, Requerimiento, Consulta).**
  * *Dado* un ticket en creación, *cuando* se elige el tipo, *entonces* se almacena su tipificación para métricas de servicio.
* **UH-09 (3 SP): Cálculo determinístico de Prioridad ITIL ($P = I \times U$).**
  * *Dado* los valores de Impacto y Urgencia, *cuando* se combinan en la matriz ITIL, *entonces* el sistema asigna reactivamente la prioridad (P1 a P5) sin intervención manual arbitraria.
* **UH-10 (2 SP): Carga de adjuntos y evidencias sanitarias.**
  * *Dado* un incidente con captura de pantalla o log, *cuando* se proporciona URL de evidencia, *entonces* se almacena vinculada al ticket.
* **UH-11 (2 SP): Edición permitida exclusivamente en estado NUEVO.**
  * *Dado* un ticket en estado `NUEVO`, *cuando* el solicitante actualiza datos antes de su asignación, *entonces* se guardan los cambios y se recalcula la prioridad.

### ÉPICA 3: BANDEJA OPERATIVA Y ASIGNACIÓN MULTI-NIVEL (14 SP)
* **UH-12 (3 SP): Bandeja unificada Cockpit con filtros dinámicos.**
  * *Dado* el panel principal de operadores, *cuando* se carga la bandeja, *entonces* se listan tickets con filtros reactivos por estado, prioridad, plataforma y cliente.
* **UH-13 (2 SP): Indicador visual SLA por semáforo de criticidad.**
  * *Dado* el listado de tickets, *cuando* se visualiza la prioridad, *entonces* se muestra badge distintivo rojo (P1), naranja (P2), amarillo (P3) y verde (P4/P5).
* **UH-14 (3 SP): Autoasignación directa ('Tomar Ticket') por Operador.**
  * *Dado* un ticket en estado `NUEVO`, *cuando* un operador de soporte presiona 'Tomar Ticket', *entonces* se asigna a su nombre y transiciona a `ASIGNADO`.
* **UH-15 (3 SP): Escalamiento formal jerárquico (N1 $\rightarrow$ N2 $\rightarrow$ N3).**
  * *Dado* un ticket asignado a N1/N2, *cuando* el operador requiere soporte avanzado, *entonces* transfiere a N2 o N3 registrando motivo obligatorio de escalamiento.
* **UH-16 (2 SP): Reasignación de operador por especialidad técnica.**
  * *Dado* un ticket en curso, *cuando* se transfiere a otro especialista del mismo nivel, *entonces* se actualiza el operador responsable con registro en auditoría.
* **UH-28 (1 SP): Ordenamiento múltiple por fecha y criticidad en Cockpit.**
  * *Dado* la vista de bandeja, *cuando* el usuario selecciona columna, *entonces* se ordenan los registros en memoria sin recargar la página.

### ÉPICA 4: MOTOR DE GESTIÓN FSM Y GUARDRAILS SANITARIOS (17 SP)
* **UH-17 (3 SP): Transición a EN_CURSO e inicio de diagnóstico.**
  * *Dado* un ticket asignado, *cuando* el operador inicia el trabajo técnico, *entonces* el estado pasa a `EN_CURSO` y se estampa el timestamp de atención.
* **UH-18 (3 SP): Pausa operativa de gestión (Estado EN_ESPERA).**
  * *Dado* un ticket en curso que aguarda información del solicitante o de un nodo externo, *cuando* el operador lo pone en espera, *entonces* pasa a `EN_ESPERA` con motivo documentado.
* **UH-19 (3 SP): Guardrail de solución técnica obligatoria (≥ 8 caracteres).**
  * *Dado* un operador intentando resolver un ticket, *cuando* ingresa una solución de menos de 8 caracteres (ej: "listo"), *entonces* el sistema rechaza la operación con HTTP 400.
* **UH-20 (3 SP): Marcación de Solución Provisoria / Workaround.**
  * *Dado* el formulario de resolución, *cuando* se marca la casilla 'Workaround', *entonces* el ticket se guarda con flag `is_workaround = True` para posterior análisis de problema raíz.
* **UH-21 (2 SP): Transición efectiva a estado RESUELTO.**
  * *Dado* un ticket con solución válida, *cuando* se confirma la resolución, *entonces* pasa a `RESUELTO` y se notifica al solicitante.
* **UH-22 (3 SP): Cierre formal con conformidad e inmutabilidad terminal.**
  * *Dado* un ticket en `RESUELTO`, *cuando* el solicitante confirma conformidad, *entonces* pasa a `CERRADO` y se bloquea estrictamente cualquier edición o transición posterior.

### ÉPICA 5: COLABORACIÓN, TRAZABILIDAD Y AUDITORÍA SANITARIA (10 SP)
* **UH-23 (3 SP): Registro de comentarios públicos bidireccionales.**
  * *Dado* un ticket en gestión, *cuando* solicitante o soporte publican comentario, *entonces* es visible para ambas partes en la línea de tiempo.
* **UH-24 (3 SP): Registro de notas técnicas internas privadas (RBAC estricto).**
  * *Dado* un operador registrando trazas técnicas confidenciales, *cuando* marca 'Nota Interna', *entonces* la nota solo es visible para perfiles `SOPORTE` y `ADMIN`.
* **UH-25 (2 SP): Trazabilidad de adjuntos en comentarios.**
  * *Dado* un intercambio en el hilo del ticket, *cuando* se adjunta evidencia adicional, *entonces* queda anexada al mensaje específico.
* **UH-27 (2 SP): Historial inmutable de auditoría forense (Caja Negra).**
  * *Dado* cualquier cambio de estado, asignación o prioridad, *cuando* se ejecuta, *entonces* se genera un registro inmutable en `ticket_audit_log` con usuario, timestamp ISO, valores anterior/nuevo y motivo.

### ÉPICA 6: CATÁLOGOS SANITARIOS Y ADMINISTRACIÓN (8 SP)
* **UH-26 (2 SP): Notificaciones automáticas de cambio de estado.**
  * *Dado* un evento de transición en el ticket, *cuando* se completa, *entonces* se dispara simulación de correo con log registrado en base de datos.
* **UH-29 (1 SP): Panel de métricas rápidas de bandeja.**
  * *Dado* el Cockpit principal, *cuando* se carga, *entonces* muestra contadores de tickets en Nuevo, En Curso, Resueltos y Cerrados.
* **UH-30 (2 SP): Búsqueda por texto libre en títulos y descripciones.**
  * *Dado* la bandeja de tickets, *cuando* se escribe un término clínico (ej: "receta"), *entonces* se filtran instantáneamente los resultados coincidentes.
* **UH-31 (2 SP): Alta y administración de usuarios operativos.**
  * *Dado* el módulo de administración, *cuando* se registra un nuevo analista, *entonces* se asigna su nivel ITIL y rol de acceso.
* **UH-32 (1 SP): Configuración de parámetros globales del ServiceDesk.**
  * *Dado* el Administrador del sistema, *cuando* accede a configuración, *entonces* puede consultar y ajustar parámetros operativos y de SLAs.

### ÉPICA 7: BASE DE CONOCIMIENTO CLÍNICO & AUTO-DOCUMENTACIÓN (10 SP)
* **UH-33 (3 SP): Consulta, búsqueda y filtrado de protocolos clínicos.**
  * *Dado* un operador o médico, *cuando* consulta la Base de Conocimiento, *entonces* accede a más de 14 protocolos oficiales categorizados (Receta Digital, Telemedicina, Facturación, etc.).
* **UH-34 (3 SP): Publicación de nuevos artículos de conocimiento estructurados.**
  * *Dado* un especialista técnico, *cuando* redacta un nuevo procedimiento asistencial con tags, *entonces* se publica con versión inicial `v1.0`.
* **UH-35 (2 SP): Versionado histórico inmutable y changelog de protocolos.**
  * *Dado* un artículo existente, *cuando* se actualiza a `v1.1`, *entonces* la versión anterior se preserva en `kb_article_versions` con su changelog y autor.
* **UH-36 (2 SP): Auto-publicación de artículos desde la resolución de tickets.**
  * *Dado* un ticket resuelto con solución novedosa, *cuando* el operador selecciona 'Publicar en KB', *entonces* se genera automáticamente el borrador de artículo vinculado a la plataforma clínica.

### ÉPICA 8: GESTIÓN MULTI-NIVEL ITIL Y AUDITORÍA FORENSE (6 SP)
* **UH-37 (3 SP): Tablero de dotación y mesas especializadas por nivel N1/N2/N3.**
  * *Dado* el panel de supervisión de mesas, *cuando* se consulta, *entonces* se visualiza la carga activa, especialidad técnica y dotación de operadores por nivel ITIL.
* **UH-38 (3 SP): Exportación forense de solicitudes y auditoría en CSV UTF-8.**
  * *Dado* un requerimiento de auditoría o análisis de SLAs, *cuando* el Administrador presiona 'Exportar CSV', *entonces* se descarga el dataset completo con codificación UTF-8 compatible con Excel/PowerBI.

---

### APROBACIÓN DE ESPECIFICACIÓN
* **Solution Owner:** *Freddy Cortés*
* **Comité Evaluador:** *Paula Sbarbati, Diego Martínez, Carolina Brizuela, Nicolás Sánchez*
* **Fecha:** Septiembre 2026 • Versión `v3.2.0-UAT`
