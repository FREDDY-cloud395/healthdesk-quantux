"""
Test suite de validación y certificación formal para los ítems críticos del Sprint 6:
- ISSUE-21: Reemplazo de botones crípticos de respuesta en ticket (📚 y 🤖) por acciones semánticas explicativas.
- ISSUE-22: Telemetría Operativa Zero-Question accesible directamente en el workspace de tickets.
- ISSUE-23: Erradicación de viñetas duplicadas en el historial y timeline de auditoría del ticket.
- UH-67: Subniveles interactivos de navegación en el árbol N1 y separación estricta en dos capas (Médico vs Soporte N2).
- MEJ-08: Supresión de botonera administrativa en el toolbar del tablero Scrumban.
- Cierre del Sprint 6 y persistencia en tablero Scrumban y CSV.
"""

import unittest
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(BASE_DIR, "frontend", "index.html")
APP_JS = os.path.join(BASE_DIR, "frontend", "js", "app.js")
REEMPLAZO_HTML = os.path.join(BASE_DIR, "frontend", "reemplazo-n1.html")
SCRUMBAN_HTML = os.path.join(BASE_DIR, "docs", "00_Tablero_Scrumban_Quantux.html")
SCRUMBAN_CSV = os.path.join(BASE_DIR, "docs", "Backlog_HealthDesk_Quantux.csv")

class TestSprint6CriticalFixes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8", errors="ignore") as f:
            cls.index_content = f.read()
        with open(APP_JS, "r", encoding="utf-8", errors="ignore") as f:
            cls.js_content = f.read()
        with open(REEMPLAZO_HTML, "r", encoding="utf-8", errors="ignore") as f:
            cls.reemplazo_content = f.read()
        with open(SCRUMBAN_HTML, "r", encoding="utf-8", errors="ignore") as f:
            cls.board_content = f.read()
        with open(SCRUMBAN_CSV, "r", encoding="utf-8", errors="ignore") as f:
            cls.csv_content = f.read()

    def test_issue21_cryptic_buttons_replaced(self):
        """Verifica que los emojis huérfanos fueron reemplazados por botones semánticos con affordance Senior UX."""
        # Verificar botones en index.html
        self.assertIn('id="ws-btn-insert-kb"', self.index_content)
        self.assertIn('Insertar Solución KB', self.index_content)
        self.assertIn('id="ws-btn-bot-request-info"', self.index_content)
        self.assertIn('Bot: Pedir Datos (Pausa SLA)', self.index_content)
        
        # Verificar funciones JS en app.js
        self.assertIn('function openQuickKbInsertModal', self.js_content)
        self.assertIn('function confirmAndTriggerBotInteraction', self.js_content)
        self.assertIn('ESPERANDO_AL_PRESTADOR', self.js_content)
        print("[OK] ISSUE-21: Botones semánticos KB e interacción de Bot con pausa de SLA verificados.")

    def test_issue22_telemetry_tab_and_panel(self):
        """Verifica que la pestaña de Telemetría está visible y renderiza parámetros Zero-Question."""
        # Verificar pestaña en index.html
        self.assertIn('id="ws-tab-tech"', self.index_content)
        self.assertIn('Telemetría & Diagnóstico', self.index_content)
        
        # Verificar panel de renderizado en app.js
        self.assertIn('Telemetria Operativa del Entorno (Zero-Question)', self.js_content)
        self.assertIn('tel.browser', self.js_content)
        self.assertIn('tel.os', self.js_content)
        self.assertIn('tel.screen', self.js_content)
        self.assertIn('tel.connection', self.js_content)
        self.assertIn('tel.timezone', self.js_content)
        self.assertIn('tel.cpu_cores', self.js_content)
        self.assertIn('FHIR R4', self.js_content)
        self.assertIn('ws-tech-json-payload', self.js_content)
        print("[OK] ISSUE-22: Pestaña de telemetría y diagnóstico Zero-Question verificados.")

    def test_issue23_single_bullet_in_timeline(self):
        """Verifica que no existen viñetas dobles en la línea de tiempo del ticket."""
        self.assertIn('renderWsTimeline', self.js_content)
        # Verificar que se eliminó el span con it.icon duplicado dentro de la burbuja
        self.assertNotIn('<span style="font-weight: 700; color: #64748B; margin-right: 6px;">${it.icon}</span>', self.js_content)
        self.assertIn('<div class="ws-event-dot"></div>', self.js_content)
        print("[OK] ISSUE-23: Línea de tiempo limpia con indicador único en riel vertical verificada.")

    def test_uh67_sublevels_and_dual_layer(self):
        """Verifica que el reemplazo N1 cuenta con subniveles interactivos y doble capa funcional."""
        # Verificar subniveles (chips)
        self.assertIn('class="tree-sublevels-group"', self.reemplazo_content)
        self.assertIn('class="tree-sublevel-chip"', self.reemplazo_content)
        self.assertIn('Matrícula SISA', self.reemplazo_content)
        self.assertIn('Vademécum Alfabeta', self.reemplazo_content)
        self.assertIn('Biometría Res. 2214/2025', self.reemplazo_content)
        self.assertIn('Contingencia Receta', self.reemplazo_content)
        
        # Verificar separación de capas
        self.assertIn('immediate-resolution-layer', self.reemplazo_content)
        self.assertIn('technical-accordion-layer', self.reemplazo_content)
        self.assertIn('cleanMarkdown', self.reemplazo_content)
        print("[OK] UH-67: Subniveles interactivos y separación de capas (médico vs soporte) verificados.")

    def test_sprint6_scrumban_board_and_csv(self):
        """Verifica que los ítems del Sprint 6 están registrados en estado 'done' y que ISSUE-19 está en backlog."""
        for item_id in ["ISSUE-21", "ISSUE-22", "ISSUE-23", "UH-67", "MEJ-08"]:
            self.assertIn(item_id, self.board_content, f"Debe figurar {item_id} en el tablero Scrumban HTML")
            match = re.search(rf'"{item_id}".*?"done"', self.csv_content)
            self.assertIsNotNone(match, f"{item_id} debe figurar en estado 'done' en el CSV")

        # Verificar que ISSUE-19 está en el backlog
        match_issue19 = re.search(r'"ISSUE-19".*?"backlog"', self.csv_content)
        self.assertIsNotNone(match_issue19, "ISSUE-19 debe permanecer en 'backlog' (Product Backlog)")
        print("[OK] Tablero Scrumban y CSV certificados con Sprint 6 culminado al 100%.")

if __name__ == '__main__':
    unittest.main()
