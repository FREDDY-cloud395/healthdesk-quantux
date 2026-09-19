from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from app.db.session import get_session
from app.models.entities import SoftwareRelease, ReleaseStatus, Ticket, TicketStatus, TicketAuditLog, SupportLevel

router = APIRouter()

class ReleaseCreateRequest(BaseModel):
    tag: str
    name: str
    notes: Optional[str] = None
    created_by: str = "admin"

class ReleaseDeployRequest(BaseModel):
    deployed_by: str = "admin"
    resolution_notes: Optional[str] = None

class ReleaseStatusUpdateRequest(BaseModel):
    status: ReleaseStatus
    updated_by: str = "admin"

class LinkTicketReleaseRequest(BaseModel):
    ticket_id: str
    release_tag: str
    action_by: str = "admin"

@router.get("", response_model=List[dict])
def list_releases(session: Session = Depends(get_session)):
    releases = session.exec(select(SoftwareRelease).order_by(SoftwareRelease.created_at.desc())).all()
    results = []
    for rel in releases:
        linked_tickets = session.exec(
            select(Ticket).where(Ticket.release_tag == rel.tag)
        ).all()
        results.append({
            "id": rel.id,
            "tag": rel.tag,
            "name": rel.name,
            "status": rel.status.value if hasattr(rel.status, "value") else str(rel.status),
            "notes": rel.notes,
            "created_by": rel.created_by,
            "deployed_at": rel.deployed_at,
            "created_at": rel.created_at,
            "linked_tickets_count": len(linked_tickets),
            "linked_tickets": [{"id": t.id, "title": t.title, "priority": t.priority.value if hasattr(t.priority, "value") else str(t.priority), "status": t.status.value if hasattr(t.status, "value") else str(t.status)} for t in linked_tickets]
        })
    return results

@router.post("", response_model=SoftwareRelease)
def create_release(req: ReleaseCreateRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(SoftwareRelease).where(SoftwareRelease.tag == req.tag.strip())).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"La versión {req.tag} ya se encuentra registrada.")
    
    release = SoftwareRelease(
        tag=req.tag.strip(),
        name=req.name.strip(),
        notes=req.notes,
        created_by=req.created_by,
        status=ReleaseStatus.PLANIFICADA,
        created_at=datetime.utcnow()
    )
    session.add(release)
    session.commit()
    session.refresh(release)
    return release

@router.patch("/{tag}/status")
def update_release_status(tag: str, req: ReleaseStatusUpdateRequest, session: Session = Depends(get_session)):
    release = session.exec(select(SoftwareRelease).where(SoftwareRelease.tag == tag)).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release no encontrada.")
    release.status = req.status
    session.add(release)
    session.commit()
    session.refresh(release)
    return {"status": "success", "tag": tag, "new_status": release.status.value if hasattr(release.status, "value") else str(release.status)}

@router.post("/link-ticket")
def link_ticket_to_release(req: LinkTicketReleaseRequest, session: Session = Depends(get_session)):
    ticket = session.exec(select(Ticket).where(Ticket.id == req.ticket_id)).first()
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {req.ticket_id} no encontrado.")
    
    release = session.exec(select(SoftwareRelease).where(SoftwareRelease.tag == req.release_tag)).first()
    if not release:
        raise HTTPException(status_code=404, detail=f"Release {req.release_tag} no encontrada.")
        
    old_tag = ticket.release_tag
    ticket.release_tag = req.release_tag
    ticket.support_level = SupportLevel.N3
    session.add(ticket)
    session.add(TicketAuditLog(
        ticket_id=ticket.id,
        changed_by_username=req.action_by,
        field_changed="release_tag",
        old_value=old_tag,
        new_value=req.release_tag,
        change_reason=f"Escalado a Desarrollo N3 y vinculado a tarjeta en tablero Kanban ({req.release_tag})"
    ))
    session.commit()
    session.refresh(ticket)
    return {"status": "success", "ticket_id": ticket.id, "release_tag": req.release_tag}

@router.post("/{tag}/deploy")
def deploy_release(tag: str, req: ReleaseDeployRequest, session: Session = Depends(get_session)):
    release = session.exec(select(SoftwareRelease).where(SoftwareRelease.tag == tag)).first()
    if not release:
        raise HTTPException(status_code=404, detail="Release no encontrada.")
    
    release.status = ReleaseStatus.DESPLEGADA
    release.deployed_at = datetime.utcnow()
    session.add(release)
    
    # Cascada de resolución a todos los tickets vinculados a este release
    linked_tickets = session.exec(
        select(Ticket).where(
            Ticket.release_tag == tag,
            Ticket.status != TicketStatus.RESUELTO,
            Ticket.status != TicketStatus.CERRADO
        )
    ).all()
    
    resolved_count = 0
    cascade_children_count = 0
    res_text = req.resolution_notes or f"Desplegado a Producción en Release {release.tag} ({release.name})"
    
    for t in linked_tickets:
        old_status = t.status.value if hasattr(t.status, "value") else str(t.status)
        t.status = TicketStatus.CERRADO
        t.resolved_at = t.resolved_at or datetime.utcnow()
        t.closed_at = datetime.utcnow()
        t.resolved_by = req.deployed_by
        t.resolution_notes = res_text
        session.add(t)
        
        session.add(TicketAuditLog(
            ticket_id=t.id,
            changed_by_username=req.deployed_by,
            field_changed="status",
            old_value=old_status,
            new_value="CERRADO",
            change_reason=f"Cierre definitivo por despliegue de Fix N3 en Release {release.tag} ({release.name})"
        ))
        resolved_count += 1

        # Cascada a todos los tickets secundarios o relacionados (parent_ticket_id == t.id)
        children = session.exec(
            select(Ticket).where(
                Ticket.parent_ticket_id == t.id,
                Ticket.status != TicketStatus.CERRADO
            )
        ).all()
        for child in children:
            old_child_status = child.status.value if hasattr(child.status, "value") else str(child.status)
            child.status = TicketStatus.CERRADO
            child.resolved_at = child.resolved_at or datetime.utcnow()
            child.closed_at = datetime.utcnow()
            child.resolved_by = req.deployed_by
            child.resolution_notes = f"Cerrado en cascada por despliegue de Fix N3 en solicitud principal #{t.id} (Release {release.tag})"
            session.add(child)
            session.add(TicketAuditLog(
                ticket_id=child.id,
                changed_by_username=req.deployed_by,
                field_changed="status",
                old_value=old_child_status,
                new_value="CERRADO",
                change_reason=f"Cierre en cascada por despliegue de Fix N3 en incidente padre #{t.id} (Release {release.tag})"
            ))
            cascade_children_count += 1
        
    session.commit()

    # Enviar alerta/aviso de que la incidencia fue solucionada a todos los involucrados
    try:
        from app.services.email_service import notify_ticket_closed
        for t in linked_tickets:
            notify_ticket_closed(t, conformity_feedback=f"Solución definitiva implementada por N3 en Release {release.tag}", closed_by_username=req.deployed_by)
    except Exception as e:
        print(f"Error al despachar alertas de cierre N3: {e}")
    session.refresh(release)
    total_resolved = resolved_count + cascade_children_count
    return {
        "status": "success",
        "message": f"Release {tag} desplegada con éxito. Se resolvieron {resolved_count} solicitudes directas y {cascade_children_count} secundarias en cascada ({total_resolved} total).",
        "release": release,
        "resolved_tickets_count": resolved_count,
        "cascade_children_count": cascade_children_count,
        "total_resolved": total_resolved
    }

