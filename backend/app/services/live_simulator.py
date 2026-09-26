"""
Live Demo Simulator Service for Quantux HealthDesk.
Runs as a background daemon thread to maintain continuous, realistic activity:
- Periodically creates new healthcare tickets across platforms and institutions.
- Transitions tickets (NUEVO -> ASIGNADO -> EN_CURSO -> RESUELTO -> CERRADO).
- Ensures balanced distribution for all KPIs (Overdue, Due Today, Open, On Hold, Unassigned, All).
"""

import threading
import time
import random
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.db.session import engine
from app.models.entities import (
    Ticket, TicketStatus, PriorityLevel, ImpactLevel, UrgencyLevel,
    TicketType, SupportLevel, TicketAuditLog, TicketComment
)

PLATFORMS = ["CAT_RECETA", "CAT_TELEMED", "CAT_HCE", "CAT_PORTAL", "CAT_TURNO", "CAT_LAB"]
INSTITUTIONS = [
    "ALEMAN", "ITALIANO", "BRITANICO", "OSDE", "SWISS_MED", "GALENO",
    "MATER_DEI", "TRINIDAD_PAL", "OTAMENDI", "ESPANYOL", "CEMIC", "FAVALORO"
]
TITLES = [
    ("Falla de sincronización en Receta Electrónica de guardia", "CAT_RECETA", TicketType.INCIDENTE, ImpactLevel.CRITICO, UrgencyLevel.CRITICA, PriorityLevel.P1),
    ("Médico de guardia reporta demora en validación de prescripciones", "CAT_RECETA", TicketType.INCIDENTE, ImpactLevel.ALTO, UrgencyLevel.ALTA, PriorityLevel.P2),
    ("Solicitud de alta de nuevo profesional en portal de turnos", "CAT_TURNO", TicketType.REQUERIMIENTO, ImpactLevel.MEDIO, UrgencyLevel.MEDIA, PriorityLevel.P3),
    ("Consulta sobre actualización de visor de estudios DICOM", "CAT_HCE", TicketType.CONSULTA, ImpactLevel.BAJO, UrgencyLevel.BAJA, PriorityLevel.P4),
    ("Error 504 al consultar historial farmacológico del paciente", "CAT_HCE", TicketType.INCIDENTE, ImpactLevel.ALTO, UrgencyLevel.CRITICA, PriorityLevel.P1),
    ("Solicitud de ventana de mantenimiento para servidor de imágenes", "CAT_LAB", TicketType.CAMBIO, ImpactLevel.MEDIO, UrgencyLevel.MEDIA, PriorityLevel.P3),
    ("Lentitud en la carga de agenda médica en consultorios externos", "CAT_PORTAL", TicketType.INCIDENTE, ImpactLevel.MEDIO, UrgencyLevel.MEDIA, PriorityLevel.P3),
    ("Audio-consulta en telemedicina presenta corte intermitente", "CAT_TELEMED", TicketType.INCIDENTE, ImpactLevel.ALTO, UrgencyLevel.ALTA, PriorityLevel.P2)
]
OPERATORS = ["soporte", "cpaez", "dnavarro"]
DOCTORS = ["dra_martinez", "dr_lopez", "solicitante", "dr_fernandez", "dra_gomez"]

_last_major_incident_time = None

