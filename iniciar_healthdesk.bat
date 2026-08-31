@echo off
title HealthDesk Quantux - Sistema Integral de Mesa de Ayuda
color 0B
cls
echo =============================================================================
echo                    HEALTHDESK QUANTUX - QUANTUX SALUD
echo           Sistema Integral de Mesa de Ayuda y Soporte Hospitalario
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
echo [2/3] Iniciando Servidor Backend FastAPI en http://127.0.0.1:8000...
cd /d "%~dp0backend"
start "" cmd /c "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
timeout /t 2 /nobreak >nul
echo.
echo [3/3] Abriendo Consola Central de Gestion en el navegador...
start "" "http://127.0.0.1:8000/cockpit"
echo.
echo ============================================================================
echo  HEALTHDESK QUANTUX ESTA EN EJECUCION EXITOSA
echo.
echo  - Consola Central:  http://127.0.0.1:8000/cockpit
echo  - Swagger API Docs: http://127.0.0.1:8000/docs
echo.
echo  Para detener el servidor, cierre la ventana secundaria de Uvicorn.
echo ===========================================================================
echo.
pause
