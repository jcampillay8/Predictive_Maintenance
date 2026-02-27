from datetime import datetime as dt_type
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class Error(Base):
    __tablename__ = "errors"

    # Usamos un ID autoincremental para errores ya que no hay una PK clara en el CSV
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    datetime: Mapped[dt_type] = mapped_column(nullable=False)
    machineID: Mapped[int] = mapped_column(ForeignKey("machines.machineID"), nullable=False)
    errorID: Mapped[str] = mapped_column(String(50), nullable=False) # ej: 'error1'

    machine: Mapped["Machine"] = relationship()

    def __repr__(self):
        return f"<Error(machine={self.machineID}, type='{self.errorID}')>"