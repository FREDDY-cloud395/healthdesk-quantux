from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

# ENUMS
class UserRole(str, Enum):
    SOLICITANTE = "SOLICITANTE"
    SOPORTE = "SOPORTE"
    TEAM_LEADER = "TEAM_LEADER"
    ADMIN = "ADMIN"

class TicketStatus(str, Enum):
    NUEVO = "NUEVO"
    ASIGNADO = "ASIGNADO"
    EN_CURSO = "EN_CURSO"
    EN_ESPERA = "EN_ESPERA"
    RESUELTO = "RESUELTO"
    CERRADO = "CERRADO"

class TicketType(str, Enum):
    INCIDENTE = "INCIDENTE"
    REQUERIMIENTO = "REQUERIMIENTO"
    CONSULTA = "CONSULTA"
    CAMBIO = "CAMBIO"
    PROBLEMA = "PROBLEMA"
    INC = "INC"
    REQ = "REQ"
    CON = "CON"
    CHG = "CHG"
    PRB = "PRB"

class ImpactLevel(str, Enum):
    CRITICO = "CRITICO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"

class UrgencyLevel(str, Enum):
    CRITICA = "CRITICA"
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"
    CRITICO = "CRITICO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"

class PriorityLevel(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"

class SupportLevel(str, Enum):
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"

class ReleaseStatus(str, Enum):
    PLANIFICADA = "PLANIFICADA"
    EN_DESARROLLO = "EN_DESARROLLO"
    STAGING = "STAGING"
    DESPLEGADA = "DESPLEGADA"
    CANCELADA = "CANCELADA"

# MODELOS DE TABLAS
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    full_name: str
    email: str
    role: UserRole = Field(default=UserRole.SOLICITANTE, index=True)
    support_level: Optional[SupportLevel] = Field(default=None)
    is_active: bool = Field(default=True, index=True)
    groups: Optional[str] = Field(default="mesa-de-ayuda")
    product_access: Optional[str] = Field(default="Mesa de Ayuda")
    institution_code: Optional[str] = Field(default=None, nullable=True)
    assigned_institutions: Optional[str] = Field(default="ALL", nullable=True)
    phone: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Platform(SQLModel, table=True):
    __tablename__ = "platforms"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    name: str
    description: str
    is_active: bool = Field(default=True)

class Institution(SQLModel, table=True):
    __tablename__ = "institutions"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    name: str
    segment: str  # Financiador, Sanatorio, Internación Domiciliaria
    is_active: bool = Field(default=True)

class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"
    id: str = Field(primary_key=True, index=True)  # TICK-202608-0001
    title: str
    description: str
    platform_code: str = Field(foreign_key="platforms.code", index=True)
    institution_code: str = Field(foreign_key="institutions.code", index=True)
    ticket_type: TicketType = Field(default=TicketType.INCIDENTE)
    impact: ImpactLevel = Field(default=ImpactLevel.MEDIO)
    urgency: UrgencyLevel = Field(default=UrgencyLevel.MEDIO)
    priority: PriorityLevel = Field(default=PriorityLevel.P3, index=True)
    status: TicketStatus = Field(default=TicketStatus.NUEVO, index=True)
    requester_username: str = Field(foreign_key="users.username", index=True)
    assignee_username: Optional[str] = Field(default=None, foreign_key="users.username", nullable=True, index=True)
    support_level: SupportLevel = Field(default=SupportLevel.N1)
    attachment_url: Optional[str] = Field(default=None, nullable=True)
    resolution_notes: Optional[str] = Field(default=None, nullable=True)
    is_workaround: bool = Field(default=False)
    # v4.0.0 Mejoras: Incidentes Masivos & Releases
    parent_ticket_id: Optional[str] = Field(default=None, nullable=True, index=True)
    is_major_incident: bool = Field(default=False)
    release_tag: Optional[str] = Field(default=None, nullable=True, index=True)
    # v4.0.0 Mejoras: Cierre Exclusivo, CSAT y Service Recovery
    resolved_by: Optional[str] = Field(default=None, nullable=True)
    closed_by: Optional[str] = Field(default=None, nullable=True)
    rating_stars: Optional[int] = Field(default=None, nullable=True)
    rating_kudos: Optional[str] = Field(default=None, nullable=True)
    rating_feedback: Optional[str] = Field(default=None, nullable=True)
    requires_service_recovery: bool = Field(default=False)
    telemetry_data: Optional[str] = Field(default=None, nullable=True)  # JSON Zero-Question
    # v4.1.0 Mejoras: Trazabilidad Total Chat IA & Deflexión Asistencial
    channel: Optional[str] = Field(default="PORTAL", nullable=True)  # PORTAL, CHAT_IA, CORREO, MANUAL
    is_ia_resolved: bool = Field(default=False)
    ia_feedback: Optional[str] = Field(default=None, nullable=True)
    # v4.2.0 Ingeniería N3: Git & DevOps Metadata
    git_branch: Optional[str] = Field(default=None, nullable=True)
    git_pr: Optional[str] = Field(default=None, nullable=True)
    git_commit: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = Field(default=None, nullable=True, index=True)
    closed_at: Optional[datetime] = Field(default=None, nullable=True)

class SoftwareRelease(SQLModel, table=True):
    __tablename__ = "software_releases"
    id: Optional[int] = Field(default=None, primary_key=True)
    tag: str = Field(unique=True, index=True)  # e.g. "v4.0.0", "v4.1.0"
    name: str  # e.g. "Actualización de Seguridad y Pasarelas"
    status: ReleaseStatus = Field(default=ReleaseStatus.PLANIFICADA)
    notes: Optional[str] = None
    created_by: str = Field(default="admin")
    deployed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TicketComment(SQLModel, table=True):
    __tablename__ = "ticket_comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(foreign_key="tickets.id", index=True)
    author_username: str = Field(foreign_key="users.username")
    message: str
    is_internal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TicketAuditLog(SQLModel, table=True):
    __tablename__ = "ticket_audit_log"
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(foreign_key="tickets.id", index=True)
    changed_by_username: str = Field(foreign_key="users.username", index=True)
    field_changed: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    change_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

class EmailNotificationLog(SQLModel, table=True):
    __tablename__ = "email_notification_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(foreign_key="tickets.id", index=True)
    recipient_email: str
    recipient_role: str
    subject: str
    event_type: str  # TICKET_CREATED, TICKET_ASSIGNED, STATUS_CHANGED, TICKET_RESOLVED, TICKET_CLOSED, P1_ALERT, COMMENT_ADDED
    body_html: str
    sent_status: str = Field(default="SENT", index=True)  # SENT | SIMULATED | FAILED
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

class KBArticle(SQLModel, table=True):
    __tablename__ = "kb_articles"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str = Field(default="General", index=True)
    content: str
    author_username: str = Field(default="admin")
    tags: Optional[str] = None
    version: str = Field(default="v1.0")
    changelog: Optional[str] = Field(default="Versión inicial homologada")
    view_count: int = Field(default=0)
    requests_deflected: int = Field(default=0)
    helpful_score: int = Field(default=95)
    space_name: Optional[str] = Field(default="Guías Asistenciales")
    source_ticket_id: Optional[str] = Field(default=None, nullable=True)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class KBArticleHistory(SQLModel, table=True):
    __tablename__ = "kb_article_history"
    id: Optional[int] = Field(default=None, primary_key=True)
    article_id: int = Field(foreign_key="kb_articles.id", index=True)
    version: str = Field(default="v1.0")
    title: str
    category: str
    content: str
    author_username: str
    tags: Optional[str] = None
    changelog: str = Field(default="Actualización de contenido")
    source_ticket_id: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TicketAttachment(SQLModel, table=True):
    __tablename__ = "ticket_attachments"
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(foreign_key="tickets.id", index=True)
    filename: str
    file_path: str
    file_size_bytes: int
    content_type: str
    sha256_hash: str
    uploaded_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TicketChatMessage(SQLModel, table=True):
    __tablename__ = "ticket_chat_messages"
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(foreign_key="tickets.id", index=True)
    sender_username: str
    sender_role: str  # N1, SOLICITANTE, N2, SYSTEM
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

