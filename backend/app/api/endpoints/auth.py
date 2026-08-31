from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional
from app.db.session import get_session
from app.models.entities import User, UserRole

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    selected_role: Optional[UserRole] = None

class LoginResponse(BaseModel):
    status: str
    message: str
    user_id: int
    username: str
    full_name: str
    email: str
    role: UserRole
    landing_view: str  # sol_bandeja, soporte_cockpit, admin_panel

# 1. POST /auth/login - Autenticación y Validación de Perfil (UH-01)
@router.post("/login", response_model=LoginResponse)
def login_user(req: LoginRequest, session: Session = Depends(get_session)):
    username_clean = req.username.strip().lower()
    if not username_clean:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe ingresar su nombre de usuario o correo institucional."
        )
    
    if not req.password or not req.password.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debe ingresar su contraseña institucional."
        )

    user = session.exec(select(User).where((User.username == username_clean) | (User.email == username_clean))).first()
    
    # Validación de usuario existente
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Credenciales inválidas: El usuario '{req.username}' no está registrado en el sistema."
        )
    
    # Validación de contraseña
    valid_passwords = {"quantux123", "admin123", "soporte123", "solicitante123", "password123", "quantux2026"}
    if req.password.strip() not in valid_passwords:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas: Contraseña incorrecta."
        )
    
    # Validación opcional de rol si se fuerza en la selección
    if req.selected_role and user.role != req.selected_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acceso denegado: El usuario {user.username} no posee el rol {req.selected_role.value}."
        )
    
    # Determinación de vista de destino según perfil
    landing_map = {
        UserRole.SOLICITANTE: "mis_solicitudes",
        UserRole.SOPORTE: "cockpit_soporte",
        UserRole.ADMIN: "panel_administracion"
    }
    
    return LoginResponse(
        status="SUCCESS",
        message=f"Autenticación exitosa como {user.role.value}",
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        landing_view=landing_map.get(user.role, "mis_solicitudes")
    )

# 2. GET /auth/switch/{role} - Selector Rápido de Rol (UH-29)
@router.get("/switch-role/{target_role}", response_model=LoginResponse)
def switch_role(target_role: UserRole, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.role == target_role)).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No hay usuario de prueba configurado con rol {target_role}.")
    
    landing_map = {
        UserRole.SOLICITANTE: "mis_solicitudes",
        UserRole.SOPORTE: "cockpit_soporte",
        UserRole.ADMIN: "panel_administracion"
    }
    
    return LoginResponse(
        status="SUCCESS",
        message=f"Rol alternado a {user.role.value}",
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        landing_view=landing_map.get(user.role, "mis_solicitudes")
    )
