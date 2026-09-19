#!/usr/bin/env python3
"""
HealthDesk Quantux - Preflight Health & Environment Diagnostic (v4.0.0)
Diagnostica rápidamente el entorno del servidor: Python, paquetes requeridos,
rutas críticas, puertos de red (8000, 3000, 8005), base de datos SQLite y variables .env.

Uso:
    python check_health_env.py
    python check_health_env.py --fix
    python check_health_env.py --json
    python check_health_env.py --ports 8000,3000,8005
"""

import sys
import os
import socket
import sqlite3
import shutil
import argparse
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional

# Configuración de salida en Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Directorio raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
DOCS_DIR = ROOT_DIR / "docs"
UPLOADS_DIR = BACKEND_DIR / "uploads"
DB_PATH = BACKEND_DIR / "healthdesk.db"

# Códigos ANSI para formato de consola
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def print_status(tag: str, msg: str, color: str = Colors.GREEN):
    print(f"  {color}[{tag}]{Colors.RESET} {msg}")

def check_python_version() -> Tuple[bool, str, Dict[str, Any]]:
    min_ver = (3, 10)
    current_ver = sys.version_info
    ver_str = f"{current_ver.major}.{current_ver.minor}.{current_ver.micro}"
    is_venv = (sys.prefix != sys.base_prefix)
    
    details = {
        "version": ver_str,
        "executable": sys.executable,
        "is_virtualenv": is_venv,
        "platform": sys.platform,
        "architecture": "64-bit" if sys.maxsize > 2**32 else "32-bit"
    }

    if current_ver < min_ver:
        return False, f"Python {ver_str} es incompatible. Requiere Python >= 3.10", details
    
    status_msg = f"Python {ver_str} ({details['architecture']}) en {sys.executable}"
    if is_venv:
        status_msg += " [Entorno Virtual: Activo]"
    else:
        status_msg += " [Sistema Global / Standalone]"
    return True, status_msg, details

def check_dependencies() -> Tuple[bool, List[str], List[str], Dict[str, str]]:
    required_pkgs = [
        ("fastapi", "FastAPI Framework"),
        ("uvicorn", "Uvicorn ASGI Server"),
        ("sqlmodel", "SQLModel ORM"),
        ("sqlalchemy", "SQLAlchemy Engine"),
        ("pydantic", "Pydantic Schema Validator"),
        ("pydantic_settings", "Pydantic Settings"),
        ("multipart", "python-multipart (Form/File Uploads)"),
    ]
    optional_pkgs = [
        ("dotenv", "python-dotenv (Environment Loader)"),
        ("psycopg2", "psycopg2-binary (PostgreSQL Driver)"),
    ]

    installed = {}
    missing_required = []
    missing_optional = []

    for mod_name, label in required_pkgs:
        try:
            mod = __import__(mod_name)
            ver = getattr(mod, "__version__", "instalado")
            installed[label] = ver
        except ImportError:
            missing_required.append(label)

    for mod_name, label in optional_pkgs:
        try:
            mod = __import__(mod_name)
            ver = getattr(mod, "__version__", "instalado")
            installed[label] = ver
        except ImportError:
            missing_optional.append(label)

    success = len(missing_required) == 0
    return success, missing_required, missing_optional, installed

def check_filesystem(auto_fix: bool = False) -> Tuple[bool, List[str], List[str]]:
    errors = []
    warnings = []

    # Validar directorios principales
    if not BACKEND_DIR.is_dir():
        errors.append(f"Directorio backend no encontrado: {BACKEND_DIR}")
    if not FRONTEND_DIR.is_dir():
        errors.append(f"Directorio frontend no encontrado: {FRONTEND_DIR}")
    if not DOCS_DIR.is_dir():
        warnings.append(f"Directorio docs no encontrado: {DOCS_DIR}")

    # Validar archivos clave
    key_files = [
        (BACKEND_DIR / "app" / "main.py", "FastAPI app entrypoint"),
        (BACKEND_DIR / "app" / "db" / "session.py", "Database session module"),
        (BACKEND_DIR / "requirements.txt", "Requirements manifest"),
        (FRONTEND_DIR / "index.html", "Cockpit UI principal"),
    ]
    for file_path, desc in key_files:
        if not file_path.is_file():
            errors.append(f"Archivo crítico ausente ({desc}): {file_path}")

    # Validar carpeta uploads
    if not UPLOADS_DIR.exists():
        if auto_fix:
            try:
                UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
                warnings.append(f"Carpeta uploads auto-creada: {UPLOADS_DIR}")
            except Exception as e:
                errors.append(f"No se pudo crear carpeta uploads: {e}")
        else:
            warnings.append(f"Carpeta uploads no existe aún: {UPLOADS_DIR} (se auto-creará al iniciar o con --fix)")
    else:
        # Probar permisos de escritura
        test_file = UPLOADS_DIR / ".write_test"
        try:
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink(missing_ok=True)
        except Exception as e:
            errors.append(f"Permisos insuficientes para escribir en uploads: {e}")

    return len(errors) == 0, errors, warnings

