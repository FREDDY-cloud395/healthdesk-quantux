#!/usr/bin/env python3
"""
tests/test_mej01_precommit_and_tdd.py
=====================================
Suite de Pruebas de Calidad para el Requerimiento MEJ-01 (5 SP):
"Automatización de Bucle TDD y Pre-commit Hooks para Validadores OJO"

Verifica los 3 Criterios de Aceptación Gherkin definidos en DOC-GOV-008:
- Escenario 1: Bloqueo con Exit Code 1 ante violaciones de Regla OJO (cards, rojos, términos clínicos).
- Escenario 2: Certificación Exit Code 0 en código 100% limpio y conforme.
- Escenario 3: Ejecución de bucle TDD (falla inicial comprobada antes de la solución mínima).
- Verificación del Git Hook pre-commit instalado en el repositorio.
"""

import os
import sys
import tempfile
import subprocess
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestMEJ01PreCommitAndTDD(unittest.TestCase):

    def test_scenario_01_blocking_exit_code_1_on_violations(self):
        """
        Escenario 1: Bloqueo Automatizado en Commit / Compuerta
        DADO un archivo temporal con violaciones OJO (.card, #EF4444, guardia asistencial),
        CUANDO se ejecuta validate_ojo_compliance.py o pre_commit_runner.py,
        ENTONCES el proceso finaliza con Exit Code 1, abortando la entrega y detallando la violación.
        """
        with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False, encoding="utf-8") as tmp:
            tmp.write("""
            <!DOCTYPE html>
            <html>
            <body>
                <div class="ticket-card" style="background: #EF4444;">
                    <span>Atención de Guardia Asistencial</span>
                </div>
            </body>
            </html>
            """)
            tmp_path = tmp.name

        try:
            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "tools", "pre_commit_runner.py"), "--files", tmp_path, "--skip-tests"]
            result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(result.returncode, 1, "Debe finalizar con Exit Code 1 al detectar violaciones")
            self.assertIn("CARD_VIOLATION", result.stdout + result.stderr)
            self.assertIn("RED_COLOR_VIOLATION", result.stdout + result.stderr)
            self.assertIn("CLINICAL_TERMS_VIOLATION", result.stdout + result.stderr)
            print("[OK] MEJ-01 Escenario 1: Bloqueo con Exit Code 1 ante violaciones verificado.")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_scenario_02_certification_exit_code_0_on_clean_code(self):
        """
        Escenario 2: Certificación Verde
        DADO código refactorizado y limpio conforme a las pautas neutrales,
        CUANDO se corre el runner de pre-commit,
        ENTONCES reporta Exit Code 0 ("100% COMPLIANT") y autoriza la integración.
        """
        cmd = [
            sys.executable,
            os.path.join(PROJECT_ROOT, "tools", "pre_commit_runner.py"),
            "--files",
            "frontend/reemplazo-n1.html",
            "frontend/index.html",
            "--skip-tests"
        ]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, f"Debe retornar Exit Code 0 en archivos limpios. Salida:\n{result.stdout}\n{result.stderr}")
        self.assertIn("Regla OJO 100% Compliant", result.stdout)
        print("[OK] MEJ-01 Escenario 2: Certificación Exit Code 0 en código limpio verificado.")

    def test_scenario_03_tdd_loop_execution(self):
        """
        Escenario 3: Automatización del Bucle TDD
        DADO el suite completo de pre-commit runner (linter OJO + tests DOM + tests Backend),
        CUANDO se ejecuta de principio a fin,
        ENTONCES todos los pasos de la compuerta se validan secuencialmente con Exit Code 0.
        """
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "tools", "pre_commit_runner.py")]
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 0, f"El runner completo debe culminar con Exit Code 0:\n{result.stdout}\n{result.stderr}")
        self.assertIn("Suite de Validación Visual DOM: 6/6 tests exitosos", result.stdout)
        self.assertIn("Suite Backend ITIL 4: 5/5 tests exitosos", result.stdout)
        print("[OK] MEJ-01 Escenario 3: Ejecución completa del bucle TDD verificada.")

    def test_precommit_hook_installed_and_configured(self):
        """
        Verificación de instalación del hook .git/hooks/pre-commit
        """
        hook_path = os.path.join(PROJECT_ROOT, ".git", "hooks", "pre-commit")
        self.assertTrue(os.path.exists(hook_path), "El archivo .git/hooks/pre-commit debe existir")
        with open(hook_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("tools/pre_commit_runner.py", content, "El hook debe invocar a tools/pre_commit_runner.py")
        print("[OK] MEJ-01 Git Hook: Archivo .git/hooks/pre-commit verificado y enlazado.")

if __name__ == "__main__":
    unittest.main()
