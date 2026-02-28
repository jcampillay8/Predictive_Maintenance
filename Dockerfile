FROM python:3.11-slim

# Evita que Python genere archivos .pyc y asegura que los logs salgan directo a la terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
ENV PORT=8080

WORKDIR /app

# Instalamos dependencias del sistema necesarias para psycopg2 y herramientas de compilación
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiamos solo los archivos de dependencias primero para aprovechar el cache de capas de Docker
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Railway inyecta la variable PORT automáticamente
EXPOSE 8080

# Gunicorn configurado para producción:
# -w 2: Dos procesos trabajadores
# --threads 4: Manejo de concurrencia dentro de cada proceso
# -k uvicorn.workers.UvicornWorker: Permite que Gunicorn maneje FastAPI (ASGI)
CMD ["gunicorn", "-w", "2", "--threads", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "src.main:app"]