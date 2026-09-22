import sqlite3
import datetime

conn = sqlite3.connect('backend/healthdesk.db')
cursor = conn.cursor()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()

manual_articles = [
    {
        "title": "Manual CD2 - Parte 1: Arquitectura del Ecosistema y Microservicios",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "arquitectura, microservicios, cloud run, sse, mtls, jitsi, webrtc, jwt, veracode, gcs",
        "space_name": "Soporte N2/N3 & DevOps",
        "content": """# Manual CD2 - Parte 1: Arquitectura del Ecosistema y Microservicios

## 1.1 Componentes Principales de la Plataforma
* **consultorio-frontend:** Aplicación web principal utilizada por los profesionales de la salud para la atención clínica, emisión de recetas, indicaciones y ordenamiento de turnos.
* **consultorio-landing-socio:** Interfaz de acceso para los pacientes/socios desde donde ingresan a la videoconsulta y visualizan la información de su atención.
* **consultorio-api-core:** Núcleo backend encargado de la lógica de negocio clínica, orquestación de la sesión, gestión de turnos y reglas de dominio.
* **consultorio-backend-negocio:** Microservicio que procesa y ejecuta las validaciones complejas de elegibilidad, cobertura y prescripción clínica.
* **consultorio-mensajeria y consultorio-notif-sender:** Servicios encargados de la generación de documentos PDF (recetas, certificados, indicaciones), firma digital y envío de notificaciones multicanal vía correo electrónico y WhatsApp.
* **consultorio-cifrado:** Componente público desacoplado que desencripta las URL seguras enviadas a los pacientes y recupera los archivos PDF desde los buckets de almacenamiento en Google Cloud Storage (GCS).
* **web-event-prestadores:** Canal de mensajería en tiempo real implementado mediante Server-Sent Events (SSE) sobre Cloud Run, encargado de notificar al prestador el ingreso inmediato de pacientes a la sala de espera.
* **Capa de Caché (cache-prestadores y cache-socios):** Microservicios dedicados a la optimización de latencia y reducción de consultas repetitivas a las bases de datos principales.

## 1.2 Seguridad, Infraestructura y Monitoreo
* **Autenticación mTLS:** Comunicación encriptada punto a punto mediante certificados mTLS entre el validador externo Quercus y los servicios backend.
* **Seguridad de Código:** Escaneo continuo de vulnerabilidades mediante Veracode e implementación de refresco coordinado de tokens JWT entre pestañas del navegador para prevenir errores HTTP 401.
* **Servidor de Videoconsulta (Jitsi San Pablo):** Salas de videollamada alojadas en infraestructura propia desplegada en la región de San Pablo para reducir latencias respecto a servidores en EE. UU.
* **Capacidad SSE en Cloud Run:** El servicio web-event-prestadores se encuentra configurado en Terraform con `minScale=5 / maxScale=15` e instancias con concurrencia de hasta 600 solicitudes SSE en simultáneo para evitar bloqueos HTTP 429 por límite de conexiones sostenidas.
"""
    },
    {
        "title": "Manual CD2 - Parte 2: Módulos Funcionales y Reglas de Negocio Clínicas",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "reglas de negocio, diagnostico, russ, tips salud, sdt, snomed, fhir, debounce, ips, alergias, dwh",
        "space_name": "Soporte N1/N2/N3",
        "content": """# Manual CD2 - Parte 2: Módulos Funcionales y Reglas de Negocio Clínicas

## 2.1 Atención Clínica y Reglas RUSS
* **Diagnóstico Obligatorio:** El registro del diagnóstico es un requisito obligatorio e infranqueable para finalizar cualquier atención presencial o virtual.
* **Evolución Clínica Opcional:** La carga de comentarios en la evolución es opcional. Si el profesional deja la evolución en blanco, el backend de CD2 genera automáticamente un texto formateado para la historia clínica centralizada de RUSS con la estructura: `"Turno Presencial"` o `"Turno Virtual"` + `Especialidad`.

## 2.2 Servidor Terminológico / Tips Salud (NEC-6618)
* **Consultas Sincrónicas:** Búsquedas en tiempo real contra el servicio centralizado mediante el endpoint `POST /os-terminologiaclinica/v2/textos-codificados/terminos-sugeridos` aplicando un mecanismo de debounce en frontend para evitar la saturación de peticiones HTTP.
* **Ruteo de Catálogos por Sección:**
  * **Laboratorios:** `IdDominio: 128` (Procedimientos) e `IdCatalogo: 30` (Laboratorio OSDE).
  * **Imágenes:** `IdDominio: 128` e `IdCatalogo: 31` (u otros catálogos específicos de imágenes).
  * **Prácticas:** `IdDominio: 128` e `IdCatalogo: 29` (Prescribibles OSDE generales).
* **Persistencia FHIR:** Mapeo estandarizado a base de datos donde `CodigoExterno` de SNOMED CT se almacena en `code.coding.code` y la `Descripcion` en `code.coding.display`.
* **Estrategia de Caché Local y Fallback try-catch:** Si la API externa no responde (HTTP 422, 500, timeout o corte de red), la aplicación captura la excepción y conmuta la búsqueda hacia el maestro local en la BD de CD2. Al seleccionar un término de Tips Salud, un Background Job verifica e inserta el código y la descripción en el caché local.
* **Términos Sensibles:** Cuando la propiedad del término es `EsSensible == true`, la interfaz aplica marcado especial y se ofuscan los datos clínicos en la impresión del PDF.

## 2.3 Información del Paciente en Atención (IPS) y Alergias
* Módulo integrado dentro de la ficha médica que mantiene la trazabilidad clínica utilizando el Identificador Comercial (IC) del paciente para preservar su historial unificado aunque cambie de grupo familiar o plan.

## 2.4 Registración Diferida y Anulaciones
* Funcionalidad operacional para registrar atenciones atendidas de forma diferida o anular registraciones erróneas causadas por caídas intermitentes en los validadores de los operadores externos (ITC, Activia, APG).

## 2.5 Data Warehouse 1.2 (NEC-6836 / NEC-6838)
* **Desacople de Institución:** Exposición del nodo `institution` (`_id`, `id`) por fuera del nodo `appointment` para capturar el contrato y la filial en atenciones modulares (emitidas fuera de consulta).
* **Vista Prestadores:** Inclusión de todas las especialidades declaradas con los flags `prescription` y `psicopatology`.
* **Vista Consolidada de Atenciones:** Estructura unificada expuesta mediante servicio GET con filtros `fechaDesde` / `fechaHasta` en formato estándar ISO 8601 UTC (`YYYY-MM-DDTHH:mm:ss.000Z`).
"""
    },
    {
        "title": "Manual CD2 - Parte 3: Guía de Operaciones y Procedimientos de Base de Datos (MongoDB / GCP)",
        "category": "Operaciones & Base de Datos CD2",
        "tags": "mongodb, scripts, operaciones, baja prestador, baja consultorio, prefijos, turnos futuros, pau",
        "space_name": "DBA & Soporte N3",
        "content": """# Manual CD2 - Parte 3: Guía de Operaciones y Base de Datos (MongoDB / GCP)

## 3.1 Inhabilitación Total de Acceso a Prestador (Baja Total por IC)
Para revocar en su totalidad el acceso de un profesional a la plataforma sin eliminar sus registros históricos, se añade el prefijo `1000` a su campo `icPractitioner` en la colección `users`:
```javascript
db.users.updateOne(
  { icPractitioner: "2003825668" },
  { $set: { icPractitioner: "10002003825668" } }
);
```

## 3.2 Baja Lógica de Consultorio / Institución
Para inhabilitar un consultorio específico de la cartilla del médico se modifica el flag `isDeleted` en la colección `institutions` utilizando el ID del consultorio:
```javascript
db.institutions.updateOne(
  { _id: ObjectId("687b421026c0c0ba5f55654e") },
  { $set: { isDeleted: true } }
);
```

## 3.3 Actualización de Prefijos Académicos (Dr. / Lic.) en Turnos Futuros
Como el prefijo profesional se graba de forma fija en la base de datos al crearse el primer turno, para actualizar cuentas con una gran cantidad de turnos agendados a futuro:
1. Se actualiza el prefijo profesional en la tabla de usuarios de CD2.
2. Se ejecuta un proceso batch sobre la colección `appointments` en MongoDB fuera de horario operativo actualizando los identificadores de los turnos programados.
"""
    },
    {
        "title": "Manual CD2 - Parte 4: Matriz Exhaustiva de Errores de Soporte y Soluciones Operativas",
        "category": "Soporte Técnico CD2",
        "tags": "errores frecuentes, matriz, matriculas, jitsi, snomed, crm, pdf 404, pdf 400, receta, certificados",
        "space_name": "Soporte N1/N2/N3",
        "content": """# Manual CD2 - Parte 4: Matriz Exhaustiva de Errores de Soporte y Soluciones Operativas

| Categoría | Problema / Mensaje de Error | Causa Raíz | Solución Técnica / Flujo de Acción (SOP) |
| :--- | :--- | :--- | :--- |
| **Matrículas** | Selector de matrícula congelado o bloqueado en la interfaz | La matrícula por defecto del médico está inhabilitada y el frontend detectaba una sola matrícula activa en el arreglo, bloqueando el desplegable. | **Fix en v3.9.0:** El frontend compara la matrícula por defecto con la habilitada; si son distintas, desbloquea automáticamente el select. |
| **Matrículas** | Médico figura sin matrículas habilitadas para prescribir | Duplicación de ICs en CRM por registros históricos con CUIT extranjero, cargando matrículas ficticias (con 0 o 1). | Tramitar la unificación de ICs en CRM mediante ticket PAU a MDA/CRM. Como contingencia urgente en BD, replicar el objeto `matrículaSISA` dentro de `defaultMatricula`. |
| **Videoconsulta** | Bucle de carga infinitamente colgado (`joinTimeout` / Spinner) | Microcortes de conexión a red o bloqueo de pantalla en dispositivos móviles. | Sistema de reconexión automática con tope de 5 reintentos cada 20 segundos. Si falla, solicitar reingresar desde la sala de espera o refrescar. |
| **Videoconsulta** | El médico no ve su propia imagen de cámara (`self-view`) | Atributo faltante en la propiedad de la etiqueta `iframe` del componente Jitsi. | Inclusión del atributo en el `iframe` de Jitsi para restaurar la miniatura de video. |
| **SNOMED CT** | Estudio de laboratorio no encontrado por nombre coloquial | Implementación estricta de nombres normados SNOMED que difieren del lenguaje cotidiano (ej. `"hepatograma"`). | Inclusión de términos coloquiales entre paréntesis en el catálogo local y fallback `try-catch` a BD local ante fallas del servidor terminológico. |
| **CRM / Regiones** | Botón `"Registrar Prestación"` bloqueado / Sin Operador ni Terminal | Discrepancia en CRM entre la región de atención física y la región de residencia contractual del médico. | Validar coincidencia 100% en Efector, Filial, Región y Estado entre CRM y CD2. Tramitar el alta de la región de atención correspondiente en CRM. |
| **Descarga PDFs** | Error 404 (Documento no encontrado / Not Found) | El socio hace clic en un enlace de correo antiguo cuyo archivo PDF fue purgado. | Informar que los archivos PDF en Google Cloud Storage tienen una política de retención fija de 6 meses por vencimiento legal. |
| **Descarga PDFs** | Error 400 (Bad Request / Solicitud Incorrecta) | El usuario copió o pegó la URL manualmente truncando o cortando la cadena del hash. | Indicar al usuario que vuelva a hacer clic directamente sobre el enlace original del correo electrónico. |
| **Receta Electrónica** | Rechazo de recetas por el Repositorio de Medicamentos | Envío del texto descriptivo de la jurisdicción en lugar del código numérico estandarizado. | Envío del código de jurisdicción hacia el repositorio y personalización de mensajes de error según categoría (datos de paciente vs. error 500). |
| **Formulario** | Imposibilidad de finalizar consulta o error en certificados | Intentar cerrar la consulta sin diagnóstico o ingresar el valor `'0'` en campos de certificados sin reposo. | El diagnóstico es obligatorio. Si no hay evolución, se autogenera el texto para RUSS. Se ajustaron las reglas en certificados para admitir el valor 0 cuando no implica reposo laboral. |
"""
    },
    {
        "title": "Manual CD2 - Parte 5: Metodología y Flujos del Equipo de Desarrollo",
        "category": "DevOps & SRE CD2",
        "tags": "desarrollo, metodología, ambientes, desa, test, uat, prod, releases, hot deploy, apm, logging",
        "space_name": "DevOps & SRE",
        "content": """# Manual CD2 - Parte 5: Metodología y Flujos del Equipo de Desarrollo

## 5.1 Promoción de Entornos
Flujo de despliegues secuencial estricto:
`Desarrollo (DESA)` $\\rightarrow$ `Testing (TEST)` $\\rightarrow$ `Certificación / UAT` $\\rightarrow$ `Producción (PROD)`.

## 5.2 Ciclo de Releases y Sprints
Entregas planificadas en hojas de ruta con salidas a producción quincenales o mensuales.

## 5.3 Despliegues Hotfix / Hot Deploy
Parches de emergencia aprobados mediante tickets de implementación y validados con pruebas de humo antes de la publicación productiva.

## 5.4 Observabilidad y Alertas
Monitoreo proactivo a través de métricas de APM, alertas en GCP Cloud Logging y dashboards de concurrencia SSE.
"""
    }
]

for art in manual_articles:
    cursor.execute("SELECT id FROM kb_articles WHERE title = ?", (art["title"],))
    row = cursor.fetchone()
    if row:
        cursor.execute("""
            UPDATE kb_articles
            SET category = ?, tags = ?, space_name = ?, content = ?, updated_at = ?
            WHERE id = ?
        """, (art["category"], art["tags"], art["space_name"], art["content"], now, row[0]))
    else:
        cursor.execute("""
            INSERT INTO kb_articles (
                title, category, content, author_username, tags, version,
                changelog, view_count, requests_deflected, helpful_score,
                space_name, is_published, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            art["title"], art["category"], art["content"], "admin", art["tags"],
            "v2.0", "Carga oficial Manual de Entrenamiento CD2 Partes 1 a 5",
            0, 0, 99, art["space_name"], 1, now, now
        ))

conn.commit()
cursor.execute("SELECT COUNT(*) FROM kb_articles")
total = cursor.fetchone()[0]
conn.close()
print(f"Cargadas las 5 partes del Manual CD2. Total articulos en KB: {total}")
