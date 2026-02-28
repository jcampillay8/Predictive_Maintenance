# src/dashboard/callbacks.py
from dash import Output, Input, State
import plotly.graph_objects as go
import polars as pl
from sqlalchemy import select
from src.database.session import SessionLocal, engine
from src.models.machine import Machine
from src.models.telemetry import Telemetry
from src.models.error import Error
from src.models.failure import Failure
from src.services.ai_analyst import AIAnalyst

def register_callbacks(app):
    
    # --- Callback 1: Poblar el Dropdown ---
    @app.callback(
        Output('machine-selector', 'options'),
        Input('machine-selector', 'id')
    )
    def populate_dropdown(_):
        with SessionLocal() as db:
            machines = db.execute(select(Machine.machineID, Machine.model)).all()
            return [
                {'label': f"Máquina {m.machineID} (Mod: {m.model})", 'value': m.machineID} 
                for m in machines
            ]

    # --- Callback 2: Actualizar Dashboard Operacional ---
    @app.callback(
        [Output('telemetry-graph', 'figure'),
         Output('error-table', 'data'),
         Output('machine-stats', 'children')],
        [Input('machine-selector', 'value')]
    )
    def update_dashboard(selected_machine):
        # 1. FORZAMOS EL VALOR 1 si Dash envía None al inicio
        machine_to_query = selected_machine if selected_machine is not None else 1

        with SessionLocal() as db:
            # 2. Info de la Máquina (Usando machine_to_query)
            m_info = db.execute(select(Machine).filter(Machine.machineID == machine_to_query)).scalar_one_or_none()
            
            if not m_info:
                return go.Figure(), [], "Máquina no encontrada en DB."

            stats_text = f"Modelo: {m_info.model} | Edad: {m_info.age} años"

            # 3. Telemetría (Usando machine_to_query)
            tel_query = (
                select(Telemetry)
                .filter(Telemetry.machineID == machine_to_query)
                .order_by(Telemetry.datetime.desc())
                .limit(200)
            )
            tel_results = db.execute(tel_query).scalars().all()
            
            fig = go.Figure()
            if tel_results:
                d_time = [r.datetime for r in tel_results][::-1]
                d_volt = [r.volt for r in tel_results][::-1]
                d_rotate = [r.rotate for r in tel_results][::-1]
                d_pressure = [r.pressure for r in tel_results][::-1]
                d_vibration = [r.vibration for r in tel_results][::-1]

                for name, data in zip(['Volt', 'Rotate', 'Pressure', 'Vibration'], 
                                     [d_volt, d_rotate, d_pressure, d_vibration]):
                    fig.add_trace(go.Scatter(x=d_time, y=data, mode='lines', name=name))
                
                    fig.update_layout(
                    # Usamos <b> para negrita y aumentamos un poco el tamaño con span si quisieras
                    title=dict(
                        text=f"<b>Telemetría en Tiempo Real - Máquina {machine_to_query}</b>",
                        font=dict(size=20) # Opcional: para que destaque más
                    ),
                    paper_bgcolor='white', 
                    plot_bgcolor='white',
                    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
                    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
            else:
                fig.update_layout(title="Sin datos de telemetría")

            # 4. Errores y Fallas (¡IMPORTANTE! Cambiado a machine_to_query aquí también)
            err_res = db.execute(select(Error).filter(Error.machineID == machine_to_query).order_by(Error.datetime.desc()).limit(10)).scalars().all()
            fail_res = db.execute(select(Failure).filter(Failure.machineID == machine_to_query).order_by(Failure.datetime.desc()).limit(10)).scalars().all()

            table_data = []
            for e in err_res:
                table_data.append({
                    "datetime": e.datetime.strftime("%Y-%m-%d %H:%M"), 
                    "type": "⚠️ ERROR", 
                    "errorID": getattr(e, 'errorID', 'N/A')
                })
            for f in fail_res:
                table_data.append({
                    "datetime": f.datetime.strftime("%Y-%m-%d %H:%M"), 
                    "type": f"🚨 FALLA ({f.failure})", 
                    "errorID": f.id
                })

            return fig, sorted(table_data, key=lambda x: x['datetime'], reverse=True), stats_text

    # --- Callback 3: Vista Estratégica ---
    @app.callback(
        [Output('kpi-comparison-graph', 'figure'),
         Output('kpi-table', 'data'),
         Output('kpi-table', 'columns')],
        Input('machine-selector', 'id')
    )
    def update_strategic_view(_):
        with SessionLocal() as db:
            # Usamos una conexión directa para Polars
            with engine.connect() as conn:
                # Busca esta línea (aproximadamente línea 115):
                df = pl.read_database("SELECT * FROM maintenance.reliability_stats", connection=conn)
            
            fig = go.Figure(data=[
                go.Bar(name='MTBF (Horas)', x=df['machineID'].to_list(), y=df['MTBF_hours'].to_list()),
                go.Bar(name='MTTR (Horas)', x=df['machineID'].to_list(), y=df['MTTR_hours'].to_list())
            ])
            
            fig.update_layout(
                title="Comparativa MTBF vs MTTR por Máquina",
                barmode='group', paper_bgcolor='white', plot_bgcolor='white'
            )
            
            columns = [{"name": i, "id": i} for i in df.columns]
            return fig, df.to_dicts(), columns

    # --- Callback 4: IA Estratégica ---
    @app.callback(
        Output("ai-output", "children"),
        Input("ask-ai-btn", "n_clicks"),
        State("ai-input", "value"),
        State("kpi-table", "data"),
        prevent_initial_call=True
    )
    def get_ai_insight(n_clicks, user_question, kpi_data):
        if not n_clicks or not user_question:
            return "Por favor, ingrese una pregunta para el analista."
        analyst = AIAnalyst()
        context = f"DATOS DEL DATA MART: {str(kpi_data)}"
        return analyst.ask_llm(context, user_question)

    # --- Callback 5: IA Operacional ---
    @app.callback(
        Output("ai-output-ops", "children"),
        Input("ask-ai-btn-ops", "n_clicks"),
        State("ai-input-ops", "value"),
        State("machine-selector", "value"),
        State("error-table", "data"),
        prevent_initial_call=True
    )
    def get_operational_ai_insight(n_clicks, user_question, machine_id, table_data):
        # Aquí también protegemos el machine_id
        m_id = machine_id if machine_id is not None else 1
        
        if not n_clicks or not user_question:
            return "Por favor, ingrese una pregunta."

        analyst = AIAnalyst()
        with SessionLocal() as db:
            tel = db.execute(select(Telemetry).filter(Telemetry.machineID == m_id).order_by(Telemetry.datetime.desc()).limit(10)).scalars().all()
            telemetry_summary = str([{"volt": r.volt, "rotate": r.rotate} for r in tel])

        return analyst.ask_llm_operational(str(m_id), telemetry_summary, str(table_data[:5]), user_question)