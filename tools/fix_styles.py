import re

with open("frontend/css/styles.css", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Variables
content = content.replace("--p1-red: #EF4444;", "--p1-red: #0F172A;")

# 2. Reemplazar selectores y clases tipo card
content = re.sub(r'\.kpi-card\b', '.kpi-row-item', content)
content = re.sub(r'\.chart-card\b', '.chart-panel', content)
content = re.sub(r'\.ticket-card-clean\b', '.tree-node-row', content)

# 3. Reemplazar grids de repeat por flex continuo
content = re.sub(r'grid-template-columns\s*:\s*repeat\s*\(\s*(?:auto-fit|auto-fill|\d+)\s*,\s*minmax\([^)]+\)\s*\)\s*(!important)?\s*;', 
                 'grid-template-columns: 1fr;', content)

# 4. Reemplazar colores rojos
content = content.replace("#EF4444", "#334155")
content = content.replace("#ef4444", "#334155")
content = content.replace("#DC2626", "#0F172A")
content = content.replace("#dc2626", "#0F172A")
content = content.replace("#F87171", "#64748B")
content = content.replace("#f87171", "#64748B")
content = content.replace("#B91C1C", "#1E293B")
content = content.replace("#b91c1c", "#1E293B")
content = content.replace("#991B1B", "#0F172A")
content = content.replace("#991b1b", "#0F172A")
content = content.replace("#FEF2F2", "#F8FAFC")
content = content.replace("#FEE2E2", "#F1F5F9")
content = content.replace("#FECACA", "#CBD5E1")
content = content.replace("#FCA5A5", "#CBD5E1")

# 5. Reemplazar azul marino y colores oscuros en fondos
content = content.replace("#1D4ED8", "#00A896")
content = content.replace("#1d4ed8", "#00A896")
content = content.replace("#1E40AF", "#334155")
content = content.replace("#1e40af", "#334155")
content = content.replace("#002B49", "#00A896")
content = content.replace("#002b49", "#00A896")
content = content.replace("#1E3A8A", "#00A896")
content = content.replace("#1e3a8a", "#00A896")
content = content.replace("#172554", "#0F172A")
content = content.replace("#172554", "#0F172A")

# Backgrounds oscuros específicos
content = re.sub(r'background(?:-color)?\s*:\s*#0F172A\s*(!important)?\s*;', 'background: #F8FAFC;', content, flags=re.IGNORECASE)
content = re.sub(r'background(?:-color)?\s*:\s*#1E293B\s*(!important)?\s*;', 'background: #FFFFFF;', content, flags=re.IGNORECASE)
content = re.sub(r'background(?:-color)?\s*:\s*#000000\s*(!important)?\s*;', 'background: #FFFFFF;', content, flags=re.IGNORECASE)

# 6. Clínicos
content = content.replace("SUITE ASISTENCIAL EXCLUSIVA PARA MÉDICOS", "SUITE TÉCNICO-OPERATIVA EXCLUSIVA")

with open("frontend/css/styles.css", "w", encoding="utf-8") as f:
    f.write(content)

print("styles.css actualizado con éxito.")
