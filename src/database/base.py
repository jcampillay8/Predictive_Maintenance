# src/database/base.py
from datetime import datetime
from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.core.config import settings

# Forzamos a que todos los modelos usen el schema definido
metadata = MetaData(schema=settings.DB_SCHEMA)

class Base(DeclarativeBase):
    metadata = metadata
    
    # Campos de auditoría que siempre vienen bien
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )