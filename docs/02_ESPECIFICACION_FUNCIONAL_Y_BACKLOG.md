# 📑 DOCUMENTO 2: ESPECIFICACIÓN FUNCIONAL Y BACKLOG
**Código:** DOC-REQ-002 (Versión 1.1 Oficial)
**Proyecto:** HealthDesk Quantux — Sistema Centralizado de Gestión de Tickets de Soporte
**Organización:** Quantux Salud
**Solution Owner:** Freddy Cortés (Analista Funcional)
**Dimensión:** 6 Épicas | 48 Historias de Usuario Consolidadas | 148 Story Points
**Fecha de Línea Base:** 28 de Agosto de 2026 | **Fecha de Versión 1.1:** 26 de Septiembre de 2026
**Comité Evaluador:** Paula Sbarbati, Diego Martínez, Carolina Brizuela, Nicolás Sánchez

---

### Control de Versiones y Distribución
| Versión | Fecha | Responsable | Detalle de Modificaciones / Estado |
| :--- | :--- | :--- | :--- |
| **v1.0** | 28/08/2026 | Freddy Cortés | **Línea Base Funcional Oficial del MVP:** 32 Historias de Usuario, 6 Épicas, circuitos de 5 estados ITIL y catálogos de 9 plataformas y 14 clientes. |
| **v1.1** | 26/09/2026 | Freddy Cortés | **Consolidación de Backlog (48 UHs), Política de Scope Freeze y Aislamiento de Evolutivos:** Congelamiento de alcance para demo del 01-Oct-2026, incorporación de UH-33 a UH-69, y derivación mandatoria de nuevos requerimientos al Product Backlog. |

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

*(El detalle completo de narrativas, escenarios Gherkin y criterios de adaptación se encuentra en el Documento DOC-GOV-008, DOC-QA-004 y en el Tablero Scrumban interactivo docs/00_Tablero_Scrumban_Quantux.html).*

---

### 4. Gobernanza del Backlog: Alcance Cerrado (Scope Freeze) y Trazabilidad

> [!IMPORTANT]
> **POLÍTICA MANDATORIA DE ALCANCE CERRADO (SCOPE FREEZE):**  
> Habiéndose consolidado la especificación de las **48 Historias de Usuario (148 Story Points)**, el alcance funcional del producto para la presentación oficial del **01 de Octubre de 2026** queda formal y estrictamente cerrado.  
> 1. Ninguna nueva historia de usuario, requerimiento de alcance o funcionalidad adicional podrá ser admitida para desarrollo en el Sprint 6 (Hardening).  
> 2. Toda propuesta, optimización futura o requerimiento emergente (por ejemplo, el comportamiento de botones al cerrar tickets catalogado en `ISSUE-19`) será registrado exclusivamente en la columna `📋 Product Backlog` con estado `backlog`.  
> 3. La única actividad autorizada en el ciclo actual consiste en:  
>    * Cierre de no-conformidades y retrabajos funcionales (`UH-67`, `MEJ-08`).  
>    * Aseguramiento de calidad TDD y cumplimiento estricto de la Regla OJO / Pizarra Neutral.  
>    * Congelamiento técnico total el **Lunes 28 de Septiembre a las 18:00 hs**, garantizando 48 hs libres al Solution Owner para la preparación y ensayos de la demo.

