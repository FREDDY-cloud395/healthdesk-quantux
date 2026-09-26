import re
from pathlib import Path

html = Path("frontend/index.html").read_text(encoding="utf-8")
js = Path("frontend/js/app.js").read_text(encoding="utf-8")

print("--- 1. BUSCANDO DUPLICADOS DE requester-chat-input ---")
for no, line in enumerate(html.splitlines(), 1):
    if 'id="requester-chat-input"' in line or "id='requester-chat-input'" in line:
        print(f"Línea {no}: {line.strip()[:100]}")

print("\n--- 2. BUSCANDO LLAMADAS ON* SOSPECHOSAS ---")
matches = re.findall(r'(on\w+=["\'][^"\']*["\'])', html)
for m in matches:
    if 'if' in m or 'Typeahead' in m:
        print(f"Evento encontrado: {m}")

print("\n--- 3. DETALLE DE FUNCIONES DUPLICADAS EN APP.JS ---")
declared = re.findall(r"function\s+([a-zA-Z0-9_]+)\s*\(", js)
from collections import Counter
counts = Counter(declared)
for fn, c in counts.items():
    if c > 1:
        print(f"Función '{fn}' declarada {c} veces en app.js")

print("\n--- 4. BUSCANDO MODAL-LINK-CHILDREN Y OTROS MODALES ROJOS ---")
for no, line in enumerate(html.splitlines(), 1):
    if 'modal-link-children' in line or 'DC2626' in line:
        print(f"Línea {no}: {line.strip()[:100]}")
