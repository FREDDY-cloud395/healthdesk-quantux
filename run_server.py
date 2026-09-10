"""
HealthDesk Quantux - Robust Server Launcher (v2.5.0 ITIL Edition)
Ejecuta migraciones automáticas, verifica la base de datos e inicia FastAPI / Uvicorn.
"""
import sys
import os
import time
import socket
import webbrowser
import threading
from pathlib import Path

# Ajustar PYTHONPATH para incluir backend
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

def check_port_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) != 0

def open_browser_delayed(url: str, delay: float = 1.5):
    def _target():
        time.sleep(delay)
        print(f"\n🚀 Abriendo navegador en: {url}\n")
        try:
            webbrowser.open(url)
        except Exception:
            pass
    t = threading.Thread(target=_target, daemon=True)
    t.start()

def main():
    print("=" * 76)
    print("          HEALTHDESK QUANTUX — QUANTUX SALUD (v2.5.0 ITIL Edition)")
    print("    Sistema de Mesa de Ayuda con Escalamiento ITIL (N1 / N2 / N3)")
    print("=" * 76)
    
    # 1. Inicialización y Migración de Base de Datos SQLite
    print("\n[1/3] Verificando esquema y migraciones de base de datos SQLite...")
    try:
        from app.db.session import init_db
        from app.db.seed import run_seed
        init_db()
        run_seed()
        print("  ✓ Base de datos validada y sincronizada correctamente.")
    except Exception as e:
        print(f"  ❌ Error en inicialización de base de datos: {e}")
        sys.exit(1)

    # 2. Comprobar puerto 8000
    host = "127.0.0.1"
    port = 8000
    print(f"\n[2/3] Verificando disponibilidad de puerto {port}...")
    if not check_port_free(host, port):
        print(f"  ⚠️  El puerto {port} está ocupado por otra instancia.")
        print(f"  Se intentará conectar directamente o reusar el puerto.")
    else:
        print(f"  ✓ Puerto {port} libre y listo para escuchar.")

    # 3. Lanzar Uvicorn
    cockpit_url = f"http://{host}:{port}/cockpit"
    docs_url = f"http://{host}:{port}/docs"
    
    print("\n[3/3] Iniciando Servidor Uvicorn...")
    print(f"  📍 Cockpit Operativo:  {cockpit_url}")
    print(f"  📍 Swagger API Docs:   {docs_url}")
    print(f"  📍 Configuración ITIL: {cockpit_url}#config")
    print("\nPresione CTRL+C para detener el servicio.\n" + "-" * 76)

    open_browser_delayed(cockpit_url, delay=1.2)

    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        app_dir=str(BACKEND_DIR),
        log_level="info"
    )

if __name__ == "__main__":
    main()
