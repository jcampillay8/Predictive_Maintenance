# 🚜 Predictive Maintenance Dash: AI-Powered Industrial Analytics

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.133+-009688.svg)](https://fastapi.tiangolo.com/)
[![Polars](https://img.shields.io/badge/Polars-1.38-orange.svg)](https://pola.rs/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Railway-0b0d0e.svg)](https://railway.app)

MVP de una plataforma de mantenimiento predictivo que transforma datos de telemetría industrial en decisiones estratégicas. Utiliza procesamiento de alto rendimiento, modelos relacionales en la nube y agentes de IA para optimizar la disponibilidad de flotas.

📍 **Live Demo:** [Dashboard Online](https://predictivemaintenance-production.up.railway.app/dashboard/)

---

## 🚀 Key Features

* **High-Performance ETL:** Ingesta de **+870,000 registros** de telemetría utilizando **Polars** para un procesamiento eficiente de memoria y CPU.
* **Strategic KPIs:** Cálculo automatizado de métricas de confiabilidad: **MTBF** (Mean Time Between Failures) y **MTTR** (Mean Time To Repair).
* **AI Insights:** Integración con **Gemini 3 Flash** para generar diagnósticos técnicos y recomendaciones basadas en patrones de falla detectados.
* **Cloud Native:** Arquitectura diseñada para la nube con **PostgreSQL Serverless (Neon)** y despliegue automatizado en **Railway**.
* **Hybrid Backend:** Combinación de **FastAPI** para la lógica de API robusta y **Dash/Plotly** para una visualización interactiva avanzada.

---

## 🛠️ Architecture & Tech Stack

* **Language:** `Python 3.11+`
* **Data Processing:** `Polars`, `Pandas`, `PyArrow`.
* **Database & ORM:** `PostgreSQL (Neon)`, `SQLAlchemy 2.0`.
* **API & Web Server:** `FastAPI`, `Dash`, `Plotly`, `Gunicorn` (Uvicorn Workers).
* **AI/LLM:** `Google Generative AI (Gemini 3 Flash)`.
* **Infrastructure:** `Docker`, `Railway`.

---

## 📂 Project Structure

```plaintext
├── src/
│   ├── analysis/       # Lógica de cálculo de KPIs (MTBF/MTTR)
│   ├── core/           # Configuración global y variables de entorno (Pydantic)
│   ├── database/       # Conexión, sesión y configuración de esquemas
│   ├── models/         # Modelos de SQLAlchemy (Machine, Telemetry, etc.)
│   ├── services/       # Ingesta de datos y Agente de IA
│   ├── dashboard/      # UI, Layouts y Callbacks de Dash
│   └── main.py         # Punto de entrada de la aplicación FastAPI
├── Data/               # Datasets originales (CSV)
├── Dockerfile          # Configuración de contenedor para producción
└── pyproject.toml      # Gestión de dependencias y metadata
```

## 🔧 Installation & Local Setup

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/jcampillay8/Predictive_Maintenance.git](https://github.com/jcampillay8/Predictive_Maintenance.git)
   cd Predictive_Maintenance
   ```

2. **Configurar variables de entorno (`.env`):**

Asegúrate de crear un archivo `.env` en la raíz del proyecto con los siguientes parámetros:

```env
ENVIRONMENT=development
PROJECT_NAME="Predictive Maintenance"
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
WEBSITE_URL=http://localhost:8080
DB_HOST=your_host
DB_NAME=Maintenance
DB_USER=your_user
DB_PASSWORD=your_password
GEMINI_API_KEY=your_key
```
## 📈 Strategic Impact

Este proyecto permite a los jefes de flota y gerentes de mantenimiento:

* **Reducir el Downtime:** Identificando proactivamente máquinas con un **MTBF** crítico.
* **Optimizar Recursos:** Priorizando intervenciones en equipos con mayor frecuencia de fallas.
* **Análisis Proactivo:** Usando **IA** para interpretar datos de sensores antes de que ocurra una falla catastrófica.

---

## 👨‍💻 Author

**Jaime Campillay** - *Data & Software Engineer* 🔗 [LinkedIn](https://www.linkedin.com/in/jaime-campillay/) 