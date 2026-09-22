import sqlite3
import datetime

conn = sqlite3.connect('backend/healthdesk.db')
cursor = conn.cursor()

now = datetime.datetime.utcnow().isoformat()

articles = [
    {
        "title": "Matriz Maestra de Interoperabilidad: Socio, Prestador y Consultorio (SAP, CRM, IAM, Turnos, Cartilla, PAU)",
        "category": "Interoperabilidad & Soporte CD2",
        "tags": "interoperabilidad, matriz, sap, crm, iam, turnos, cartilla, pau, socio, prestador, consultorio",
        "space_name": "Soporte N1/N2/N3",
        "content": """# Matriz Maestra de Interoperabilidad: Ciclo de Vida del Dato

Documento oficial de referencia permanente para el equipo de soporte técnico sobre el origen, sincronización y actualización de atributos en Consultorio Digital 2 (CD2).

---

## 1. Entidad SOCIO (Paciente)

| Atributo | Origen del Dato | Cuándo y Cómo se Actualiza | Regla Operativa de Soporte |
| :--- | :--- | :--- | :--- |
| **Nombre y apellido** | Caché de socios (SAP) / Servicio de Socios | SAP notifica novedades. Se recarga al consultar turnos del prestador. | El dato maestro reside en SAP. |
| **Número de socio OSDE** | Caché de socios (SAP) / Servicio de Socios | SAP notifica novedades. Se recarga al consultar turnos del prestador. | Inmutable desde la interfaz de CD2. |
| **IC (Identificador OSDE)** | Identificador único OSDE | **No se modifica.** | Clave primaria inmutable para la unificación de historia clínica. |
| **DNI** | Caché de socios (SAP) / Servicio de Socios | Notificación de novedades SAP o con la generación del turno. | Verificado contra padrón de afiliados. |
| **Plan OSDE** | Caché de socios (SAP) / Servicio de Socios | Notificación de novedades SAP o con la generación del turno. | Determina cobertura y arancel de atención. |
| **Teléfono** | Solicitud de turnos desde el frontend (dispara sincronización con caché de socios y consulta a SAP si difiere). | Al solicitar turnos del prestador, se sincronizan los turnos del paciente y se coteja con SAP. | Si difiere de la base local, la consulta a SAP prevalece. |
| **Email** | Sincronización en turnos con caché SAP y registro de turnos. | **Creación del paciente:** Se crea automáticamente al generar su primer turno con el mail y teléfono iniciales.<br>**Turnos posteriores:** En cada nuevo turno se adoptan el mail y teléfono específicos cargados para esa cita (sin importar si difieren de los históricos). | Las notificaciones y recordatorios se envían a los datos cargados en ese turno específico. |
| **Género** | Caché de socios (SAP) / Servicio de Socios | Notificación de novedades SAP o recarga de turnos. | Regulado por padrón central. |
| **Fecha de nacimiento** | Solicitud de turnos desde el frontend con sincro a caché de socios y SAP. | Al recargar turnos al prestador. | Cotejado contra padrón central de afiliados. |

---

## 2. Entidad PRESTADOR (Profesional Médico)

| Atributo | Origen del Dato | Cuándo y Cómo se Actualiza | Regla Operativa de Soporte |
| :--- | :--- | :--- | :--- |
| **Nombre y apellido** | Servicio de Turnos | Se verifica y actualiza cada vez que se genera un turno. | Impacta en la cartilla y la cita. |
| **CUIT (AFIP)** | Actualización manual | Actualización manual administrativa. | Requiere validación de constancia de inscripción AFIP. |
| **IC (Identificador Comercial)** | Login / CD | Validar IC de login, consultar a Ezequiel Cupito y actualizar en CD. | Crucial para unificación de cuentas duplicadas. |
| **Teléfono (Mis Datos)** | Servicio de Turnos | Cada vez que se genera un turno. | El profesional puede editarlo desde su perfil de Extranet. |
| **Email (Mis Datos)** | Servicio de Turnos | Cada vez que se genera un turno. | El profesional puede editarlo desde su perfil de Extranet. |
| **Prefijo Académico (Dr. / Lic.)** | Cartilla Médica (Ana Laura) / CRM (Contratos) | Se contempló que cuando esté vacío no tenga valores por defecto forzados. | No se implementó lógica para actualizarlo basado en el turno. Para turnos futuros masivos se requiere script batch. |
| **Matrículas (Nacional / Provincial)** | CRM | Se verifica directamente contra CRM. | Si está bloqueada, se coteja SISA y se aplica bypass de selección. |
| **Mail de login** | IAM | Validar IC de login, consultar a Ezequiel Cupito y actualizar en CD. | Gestionado a través del proveedor de identidad federada. |
| **Terminal** | CRM | Cada vez que se genera un turno o cuando el prestador ingresa a la plataforma. | Debe coincidir 100% con la región configurada. |
| **Operador** | CRM | Cada vez que se genera un turno o cuando el prestador ingresa a la plataforma. | Debe coincidir 100% con la filial y efector. |
| **Nombre en la web** | IAM | Se envía a IAM para corrección. Se deriva ticket a **MDA-Aplicaciones N1** solicitando pase a IAM. | Si el nombre en la web difiere de la videollamada, el primero es IAM y el segundo Turnos/CRM. |

---

## 3. Entidad CONSULTORIO (Institución / Sede)

| Atributo | Origen del Dato | Cuándo y Cómo se Actualiza | Regla Operativa de Soporte |
| :--- | :--- | :--- | :--- |
| **Dirección** | Base de Datos CD2 | **Actualización manual:** Solicitar ticket PAU a Mesa de Ayuda, armar y validar query en BD. | No editable directamente por frontend por integridad fiscal. |
| **Teléfono** | Base de Datos CD2 | **Actualización manual:** Solicitar ticket PAU a Mesa de Ayuda, armar y validar query en BD. | Requiere autorización y pase a DBA. |
| **Email de Notificaciones** | Servicio de Turnos | **No se actualiza automáticamente.** La mensajería toma el mail del JSON de confirmación. Lo modifica el prestador desde Extranet/Mis Datos. | **Regla de oro:** Se envía notificación a 1 sola casilla de mail: la configurada como principal en Cartilla Médica. |
| **Terminal y Operador** | CRM | Cada vez que se genera un turno. | Asignados según filial y punto de atención. |
| **Baja de Consultorio** | Base de Datos CD2 | **Baja lógica manual:** Se ejecuta `db.institutions.updateOne({ _id: ObjectId("...") }, { $set: { isDeleted: true } })`. | Nunca eliminar físicamente el registro (conservar integridad referencial). |
"""
    },
    {
        "title": "Manual Técnico-Funcional CD2: Arquitectura del Ecosistema, Microservicios y Cloud Run",
        "category": "Arquitectura & Microservicios CD2",
        "tags": "arquitectura, microservicios, cloud run, sse, mtls, jitsi, webrtc, jwt, veracode, gcs",
        "space_name": "Soporte N2/N3 & DevOps",
        "content": """# Manual Técnico-Funcional CD2: Arquitectura del Ecosistema y Microservicios

## 1. Componentes Principales
* **Frontend (`consultorio-frontend`, `consultorio-landing-socio`):** Capa de interfaz web SPA responsiva para prestadores y socios.
* **Backend Core & Negocio (`consultorio-api-core`, `consultorio-backend-negocio`):** Orquestador central de lógica clínica, reglas de negocio y procesamiento transaccional de peticiones.
* **Mensajería y Notificaciones (`consultorio-mensajeria`, `consultorio-notif-sender`):** Generador de prescripciones en PDF y despacho multicanal de notificaciones por Correo Electrónico y WhatsApp.
* **Microservicio de Cifrado (`consultorio-cifrado`):** Componente público que desencripta las URLs de recetas y certificados médicos, recuperando los archivos PDF almacenados en Google Cloud Storage (GCS).
* **Eventos en Tiempo Real (`web-event-prestadores`):** Canal de Server-Sent Events (SSE) desplegado sobre Google Cloud Run que notifica al médico en tiempo real el ingreso de pacientes a la sala de espera virtual.
* **Capa de Caché (`cache-prestadores`, `cache-socios`):** Optimización en memoria de consultas frecuentes de datos de usuarios y afiliados.

## 2. Seguridad e Infraestructura
* **Autenticación mTLS:** Enlace de transporte seguro con autenticación mutua TLS (mTLS) entre Quercus y el backend de CD2.
* **Seguridad de Código y JWT:** Análisis estático de vulnerabilidades continuo mediante Veracode y renovación coordinada de tokens JWT entre pestañas activas del navegador para prevenir errores HTTP 401.
* **Escalabilidad en Cloud Run:** `web-event-prestadores` configurado con escalado fijo `minScale=15 / maxScale=15` y concurrencia de 600 solicitudes por instancia para absorber picos masivos de conexión SSE sin errores HTTP 429 (Too Many Requests).
* **Servidores de Videoconsulta Jitsi:** Clúster de servidores WebRTC migrado a infraestructura dedicada de CD2 en la región de San Pablo (Brasil) para reducir latencias a menos de 45ms.
"""
    },
    {
        "title": "Manual Técnico-Funcional CD2: Módulos Funcionales, Reglas de Negocio, SDT Tips Salud y DWH",
        "category": "Reglas de Negocio & Módulos CD2",
        "tags": "sdt, tips salud, snomed, russ, fhir, debounce, dwh, ips, alergias, nec-6618, nec-6836",
        "space_name": "Soporte N1/N2/N3",
        "content": """# Manual Técnico-Funcional CD2: Módulos Funcionales y Reglas de Negocio

## 1. Atención Clínica y Registro
* **Diagnóstico Obligatorio:** El campo de Diagnóstico codificado es estrictamente obligatorio para finalizar la consulta y emitir el cierre.
* **Evolución Opcional y RUSS:** La evolución clínica escrita es opcional. Si el profesional la deja en blanco, el backend genera automáticamente un texto genérico para RUSS:
  `"Turno Presencial"` o `"Turno Virtual"` + `Especialidad`.

## 2. Servidor Terminológico (SDT / Tips Salud - NEC-6618)
* **Búsqueda Sincrónica con Debounce:** Consulta en tiempo real mediante `POST /os-terminologiaclinica/v2/textos-codificados/terminos-sugeridos` aplicando mecanismo de debounce para proteger el servidor de sobrecarga.
* **Catálogos por Sección:**
  * `IdDominio: 128` (Procedimientos para todas las secciones).
  * `IdCatalogo: 30` (Laboratorios OSDE).
  * `IdCatalogo: 31` (Imágenes y Diagnóstico por Imágenes).
  * `IdCatalogo: 29` (Prácticas prescribibles ambulatorias).
* **Priorización y Mapeo FHIR:** Los resultados se ordenan por `EsTerminoValido: true`, `EsPreferido: true` y sinónimos. Mapeo directo a base de datos bajo estándar FHIR:
  `code.coding.code` (Código canónico SNOMED CT) y `code.coding.display` (Descripción legible).
* **Contingencia y Caché Local:** Ante errores HTTP 422, 500, timeouts o caídas de red, el sistema captura la excepción (`try-catch`) y conmuta de forma transparente la búsqueda a la base de datos local de CD2. Al seleccionar un término de Tips Salud, un Background Job asíncrono lo inserta en la BD local.
* **Términos Sensibles:** Si `EsSensible == true`, se aplica marcado especial en la interfaz de usuario y ofuscación de datos en la impresión del PDF para resguardo de secreto médico.

## 3. Información del Paciente (IPS) y Alergias
* Sección integrada dentro de la atención clínica con trazabilidad por Identificador Comercial/Persona (IC) para mantener el historial unificado e inmutable del socio.

## 4. Data Warehouse 1.2 (NEC-6836 / NEC-6838)
* **Desacople de Institución:** Desacople del nodo `institution` fuera de `appointment` en recetas, indicaciones y evoluciones para exponer contrato y filial en atenciones modulares (fuera de consulta programada).
* **Vista de Prestadores y Atenciones:** Exposición completa de especialidades con flags `prescription` y `psicopatology`. Vista consolidada de Atenciones que unifica consultas con turno y atenciones modulares consumida vía GET con parámetros `fechaDesde` / `fechaHasta` en formato ISO 8601 UTC (`YYYY-MM-DDTHH:mm:ss.000Z`).
"""
    },
    {
        "title": "SOP Operaciones CD2: Procedimientos de Base de Datos MongoDB y GCP",
        "category": "Operaciones & Base de Datos CD2",
        "tags": "mongodb, sop, operaciones, gcp, script, baja prestador, baja consultorio, turnos futuros, prefijos",
        "space_name": "DBA & Soporte N3",
        "content": """# SOP Operaciones CD2: Procedimientos de Base de Datos (MongoDB & GCP)

Guía pericial con las queries y comandos autorizados para ejecución por parte de Administradores de Base de Datos y Soporte N3.

---

## 1. Inhabilitación Total de Acceso a Prestador (Baja Total)
Para suspender o inhabilitar a un prestador de forma definitiva impidiendo cualquier inicio de sesión:
* Se modifica el campo `icPractitioner` agregando el prefijo `1000` al IC original del usuario:
```javascript
// Actualización individual
db.users.updateOne(
  { icPractitioner: "200XXXXXXX" },
  { $set: { icPractitioner: "1000200XXXXXXX" } }
);

// O mediante ejecución masiva por lote (bulkWrite)
```

---

## 2. Baja Lógica de Consultorio (Inhabilitación de Institución)
Para dar de baja una sede o consultorio preservando la integridad histórica de atenciones pasadas:
* Se aplica una baja lógica (`isDeleted: true`) utilizando el `ObjectId` de la institución:
```javascript
db.institutions.updateOne(
  { _id: ObjectId("64a1b2c3d4e5f6a7b8c9d0e1") },
  { $set: { isDeleted: true } }
);
```
> **Nota de Seguridad:** Nunca ejecutar `db.institutions.deleteOne()` ni remover registros físicamente.

---

## 3. Actualización de Prefijos Académicos (Dr. / Lic.) en Turnos Futuros
* **Causa:** El prefijo profesional se persiste de forma estática al generarse el primer turno.
* **Procedimiento:** Cuando un profesional actualiza su título en Cartilla Médica y cuenta con más de 200 turnos agendados hacia adelante:
  1. Actualizar el prefijo en la colección de prestadores en la BD de CD2.
  2. Ejecutar el script batch sobre la colección de turnos en MongoDB **fuera de horario operativo (ventana de mantenimiento nocturna)** para actualizar los identificadores sin bloquear la atención.
"""
    },
    {
        "title": "Guía de Soporte CD2: Matrículas SISA/CRM, Videoconsulta Jitsi, SNOMED CT y Registración Regional",
        "category": "Soporte Técnico CD2",
        "tags": "soporte, resolucion, matriculas, sisa, crm, jitsi, jointimeout, snomed, filial, region",
        "space_name": "Soporte N1/N2",
        "content": """# Guía de Soporte CD2: Diagnóstico y Resolución de Casos Críticos

## 1. Gestión y Selección de Matrículas (SISA / CRM)
* **Incidencia:** Selector de matrícula bloqueado en la interfaz cuando la matrícula por defecto del médico está inhabilitada pero cuenta con otra habilitada en su arreglo. Duplicación de ICs en CRM por cambios de CUIT extranjero (con matrículas ficticias con 0 o 1).
* **Solución de Soporte:**
  * El frontend compara la matrícula por defecto con la habilitada; si son distintas, desbloquea automáticamente el menú desplegable (select).
  * Para errores de CRM, gestionar la unificación de ICs mediante ticket PAU derivado a Soporte CRM.
  * Como contingencia urgente en BD, replicar todo el objeto `matrículaSISA` dentro de `defaultMatricula`.

## 2. Videoconsulta, Sala de Espera y Conectividad (Jitsi)
* **Incidencia:** Bucle de carga/spinner eterno (`joinTimeout`), falta de visualización de la propia miniatura (`self-view`) o cortes de reconexión.
* **Solución de Soporte:**
  * Sistema de reconexión automática con tope de 5 reintentos a intervalos de 20 segundos.
  * Pre-check de permisos: verificar que Cámara y Micrófono estén en 'Permitir' en el navegador.
  * En casos recurrentes (14+ reintentos), auditar logs en el Load Balancer filtrando por ID de sala, hash del turno y User-Agent.

## 3. Prescripción de Laboratorios y Búsqueda (SNOMED CT)
* **Incidencia:** Médicos no encuentran estudios por nombres cotidianos o coloquiales.
* **Solución de Soporte:**
  * Se han incorporado descripciones cotidianas entre paréntesis (ej. `hepatograma`, `(HIV)`).
  * Instruir al profesional a buscar ingresando las primeras 4 letras de la práctica.
  * Ante errores HTTP 422/500 de Tips Salud, actúa el fallback automático a la base de datos local.

## 4. Medios de Registración y Configuración de Consultorio (CRM / Regiones)
* **Incidencia:** Botón 'Registrar Prestación' bloqueado o ausencia de Operador y Terminal.
* **Solución de Soporte:**
  * Exigir coincidencia exacta del 100% en Efector, Filial, Región y Estado entre CRM y CD2.
  * Corregir la discrepancia geográfica (ej. residencia en Mar del Plata Región 22 vs. atención en Bariloche Región 17) tramitando el alta de la región correspondiente en CRM.
"""
    },
    {
        "title": "Guía de Soporte CD2: Descarga de PDFs (consultorio-cifrado), Receta Digital y Cierre de Atención",
        "category": "Soporte Técnico CD2",
        "tags": "pdf, 404, 400, consultorio-cifrado, gcs, mi argentina, receta digital, cierre, diagnostico",
        "space_name": "Soporte N1/N2",
        "content": """# Guía de Soporte CD2: Descarga de Documentos, Recetas y Cierre

## 1. Descarga y Cifrado de Documentos / PDFs (`consultorio-cifrado`)
* **Error 404 en enlace de receta/certificado:**
  * **Causa:** El archivo PDF fue depurado automáticamente por la política de retención límite de 6 meses de Google Cloud Storage (GCS). **Es un comportamiento normal del ciclo de vida del dato por vencimiento legal, no una falla del sistema.**
  * **Acción de Soporte:** Explicar al afiliado/médico que la prescripción ha caducado y debe emitirse una nueva consulta/receta.
* **Error 400 en enlace de receta/certificado:**
  * **Causa:** El usuario copió y pegó manualmente la URL en el navegador truncando o cortando caracteres de la firma hash.
  * **Acción de Soporte:** Indicar al usuario que haga clic directo sobre el botón o enlace original del correo electrónico, sin copiar y pegar la dirección.

## 2. Repositorio de Medicamentos y Receta Electrónica
* **Incidencia:** Rechazo en bloque de recetas o falta de visualización en la app Mi Argentina.
* **Solución de Soporte:**
  * El backend envía el código numérico de jurisdicción en lugar del texto descriptivo.
  * Verificar en logs si el error es de formato de datos del paciente o falla de servicio HTTP 500-599 de los padrones nacionales.

## 3. Validaciones de Formulario y Cierre de Atención
* **Incidencia:** Imposibilidad de finalizar consulta o bloqueo en certificados médicos al ingresar '0'.
* **Solución de Soporte:**
  * El Diagnóstico codificado es mandatorio; la evolución escrita es opcional (el backend autogenera el texto para RUSS).
  * En certificados médicos, el valor '0' está habilitado para días/horas cuando no corresponda a reposo laboral.
"""
    },
    {
        "title": "Manual de Ingeniería CD2: Ciclo de Releases, Promoción de Ambientes, Terraform y Observabilidad",
        "category": "DevOps & SRE CD2",
        "tags": "releases, ambientes, desa, test, uat, prod, terraform, hot deploy, apm, cloud logging, sse",
        "space_name": "DevOps & SRE",
        "content": """# Manual de Ingeniería CD2: Ciclo de Releases y Operaciones Cloud

## 1. Ciclo de Releases y Sprints
* Entregas continuas planificadas mediante releases quincenales o mensuales sincronizadas con la hoja de ruta de producto.

## 2. Promoción Estricta de Ambientes
* Flujo mandatorio de código:
  `Desarrollo (DESA)` $\\rightarrow$ `Testing (TEST)` $\\rightarrow$ `Certificación / UAT` $\\rightarrow$ `Producción (PROD)`.
* Ningún cambio llega a Producción sin validación de QA y certificación funcional en UAT.

## 3. Despliegues e Infraestructura como Código
* Infraestructura en GCP aprovisionada y mantenida exclusivamente a través de scripts declarativos de Terraform.
* Los despliegues urgentes (Hot Deploy) o parches de seguridad requieren ejecución obligatoria de pruebas de humo (smoke tests) previas a la publicación.

## 4. Observabilidad y Telemetría
* Monitoreo proactivo 24/7 mediante métricas de rendimiento de aplicaciones (APM).
* Alertas automatizadas en Google Cloud Logging para excepciones HTTP 5xx.
* Tableros en tiempo real para supervisar la concurrencia de conexiones SSE en `web-event-prestadores`.
"""
    }
]

inserted = 0
updated = 0
for art in articles:
    cursor.execute("SELECT id FROM kb_articles WHERE title = ?", (art["title"],))
    row = cursor.fetchone()
    if row:
        cursor.execute("""
            UPDATE kb_articles
            SET category = ?, tags = ?, space_name = ?, content = ?, updated_at = ?
            WHERE id = ?
        """, (art["category"], art["tags"], art["space_name"], art["content"], now, row[0]))
        updated += 1
    else:
        cursor.execute("""
            INSERT INTO kb_articles (
                title, category, content, author_username, tags, version,
                changelog, view_count, requests_deflected, helpful_score,
                space_name, is_published, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art["title"], art["category"], art["content"], "admin", art["tags"],
            "v2.0", "Homologación pericial completa CD2 y Matriz Interoperabilidad",
            0, 0, 99, art["space_name"], 1, now, now
        ))
        inserted += 1

conn.commit()
conn.close()

print(f"Resultado KB CD2: {inserted} insertados, {updated} actualizados.")
