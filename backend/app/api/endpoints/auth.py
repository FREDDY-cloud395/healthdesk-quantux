from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Optional
from app.db.session import get_session
from app.models.entities import User, UserRole

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: Optional[str] = "quantux123"
    selected_role: Optional[UserRole] = None

class LoginResponse(BaseModel):
    status: str
    message: str
    user_id: int
    username: str
    full_name: str
    email: str
    role: UserRole
    landing_view: str  # mis_solicitudes, cockpit_soporte, torre_control, panel_administracion
    iam_provider: str = "Quantux-IAM-Enterprise"
    permissions: list[str] = []

ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        "iam:manage_users",
        "iam:assign_roles",
        "catalog:manage_institutions",
        "catalog:manage_platforms",
        "releases:deploy",
        "audit:export",
        "team_leader:access",
        "team_leader:reassign",
        "team_leader:rescue",
        "tickets:view_all",
        "tickets:resolve",
        "tickets:close",
        "tickets:create",
        "kb:manage"
    ],
    UserRole.TEAM_LEADER: [
        "team_leader:access",
        "team_leader:reassign",
        "team_leader:rescue",
        "tickets:view_all",
        "tickets:resolve",
        "tickets:create",
        "kb:view",
        "metrics:view"
    ],
    UserRole.SOPORTE: [
        "tickets:view_all",
        "tickets:work",
        "tickets:internal_notes",
        "tickets:escalate",
        "tickets:resolve",
        "kb:view",
        "metrics:view"
    ],
    UserRole.SOLICITANTE: [
        "tickets:create",
        "tickets:view_own",
        "tickets:reply",
        "tickets:close",
        "csat:rate",
        "kb:view"
    ]
}

# 1. POST /auth/login - Autenticación y Validación de Perfil (UH-01)
@router.post("/login", response_model=LoginResponse)
def login_user(req: LoginRequest, session: Session = Depends(get_session)):
    username_clean = req.username.strip().lower()
    if not username_clean:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe ingresar su nombre de usuario o correo institucional."
        )
    
    pwd = (req.password if req.password is not None else "quantux123").strip()
    if not pwd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debe ingresar su contraseña institucional."
        )

    alias_map = {
        "n1": "cpaez",
        "n2": "soporte",
        "n3": "dnavarro",
        "tl": "teamleader",
        "medico": "solicitante"
    }
    lookup_user = alias_map.get(username_clean, username_clean)
    user = session.exec(select(User).where((User.username == lookup_user) | (User.email == lookup_user))).first()
    
    # Validación de usuario existente
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Credenciales inválidas: El usuario '{req.username}' no está registrado en el sistema."
        )
    
    # Validación de contraseña
    valid_passwords = {"quantux123", "admin123", "soporte123", "solicitante123", "password123", "quantux2026", "demo123"}
    if pwd not in valid_passwords:
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
        UserRole.TEAM_LEADER: "torre_control",
        UserRole.ADMIN: "panel_administracion"
    }
    
    return LoginResponse(
        status="SUCCESS",
        message=f"Autenticación exitosa vía Quantux IAM como {user.role.value}",
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        landing_view=landing_map.get(user.role, "mis_solicitudes"),
        iam_provider="Quantux-IAM-Enterprise",
        permissions=ROLE_PERMISSIONS.get(user.role, [])
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
        UserRole.TEAM_LEADER: "torre_control",
        UserRole.ADMIN: "panel_administracion"
    }
    
    return LoginResponse(
        status="SUCCESS",
        message=f"Rol alternado vía Quantux IAM a {user.role.value}",
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        landing_view=landing_map.get(user.role, "mis_solicitudes"),
        iam_provider="Quantux-IAM-Enterprise",
        permissions=ROLE_PERMISSIONS.get(user.role, [])
    )
