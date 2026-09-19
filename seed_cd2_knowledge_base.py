# -*- coding: utf-8 -*-
"""
Script de Ingesta Pericial de Base de Conocimiento para Consultorio Digital 2 (CD2)
y Matriz Maestra de Interoperabilidad (SAP, CRM, IAM, Turnos, Cartilla, PAU).
Diseñado para alimentar el Motor de Análisis Cognitivo N3 y la Base de Conocimiento ITSM.
"""

from datetime import datetime
from sqlmodel import Session, select
from backend.app.db.session import engine, init_db
from backend.app.models.entities import KBArticle, KBArticleHistory

CD2_ARTICLES = [
    {
        "title": "Gestión y Selección de Matrículas (SISA / CRM): Desbloqueo de Selector y Contingencias",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "matricula, sisa, crm, selector bloqueado, ic duplicado, prescripcion, consultorio digital",
        "version": "v2.0",
        "changelog": "Lógica de comparación automática frontend y procedimiento de réplica en BD",
        "helpful_score": 98,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Selector de matrícula bloqueado en la interfaz:** Ocurre cuando un profesional tiene su matrícula por defecto inhabilitada pero cuenta con otra matrícula habilitada activa (por ejemplo, con diferente especialidad o jurisdicción). El sistema detectaba una sola matrícula activa y bloqueaba el menú desplegable, impidiéndole seleccionarla manualmente para prescribir.
- **Inconsistencias y datos ficticios desde CRM / SISA:** Médicos que figuran sin matrículas en la plataforma porque en CRM sus matrículas reales de SISA quedaron asociadas a un Identificador Comercial (IC) antiguo (por ejemplo, registrado con CUIT extranjero), provocando que en la nueva postulación se hayan cargado matrículas con caracteres ficticios (como un 0 adelante o un 1 al final) para saltear el bloqueo de duplicados.
- **Inercia operativa:** Reclamos por "matrícula inválida" donde el médico intenta prescribir con la inercia de la versión anterior, desconociendo cómo cambiar manualmente su matrícula activa configurada por defecto desde la interfaz.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Desbloqueo del Selector en Frontend:** Se implementó una lógica donde el sistema compara la matrícula por defecto con la matrícula habilitada disponible; si la matrícula habilitada es distinta a la de por defecto, el selector (`<select>`) se desbloquea automáticamente para permitirle al médico elegir la activa y prescribir.
2. **Matrículas Ficticias / Duplicación de ICs:** Cuando CRM genera registros duplicados por cambios de CUIT (nacional vs. extranjero) o errores ortográficos en el apellido, solicitar la unificación de ICs mediante un ticket PAU a Soporte CRM / MDA (ej. PAU #895833) para restablecer las matrículas reales de SISA.
3. **Contingencia por Base de Datos:** Para destrabar bloqueos urgentes en producción, el analista N3 ejecuta una query en la BD de CD2 que replica de forma exacta todos los campos del objeto `matriculaSISA` dentro de `defaultMatricula`.
4. **Estado de Habilitación:** El sistema considera exclusivamente el estado 'Habilitada' para permitir la emisión de recetas, independientemente de la fecha de vencimiento informada."""
    },
    {
        "title": "Videoconsulta, Sala de Espera y Conectividad (Jitsi): joinTimeout, Permisos y Self-View",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "videoconsulta, jitsi, webrtc, jointimeout, spinner, self-view, permisos, camara, microfono",
        "version": "v2.1",
        "changelog": "Algoritmo de reconexión transparente (5 reintentos de 20s) y pre-check de hardware",
        "helpful_score": 97,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Bucle de carga o tiempo de espera agotado (joinTimeout / Spinner eterno):** Dificultades o demoras para establecer la conexión con la sala de llamada por microcortes de red, suspensiones de pantalla en dispositivos móviles o demoras en la respuesta del servidor WebRTC.
- **Visualización de video y permisos de dispositivos:** Reportes donde el prestador no lograba visualizar su propia imagen en miniatura (*self-view*) dentro del cuadro de video de la llamada, o bloqueos provocados por falta de habilitación de permisos de cámara y micrófono en el navegador.
- **Cierre accidental de la sesión:** Inconveniente donde el médico, al intentar cerrar o minimizar la ventana de la videoconsulta, desconecta o expulsa involuntariamente al paciente de la atención.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Reconexión y Bucle (joinTimeout):** El sistema ejecuta un proceso de reconexión automática transparente en segundo plano. Para evitar bucles infinitos, se limita a 5 reintentos con intervalos de 20 segundos. Si la falla persiste, la IA o el operador N1 debe indicar al usuario refrescar la pantalla (`F5`) o volver a la sala de espera.
2. **Vista Previa de Cámara (Self-view) y Permisos:** Guiar al médico a habilitar permisos en el candado del navegador (`chrome://settings/content/camera`). Verificar en el iframe de Jitsi que la propiedad `disableSelfView` se encuentre en `false`.
3. **Cierre Accidental:** Se implementó un modal de confirmación obligatoria previa al cierre de la pestaña (`window.onbeforeunload`) para prevenir desconexiones no deseadas del paciente."""
    },
    {
        "title": "Prescripción de Laboratorios y Búsqueda de Estudios (SNOMED CT): Mapeo de Términos Coloquiales",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "laboratorios, snomed ct, prescripcion, estudios, hepatograma, hiv, hemograma, terminologia",
        "version": "v1.9",
        "changelog": "Catálogo de sinónimos clínicos enriquecidos y términos cotidianos",
        "helpful_score": 96,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Dificultad en la búsqueda por términos coloquiales:** Al implementar el nomenclador estricto SNOMED CT para laboratorios, los profesionales no encontraban determinaciones habituales en el buscador por su nombre cotidiano o tradicional (por ejemplo, "hepatograma", "HIV", "orina completa", "perfil lipídico"). Esto generaba dudas sobre la presencia del estudio y rechazos de las órdenes en efectores externos.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Inclusión de Términos Coloquiales:** Se actualizaron las descripciones del catálogo local incorporando términos comunes o aclaraciones entre paréntesis (ej. 'hepatograma' -> 'Prueba de función hepática (hepatograma)', 'HIV' -> 'Detección de anticuerpos contra virus de inmunodeficiencia humana (HIV)').
2. **Procedimiento de Asistencia:**
   - Si el médico no localiza el estudio, indicarle que tipee las primeras 4 letras de la práctica médica principal.
   - En caso de requerir un estudio no indexado, el analista funcional N3 registra el término en la cola de homologación semántica para incorporarlo en la siguiente release."""
    },
    {
        "title": "Medios de Registración y Configuración de Consultorio: Conciliación de Región CRM y Terminal",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "medios de registracion, registrar prestacion, crm, terminal, operador, region, contrato",
        "version": "v1.5",
        "changelog": "Validación automática de coherencia de sede y contrato",
        "helpful_score": 95,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Botón 'Registrar Prestación' bloqueado / Falta de Operador y Terminal:** Discrepancia en los registros de CRM entre la región donde el médico atiende efectivamente y la región asignada en su contrato (por ejemplo, atención en Mar del Plata versus residencia en Bariloche, o falta de alta de la región correspondiente). Esta incoherencia impide que el sistema recupere los medios de registración requeridos para validar y facturar la consulta.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Verificación de Datos en CRM:** Comprobar que el médico tenga cargada la terminal y el operador correctos en su perfil de prestador en CRM. El sistema los actualiza cada vez que se genera un turno o cuando el médico inicia sesión.
2. **Acción de Contingencia N2/N3:**
   - Comprobar si existe solicitud de cambio de sede en trámite.
   - Si la terminal figura vacía, generar solicitud formal a Operaciones CRM solicitando la vinculación de la terminal activa para la circunscripción contractual."""
    },
    {
        "title": "Descarga y Apertura de Documentos y PDFs Cifrados: Diagnóstico de Errores 404 y 400",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "pdf, descarga, error 404, error 400, hash trunco, retencion bucket, receta pdf",
        "version": "v2.0",
        "changelog": "Regeneración segura de enlaces y política de retención de 6 meses",
        "helpful_score": 99,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Error 404 (Documento no encontrado / Vencido):** Consultas de socios o prestadores al hacer clic en enlaces de correos electrónicos antiguos. Ocurre porque los archivos PDF guardados en el bucket tienen una política de retención máxima de 6 meses y, transcurrido ese tiempo, son eliminados automáticamente por ciclo de vida de almacenamiento.
- **Error 400 (Enlace / Hash incompleto):** Errores producidos cuando el usuario copia y pega manualmente la URL de la receta o certificado en el navegador cortando o truncando la cadena del hash criptográfico.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Resolución ante Error 404 (> 6 meses):**
   - El documento no puede recuperarse del bucket expirado.
   - Indicar al socio o médico ingresar a su Portal de Historial Clínico para regenerar la orden digital o solicitar una nueva prescripción al profesional tratante.
2. **Resolución ante Error 400 (Hash trunco):**
   - Indicar al usuario que no copie la URL como texto sino que haga clic directamente sobre el botón del correo electrónico, o regenerar el enlace firmado desde el panel de soporte enviándolo a la casilla principal verificada."""
    },
    {
        "title": "Repositorio de Medicamentos y Receta Electrónica: Fallas de Validación y Comunicación 500",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "receta electronica, repositorio medicamentos, error 500, validacion afiliado, rechazo",
        "version": "v2.2",
        "changelog": "Manejo de reintentos exponenciales y validación estricta de padrón",
        "helpful_score": 97,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Rechazo en bloque de recetas:** Incidencias donde el Repositorio de Medicamentos rechaza la validación de la receta debido a inconsistencias o faltantes en los datos del paciente (por ejemplo, número de credencial vencida, plan no homologado o falta de diagnóstico CIE-10) o por fallas temporales de comunicación HTTP 500 del servicio central de recetas.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Validación de Datos del Socio:** Verificar que el número de afiliado y plan estén debidamente sincronizados con el Caché de Socios SAP. Si el plan no tiene cobertura para la molécula prescrita, el repositorio emitirá rechazo formal.
2. **Falla de Comunicación HTTP 500:**
   - La plataforma retiene la receta en cola local con estado `PENDIENTE_VALIDACION`.
   - Se ejecutan 3 reintentos automáticos espaciados. Si la falla del repositorio externo es generalizada, N3 activa el protocolo de contingencia de receta con firma diferida."""
    },
    {
        "title": "Actualización de Datos y Prefijos Profesionales (Dr. / Lic.) en Turnos Futuros y Cartilla",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "prefijo, dr, lic, turnos futuros, cartilla, crm, notificaciones, contratos",
        "version": "v1.7",
        "changelog": "Lógica de actualización de prefijo sin valores residuales por defecto",
        "helpful_score": 94,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Inconsistencia en el prefijo profesional (Dr. / Lic.):** Al corregir o actualizar el título académico/prefijo de un prestador en el sistema, los turnos futuros ya agendados continúan enviando las notificaciones con el prefijo anterior, debido a que el dato queda grabado de forma fija al crearse el primer turno en la tabla de turnos.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Gobernanza del Prefijo:**
   - En **Cartilla Médica**: es administrado por el equipo interno de Cartilla (Ana Laura).
   - En **CRM**: se define y valida desde el módulo de Contratos.
2. **Comportamiento del Sistema:** Se contempló cuándo el campo está vacío para que no tenga valores por defecto que impidan la asignación de Lic. o Dr.
3. **Turnos ya Emitidos:** Las notificaciones de turnos previamente agendados conservan el prefijo con el que fueron sellados en el JSON original; las nuevas reservas tomarán el prefijo actualizado automáticamente."""
    },
    {
        "title": "Validaciones de Formularios y Cierre de Atención: Diagnóstico Obligatorio y Certificados",
        "category": "Consultorio Digital 2 (CD2)",
        "tags": "cierre de atencion, diagnostico obligatorio, certificados, valor cero, formulario, finalizacion",
        "version": "v1.8",
        "changelog": "Validación preventiva en frontend de campos mandatorios y rangos",
        "helpful_score": 96,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Diagnóstico Pericial y Casuística
- **Bloqueo de cierre de atención por Diagnóstico:** Imposibilidad de finalizar la consulta si el profesional no ha seleccionado explícitamente un Diagnóstico obligatorio codificado (incluso si completó el campo opcional de Evolución Médica).
- **Carga de cero (0) en certificados:** Fallas de validación en el formulario al ingresar el valor '0' en campos de días u horas de certificados que no corresponden a indicación de reposo asistencial.

### 2. Procedimiento de Resolución Estandarizado (SOP)
1. **Cierre de Atención:** Recordar al profesional que el campo `Diagnóstico Principal` es un requisito médico-legal mandatorio. Debe buscar la patología en el selector SNOMED/CIE-10 para habilitar el botón `Finalizar Atención`.
2. **Certificados Médicos:** En certificados que no conllevan días de reposo (ej. aptitud física o constancia de asistencia), dejar el campo de días vacío en lugar de digitar '0', o marcar la casilla 'Sin días de reposo'."""
    },
    {
        "title": "Matriz Maestra de Interoperabilidad y Ciclo de Vida del Dato: SAP, CRM, IAM, Turnos, Cartilla y PAU",
        "category": "Interoperabilidad & Sincronización",
        "tags": "sap, crm, iam, turnos, cartilla, pau, matriz de datos, sincronizacion, origen del dato",
        "version": "v2.5",
        "changelog": "Matriz consolidada de fuentes maestras, eventos de actualización y circuitos de escalamiento",
        "helpful_score": 100,
        "author_username": "admin",
        "space_name": "Guías Periciales N3",
        "content": """### 1. Matriz Integral de Orígenes del Dato y Reglas de Sincronización

| Dato / Entidad | Origen del Dato | Cuándo se Actualiza / Regla Operativa | Circuito de Derivación / Contingencia |
|---|---|---|---|
| **Nombre y Apellido del Socio** | Caché de Socios (SAP) / Servicio de Socios | SAP notifica novedades automáticas. Se verifica cada vez que se genera un turno. | Sincronización transparente con SAP al solicitar turnos. |
| **N° Socio OSDE, DNI, Plan, Género** | Caché de Socios (SAP) / Servicio de Socios | SAP notifica novedades. Se actualiza con la recarga de turnos al prestador. | Consulta automatizada al bus de socios. |
| **Fecha de Nacimiento del Socio** | Frontend / Turnos / SAP | Al solicitar turnos del prestador se dispara la reconciliación con el caché local frente a SAP. | Inmutable tras validación con padrón. |
| **Email y Teléfono del Paciente** | Turnos / Creación de Paciente | Se crea automáticamente con el primer turno. En turnos posteriores se usa el mail y teléfono cargados en ese turno específico. | Notificaciones y recordatorios se envían a los datos configurados en ese nuevo turno específico. |
| **Identificador Comercial (IC OSDE)** | CRM / Base CD | No se modifica de forma estándar. | Validar IC de login, consultar con Ezequiel Cupito y actualizar en base CD. |
| **CUIT (AFIP) del Prestador** | AFIP / Gestión Interna | Actualización manual administrativa. | Gestión formal de padrón de prestadores. |
| **Dirección y Teléfono del Prestador** | Base de Datos CD | Actualización manual controlada. | Solicitar ticket PAU, armar y validar query SQL para ejecución en BD. |
| **Email del Prestador (Mensajería)** | Turnos / Extranet / Cartilla | No se actualiza automáticamente; toma el mail del JSON. El prestador lo modifica en Extranet. | Se envía notificación a 1 sola casilla: la configurada como principal en Cartilla Médica. |
| **Prefijo Profesional (Dr. / Lic.)** | Cartilla Médica / CRM Contratos | Se contempla cuándo está vacío para evitar valores por defecto que impidan el título. | No depende del turno; se actualiza en Cartilla Médica (Ana Laura) o CRM Contratos. |
| **Terminal y Operador del Prestador** | CRM | Cada vez que se genera un turno o cuando el médico ingresa a la plataforma. | Actualización automática de sesión. |
| **Nombre en Web CD2 vs Videoconsulta** | Web: IAM / Videoconsulta: Turnos | Web: Se envía a IAM para corrección. Videoconsulta: Se actualiza en CRM. | Para Web: derivar a MDA-Aplicaciones N1 solicitando pase a IAM con el dato exacto. |
| **Baja de Consultorio** | Base de Datos CD | Acción administrativa manual. | Aplicación de bandera lógica `isDeleted = true`. |"""
    }
]

def seed_cd2_kb():
    init_db()
    with Session(engine) as session:
        created_count = 0
        updated_count = 0
        for art_data in CD2_ARTICLES:
            existing = session.exec(select(KBArticle).where(KBArticle.title == art_data["title"])).first()
            if not existing:
                article = KBArticle(**art_data)
                session.add(article)
                session.commit()
                session.refresh(article)
                
                # Historial inicial
                hist = KBArticleHistory(
                    article_id=article.id,
                    version=article.version,
                    title=article.title,
                    category=article.category,
                    content=article.content,
                    author_username=article.author_username,
                    tags=article.tags,
                    changelog=article.changelog or "Versión inicial homologada N3",
                    created_at=datetime.utcnow()
                )
                session.add(hist)
                session.commit()
                created_count += 1
            else:
                existing.content = art_data["content"]
                existing.category = art_data["category"]
                existing.tags = art_data["tags"]
                existing.version = art_data["version"]
                existing.changelog = art_data["changelog"]
                existing.helpful_score = art_data["helpful_score"]
                session.add(existing)
                session.commit()
                updated_count += 1
                
        print(f"CD2 KB Seeding complete! Created: {created_count}, Updated: {updated_count}")

if __name__ == "__main__":
    seed_cd2_kb()
