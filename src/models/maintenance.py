from datetime import datetime as dt_type
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class Maintenance(Base):
    __tablename__ = "maint"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    datetime: Mapped[dt_type] = mapped_column(nullable=False)
    machineID: Mapped[int] = mapped_column(ForeignKey("machines.machineID"), nullable=False)
    comp: Mapped[str] = mapped_column(String(50), nullable=False) # ej: 'comp2'

    machine: Mapped["Machine"] = relationship()

    def __repr__(self):
        return f"<Maint(machine={self.machineID}, replaced='{self.comp}')>"