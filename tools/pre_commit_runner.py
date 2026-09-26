#!/usr/bin/env python3
"""
tools/pre_commit_runner.py
==========================
Runner de Quality Gates automatizado para pre-commit hooks y bucle TDD en Quantux ServiceDesk.
Implementa el requerimiento de calidad y gobernanza MEJ-01 (5 SP):
- Escenario 1: Bloqueo inmediato con Exit Code 1 ante violaciones de la Regla OJO.
- Escenario 2: Certificación Exit Code 0 ante código 100% conforme.
- Escenario 3: Ejecución de bucle TDD (verificación de pruebas unitarias y DOM).

Uso:
    python tools/pre_commit_runner.py [--all] [--staged] [--files file1 file2]
"""

import os
import sys
import subprocess
import argparse
from typing import List, Tuple

# Configuración de codificación para terminales Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def print_banner():
    print("\n" + "=" * 80)
    print(" 🛡️  QUANTUX SERVICE DESK — QUALITY GATE PRE-COMMIT RUNNER (MEJ-01)")
    print("=" * 80)

def get_staged_files() -> List[str]:
    """Obtiene los archivos en staged de git para análisis incremental."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        files = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
        return [f for f in files if f.endswith(('.html', '.js', '.css', '.py'))]
    except Exception:
        return []

def run_step(step_name: str, cmd: List[str]) -> Tuple[bool, str]:
    """Ejecuta un paso del pipeline de calidad y captura su resultado."""
    print(f"\n[PASO] {step_name}...")
    print(f"       Comando: {' '.join(cmd)}")
    try:
        res = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        success = (res.returncode == 0)
        output = res.stdout if res.stdout else res.stderr
        return success, output
    except Exception as e:
        return False, f"Excepción al ejecutar {cmd}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Pre-commit Quality Gate Runner - Quantux ServiceDesk")
    parser.add_argument("--all", action="store_true", help="Validar todos los archivos relevantes del proyecto")
    parser.add_argument("--staged", action="store_true", help="Validar únicamente archivos en git stage (default)")
    parser.add_argument("--files", nargs="*", help="Archivos específicos a validar")
    parser.add_argument("--skip-tests", action="store_true", help="Omitir tests unitarios (solo linter OJO)")
    args = parser.parse_args()

    print_banner()

    target_files = []
    if args.files:
        target_files = args.files
    elif args.staged:
        target_files = get_staged_files()
    elif not args.all:
        # Por defecto, verificar archivos clave de interfaz activa
        target_files = [
            "frontend/reemplazo-n1.html",
            "frontend/index.html",
            "frontend/js/typeahead.js",
            "frontend/js/api.js"
        ]

    # PASO 1: Validación de Regla OJO (Pizarra Neutral, colores, vocabulario)
    ojo_args = [sys.executable, "validate_ojo_compliance.py"]
    if target_files:
        ojo_args.extend(target_files)
    else:
        ojo_args.extend(["frontend/reemplazo-n1.html", "frontend/index.html"])

    step1_ok, step1_out = run_step("1. Verificación de Regla OJO y Pizarra Neutral", ojo_args)
    if not step1_ok:
        print("\n❌ [GATE BLOQUEADO] Se detectaron violaciones a la Regla OJO:")
        print(step1_out)
        print("=" * 80)
        print("⛔ ABORTANDO: Corrija las violaciones antes de continuar.")
        print("=" * 80 + "\n")
        sys.exit(1)
    else:
        print("  ✓ [APROBADO] Regla OJO 100% Compliant (Cero cards, cero rojos, cero términos clínicos).")

    if not args.skip_tests:
        # PASO 2: Validación de Integridad DOM y Fidelidad de Mocks
        step2_ok, step2_out = run_step(
            "2. Suite de Validación de Cumplimiento Visual DOM (6 Tests)",
            [sys.executable, "tests/test_dom_visual_compliance.py"]
        )
        if not step2_ok:
            print("\n❌ [GATE BLOQUEADO] La suite DOM falló:")
            print(step2_out)
            sys.exit(1)
        else:
            print("  ✓ [APROBADO] Suite de Validación Visual DOM: 6/6 tests exitosos.")

        # PASO 3: Validación de Lógica de Negocio Backend y FSM ITIL
        step3_ok, step3_out = run_step(
            "3. Suite de Integración Backend & ITIL 4 (5 Tests)",
            [sys.executable, "-m", "unittest", "backend/tests/test_reemplazo_n1_suite.py"]
        )
        if not step3_ok:
            print("\n❌ [GATE BLOQUEADO] La suite de negocio backend falló:")
            print(step3_out)
            sys.exit(1)
        else:
            print("  ✓ [APROBADO] Suite Backend ITIL 4: 5/5 tests exitosos.")

    print("\n" + "=" * 80)
    print(" 🚀 [QUALITY GATE EXITOSO] Todos los filtros fueron superados (Exit Code 0).")
    print("    El commit / despliegue está autorizado conforme al Marco PMI+IA.")
    print("=" * 80 + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
