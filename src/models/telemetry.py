# src/models/telemetry.py
from datetime import datetime as dt_type
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class Telemetry(Base):
    __tablename__ = "telemetry"

    datetime: Mapped[dt_type] = mapped_column(nullable=False)
    machineID: Mapped[int] = mapped_column(ForeignKey("machines.machineID"), nullable=False)
    volt: Mapped[float] = mapped_column(nullable=True)
    rotate: Mapped[float] = mapped_column(nullable=True)
    pressure: Mapped[float] = mapped_column(nullable=True)
    vibration: Mapped[float] = mapped_column(nullable=True)

    # Clave primaria compuesta (importante para series temporales)
    __table_args__ = (
        PrimaryKeyConstraint("datetime", "machineID"),
    )

    # Relación con el padre
    machine: Mapped["Machine"] = relationship(back_populates="telemetries")

    def __repr__(self) -> str:
        return f"<Telemetry(machine={self.machineID}, time={self.datetime})>"