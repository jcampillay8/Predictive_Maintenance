# src/dashboard/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Predictive Maintenance Dashboard", className="text-center my-4"))
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Seleccionar Máquina:"),
                dcc.Dropdown(id='machine-selector', options=[])
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='telemetry-graph'), width=12)
        ])
    ], fluid=True)

# Definimos la variable que main.py está buscando
layout = create_layout()