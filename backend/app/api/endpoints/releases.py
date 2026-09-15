from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from app.db.session import get_session
from app.models.entities import SoftwareRelease, ReleaseStatus, Ticket, TicketStatus, TicketAuditLog

router = APIRouter()

class ReleaseCreateRequest(BaseModel):
    tag: str
    name: str
    notes: Optional[str] = None
    created_by: str = "admin"

class ReleaseDeployRequest(BaseModel):
    deployed_by: str = "admin"
    resolution_notes: Optional[str] = None

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
            "linked_tickets": [{"id": t.id, "title": t.title, "status": t.status.value if hasattr(t.status, "value") else str(t.status)} for t in linked_tickets]
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
    res_text = req.resolution_notes or f"Desplegado a Producción en Release {release.tag} ({release.name})"
    
    for t in linked_tickets:
        old_status = t.status.value if hasattr(t.status, "value") else str(t.status)
        t.status = TicketStatus.RESUELTO
        t.resolved_at = datetime.utcnow()
        t.resolved_by = req.deployed_by
        t.resolution_notes = res_text
        session.add(t)
        
        session.add(TicketAuditLog(
            ticket_id=t.id,
            changed_by_username=req.deployed_by,
            field_changed="status",
            old_value=old_status,
            new_value="RESUELTO",
            change_reason=f"Resolución automática en despliegue de Release {release.tag}"
        ))
        resolved_count += 1
        
    session.commit()
    session.refresh(release)
    return {
        "status": "success",
        "message": f"Release {tag} desplegada con éxito. Se resolvieron automáticamente {resolved_count} solicitudes vinculadas.",
        "release": release,
        "resolved_tickets_count": resolved_count
    }
