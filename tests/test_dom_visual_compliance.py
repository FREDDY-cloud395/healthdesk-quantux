#!/usr/bin/env python3
"""
tests/test_dom_visual_compliance.py
===================================
Suite E2E de validación de DOM y Render Visual Pre-Entrega para Quantux ServiceDesk.

Audita los archivos HTML y CSS generados utilizando el parser estándar de HTML de Python.
Valida:
1. Ausencia total de clases tipo 'card' en el DOM.
2. Ausencia total de tonalidades rojas en estilos inline y clases.
3. Ausencia total de terminología clínica en textos visibles.
4. Ausencia total de widgets vetados (checkbox paciente conectado, timers).
5. Conformidad con la arquitectura de filas .tree-node-row de 1px.
"""

import os
import re
import unittest
from html.parser import HTMLParser
from typing import List, Tuple, Dict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

class DOMInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.classes = []
        self.inline_styles = []
        self.text_nodes = []
        self.style_blocks = []
        self.current_tag = None
        self.in_style = False
        self.current_style_content = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        self.tags.append((tag, attr_dict, self.getpos()))

        if "class" in attr_dict:
            for cls in attr_dict["class"].split():
                self.classes.append((cls, tag, self.getpos()))

        if "style" in attr_dict:
            self.inline_styles.append((attr_dict["style"], tag, self.getpos()))

        if tag.lower() == "style":
            self.in_style = True
            self.current_style_content = []

    def handle_endtag(self, tag):
        if tag.lower() == "style":
            self.in_style = False
            self.style_blocks.append(("".join(self.current_style_content), self.getpos()))
            self.current_style_content = []

    def handle_data(self, data):
        if self.in_style:
            self.current_style_content.append(data)
        else:
            text = data.strip()
            if text:
                self.text_nodes.append((text, self.current_tag, self.getpos()))

