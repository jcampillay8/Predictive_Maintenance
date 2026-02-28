# src/analysis/reliability_metrics.py
import polars as pl
from sqlalchemy import select
from src.core.config import settings  # <--- IMPORTANTE: Añade esta línea
from src.database.session import SessionLocal, engine
from src.models.failure import Failure
from src.models.maintenance import Maintenance

def get_processed_data():
    """Extrae datos de la DB y calcula KPIs de confiabilidad (MTBF y MTTR)."""
    with SessionLocal() as db:
        # 1. Traemos fallas y mantenimientos
        fail_results = db.execute(select(Failure)).scalars().all()
        maint_results = db.execute(select(Maintenance)).scalars().all()

        if not fail_results:
            print("⚠️ No hay datos de fallas suficientes para calcular métricas.")
            return None

        # 2. Convertir a Polars
        df_fail = pl.DataFrame([
            {"machineID": f.machineID, "datetime": f.datetime, "type": "failure"} 
            for f in fail_results
        ])
        
        df_maint = pl.DataFrame([
            {"machineID": m.machineID, "datetime": m.datetime, "type": "maint"} 
            for m in maint_results
        ])

        # 3. Unión y cálculo de diferencias de tiempo
        df_combined = pl.concat([df_fail, df_maint]).sort(["machineID", "datetime"])

        # Calculamos la diferencia de tiempo entre eventos consecutivos por máquina
        df_combined = df_combined.with_columns(
            pl.col("datetime").diff().over("machineID").alias("diff")
        )

        # 4. Agregación de KPIs (MTBF y MTTR)
        metrics = df_combined.group_by("machineID").agg([
            pl.col("diff").filter(pl.col("type") == "failure").dt.total_hours().mean().alias("MTBF_hours"),
            pl.col("diff").filter(pl.col("type") == "maint").dt.total_hours().mean().alias("MTTR_hours"),
            pl.col("type").filter(pl.col("type") == "failure").count().alias("total_failures")
        ]).fill_null(0)

        return metrics

def update_reliability_table():
    """Calcula las métricas y las guarda en la tabla 'reliability_stats'."""
    print("🚀 Iniciando procesamiento de KPIs estratégicos en Neon...")
    
    summary = get_processed_data()
    
    if summary is not None:
        try:
            # Guardamos con el esquema correcto para evitar que se vaya a 'public'
            summary.to_pandas().to_sql(
                "reliability_stats", 
                con=engine, 
                schema=settings.DB_SCHEMA, # Forzamos el esquema 'maintenance'
                if_exists="replace", 
                index=False
            )
            print("✅ Tabla 'reliability_stats' actualizada con éxito en el esquema:", settings.DB_SCHEMA)
            print(summary.head())
        except Exception as e:
            print(f"❌ Error al guardar en la base de datos: {e}")
    else:
        print("❌ No se pudo actualizar la tabla por falta de datos origen.")

if __name__ == "__main__":
    update_reliability_table()