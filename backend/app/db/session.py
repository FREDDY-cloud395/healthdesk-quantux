import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, text, select

DB_PATH = Path(__file__).resolve().parent.parent.parent / "healthdesk.db"
DATABASE_URL = os.getenv("DATABASE_URL")

from sqlalchemy import event

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
else:
    SQLITE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False, "timeout": 60.0},
        echo=False
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA busy_timeout=60000;")
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()
        except Exception:
            pass

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for col_def in [
            "ALTER TABLE users ADD COLUMN support_level TEXT",
            "ALTER TABLE tickets ADD COLUMN support_level TEXT DEFAULT 'N1'",
            "ALTER TABLE tickets ADD COLUMN attachment_url TEXT",
            "ALTER TABLE kb_articles ADD COLUMN version TEXT DEFAULT 'v1.0'",
            "ALTER TABLE kb_articles ADD COLUMN changelog TEXT DEFAULT 'Versión inicial homologada'",
            "ALTER TABLE kb_articles ADD COLUMN view_count INTEGER DEFAULT 0",
            "ALTER TABLE kb_articles ADD COLUMN source_ticket_id TEXT",
            "ALTER TABLE tickets ADD COLUMN parent_ticket_id TEXT",
            "ALTER TABLE tickets ADD COLUMN is_major_incident INTEGER DEFAULT 0",
            "ALTER TABLE tickets ADD COLUMN release_tag TEXT",
            "ALTER TABLE tickets ADD COLUMN resolved_by TEXT",
            "ALTER TABLE tickets ADD COLUMN closed_by TEXT",
            "ALTER TABLE tickets ADD COLUMN rating_stars INTEGER",
            "ALTER TABLE tickets ADD COLUMN rating_kudos TEXT",
            "ALTER TABLE tickets ADD COLUMN rating_feedback TEXT",
            "ALTER TABLE tickets ADD COLUMN requires_service_recovery INTEGER DEFAULT 0",
            "ALTER TABLE tickets ADD COLUMN telemetry_data TEXT",
            "ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1",
            "ALTER TABLE users ADD COLUMN groups TEXT DEFAULT 'mesa-de-ayuda'",
            "ALTER TABLE users ADD COLUMN product_access TEXT DEFAULT 'Mesa de Ayuda'",
            "ALTER TABLE users ADD COLUMN institution_code TEXT",
            "ALTER TABLE users ADD COLUMN assigned_institutions TEXT DEFAULT 'ALL'",
            "ALTER TABLE users ADD COLUMN phone TEXT",
            "ALTER TABLE kb_articles ADD COLUMN requests_deflected INTEGER DEFAULT 0",
            "ALTER TABLE kb_articles ADD COLUMN helpful_score INTEGER DEFAULT 95",
            "ALTER TABLE kb_articles ADD COLUMN space_name TEXT DEFAULT 'Guías y Documentación de Soporte Asistencial'",
            "ALTER TABLE tickets ADD COLUMN channel TEXT DEFAULT 'PORTAL'",
            "ALTER TABLE tickets ADD COLUMN is_ia_resolved INTEGER DEFAULT 0",
            "ALTER TABLE tickets ADD COLUMN ia_feedback TEXT",
            "ALTER TABLE tickets ADD COLUMN git_branch TEXT",
            "ALTER TABLE tickets ADD COLUMN git_pr TEXT",
            "ALTER TABLE tickets ADD COLUMN git_commit TEXT"
        ]:
            try:
                session.exec(text(col_def))
                session.commit()
            except Exception:
                pass
        try:
            session.exec(text("UPDATE users SET is_active = 1 WHERE is_active IS NULL"))
            session.exec(text("UPDATE users SET groups = 'jira-admins, soporte-n3' WHERE role = 'ADMIN' AND (groups IS NULL OR groups = 'mesa-de-ayuda')"))
            session.exec(text("UPDATE users SET groups = 'soporte-n1, guardia-asistencial' WHERE role = 'SOPORTE' AND support_level = 'N1' AND (groups IS NULL OR groups = 'mesa-de-ayuda')"))
            session.exec(text("UPDATE users SET groups = 'especialistas-n2, clinica-osde' WHERE role = 'SOPORTE' AND support_level = 'N2' AND (groups IS NULL OR groups = 'mesa-de-ayuda')"))
            session.exec(text("UPDATE users SET groups = 'infraestructura-n3, devops-core' WHERE role = 'SOPORTE' AND support_level = 'N3' AND (groups IS NULL OR groups = 'mesa-de-ayuda')"))
            session.exec(text("UPDATE users SET groups = 'jefatura-guardia, aprobadores-it' WHERE role = 'TEAM_LEADER' AND (groups IS NULL OR groups = 'mesa-de-ayuda')"))
            session.exec(text("UPDATE users SET groups = 'medicos-asistenciales, sol-portal' WHERE role = 'SOLICITANTE' AND (groups IS NULL OR groups = 'mesa-de-ayuda')"))
            session.exec(text("UPDATE users SET product_access = 'Mesa de Ayuda, Receta Digital, Telemedicina, HCE Clínico' WHERE role IN ('ADMIN', 'TEAM_LEADER')"))
            session.exec(text("UPDATE users SET product_access = 'Mesa de Ayuda, Base de Conocimiento' WHERE role = 'SOPORTE' AND (product_access IS NULL OR product_access = 'Mesa de Ayuda')"))
            session.exec(text("UPDATE users SET product_access = 'Portal Paciente, Consultorio Digital' WHERE role = 'SOLICITANTE' AND (product_access IS NULL OR product_access = 'Mesa de Ayuda')"))
            session.exec(text("UPDATE kb_articles SET space_name = 'Guías y Documentación de Soporte Asistencial' WHERE space_name IS NULL"))
            session.exec(text("UPDATE kb_articles SET requests_deflected = CAST((view_count * 0.45) AS INTEGER) WHERE requests_deflected IS NULL OR requests_deflected = 0"))
            session.exec(text("UPDATE kb_articles SET helpful_score = 94 WHERE helpful_score IS NULL OR helpful_score = 0"))
            session.commit()
        except Exception:
            pass
        try:
            session.exec(text("UPDATE users SET email = 'fcortes@quantuxsalud.com' WHERE username = 'admin' OR full_name LIKE '%Freddy%'"))
            session.commit()
        except Exception:
            pass
        try:
            from app.models.entities import User, UserRole, SupportLevel
            tl = session.exec(select(User).where(User.username == "teamleader")).first()
            if not tl:
                session.add(User(
                    username="teamleader",
                    full_name="Carla Daneri",
                    email="cdaneri@quantux.com",
                    role=UserRole.TEAM_LEADER,
                    support_level=SupportLevel.N2
                ))
                session.commit()
        except Exception:
            pass

        # Creación estratégica de índices para optimización de alto rendimiento
        for idx_def in [
            "CREATE INDEX IF NOT EXISTS ix_tickets_created_at ON tickets(created_at DESC)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_assignee_username ON tickets(assignee_username)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_assignee_status ON tickets(assignee_username, status)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_requester_username ON tickets(requester_username)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_priority_status ON tickets(priority, status)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_status_created_at ON tickets(status, created_at DESC)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_parent_ticket_id ON tickets(parent_ticket_id)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_resolved_at ON tickets(resolved_at)",
            "CREATE INDEX IF NOT EXISTS ix_tickets_release_tag ON tickets(release_tag)",
            "CREATE INDEX IF NOT EXISTS ix_ticket_audit_log_ticket_created ON ticket_audit_log(ticket_id, created_at ASC)",
            "CREATE INDEX IF NOT EXISTS ix_ticket_audit_log_changed_by ON ticket_audit_log(changed_by_username)",
            "CREATE INDEX IF NOT EXISTS ix_ticket_comments_ticket_created ON ticket_comments(ticket_id, created_at ASC)",
            "CREATE INDEX IF NOT EXISTS ix_email_logs_ticket_created ON email_notification_logs(ticket_id, created_at DESC)",
            "CREATE INDEX IF NOT EXISTS ix_email_logs_sent_status ON email_notification_logs(sent_status)",
            "CREATE INDEX IF NOT EXISTS ix_users_role_is_active ON users(role, is_active)"
        ]:
            try:
                session.exec(text(idx_def))
                session.commit()
            except Exception:
                pass

def get_session():
    with Session(engine) as session:
        yield session
