#!/usr/bin/env python3
"""
================================================================================
Quantux HealthDesk - Módulo de Respaldo y Mantenimiento Seguro de Base de Datos
================================================================================
Este script implementa copias de respaldo en caliente (Zero Downtime / Non-blocking)
utilizando el API Online Backup de SQLite3, verificación de integridad física y
lógica (PRAGMA integrity_check / foreign_key_check), optimización de estadísticas
del query planner y política de retención automática de copias históricas.

Uso:
    python backup_db.py --backup              # Genera backup en caliente con timestamp
    python backup_db.py --check               # Ejecuta chequeo de integridad física y lógica
    python backup_db.py --optimize            # Ejecuta PRAGMA optimize y WAL checkpoint
    python backup_db.py --all                 # Ejecuta pipeline completo de mantenimiento
    python backup_db.py --all --json          # Salida estructurada JSON para monitoreo
================================================================================
"""

import sys
import os
import argparse
import time
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Configuración de directorios por defecto
BACKEND_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BACKEND_DIR / "healthdesk.db"
DEFAULT_BACKUP_DIR = BACKEND_DIR / "backups"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("quantux_backup")


class DatabaseMaintenanceManager:
    def __init__(self, db_path: Path = DEFAULT_DB_PATH, backup_dir: Path = DEFAULT_BACKUP_DIR):
        self.db_path = Path(db_path).resolve()
        self.backup_dir = Path(backup_dir).resolve()
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def check_database_exists(self) -> bool:
        return self.db_path.exists() and self.db_path.stat().st_size > 0

    def verify_integrity(self, target_path: Path = None) -> dict:
        """
        Ejecuta verificación exhaustiva de integridad física y lógica:
        1. PRAGMA integrity_check
        2. PRAGMA quick_check
        3. PRAGMA foreign_key_check
        """
        db_file = target_path or self.db_path
        if not db_file.exists():
            return {
                "success": False,
                "target": str(db_file),
                "error": "El archivo de base de datos no existe"
            }

        report = {
            "target": str(db_file),
            "size_bytes": db_file.stat().st_size,
            "physical_integrity_ok": False,
            "quick_check_ok": False,
            "foreign_keys_ok": False,
            "foreign_key_violations": [],
            "errors": []
        }

        try:
            # Abrir en modo de solo lectura (read-only) para no bloquear concurrentes
            conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True, timeout=10.0)
            cursor = conn.cursor()

            # 1. Quick Check (rápido)
            cursor.execute("PRAGMA quick_check;")
            qc_result = cursor.fetchall()
            report["quick_check_ok"] = (len(qc_result) == 1 and qc_result[0][0].lower() == "ok")

            # 2. Integrity Check (completo)
            cursor.execute("PRAGMA integrity_check;")
            ic_result = cursor.fetchall()
            report["physical_integrity_ok"] = (len(ic_result) == 1 and ic_result[0][0].lower() == "ok")
            if not report["physical_integrity_ok"]:
                report["errors"].extend([r[0] for r in ic_result])

            # 3. Foreign Key Check (lógica relacional)
            cursor.execute("PRAGMA foreign_key_check;")
            fk_violations = cursor.fetchall()
            if not fk_violations:
                report["foreign_keys_ok"] = True
            else:
                report["foreign_keys_ok"] = False
                report["foreign_key_violations_count"] = len(fk_violations)
                # Muestra de violaciones representativas
                report["foreign_key_violations"] = [
                    {"table": v[0], "rowid": v[1], "parent_table": v[2], "fkid": v[3]}
                    for v in fk_violations[:10]
                ]

            conn.close()
            report["success"] = report["physical_integrity_ok"] and report["foreign_keys_ok"]
        except Exception as e:
            report["success"] = False
            report["errors"].append(str(e))

        return report

    def create_online_backup(self, max_pages_per_step: int = 250) -> dict:
        """
        Crea una copia de seguridad en caliente (online, non-blocking) usando
        la API sqlite3.Connection.backup().
        Esta técnica permite que los hilos y clientes de FastAPI sigan leyendo
        y escribiendo concurrentemente sin recibir 'database is locked'.
        """
        if not self.check_database_exists():
            return {
                "success": False,
                "error": f"Base de datos de origen inexistente o vacía: {self.db_path}"
            }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"healthdesk_backup_{timestamp}.db"
        dest_path = self.backup_dir / backup_filename

        start_time = time.time()
        pages_stat = {"copied": 0, "total": 0}

        def backup_progress(status, remaining, total):
            pages_stat["copied"] = total - remaining
            pages_stat["total"] = total

        try:
            logger.info(f"Iniciando respaldo en caliente: {self.db_path} -> {dest_path}")
            # Conexión origen en modo read-only
            src_conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True, timeout=15.0)
            dest_conn = sqlite3.connect(str(dest_path), timeout=15.0)

            # Ejecución en bloques de páginas para ceder I/O al motor concurrentemente
            src_conn.backup(dest_conn, pages=max_pages_per_step, progress=backup_progress)

            dest_conn.close()
            src_conn.close()

            elapsed = round(time.time() - start_time, 3)
            size_bytes = dest_path.stat().st_size

            # Inmediatamente verificar la integridad de la copia generada
            verification = self.verify_integrity(dest_path)

            return {
                "success": verification.get("physical_integrity_ok", False),
                "backup_file": str(dest_path),
                "backup_filename": backup_filename,
                "timestamp": timestamp,
                "elapsed_seconds": elapsed,
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / (1024 * 1024), 2),
                "pages_copied": pages_stat["copied"],
                "total_pages": pages_stat["total"],
                "verification": verification
            }
        except Exception as e:
            logger.error(f"Error generando respaldo en caliente: {e}")
            if dest_path.exists():
                try:
                    dest_path.unlink()
                except Exception:
                    pass
            return {
                "success": False,
                "error": str(e)
            }

    def optimize_database(self) -> dict:
        """
        Ejecuta operaciones de mantenimiento proactivo:
        - PRAGMA wal_checkpoint(PASSIVE) para sincronizar logs WAL con el archivo principal.
        - PRAGMA optimize para recopilar estadísticas de índices para el planificador de consultas.
        """
        if not self.check_database_exists():
            return {"success": False, "error": "Base de datos no encontrada"}

        report = {"success": True, "actions": []}
        try:
            conn = sqlite3.connect(str(self.db_path), timeout=10.0)
            cursor = conn.cursor()

            # 1. Check WAL mode
            cursor.execute("PRAGMA journal_mode;")
            jmode = cursor.fetchone()[0]
            report["journal_mode"] = jmode

            # 2. Checkpoint WAL si aplica
            if jmode.lower() == "wal":
                cursor.execute("PRAGMA wal_checkpoint(PASSIVE);")
                ckpt = cursor.fetchone()
                report["actions"].append(f"WAL checkpoint PASSIVE: busy={ckpt[0]}, log={ckpt[1]}, ckpt={ckpt[2]}")

            # 3. Optimize query planner
            cursor.execute("PRAGMA optimize;")
            report["actions"].append("PRAGMA optimize ejecutado correctamente")

            conn.commit()
            conn.close()
        except Exception as e:
            report["success"] = False
            report["error"] = str(e)

        return report

    def purge_old_backups(self, retention_days: int = 7, min_keep: int = 5) -> dict:
        """
        Aplica política de retención para no saturar disco:
        - Elimina backups que superen 'retention_days'.
        - Garantiza siempre conservar al menos 'min_keep' copias más recientes.
        """
        backups = sorted(
            [f for f in self.backup_dir.glob("healthdesk_backup_*.db") if f.is_file()],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        cutoff = datetime.now() - timedelta(days=retention_days)
        deleted = []
        kept = []

        for idx, bkp in enumerate(backups):
            bkp_mtime = datetime.fromtimestamp(bkp.stat().st_mtime)
            # Conservar si está dentro de min_keep o más reciente que cutoff
            if idx < min_keep or bkp_mtime >= cutoff:
                kept.append(bkp.name)
            else:
                try:
                    bkp.unlink()
                    deleted.append(bkp.name)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar backup antiguo {bkp.name}: {e}")

        return {
            "total_found": len(backups),
            "kept_count": len(kept),
            "deleted_count": len(deleted),
            "deleted_files": deleted
        }

    def run_full_pipeline(self, retention_days: int = 7) -> dict:
        """
        Ejecuta el ciclo de vida completo de mantenimiento:
        1. Verificación inicial de la base activa
        2. Respaldo online seguro
        3. Verificación de la copia
        4. Optimización de índices y estadísticas
        5. Purga de respaldos antiguos
        """
        pipeline_start = time.time()
        logger.info("=================================================================")
        logger.info("QUANTUX HEALTHDESK - EJECUCIÓN PIPELINE DE MANTENIMIENTO DBA")
        logger.info("=================================================================")

        # 1. Verificación inicial
        logger.info("[1/4] Verificando integridad de base activa...")
        pre_check = self.verify_integrity()

        # 2. Respaldo Online
        logger.info("[2/4] Generando copia de respaldo en caliente (Online Backup API)...")
        backup_result = self.create_online_backup()

        # 3. Optimización
        logger.info("[3/4] Optimizando base de datos y planificador...")
        opt_result = self.optimize_database()

        # 4. Purga
        logger.info("[4/4] Aplicando políticas de retención histórica...")
        retention_result = self.purge_old_backups(retention_days=retention_days)

        elapsed = round(time.time() - pipeline_start, 3)
        overall_success = pre_check.get("physical_integrity_ok", False) and backup_result.get("success", False)

        result = {
            "success": overall_success,
            "pipeline_elapsed_seconds": elapsed,
            "timestamp": datetime.now().isoformat(),
            "pre_check": pre_check,
            "backup": backup_result,
            "optimization": opt_result,
            "retention": retention_result
        }

        if overall_success:
            logger.info(f"Pipeline de mantenimiento DBA completado con ÉXITO en {elapsed}s.")
        else:
            logger.error(f"Pipeline de mantenimiento DBA finalizó con ADVERTENCIAS/ERRORES.")

        return result


def main():
    parser = argparse.ArgumentParser(
        description="Quantux HealthDesk - Herramienta de Respaldo y Mantenimiento de Base de Datos"
    )
    parser.add_argument("--backup", action="store_true", help="Genera copia en caliente de la base de datos")
    parser.add_argument("--check", action="store_true", help="Ejecuta chequeo de integridad física y lógica")
    parser.add_argument("--optimize", action="store_true", help="Ejecuta PRAGMA optimize y WAL checkpoint")
    parser.add_argument("--all", action="store_true", help="Ejecuta ciclo completo: backup, check, optimize y purge")
    parser.add_argument("--retention-days", type=int, default=7, help="Días de retención para copias antiguas (default: 7)")
    parser.add_argument("--target", type=str, default=str(DEFAULT_DB_PATH), help="Ruta a la base de datos objetivo")
    parser.add_argument("--backup-dir", type=str, default=str(DEFAULT_BACKUP_DIR), help="Directorio de destino de backups")
    parser.add_argument("--json", action="store_true", help="Imprime el resultado en formato JSON estructurado")

    args = parser.parse_args()
    mgr = DatabaseMaintenanceManager(db_path=Path(args.target), backup_dir=Path(args.backup_dir))

    # Si no se pasó ninguna opción de acción, por defecto ejecutar --check
    if not (args.backup or args.check or args.optimize or args.all):
        args.check = True

    output = {}

    if args.all:
        output = mgr.run_full_pipeline(retention_days=args.retention_days)
    else:
        if args.check:
            output["check"] = mgr.verify_integrity()
        if args.backup:
            output["backup"] = mgr.create_online_backup()
        if args.optimize:
            output["optimize"] = mgr.optimize_database()

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        # Formato texto para consola
        if "check" in output:
            chk = output["check"]
            fk_msg = "OK (0 violaciones)" if chk.get("foreign_keys_ok") else f"FALLÓ ({chk.get('foreign_key_violations_count', 0)} violaciones)"
            print("\n--- REPORTE DE INTEGRIDAD ---")
            print(f"Archivo: {chk.get('target')}")
            print(f"Integridad Física (PRAGMA integrity_check): {'OK' if chk.get('physical_integrity_ok') else 'FALLÓ'}")
            print(f"Chequeo Rápido (PRAGMA quick_check): {'OK' if chk.get('quick_check_ok') else 'FALLÓ'}")
            print(f"Integridad Relacional (PRAGMA foreign_key_check): {fk_msg}")
            if chk.get("errors"):
                print("Errores encontrados:")
                for err in chk["errors"]:
                    print(f"  * {err}")

        if "backup" in output:
            bk = output["backup"]
            print("\n--- REPORTE DE RESPALDO ---")
            if bk.get("success"):
                print(f"Archivo generado: {bk.get('backup_file')}")
                print(f"Tamaño: {bk.get('size_mb')} MB ({bk.get('size_bytes'):,} bytes)")
                print(f"Páginas copiadas: {bk.get('pages_copied')} de {bk.get('total_pages')}")
                print(f"Tiempo de ejecución: {bk.get('elapsed_seconds')} segundos")
                print(f"Verificación de la copia: {'OK' if bk.get('verification', {}).get('physical_integrity_ok') else 'FALLÓ'}")
            else:
                print(f"ERROR en respaldo: {bk.get('error')}")

        if "optimize" in output:
            opt = output["optimize"]
            print("\n--- REPORTE DE OPTIMIZACIÓN ---")
            print(f"Journal Mode: {opt.get('journal_mode', 'N/A')}")
            for act in opt.get("actions", []):
                print(f"  * {act}")

    # Determinar código de salida
    success = True
    if "success" in output and not output["success"]:
        success = False
    if "check" in output and not output["check"].get("success", False):
        success = False
    if "backup" in output and not output["backup"].get("success", False):
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
