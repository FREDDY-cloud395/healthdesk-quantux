# HealthDesk Quantux v2.5.0 - PowerShell Launcher
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "          HEALTHDESK QUANTUX — QUANTUX SALUD (v2.5.0 ITIL Edition)" -ForegroundColor White
Write-Host "     Sistema Integral de Mesa de Ayuda y Soporte Hospitalario N1/N2/N3" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Liberar puerto 8000 si está ocupado
try {
    $conn = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Host "[INFO] Liberando proceso previo en puerto 8000 (PID $($conn.OwningProcess))..." -ForegroundColor Yellow
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
    }
} catch {}

# 2. Iniciar servidor
Set-Location -Path $PSScriptRoot
python run_server.py
