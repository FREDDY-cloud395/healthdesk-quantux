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

def run_simulation_cycle():
    """Ejecuta una iteración del simulador de actividad continua."""
    try:
        with Session(engine) as session:
            now = datetime.utcnow()
            
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

            # 3. Avanzar 1 ticket de NUEVO a ASIGNADO
            new_t = session.exec(select(Ticket).where(Ticket.status == TicketStatus.NUEVO)).first()
            if new_t and random.random() < 0.5:
                op = random.choice(OPERATORS)
                new_t.status = TicketStatus.ASIGNADO
                new_t.assignee_username = op
                new_t.support_level = SupportLevel.N1
                new_t.updated_at = now
                session.add(new_t)
                session.add(TicketAuditLog(
                    ticket_id=new_t.id,
                    changed_by_username="sistema_triage",
                    field_changed="assignee_username",
                    old_value="",
                    new_value=op,
                    change_reason=f"Asignación automática a especialista de guardia ({op}).",
                    created_at=now
                ))
                session.commit()

            # 4. Avanzar 1 ticket de ASIGNADO a EN_CURSO
            assigned_t = session.exec(select(Ticket).where(Ticket.status == TicketStatus.ASIGNADO)).first()
            if assigned_t and random.random() < 0.5:
                assigned_t.status = TicketStatus.EN_CURSO
                assigned_t.updated_at = now
                session.add(assigned_t)
                session.add(TicketAuditLog(
                    ticket_id=assigned_t.id,
                    changed_by_username=assigned_t.assignee_username or "soporte",
                    field_changed="status",
                    old_value="ASIGNADO",
                    new_value="EN_CURSO",
                    change_reason="Inicio de análisis técnico y diagnóstico de servicio.",
                    created_at=now
                ))
                session.commit()

            # 5. Resolver 1 ticket en EN_CURSO
            in_progress_t = session.exec(select(Ticket).where(Ticket.status == TicketStatus.EN_CURSO)).first()
            if in_progress_t and random.random() < 0.35:
                in_progress_t.status = TicketStatus.RESUELTO
                in_progress_t.resolved_at = now
                in_progress_t.updated_at = now
                in_progress_t.resolved_by = in_progress_t.assignee_username or "soporte"
                in_progress_t.resolution_notes = "Se aplicó corrección en la pasarela asistencial y se verificó disponibilidad con el personal de guardia."
                in_progress_t.is_workaround = False
                session.add(in_progress_t)
                session.add(TicketAuditLog(
                    ticket_id=in_progress_t.id,
                    changed_by_username=in_progress_t.resolved_by,
                    field_changed="status",
                    old_value="EN_CURSO",
                    new_value="RESUELTO",
                    change_reason="Resolución técnica verificada en producción.",
                    created_at=now
                ))
                session.commit()

            # 6. Cerrar 1 ticket en RESUELTO con CSAT
            resolved_t = session.exec(select(Ticket).where(Ticket.status == TicketStatus.RESUELTO)).first()
            if resolved_t and random.random() < 0.3:
                resolved_t.status = TicketStatus.CERRADO
                resolved_t.closed_at = now
                resolved_t.updated_at = now
                resolved_t.closed_by = resolved_t.requester_username or "solicitante"
                resolved_t.rating_stars = random.choice([4, 5])
                resolved_t.rating_kudos = random.choice(["Rapidez", "Excelente Trato", "Claridad Técnica", "Resolución Definitiva"])
                resolved_t.rating_feedback = "Excelente atención y rápida respuesta de la guardia técnica."
                session.add(resolved_t)
                session.add(TicketAuditLog(
                    ticket_id=resolved_t.id,
                    changed_by_username=resolved_t.closed_by,
                    field_changed="status",
                    old_value="RESUELTO",
                    new_value="CERRADO",
                    change_reason=f"Conformidad del solicitante con CSAT {resolved_t.rating_stars} estrellas.",
                    created_at=now
                ))
                session.commit()

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
