from datetime import datetime, date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from app.db.session import get_session
from app.models.entities import Ticket, TicketStatus, PriorityLevel, User, UserRole, TicketAuditLog

router = APIRouter()

class TLReassignRequest(BaseModel):
    ticket_id: str
    new_assignee_username: str
    reason: str
    team_leader_username: str = "fcortes"

class TLRescueRequest(BaseModel):
    rescue_notes: str
    team_leader_username: str = "fcortes"

@router.get("/overview")
def get_team_leader_overview(session: Session = Depends(get_session)):
    all_tickets = session.exec(select(Ticket)).all()
    active_tickets = [t for t in all_tickets if t.status not in (TicketStatus.RESUELTO, TicketStatus.CERRADO)]
    
    # 1. P1 Activos
    p1_active = [t for t in active_tickets if t.priority == PriorityLevel.P1]
    
    # 2. Sin Asignar
    unassigned = [t for t in active_tickets if not t.assignee_username or t.status == TicketStatus.NUEVO]
    
    # 3. Alertas de Rescate CSAT (Quejas calificadas con 1 o 2 estrellas)
    rescue_alerts = [t for t in all_tickets if getattr(t, "requires_service_recovery", False)]
    
    # 4. Carga Operativa por Analista (SOPORTE / ADMIN)
    support_users = session.exec(
        select(User).where(User.role.in_([UserRole.SOPORTE, UserRole.ADMIN, UserRole.TEAM_LEADER]))
    ).all()
    
    agent_workload = []
    today_start = datetime.combine(date.today(), datetime.min.time())
    
    for u in support_users:
        assigned_active = [t for t in active_tickets if t.assignee_username == u.username]
        resolved_today = [
            t for t in all_tickets 
            if t.assignee_username == u.username 
            and t.status in (TicketStatus.RESUELTO, TicketStatus.CERRADO)
            and t.resolved_at and t.resolved_at >= today_start
        ]
        agent_workload.append({
            "username": u.username,
            "full_name": u.full_name,
            "role": u.role.value if hasattr(u.role, "value") else str(u.role),
            "support_level": u.support_level.value if hasattr(u.support_level, "value") and u.support_level else "N1",
            "active_tickets_count": len(assigned_active),
            "resolved_today_count": len(resolved_today),
            "active_ticket_ids": [t.id for t in assigned_active]
        })
        
    return {
        "metrics": {
            "total_active": len(active_tickets),
            "p1_active_count": len(p1_active),
            "unassigned_count": len(unassigned),
            "rescue_alerts_count": len(rescue_alerts),
            "active_agents_count": len(support_users)
        },
        "p1_active_tickets": p1_active,
        "unassigned_tickets": unassigned,
        "rescue_alerts": rescue_alerts,
        "agent_workload": agent_workload
    }

@router.post("/reassign")
def reassign_ticket_by_team_leader(req: TLReassignRequest, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, req.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")
    
    new_user = session.exec(select(User).where(User.username == req.new_assignee_username)).first()
    if not new_user:
        raise HTTPException(status_code=404, detail=f"Usuario analista {req.new_assignee_username} no encontrado.")
        
    old_assignee = ticket.assignee_username or "Sin Asignar"
    ticket.assignee_username = req.new_assignee_username
    if ticket.status == TicketStatus.NUEVO:
        ticket.status = TicketStatus.ASIGNADO
    ticket.updated_at = datetime.utcnow()
    session.add(ticket)
    
    session.add(TicketAuditLog(
        ticket_id=ticket.id,
        changed_by_username=req.team_leader_username,
        field_changed="assignee_username",
        old_value=old_assignee,
        new_value=req.new_assignee_username,
        change_reason=f"[Torre de Control TL] Rebalanceo operativo: {req.reason}"
    ))
    
    session.commit()
    session.refresh(ticket)
    return {
        "status": "success",
        "message": f"Solicitud #{ticket.id} reasignada exitosamente a {new_user.full_name} ({req.new_assignee_username}).",
        "ticket": ticket
    }

@router.post("/rescue/{ticket_id}")
def rescue_ticket_complaint(ticket_id: str, req: TLRescueRequest, session: Session = Depends(get_session)):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")
        
    ticket.requires_service_recovery = False
    ticket.updated_at = datetime.utcnow()
    session.add(ticket)
    
    session.add(TicketAuditLog(
        ticket_id=ticket.id,
        changed_by_username=req.team_leader_username,
        field_changed="requires_service_recovery",
        old_value="True",
        new_value="False",
        change_reason=f"[Torre de Control TL - Rescate CSAT] {req.rescue_notes}"
    ))
    
    session.commit()
    session.refresh(ticket)
    return {
        "status": "success",
        "message": f"Rescate de satisfacción registrado con éxito para la solicitud #{ticket.id}.",
        "ticket": ticket
    }