def check_sqlite_database() -> Tuple[bool, str, Dict[str, Any]]:
    details = {"tables": [], "counts": {}, "file_size_mb": 0.0}
    
    if not DB_PATH.is_file():
        return True, f"Base de datos SQLite no inicializada aún en {DB_PATH.name} (se creará automáticamente al iniciar)", details

    file_size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    details["file_size_mb"] = round(file_size_mb, 2)

    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=3.0)
        cursor = conn.cursor()
        
        # Validar integridad SQLite
        cursor.execute("PRAGMA integrity_check;")
        integrity = cursor.fetchone()
        if not integrity or integrity[0] != "ok":
            conn.close()
            return False, f"Falla en verificación de integridad de SQLite: {integrity}", details

        # Listar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
        details["tables"] = tables

        # Contar registros clave
        for table in ["users", "tickets", "platforms", "institutions", "kb_articles"]:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                details["counts"][table] = cursor.fetchone()[0]

        conn.close()
        
        expected_tables = {"users", "tickets", "platforms", "institutions", "kb_articles"}
        missing_tables = expected_tables - set(tables)
        if missing_tables:
            return False, f"Tablas requeridas faltantes en base de datos: {list(missing_tables)}", details

        users_cnt = details["counts"].get("users", 0)
        tickets_cnt = details["counts"].get("tickets", 0)
        kb_cnt = details["counts"].get("kb_articles", 0)
        msg = f"SQLite saludable ({details['file_size_mb']} MB, {len(tables)} tablas | {users_cnt} usuarios, {tickets_cnt} tickets, {kb_cnt} artículos KB)"
        return True, msg, details

    except Exception as e:
        return False, f"Error al inspeccionar base de datos SQLite: {e}", details

def get_process_on_port(port: int) -> Optional[Dict[str, Any]]:
    """Intenta identificar qué proceso está escuchando en un puerto específico en Windows/Linux."""
    if sys.platform == "win32":
        try:
            import subprocess
            cmd = f'netstat -aon | findstr ":{port} "'
            out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            for line in out.strip().splitlines():
                if "LISTENING" in line:
                    parts = line.strip().split()
                    pid = parts[-1]
                    # Buscar nombre de proceso
                    pname = "Desconocido"
                    try:
                        pout = subprocess.check_output(f'tasklist /FI "PID eq {pid}" /FO CSV /NH', shell=True, text=True, stderr=subprocess.DEVNULL)
                        if pout:
                            pname = pout.strip().split(',')[0].strip('"')
                    except Exception:
                        pass
                    return {"pid": pid, "name": pname}
        except Exception:
            return None
    return None

def check_network_port(port: int) -> Dict[str, Any]:
    result = {
        "port": port,
        "is_free": False,
        "process": None,
        "is_quantux_instance": False,
        "health_response": None
    }
    
    # Verificar si el socket puede escuchar
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        # connect_ex devuelve 0 si hay un servidor escuchando
        is_occupied = (s.connect_ex(("127.0.0.1", port)) == 0)
    
    result["is_free"] = not is_occupied
    
    if is_occupied:
        proc = get_process_on_port(port)
        result["process"] = proc
        # Probar si es una instancia activa de Quantux respondiendo en /health
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}/health", headers={"User-Agent": "Quantux-Preflight"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    payload = json.loads(resp.read().decode("utf-8"))
                    result["is_quantux_instance"] = ("Quantux" in payload.get("system", "") or "status" in payload)
                    result["health_response"] = payload
        except Exception:
            pass

    return result

