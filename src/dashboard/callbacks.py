from dash import Output, Input
import plotly.graph_objects as go
import polars as pl
from sqlalchemy import select
from src.database.session import SessionLocal
from src.models.machine import Machine
from src.models.telemetry import Telemetry
from src.dashboard.layout import layout

def register_callbacks(app):
    
    # --- Callback 1: Poblar el Dropdown al cargar la página ---
    @app.callback(
        Output('machine-selector', 'options'),
        Input('machine-selector', 'id') # Trigger al cargar
    )
    def populate_dropdown(_):
        with SessionLocal() as db:
            # Traemos solo ID y Modelo para no sobrecargar
            machines = db.execute(select(Machine.machineID, Machine.model)).all()
            return [
                {'label': f"Máquina {m.machineID} (Mod: {m.model})", 'value': m.machineID} 
                for m in machines
            ]

    # --- Callback 2: Actualizar Gráfico según Máquina Seleccionada ---
    @app.callback(
        Output('telemetry-graph', 'figure'),
        Input('machine-selector', 'value')
    )
    def update_graph(selected_machine):
        if not selected_machine:
            return {
                'data': [],
                'layout': {'title': 'Seleccione una máquina para comenzar'}
            }

        with SessionLocal() as db:
            # Consultamos las últimas 100 mediciones de telemetría
            # Nota: Ajustamos el límite para que el gráfico sea fluido
            query = (
                select(Telemetry)
                .filter(Telemetry.machineID == selected_machine)
                .order_by(Telemetry.datetime.desc())
                .limit(200)
            )
            
            # Convertimos el resultado de SQLAlchemy a un DataFrame de Polars
            results = db.execute(query).scalars().all()
            
            if not results:
                return {'data': [], 'layout': {'title': 'No hay datos disponibles'}}

            # Creamos el DF de Polars para manipulación rápida
            df = pl.DataFrame([
                {
                    "datetime": r.datetime,
                    "volt": r.volt,
                    "rotate": r.rotate,
                    "pressure": r.pressure,
                    "vibration": r.vibration
                } for r in results
            ]).sort("datetime")

            # Creamos el gráfico con múltiples ejes o líneas
            fig = go.Figure()
            
            variables = ['volt', 'rotate', 'pressure', 'vibration']
            for var in variables:
                fig.add_trace(go.Scatter(
                    x=df["datetime"], 
                    y=df[var],
                    mode='lines',
                    name=var.capitalize()
                ))

            fig.update_layout(
                title=f"Telemetría Real-Time: Máquina {selected_machine}",
                xaxis_title="Tiempo",
                yaxis_title="Valor Medido",
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            return fig