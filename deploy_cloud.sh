#!/bin/bash
# =============================================================================
# QUANTUX SERVICEDESK - SCRIPT DE DESPLIEGUE AUTOMÁTICO EN LA NUBE (PRODUCCIÓN)
# =============================================================================

set -e

echo "========================================================"
echo "🚀 INICIANDO DESPLIEGUE A PRODUCCIÓN - QUANTUX SERVICEDESK"
echo "========================================================"

# Opción 1: Despliegue con Docker Compose en Servidor / VM en la nube
if command -v docker-compose &> /dev/null; then
    echo "🐳 Construyendo y levantando contenedores con Docker Compose..."
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml build --no-cache
    docker-compose -f docker-compose.prod.yml up -d
    echo "✅ Servicio disponible en http://localhost:8000"
    exit 0
fi

# Opción 2: Despliegue en Google Cloud Run
if command -v gcloud &> /dev/null; then
    echo "☁️ Desplegando en Google Cloud Run..."
    PROJECT_ID=$(gcloud config get-value project)
    gcloud builds submit --config cloudbuild.yaml .
    echo "✅ Despliegue en Cloud Run completado con éxito."
    exit 0
fi

echo "⚠️ No se detectó docker-compose ni gcloud. Por favor verifique sus herramientas de nube."
