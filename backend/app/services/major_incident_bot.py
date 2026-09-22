# -*- coding: utf-8 -*-
"""
Bot de Gestión de Incidencias Masivas (Major Incident Bot) - QuantUX v4.1.0-DEV
Implementación de los Criterios ITIL de Detección, Gestión de Ticket Padre,
Alerta Proactiva para Solicitantes y Generación de Tarjetas Kanban N3.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select, func

from app.models.entities import (
    Ticket, TicketStatus, TicketType, ImpactLevel, UrgencyLevel,
    PriorityLevel, SupportLevel, TicketAuditLog, User
)

# Plataformas críticas asistenciales
CRITICAL_PLATFORMS = {
    "CAT_CONSULTORIO_DIGITAL", "CD2", "CONSULTORIO_DIGITAL",
    "CAT_RECETA", "RECETA", "RECETA_ELECTRONICA",
    "CAT_TELEMEDICINA", "TELEMEDICINA"
}

PLATFORM_ALIASES = {
    "CD2": "CAT_CONSULTORIO_DIGITAL",
    "CONSULTORIO_DIGITAL": "CAT_CONSULTORIO_DIGITAL",
    "CAT_CONSULTORIO_DIGITAL": "CAT_CONSULTORIO_DIGITAL",
    "RECETA": "CAT_RECETA",
    "RECETA_ELECTRONICA": "CAT_RECETA",
    "CAT_RECETA": "CAT_RECETA",
    "TELEMEDICINA": "CAT_TELEMEDICINA",
    "CAT_TELEMEDICINA": "CAT_TELEMEDICINA",
}

def get_canonical_platform(code: Optional[str]) -> str:
    if not code:
        return ""
    code_upper = code.strip().upper()
    return PLATFORM_ALIASES.get(code_upper, code_upper)

def platforms_match(plat1: Optional[str], plat2: Optional[str]) -> bool:
    if not plat1 or not plat2:
        return False
    if plat1 == plat2:
        return True
    return get_canonical_platform(plat1) == get_canonical_platform(plat2)

def generate_major_incident_id(session: Session) -> str:
    now = datetime.utcnow()
    month_str = now.strftime('%Y%m')
    candidate = f"TICK-{month_str}-MAJOR-{int(now.timestamp() * 1000) % 100000:05d}"
    seq = 1
    while session.get(Ticket, candidate) is not None:
        candidate = f"TICK-{month_str}-MAJOR-{(int(now.timestamp() * 1000) + seq) % 100000:05d}"
        seq += 1
    return candidate


class MajorIncidentBot:
    """
    Motor autónomo pericial para la detección y gestión de incidentes mayores:
    1. Evalúa umbrales de afectación masiva (>=3 tickets en <30 min sobre la misma plataforma o plataforma crítica).
    2. Identifica o crea el 'Ticket Padre' (Problem / Major Incident, P1, PROBLEMA, is_major_incident=True).
    3. Asocia los reportes individuales como 'Tickets Hijos' (parent_ticket_id = padre.id).
    4. Emite alerta en el portal para evitar el colapso de la mesa de soporte.
    5. Inyecta la tarjeta prioritaria en el Tablero Kanban.
    """

    @staticmethod
    def get_active_major_incident(session: Optional[Session] = None) -> Optional[Dict[str, Any]]:
        """
        Devuelve la incidencia masiva activa si existe (no resuelta ni cerrada),
        incluyendo el ticket padre y la lista completa de tickets hijos.
        """
        if session is None:
            from app.db.session import engine
            with Session(engine) as s:
                return MajorIncidentBot.get_active_major_incident(s)

        active_majors = session.exec(
            select(Ticket)
            .where(Ticket.is_major_incident == True)
            .where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
            .order_by(Ticket.created_at.desc())
        ).all()

        if not active_majors:
            return None

        parent = active_majors[0]
        child_tickets = session.exec(
            select(Ticket)
            .where(Ticket.parent_ticket_id == parent.id)
            .order_by(Ticket.created_at.desc())
        ).all()

        child_list = [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "platform_code": c.platform_code,
                "institution_code": c.institution_code,
                "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                "priority": c.priority.value if hasattr(c.priority, "value") else str(c.priority),
                "requester_username": c.requester_username,
                "parent_ticket_id": c.parent_ticket_id,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in child_tickets
        ]

        return {
            "has_active_major_incident": True,
            "parent_ticket": {
                "id": parent.id,
                "title": parent.title,
                "description": parent.description,
                "platform_code": parent.platform_code,
                "institution_code": parent.institution_code,
                "ticket_type": parent.ticket_type.value if hasattr(parent.ticket_type, "value") else str(parent.ticket_type),
                "priority": parent.priority.value if hasattr(parent.priority, "value") else str(parent.priority),
                "status": parent.status.value if hasattr(parent.status, "value") else str(parent.status),
                "is_major_incident": parent.is_major_incident,
                "created_at": parent.created_at.isoformat() if parent.created_at else None,
                "child_count": len(child_tickets)
            },
            "child_tickets": child_list,
            "child_ticket_ids": [c.id for c in child_tickets],
            "alert_banner": {
                "level": "CRITICAL",
                "title": f"⚠️ INCIDENCIA MASIVA EN CURSO: {parent.title}",
                "message": (
                    f"Se ha detectado una degradación generalizada en el módulo de {parent.platform_code}. "
                    f"El equipo de guardia N3 e ingeniería ya está trabajando bajo el Ticket de Problema #{parent.id}. "
                    f"No es necesario generar nuevos tickets por este inconveniente."
                ),
                "badge": "INCIDENTE MAYOR (P1)",
                "parent_id": parent.id
            }
        }

    @staticmethod
    def evaluate_and_associate(
        session: Session,
        new_ticket: Ticket,
        time_window_minutes: int = 30,
        threshold_count: int = 3
    ) -> Optional[Ticket]:
        """
        Al ingresar un nuevo ticket, evalúa si forma parte de una casuística masiva ITIL:
        1. Si ya hay un ticket padre activo en la misma plataforma/módulo, asocia automáticamente el ticket entrante (parent_ticket_id = padre.id).
        2. Si se alcanza el umbral de >= 3 reportes concurrentes en < 30 minutos sobre la misma plataforma
           (especialmente plataformas críticas como CAT_CONSULTORIO_DIGITAL, CD2, CAT_RECETA),
           crea automáticamente el Ticket Padre de Problema (is_major_incident=True, ticket_type='PROBLEMA', priority='P1')
           y asocia todos los tickets similares como tickets hijos.
        """
        # Si el ticket ya es incidente mayor, no procesar como hijo
        if new_ticket.is_major_incident:
            return None

        # Si ya tiene un ticket padre asignado explícitamente, devolverlo
        if new_ticket.parent_ticket_id:
            return session.get(Ticket, new_ticket.parent_ticket_id)

        # 1. Comprobar si ya existe un ticket padre activo en la misma plataforma
        active_parents = session.exec(
            select(Ticket)
            .where(Ticket.is_major_incident == True)
            .where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
            .order_by(Ticket.created_at.desc())
        ).all()

        active_parent = next((p for p in active_parents if platforms_match(p.platform_code, new_ticket.platform_code)), None)

        if active_parent:
            new_ticket.parent_ticket_id = active_parent.id
            session.add(new_ticket)
            session.add(TicketAuditLog(
                ticket_id=new_ticket.id,
                changed_by_username="sistema_triage",
                field_changed="parent_ticket_id",
                old_value=None,
                new_value=active_parent.id,
                change_reason=f"Asociación automática como ticket hijo al incidente mayor activo {active_parent.id}"
            ))
            session.commit()
            session.refresh(new_ticket)
            return active_parent

        # 2. Comprobar si se alcanza el umbral de casuística repetida (Regla ITIL)
        window_start = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        recent_candidates = session.exec(
            select(Ticket)
            .where(Ticket.created_at >= window_start)
            .where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
            .where(Ticket.is_major_incident == False)
            .where(Ticket.parent_ticket_id.is_(None))
            .order_by(Ticket.created_at.desc())
        ).all()

        similar_recent = [
            t for t in recent_candidates
            if platforms_match(t.platform_code, new_ticket.platform_code)
        ]

        if new_ticket.id not in [t.id for t in similar_recent]:
            similar_recent.append(new_ticket)

        is_critical = new_ticket.platform_code in CRITICAL_PLATFORMS or get_canonical_platform(new_ticket.platform_code) in CRITICAL_PLATFORMS

        if len(similar_recent) >= threshold_count:
            # Declarar Incidencia Masiva y Crear Ticket Padre (ITIL Problem P1)
            parent_id = generate_major_incident_id(session)
            crit_label = " [CRÍTICO]" if is_critical else ""
            parent_ticket = Ticket(
                id=parent_id,
                title=f"[INCIDENCIA MASIVA] Interrupción de Servicio en {new_ticket.platform_code}{crit_label}",
                description=(
                    f"Incidencia Masiva declarada automáticamente por el Bot de Soporte ITIL tras detectar "
                    f"{len(similar_recent)} reportes concurrentes en menos de {time_window_minutes} minutos.\n"
                    f"Servicio Afectado: {new_ticket.platform_code}\n"
                    f"Protocolo de Incidente Mayor (P1) activado con alerta general en portal."
                ),
                platform_code=new_ticket.platform_code,
                institution_code=new_ticket.institution_code or "OSDE",
                ticket_type=TicketType.PROBLEMA,
                impact=ImpactLevel.ALTO,
                urgency=UrgencyLevel.ALTO,
                priority=PriorityLevel.P1,
                status=TicketStatus.EN_CURSO,
                requester_username=new_ticket.requester_username or "admin",
                support_level=SupportLevel.N3,
                is_major_incident=True,
                channel="BOT_AUTOMATION",
                release_tag=parent_id,  # Vincular ticket principal al Release de Kanban N3
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(parent_ticket)
            session.add(TicketAuditLog(
                ticket_id=parent_ticket.id,
                changed_by_username="sistema_triage",
                field_changed="is_major_incident",
                old_value=None,
                new_value="True",
                change_reason=f"Declaración automática de Incidencia Masiva ITIL ({len(similar_recent)} tickets en {time_window_minutes}m)"
            ))

            # Crear automáticamente la tarjeta SoftwareRelease para el Kanban N3
            from app.models.entities import SoftwareRelease, ReleaseStatus
            kanban_card = SoftwareRelease(
                tag=parent_id,
                name=parent_ticket.title,
                notes=parent_ticket.description,
                status=ReleaseStatus.EN_DESARROLLO,
                created_by="sistema_triage",
                created_at=datetime.utcnow()
            )
            session.add(kanban_card)
            session.commit()
            session.refresh(parent_ticket)

            # Asociar todos los tickets recientes como hijos y vincularlos al release
            for t in similar_recent:
                t.parent_ticket_id = parent_ticket.id
                t.release_tag = parent_id  # Asociar también los hijos al Release de Kanban N3 para que aparezcan agrupados
                session.add(t)
                session.add(TicketAuditLog(
                    ticket_id=t.id,
                    changed_by_username="sistema_triage",
                    field_changed="parent_ticket_id",
                    old_value=None,
                    new_value=parent_ticket.id,
                    change_reason=f"Asociación automática como ticket hijo al incidente mayor {parent_ticket.id}"
                ))

            session.commit()
            session.refresh(new_ticket)
            return parent_ticket

        return None

    @staticmethod
    def declare_major_incident(
        session: Session,
        title: str,
        description: str,
        platform_code: str,
        institution_code: str = "OSDE",
        declared_by: str = "admin",
        time_window_hours: int = 2
    ) -> Dict[str, Any]:
        """
        Declaración manual de una Incidencia Masiva (Ticket Padre P1 / PROBLEMA)
        y vinculación retrospectiva de tickets recientes de la misma plataforma.
        """
        now = datetime.utcnow()
        parent_id = generate_major_incident_id(session)
        full_title = f"[INCIDENCIA MASIVA] {title}" if not title.startswith("[INCIDENCIA MASIVA]") else title

        parent_ticket = Ticket(
            id=parent_id,
            title=full_title,
            description=description,
            platform_code=platform_code,
            institution_code=institution_code or "OSDE",
            ticket_type=TicketType.PROBLEMA,
            impact=ImpactLevel.ALTO,
            urgency=UrgencyLevel.ALTO,
            priority=PriorityLevel.P1,
            status=TicketStatus.EN_CURSO,
            requester_username=declared_by or "admin",
            support_level=SupportLevel.N3,
            is_major_incident=True,
            channel="MAJOR_INCIDENT_PROTOCOL",
            release_tag=parent_id,  # Vincular ticket principal al Release de Kanban N3
            created_at=now,
            updated_at=now
        )
        session.add(parent_ticket)
        session.add(TicketAuditLog(
            ticket_id=parent_ticket.id,
            changed_by_username=declared_by or "admin",
            field_changed="is_major_incident",
            old_value=None,
            new_value="True",
            change_reason="Declaración manual de Incidencia Masiva (Protocolo P1)"
        ))

        # Crear automáticamente la tarjeta SoftwareRelease para el Kanban N3
        from app.models.entities import SoftwareRelease, ReleaseStatus
        kanban_card = SoftwareRelease(
            tag=parent_id,
            name=parent_ticket.title,
            notes=parent_ticket.description,
            status=ReleaseStatus.EN_DESARROLLO,
            created_by=declared_by or "admin",
            created_at=now
        )
        session.add(kanban_card)
        session.commit()
        session.refresh(parent_ticket)

        # Vincular automáticamente tickets recientes no resueltos de la misma plataforma
        window_start = now - timedelta(hours=time_window_hours)
        candidates = session.exec(
            select(Ticket)
            .where(Ticket.created_at >= window_start)
            .where(Ticket.id != parent_id)
            .where(Ticket.is_major_incident == False)
            .where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
        ).all()

        children = [c for c in candidates if platforms_match(c.platform_code, platform_code)]
        for c in children:
            c.parent_ticket_id = parent_id
            c.release_tag = parent_id  # Asociar también los hijos al Release de Kanban N3
            session.add(c)
            session.add(TicketAuditLog(
                ticket_id=c.id,
                changed_by_username=declared_by or "admin",
                field_changed="parent_ticket_id",
                old_value=None,
                new_value=parent_id,
                change_reason=f"Asociación a Incidencia Masiva declarada {parent_id}"
            ))

        session.commit()

        child_list = [
            {
                "id": c.id,
                "title": c.title,
                "platform_code": c.platform_code,
                "status": c.status.value if hasattr(c.status, "value") else str(c.status),
                "priority": c.priority.value if hasattr(c.priority, "value") else str(c.priority),
                "requester_username": c.requester_username,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in children
        ]

        return {
            "status": "success",
            "parent_ticket_id": parent_id,
            "parent_ticket": {
                "id": parent_ticket.id,
                "title": parent_ticket.title,
                "description": parent_ticket.description,
                "platform_code": parent_ticket.platform_code,
                "institution_code": parent_ticket.institution_code,
                "ticket_type": parent_ticket.ticket_type.value if hasattr(parent_ticket.ticket_type, "value") else str(parent_ticket.ticket_type),
                "priority": parent_ticket.priority.value if hasattr(parent_ticket.priority, "value") else str(parent_ticket.priority),
                "status": parent_ticket.status.value if hasattr(parent_ticket.status, "value") else str(parent_ticket.status),
                "is_major_incident": parent_ticket.is_major_incident,
                "created_at": parent_ticket.created_at.isoformat() if parent_ticket.created_at else None,
                "child_count": len(children)
            },
            "children_linked_count": len(children),
            "child_tickets": child_list,
            "child_ticket_ids": [c.id for c in children],
            "message": "Incidencia Masiva declarada exitosamente. Protocolo activado."
        }
