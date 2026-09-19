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
    new_assignee_username: Optional[str] = None
    assigned_to_username: Optional[str] = None
    reason: str = "Rebalanceo operativo"
    team_leader_username: str = "cdaneri"

class TLRescueRequest(BaseModel):
    rescue_notes: str
    team_leader_username: str = "cdaneri"

class TLCustomRebalanceRequest(BaseModel):
    analyst_usernames: List[str]
    strategy: Optional[str] = "even"
    institution_code: Optional[str] = None
    team_leader_username: Optional[str] = "cdaneri"

@router.get("/overview")
def get_team_leader_overview(institution_code: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(Ticket)
    if institution_code and institution_code != "all":
        query = query.where(Ticket.institution_code == institution_code)
    all_tickets = session.exec(query).all()
    active_tickets = [t for t in all_tickets if t.status not in (TicketStatus.RESUELTO, TicketStatus.CERRADO)]
    
    # 1. P1 Activos
    p1_active = [t for t in active_tickets if t.priority == PriorityLevel.P1]
    
    # 2. Sin Asignar
    unassigned = [t for t in active_tickets if not t.assignee_username or t.status == TicketStatus.NUEVO]
    
    # 3. Alertas de Rescate CSAT (Quejas calificadas con 1 o 2 estrellas)
    rescue_alerts = [t for t in all_tickets if getattr(t, "requires_service_recovery", False)]
    
    # 4. Carga Operativa por Analista (SOPORTE / ADMIN / TEAM_LEADER)
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
    
    target_username = req.new_assignee_username or req.assigned_to_username
    if not target_username:
        raise HTTPException(status_code=400, detail="Debe indicar el nuevo analista asignado.")

    new_user = session.exec(select(User).where(User.username == target_username)).first()
    if not new_user:
        raise HTTPException(status_code=404, detail=f"Usuario analista {target_username} no encontrado.")
        
    old_assignee = ticket.assignee_username or "Sin Asignar"
    ticket.assignee_username = target_username
    if ticket.status == TicketStatus.NUEVO:
        ticket.status = TicketStatus.ASIGNADO
    ticket.updated_at = datetime.utcnow()
    session.add(ticket)
    
    session.add(TicketAuditLog(
        ticket_id=ticket.id,
        changed_by_username=req.team_leader_username or "teamleader",
        field_changed="assignee_username",
        old_value=old_assignee,
        new_value=target_username,
        change_reason=f"[Torre de Control TL] Rebalanceo operativo: {req.reason}"
    ))
    
    session.commit()
    session.refresh(ticket)
    return {
        "status": "success",
        "message": f"Solicitud #{ticket.id} reasignada exitosamente a {new_user.full_name} (@{target_username}).",
        "ticket": ticket
    }

@router.post("/custom-rebalance")
def custom_rebalance_workload(req: TLCustomRebalanceRequest, session: Session = Depends(get_session)):
    if not req.analyst_usernames:
        raise HTTPException(status_code=400, detail="Debe seleccionar al menos un analista para el balanceo.")
        
    selected_users = session.exec(
        select(User).where(User.username.in_(req.analyst_usernames))
    ).all()
    if not selected_users:
        raise HTTPException(status_code=404, detail="No se encontraron los analistas seleccionados.")

    query = select(Ticket).where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
    if req.institution_code and req.institution_code != "all":
        query = query.where(Ticket.institution_code == req.institution_code)
    active_tickets = session.exec(query).all()

    user_keys = [u.username for u in selected_users]
    workload = {u: 0 for u in user_keys}
    for t in active_tickets:
        if t.assignee_username in workload:
            workload[t.assignee_username] += 1

    reassigned_count = 0
    unassigned = [t for t in active_tickets if not t.assignee_username or t.status == TicketStatus.NUEVO]
    for t in unassigned:
        target_user = min(user_keys, key=lambda u: workload[u])
        t.assignee_username = target_user
        t.status = TicketStatus.ASIGNADO
        t.updated_at = datetime.utcnow()
        session.add(t)
        workload[target_user] += 1
        reassigned_count += 1
        session.add(TicketAuditLog(
            ticket_id=t.id,
            changed_by_username=req.team_leader_username or "cdaneri",
            field_changed="assignee_username",
            old_value="Sin Asignar",
            new_value=target_user,
            change_reason="[Rebalanceo Táctico TL] Asignación a analista seleccionado de menor carga"
        ))

    for _ in range(30):
        max_user = max(user_keys, key=lambda u: workload[u])
        min_user = min(user_keys, key=lambda u: workload[u])
        if workload[max_user] - workload[min_user] >= 2:
            candidate = next((t for t in active_tickets if t.assignee_username == max_user and t.priority != PriorityLevel.P1), None)
            if not candidate:
                candidate = next((t for t in active_tickets if t.assignee_username == max_user), None)
            if candidate:
                candidate.assignee_username = min_user
                candidate.updated_at = datetime.utcnow()
                session.add(candidate)
                workload[max_user] -= 1
                workload[min_user] += 1
                reassigned_count += 1
                session.add(TicketAuditLog(
                    ticket_id=candidate.id,
                    changed_by_username=req.team_leader_username or "cdaneri",
                    field_changed="assignee_username",
                    old_value=max_user,
                    new_value=min_user,
                    change_reason=f"[Rebalanceo Táctico TL] Descompresión de carga hacia @{min_user}"
                ))
        else:
            break

    session.commit()
    return {
        "status": "success",
        "message": f"Balanceo completado con éxito: {reassigned_count} tickets reasignados equitativamente entre los {len(selected_users)} analistas seleccionados.",
        "reassigned_count": reassigned_count,
        "workload": workload
    }

@router.post("/auto-rebalance")
def auto_rebalance_workload(session: Session = Depends(get_session)):
    support_users = session.exec(
        select(User).where(User.role.in_([UserRole.SOPORTE, UserRole.ADMIN, UserRole.TEAM_LEADER]))
    ).all()
    if not support_users:
        return {"status": "warning", "message": "No hay analistas de soporte activos para balancear.", "reassigned_count": 0}

    all_tickets = session.exec(select(Ticket)).all()
    active_tickets = [t for t in all_tickets if t.status not in (TicketStatus.RESUELTO, TicketStatus.CERRADO)]
    unassigned = [t for t in active_tickets if not t.assignee_username or t.status == TicketStatus.NUEVO]
    
    workload = {u.username: 0 for u in support_users}
    for t in active_tickets:
        if t.assignee_username in workload:
            workload[t.assignee_username] += 1
            
    reassigned_count = 0
    for t in unassigned:
        min_user = min(workload.keys(), key=lambda u: workload[u])
        t.assignee_username = min_user
        t.status = TicketStatus.ASIGNADO
        t.updated_at = datetime.utcnow()
        session.add(t)
        workload[min_user] += 1
        reassigned_count += 1
        session.add(TicketAuditLog(
            ticket_id=t.id,
            changed_by_username="torre_control",
            field_changed="assignee_username",
            old_value="Sin Asignar",
            new_value=min_user,
            change_reason="[Auto-Balanceo Algorítmico] Asignación equitativa por menor carga de guardia"
        ))

    if len(support_users) > 1:
        for _ in range(25):
            sorted_users = sorted(workload.keys(), key=lambda u: workload[u], reverse=True)
            max_user = sorted_users[0]
            min_user = sorted_users[-1]
            if workload[max_user] - workload[min_user] >= 2:
                candidate = next((t for t in active_tickets if t.assignee_username == max_user and t.priority != PriorityLevel.P1), None)
                if not candidate:
                    candidate = next((t for t in active_tickets if t.assignee_username == max_user), None)
                if candidate:
                    candidate.assignee_username = min_user
                    candidate.updated_at = datetime.utcnow()
                    session.add(candidate)
                    workload[max_user] -= 1
                    workload[min_user] += 1
                    reassigned_count += 1
                    session.add(TicketAuditLog(
                        ticket_id=candidate.id,
                        changed_by_username="torre_control",
                        field_changed="assignee_username",
                        old_value=max_user,
                        new_value=min_user,
                        change_reason=f"[Auto-Balanceo Algorítmico] Compensación de sobrecarga de @{max_user} hacia @{min_user}"
                    ))
            else:
                break

    session.commit()
    msg = f"Auto-balanceo completado: {reassigned_count} solicitudes reasignadas equitativamente entre los operadores de guardia." if reassigned_count > 0 else "La guardia ya se encuentra balanceada de forma óptima entre todos los analistas."
    return {
        "status": "success",
        "message": msg,
        "reassigned_count": reassigned_count
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
