# HealthDesk Quantux - Dockerfile Multi-Stage Produccion
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends     curl     && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo fuente
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY docs/ ./docs/

# Variable de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app/backend

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
