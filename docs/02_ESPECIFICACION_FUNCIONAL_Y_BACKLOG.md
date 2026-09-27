# 📑 DOCUMENTO 2: ESPECIFICACIÓN FUNCIONAL Y BACKLOG
**Código:** DOC-REQ-002 (Versión 1.2 Oficial - Cierre Sprint 6 & Apertura Sprint 7)
**Proyecto:** HealthDesk Quantux — Sistema Centralizado de Gestión de Tickets de Soporte
**Organización:** Quantux Salud
**Solution Owner:** Freddy Cortés (Analista Funcional)
**Dimensión:** 9 Épicas | 174 Tarjetas de Backlog Catalogadas | 100% Trazabilidad PMI+IA
**Fecha de Línea Base:** 28 de Agosto de 2026 | **Fecha de Versión 1.2:** 27 de Septiembre de 2026
**Comité Evaluador:** Paula Sbarbati, Diego Martínez, Carolina Brizuela, Nicolás Sánchez

---

### Control de Versiones y Distribución
| Versión | Fecha | Responsable | Detalle de Modificaciones / Estado |
| :--- | :--- | :--- | :--- |
| **v1.0** | 28/08/2026 | Freddy Cortés | **Línea Base Funcional Oficial del MVP:** 32 Historias de Usuario, 6 Épicas, circuitos de 5 estados ITIL y catálogos de 9 plataformas y 14 clientes. |
| **v1.1** | 26/09/2026 | Freddy Cortés | **Consolidación de Backlog (48 UHs), Política de Scope Freeze y Aislamiento de Evolutivos:** Congelamiento de alcance para demo del 01-Oct-2026, incorporación de UH-33 a UH-69, y derivación mandatoria de nuevos requerimientos al Product Backlog. |
| **v1.2** | 27/09/2026 | Freddy Cortés | **Cierre Formal Sprint 6 (93 tarjetas en Done), Activación Sprint 7 (13 tarjetas en Sprint Backlog), Integración de Pizarra Neutral Quantux y Protocolo de Resguardo Siete Llaves.** |

---

### 1. Catálogo del Ecosistema Quantux

#### 1.1. Las 9 Plataformas Digitales de Salud
1. `CAT_RECETA` — **Receta Electrónica:** Emisión, firma digital y dispensa farmacéutica (+400k recetas/mes).
2. `CAT_TELEMEDICINA` — **Telemedicina:** Videoconsultas sincrónicas, sala de espera virtual y triage.
3. `CAT_COPAGOS_PAGOS` — **Copagos y Pasarela de Pagos:** Cobro de coseguros, liquidaciones y pagos online.
4. `CAT_RPM_MONITOREO` — **Monitoreo Remoto (RPM):** Seguimiento de pacientes crónicos y telemetría de dispositivos.
5. `CAT_INTERNACION_DOM` — **Internación Domiciliaria:** Logística de visitas, insumos y evolución asistencial domiciliaria.
6. `CAT_AFILIADOS_PORTAL` — **Portal de Afiliados / Pacientes:** Autogestión de credenciales, historial y autorizaciones.
7. `CAT_CARTILLA_TURNOS` — **Cartilla Asistencial y Turnos:** Geolocalización de prestadores y reserva online de citas.
8. `CAT_REGISTRO_INTEROP` — **Interoperabilidad y Registro:** Integración bajo estándar HL7 / FHIR con entidades de salud.
9. `CAT_CONSULTORIO_DIGITAL` — **Consultorio Digital:** Historia clínica ambulatoria para 12.000 profesionales de la salud activos.

#### 1.2. Los 14 Clientes Institucionales Mapeados
* **Financiadores y Prepagas:** OSDE, Swiss Medical, Galeno, Medifé, Omint, Prevención Salud.
* **Sanatorios y Hospitales Privados:** Sanatorio Finochietto, Hospital Británico, Hospital Alemán, Sanatorio de la Trinidad.
* **Internación Domiciliaria y Redes:** IDOM, Mevaterapia, ORIEN, Red Asistencial Integral.

---

### 2. Marco Operativo de Soporte y Priorización

#### 2.1. Matriz de Prioridad ($P = I \times U$)
| Impacto \ Urgencia | Alta | Media | Baja |
| :--- | :---: | :---: | :---: |
| **Alto (Crítico)** | **P1 — Crítica (2h)** | **P2 — Alta (8h)** | **P3 — Media (24h)** |
| **Medio** | **P2 — Alta (8h)** | **P3 — Media (24h)** | P4 — Baja (48h) |
| **Bajo** | **P3 — Media (24h)** | P4 — Baja (48h) | P5 — Muy Baja (72h) |

#### 2.2. Niveles de Atención Operativa
* **Nivel 1 (N1) — Mesa de Ayuda:** Recepción, triage, validación de datos del afiliado/profesional de la salud y resolución de consultas frecuentes.
* **Nivel 2 (N2) — Soporte Técnico:** Diagnóstico especializado y aplicación obligatoria de soluciones provisorias documentadas.
* **Nivel 3 (N3) — Ingeniería y Producto:** Corrección definitiva en código fuente o infraestructura.

#### 2.3. Reglas de Negocio Funcionales del Ciclo de Vida del Ticket
1. **RN-01: Obligatoriedad de Solución Técnica para Resolución:**  
   Para efectuar la transición de un ticket al estado `RESUELTO`, el operador de soporte debe ingresar obligatoriamente una descripción de la solución técnica aplicada (longitud mínima de 8 caracteres significativos). Asimismo, debe catalogar taxativamente si se trata de una **Solución Definitiva** o una **Solución Provisoria (Workaround)**. Sin estos dos datos, el sistema rechaza la operación.
2. **RN-02: Segregación y Confidencialidad de Notas Internas (Privacidad por Rol):**  
   Todo mensaje registrado dentro de un ticket se clasifica en dos categorías:
   * **Comentario Público:** Visible para el profesional de la salud / solicitante, el equipo técnico y las instituciones involucradas. Utilizado para notificaciones de avance y comunicación directa.
   * **Nota Interna de Diagnóstico (`is_internal = True`):** Visible exclusivamente para operadores de soporte (N1, N2, N3) y administradores. Protege análisis técnicos de servidores, trazas de error o detalles de infraestructura de modo que no causen confusión ni alarma innecesaria en el personal sanitario.
