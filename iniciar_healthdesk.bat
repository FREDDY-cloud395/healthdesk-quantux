@echo off
setlocal enabledelayedexpansion
title HealthDesk Quantux v4.0.0 - Sistema Integral de Mesa de Ayuda
color 0B
cls

echo ============================================================================
echo           HEALTHDESK QUANTUX — QUANTUX SALUD (v4.0.0 Enterprise ITIL)
echo      Sistema Integral de Mesa de Ayuda y Soporte Hospitalario N1/N2/N3
echo ============================================================================
echo.

cd /d "%~dp0"

:: -----------------------------------------------------------------------------
:: PASO 1: Validar presencia de Python en PATH
:: -----------------------------------------------------------------------------
echo [1/5] Verificando instalacion de Python en PATH...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo [ERROR CRITICO] Python no se encuentra instalado o no esta en el PATH.
    echo Por favor instale Python 3.10 o superior desde https://www.python.org/
    echo y asegurese de marcar la casilla "Add Python to PATH".
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [OK] %PY_VER% detectado en el sistema.

:: -----------------------------------------------------------------------------
:: PASO 2: Validar version minima de Python (>= 3.10)
:: -----------------------------------------------------------------------------
echo.
echo [2/5] Validando compatibilidad de version de Python...
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo [ERROR CRITICO] La version actual de Python es menor a 3.10.
    echo Se requiere Python 3.10, 3.11, 3.12 o 3.14 para ejecutar Quantux ServiceDesk.
    echo.
    pause
    exit /b 1
)
echo [OK] Version de Python compatible (>= 3.10).

:: -----------------------------------------------------------------------------
:: PASO 3: Validar dependencias y paquetes requeridos de Python
:: -----------------------------------------------------------------------------
echo.
echo [3/5] Verificando paquetes y dependencias (FastAPI, Uvicorn, SQLModel, etc.)...
python -c "import fastapi, uvicorn, sqlmodel, pydantic, sqlalchemy, multipart" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Se detectaron paquetes faltantes en el entorno.
    echo Instalando requerimientos desde backend\requirements.txt...
    python -m pip install --upgrade pip
    python -m pip install -r backend\requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        color 0C
        echo.
        echo [ERROR] No se pudieron instalar las dependencias necesarias.
        echo Revise su conexion a Internet o permisos e intente nuevamente.
        echo.
        pause
        exit /b 1
    )
    echo [OK] Paquetes instalados satisfactoriamente.
) else (
    echo [OK] Todos los paquetes requeridos estan disponibles.
)

:: -----------------------------------------------------------------------------
:: PASO 4: Validar y liberar puertos 8000 y 3000 en caso de instancias colgadas
:: -----------------------------------------------------------------------------
echo.
echo [4/5] Verificando y liberando puertos de red (8000, 3000)...

:: Puerto 8000
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    echo [INFO] Cerrando proceso previo colgado en puerto 8000 [PID %%a]...
    taskkill /F /PID %%a >nul 2>&1
)

:: Puerto 3000
for /f "tokens=5" %%b in ('netstat -aon 2^>nul ^| findstr :3000 ^| findstr LISTENING') do (
    echo [INFO] Cerrando proceso previo colgado en puerto 3000 [PID %%b]...
    taskkill /F /PID %%b >nul 2>&1
)

:: Breve espera para liberar sockets TCP
timeout /t 1 /nobreak >nul 2>&1
echo [OK] Puertos 8000 y 3000 listos y disponibles.

:: -----------------------------------------------------------------------------
:: PASO 5: Diagnóstico Preflight rápido del entorno (.env, SQLite, carpetas)
:: -----------------------------------------------------------------------------
echo.
echo [5/5] Ejecutando verificacion preflight del entorno (check_health_env.py)...
python check_health_env.py --fix
if %ERRORLEVEL% NEQ 0 (
    color 0E
    echo.
    echo [ADVERTENCIA] El diagnostico preflight detecto inconsistencias.
    echo Revise el reporte anterior. Desea continuar de todos modos? (S/N)
    set /p RESP="> "
    if /i "!RESP!" NEQ "S" (
        echo Cancelando inicio.
        pause
        exit /b 1
    )
)

:: -----------------------------------------------------------------------------
:: INICIO DEL SERVIDOR
:: -----------------------------------------------------------------------------
echo.
echo ============================================================================
echo   Iniciando Plataforma Quantux ServiceDesk y Cockpit Central...
echo ============================================================================
echo.
python run_server.py
pause
