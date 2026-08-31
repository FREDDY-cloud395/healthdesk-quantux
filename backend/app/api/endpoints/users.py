from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.db.session import get_session
from app.models.entities import User, UserRole

router = APIRouter()

class UserCreateRequest(BaseModel):
    username: str
    full_name: str
    email: str
    role: UserRole = UserRole.SOLICITANTE

@router.get("", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@router.get("/operators", response_model=List[User])
def list_support_operators(session: Session = Depends(get_session)):
    return session.exec(select(User).where((User.role == UserRole.SOPORTE) | (User.role == UserRole.ADMIN))).all()

@router.post("", response_model=User)
def create_user(req: UserCreateRequest, session: Session = Depends(get_session)):
    # Validar si el username ya existe
    existing = session.exec(select(User).where(User.username == req.username.strip().lower())).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"El nombre de usuario '{req.username}' ya está registrado.")
    
    # Validar longitud mínima
    if len(req.username.strip()) < 3:
        raise HTTPException(status_code=400, detail="El nombre de usuario debe tener al menos 3 caracteres.")
    
    if len(req.full_name.strip()) < 3:
        raise HTTPException(status_code=400, detail="El nombre completo debe tener al menos 3 caracteres.")
    
    new_user = User(
        username=req.username.strip().lower(),
        full_name=req.full_name.strip(),
        email=req.email.strip().lower(),
        role=req.role,
        created_at=datetime.utcnow()
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
