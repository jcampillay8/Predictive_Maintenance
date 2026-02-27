# src/dashboard/layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        # 1. Encabezado estilizado (Mantenido de la versión anterior)
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

        # 2. Cuerpo del Dashboard: Filtros a la izquierda, Contenido a la derecha
        dbc.Row([
            
            # Columna Izquierda: Configuración
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
                        # Este Div puede mostrar info extra como edad o modelo
                        html.Div(id="machine-stats", className="small text-info")
                    ])
                ], className="shadow-sm mb-4")
            ], lg=3, md=4, xs=12),

            # Columna Derecha: Gráfico + Tabla
            dbc.Col([
                
                # Panel del Gráfico con Loading
                dbc.Card([
                    dbc.CardHeader(html.H5("Análisis de Telemetría (Últimos registros)", className="mb-0")),
                    dbc.CardBody([
                        dcc.Loading(
                            id="loading-graph",
                            type="circle",
                            children=dcc.Graph(
                                id='telemetry-graph',
                                config={'displayModeBar': True, 'responsive': True},
                                style={"height": "450px"}
                            )
                        )
                    ])
                ], className="shadow-sm mb-4"),

                # Panel de Historial de Errores y Fallas
                dbc.Card([
                    dbc.CardHeader(html.H5("Historial de Errores y Fallas", className="text-danger mb-0")),
                    dbc.CardBody([
                        dash_table.DataTable(
                            id='error-table',
                            columns=[
                                {"name": "Fecha", "id": "datetime"},
                                {"name": "Evento", "id": "type"},
                                {"name": "Código/ID", "id": "errorID"}
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left', 
                                'padding': '12px',
                                'fontFamily': 'sans-serif'
                            },
                            style_header={
                                'backgroundColor': '#f8d7da',
                                'color': '#721c24',
                                'fontWeight': 'bold',
                                'border': '1px solid #f5c6cb'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'column_id': 'type', 'filter_query': '{type} contains "🚨"'},
                                    'fontWeight': 'bold',
                                    'color': 'red'
                                }
                            ],
                            page_size=5,
                            # Estilo de la fuente de la tabla
                            style_as_list_view=True,
                        )
                    ])
                ], className="shadow-sm")

            ], lg=9, md=8, xs=12)
        ], className="g-4") 

    ], fluid=True, className="p-4 bg-light", style={"minHeight": "100vh"})

# Variable principal para la integración con FastAPI
layout = create_layout()