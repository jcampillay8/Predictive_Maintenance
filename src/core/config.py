# src/core/config.py
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Configuración para que Pydantic lea el .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # El entorno se lee del .env o de Railway. Si no existe, lanza error (o usa dev)
    ENVIRONMENT: str 
    PROJECT_NAME: str

# Soporta una lista de strings separados por coma
    ALLOWED_ORIGINS: str
    WEBSITE_URL: str

    # Base de Datos (Estas son OBLIGATORIAS en Neon/Railway)
    # Al no ponerles un valor por defecto (como = None), 
    # la App fallará rápido si faltan, lo cual es mejor para debuguear.
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_SCHEMA: str = "maintenance"

    GEMINI_API_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        # Detectamos si estamos en producción para forzar el modo SSL de Neon
        ssl_mode = "?sslmode=require" if self.ENVIRONMENT == "production" else ""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}{ssl_mode}"

settings = Settings()