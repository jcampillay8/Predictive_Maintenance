# src/services/ingestion.py
import logging
import polars as pl
from sqlalchemy.orm import Session

from src.core.config import settings
from src.database.session import engine, SessionLocal
from src.database.base import Base
from src.models.machine import Machine
from src.models.telemetry import Telemetry
from src.models.error import Error
from src.models.failure import Failure
from src.models.maintenance import Maintenance

# Configuración de logging para ver qué pasa en la terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Crea las tablas en la base de datos si no existen."""
    logger.info(f"🛠 Conectando a {settings.DB_HOST} para crear tablas...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas verificadas/creadas con éxito.")

def ingest_csv_to_db():
    """Proceso de ingesta optimizado."""
    db: Session = SessionLocal()
    
    try:
        # 1. Machines (Maestra)
        if not db.query(Machine).first():
            logger.info("🚀 Cargando Machines...")
            path = settings.DATA_PATH / "PdM_machines.csv"
            df_machines = pl.read_csv(path)
            db.bulk_insert_mappings(Machine, df_machines.to_dicts())
            db.commit()
            logger.info(f"✅ {df_machines.height} máquinas cargadas.")

        # 2. Telemetry (Carga por trozos para optimizar RAM)
        if not db.query(Telemetry).first():
            logger.info("🚀 Cargando Telemetría (871k registros)...")
            path = settings.DATA_PATH / "PdM_telemetry.csv"
            df_telemetry = pl.read_csv(path).with_columns(
                pl.col("datetime").str.to_datetime("%Y-%m-%d %H:%M:%S")
            )
            
            chunk_size = 100000
            for i in range(0, df_telemetry.height, chunk_size):
                chunk = df_telemetry.slice(i, chunk_size).to_dicts()
                db.bulk_insert_mappings(Telemetry, chunk)
                db.commit()
                logger.info(f"📦 Progress: {min(i + chunk_size, df_telemetry.height)} registros...")

        # 3. Resto de archivos (Errors, Failures, Maint)
        mapping = {
            "PdM_errors.csv": (Error, "Errores"),
            "PdM_failures.csv": (Failure, "Fallas"),
            "PdM_maint.csv": (Maintenance, "Mantenimiento")
        }

        for csv_file, (model, display_name) in mapping.items():
            if not db.query(model).first():
                logger.info(f"🚀 Cargando {display_name}...")
                path = settings.DATA_PATH / csv_file
                df = pl.read_csv(path).with_columns(
                    pl.col("datetime").str.to_datetime("%Y-%m-%d %H:%M:%S")
                )
                db.bulk_insert_mappings(model, df.to_dicts())
                db.commit()
                logger.info(f"✅ {display_name} cargado correctamente.")

    except Exception as e:
        logger.error(f"❌ Error crítico en la ingesta: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    ingest_csv_to_db()