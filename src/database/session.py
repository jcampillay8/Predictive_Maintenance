# src/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Engine configurado para alta disponibilidad
# Eliminamos connect_args para compatibilidad con Neon/PgBouncer Pooler
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20
)

# El esquema se manejará automáticamente a través de Base.metadata
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency para FastAPI que provee una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()