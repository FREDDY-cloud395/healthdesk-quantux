# =============================================================================
# QUANTUX SERVICEDESK - SCRIPT DE DESPLIEGUE AUTOMÁTICO EN LA NUBE (POWERSHELL)
# =============================================================================

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "🚀 INICIANDO DESPLIEGUE A PRODUCCIÓN - QUANTUX SERVICEDESK" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# Comprobar si existe Docker Compose
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "🐳 Construyendo y levantando contenedores con Docker Compose..." -ForegroundColor Green
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml build --no-cache
    docker-compose -f docker-compose.prod.yml up -d
    Write-Host "✅ Servicio de Producción disponible en http://localhost:8000" -ForegroundColor Green
    return
}

# Comprobar si existe gcloud CLI
if (Get-Command gcloud -ErrorAction SilentlyContinue) {
    Write-Host "☁️ Desplegando en Google Cloud Run..." -ForegroundColor Green
    gcloud builds submit --config cloudbuild.yaml .
    Write-Host "✅ Despliegue en Cloud Run completado con éxito." -ForegroundColor Green
    return
}

Write-Host "⚠️ No se detectó docker-compose ni gcloud. Por favor verifique sus herramientas de nube." -ForegroundColor Yellow
