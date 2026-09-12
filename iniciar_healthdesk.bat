@echo off
title HealthDesk Quantux v2.5.0 - Sistema Integral de Mesa de Ayuda
color 0B
cls
echo ============================================================================
echo           HEALTHDESK QUANTUX — QUANTUX SALUD (v2.5.0 ITIL Edition)
echo      Sistema Integral de Mesa de Ayuda y Soporte Hospitalario N1/N2/N3
echo ============================================================================
echo.
echo [1/3] Verificando entorno Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no se encuentra instalado o no esta en el PATH.
    echo Por favor instale Python 3.10+ para continuar.
    pause
    exit /b 1
)
echo [OK] Python detectado correctamente.
echo.
echo [2/3] Liberando puerto 8000 en caso de instancias colgadas previas...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    echo [INFO] Cerrando proceso previo en puerto 8000 [PID %%a]
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Puerto 8000 disponible.
echo.
echo [3/3] Iniciando Sistema y Cockpit Central...
cd /d "%~dp0"
python run_server.py
pause
