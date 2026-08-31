from datetime import datetime
from sqlmodel import Session, select
from app.db.session import engine, init_db
from app.models.entities import (
    User, UserRole, Platform, Institution, Ticket,
    TicketStatus, TicketType, ImpactLevel, UrgencyLevel,
    PriorityLevel, SupportLevel, TicketComment, TicketAuditLog
)

def run_seed():
    init_db()
    with Session(engine) as session:
        # 1. VERIFICAR SI YA HAY DATOS
        existing_user = session.exec(select(User)).first()
        if existing_user:
            print("Database already seeded.")
            return

        print("Seeding Quantux HealthDesk Database...")

        # 2. USUARIOS BASE (3 ROLES)
        users = [
            User(username="solicitante", full_name="Lic. Martín Gómez (Profesional de la Salud Prestador)", email="solicitante@quantux.com", role=UserRole.SOLICITANTE),
            User(username="soporte", full_name="Laura Benítez (Operadora de Soporte)", email="soporte@quantux.com", role=UserRole.SOPORTE),
            User(username="admin", full_name="Freddy Cortés (Administrador / Solution Owner)", email="admin@quantux.com", role=UserRole.ADMIN),
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
