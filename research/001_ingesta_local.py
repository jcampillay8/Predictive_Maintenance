import os
import polars as pl
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos
DB_URL = os.getenv("DATABASE_URL")

# Mapeo de archivos locales a tablas del schema maintenance
data_map = {
    "machines": "Data/PdM_machines.csv",
    "telemetry": "Data/PdM_telemetry.csv",
    "errors": "Data/PdM_errors.csv",
    "maintenance": "Data/PdM_maint.csv",
    "failures": "Data/PdM_failures.csv"
}

def load_to_postgres():
    if not DB_URL:
        print("❌ Error: No se encontró DATABASE_URL en el archivo .env")
        return
        
    engine = create_engine(DB_URL)
    
    # Orden de carga para respetar Foreign Keys
    order = ["machines", "telemetry", "errors", "maintenance", "failures"]
    
    for table in order:
        path = data_map[table]
        if os.path.exists(path):
            print(f"🚀 Cargando {path} en schema 'maintenance'...")
            
            # Leemos con Polars para velocidad extrema
            df = pl.read_csv(path)
            
            # Formatear fechas
            if "datetime" in df.columns:
                df = df.with_columns(pl.col("datetime").str.to_datetime())
            
            # Ingesta especificando el SCHEMA
            df.to_pandas().to_sql(
                table, 
                engine, 
                schema='maintenance', 
                if_exists='append', 
                index=False
            )
            print(f"✅ Tabla {table} cargada con éxito.")
        else:
            print(f"❌ Archivo no encontrado: {path}")

if __name__ == "__main__":
    load_to_postgres()