def check_env_file(auto_fix: bool = False) -> Tuple[bool, str, List[str], List[str]]:
    env_file = ROOT_DIR / ".env"
    example_file = ROOT_DIR / ".env.example"
    prod_file = ROOT_DIR / ".env.production"
    
    warnings = []
    errors = []

    if not env_file.is_file():
        if auto_fix and example_file.is_file():
            try:
                shutil.copy(example_file, env_file)
                warnings.append(f"Archivo .env auto-generado a partir de .env.example")
            except Exception as e:
                errors.append(f"No se pudo copiar .env.example a .env: {e}")
        else:
            warnings.append("No se encontró archivo '.env' en la raíz. El sistema utilizará variables de entorno del sistema o valores por defecto.")
    
    # Leer variables cargadas
    active_env = os.environ.get("APP_ENV", "development (default)")
    active_port = os.environ.get("PORT", "8000 (default)")
    secret_key = os.environ.get("SECRET_KEY")
    
    if secret_key and "change-in-vault" in secret_key and active_env == "production":
        warnings.append("SECRET_KEY contiene valor de plantilla predeterminado en entorno de producción.")

    status_msg = f"Entorno: {active_env} | Puerto configurado: {active_port}"
    return len(errors) == 0, status_msg, errors, warnings

def run_preflight_checks(ports: List[int], auto_fix: bool = False) -> Tuple[bool, Dict[str, Any]]:
    report = {
        "status": "PASS",
        "checks": {},
        "summary": {"passed": 0, "warnings": 0, "errors": 0}
    }

    # 1. Python Check
    py_ok, py_msg, py_data = check_python_version()
    report["checks"]["python"] = {"ok": py_ok, "message": py_msg, "details": py_data}
    if py_ok:
        report["summary"]["passed"] += 1
    else:
        report["summary"]["errors"] += 1
        report["status"] = "FAIL"

    # 2. Dependencies Check
    deps_ok, missing_req, missing_opt, installed = check_dependencies()
    report["checks"]["dependencies"] = {
        "ok": deps_ok,
        "missing_required": missing_req,
        "missing_optional": missing_opt,
        "installed": installed
    }
    if deps_ok:
        report["summary"]["passed"] += 1
        if missing_opt:
            report["summary"]["warnings"] += 1
    else:
        report["summary"]["errors"] += 1
        report["status"] = "FAIL"

    # 3. Filesystem Check
    fs_ok, fs_errs, fs_warns = check_filesystem(auto_fix=auto_fix)
    report["checks"]["filesystem"] = {"ok": fs_ok, "errors": fs_errs, "warnings": fs_warns}
    if fs_ok:
        report["summary"]["passed"] += 1
    else:
        report["summary"]["errors"] += 1
        report["status"] = "FAIL"
    report["summary"]["warnings"] += len(fs_warns)

    # 4. Database Check
    db_ok, db_msg, db_data = check_sqlite_database()
    report["checks"]["database"] = {"ok": db_ok, "message": db_msg, "details": db_data}
    if db_ok:
        report["summary"]["passed"] += 1
    else:
        report["summary"]["errors"] += 1
        report["status"] = "FAIL"

    # 5. Network Ports Check
    port_results = []
    has_port_conflict = False
    for p in ports:
        res = check_network_port(p)
        port_results.append(res)
    report["checks"]["ports"] = port_results
    report["summary"]["passed"] += 1

    # 6. Environment Check
    env_ok, env_msg, env_errs, env_warns = check_env_file(auto_fix=auto_fix)
    report["checks"]["environment"] = {"ok": env_ok, "message": env_msg, "errors": env_errs, "warnings": env_warns}
    if env_ok:
        report["summary"]["passed"] += 1
    else:
        report["summary"]["errors"] += 1
        report["status"] = "FAIL"
    report["summary"]["warnings"] += len(env_warns)

    return (report["status"] == "PASS"), report