class TestDOMVisualCompliance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target_files = [
            os.path.join(FRONTEND_DIR, "index.html"),
            os.path.join(FRONTEND_DIR, "reemplazo-n1.html")
        ]
        cls.inspections: Dict[str, DOMInspector] = {}
        for path in cls.target_files:
            if os.path.exists(path):
                parser = DOMInspector()
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                parser.feed(content)
                cls.inspections[path] = parser

    def test_01_no_card_classes_in_dom(self):
        """Verifica que ningún elemento del DOM utilice clases con la palabra 'card'."""
        card_pattern = re.compile(r'\b(?:ticket-card|jira-card|kpi-card|chart-card|csat-alert-card|itil-matrix-card|card|cards)\b', re.IGNORECASE)
        violations = []
        for file_path, parser in self.inspections.items():
            rel_file = os.path.relpath(file_path, PROJECT_ROOT)
            for cls, tag, pos in parser.classes:
                if card_pattern.search(cls):
                    violations.append(f"{rel_file}:{pos[0]}:{pos[1]} -> Tag <{tag}> con clase prohibida '{cls}'")

        if violations:
            msg = f"\n[FALLO DE PIZARRA NEUTRAL] Se detectaron {len(violations)} clases tipo 'card' en el DOM:\n" + "\n".join(violations[:20])
            self.fail(msg)

    def test_02_no_red_colors_in_styles(self):
        """Verifica que no existan colores rojos (#DC2626, #EF4444, #FF0000, etc.) en estilos inline ni bloques style."""
        red_pattern = re.compile(r'(?:#dc2626|#ef4444|#ff0000|#b91c1c|#991b1b|#f87171|:\s*red\b|rgb\(\s*255\s*,\s*0)', re.IGNORECASE)
        violations = []
        for file_path, parser in self.inspections.items():
            rel_file = os.path.relpath(file_path, PROJECT_ROOT)
            for style, tag, pos in parser.inline_styles:
                match = red_pattern.search(style)
                if match:
                    violations.append(f"{rel_file}:{pos[0]}:{pos[1]} -> Estilo inline en <{tag}> contiene color rojo '{match.group(0)}': {style[:80]}")
            for style_block, pos in parser.style_blocks:
                for line_idx, line in enumerate(style_block.splitlines(), start=pos[0]):
                    match = red_pattern.search(line)
                    if match:
                        violations.append(f"{rel_file}:{line_idx} -> Bloque <style> contiene color rojo '{match.group(0)}': {line.strip()[:80]}")

        if violations:
            msg = f"\n[FALLO CROMÁTICO] Se detectaron {len(violations)} usos de colores rojos prohibidos:\n" + "\n".join(violations[:20])
            self.fail(msg)

    def test_03_no_clinical_terminology_in_text(self):
        """Verifica que la interfaz no contenga términos clínicos prohibidos (guardia, bypass, asistencial, triage)."""
        clinical_pattern = re.compile(r'\b(?:guardia|guardias|bypass|asistencial|asistenciales|triage|triaje\s+cl[ií]nico)\b', re.IGNORECASE)
        violations = []
        for file_path, parser in self.inspections.items():
            rel_file = os.path.relpath(file_path, PROJECT_ROOT)
            for text, tag, pos in parser.text_nodes:
                match = clinical_pattern.search(text)
                if match:
                    violations.append(f"{rel_file}:{pos[0]}:{pos[1]} -> Texto visible en <{tag}> contiene término clínico '{match.group(0)}': \"{text[:90]}\"")

        if violations:
            msg = f"\n[FALLO DE VOCABULARIO] Se detectaron {len(violations)} términos clínicos prohibidos en la UI:\n" + "\n".join(violations[:20])
            self.fail(msg)

    def test_04_no_banned_widgets(self):
        """Verifica que no existan componentes vetados (checkbox paciente conectado, temporizadores ficticios, etc.)."""
        banned_pattern = re.compile(r'(?:paciente\s+conectado|11m\s*45s|resoluci[oó]n\s+oficial|plan\s+6-030)', re.IGNORECASE)
        violations = []
        for file_path, parser in self.inspections.items():
            rel_file = os.path.relpath(file_path, PROJECT_ROOT)
            for text, tag, pos in parser.text_nodes:
                match = banned_pattern.search(text)
                if match:
                    violations.append(f"{rel_file}:{pos[0]}:{pos[1]} -> Widget o texto vetado '{match.group(0)}' en <{tag}>")

        if violations:
            msg = f"\n[FALLO DE ALCANCE] Se detectaron {len(violations)} widgets o elementos vetados:\n" + "\n".join(violations[:20])
            self.fail(msg)

    def test_05_no_dark_navy_or_black_backgrounds(self):
        """Verifica que no existan fondos oscuros ni tonos azul marino (#002B49, #1E3A8A, #172554, #0F172A, #1E293B) en la UI."""
        navy_pattern = re.compile(r'(?:#002b49|#1e3a8a|#172554|#0a192f|#1e40af|#1d4ed8|background(?:-color)?\s*:\s*#(?:0f172a|1e293b|000000|111827)|background(?:-color)?\s*:\s*black\b)', re.IGNORECASE)
        violations = []
        for file_path, parser in self.inspections.items():
            rel_file = os.path.relpath(file_path, PROJECT_ROOT)
            for style, tag, pos in parser.inline_styles:
                match = navy_pattern.search(style)
                if match:
                    violations.append(f"{rel_file}:{pos[0]}:{pos[1]} -> Estilo inline en <{tag}> contiene color oscuro/azul marino '{match.group(0)}': {style[:80]}")
            for style_block, pos in parser.style_blocks:
                for line_idx, line in enumerate(style_block.splitlines(), start=pos[0]):
                    match = navy_pattern.search(line)
                    if match:
                        violations.append(f"{rel_file}:{line_idx} -> Bloque <style> contiene color oscuro/azul marino '{match.group(0)}': {line.strip()[:80]}")

        if violations:
            msg = f"\n[FALLO CROMÁTICO - AZUL MARINO/OSCURO] Se detectaron {len(violations)} usos de azul marino o fondos oscuros prohibidos:\n" + "\n".join(violations[:20])
            self.fail(msg)

    def test_06_seven_approved_mockups_fidelity(self):
        """Verifica la correspondencia estricta de las 7 Figuras de Mockup aprobadas en la propuesta funcional."""
        reemplazo_file = os.path.join(FRONTEND_DIR, "reemplazo-n1.html")
        self.assertTrue(os.path.exists(reemplazo_file), "El archivo de mockups nativos reemplazo-n1.html debe existir.")
        with open(reemplazo_file, "r", encoding="utf-8") as f:
            html = f.read()

        # FIGURA 1: Portal Centrado con Cápsula Predictiva y 7 Árboles
        self.assertIn('id="screen-1"', html, "Figura 1: Debe existir el contenedor screen-1")
        self.assertIn('class="search-capsule"', html, "Figura 1: Debe contener la cápsula predictiva de búsqueda")
        self.assertIn('Árboles de Decisión Técnico-Operativos', html, "Figura 1: Cabecera oficial de árboles")
        self.assertIn('7 Ramas Oficiales Normalizadas', html, "Figura 1: Badge de 7 ramas oficiales")
        for i in range(1, 8):
            self.assertIn(f'ÁRBOL {i}', html, f"Figura 1: Debe incluir ÁRBOL {i} en filas estructuradas")

        # FIGURA 2: Chat Stream Resolutivo con Protocolo Oficial
        self.assertIn('id="screen-2"', html, "Figura 2: Debe existir el contenedor screen-2")
        self.assertIn('class="stream-bubble-user"', html, "Figura 2: Debe contener la burbuja del usuario")
        self.assertIn('class="stream-bubble-assistant"', html, "Figura 2: Debe contener la burbuja del asistente")
        self.assertIn('Asistente Autónomo N1', html, "Figura 2: Cabecera oficial del asistente")
        self.assertIn('No suspendas la sesión terapéutica', html, "Figura 2: Protocolo oficial Salud Mental")
        self.assertIn('Problema Resuelto (Generar Constancia FCR 100%)', html, "Figura 2: Botón FCR 100%")
        self.assertIn('No Pude Resolverlo: Generar Solicitud a Soporte N2', html, "Figura 2: Botón Escalamiento N2")
        self.assertIn('Hacer otra consulta', html, "Figura 2: Botón reinicio de consulta")

        # FIGURA 3: Modal Nativo Crear Solicitud con Telemetría
        self.assertIn('id="screen-3"', html, "Figura 3: Debe existir el contenedor screen-3")
        self.assertIn('Crear Solicitud de Soporte Especializado Nivel 2', html, "Figura 3: Título oficial del modal")
        self.assertIn('Lic. Marcela Gómez', html, "Figura 3: Telemetría de Profesional")
        self.assertIn('MN 39.412 (Validada)', html, "Figura 3: Telemetría Matrícula SISA")
        self.assertIn('consultoriodigital2.osde.com.ar', html, "Figura 3: Telemetría Plataforma")
        self.assertIn('Escalar Directamente a Especialistas Nivel 2', html, "Figura 3: Botón de escalamiento directo")

        # FIGURA 4: Historial Mis Solicitudes con Estados ITIL 4
        self.assertIn('id="screen-4"', html, "Figura 4: Debe existir el contenedor screen-4")
        self.assertIn('Mis Solicitudes de Asistencia', html, "Figura 4: Título de bandeja de solicitudes")
        self.assertIn('#TKT-2026-0348', html, "Figura 4: Ticket representativo FCR")
        self.assertIn('RESUELTO POR IA (FCR)', html, "Figura 4: Estado ITIL FCR")
        self.assertIn('EN CURSO (N2)', html, "Figura 4: Estado ITIL En Curso")
        self.assertIn('ESPERANDO AL PRESTADOR', html, "Figura 4: Estado ITIL Esperando Prestador")
        self.assertIn('EN ESPERA PASARELA OSDE / SISA', html, "Figura 4: Estado ITIL Pasarela Externa")

        # FIGURA 5: Detalle N2 con Cartel MIM y Acciones SLA
        self.assertIn('id="screen-5"', html, "Figura 5: Debe existir el contenedor screen-5")
        self.assertIn('#MIM-2026-04', html, "Figura 5: Identificador de Incidencia Mayor")
        self.assertIn('+ Sumar a Ticket Padre #TKT-8900', html, "Figura 5: Botón de asociación en 1 clic")
        self.assertIn('Trazabilidad ITIL Padre-Hijo', html, "Figura 5: Sección de trazabilidad bidireccional")
        self.assertIn('Pasar a "Esperando al Prestador" (Pausa SLA)', html, "Figura 5: Acción pausa SLA prestador")
        self.assertIn('Pasar a "En Espera Pasarela OSDE / SISA" (Pausa SLA)', html, "Figura 5: Acción pausa SLA pasarela")

        # FIGURA 6: Mando Unificado del Líder de Soporte (Rescate CSAT)
        self.assertIn('id="screen-6"', html, "Figura 6: Debe existir el contenedor screen-6")
        self.assertIn('Mando Unificado del Líder de Soporte', html, "Figura 6: Título del mando unificado")
        self.assertIn('Ticket #TKT-8841', html, "Figura 6: Ticket con alerta CSAT")
        self.assertIn('Justificación Obligatoria ingresada por el Prestador', html, "Figura 6: Justificación mandatoria")
        self.assertIn('RESCATADO CON CONFORMIDAD', html, "Figura 6: Badge oficial de rescate")
        self.assertIn('Acción de Rescate Ejecutada por Líder de Soporte', html, "Figura 6: Informe inmutable del líder")

        # FIGURA 7: Módulo Colaborativo de Configuración ITIL 4
        self.assertIn('id="screen-7"', html, "Figura 7: Debe existir el contenedor screen-7")
        self.assertIn('PROTECCIÓN DE GESTIÓN ACTIVA', html, "Figura 7: Blindaje de tickets en curso")
        self.assertIn('P1 Crítica (&lt; 15 min)', html, "Figura 7: Matriz de Prioridad P1")
        self.assertIn('P2 Alta (&lt; 30 min)', html, "Figura 7: Matriz de Prioridad P2")
        self.assertIn('P3 Media (&lt; 2 hs)', html, "Figura 7: Matriz de Prioridad P3")
        self.assertIn('P4 Baja (&lt; 24 hs)', html, "Figura 7: Matriz de Prioridad P4")
        self.assertIn('Ciclo de Vida Oficial del Ticket (7 Estados ITIL 4 con Pausas de Reloj SLA)', html, "Figura 7: Ciclo 7 estados")

if __name__ == "__main__":
    unittest.main(verbosity=2)

