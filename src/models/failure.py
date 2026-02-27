from datetime import datetime as dt_type
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class Failure(Base):
    __tablename__ = "failures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    datetime: Mapped[dt_type] = mapped_column(nullable=False)
    machineID: Mapped[int] = mapped_column(ForeignKey("machines.machineID"), nullable=False)
    failure: Mapped[str] = mapped_column(String(50), nullable=False) # ej: 'comp1'

    machine: Mapped["Machine"] = relationship()

    def __repr__(self):
        return f"<Failure(machine={self.machineID}, component='{self.failure}')>"