# src/dashboard/callbacks.py
from dash import Output, Input

def register_callbacks(app):
    @app.callback(
        Output('telemetry-graph', 'figure'),
        Input('machine-selector', 'value')
    )
    def update_graph(selected_machine):
        # Por ahora devolvemos un gráfico vacío
        return {
            'data': [],
            'layout': {'title': 'Seleccione una máquina para ver telemetría'}
        }