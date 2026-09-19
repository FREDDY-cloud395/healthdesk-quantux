from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.db.session import get_session
from app.models.entities import User, UserRole, SupportLevel

router = APIRouter()

class UserCreateRequest(BaseModel):
    username: str
    full_name: str
    email: str
    role: UserRole = UserRole.SOLICITANTE
    support_level: Optional[SupportLevel] = None
    is_active: bool = True
    groups: Optional[str] = "mesa-de-ayuda"
    product_access: Optional[str] = "Mesa de Ayuda"
    institution_code: Optional[str] = None
    assigned_institutions: Optional[str] = "ALL"
    phone: Optional[str] = None

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    support_level: Optional[SupportLevel] = None
    is_active: Optional[bool] = None
    groups: Optional[str] = None
    product_access: Optional[str] = None
    institution_code: Optional[str] = None
    assigned_institutions: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

@router.get("", response_model=List[User])
def list_users(
    role: Optional[UserRole] = None,
    support_level: Optional[SupportLevel] = None,
    session: Session = Depends(get_session)
):
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if support_level:
        query = query.where(User.support_level == support_level)
    return session.exec(query).all()

@router.get("/operators", response_model=List[User])
def list_support_operators(
    level: Optional[SupportLevel] = None,
    session: Session = Depends(get_session)
):
    query = select(User).where((User.role == UserRole.SOPORTE) | (User.role == UserRole.ADMIN))
    if level:
        query = query.where(User.support_level == level)
    return session.exec(query).all()

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user

@router.put("/{user_id}", response_model=User)
@router.patch("/{user_id}", response_model=User)
def update_user(user_id: int, req: UserUpdateRequest, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    if req.full_name is not None and len(req.full_name.strip()) >= 3:
        user.full_name = req.full_name.strip()
    if req.email is not None and len(req.email.strip()) >= 5:
        user.email = req.email.strip().lower()
    if req.role is not None:
        user.role = req.role
    if req.support_level is not None:
        user.support_level = req.support_level
    if req.is_active is not None:
        user.is_active = req.is_active
    if req.groups is not None:
        user.groups = req.groups
    if req.product_access is not None:
        user.product_access = req.product_access
    if req.institution_code is not None:
        user.institution_code = req.institution_code.strip() if req.institution_code else None
    if req.assigned_institutions is not None:
        user.assigned_institutions = req.assigned_institutions.strip() if req.assigned_institutions else "ALL"
    if req.phone is not None:
        user.phone = req.phone.strip() if req.phone else None
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/by-username/{username}", response_model=User)
@router.patch("/by-username/{username}", response_model=User)
def update_user_by_username(username: str, req: UserUpdateRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username.strip().lower())).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario '{username}' no encontrado.")
    
    if req.full_name is not None and len(req.full_name.strip()) >= 3:
        user.full_name = req.full_name.strip()
    if req.email is not None and len(req.email.strip()) >= 5:
        user.email = req.email.strip().lower()
    if req.role is not None:
        user.role = req.role
    if req.support_level is not None:
        user.support_level = req.support_level
    if req.is_active is not None:
        user.is_active = req.is_active
    if req.groups is not None:
        user.groups = req.groups
    if req.product_access is not None:
        user.product_access = req.product_access
    if req.institution_code is not None:
        user.institution_code = req.institution_code.strip() if req.institution_code else None
    if req.assigned_institutions is not None:
        user.assigned_institutions = req.assigned_institutions.strip() if req.assigned_institutions else "ALL"
    if req.phone is not None:
        user.phone = req.phone.strip() if req.phone else None
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.patch("/{user_id}/toggle-status", response_model=User)
def toggle_user_status(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    user.is_active = not user.is_active
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

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
    
    # Asignar nivel por defecto según rol
    lvl = req.support_level
    if not lvl and req.role == UserRole.SOPORTE:
        lvl = SupportLevel.N1
    elif not lvl and req.role == UserRole.ADMIN:
        lvl = SupportLevel.N3

    new_user = User(
        username=req.username.strip().lower(),
        full_name=req.full_name.strip(),
        email=req.email.strip().lower(),
        role=req.role,
        support_level=lvl,
        is_active=req.is_active,
        groups=req.groups or "mesa-de-ayuda",
        product_access=req.product_access or "Mesa de Ayuda",
        institution_code=req.institution_code.strip() if req.institution_code else None,
        assigned_institutions=req.assigned_institutions.strip() if req.assigned_institutions else "ALL",
        phone=req.phone.strip() if req.phone else None,
        created_at=datetime.utcnow()
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
