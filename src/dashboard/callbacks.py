# src/dashboard/callbacks.py
from dash import Output, Input
import plotly.graph_objects as go
import polars as pl
from sqlalchemy import select
from src.database.session import SessionLocal, engine
from src.models.machine import Machine
from src.models.telemetry import Telemetry
from src.models.error import Error
from src.models.failure import Failure
import plotly.express as px

def register_callbacks(app):
    
    # --- Callback 1: Poblar el Dropdown al iniciar ---
    @app.callback(
        Output('machine-selector', 'options'),
        Input('machine-selector', 'id')
    )
    def populate_dropdown(_):
        with SessionLocal() as db:
            # Traemos las máquinas para llenar el selector
            machines = db.execute(select(Machine.machineID, Machine.model)).all()
            return [
                {'label': f"Máquina {m.machineID} (Mod: {m.model})", 'value': m.machineID} 
                for m in machines
            ]

    # --- Callback 2: Actualizar Dashboard Completo ---
    @app.callback(
        [Output('telemetry-graph', 'figure'),
         Output('error-table', 'data'),
         Output('machine-stats', 'children')], # Actualizamos también la info de la máquina
        Input('machine-selector', 'value')
    )
    def update_dashboard(selected_machine):
        if not selected_machine:
            return go.Figure(), [], "Seleccione una máquina para ver detalles."

        with SessionLocal() as db:
            # 0. Info de la Máquina (Modelo y Edad)
            m_info = db.execute(select(Machine).filter(Machine.machineID == selected_machine)).scalar_one_or_none()
            stats_text = f"Modelo: {m_info.model} | Edad: {m_info.age} años" if m_info else ""

            # 1. CONSULTA DE TELEMETRÍA (Últimos 200 registros)
            tel_query = (
                select(Telemetry)
                .filter(Telemetry.machineID == selected_machine)
                .order_by(Telemetry.datetime.desc())
                .limit(200)
            )
            tel_results = db.execute(tel_query).scalars().all()
            
            if tel_results:
                df_tel = pl.DataFrame([
                    {
                        "datetime": r.datetime,
                        "volt": r.volt,
                        "rotate": r.rotate,
                        "pressure": r.pressure,
                        "vibration": r.vibration
                    } for r in tel_results
                ]).sort("datetime")

                fig = go.Figure()
                for var in ['volt', 'rotate', 'pressure', 'vibration']:
                    fig.add_trace(go.Scatter(
                        x=df_tel["datetime"], 
                        y=df_tel[var],
                        mode='lines',
                        name=var.capitalize()
                    ))
                
                fig.update_layout(
                    title=f"Telemetría en Tiempo Real - Máquina {selected_machine}",
                    xaxis_title="Tiempo",
                    yaxis_title="Valor",
                    template="plotly_white",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
            else:
                fig = go.Figure().update_layout(title="Sin datos disponibles")

            # 2. CONSULTA DE ERRORES Y FALLAS
            err_query = select(Error).filter(Error.machineID == selected_machine).order_by(Error.datetime.desc()).limit(10)
            fail_query = select(Failure).filter(Failure.machineID == selected_machine).order_by(Failure.datetime.desc()).limit(10)
            
            err_results = db.execute(err_query).scalars().all()
            fail_results = db.execute(fail_query).scalars().all()

            table_data = []
            
            # Errores (Usando getattr para evitar AttributeErrors)
            for e in err_results:
                eid = getattr(e, 'errorID', getattr(e, 'id', 'N/A'))
                table_data.append({
                    "datetime": e.datetime.strftime("%Y-%m-%d %H:%M"),
                    "type": "⚠️ ERROR",
                    "errorID": eid
                })
            
            # Fallas (Corregido según tu modelo: usa .id y .failure)
            for f in fail_results:
                table_data.append({
                    "datetime": f.datetime.strftime("%Y-%m-%d %H:%M"),
                    "type": f"🚨 FALLA ({f.failure})",
                    "errorID": f.id 
                })

            # Ordenamos la tabla por fecha
            table_data = sorted(table_data, key=lambda x: x['datetime'], reverse=True)

            return fig, table_data, stats_text

    @app.callback(
        [Output('kpi-comparison-graph', 'figure'),
         Output('kpi-table', 'data'),
         Output('kpi-table', 'columns')],
        Input('machine-selector', 'id') # Se dispara al cargar
    )
    def update_strategic_view(_):
        with SessionLocal() as db:
            # Leemos la tabla procesada
            df = pl.read_database("SELECT * FROM reliability_stats", connection=engine.connect())
            
            # Gráfico de comparación MTBF vs MTTR
            fig = px.bar(
                df.to_pandas(), 
                x="machineID", 
                y=["MTBF_hours", "MTTR_hours"],
                barmode="group",
                title="Comparativa MTBF vs MTTR por Máquina",
                labels={"value": "Horas", "variable": "Métrica"}
            )
            
            columns = [{"name": i, "id": i} for i in df.columns]
            return fig, df.to_dicts(), columns