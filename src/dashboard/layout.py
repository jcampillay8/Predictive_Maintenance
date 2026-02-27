# src/dashboard/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        # Encabezado con Estilo
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1("📊 Dashboard de Mantenimiento Predictivo", className="display-4 text-primary"),
                    html.P("Monitoreo de telemetría y estado de salud de activos industriales.", className="lead text-muted"),
                    html.Hr(className="my-2"),
                ], className="py-4 text-center"),
                width=12
            )
        ]),

        # Panel de Filtros
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Configuración de Vista", className="mb-0")),
                    dbc.CardBody([
                        html.Label("Seleccionar Activo (Máquina):", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='machine-selector',
                            options=[], # Se llena vía callback
                            placeholder="Busque por ID o Modelo...",
                            className="mb-3",
                            clearable=False
                        ),
                        html.Div(id="machine-info-status", className="small text-info")
                    ])
                ], className="shadow-sm")
            ], lg=3, md=4, xs=12),

            # Panel del Gráfico
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Análisis de Telemetría (Últimos registros)", className="mb-0")),
                    dbc.CardBody([
                        dcc.Loading( # Spinner de carga mientras el callback consulta la DB
                            id="loading-graph",
                            type="circle",
                            children=dcc.Graph(
                                id='telemetry-graph',
                                config={'displayModeBar': True, 'responsive': True},
                                style={"height": "500px"}
                            )
                        )
                    ])
                ], className="shadow-sm")
            ], lg=9, md=8, xs=12)
        ], className="g-4") # Gap entre columnas

    ], fluid=True, className="p-4 bg-light", style={"minHeight": "100vh"})

# Definimos la variable para main.py
layout = create_layout()