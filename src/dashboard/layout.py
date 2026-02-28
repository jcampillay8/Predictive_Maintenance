# src/dashboard/layout.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
# 1. Encabezado de Alto Impacto con Autoría Destacada
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1("📊 Dashboard de Mantenimiento Predictivo", 
                            className="display-4 text-primary fw-bold mb-2"),
                    html.P("Gestión de Activos: Desde Monitoreo en Tiempo Real hasta Estrategia de Negocio.", 
                           className="lead text-muted mb-4"),
                    # --- BLOQUE DE AUTORÍA DESTACADO ---
                    html.Div([
                        html.P("DISEÑADO Y DESARROLLADO POR", 
                               className="text-secondary mb-1", 
                               style={"fontSize": "0.8rem", "letterSpacing": "3px", "fontWeight": "600"}),
                        html.H2("JAIME CAMPILLAY ROJAS", 
                                className="text-dark mb-0", 
                                style={"fontWeight": "800", "letterSpacing": "1px"}),
                        html.Div(className="bg-primary mx-auto my-2", 
                                 style={"height": "4px", "width": "60px", "borderRadius": "2px"}),
                        html.P("INGENIERO CIVIL INDUSTRIAL | SENIOR SOFTWARE & DATA ENGINEER", 
                               className="text-primary fw-bold small uppercase"),
                    ], className="py-3 bg-white shadow-sm rounded-3 border mb-4", style={"maxWidth": "1200px", "margin": "0 auto"}),                    
                    html.Hr(className="my-4"),
                ], className="pt-5 pb-4 text-center"),
                width=12
            )
        ]),

        # 2. Navegación por Pestañas (Tabs)
        dbc.Tabs([
            
            # --- PESTAÑA 1: OPERACIONES ---
            dbc.Tab(label="🔍 Monitoreo Operacional", tab_id="tab-ops", children=[
                dbc.Row([
                    # Columna Izquierda: Filtros
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Configuración de Activo", className="mb-0")),
                            dbc.CardBody([
                                html.Label("Seleccionar Máquina:", className="fw-bold mb-2"),
                                dcc.Dropdown(id='machine-selector', placeholder="Busque por ID...", className="mb-3", clearable=False, value=1, persistence=True),
                                html.Div(id="machine-stats", className="small text-info p-2 bg-light border rounded mb-3")
                            ])
                        ], className="shadow-sm mb-3"),

                        # --- NUEVO: CHAT IA OPERACIONAL ---
                        dbc.Card([
                            dbc.CardHeader(html.H5("🤖 Diagnóstico IA", className="text-white bg-dark mb-0")),
                            dbc.CardBody([
                                dbc.Textarea(
                                    id="ai-input-ops",
                                    placeholder="Ej: ¿La vibración actual explica el último error?",
                                    style={"height": "100px"},
                                    className="mb-2"
                                ),
                                dbc.Button("Analizar Activo", id="ask-ai-btn-ops", color="dark", size="sm", className="w-100 mb-3"),
                                dcc.Loading(
                                    html.Div(
                                        id="ai-output-ops",
                                        className="p-2 border rounded bg-white small",
                                        style={"minHeight": "150px", "whiteSpace": "pre-line", "fontSize": "0.85rem"},
                                        children="Seleccione una máquina y pregunte sobre su estado actual."
                                    )
                                )
                            ])
                        ], className="shadow-sm")
                    ], lg=3, md=4, xs=12),

                    # Columna Derecha: Gráfico y Tabla Operativa
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Análisis de Telemetría", className="mb-0")),
                            dbc.CardBody([
                                dcc.Loading(
                                    dcc.Graph(id='telemetry-graph', style={"height": "400px"})
                                )
                            ])
                        ], className="shadow-sm mb-4"),

                        dbc.Card([
                            dbc.CardHeader(html.H5("Historial de Eventos (Fallas y Errores)", className="text-danger mb-0")),
                            dbc.CardBody([
                                dash_table.DataTable(
                                    id='error-table',
                                    columns=[
                                        {"name": "Fecha", "id": "datetime"},
                                        {"name": "Evento", "id": "type"},
                                        {"name": "Código/ID", "id": "errorID"}
                                    ],
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'textAlign': 'left', 'padding': '12px'},
                                    style_header={
                                        'backgroundColor': '#f8d7da',
                                        'color': '#721c24',
                                        'fontWeight': 'bold'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'column_id': 'type', 'filter_query': '{type} contains "🚨"'},
                                            'fontWeight': 'bold', 'color': 'red'
                                        }
                                    ],
                                    page_size=5,
                                    style_as_list_view=True,
                                )
                            ])
                        ], className="shadow-sm")
                    ], lg=9, md=8, xs=12)
                ], className="g-4 mt-2")
            ]),

            # --- PESTAÑA 2: ESTRATEGIA (KPIs + AGENTE IA) ---
            dbc.Tab(label="📈 Estrategia y Mejora de Negocio", tab_id="tab-strategy", children=[
                dbc.Row([
                    # Columna de KPIs (Gráfico y Tabla)
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Indicadores de Confiabilidad Regional (MTBF vs MTTR)", className="mb-0")),
                            dbc.CardBody([
                                html.P("Análisis comparativo de disponibilidad y tiempos de respuesta por flota.", className="text-muted"),
                                dcc.Loading(
                                    dcc.Graph(id='kpi-comparison-graph')
                                )
                            ])
                        ], className="shadow-sm mt-4 mb-4"),
                        
                        dbc.Card([
                            dbc.CardHeader(html.H5("Data Mart: Métricas Consolidadas", className="mb-0")),
                            dbc.CardBody([
                                dash_table.DataTable(
                                    id='kpi-table',
                                    style_table={'overflowX': 'auto'},
                                    style_header={'backgroundColor': '#e9ecef', 'fontWeight': 'bold'},
                                    style_cell={'textAlign': 'center', 'padding': '10px'},
                                    page_size=10,
                                    style_as_list_view=True,
                                )
                            ])
                        ], className="shadow-sm mb-4")
                    ], lg=8, md=12),

                    # Columna del Agente de IA (Gemini 1.5 Pro)
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("🤖 Analista Virtual", className="text-white bg-primary mb-0")),
                            dbc.CardBody([
                                html.P("Optimización basada en modelos generativos (gemini-2.0-flash).", className="small text-muted fw-bold"),
                                html.Label("Pregunte al analista sobre la flota:", className="small"),
                                dbc.Textarea(
                                    id="ai-input",
                                    placeholder="Ej: ¿Qué máquinas tienen un MTTR crítico y cómo afecta la disponibilidad?",
                                    style={"height": "120px"},
                                    className="mb-3"
                                ),
                                dbc.Button(
                                    "Consultar Inteligencia de Activos", 
                                    id="ask-ai-btn", 
                                    color="primary", 
                                    className="w-100 mb-4 shadow-sm"
                                ),
                                html.Div([
                                    html.B("Análisis de Confiabilidad:"),
                                    dcc.Loading(
                                        html.Div(
                                            id="ai-output", 
                                            className="p-3 border rounded bg-white small shadow-inner", 
                                            style={"minHeight": "200px", "whiteSpace": "pre-line", "overflowY": "auto"},
                                            children="El analista está listo. Ingrese una consulta técnica."
                                        )
                                    )
                                ], id="ai-response-container")
                            ])
                        ], className="shadow-sm mt-4 sticky-top", style={"top": "20px"})
                    ], lg=4, md=12)
                ], className="g-4 mt-2")
            ]),

        ], active_tab="tab-ops") 

    ], fluid=True, className="p-4 bg-light", style={"minHeight": "100vh"})

layout = create_layout()