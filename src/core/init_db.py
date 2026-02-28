# src/core/init_db.py
from src.database.session import engine
from src.database.base import Base # Asegúrate de importar tu Base con todos los modelos registrados
from src.models.machine import Machine
from src.models.telemetry import Telemetry
from src.models.error import Error
from src.models.failure import Failure
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info("🚀 Creando tablas en la base de datos remota...")
    try:
        # Esto creará todas las tablas que hereden de Base en el esquema especificado
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente.")
    except Exception as e:
        logger.error(f"❌ Error al crear las tablas: {e}")

if __name__ == "__main__":
    init_database()