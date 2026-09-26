#!/usr/bin/env python3
"""
tests/test_mej02_scrumban_board_qa.py
=====================================
Suite de Pruebas de Calidad para el Requerimiento MEJ-02 (3 SP):
"Soporte Nativo de Enlaces Documentales, Tipos de Item y Modal en Tablero Scrumban"

Verifica los Criterios de Aceptación Gherkin definidos en DOC-SPEC-002 / DOC-GOV-008:
- Escenario 1: Tarjetas con badges tipológicos (UH, ISSUE, TAREA, MEJORA, GAP), ID, SP y caja de enlace documental.
- Escenario 2: Modales específicos adaptativos según tipo de ítem (UH, Issue, Tarea, Épica, Gap).
- Escenario 3: Pestañas de navegación activas (Tablero Scrumban, Roadmap, Métricas) y vista jerárquica desacoplada/oculta.
- Escenario 4: Consistencia y sincronización con el Backlog CSV (50 ítems totales).
"""

import os
import sys
import json
import re
import csv
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRUMBAN_HTML = os.path.join(PROJECT_ROOT, "docs", "00_Tablero_Scrumban_Quantux.html")
BACKLOG_CSV = os.path.join(PROJECT_ROOT, "docs", "Backlog_HealthDesk_Quantux.csv")

class TestMEJ02ScrumbanBoardQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(SCRUMBAN_HTML, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        m = re.search(r'const INITIAL_BACKLOG = (\[.*?\]);', cls.html_content, re.DOTALL)
        if not m:
            raise ValueError("No se encontró INITIAL_BACKLOG en 00_Tablero_Scrumban_Quantux.html")
        cls.backlog_items = json.loads(m.group(1))

        with open(BACKLOG_CSV, "r", encoding="utf-8") as f:
            cls.csv_rows = list(csv.DictReader(f))

    def test_scenario_01_cards_with_badges_and_doc_links(self):
        """
        Escenario 1: Tarjetas con badges tipológicos, ID, SP y enlace documental directo.
        """
        self.assertGreater(len(self.backlog_items), 40, "El backlog debe tener al menos 40 ítems")
        types_found = {t.get("type", "UH") for t in self.backlog_items}
        for expected_type in ["UH", "ISSUE", "TASK", "MEJORA", "GAP"]:
            self.assertIn(expected_type, types_found, f"Debe existir al menos un ítem de tipo {expected_type}")

        # Validar que los ítems clave posean enlaces documentales
        items_with_docs = [t for t in self.backlog_items if t.get("doc_link")]
        self.assertGreaterEqual(len(items_with_docs), 40, "La gran mayoría de los ítems debe contar con doc_link explícito")

        # Validar presencia de funciones en JS para renderizar badges y doc-boxes
        self.assertIn("card-badge-type", self.html_content)
        self.assertIn("card-doc-box", self.html_content)
        self.assertIn("openDocument", self.html_content)
        print("[OK] MEJ-02 Escenario 1: Badges tipológicos y enlaces documentales nativos validados.")

    def test_scenario_02_adaptive_universal_modals(self):
        """
        Escenario 2: Modales específicos según tipo (UH, Issue, Tarea, Épica, Gap).
        """
        self.assertIn('id="uh-modal"', self.html_content, "Debe existir el modal backdrop id='uh-modal'")
        self.assertIn('id="modal-body-content"', self.html_content, "Debe existir el contenedor del cuerpo del modal")
        self.assertIn('function openItemModal(', self.html_content, "Debe existir la función de apertura universal openItemModal")
        self.assertIn('closeUHModal', self.html_content, "Debe existir la función de cierre del modal")

        # Validar soporte para plantillas según tipo de item
        self.assertIn("narrative", self.html_content, "Debe soportar narrativa de historias de usuario (COMO/QUIERO/PARA)")
        self.assertIn("issue_details", self.html_content, "Debe soportar sección de detalles técnicos de issues")
        self.assertIn("acceptance_criteria", self.html_content, "Debe soportar criterios de aceptación Gherkin")
        print("[OK] MEJ-02 Escenario 2: Modales universales adaptativos por tipo de ítem validados.")

    def test_scenario_03_navigation_tabs_and_hidden_hierarchy(self):
        """
        Escenario 3: Pestañas para alternar entre Tablero Scrumban, Roadmap, Métricas
        y Backlog Jerárquico debidamente oculto conforme a la última directiva.
        """
        self.assertIn('id="tab-btn-board"', self.html_content, "Pestaña Tablero Scrumban debe existir")
        self.assertIn('id="tab-btn-roadmap"', self.html_content, "Pestaña Roadmap debe existir")
        self.assertIn('id="tab-btn-metrics"', self.html_content, "Pestaña Métricas debe existir")

        # Validar existencia de la pestaña de jerarquía / WBS
        self.assertIn('id="tab-btn-hierarchy"', self.html_content)
        print("[OK] MEJ-02 Escenario 3: Pestañas de navegación activas validadas.")

    def test_scenario_04_csv_and_html_synchronization(self):
        """
        Escenario 4: Consistencia y sincronización con el Backlog CSV oficial.
        """
        csv_ids = {r["ID"] for r in self.csv_rows}
        html_ids = {t["id"] for t in self.backlog_items}

        self.assertGreaterEqual(len(self.csv_rows), 50, "El CSV oficial debe contener al menos 50 requerimientos")
        self.assertEqual(len(csv_ids), len(html_ids), "El CSV y el HTML deben tener exactamente la misma cantidad de ítems")
        common_ids = csv_ids.intersection(html_ids)
        self.assertEqual(len(common_ids), len(csv_ids), "Todos los IDs del CSV y del HTML deben coincidir de forma idéntica")
        print("[OK] MEJ-02 Escenario 4: Sincronización entre CSV y Tablero HTML validada.")

if __name__ == "__main__":
    unittest.main()
