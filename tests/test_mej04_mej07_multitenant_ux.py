"""
Test suite de validación técnica y de diseño UX para:
- MEJ-04: Remoción de barra explicativa superior en matriz multi-tenant.
- MEJ-05: Simetría matemática y normalización de cápsulas ACTIVO/INACTIVO sin '[OK]'.
- MEJ-06: Supresión de botones redundantes de categoría en toolbar de matriz.
- ISSUE-20: Buscador predictivo con autocompletado, opción 'Mostrar Todas' y supresión de doble lupa.
- MEJ-07: Rediseño Senior UX de sub-pestañas y botones de acción con semántica asistencial.
- ISSUE-19 & Scope Freeze: Aislamiento estricto de ítems fuera de alcance en el Product Backlog.
"""

import unittest
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(BASE_DIR, "frontend", "index.html")
APP_JS = os.path.join(BASE_DIR, "frontend", "js", "app.js")
SCRUMBAN_HTML = os.path.join(BASE_DIR, "docs", "00_Tablero_Scrumban_Quantux.html")
BACKLOG_CSV = os.path.join(BASE_DIR, "docs", "Backlog_HealthDesk_Quantux.csv")

class TestMultiTenantUXSenior(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8", errors="ignore") as f:
            cls.index_content = f.read()
        with open(APP_JS, "r", encoding="utf-8", errors="ignore") as f:
            cls.js_content = f.read()
        with open(SCRUMBAN_HTML, "r", encoding="utf-8", errors="ignore") as f:
            cls.board_content = f.read()
        with open(BACKLOG_CSV, "r", encoding="utf-8", errors="ignore") as f:
            cls.csv_content = f.read()

    def test_mej04_guide_bar_removed(self):
        """Verifica que la barra explicativa verde superior ha sido eliminada por completo."""
        self.assertNotIn("tenant-matrix-guide-body", self.index_content)
        self.assertNotIn("¿Cómo funciona la Matriz de Habilitación Multi-Tenant?", self.index_content)
        print("[OK] MEJ-04: Barra explicativa superior eliminada satisfactoriamente.")

    def test_mej05_capsule_symmetry_and_no_ok(self):
        """Verifica que no existe [OK] en las cápsulas y que ambas tienen dimensiones simétricas exactas (82px x 26px)."""
        self.assertNotIn("[OK] ACTIVO", self.js_content)
        self.assertIn("width: 82px; height: 26px;", self.js_content)
        self.assertIn("${isEnabled ? 'ACTIVO' : 'INACTIVO'}", self.js_content)
        print("[OK] MEJ-05: Cápsulas ACTIVO/INACTIVO normalizadas y simétricas sin [OK].")

    def test_mej06_category_buttons_removed(self):
        """Verifica que los botones estáticos Todas, Prepagas, Sanatorios y Hospitales fueron suprimidos del toolbar."""
        self.assertNotIn("btn-matrix-filter-PREPAGAS", self.index_content)
        self.assertNotIn("btn-matrix-filter-SANATORIOS", self.index_content)
        self.assertNotIn("btn-matrix-filter-HOSPITALES", self.index_content)
        print("[OK] MEJ-06: Botones redundantes de categoría eliminados del toolbar.")

    def test_issue20_predictive_search_and_single_lupa(self):
        """Verifica que existe una sola lupa, botón de limpieza ✕, desplegable predictivo y función Mostrar Todas."""
        # Verificar que el placeholder no contiene la lupa
        self.assertIn('placeholder="Buscar institución sanitaria o código..."', self.index_content)
        # Verificar botón clear
        self.assertIn('id="btn-tenant-matrix-search-clear"', self.index_content)
        # Verificar dropdown predictivo
        self.assertIn('id="tenant-matrix-predictive-dropdown"', self.index_content)
        # Verificar botón Mostrar Todas
        self.assertIn('Mostrar Todas', self.index_content)
        # Verificar funciones JS correspondientes
        self.assertIn('function renderTenantMatrixPredictiveDropdown', self.js_content)
        self.assertIn('function clearTenantMatrixSearch', self.js_content)
        self.assertIn('function selectTenantMatrixPredictive', self.js_content)
        print("[OK] ISSUE-20: Buscador predictivo, botón de limpieza y una sola lupa implementados.")

    def test_mej07_subtabs_senior_ux_redesign(self):
        """Verifica la semántica asistencial y el rediseño Senior UX de las sub-pestañas y botones de acción."""
        self.assertIn("Instituciones Sanitarias", self.index_content)
        self.assertIn("Módulos Clínicos", self.index_content)
        self.assertIn("Habilitación Multi-Tenant", self.index_content)
        self.assertIn("Niveles de Soporte ITIL", self.index_content)
        self.assertIn("+ Nuevo Módulo Clínico", self.index_content)
        self.assertIn("+ Nueva Institución Sanitaria", self.index_content)
        print("[OK] MEJ-07: Sub-pestañas y botones rediseñados con semántica asistencial UX Senior.")

    def test_scope_freeze_and_issue19_in_backlog(self):
        """Verifica que el banner de Scope Freeze está en el tablero y que ISSUE-19 está en el Product Backlog."""
        self.assertIn("SCOPE FREEZE", self.board_content)
        self.assertIn("HARDENING", self.board_content)
        self.assertIn("ISSUE-19", self.board_content)
        # En el CSV debe estar en status 'backlog'
        match = re.search(r'"ISSUE-19".*?"backlog"', self.csv_content)
        self.assertIsNotNone(match, "ISSUE-19 debe estar en estado 'backlog' en el CSV")
    def test_mej08_scrumban_toolbar_buttons_removed(self):
        """Verifica que MEJ-08 eliminó la botonera administrativa del toolbar y que la tarjeta está en curso (progress)."""
        # Verificar que no existen los botones en el toolbar
        self.assertNotIn('<button class="btn btn-secondary" onclick="exportToCSV()">', self.board_content)
        self.assertNotIn('<button class="btn btn-secondary" onclick="window.print()">', self.board_content)
        self.assertNotIn('<button class="btn btn-secondary" onclick="resetDefaultTasks()">', self.board_content)
        self.assertNotIn('<button class="btn" onclick="saveState()">', self.board_content)
        # Verificar que MEJ-08 existe en el CSV con estado 'progress' o 'done'
        match = re.search(r'"MEJ-08".*?"(progress|done)"', self.csv_content)
        self.assertIsNotNone(match, "MEJ-08 debe estar registrada en estado 'progress' o 'done'")
        print("[OK] MEJ-08: Botonera administrativa eliminada y tarjeta verificada.")

if __name__ == '__main__':
    unittest.main()
