# src/analysis/reliability_metrics.py
import polars as pl
from sqlalchemy import select, text
from src.database.session import SessionLocal, engine
from src.models.failure import Failure
from src.models.machine import Machine

def calculate_reliability_data():
    with SessionLocal() as db:
        # 1. Traer todas las fallas ordenadas por máquina y fecha
        query = select(Failure).order_by(Failure.machineID, Failure.datetime)
        results = db.execute(query).scalars().all()
        
        # 2. Convertir a Polars para cálculos rápidos de tiempo
        df_failures = pl.DataFrame([
            {"machineID": f.machineID, "datetime": f.datetime} 
            for f in results
        ])

        # 3. Calcular el tiempo entre fallas (MTBF) por máquina
        # Usamos 'diff' para encontrar la diferencia de tiempo entre la fila actual y la anterior
        df_metrics = df_failures.with_columns([
            pl.col("datetime").diff().over("machineID").alias("time_to_failure")
        ])

        # 4. Limpiar datos y convertir a horas (el primer registro de cada máquina será null)
        df_metrics = df_metrics.filter(pl.col("time_to_failure").is_not_null())
        
        # Convertir la duración a horas totales (float)
        df_metrics = df_metrics.with_columns([
            (pl.col("time_to_failure").dt.total_minutes() / 60).alias("hours_between_failures")
        ])

        # 5. Resumen final por máquina
        summary = df_metrics.group_by("machineID").agg([
            pl.col("hours_between_failures").mean().alias("MTBF_hours"),
            pl.count().alias("total_failures")
        ])

        return summary

def update_reliability_table():
    with SessionLocal() as db:
        # 1. Extracción (Igual que antes)
        query = select(Failure).order_by(Failure.machineID, Failure.datetime)
        results = db.execute(query).scalars().all()
        
        if not results:
            print("No hay fallas registradas para calcular métricas.")
            return

        # 2. Transformación con Polars
        df_failures = pl.DataFrame([
            {"machineID": f.machineID, "datetime": f.datetime} for f in results
        ])

        # Cálculo de MTBF (Mean Time Between Failures)
        summary = (
            df_failures
            .with_columns(
                pl.col("datetime").diff().over("machineID").alias("diff")
            )
            .filter(pl.col("diff").is_not_null())
            .with_columns(
                (pl.col("diff").dt.total_minutes() / 60).alias("hours")
            )
            .group_by("machineID")
            .agg([
                pl.col("hours").mean().alias("mtbf_hours"),
                pl.count().alias("total_failures")
            ])
        )

        # 3. Carga (Load) a una nueva tabla para Power BI
        # Esto creará la tabla 'reliability_stats' automáticamente si no existe
        summary.to_pandas().to_sql(
            "reliability_stats", 
            con=engine, 
            if_exists="replace", 
            index=False
        )
        print("✅ Métricas actualizadas en la tabla 'reliability_stats'")    

# Ejemplo de ejecución
if __name__ == "__main__":
    update_reliability_table()
    metrics = calculate_reliability_data()
    print(metrics)