def print_cli_report(report: Dict[str, Any], ports: List[int]):
    print(f"\n{Colors.CYAN}{Colors.BOLD}============================================================================{Colors.RESET}")
    print(f"{Colors.BOLD}      HEALTHDESK QUANTUX — PREFLIGHT HEALTH & ENVIRONMENT CHECK (v4.0.0){Colors.RESET}")
    print(f"{Colors.CYAN}============================================================================{Colors.RESET}\n")

    # 1. Python
    py = report["checks"]["python"]
    if py["ok"]:
        print_status("OK", f"Python Runtime: {py['message']}", Colors.GREEN)
    else:
        print_status("ERROR", f"Python Runtime: {py['message']}", Colors.RED)

    # 2. Dependencies
    deps = report["checks"]["dependencies"]
    if deps["ok"]:
        pkg_summary = f"{len(deps['installed'])} paquetes validados (FastAPI, Uvicorn, SQLModel, Pydantic, etc.)"
        print_status("OK", f"Dependencias Core: {pkg_summary}", Colors.GREEN)
        if deps["missing_optional"]:
            print_status("INFO", f"Paquetes opcionales no detectados: {', '.join(deps['missing_optional'])}", Colors.BLUE)
    else:
        print_status("ERROR", f"Faltan paquetes requeridos: {', '.join(deps['missing_required'])}", Colors.RED)
        print(f"       -> Instale con: {Colors.BOLD}pip install -r backend/requirements.txt{Colors.RESET}")

    # 3. Filesystem
    fs = report["checks"]["filesystem"]
    if fs["ok"]:
        print_status("OK", "Estructura del Proyecto y Archivos Clave: Integridad verificada", Colors.GREEN)
    else:
        for err in fs["errors"]:
            print_status("ERROR", f"Estructura: {err}", Colors.RED)
    for warn in fs["warnings"]:
        print_status("WARN", f"Estructura: {warn}", Colors.YELLOW)

    # 4. Database
    db = report["checks"]["database"]
    if db["ok"]:
        print_status("OK", f"Base de Datos: {db['message']}", Colors.GREEN)
    else:
        print_status("ERROR", f"Base de Datos: {db['message']}", Colors.RED)

    # 5. Network Ports
    print("\n  " + Colors.BOLD + "-- Verificación de Puertos de Red --" + Colors.RESET)
    for p in report["checks"]["ports"]:
        port_num = p["port"]
        if p["is_free"]:
            print_status("OK", f"Puerto {port_num}: DISPONIBLE y listo para escuchar", Colors.GREEN)
        else:
            proc_info = ""
            if p["process"]:
                proc_info = f" [PID {p['process']['pid']} - {p['process']['name']}]"
            
            if p["is_quantux_instance"]:
                print_status("INFO", f"Puerto {port_num}: OCUPADO por instancia activa de Quantux ServiceDesk{proc_info} (Salud: ONLINE)", Colors.CYAN)
            else:
                print_status("WARN", f"Puerto {port_num}: OCUPADO por otro proceso{proc_info}", Colors.YELLOW)
                print(f"         (Los scripts de inicio pueden liberar este puerto automáticamente)")

    # 6. Environment
    env = report["checks"]["environment"]
    print("\n  " + Colors.BOLD + "-- Configuración de Entorno (.env) --" + Colors.RESET)
    if env["ok"]:
        print_status("OK", f"Configuración: {env['message']}", Colors.GREEN)
    for warn in env["warnings"]:
        print_status("WARN", warn, Colors.YELLOW)
    for err in env["errors"]:
        print_status("ERROR", err, Colors.RED)

    # Resumen Final
    summary = report["summary"]
    print(f"\n{Colors.CYAN}----------------------------------------------------------------------------{Colors.RESET}")
    if report["status"] == "PASS":
        status_banner = f"{Colors.GREEN}{Colors.BOLD}✔ PREFLIGHT CHECK EXITOSO{Colors.RESET}"
    else:
        status_banner = f"{Colors.RED}{Colors.BOLD}✖ PREFLIGHT CHECK CON OBSERVACIONES CRÍTICAS{Colors.RESET}"
    
    print(f"  Estado Global: {status_banner}")
    print(f"  Métricas: {Colors.GREEN}{summary['passed']} Aprobados{Colors.RESET} | {Colors.YELLOW}{summary['warnings']} Advertencias{Colors.RESET} | {Colors.RED}{summary['errors']} Errores{Colors.RESET}")
    print(f"{Colors.CYAN}============================================================================{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="HealthDesk Quantux - Preflight Diagnostic Tool")
    parser.add_argument("--ports", type=str, default="8000,3000,8005", help="Puertos separados por coma a verificar (ej. 8000,3000,8005)")
    parser.add_argument("--fix", action="store_true", help="Auto-repara problemas comunes (crea directorios, genera .env)")
    parser.add_argument("--json", action="store_true", help="Genera reporte estructurado en formato JSON")
    parser.add_argument("--quiet", action="store_true", help="Suprime salida en consola, solo retorna código de salida")
    
    args = parser.parse_args()

    port_list = []
    for p in args.ports.split(","):
        p = p.strip()
        if p.isdigit():
            port_list.append(int(p))
    if not port_list:
        port_list = [8000, 3000, 8005]

    is_success, report = run_preflight_checks(ports=port_list, auto_fix=args.fix)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif not args.quiet:
        print_cli_report(report, port_list)

    sys.exit(0 if is_success else 1)

if __name__ == "__main__":
    main()
