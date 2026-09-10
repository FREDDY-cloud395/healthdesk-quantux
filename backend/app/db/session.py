from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session, text

DB_PATH = Path(__file__).resolve().parent.parent.parent / "healthdesk.db"
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
            "ALTER TABLE kb_articles ADD COLUMN source_ticket_id TEXT"
        ]:
            try:
                session.exec(text(col_def))
                session.commit()
            except Exception:
                pass

def get_session():
    with Session(engine) as session:
        yield session