def run_simulation_cycle():
    """Ejecuta una iteración del simulador de actividad continua."""
    global _last_major_incident_time
    try:
        with Session(engine) as session:
            now = datetime.utcnow()
            
            # Inyectar incidente masivo cada 5 minutos (300 segundos)
            if _last_major_incident_time is None or (now - _last_major_incident_time).total_seconds() >= 300:
                _last_major_incident_time = now
                try:
                    from app.services.major_incident_bot import MajorIncidentBot
                    platform = "CAT_RECETA"  # Receta Electrónica es la plataforma crítica por defecto
                    institution = random.choice(INSTITUTIONS)
                    doctor = random.choice(DOCTORS)
                    print(f"[LiveDemoSimulator] INICIANDO SIMULACION DE INCIDENTE MASIVO en plataforma {platform}...")
                    
                    for i in range(3):
                        prefix = f"TICK-{now.strftime('%Y%m')}"
                        existing_ids = session.exec(select(Ticket.id).where(Ticket.id.startswith(prefix))).all()
                        next_seq = len(existing_ids) + 1
                        t_id = f"{prefix}-{next_seq:04d}"
                        
                        title = f"Falla masiva de acceso concurrente en modulo {platform} - Lote #{i+1}"
                        new_tkt = Ticket(
                            id=t_id,
                            title=title,
                            description=f"Incidencia masiva critica simulada en la guardia de {institution}. Corte total del servicio {platform}. Se reportan errores 500 continuos en las terminales medicas.",
                            platform_code=platform,
                            institution_code=institution,
                            ticket_type=TicketType.INCIDENTE,
                            impact=ImpactLevel.CRITICO,
                            urgency=UrgencyLevel.CRITICA,
                            priority=PriorityLevel.P1,
                            status=TicketStatus.NUEVO,
                            requester_username=doctor,
                            assignee_username=None,
                            created_at=now,
                            updated_at=now
                        )
                        session.add(new_tkt)
                        
                        audit = TicketAuditLog(
                            ticket_id=t_id,
                            changed_by_username=doctor,
                            field_changed="status",
                            old_value="",
                            new_value="NUEVO",
                            change_reason="Creacion automatica de reporte critico de guardia.",
                            created_at=now
                        )
                        session.add(audit)
                        session.flush()  # Sincronizar para que la consulta del bot pericial encuentre el ticket
                        
                        # Disparar evaluacion del bot pericial ITIL
                        MajorIncidentBot.evaluate_and_associate(session, new_tkt)
                    
                    session.commit()
                    print("[LiveDemoSimulator] Incidente Masivo P1 creado con exito.")
                except Exception as e:
                    print(f"[LiveDemoSimulator ERROR al declarar incidente masivo]: {e}")
            
            # 1. Asegurar tickets con fechas de HOY y fechas distribuidas
            total_tickets = session.exec(select(Ticket)).all()
            if not total_tickets:
                return

            active_tickets = [t for t in total_tickets if t.status in (TicketStatus.NUEVO, TicketStatus.ASIGNADO, TicketStatus.EN_CURSO)]
            
            # 2. Generar nuevos tickets para mantener la mesa siempre con actividad activa (>220 tickets activos)
            if len(active_tickets) < 260 or random.random() < 0.4:
                item = random.choice(TITLES)
                inst = random.choice(INSTITUTIONS)
                doctor = random.choice(DOCTORS)
                
                # Generar ID
                prefix = f"TICK-{now.strftime('%Y%m')}"
                existing_ids = session.exec(select(Ticket.id).where(Ticket.id.startswith(prefix))).all()
                next_seq = len(existing_ids) + 1
                t_id = f"{prefix}-{next_seq:04d}"
                
                new_tkt = Ticket(
                    id=t_id,
                    title=item[0],
                    description=f"Incidencia reportada desde guardia de {inst}. {item[0]}. Se requiere atención según criticidad.",
                    platform_code=item[1],
                    institution_code=inst,
                    ticket_type=item[2],
                    impact=item[3],
                    urgency=item[4],
                    priority=item[5],
                    status=TicketStatus.NUEVO,
                    requester_username=doctor,
                    assignee_username=None,
                    created_at=now,
                    updated_at=now
                )
                session.add(new_tkt)
                
                audit = TicketAuditLog(
                    ticket_id=t_id,
                    changed_by_username=doctor,
                    field_changed="status",
                    old_value="",
                    new_value="NUEVO",
                    change_reason="Creación de solicitud asistencial en tiempo real.",
                    created_at=now
                )
                session.add(audit)
                session.commit()

            # 3. Avanzar tickets con el Bot Gestor de Tickets (diálogo multi-rol, sectores y aporte a KB)
            try:
                from app.services.ticket_manager_bot import TicketManagerBot
                TicketManagerBot.run_automation_cycle(session, max_tickets=2)
            except Exception as bot_err:
                print(f"[LiveDemoSimulator Bot Error]: {bot_err}")

    except Exception as e:
        print(f"[LiveDemoSimulator Error]: {e}")

class LiveSimulatorThread(threading.Thread):
    def __init__(self, interval_seconds=30):
        super().__init__(daemon=True)
        self.interval = interval_seconds
        self._running = True

    def run(self):
        print(f"[LiveDemoSimulator] Iniciado motor de actividad continua (intervalo: {self.interval}s).")
        # Ciclo inicial para balancear
        run_simulation_cycle()
        while self._running:
            time.sleep(self.interval)
            run_simulation_cycle()

    def stop(self):
        self._running = False

_simulator_instance = None

def start_live_simulator(interval_seconds=30):
    global _simulator_instance
    if _simulator_instance is None or not _simulator_instance.is_alive():
        _simulator_instance = LiveSimulatorThread(interval_seconds)
        _simulator_instance.start()
