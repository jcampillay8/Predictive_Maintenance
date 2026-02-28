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
# Convertimos el string de ALLOWED_ORIGINS en una lista real de Python
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if settings.ENVIRONMENT == "production" else ["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 📊 Dash App Configuration
# ==============================
# 1. Inicializamos Dash sin pasarle server=True.
# Dejamos que Dash cree su Flask interno para luego montarlo.
dash_app = Dash(
    __name__,
    requests_pathname_prefix="/dashboard/",
    serve_locally=True, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True 
)

# 2. Definir layout y callbacks
dash_app.title = "Komatsu | Predictive Maintenance"
dash_app.layout = layout

# IMPORTANTE: Registrar los callbacks antes de montar la app
register_callbacks(dash_app)

# 3. Montaje en FastAPI
# Usamos dash_app.server, que es la instancia de Flask creada por Dash
app.mount("/dashboard", WSGIMiddleware(dash_app.server))

# ==============================
# 🧭 FastAPI Routes (API)
# ==============================
@app.get("/")
async def root():
    return {"message": "Predictive Maintenance API. Go to /dashboard/ for the UI", "health": "/health"}

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }

# ==============================
# ⏯ Startup & Shutdown
# ==============================
@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode")

if __name__ == "__main__":
    import uvicorn
    # Ajustado al puerto 8080 para que coincida con tu configuración de Docker habitual
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)