from datetime import datetime
from sqlmodel import Session, select
from app.db.session import engine, init_db
from app.models.entities import (
    User, UserRole, Platform, Institution, Ticket,
    TicketStatus, TicketType, ImpactLevel, UrgencyLevel,
    PriorityLevel, SupportLevel, TicketComment, TicketAuditLog,
    KBArticle, KBArticleHistory
)

def seed_kb_articles(session: Session):
    existing_kb = session.exec(select(KBArticle)).first()
    if existing_kb:
        print("KB Articles already seeded.")
        return

    print("Seeding Knowledge Base (Base de Conocimiento) Articles...")
    articles = [
        # --- 1. RECETA DIGITAL ---
        KBArticle(
            title="Protocolo de Contingencia: Firma Digital Remota PKI en Receta Electrónica",
            category="Receta Digital",
            tags="receta, firma digital, pki, token, dispensa, farmacia, anmat",
            version="v2.1",
            changelog="Actualización de certificados raíz ANMAT y soporte HSM en la nube",
            view_count=142,
            source_ticket_id="TICK-202608-0001",
            author_username="admin",
            content="""### 1. Diagnóstico del Problema
Cuando el servicio de firma digital PKI responde con error `ERR_PKI_CERT_EXPIRED` o `ERR_HSM_TIMEOUT`, las recetas emitidas quedan en estado 'Borrador Sin Firma' y no pueden ser dispensadas en la red de farmacias.

### 2. Procedimiento de Resolución Técnica
1. **Verificación del Servicio HSM:** Ejecutar en la consola de administración el comando de diagnóstico `curl -k https://pki.quantux.salud.ar/health/ready`.
2. **Conmutación por Falla (Failover):** Si el cluster principal presenta latencia > 1500ms, habilitar el HSM secundario en `Configuración > Integraciones PKI > Modo Respaldo`.
3. **Renovación de Certificados:** Cargar el nuevo paquete de Autoridad Certificante Raíz (.p12) validado por ANMAT / Ley 25.506.
4. **Firma Masiva de Pendientes:** Seleccionar las recetas en cola y presionar 'Firmar y Despachar Lote'. Se enviará el token criptográfico al correo del paciente y la receta quedará validada con código QR inmutable."""
        ),
        KBArticle(
            title="Resolución de Rechazos de Dispensa en Red Farmacéutica FACAF / COFA",
            category="Receta Digital",
            tags="dispensa, validacion, vademecum, codigos troquel, trazabilidad, cefa",
            version="v1.4",
            changelog="Integración de nuevos códigos GTIN/Troquel para medicamentos de alto costo",
            view_count=89,
            source_ticket_id="TICK-202608-0002",
            author_username="soporte",
            content="""### 1. Causa Frecuente
El 90% de los rechazos en punto de farmacia se originan en discrepancias entre el código de troquel prescripto y el catálogo actualizado del financiador (OSDE, Swiss Medical, Galeno, PAMI).

### 2. Pasos de Normalización
1. **Verificación de Cobertura:** Comprobar que el principio activo (DCI) esté homologado en el Vademécum Unificado Nacional.
2. **Resincronización de Catálogo:** Ir a `Plataformas > Receta Electrónica > Sincronizar Vademécum COFA`.
3. **Emisión de Duplicado Rectificado:** Si la receta fue rechazada físicamente, anular la orden previa ingresando el motivo 'Discrepancia de Presentación' y generar una nueva orden con el GTIN comercial homologado."""
        ),

        # --- 2. TELEMEDICINA ---
        KBArticle(
            title="Optimización WebRTC y Manejo de Baja Conectividad en Videoconsultas",
            category="Telemedicina",
            tags="webrtc, video, audio, coturn, stun, turn, ancho de banda, 4g",
            version="v2.0",
            changelog="Incorporación de codecs adaptativos VP9/Opus y fallback automático a TURN TCP:443",
            view_count=215,
            source_ticket_id="TICK-202608-0003",
            author_username="dnavarro",
            content="""### 1. Escenario Clínico
En zonas con conectividad intermitente (latencia > 250ms o pérdida de paquetes > 5%), la sesión WebRTC puede experimentar congelamiento de video o pérdida de audio bidireccional.

### 2. Medidas de Mitigación Inmediatas
1. **Fallback Dinámico de Codec:** La plataforma conmuta automáticamente a compresión VP9 y audio mono Opus a 24 kbps.
2. **Forzar Canal TURN Seguro:** Si el firewall institucional bloquea UDP (puertos 49152-65535), el sistema conmuta a `turn.quantux.salud.ar:443` vía TCP/TLS.
3. **Modo Solo Audio:** Si el ancho de banda desciende de 128 kbps, se pausa la pista de video preservando la comunicación clínica sin cortar la llamada."""
        ),
        KBArticle(
            title="Configuración de Sala de Espera Virtual, Triage y Notificaciones Push",
            category="Telemedicina",
            tags="sala de espera, push, websocket, notificaciones, fcm, turnos, triage",
            version="v1.2",
            changelog="Implementación de canal de contingencia vía SMS para pacientes sin app activa",
            view_count=78,
            author_username="soporte",
            content="""### 1. Flujo de Atención Virtual
El paciente ingresa a la sala de espera web tras completar el cuestionario de triage de síntomas. El médico visualiza la lista clasificada por escala Manchester (Rojo/Amarillo/Verde).

### 2. Reglas de Notificación
1. **Alerta 10 minutos antes:** Notificación Push y correo recordatorio con enlace directo de acceso.
2. **Llamado del Profesional:** Cuando el médico pulsa 'Llamar Paciente', se dispara un ping WebSocket con tono audible y vibración.
3. **Canal SMS de Respaldo:** Si no se detecta conexión activa en 60 segundos, se despacha un SMS automático con el enlace de conexión rápida."""
        ),

        # --- 3. HISTORIA CLÍNICA ---
        KBArticle(
            title="Procedimiento de Bloqueo Criptográfico y Sellado de Tiempo en HCE",
            category="Historia Clínica",
            tags="hce, sellado de tiempo, tsa, rfc 3161, ley 25506, auditoria, inmutabilidad",
            version="v3.0",
            changelog="Homologación con Autoridad Certificante Raíz y Ley 25.506 de Firma Digital",
            view_count=167,
            source_ticket_id="TICK-202608-0004",
            author_username="admin",
            content="""### 1. Requisitos Legales y de Seguridad
Conforme a la Ley 26.529 de Derechos del Paciente y Ley 25.506 de Firma Digital, todo registro clínico debe ser inmutable y contar con sellado de tiempo criptográfico (Timestamping Authority - RFC 3161).

### 2. Protocolo de Bloqueo
1. **Cierre de Evolución:** Al guardar la consulta, el motor genera un hash SHA-256 del contenido clínico.
2. **Firma y Estampillado:** Se solicita la firma digital del profesional y la estampilla de tiempo del servidor TSA central.
3. **Auditoría Pericial:** Toda rectificación posterior genera una adenda encadenada sin modificar el registro original."""
        ),
        KBArticle(
            title="Reconciliación de Identidad de Pacientes y Fusión de Registros en MPI",
            category="Historia Clínica",
            tags="mpi, pacientes, dni, fusion registros, homonimia, duplicados, renaper",
            version="v1.5",
            changelog="Algoritmo probabilístico de coincidencia Jaro-Winkler para detección de duplicados",
            view_count=94,
            author_username="soporte",
            content="""### 1. Problema de Homonimia y Duplicados
Ocurre cuando un paciente es registrado con errores en su DNI, fecha de nacimiento o cambio de apellido conyugal, generando historias clínicas fragmentadas.

### 2. Procedimiento de Fusión Segura (Merge)
1. **Búsqueda en MPI:** Ingresar a `Historia Clínica > Herramientas MPI > Detección de Duplicados`.
2. **Validación RENAPER:** Validar los datos biométricos contra el padrón nacional de personas.
3. **Ejecución de Merge:** Seleccionar el registro 'Master' (destino) y el registro 'Secundario' (origen). El sistema fusiona evoluciones, alergias y estudios diagnósticos manteniendo el registro de auditoría del operador."""
        ),

        # --- 4. CONTINGENCIAS ---
        KBArticle(
            title="Plan de Continuidad Operativa (BCP): Caída de Enlace Sanatorial y Modo Offline",
            category="Contingencias",
            tags="bcp, offline, contingencia, caida enlace, sqlite local, resincronizacion",
            version="v2.3",
            changelog="Prueba semestral de desastre simulado superada con éxito (RTO < 5 min)",
            view_count=312,
            source_ticket_id="TICK-202608-0006",
            author_username="admin",
            content="""### 1. Activación del Protocolo BCP
Ante la pérdida de enlace a Internet en guardias médicas o centros ambulatorios, los puestos de trabajo conmutan automáticamente a la base de datos local SQLite cifrada en memoria (AES-256).

### 2. Operación en Modo Autónomo
- **Atención de Guardia:** Se pueden registrar evoluciones de emergencia y prescribir medicamentos básicos.
- **Identificación:** Se valida la identidad con la base local de afiliados cacheados.

### 3. Recuperación y Resincronización
Al restablecerse la conectividad WAN:
1. El agente de sincronización en segundo plano envía las atenciones firmadas en lotes de 20 registros.
2. Se resuelve cualquier colisión de turnos mediante política 'Last Write Wins con Adenda Humana'.
3. Se genera el informe de conciliación de contingencia."""
        ),
        KBArticle(
            title="Protocolo de Mitigación y Notificación ante Incidentes de Ciberseguridad",
            category="Contingencias",
            tags="seguridad, breach, hipaa, proteccion de datos, ciso, aislamiento, soc",
            version="v1.1",
            changelog="Alineación con directivas de ciberseguridad para infraestructura crítica de salud",
            view_count=129,
            author_username="admin",
            content="""### 1. Detección Temprana
Si el sistema SIEM / SOC detecta patrones anómalos de extracción masiva de datos clínicos o intentos de fuerza bruta en cuentas de médicos:

### 2. Acciones Inmediatas (Fase de Contención)
1. **Aislamiento de Sesión:** Revocación instantánea de todos los tokens JWT emitidos para la cuenta afectada.
2. **Bloqueo de IP:** Incorporación automática de la dirección IP de origen en la lista negra del WAF.
3. **Preservación de Evidencias:** Extracción de logs inmutables de acceso y auditoría de base de datos para peritaje forense."""
        ),

        # --- 5. FACTURACIÓN Y PAGOS ---
        KBArticle(
            title="Conciliación de Copagos Online y Recuperación de Transacciones Huérfanas",
            category="Facturación y Pagos",
            tags="copagos, pasarela, mercado pago, stripe, devoluciones, conciliacion",
            version="v1.8",
            changelog="Webhook idempotente y reintento con backoff exponencial",
            view_count=104,
            source_ticket_id="TICK-202608-0007",
            author_username="soporte",
            content="""### 1. Transacción Huérfana
Se produce cuando el paciente abona el copago en la pasarela de pagos pero cierra la ventana antes de redirigir al portal, dejando el turno en estado 'Pendiente de Confirmación'.

### 2. Conciliación Automática y Manual
1. **Webhook de Pasarela:** El sistema procesa el evento `payment.succeeded` de forma asíncrona mediante un endpoint idempotente.
2. **Comprobación Manual:** Si el paciente presenta el comprobante de pago bancario, ingresar a `Copagos > Transacciones Pendientes > Forzar Conciliación por ID de Operación`.
3. El turno se confirma inmediatamente y se emite la factura electrónica AFIP / CAE."""
        ),
        KBArticle(
            title="Configuración de Matrices de Copago y Coseguros Multi-Convenio",
            category="Facturación y Pagos",
            tags="obras sociales, prepagas, nomenclador, aranceles, copago porcentual",
            version="v1.3",
            changelog="Actualización de tablas de aranceles Nomenclador Nacional 2026",
            view_count=65,
            author_username="soporte",
            content="""### 1. Estructura de Aranceles
El módulo de facturación permite parametrizar reglas de copago fijas, porcentuales o mixtas según el plan del afiliado (ej: Plan Clásico vs. Plan Premium).

### 2. Carga de Reglas
1. Dirigirse a `Configuración > Reglas de Facturación > Nuevo Convenio`.
2. Seleccionar la Institución Sanitaria y el Financiador.
3. Definir los aranceles por código de práctica médica (consulta médica general, especialista, telemedicina guardia).
4. Guardar y verificar con la calculadora de cotización en tiempo real."""
        ),

        # --- 6. INTEROPERABILIDAD ---
        KBArticle(
            title="Guía de Integración FHIR R4: Recursos Patient, Encounter, MedicationRequest",
            category="Interoperabilidad",
            tags="fhir, hl7, r4, json, api rest, interoperabilidad, bus de salud, snomed",
            version="v2.4",
            changelog="Soporte de perfiles de la Red Nacional de Salud Digital e IPS (International Patient Summary)",
            view_count=188,
            source_ticket_id="TICK-202608-0005",
            author_username="admin",
            content="""### 1. Arquitectura REST FHIR R4
Quantux ServiceDesk expone un servidor FHIR R4 conforme al estándar HL7 Internacional para la interoperabilidad semántica entre prestadores de salud.

### 2. Endpoints Principales
- `GET /fhir/r4/Patient?identifier=DNI|12345678`: Consulta de datos demográficos.
- `POST /fhir/r4/Encounter`: Registro de evento de atención clínica o guardia.
- `POST /fhir/r4/MedicationRequest`: Prescripción electrónica estandarizada con códigos SNOMED CT.
- `GET /fhir/r4/DiagnosticReport?patient={id}`: Consulta de informes de laboratorio e imágenes.

### 3. Autenticación y Seguridad
Todas las peticiones requieren token OAuth2 / SMART on FHIR con scopes clínicos granulares (`patient/*.read`, `encounter/*.write`)."""
        ),
        KBArticle(
            title="Mapeo y Transformación de Mensajes HL7 v2.5.1 (ADT, ORM, ORU) con Mirth Connect",
            category="Interoperabilidad",
            tags="hl7 v2, mirth connect, nextgen, adt a08, orm o01, oru r01, mllp, his",
            version="v1.6",
            changelog="Canales MLLP con TLS 1.3 y reintentos automáticos en cola Dead-Letter",
            view_count=117,
            author_username="dnavarro",
            content="""### 1. Canales de Integración Hospitalaria (HIS/LIS/RIS)
Para instituciones con sistemas legados, el ServiceDesk incluye canales de integración MLLP basados en Mirth Connect.

### 2. Mapeo de Eventos
- **ADT^A04 / ADT^A08:** Admisión y actualización demográfica de pacientes.
- **ORM^O01:** Solicitud de estudios complementarios y órdenes de interconsulta.
- **ORU^R01:** Retorno de resultados diagnósticos estructurados.

### 3. Procedimiento ante Errores de Segmento
Si el mensaje es rechazado con `AR` (Application Reject) por falta del campo `PID-3` o `PV1-2`, inspeccionar la cola de mensajes en `Herramientas > Visor MLLP` y aplicar la regla de transformación JavaScript correspondiente."""
        ),

        # --- 7. CONSULTORIO DIGITAL ---
        KBArticle(
            title="Configuración de Agenda Médica Inteligente, Sobreturnos y Cancelaciones",
            category="Consultorio Digital",
            tags="agenda, turnos, consultorio, sobreturnos, cancelacion automatica, whatsapp",
            version="v1.7",
            changelog="Recordatorios automáticos vía WhatsApp con confirmación interactiva 1-click",
            view_count=155,
            author_username="soporte",
            content="""### 1. Gestión Eficiente de la Demanda Asistencial
El módulo de Consultorio Digital permite configurar intervalos de consulta según especialidad (ej: 15 min para medicina general, 45 min para salud mental).

### 2. Funcionalidades Clave
1. **Reglas de Sobreturnos:** Límite máximo de 2 sobreturnos por bloque horario para evitar demoras en sala de espera.
2. **Confirmación Automatizada:** Despacho de mensaje WhatsApp 24h antes del turno. Si el paciente presiona 'Cancelar', el turno se libera automáticamente para la lista de espera prioritaria.
3. **Bloqueos Preventivos:** Habilitación de franjas de investigación o ateneos clínicos con 1 solo clic."""
        ),
        KBArticle(
            title="Emisión de Certificados Médicos Digitales y Reposo Laboral con QR Inmutable",
            category="Consultorio Digital",
            tags="certificados medicos, reposo laboral, qr, validacion web, firma digital",
            version="v1.2",
            changelog="Portal público de verificación de autenticidad de certificados sin credenciales",
            view_count=98,
            author_username="soporte",
            content="""### 1. Emisión Segura y Validez Legal
Los certificados médicos de reposo laboral, aptitud física o recetas de uso prolongado cuentan con firma digital homologada y código QR de validación inmutable.

### 2. Pasos para el Profesional
1. Desde la Historia Clínica, hacer clic en `Documentos > Nuevo Certificado Médico`.
2. Seleccionar el tipo de documento (Reposo Laboral / Apto Físico / Certificado de Tratamiento).
3. Ingresar los días de reposo y diagnóstico (codificado según CIE-10).
4. Firmar con token digital. El paciente recibe el PDF firmado en su app y los empleadores pueden escanear el QR para verificar su autenticidad sin necesidad de ingresar al sistema."""
        ),
    ]

    for a in articles:
        session.add(a)

    session.commit()

    # Generar registros de historial para simular versionado profesional
    for a in articles:
        session.add(KBArticleHistory(
            article_id=a.id,
            version="v1.0",
            title=a.title,
            category=a.category,
            content=a.content,
            author_username="admin",
            tags=a.tags,
            changelog="Creación inicial del protocolo y homologación con el equipo médico",
            source_ticket_id=a.source_ticket_id,
            created_at=datetime.utcnow()
        ))
        if a.version != "v1.0":
            session.add(KBArticleHistory(
                article_id=a.id,
                version=a.version,
                title=a.title,
                category=a.category,
                content=a.content,
                author_username=a.author_username,
                tags=a.tags,
                changelog=a.changelog or "Actualización de versión",
                source_ticket_id=a.source_ticket_id,
                created_at=datetime.utcnow()
            ))

    session.commit()
    print(f"Successfully seeded {len(articles)} Knowledge Base articles with full history!")

