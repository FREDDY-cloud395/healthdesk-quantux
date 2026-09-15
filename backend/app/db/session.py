import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, text

DB_PATH = Path(__file__).resolve().parent.parent.parent / "healthdesk.db"
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
else:
    SQLITE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

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
            "ALTER TABLE tickets ADD COLUMN telemetry_data TEXT"
        ]:
            try:
                session.exec(text(col_def))
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

def get_session():
    with Session(engine) as session:
        yield session
