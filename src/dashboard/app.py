# src/dashboard/app.py
from dash import Dash
import dash_bootstrap_components as dbc
from .layout import layout
from .callbacks import register_callbacks

def init_dashboard(server):
    """Inicializa Dash dentro de un servidor FastAPI (Flask/Starlette)"""
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = layout
    register_callbacks(dash_app)
    
    return server