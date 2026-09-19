from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
from sqlmodel import Session, select

from app.services.file_bot import (
    save_uploaded_file, get_file_bot_status, UPLOAD_DIR, ALLOWED_EXTENSIONS
)
from app.db.session import get_session
from app.models.entities import TicketAttachment, Ticket

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    ticket_id: Optional[str] = Form(None),
    uploaded_by: Optional[str] = Form("solicitante"),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo inválido")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Extensión {ext} no permitida")
    content = await file.read()
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo supera el límite máximo de 20 MB")
    
    file_info = save_uploaded_file(content, file.filename)
    
    # Si viene asociado a un ticket, persistir en TicketAttachment y vincular
    if ticket_id:
        attachment_record = TicketAttachment(
            ticket_id=ticket_id,
            filename=file_info["original_name"],
            file_path=file_info["filename"],
            file_size_bytes=file_info["size_bytes"],
            content_type=file.content_type or "application/octet-stream",
            sha256_hash=file_info["sha256"],
            uploaded_by=uploaded_by or "solicitante",
            created_at=datetime.utcnow()
        )
        session.add(attachment_record)
        
        # Actualizar ticket si no tiene attachment_url
        ticket = session.get(Ticket, ticket_id)
        if ticket and not ticket.attachment_url:
            ticket.attachment_url = file_info["file_url"]
            session.add(ticket)
            
        session.commit()
        session.refresh(attachment_record)
        file_info["attachment_id"] = attachment_record.id
        
    return file_info

@router.get("/ticket/{ticket_id}")
def get_ticket_attachments(
    ticket_id: str,
    session: Session = Depends(get_session)
) -> List[Dict[str, Any]]:
    attachments = session.exec(
        select(TicketAttachment).where(TicketAttachment.ticket_id == ticket_id)
    ).all()
    return [
        {
            "id": a.id,
            "ticket_id": a.ticket_id,
            "filename": a.filename,
            "file_url": f"/api/v1/files/download/{a.file_path}",
            "file_size_bytes": a.file_size_bytes,
            "sha256": a.sha256_hash,
            "uploaded_by": a.uploaded_by,
            "created_at": a.created_at.isoformat()
        }
        for a in attachments
    ]

@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = UPLOAD_DIR / Path(filename).name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(path=str(file_path), filename=Path(filename).name)

@router.get("/bot/status")
def file_bot_status() -> Dict[str, Any]:
    return get_file_bot_status()