3. **RN-03: Cierre Definitivo Basado en Conformidad del Solicitante:**  
   Un ticket en estado `RESUELTO` no puede ser cerrado unilateralmente por el operador técnico sin la conformidad del solicitante. El usuario solicitante valida que el problema haya sido subsanado en su puesto de trabajo antes de promover el ticket a `CERRADO`.
4. **RN-04: Inmutabilidad del Estado Terminal (Caja Negra):**  
   Una vez alcanzado el estado `CERRADO`, la ficha del ticket se convierte en un registro histórico inmutable para fines de auditoría sanitaria y legal. No se permiten modificaciones en sus campos ni reaperturas informales (debe crearse un nuevo ticket vinculado si surge un nuevo incidente).
5. **RN-05: Cálculo Automatizado de Prioridad Dinámica:**  
   La prioridad del ticket ($P1$ a $P5$) se calcula en el momento del alta o reevaluación mediante la función determinística de la matriz $P = Impacto \times Urgencia$, eliminando la discrecionalidad subjetiva del operador.

---

### 3. User Story Mapping (Mapeo del Flujo de 5 Pasos del MVP)

* **PASO 1 • REGISTRAR (Crear Ticket y Clasificación):**  
  UH-01 (Login), UH-05 (Alta de Ticket), UH-06 (Plataforma), UH-07 (Cliente), UH-08 (Tipo de Solicitud), UH-09 (Prioridad), UH-10 (Adjuntos).
* **PASO 2 • ASIGNAR (Recepción y Derivación a Soporte):**  
  UH-12 (Bandeja de Entrada), UH-13 (Asignación de Responsable), UH-14 (Autoasignación "Tomar Ticket"), UH-15 (Derivación N2/N3), UH-16 (Reasignación de Responsable), UH-28 (Cockpit 3 Columnas).
* **PASO 3 • GESTIONAR (Seguimiento, Estados y Comunicación):**  
  UH-17 (Pase a En Curso), UH-18 (Pausa/Espera de Información), UH-23 (Comentarios Públicos), UH-24 (Notas Internas Privadas), UH-25 (Avisos Básicos), UH-29 (Selector Rápido de Rol).
* **PASO 4 • RESOLVER (Documentación de Solución):**  
  UH-19 (Registro de Solución), UH-20 (Solución Provisoria / Alternativa), UH-21 (Transición a Resuelto), UH-26 (Aviso Destacado de Resolución).
* **PASO 5 • CERRAR (Conformidad, Historial y Tablas Maestras):**  
  UH-22 (Cierre Definitivo), UH-27 (Historial y Trazabilidad), UH-02 (Permisos RBAC), UH-03 (Auditoría de Acceso), UH-04 (Cierre de Sesión), UH-11 (Edición Básica Pre-Asignación), UH-30 (Búsqueda y Filtros), UH-31 (Gestión de Usuarios), UH-32 (Tablas Maestras).

---

### 4. Especificación Detallada de las 32 Historias de Usuario

#### ÉPICA 1 (EP-01): Acceso, Roles y Permisos Básicos (7 SP)
*(Módulo MVP: Acceso — Login + roles y permisos básicos)*

* **UH-01: Autenticación de Usuarios por Rol (2 SP)**
  * *Narrativa:* **Como** usuario de Quantux Salud, **quiero** ingresar con mis credenciales seleccionando mi rol (Solicitante, Soporte, Administrador), **para** acceder a las funciones de mi perfil.
  * *Criterios de Aceptación:*
    * **Dado** un usuario registrado, **cuando** ingresa credenciales válidas, **entonces** accede a su bandeja principal.
    * **Dado** credenciales inválidas, **cuando** intenta ingresar, **entonces** el sistema muestra error y no permite el acceso.

* **UH-02: Control de Permisos por Perfil (2 SP)**
  * *Narrativa:* **Como** Administrador, **quiero** restringir las acciones del sistema según el rol del usuario, **para** evitar modificaciones no autorizadas en tickets o tablas maestras.
  * *Criterios de Aceptación:*
    * **Dado** un Solicitante, **cuando** consulta el sistema, **entonces** solo ve y crea sus propios tickets.
    * **Dado** un Operador de Soporte, **cuando** opera, **entonces** puede gestionar tickets pero no administrar usuarios ni tablas maestras.

* **UH-03: Auditoría Básica de Acceso (2 SP)**
  * *Narrativa:* **Como** Administrador, **quiero** registrar los inicios de sesión, **para** mantener la trazabilidad de seguridad.
  * *Criterios de Aceptación:*
    * **Dado** un login exitoso, **cuando** el usuario entra, **entonces** se guarda usuario, fecha, hora y rol en la bitácora.

* **UH-04: Cierre de Sesión Seguro (1 SP)**
  * *Narrativa:* **Como** usuario autenticado, **quiero** cerrar mi sesión en 1 clic, **para** proteger mi cuenta al desocupar la estación de trabajo.
  * *Criterios de Aceptación:*
    * **Dado** un usuario con sesión abierta, **cuando** presiona "Cerrar Sesión", **entonces** se limpia la sesión activa y regresa al login.

---

#### ÉPICA 2 (EP-02): Tickets y Datos de Solicitud (15 SP)
*(Módulos MVP: Tickets, Datos — Alta, consulta y edición; Título, descripción, categoría, prioridad, solicitante y fecha)*

* **UH-05: Formulario Unificado de Alta de Ticket (3 SP)**
  * *Narrativa:* **Como** Solicitante u Operador de Soporte, **quiero** cargar un ticket con título, descripción y datos de contacto, **para** reportar una solicitud formalmente.
  * *Criterios de Aceptación:*
    * **Dado** el formulario de alta, **cuando** se completan los campos obligatorios, **entonces** se genera el ticket en estado `Nuevo` con identificador único.

