# =============================================================================
# HEALTHDESK QUANTUX — POWERSHELL SERVICE LAUNCHER (v4.0.0 Enterprise ITIL)
# =============================================================================

$ErrorActionPreference = "Continue"

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "          HEALTHDESK QUANTUX — QUANTUX SALUD (v4.0.0 Enterprise ITIL)" -ForegroundColor White
Write-Host "     Sistema Integral de Mesa de Ayuda y Soporte Hospitalario N1/N2/N3" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot

# -----------------------------------------------------------------------------
# 1. Validar instalación y versión de Python (>= 3.10)
# -----------------------------------------------------------------------------
Write-Host "[1/5] Verificando entorno de ejecución Python..." -ForegroundColor Yellow

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR CRÍTICO] Python no está instalado o no se encuentra en el PATH del sistema." -ForegroundColor Red
    Write-Host "Por favor instale Python 3.10+ desde https://www.python.org/ marcando 'Add to PATH'." -ForegroundColor Red
    Read-Host "Presione ENTER para salir"
    exit 1
}

try {
    $pyVer = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    $isCompatible = python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR CRÍTICO] Se detectó Python $pyVer. Se requiere Python >= 3.10." -ForegroundColor Red
        Read-Host "Presione ENTER para salir"
        exit 1
    }
    Write-Host "[OK] Python $pyVer detectado y validado (compatible >= 3.10)." -ForegroundColor Green
} catch {
    Write-Host "[ERROR] No se pudo verificar la versión de Python: $_" -ForegroundColor Red
    exit 1
}

# -----------------------------------------------------------------------------
# 2. Validar paquetes y dependencias requeridas
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[2/5] Verificando dependencias (FastAPI, Uvicorn, SQLModel, Pydantic)..." -ForegroundColor Yellow

python -c "import fastapi, uvicorn, sqlmodel, pydantic, sqlalchemy, multipart" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[AVISO] Se detectaron dependencias faltantes. Instalando desde backend/requirements.txt..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r backend/requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la instalación de dependencias. Verifique conectividad o permisos." -ForegroundColor Red
        Read-Host "Presione ENTER para salir"
        exit 1
    }
    Write-Host "[OK] Dependencias instaladas satisfactoriamente." -ForegroundColor Green
} else {
    Write-Host "[OK] Todas las dependencias requeridas están instaladas." -ForegroundColor Green
}

# -----------------------------------------------------------------------------
# 3. Validar y liberar puertos 8000 y 3000 (y 8005)
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[3/5] Verificando y liberando puertos de red (8000, 3000)..." -ForegroundColor Yellow

$targetPorts = @(8000, 3000)
foreach ($port in $targetPorts) {
    try {
        $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
        if ($conns) {
            foreach ($c in $conns) {
                $pidToKill = $c.OwningProcess
                Write-Host "[INFO] Liberando proceso colgado en puerto $port (PID: $pidToKill)..." -ForegroundColor Yellow
                Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
            }
            Start-Sleep -Milliseconds 600
        }
        Write-Host "[OK] Puerto $port disponible y libre." -ForegroundColor Green
    } catch {
        Write-Host "[INFO] Puerto $port listo para escuchar." -ForegroundColor Green
    }
}

# -----------------------------------------------------------------------------
# 4. Ejecutar Preflight Check de diagnóstico (check_health_env.py)
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[4/5] Ejecutando diagnóstico de preflight (check_health_env.py)..." -ForegroundColor Yellow
python check_health_env.py --fix
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ADVERTENCIA] Se detectaron observaciones en el diagnóstico previo." -ForegroundColor Yellow
    $ans = Read-Host "¿Desea iniciar el servidor de todas maneras? (S/N)"
    if ($ans.ToUpper() -ne "S") {
        Write-Host "Inicio cancelado por el usuario." -ForegroundColor Gray
        exit 1
    }
}

# -----------------------------------------------------------------------------
# 5. Iniciar Servidor Uvicorn y Cockpit Central
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "[5/5] Iniciando Quantux ServiceDesk y Cockpit Central..." -ForegroundColor Green
python run_server.py