def run_seed():
    init_db()
    with Session(engine) as session:
        # Asegurar siempre que los artículos de KB estén sembrados
        seed_kb_articles(session)

        # 1. VERIFICAR SI YA HAY DATOS DE USUARIOS
        existing_user = session.exec(select(User)).first()
        if existing_user:
            print("Users and base entities already seeded.")
            return

        print("Seeding Quantux HealthDesk Base Entities...")

        # 2. USUARIOS BASE (3 ROLES CON NIVELES ITIL)
        users = [
            User(username="admin", full_name="Freddy Cortés", email="fcortes@quantuxsalud.com", role=UserRole.ADMIN, support_level=SupportLevel.N3),
            User(username="mrodriguez", full_name="Mariana Rodríguez", email="mrodriguez@quantux.com", role=UserRole.ADMIN, support_level=SupportLevel.N3),
            User(username="cpaez", full_name="Carlos Páez", email="cpaez@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N1),
            User(username="svaldez", full_name="Sofía Valdez", email="svaldez@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N1),
            User(username="mflores", full_name="Marcos Flores", email="mflores@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N1),
            User(username="soporte", full_name="Laura Benítez", email="soporte@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N2),
            User(username="gfernandez", full_name="Gonzalo Fernández", email="gfernandez@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N2),
            User(username="vromero", full_name="Valeria Romero", email="vromero@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N2),
            User(username="dnavarro", full_name="Diego Navarro", email="dnavarro@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N3),
            User(username="ealvarez", full_name="Esteban Álvarez", email="ealvarez@quantux.com", role=UserRole.SOPORTE, support_level=SupportLevel.N3),
            User(username="solicitante", full_name="Dr. Martín Gómez", email="solicitante@quantux.com", role=UserRole.SOLICITANTE, support_level=None),
            User(username="alopez", full_name="Dra. Andrea López", email="alopez@sanatorio.salud.ar", role=UserRole.SOLICITANTE, support_level=None),
            User(username="jmolina", full_name="Dr. Javier Molina", email="jmolina@swissmedical.com.ar", role=UserRole.SOLICITANTE, support_level=None),
            User(username="cbenedetti", full_name="Dra. Clara Benedetti", email="cbenedetti@hospitalaleman.com", role=UserRole.SOLICITANTE, support_level=None),
        ]
        for u in users:
            session.add(u)

        # 3. LAS 9 PLATAFORMAS OFICIALES
        platforms = [
            Platform(code="CAT_RECETA", name="Receta Electrónica", description="Emisión, firma digital y dispensa farmacéutica (+400k recetas/mes)"),
            Platform(code="CAT_TELEMEDICINA", name="Telemedicina", description="Videoconsultas sincrónicas, sala de espera virtual y triage"),
            Platform(code="CAT_COPAGOS_PAGOS", name="Copagos y Pasarela de Pagos", description="Cobro de coseguros, liquidaciones y pagos online"),
            Platform(code="CAT_RPM_MONITOREO", name="Monitoreo Remoto (RPM)", description="Seguimiento de pacientes crónicos y telemetría de dispositivos"),
            Platform(code="CAT_INTERNACION_DOM", name="Internación Domiciliaria", description="Logística de visitas, insumos y evolución asistencial domiciliaria"),
            Platform(code="CAT_AFILIADOS_PORTAL", name="Portal de Afiliados / Pacientes", description="Autogestión de credenciales, historial y autorizaciones"),
            Platform(code="CAT_CARTILLA_TURNOS", name="Cartilla Asistencial y Turnos", description="Geolocalización de prestadores y reserva online de citas"),
            Platform(code="CAT_REGISTRO_INTEROP", name="Interoperabilidad y Registro", description="Integración bajo estándar HL7 / FHIR con entidades de salud"),
            Platform(code="CAT_CONSULTORIO_DIGITAL", name="Consultorio Digital", description="Historia clínica ambulatoria para 12.000 profesionales de la salud activos"),
        ]
        for p in platforms:
            session.add(p)

        # 4. LOS 14 CLIENTES INSTITUCIONALES
        institutions = [
            Institution(code="OSDE", name="OSDE", segment="Financiador / Prepaga"),
            Institution(code="SWISS_MEDICAL", name="Swiss Medical", segment="Financiador / Prepaga"),
            Institution(code="GALENO", name="Galeno", segment="Financiador / Prepaga"),
            Institution(code="MEDIFE", name="Medifé", segment="Financiador / Prepaga"),
            Institution(code="OMINT", name="Omint", segment="Financiador / Prepaga"),
            Institution(code="PREVENCION_SALUD", name="Prevención Salud", segment="Financiador / Prepaga"),
            Institution(code="SANATORIO_FINOCHIETTO", name="Sanatorio Finochietto", segment="Sanatorio / Hospital"),
            Institution(code="HOSPITAL_BRITANICO", name="Hospital Británico", segment="Sanatorio / Hospital"),
            Institution(code="HOSPITAL_ALEMAN", name="Hospital Alemán", segment="Sanatorio / Hospital"),
            Institution(code="SANATORIO_TRINIDAD", name="Sanatorio de la Trinidad", segment="Sanatorio / Hospital"),
            Institution(code="IDOM", name="IDOM", segment="Internación Domiciliaria"),
            Institution(code="MEVATERAPIA", name="Mevaterapia", segment="Internación Domiciliaria"),
            Institution(code="ORIEN", name="ORIEN", segment="Internación Domiciliaria"),
            Institution(code="RED_ASISTENCIAL", name="Red Asistencial Integral", segment="Internación Domiciliaria"),
        ]
        for inst in institutions:
            session.add(inst)

        session.commit()

        # 5. TICKETS DE EJEMPLO CUBRIENDO LOS 5 ESTADOS DEL FLUJO
        tickets = [
            # TICKET 1: NUEVO
            Ticket(
                id="TICK-202608-0001",
                title="Error de firma digital en receta OSDE",
                description="Profesional de la Salud reporta bloqueo al intentar firmar receta digital de psicotrópicos con certificado.",
                platform_code="CAT_RECETA",
                institution_code="OSDE",
                ticket_type=TicketType.INCIDENTE,
                impact=ImpactLevel.ALTO,
                urgency=UrgencyLevel.ALTO,
                priority=PriorityLevel.P1,
                status=TicketStatus.NUEVO,
                requester_username="solicitante",
                support_level=SupportLevel.N1,
                created_at=datetime.utcnow()
            ),
            # TICKET 2: ASIGNADO
            Ticket(
                id="TICK-202608-0002",
                title="Cámara no inicia en sala de espera virtual",
                description="Paciente no logra habilitar video en consulta de telemedicina con Swiss Medical.",
                platform_code="CAT_TELEMEDICINA",
                institution_code="SWISS_MEDICAL",
                ticket_type=TicketType.INCIDENTE,
                impact=ImpactLevel.MEDIO,
                urgency=UrgencyLevel.ALTO,
                priority=PriorityLevel.P2,
                status=TicketStatus.ASIGNADO,
                requester_username="solicitante",
                assignee_username="soporte",
                support_level=SupportLevel.N1,
                created_at=datetime.utcnow()
            ),
            # TICKET 3: EN CURSO
            Ticket(
                id="TICK-202608-0003",
                title="Rechazo en pasarela de copagos Galeno",
                description="Se reporta timeout recurrente al procesar coseguro en línea para pacientes ambulatorios.",
                platform_code="CAT_COPAGOS_PAGOS",
                institution_code="GALENO",
                ticket_type=TicketType.INCIDENTE,
                impact=ImpactLevel.MEDIO,
                urgency=UrgencyLevel.MEDIO,
                priority=PriorityLevel.P3,
                status=TicketStatus.EN_CURSO,
                requester_username="solicitante",
                assignee_username="soporte",
                support_level=SupportLevel.N2,
                created_at=datetime.utcnow()
            ),
            # TICKET 4: RESUELTO
            Ticket(
                id="TICK-202608-0004",
                title="Alta de prestador en internación domiciliaria IDOM",
                description="Enfermera no figuraba en el padrón para carga de evolución asistencial en domicilio.",
                platform_code="CAT_INTERNACION_DOM",
                institution_code="IDOM",
                ticket_type=TicketType.REQUERIMIENTO,
                impact=ImpactLevel.BAJO,
                urgency=UrgencyLevel.MEDIO,
                priority=PriorityLevel.P4,
                status=TicketStatus.RESUELTO,
                requester_username="solicitante",
                assignee_username="soporte",
                support_level=SupportLevel.N1,
                resolution_notes="Se habilitó el perfil asistencial en la base de IDOM y se verificó ingreso exitoso.",
                is_workaround=False,
                created_at=datetime.utcnow(),
                resolved_at=datetime.utcnow()
            ),
            # TICKET 5: CERRADO
            Ticket(
                id="TICK-202608-0005",
                title="Consulta sobre integración HL7 FHIR Finochietto",
                description="Validación de endpoints para sincronización de turnos ambulatorios.",
                platform_code="CAT_REGISTRO_INTEROP",
                institution_code="SANATORIO_FINOCHIETTO",
                ticket_type=TicketType.CONSULTA,
                impact=ImpactLevel.BAJO,
                urgency=UrgencyLevel.BAJO,
                priority=PriorityLevel.P5,
                status=TicketStatus.CERRADO,
                requester_username="solicitante",
                assignee_username="soporte",
                support_level=SupportLevel.N3,
                resolution_notes="Se envió documentación de API y credenciales del entorno sandbox.",
                is_workaround=False,
                created_at=datetime.utcnow(),
                resolved_at=datetime.utcnow(),
                closed_at=datetime.utcnow()
            )
        ]

        for t in tickets:
            session.add(t)

        # 6. COMENTARIOS Y AUDITORÍA INICIAL
        session.add(TicketComment(
            ticket_id="TICK-202608-0003",
            author_username="soporte",
            message="Se contactó al equipo de infraestructura para revisar latencia con el gateway de Galeno.",
            is_internal=True
        ))

        session.add(TicketAuditLog(
            ticket_id="TICK-202608-0004",
            changed_by_username="soporte",
            field_changed="status",
            old_value="EN_CURSO",
            new_value="RESUELTO",
            change_reason="Solución aplicada y verificada con el usuario."
        ))

        session.commit()
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    run_seed()