* **UH-06: Selección de Plataforma / Categoría (2 SP)**
  * *Narrativa:* **Como** Solicitante, **quiero** elegir la plataforma afectada de entre las 9 oficiales, **para** canalizar el ticket al equipo especialista correcto.
  * *Criterios de Aceptación:*
    * **Dado** el selector de plataformas, **cuando** el usuario elige una opción, **entonces** el ticket queda asociado a su código de catálogo (ej. `CAT_RECETA`).

* **UH-07: Vinculación con Cliente Institucional (2 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** asociar el ticket a uno de los 14 clientes institucionales, **para** identificar el impacto sobre la entidad de salud.
  * *Criterios de Aceptación:*
    * **Dado** el campo cliente, **cuando** se guarda el ticket, **entonces** queda registrada la institución (ej. OSDE, Swiss Medical, Finochietto).

* **UH-08: Tipificación de la Solicitud (2 SP)**
  * *Narrativa:* **Como** Operador de Soporte N1, **quiero** clasificar el ticket como Incidente, Requerimiento o Consulta, **para** aplicar las pautas de atención correspondientes.
  * *Criterios de Aceptación:*
    * **Dado** un ticket en triage, **cuando** se asigna el tipo, **entonces** queda visible en el detalle y listado.

* **UH-09: Asignación de Prioridad ($P = I \times U$) (3 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** definir el Impacto y la Urgencia, **para** que el sistema determine la Prioridad (P1 a P5).
  * *Criterios de Aceptación:*
    * **Dado** Impacto Alto y Urgencia Alta, **cuando** se registran los valores, **entonces** el sistema establece Prioridad P1 (Crítica).

* **UH-10: Adjunto de Evidencias (2 SP)**
  * *Narrativa:* **Como** Solicitante, **quiero** adjuntar capturas o enlaces del error, **para** que soporte pueda reproducir la falla rápidamente.
  * *Criterios de Aceptación:*
    * **Dado** un archivo o URL, **cuando** se adjunta al ticket, **entonces** queda accesible en la vista de detalle.

* **UH-11: Consulta y Edición Básica de Ticket (1 SP)**
  * *Narrativa:* **Como** Solicitante, **quiero** consultar el estado y editar los datos mientras el ticket esté en `Nuevo`, **para** corregir omisiones antes del inicio de la atención.
  * *Criterios de Aceptación:*
    * **Dado** un ticket en estado `Nuevo`, **cuando** el creador edita el texto, **entonces** los cambios se guardan y se registra la edición en el historial.

---

#### ÉPICA 3 (EP-03): Bandeja de Atención y Asignación de Responsable (10 SP)
*(Módulos MVP: Bandeja, Gestión — Listado, búsqueda y filtros básicos; Asignación de responsable)*

* **UH-12: Bandeja de Entrada de Solicitudes (3 SP)**
  * *Narrativa:* **Como** Operador de Soporte N1, **quiero** ver todos los tickets sin asignar en tiempo real, **para** revisarlos y distribuirlos al equipo correspondiente.
  * *Criterios de Aceptación:*
    * **Dado** un ticket en estado `Nuevo`, **cuando** el operador abre la bandeja, **entonces** aparece ordenado y destacado por su prioridad.

* **UH-13: Asignación de Responsable de Soporte (2 SP)**
  * *Narrativa:* **Como** Supervisor u Operador N1, **quiero** asignar un ticket a un responsable de soporte, **para** pasar el ticket a `Asignado`.
  * *Criterios de Aceptación:*
    * **Dado** un ticket `Nuevo`, **cuando** se selecciona un responsable de soporte, **entonces** el estado cambia a `Asignado` y se guarda el usuario asignado.

* **UH-14: Autoasignación Directa ("Tomar Ticket") (1 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** autoasignarme un ticket con un solo clic, **para** comenzar la atención de inmediato.
  * *Criterios de Aceptación:*
    * **Dado** un ticket sin asignar, **cuando** el operador presiona "Tomar Ticket", **entonces** queda asignado a su usuario y pasa a `Asignado`.

* **UH-15: Derivación a Nivel de Soporte Especializado (2 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** escalar el ticket a N2 o N3, **para** que intervenga un especialista técnico o de infraestructura.
  * *Criterios de Aceptación:*
    * **Dado** un ticket en atención, **cuando** se cambia el nivel de soporte, **entonces** se registra el escalamiento y queda disponible para el nuevo grupo.

* **UH-16: Reasignación de Responsable (2 SP)**
  * *Narrativa:* **Como** Supervisor, **quiero** reasignar un ticket indicando una justificación, **para** balancear la carga operativa o cubrir ausencias.
  * *Criterios de Aceptación:*
    * **Dado** un cambio de responsable, **cuando** se guarda con motivo, **entonces** el historial refleja el usuario anterior, el nuevo y la razón.

---

#### ÉPICA 4 (EP-04): Ciclo de Estados y Registro de Solución (14 SP)
*(Módulo MVP: Estados — Nuevo → Asignado → En curso → Resuelto → Cerrado)*

* **UH-17: Transición de Estado a "En Curso" (2 SP)**
  * *Narrativa:* **Como** Operador asignado, **quiero** cambiar el estado a `En Curso`, **para** indicar que el análisis técnico ha comenzado activamente.
  * *Criterios de Aceptación:*
    * **Dado** un ticket en `Asignado`, **cuando** el operador inicia el trabajo, **entonces** el estado pasa a `En Curso` y se registra la fecha/hora.

* **UH-18: Pausa de Gestión por Información Pendiente (2 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** marcar el ticket en espera de información adicional, **para** documentar que está detenido por causas externas.
  * *Criterios de Aceptación:*
    * **Dado** un ticket `En Curso`, **cuando** se solicita más información al usuario, **entonces** el ticket refleja la espera y se registra el comentario correspondiente.

* **UH-19: Registro Obligatorio de Solución (3 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** documentar la resolución técnica aplicada, **para** que el usuario conozca la respuesta y quede archivada.
  * *Criterios de Aceptación:*
    * **Dado** un ticket `En Curso`, **cuando** se carga la solución, **entonces** el texto de resolución es obligatorio para habilitar el paso a `Resuelto`.

* **UH-20: Registro de Solución Provisoria / Alternativa (3 SP)**
  * *Narrativa:* **Como** Operador de Soporte N2, **quiero** registrar si la solución fue provisoria (procedimiento alternativo), **para** restablecer el servicio asistencial mientras N3 resuelve la causa de fondo.
  * *Criterios de Aceptación:*
    * **Dado** un incidente operativo, **cuando** se aplica una solución temporal, **entonces** se guarda la descripción del procedimiento y la marca de solución provisoria.

* **UH-21: Transición a Estado "Resuelto" (2 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** marcar el ticket como `Resuelto`, **para** informar que la atención técnica ha finalizado exitosamente.
  * *Criterios de Aceptación:*
    * **Dado** un ticket con solución registrada, **cuando** se confirma la acción, **entonces** el estado cambia a `Resuelto` y se notifica al solicitante.

* **UH-22: Transición a Estado "Cerrado" (2 SP)**
  * *Narrativa:* **Como** Solicitante o Administrador, **quiero** validar la conformidad y pasar el ticket a `Cerrado`, **para** archivar el ciclo de atención de forma inmutable.
  * *Criterios de Aceptación:*
    * **Dado** un ticket `Resuelto`, **cuando** se confirma el cierre, **entonces** pasa a `Cerrado` y se bloquea cualquier edición posterior.

---

#### ÉPICA 5 (EP-05): Seguimiento, Notificaciones e Historial (9 SP)
*(Módulos MVP: Seguimiento, Historial, Notificaciones — Comentarios, trazabilidad y avisos básicos)*

* **UH-23: Comentarios Públicos de Seguimiento (2 SP)**
  * *Narrativa:* **Como** Solicitante u Operador, **quiero** intercambiar mensajes públicos en el hilo del ticket, **para** mantener una comunicación fluida sobre el avance del caso.
  * *Criterios de Aceptación:*
    * **Dado** un nuevo mensaje público, **cuando** se envía, **entonces** queda visible en el hilo del ticket para todos los involucrados.

* **UH-24: Notas Internas para el Equipo de Soporte (2 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** escribir notas técnicas internas invisibles para el solicitante, **para** coordinar diagnósticos entre técnicos.
  * *Criterios de Aceptación:*
    * **Dado** una nota marcada como privada, **cuando** un Solicitante consulta el ticket, **entonces** la nota no es visible en su pantalla.

* **UH-25: Avisos Básicos por Asignación y Cambio de Estado (2 SP)**
  * *Narrativa:* **Como** usuario del sistema, **quiero** recibir avisos visuales ante cambios de estado o asignaciones, **para** enterarme en tiempo real.
  * *Criterios de Aceptación:*
    * **Dado** un cambio en un ticket propio, **cuando** ocurre la acción, **entonces** aparece una alerta en pantalla con el detalle de la actualización.

* **UH-26: Aviso Destacado de Ticket Resuelto (1 SP)**
  * *Narrativa:* **Como** Solicitante, **quiero** ver claramente cuando mi ticket es marcado como `Resuelto`, **para** verificar la solución antes de cerrar.
  * *Criterios de Aceptación:*
    * **Dado** el pase a `Resuelto`, **cuando** el solicitante entra al sistema, **entonces** ve un aviso destacado de confirmación de solución.

* **UH-27: Historial y Trazabilidad de Cambios Relevantes (2 SP)**
  * *Narrativa:* **Como** Administrador o Auditor, **quiero** ver la cronología completa de cambios con fecha, hora y responsable, **para** garantizar la total transparencia del ciclo.
  * *Criterios de Aceptación:*
    * **Dado** cualquier cambio en un ticket, **cuando** se consulta el historial, **entonces** se listan todas las mutaciones sin posibilidad de ser borradas.

---

#### ÉPICA 6 (EP-06): Administración y Operación Centralizada (20 SP)
*(Módulos MVP: Administración, Bandeja — Usuarios, categorías y prioridades; Cockpit en pantalla única)*

* **UH-28: Interfaz Centralizada de Operación en Pantalla Única (6 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** operar en una sola pantalla con Filtros (Col 1), Bandeja (Col 2) y Detalle/Gestión (Col 3), **para** resolver tickets rápidamente sin recargar la página.
  * *Criterios de Aceptación:*
    * **Dado** el ingreso al sistema, **cuando** el operador hace clic en un ticket de la lista, **entonces** el detalle y las acciones se abren inmediatamente en la tercera columna.

* **UH-29: Selector Rápido de Rol de Usuario (3 SP)**
  * *Narrativa:* **Como** evaluador o usuario de pruebas, **quiero** alternar entre los roles de Solicitante, Soporte y Admin con un botón en la barra superior, **para** validar la experiencia de cada perfil en segundos durante la demo.
  * *Criterios de Aceptación:*
    * **Dado** el selector en el encabezado, **cuando** se elige otro rol, **entonces** la interfaz adapta los permisos y vistas instantáneamente.

* **UH-30: Listado, Búsqueda y Filtros Básicos (4 SP)**
  * *Narrativa:* **Como** Operador de Soporte, **quiero** filtrar la bandeja por estado, plataforma, cliente o buscar por palabra clave, **para** localizar cualquier ticket en menos de 2 segundos.
  * *Criterios de Aceptación:*
    * **Dado** un criterio de búsqueda, **cuando** el usuario escribe o selecciona un filtro, **entonces** la lista se actualiza al instante.

* **UH-31: Administración de Usuarios y Asignación de Roles (4 SP)**
  * *Narrativa:* **Como** Administrador, **quiero** listar, crear y asignar roles a los usuarios, **para** gestionar el personal operativo de Quantux Salud.
  * *Criterios de Aceptación:*
    * **Dado** el módulo de administración, **cuando** se crea un usuario, **entonces** queda habilitado para operar según su perfil asignado.

* **UH-32: Administración de Categorías y Prioridades (3 SP)**
  * *Narrativa:* **Como** Administrador, **quiero** administrar las plataformas, tipos de ticket y niveles de prioridad, **para** mantener el sistema alineado a la evolución del catálogo corporativo.
  * *Criterios de Aceptación:*
    * **Dado** el panel de configuración, **cuando** se edita una categoría, **entonces** los formularios de alta y filtros reflejan los cambios de forma consistente.

---

### 5. Épica de Gobernanza, Calidad PMI+IA y Mejoras de Backlog (EP-07)
*Marco de Referencia:* **DOC-GOV-008** (`docs/08_MARCO_DE_TRABAJO_PMI_IA_Y_GOBERNANZA_CALIDAD.md`)

En virtud del protocolo de adaptación PMI y aseguramiento de calidad, todo gap funcional, mejora técnica u oportunidad se gestiona atómicamente en formato de Historia de Usuario con criterios Gherkin y criterios de adaptación metodológica:
* **GAP-01 (5 SP):** Formalización del Marco PMI+IA y Protocolo de Calidad en Suite Documental.
* **MEJ-01 (5 SP):** Automatización de Bucle TDD y Pre-commit Hooks para Validadores OJO.
* **OM-01 (8 SP):** Trazabilidad Bidireccional de Tickets hacia Contratos OpenAPI y Esquemas DDL.
* **GAP-02 (5 SP):** Blindaje de Integridad de Contexto para Auditorías TQM y Cero Scope Creep.
* **MEJ-02 (3 SP):** Soporte Nativo de Enlaces Documentales y Modal de UH en Tablero Scrumban.

#### Nuevos Items de Alta Prioridad Incorporados al Sprint Backlog (Sprint 6):
* **UH-66 [P1 - 3 SP]:** Depuración de Componentes de Debug, Subtítulo Redundante y Limpieza Zen del Portal del Solicitante.
  * *Narrativa:* **Como** Profesional Médico y Solicitante del Centro de Ayuda, **quiero** un portal limpio y sin ruido visual de desarrollo (sin pastillas de mockups 1 a 7, sin subtítulo redundante y sin elementos desbordados), **para** concentrarme exclusivamente en resolver mi consulta sin distracciones.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el ingreso al sistema, **cuando** se visualiza la barra de navegación superior, **entonces** no existe el contenedor de debug `#nav-mockup-pills` (1. Portal a 7. Config ITIL).
    * **Dado** el Portal del Solicitante en reposo, **cuando** se renderiza el Hero centrado, **entonces** solo se muestra el logo, el título "¿En qué podemos asistirte hoy?" y el buscador, sin el subtítulo redundante.
    * **Dado** cualquier ancho de pantalla, **cuando** se renderiza la cabecera, **entonces** las acciones (`+ Crear Solicitud`, `Mis Solicitudes`, Chip de Perfil) se alinean perfectamente sin truncamiento ni botones espurios [M...].
* **ISSUE-04 [P1 - 3 SP]:** Imposibilidad de scroll en desplegable de temas oficiales homologados (Typeahead).
  * *Componente:* `frontend/index.html` (`#requester-typeahead-dropdown`), `frontend/js/typeahead.js`.
  * *Causa:* Desbordamiento vertical fuera de viewport con `overflow: hidden` en contenedores superiores.
  * *Criterios:* Scroll vertical fluido habilitado con `overflow-y: auto !important` y `max-height: calc(100vh - 420px)`.
* **ISSUE-05 [P1 - 2 SP]:** Botón 'Hacer otra consulta' no oculta ni reinicia el historial de consultas anteriores.
  * *Componente:* `frontend/js/app.js` (líneas 2876, 2896, 2909).
  * *Causa:* Invocación a `focusRequesterChatInput()` en lugar de reseteo completo con `clearRequesterChat()`.
  * *Criterios:* Al presionar "Hacer otra consulta", el stream previo se oculta de inmediato y se restaura el Hero centrado con input en blanco.
* **ISSUE-06 [P1 - 3 SP]:** Falla en visualización de Constancia de Resolución Inmediata y campo/toast fantasma sin texto.
  * *Componente:* `frontend/js/app.js` (`requesterAiResolve`), `frontend/css/styles.css` (`.toast`).
  * *Causa:* Notificación toast con texto blanco puro (`#FFFFFF`) sobre fondo blanco hueso (`#F8FAFC`) creando una caja fantasma sin texto legible, y falta de anclaje de la constancia formal al hacer clic en "Ver en Mis Solicitudes".
  * *Criterios:* Toasts con contraste corporativo de alto impacto (`#0F172A`) y apertura de Constancia FCR Oficial certificada con número de ticket.

* **UH-67 [P1 - 5 SP]:** Subniveles Interactivos de Navegación en Árbol N1 y Separación de Capas Médico vs Soporte.
  * *Evidencia Visual:* ![Captura UH-67](assets/capturas/UH-67_doble_informacion_subniveles_arbol.png)
  * *Narrativa:* **Como** Profesional Médico y Solicitante, **quiero** que al consultar por un tema del árbol de decisiones N1 el sistema me presente subniveles de navegación claros e interactivos y una respuesta sin ambigüedades, separando la acción resolutiva asistencial de los fundamentos normativos para soporte, **para** comprender de inmediato qué debo hacer en Consultorio Digital sin saturarme de información técnica no aplicable.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** una consulta que activa un árbol con subramas (ej: Matrícula SISA / Vademécum), **cuando** el Asistente N1 responde, **entonces** despliega chips de navegación interactiva (`[ Matrícula SISA ]`, `[ Vademécum ]`, `[ Validación Biométrica ]`, `[ Receta en Contingencia ]`) para desambiguar la necesidad.
    * **Dado** el contenido de la respuesta, **cuando** se renderiza para el médico, **entonces** la Capa 1 presenta únicamente el paso resolutivo inmediato en lenguaje claro, y la Capa 2 (marco normativo, leyes, validaciones de backend) queda accesible bajo un botón/acordeón colapsable `"▾ Ver Fundamento Normativo y Técnico Oficial"`.
    * **Dado** el texto de respuesta con formato, **cuando** se renderiza en pantalla, **entonces** los asteriscos de Markdown se transforman en negritas y viñetas HTML limpias.
  * *Criterios de Adaptación PMI (4 Pasos):*
    1. Reducción de carga cognitiva en el punto de atención médica.
    2. Separación de incumbencias: Médico asistencial (Paso resolutivo) vs Analista de soporte (Fundamento técnico/regulatorio).
    3. Reutilización del catálogo local y del endpoint `/api/ai/triage`.
    4. Trazabilidad con captura original `UH-67_doble_informacion_subniveles_arbol.png`.

* **UH-68 [P1 - 2 SP]:** Remoción de Métricas y Etiquetas de SLA en el Portal del Solicitante / Médico.
  * *Evidencia Visual:* ![Captura UH-68](assets/capturas/UH-68_quitar_sla_solicitante.png)
  * *Narrativa:* **Como** Profesional Médico Solicitante, **quiero** que el sistema no exhiba tiempos ni etiquetas de compromisos de SLA internos de TI en mi vista ni en mis comprobantes de solicitud, **para** que la interfaz esté libre de métricas burocráticas internas que nadie solicitó y que no aportan valor asistencial a mi práctica clínica.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el modal de detalle de solicitud del solicitante, **cuando** se visualiza el asunto registrado, **entonces** no figura la etiqueta `⏱️ SLA de Atención: < 15 min`.
    * **Dado** un incidente escalado a Soporte N2 en el chat, **cuando** se renderiza la tarjeta de confirmación, **entonces** no figura la línea `• SLA de Atención N2: < 15 minutos en cola prioritaria`.
    * **Dado** el acceso de analistas N2, supervisores y líderes en la Mesa de Ayuda y Tableros ITIL, **cuando** se gestionan los tickets, **entonces** los cálculos y monitores de SLA permanecen plenamente operativos para la gestión operativa interna.
  * *Criterios de Adaptación PMI (4 Pasos):*
    1. Simplificación y despojo de ruidos burocráticos hacia el usuario final asistencial.
    2. Respeto a las directivas del Solution Owner: "quita el sla, nadie lo pidió".
    3. Verificación de no regresión en endpoints backend de cálculo SLA ITIL.
    4. Trazabilidad con captura original `UH-68_quitar_sla_solicitante.png`.

* **ISSUE-07 [P1 - 3 SP]:** Erradicación de Terminología Médica/Hospitalaria en Mensajes y Estados del Sistema de TI.
  * *Evidencia Visual:* ![Captura ISSUE-07](assets/capturas/ISSUE-07_terminologia_medica_guardia.png)
  * *Severidad:* P1 — Alta Prioridad / Dominio Conceptual y Vocabulario.
  * *Componente:* `frontend/index.html` (navbar, placeholders), `frontend/js/app.js` (`openRequesterTicketDetail`, `renderRequesterChatStream`).
  * *Descripción:* El sistema utiliza terminología de la medicina asistencial ('Estado de Guardia Técnica', 'Transcripción clínica completa', 'Asunto Clínico Registrado', 'Conversación y Contexto Asistencial Transferido', 'Centro de Ayuda & Guardia Médica', 'Escribe tu consulta o síntoma médico') para describir procesos y estados que corresponden estrictamente al soporte técnico de software TI. El Solution Owner ha establecido taxativamente: "no deben haber en el producto términos similares a los usados en la terminología médica".
  * *Solución Estandarizada ITIL:*
    1. `ESTADO DE GUARDIA TÉCNICA:` -> `ESTADO DE LA SOLICITUD DE SOPORTE:`
    2. `transcripción clínica completa` -> `diagnóstico y detalle técnico transferido`
    3. `ASUNTO CLÍNICO REGISTRADO:` -> `ASUNTO DE LA SOLICITUD:`
    4. `CONVERSACIÓN Y CONTEXTO ASISTENCIAL TRANSFERIDO:` -> `HISTORIAL Y CONTEXTO DE LA CONSULTA:`
    5. `Centro de Ayuda & Guardia Médica` (Navbar) -> `Centro de Ayuda & Mesa de Soporte`
    6. Placeholder del chat: `Escribe tu consulta sobre Consultorio Digital (ej: matrícula provincial, error en receta, cambio de cuit)...`
    7. `Guardia N1/N2` -> `Soporte N1/N2`
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el modal de solicitud y el chat del solicitante, **cuando** se visualizan los estados, **entonces** no figura la palabra "Guardia", "Clínico" o "Asistencial" para referirse a tickets, operadores o sistemas TI.
    * **Dado** cualquier mensaje generado por el sistema, **cuando** describe el flujo de soporte, **entonces** emplea vocabulario estándar de Service Desk ("Solicitud de Soporte", "Detalle Técnico", "Mesa de Ayuda").
    * **Dado** el issue registrado en el tablero, **cuando** se abre la tarjeta, **entonces** presenta la captura con el recuadro verde "ESTADO DE GUARDIA TÉCNICA" como evidencia.

* **UH-69 [P1 - 8 SP]:** Bot Gestor de Tickets Multi-Rol, Evaluación KCS v6 y Trazabilidad de Tickets Contribuyentes en Base de Conocimiento.
  * *Narrativa:* **Como** Solution Owner, Analista de Soporte y Profesional Asistencial, **quiero** que el Bot Gestor de Tickets avance automáticamente los casos interactuando con todos los roles y sectores institucionales, registre los diálogos con autor, rol y sector, evalúe según el negocio si el caso capitaliza conocimiento para asociarlo a la Base de Conocimiento al resolverse, y permita que al consultar la KB se visualicen los tickets que sumaron información, **para** asegurar la continuidad operativa, trazabilidad conversacional y enriquecimiento continuo de la Base de Conocimiento (KCS v6) sin sobrecarga burocrática manual.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** un ticket en cualquier estado del flujo ITIL (`NUEVO`, `ASIGNADO`, `EN_CURSO`), **cuando** el bot gestor procesa un paso, **entonces** interactúa con el rol correspondiente (`SOLICITANTE`, `SOPORTE_N1`, `ESPECIALISTA_N2`, `ADMIN_INFRAESTRUCTURA_N3`, `TEAM_LEADER`, `PASARELA_TERCEROS`) y su sector (Guardia Central, Farmacia y Triage, Integraciones y Pasarelas OSDE/SISA, Infraestructura N3), registrando cada mensaje en `ticket_comments` con `author_role` y `author_sector`.
    * **Dado** un ticket en transición a `RESUELTO`, **cuando** el bot evalúa la resolución, **entonces** si es una incidencia técnica transferible (errores 500/504, caídas de pasarela, timeout SISA, nomencladores) lo asocia al artículo KB creando la entidad `KBArticleContribution` y marcando `contributed_to_kb = True` y `associated_kb_id`; y si es una rutina administrativa sin valor de conocimiento (reseteo simple, duplicado) lo resuelve justificando la no asociación.
    * **Dado** un usuario u operador que consulta la Base de Conocimiento por tema (vía listado `/articles`, detalle `/articles/{id}`, o `/copilot-chat`), **cuando** se inspecciona el artículo o se responde la consulta, **entonces** el sistema exhibe los tickets específicos (ID, rol, sector, autor, fecha y síntesis de solución/RCA) que sumaron información al resolverse.
    * **Dado** el backend FastAPI y el simulador en segundo plano `live_simulator`, **cuando** el bot se ejecuta o se invocan los endpoints `/api/v1/tickets/bot/advance-cycle`, `/bot/step`, `/bot/advance-to-resolution` y `/kb-contribution`, **entonces** responden con HTTP 200 y actualizan la persistencia relacional SQLite con índices optimizados.
  * *Criterios de Adaptación PMI (4 Pasos):*
    1. Especificación predictiva de la matriz de roles, sectores y reglas de negocio KCS v6 combinada con ejecución ágil automatizada.
    2. Cumplimiento de la Pizarra Neutral Quantux (cero fondos oscuros masivos, cero rojos `#DC2626` / `#EF4444`, acento Teal `#00A896`).
    3. Verificación técnica automatizada con suite de pruebas dedicada (`test_ticket_manager_bot_and_kb.py`: 4/4 tests OK).
    4. Trazabilidad inmutable e indexada en SQLite (`ix_kb_contributions_article`, `ix_kb_contributions_ticket`) y sincronización con el tablero Scrumban.

* **UH-70 [P1 - 2 SP]:** Menú Lateral Zen: Ocultamiento de Accesos a Tablero de Control y Torre de Control Preservando Funcionalidad Subyacente.
  * *Narrativa:* **Como** Operador Asistencial y Solution Owner, **quiero** que el menú lateral oculte los botones de Tablero de Control y Torre de Control manteniendo el código y la capacidad analítica intacta, **para** que la barra de navegación lateral sea minimalista y enfocada en la atención sin ruido de accesos no utilizados en la rutina diaria.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el menú lateral de navegación, **cuando** se renderizan los ítems principales, **entonces** los accesos `#tab-dashboard` y `#tab-team-leader` están completamente invisibles (`display: none !important;`).
    * **Dado** el código JavaScript y backend, **cuando** se consultan las métricas o se abren las vistas programáticamente, **entonces** todas las funciones y controladores operan normalmente sin excepciones.
    * **Dado** el registro en el Scrumban, **cuando** se abre la tarjeta UH-70, **entonces** exhibe la captura de evidencia remitida por el Solution Owner.

* **MEJ-12 [P2 - 3 SP]:** Barra de Progreso Unificada en Tareas en Ejecución (Sprint 6, estado `done`).
  * *Nota de Evolución / MEJ-16:* Conforme a la Directiva OJO de Pizarra Neutral Quantux, cualquier tinte rojizo fue erradicado y unificado en la paleta oficial Slate `#334155` y Teal `#00A896` para evitar alarmas visuales en el monitoreo.

* **ISSUE-55 [P1 - 2 SP]:** Enlace Interactivo en Badge de Ticket en Constancia de Resolución FCR (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Profesional Solicitante y Auditor TI, **quiero** que el badge de ticket `#TKT-2026-0348` de la constancia emitida por el asistente virtual funcione como un enlace interactivo, **para** acceder de inmediato a la auditoría técnica y conversación completa del ticket.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el mensaje de resolución emitido por el Asistente TI, **cuando** el usuario hace clic sobre el badge interactivo `#TICK-...`, **entonces** se abre directamente el modal con el detalle y la traza completa de la solicitud.

* **ISSUE-56 [P1 - 3 SP]:** Disponibilidad y Persistencia de Ticket de Autogestión FCR en Historial del Solicitante (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Profesional Solicitante, **quiero** que el ticket generado como constancia de solución figure de manera garantizada en mi historial de solicitudes, **para** que nunca retorne vacío y mantenga trazabilidad para auditorías clínicas y facturación.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** un ticket resuelto por autogestión FCR, **cuando** el profesional abre "Mis Solicitudes", **entonces** figura listado de forma inmediata con su identificador, asunto clínico, fecha y estado de resolución.

* **ISSUE-65 [P1 - 3 SP]:** Persistencia de Configuración de SLA sin Cierre de Diálogo y Actualización Reactiva en Ficha 360° del Cliente (Sprint 7, estado `sprint` - Prioridad 1).
  * *Narrativa:* **Como** Administrador del Sistema y Solution Owner, **quiero** guardar las modificaciones en la matriz de tiempos SLA institucionales sin que se cierre intempestivamente el modal de edición de institución, **para** verificar de inmediato la persistencia correcta y observar los cambios reflejados en vivo en los 4 tiles P1-P4 de la Ficha 360°.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el modal de Configuración Institucional, **cuando** el usuario modifica las horas de SLA y presiona "Guardar Configuración", **entonces** la petición AJAX se despacha asincrónicamente a `/api/v1/masters/organizations/{id}/settings`, se emite una notificación toast de éxito, el modal permanece abierto y la ficha 360° en segundo plano actualiza los tiles de SLA reactivamente.

* **MEJ-13 [P2 - 2 SP]:** Depuración de Botones Redundantes 'Resolver Ticket' y 'Registrar Notas' (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Operador de Soporte, **quiero** eliminar acciones duplicadas en el panel lateral de 'Acciones del Ticket', **para** simplificar la toma de decisiones y evitar confusión entre la botonera inferior de respuesta y la barra lateral.

* **MEJ-14 [P2 - 2 SP]:** Visualización Permanente y Dinámica de la Descripción de Estado en Workspace (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Operador Asistencial, **quiero** ver de forma explícita el significado operativo del estado actual del ticket (ej. qué implica 'En Espera del Prestador'), **para** comprender de inmediato qué acción se espera sin tener que consultar la documentación externa.

* **MEJ-15 [P2 - 2 SP]:** Diferenciación Cromática de Botonera Dual 'Responder' vs 'Responder y Resolver' (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Operador de Soporte, **quiero** una clara distinción visual entre el envío de un comentario intermedio y el cierre resolutivo de un ticket, **para** prevenir resoluciones accidentales por pulsaciones equivocadas.

* **MEJ-16 [P1 - 2 SP]:** Directiva de Diseño Quantux: Erradicación de Tonos Rojizos en Barras e Interfaz (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Solution Owner y Auditor OJO, **quiero** asegurar la total erradicación de colores `#DC2626`, `#EF4444` y fondos rojizos en toda la interfaz, migrando a tonos Slate `#334155` y Teal Quantux `#00A896`, **para** cumplir estrictamente la política institucional de Pizarra Neutral.

* **ISSUE-78 [P1 - 3 SP]:** Indicador de Estado Operativo de SLA Dinámico (Pausado / Activo con Segundos) (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Operador y Team Leader, **quiero** visualizar el contador de SLA con segundero en vivo y su estado formal (Activo / En Pausa por Espera de Prestador), **para** auditar el consumo exacto de tiempo sin discrepancias.

* **ISSUE-79 [P2 - 2 SP]:** Depuración de Botonera Redundante de Asignación en Agent Workspace (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Especialista Técnico, **quiero** una única botonera limpia de autoasignación o reasignación, **para** despejar la interfaz de trabajo.

* **ISSUE-80 [P1 - 3 SP]:** Evaluación Obligatoria y Renderizado Dinámico de Impacto en Producto y Negocio (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Auditor Sanitario y Gerencia General, **quiero** que todo ticket registre obligatoriamente su impacto operativo en el negocio de salud, **para** alimentar la priorización automática y los reportes ejecutivos.

* **ISSUE-81 [P2 - 2 SP]:** Botón de Cierre 'X' Circular de Alto Contraste y Cierre por Escape en Lightbox (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Usuario y Operador, **quiero** cerrar fácilmente el visor modal de capturas adjuntas mediante la tecla Escape, clic en el fondo o un botón 'X' circular destacado, **para** agilizar la revisión documental.

* **ISSUE-82 [P1 - 2 SP]:** Ocultamiento Total del Módulo 'Configuración' en Barra Lateral (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Solution Owner, **quiero** ocultar el acceso a Configuración en la barra lateral para todos los roles, **para** resguardar los parámetros globales del sistema.

* **ISSUE-83 [P1 - 3 SP]:** Ocultamiento de 'Niveles ITIL' y Formalización de Parametrización por Base de Datos (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Arquitecto de Software y Solution Owner, **quiero** que la estructura de niveles ITIL (N1, N2, N3) se configure directamente por base de datos, **para** asegurar inmutabilidad y cumplimiento estricto con ITIL 4.

* **PWA-01 [P1 - 4 SP]:** Aplicación Móvil Descargable (Progressive Web App - PWA v4.4) (Sprint 7, estado `sprint`).
  * *Narrativa:* **Como** Médico Asistencial o Directivo en Movilidad, **quiero** instalar la aplicación HealthDesk Quantux en mi smartphone o tablet desde el navegador, **para** consultar y gestionar solicitudes de soporte con experiencia nativa y soporte offline.

---

### 4. Gobernanza del Backlog: Cierre de Sprint 6 y Ciclo Operativo de Sprint 7

> [!IMPORTANT]
> **CERTIFICACIÓN FORMAL DE CIERRE DE SPRINT 6:**  
> Habiéndose certificado el **100% de las 93 tarjetas del Sprint 6 en estado Done**, el sistema queda blindado bajo el protocolo notarial de **Siete Llaves**.  
> El **Sprint 7** se encuentra formalmente **ACTIVO** con 13 tarjetas priorizadas en el **Sprint Backlog (35 SP)** para ejecución inmediata, preservando como hito rector inamovible la **Demostración Final ante el Comité Evaluador el 01 de Octubre de 2026**.

---

## 5. GOBERNANZA DE CONFIGURACIÓN ITIL v4 Y DESACOPLAMIENTO DE NIVELES (SPRINT 7)

> ### 📌 DIRECTIVA DE ARQUITECTURA ITIL v4: PARAMETRIZACIÓN INICIAL POR BASE DE DATOS
> En concordancia con las mejores prácticas internacionales de gestión de servicios de tecnología en salud (**ITIL v4 Service Management Framework**), la funcionalidad interactiva de edición y parametrización de **Niveles de Atención ITIL (N1 / N2 / N3)** y el módulo global de **Configuración de Sistema** se encuentran deliberadamente **ocultos y protegidos** en la interfaz de usuario para la totalidad de los roles y perfiles operativos.
> 
> **Fundamentación y Criterios Técnicos:**
> 1. **Inmutabilidad y Consistencia Operativa:** La matriz de niveles de soporte (Nivel 1 Triage Asistencial/FCR, Nivel 2 Especialistas de Plataformas Clínicas HIS/EHR/Facturación, Nivel 3 Infraestructura de Red & Pasarelas Sanitarias SISA/OSDE) se provisiona y versiona directamente a nivel de base de datos (`seed_database_v4.py` / tablas relacionales de soporte), garantizando coherencia formal ante auditorías hospitalarias.
> 2. **Prevención de Desalineación Operativa:** Se neutraliza el riesgo de modificaciones no autorizadas o accidentales de matrices de escalamiento clínico desde la interfaz de usuario.
> 3. **Desacoplamiento de Responsabilidades:** La política de niveles de servicio (SLA) se administra en la capa de persistencia institucional centralizada, mientras el front-end consume de forma reactiva y auditable las métricas de respuesta y resolución en tiempo real.

