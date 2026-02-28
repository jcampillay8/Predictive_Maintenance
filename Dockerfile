FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

# Instalamos dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiamos archivos de dependencias
COPY requirements.txt .
# Forzamos la instalación de gunicorn y uvicorn explícitamente por seguridad
RUN pip install --no-cache-dir --default-timeout=100 --retries 5 -r requirements.txt && \
    pip install --no-cache-dir --default-timeout=100 --retries 5 gunicorn uvicorn

COPY . .

EXPOSE 8080

# Usamos python -m para invocar el módulo directamente
CMD ["python", "-m", "gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "src.main:app"]