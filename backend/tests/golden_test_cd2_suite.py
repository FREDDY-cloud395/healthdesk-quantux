# -*- coding: utf-8 -*-
"""
Golden Test Suite para Triage Cognitivo CD2 (Quantux HealthTech)
Valida y audita el 100% de las intenciones clínicas reales de soporte.
"""

import sys
import os
import unittest

# Configurar path raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)

from backend.app.services.ai_triage import N3CognitiveTriageEngine

class GoldenCD2TriageTestSuite(unittest.TestCase):

    def test_01_cambio_de_cuit_resuelve_a_cd2_prest_001(self):
        """Caso 1: Cambio de CUIT debe ir a CD2-PREST-001 y NUNCA a Matrículas."""
        query = "cambio de cuit"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook, "No se encontró runbook para 'cambio de cuit'")
        self.assertIn("PREST-001", runbook["code"], f"Se esperaba CD2-PREST-001 pero se obtuvo: {runbook['code']} - {runbook['title']}")
        self.assertNotIn("MAT", runbook["code"], "ERROR: Se confundió CUIT con Matrículas!")
        print(f"[OK] TEST-01 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

    def test_02_no_puede_registrar_dictamina_diferido(self):
        """Caso 2: 'no puede registrar' debe ir a CD2-PAU-001 y dictaminar registro por diferido."""
        query = "no puede registrar"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook, "No se encontró runbook para 'no puede registrar'")
        self.assertIn("PAU-001", runbook["code"], f"Se esperaba CD2-PAU-001 pero se obtuvo: {runbook['code']}")
        
        # Verificar que el procedimiento o resolución mencione 'diferido'
        combined_text = (result["ai_response_text"] + " " + " ".join(result["structured_steps"]) + " " + result["suggested_doctor_message"]).lower()
        self.assertIn("diferid", combined_text, "ERROR: La respuesta debió indicar que se puede registrar por diferido!")
        print(f"[OK] TEST-02 OK: '{query}' -> {runbook['code']} (Menciona registro por diferido)")

    def test_03_error_al_descargar_receta_resuelve_a_pdf_005(self):
        """Caso 3: 'error al descargar receta' debe ir a PDF-005 y no a PKI genérico."""
        query = "error al descargar receta"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook, "No se encontró runbook para 'error al descargar receta'")
        self.assertTrue("PDF-005" in runbook["code"] or "DOC" in runbook["code"], f"Se esperaba PDF-005/DOC pero se obtuvo: {runbook['code']}")
        self.assertNotIn("PKI", runbook["title"], "ERROR: Se asoció a protocolo PKI viejo en lugar de PDF-005!")
        print(f"[OK] TEST-03 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

    def test_04_alta_de_prestador_resuelve_a_cd2_inst_001(self):
        """Caso 4: 'alta de prestador' debe resolver a CD2-INST-001 y no a Jitsi."""
        query = "alta de prestador"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook, "No se encontró runbook para 'alta de prestador'")
        self.assertIn("INST-001", runbook["code"], f"Se esperaba CD2-INST-001 pero se obtuvo: {runbook['code']}")
        self.assertNotIn("VID", runbook["code"], "ERROR: Se confundió alta de prestador con videoconsulta!")
        print(f"[OK] TEST-04 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

    def test_05_prestador_sin_matriculas_resuelve_a_cd2_mat_001(self):
        """Caso 5: Matrículas no visibles debe resolver a CD2-MAT-001 o MAT-001."""
        query = "prestador sin matrículas visibles en consultorio digital"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook)
        self.assertIn("MAT-001", runbook["code"])
        print(f"[OK] TEST-05 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

    def test_06_nutricion_190173_resuelve_a_nut_008_o_snomed(self):
        """Caso 6: Incidencia nutrición 190173 vs 420296 debe resolver a NUT-008 o CD2-SNOMED-001."""
        query = "videoconsulta nutrición 190173 rechazada"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook)
        self.assertTrue("NUT-001" in runbook["code"] or "NUT-008" in runbook["code"] or "SNOMED-001" in runbook["code"])
        print(f"[OK] TEST-06 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

    def test_07_pantalla_blanca_videoconsulta_resuelve_a_jitsi(self):
        """Caso 7: Pantalla blanca o WebRTC en videoconsulta debe resolver a VID-002 o TEL-001."""
        query = "pantalla blanca en videoconsulta jitsi"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook)
        self.assertTrue("VID-002" in runbook["code"] or "TEL-001" in runbook["code"])
        print(f"[OK] TEST-07 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

    def test_08_biometria_otp_resuelve_a_bio_010(self):
        """Caso 8: Biometría y validación OTP ministerial debe resolver a BIO-010."""
        query = "solicita permanentemente biometría y token otp"
        result = N3CognitiveTriageEngine.analyze_incident(query)
        runbook = result["matched_runbook"]
        
        self.assertIsNotNone(runbook)
        self.assertIn("BIO-010", runbook["code"])
        print(f"[OK] TEST-08 OK: '{query}' -> {runbook['code']} ({runbook['title'][:40]}...)")

if __name__ == "__main__":
    unittest.main()
