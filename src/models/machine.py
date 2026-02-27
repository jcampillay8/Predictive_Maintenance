from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base

class Machine(Base):
    __tablename__ = "machines"

    machineID: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

    # Relación inversa para acceder a la telemetría desde la máquina
    telemetries: Mapped[list["Telemetry"]] = relationship(back_populates="machine", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Machine(id={self.machineID}, model='{self.model}')>"