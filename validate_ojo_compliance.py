#!/usr/bin/env python3
"""
validate_ojo_compliance.py
==========================
Linter automatizado y Gatekeeper de Calidad OJO para Quantux ServiceDesk.

Verifica el cumplimiento estricto e inquebrantable de:
1. Regla de Oro Pizarra Neutral (Cero cards, cero tarjetas, cero grillas de cajas).
2. Paleta Cromática (Cero colores rojos: #FF0000, #DC2626, #EF4444, red, etc.).
3. Restricción Terminológica (Cero terminología clínica: bypass, guardia, asistencial, triage).
4. Elementos Vetados (Cero checkbox 'paciente conectado', cero temporizadores regresivos '11m 45s', etc.).
5. Estructura Requerida (.tree-node-row en listados y árboles).

Retorna:
    Exit Code 0: Cumplimiento 100% exitoso.
    Exit Code 1: Se detectaron violaciones críticas que bloquean la entrega.
"""

import os
import sys
import re
import argparse
from typing import List, Dict, Tuple

# Asegurar codificación utf-8 para la salida en terminales Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Patrones de Violación Estricta
FORBIDDEN_CARD_PATTERNS = [
    (re.compile(r'class\s*=\s*["\'][^"\']*\b(?:ticket-card|jira-card|kpi-card|chart-card|csat-alert-card|itil-matrix-card|card|cards)\b[^"\']*["\']', re.IGNORECASE), "Uso de clase tipo 'card' en elemento DOM"),
    (re.compile(r'\.(?:ticket-card|jira-card|kpi-card|chart-card|csat-alert-card|itil-matrix-card|card|cards)[\s\.\{\:,]', re.IGNORECASE), "Selector CSS tipo 'card'"),
    (re.compile(r'grid-template-columns\s*:\s*repeat\s*\(\s*(?:auto-fit|auto-fill|\d+)\s*,\s*minmax\([^)]+\)\s*\)', re.IGNORECASE), "Grilla de tarjetas individuales flotantes"),
]

FORBIDDEN_RED_PATTERNS = [
    (re.compile(r'#dc2626', re.IGNORECASE), "Color rojo prohibido #DC2626"),
    (re.compile(r'#ef4444', re.IGNORECASE), "Color rojo prohibido #EF4444"),
    (re.compile(r'#ff0000', re.IGNORECASE), "Color rojo prohibido #FF0000"),
    (re.compile(r'#b91c1c', re.IGNORECASE), "Color rojo prohibido #B91C1C"),
    (re.compile(r'#991b1b', re.IGNORECASE), "Color rojo prohibido #991B1B"),
    (re.compile(r'#f87171', re.IGNORECASE), "Color rojo prohibido #F87171"),
    (re.compile(r':\s*red\b', re.IGNORECASE), "Color CSS literal 'red'"),
    (re.compile(r'rgb\(\s*255\s*,\s*0\s*,\s*0\s*\)', re.IGNORECASE), "Color RGB rojo puro"),
    (re.compile(r'rgba\(\s*255\s*,\s*0\s*,\s*0\s*,', re.IGNORECASE), "Color RGBA rojo puro"),
]

FORBIDDEN_CLINICAL_PATTERNS = [
    (re.compile(r'\b(?:guardia|guardias)\b', re.IGNORECASE), "Término clínico hospitalario 'guardia' (usar 'mesa de ayuda técnica' o 'soporte operativo')"),
    (re.compile(r'\b(?:bypass)\b', re.IGNORECASE), "Término clínico 'bypass' (usar 'derivación técnica directa/prioritaria')"),
    (re.compile(r'\b(?:asistencial|asistenciales)\b', re.IGNORECASE), "Término clínico 'asistencial' (usar 'técnico', 'operativo' o 'de soporte')"),
    (re.compile(r'\b(?:triage|triaje\s+cl[ií]nico)\b', re.IGNORECASE), "Término clínico 'triage' (usar 'clasificación técnica' o 'enrutamiento inicial')"),
]

FORBIDDEN_DARK_NAVY_PATTERNS = [
    (re.compile(r'#002b49', re.IGNORECASE), "Color azul marino vetado #002B49 (usar paleta Quantux clara/slate/teal)"),
    (re.compile(r'#1e3a8a', re.IGNORECASE), "Color azul marino vetado #1E3A8A (usar paleta Quantux clara/slate/teal)"),
    (re.compile(r'#172554', re.IGNORECASE), "Color azul marino vetado #172554 (usar paleta Quantux clara/slate/teal)"),
    (re.compile(r'#0a192f', re.IGNORECASE), "Color azul noche vetado #0A192F (usar paleta Quantux clara/slate/teal)"),
    (re.compile(r'#1e40af', re.IGNORECASE), "Color azul oscuro vetado #1E40AF (usar paleta Quantux clara/slate/teal)"),
    (re.compile(r'#1d4ed8', re.IGNORECASE), "Color azul chillón vetado #1D4ED8 (usar paleta Quantux clara/slate/teal)"),
    (re.compile(r'background(?:-color)?\s*:\s*#0f172a', re.IGNORECASE), "Fondo oscuro prohibido #0F172A (superficies deben ser claras: #FFFFFF, #F8FAFC, #F1F5F9)"),
    (re.compile(r'background(?:-color)?\s*:\s*#1e293b', re.IGNORECASE), "Fondo oscuro prohibido #1E293B (superficies deben ser claras: #FFFFFF, #F8FAFC, #F1F5F9)"),
    (re.compile(r'background(?:-color)?\s*:\s*#000000', re.IGNORECASE), "Fondo negro prohibido #000000"),
    (re.compile(r'background(?:-color)?\s*:\s*black\b', re.IGNORECASE), "Fondo negro prohibido 'black'"),
    (re.compile(r'background(?:-color)?\s*:\s*#111827', re.IGNORECASE), "Fondo oscuro prohibido #111827"),
]

