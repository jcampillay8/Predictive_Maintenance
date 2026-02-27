import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Detectamos la raíz del proyecto: 
# __file__ es src/core/config.py -> .parent es src/core -> .parent es src -> .parent es Raíz
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Predictive Maintenance"

    # Rutas de Archivos
    DATA_PATH: Path = BASE_DIR / "Data"

    # Base de Datos
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_SCHEMA: str = "maintenance"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()