import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from dash import Dash
import dash_bootstrap_components as dbc

from src.core.config import settings
from src.dashboard.layout import layout
from src.dashboard.callbacks import register_callbacks

# ==============================
# 🪵 Logging Configuration
# ==============================
logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ==============================
# 🚀 FastAPI App Init
# ==============================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="API and Dashboard for Predictive Maintenance"
)

# 🧱 Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ajustar según settings.ALLOWED_ORIGINS más adelante
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 📊 Dash App Integration
# ==============================
# ==============================
# 1. Creamos Dash de forma independiente (server=True crea un Flask interno)
# ==============================
# 📊 Dash App Integration
# ==============================
dash_app = Dash(
    __name__,
    server=True, 
    # Cambiamos url_base_pathname por requests_pathname_prefix
    requests_pathname_prefix="/dashboard/", 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)

dash_app.title = "Predictive Maintenance Dashboard"
dash_app.layout = layout
register_callbacks(dash_app)

# Asegúrate de que este path sea EXACTAMENTE igual al prefijo de arriba
app.mount("/dashboard", WSGIMiddleware(dash_app.server))
# ==============================
# 🧭 FastAPI Routes (API)
# ==============================
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "database": "connected" # Podrías añadir lógica de check real aquí
    }

# ==============================
# ⏯ Startup & Shutdown
# ==============================
@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode")

if __name__ == "__main__":
    import uvicorn
    # Sin el ".py" en el string
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)