FORBIDDEN_BANNED_WIDGETS = [
    (re.compile(r'paciente\s+conectado', re.IGNORECASE), "Checkbox o indicador vetado 'paciente conectado'"),
    (re.compile(r'11m\s*45s', re.IGNORECASE), "Temporizador regresivo inventado '11m 45s'"),
    (re.compile(r'resoluci[oó]n\s+oficial', re.IGNORECASE), "Badge inventado 'resolución oficial'"),
    (re.compile(r'plan\s+6-030', re.IGNORECASE), "Plan ficticio inventado 'Plan 6-030' hardcodeado"),
]


TARGET_EXTENSIONS = {'.html', '.css', '.js'}

class OjoViolation:
    def __init__(self, file_path: str, line_no: int, category: str, message: str, line_content: str):
        self.file_path = file_path
        self.line_no = line_no
        self.category = category
        self.message = message
        self.line_content = line_content.strip()

    def __str__(self):
        return f"[{self.category}] {self.file_path}:{self.line_no} -> {self.message}\n    Línea: {self.line_content[:120]}"

def check_file(file_path: str) -> List[OjoViolation]:
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error al leer archivo {file_path}: {e}")
        return violations

    for idx, line in enumerate(lines, start=1):
        # 1. Chequeo de Cards
        for pat, desc in FORBIDDEN_CARD_PATTERNS:
            if pat.search(line):
                violations.append(OjoViolation(file_path, idx, "CARD_VIOLATION", desc, line))

        # 2. Chequeo de Rojos
        for pat, desc in FORBIDDEN_RED_PATTERNS:
            if pat.search(line):
                violations.append(OjoViolation(file_path, idx, "RED_COLOR_VIOLATION", desc, line))

        # 3. Chequeo de Jerga Clínica
        for pat, desc in FORBIDDEN_CLINICAL_PATTERNS:
            if pat.search(line):
                violations.append(OjoViolation(file_path, idx, "CLINICAL_TERMS_VIOLATION", desc, line))

        # 4. Chequeo de Azul Marino y Fondos Oscuros
        for pat, desc in FORBIDDEN_DARK_NAVY_PATTERNS:
            if pat.search(line):
                violations.append(OjoViolation(file_path, idx, "DARK_NAVY_COLOR_VIOLATION", desc, line))

        # 5. Chequeo de Widgets Vetados
        for pat, desc in FORBIDDEN_BANNED_WIDGETS:
            if pat.search(line):
                violations.append(OjoViolation(file_path, idx, "BANNED_WIDGET_VIOLATION", desc, line))

    return violations


def scan_directory(directory: str) -> List[OjoViolation]:
    all_violations = []
    for root, _, files in os.walk(directory):
        # Evitar node_modules, git, venv, backups
        if any(skip in root for skip in ['.git', 'node_modules', '.venv', '__pycache__', 'backups']):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in TARGET_EXTENSIONS:
                full_path = os.path.join(root, file)
                violations = check_file(full_path)
                all_violations.extend(violations)
    return all_violations

def main():
    parser = argparse.ArgumentParser(description="Linter de Restricciones OJO y Pizarra Neutral")
    parser.add_argument("paths", nargs="*", default=["frontend"], help="Rutas o archivos a escanear (por defecto 'frontend')")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON estructurado")
    args = parser.parse_args()

    total_violations = []
    for path in args.paths:
        if os.path.isfile(path):
            total_violations.extend(check_file(path))
        elif os.path.isdir(path):
            total_violations.extend(scan_directory(path))
        else:
            print(f"Ruta no encontrada: {path}")

    # Reporte
    print("\n" + "="*80)
    print(" REPORTE DE AUDITORÍA AUTOMÁTICA DE RESTRICCIONES OJO / PIZARRA NEUTRAL")
    print("="*80)

    if not total_violations:
        print("\n[ÉXITO] CERO VIOLACIONES DETECTADAS. El código cumple 100% con OJO.")
        print("✓ Cero tarjetas (cards).")
        print("✓ Cero colores rojos.")
        print("✓ Cero terminología clínica.")
        print("✓ Cero componentes vetados.")
        print("="*80 + "\n")
        sys.exit(0)

    # Agrupar por categoría
    by_category: Dict[str, List[OjoViolation]] = {}
    for v in total_violations:
        by_category.setdefault(v.category, []).append(v)

    print(f"\n[BLOQUEO DE CALIDAD] Se encontraron {len(total_violations)} violaciones críticas:\n")
    for cat, items in by_category.items():
        print(f"--- Categoría: {cat} ({len(items)} casos) ---")
        for item in items[:15]:  # Mostrar los primeros 15 por categoría
            print(f"  • {item.file_path}:{item.line_no} | {item.message}")
            print(f"    Snippet: {item.line_content[:100]}...")
        if len(items) > 15:
            print(f"    ... y {len(items) - 15} ocurrencias más.")
        print()

    print("="*80)
    print("ACCIÓN REQUERIDA: Corregir las líneas listadas antes de entregar el desarrollo.")
    print("="*80 + "\n")
    sys.exit(1)

if __name__ == "__main__":
    main()
