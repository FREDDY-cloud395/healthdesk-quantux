# =============================================================================
# HEALTHDESK QUANTUX — DOCKERFILE MULTI-STAGE PRODUCCIÓN (v4.0.0)
# Arquitectura Optimizada: Hardening de Seguridad, Non-Root User & Healthcheck
# =============================================================================

# -----------------------------------------------------------------------------
# STAGE 1: BUILDER (Compilación y Resolución de Dependencias)
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Instalar dependencias del sistema requeridas para compilar extensiones C
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar manifiesto de dependencias
COPY backend/requirements.txt ./requirements.txt

# Instalar paquetes en prefijo aislado para copia limpia
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# -----------------------------------------------------------------------------
# STAGE 2: RUNNER (Imagen Final de Producción Mínima y Segura)
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS runner

LABEL maintainer="Quantux DevOps Team <devops@quantuxsalud.com>"
LABEL version="4.0.0"
LABEL description="HealthDesk Quantux Enterprise ServiceDesk Platform"

# Instalar utilitarios mínimos de ejecución y diagnóstico (curl para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario y grupo de sistema sin privilegios root (CIS Benchmark / DevSecOps)
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/bash -m appuser

WORKDIR /app

# Copiar paquetes pre-compilados desde el builder
COPY --from=builder /install /usr/local

# Preparar directorios de aplicación y datos persistentes con permisos correctos
RUN mkdir -p /app/backend/uploads /app/docs /app/frontend && \
    chown -R appuser:appuser /app

# Copiar código fuente y activos estáticos preservando propiedad
COPY --chown=appuser:appuser backend/ ./backend/
COPY --chown=appuser:appuser frontend/ ./frontend/
COPY --chown=appuser:appuser docs/ ./docs/

# Variables de entorno del contenedor
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/backend \
    PORT=8000 \
    APP_ENV=production

# Verificación de Salud Integrada en Docker Engine / Kubernetes / Cloud Run
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Cambiar a usuario sin privilegios
USER appuser

# Directorio de trabajo para Uvicorn
WORKDIR /app/backend

# Puerto de escucha estándar
EXPOSE 8000

# Comando de inicio del servidor ASGI
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]
