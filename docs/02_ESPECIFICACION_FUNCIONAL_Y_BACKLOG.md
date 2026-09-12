# 📑 DOCUMENTO 2: ESPECIFICACIÓN FUNCIONAL Y BACKLOG
**Código:** DOC-REQ-002 (Versión 1.0 Oficial)
**Proyecto:** HealthDesk Quantux — Sistema Centralizado de Gestión de Tickets de Soporte
**Organización:** Quantux Salud
**Solution Owner:** Freddy Cortés (Analista Funcional)
**Dimensión:** 6 Épicas | 32 Historias de Usuario | 75 Story Points
**Fecha:** 28 de Agosto de 2026

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
