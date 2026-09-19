#!/usr/bin/env python3
"""
Quantux HealthDesk - Full Project Safeguard & Snapshot Tool
Creates a timestamped complete ZIP snapshot of the entire project,
including source code, tests, docs, configs, and verified database.
"""
import os
import sys
import zipfile
import hashlib
from datetime import datetime
from pathlib import Path

# Force UTF-8 on Windows stdout if possible
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
BACKUP_DIR = ROOT_DIR / "backups_archive"
BACKUP_DIR.mkdir(exist_ok=True)

# Ignored directory names and patterns
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    "qa_screenshots",
    "scratch",
    ".idea",
    ".vscode",
    "backups_archive"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".tmp",
    ".db-shm",
    ".db-wal",
    ".db-journal"
}

def calculate_sha256(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_full_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"quantux_healthdesk_v4_FULL_BACKUP_{timestamp}.zip"
    zip_path = BACKUP_DIR / zip_name

    print(f"[+] Iniciando empaquetado y resguardo integral en: {zip_path}")
    
    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_p = Path(root) / file
                
                # Check extension exclusions
                if file_p.suffix.lower() in EXCLUDE_EXTENSIONS:
                    continue
                
                # Skip the archive zip itself if somehow matched
                if file_p.resolve() == zip_path.resolve():
                    continue

                rel_path = file_p.relative_to(ROOT_DIR)
                zipf.write(file_p, arcname=str(rel_path))
                file_count += 1
                total_uncompressed_bytes += file_p.stat().st_size

    archive_size_bytes = zip_path.stat().st_size
    archive_size_mb = round(archive_size_bytes / (1024 * 1024), 2)
    uncompressed_mb = round(total_uncompressed_bytes / (1024 * 1024), 2)
    checksum = calculate_sha256(zip_path)

    print("=================================================================")
    print("[OK] RESGUARDO INTEGRAL DE PROYECTO COMPLETADO")
    print("=================================================================")
    print(f"Directorio de Respaldo: {zip_path}")
    print(f"Archivos incluidos:     {file_count}")
    print(f"Tamano Comprimido:      {archive_size_mb} MB ({archive_size_bytes:,} bytes)")
    print(f"Tamano Original:        {uncompressed_mb} MB ({total_uncompressed_bytes:,} bytes)")
    print(f"SHA256 Checksum:        {checksum}")
    print("=================================================================")

if __name__ == "__main__":
    create_full_backup()
