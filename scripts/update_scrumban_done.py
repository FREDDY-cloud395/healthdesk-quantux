#!/usr/bin/env python3
"""
scripts/update_scrumban_done.py
Actualiza el Tablero Scrumban para promover MEJ-01 y MEJ-02 a 'done' y reflejar las métricas actualizadas.
"""
import os
import re

html_path = os.path.join(os.path.dirname(__file__), "..", "docs", "00_Tablero_Scrumban_Quantux.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Actualizar métricas
html = html.replace("173 <small>/ 274 SP (63.1%)</small>", "181 <small>/ 274 SP (66.1%)</small>")
html = html.replace("36 SP <small>(5 SP Done, 31 SP en curso)</small>", "36 SP <small>(13 SP Done, 23 SP en curso)</small>")

# Actualizar status de MEJ-02
pattern_mej02 = r'("id":\s*"MEJ-02".*?"status":\s*)"qa"'
html, count2 = re.subn(pattern_mej02, r'\1"done"', html)
print(f"MEJ-02 matches updated: {count2}")

# Actualizar status de MEJ-01
pattern_mej01 = r'("id":\s*"MEJ-01".*?"status":\s*)"qa"'
html, count1 = re.subn(pattern_mej01, r'\1"done"', html)
print(f"MEJ-01 matches updated: {count1}")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("HTML actualizado correctamente.")
