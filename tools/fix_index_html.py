import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Cards y Grillas en index.html
content = re.sub(r'\bjira-kpi-card\b', 'tree-node-row', content)
content = re.sub(r'\bticket-card-clean\b', 'tree-node-row', content)
content = re.sub(r'\bchart-card-modern\b', 'chart-panel', content)
content = re.sub(r'\bchart-card\b', 'chart-panel', content)
content = re.sub(r'\bkpi-card\b', 'tree-node-row', content)
content = re.sub(r'\bcsat-alert-card\b', 'csat-alert-panel', content)
content = re.sub(r'\bitil-matrix-card\b', 'itil-matrix-panel', content)

# Clases card genéricas: class="... card ..." -> class="... tree-node-row ..."
def replace_card_class(m):
    classes = m.group(1).split()
    new_classes = [c if c.lower() not in ['card', 'cards', 'ticket-card'] else 'tree-node-row' for c in classes]
    return f'class="{" ".join(new_classes)}"'

content = re.sub(r'class="([^"]*\b(?:card|cards|ticket-card)\b[^"]*)"', replace_card_class, content)

# Grillas repetitivas
content = re.sub(r'grid-template-columns\s*:\s*repeat\s*\(\s*(?:auto-fit|auto-fill|\d+)\s*,\s*minmax\([^)]+\)\s*\)\s*;?',
                 'display: flex; flex-direction: column;', content)

# 2. Colores Rojos y Variantes
red_map = {
    "#EF4444": "#334155",
    "#ef4444": "#334155",
    "#DC2626": "#0F172A",
    "#dc2626": "#0F172A",
    "#F87171": "#64748B",
    "#f87171": "#64748B",
    "#B91C1C": "#1E293B",
    "#b91c1c": "#1E293B",
    "#991B1B": "#0F172A",
    "#991b1b": "#0F172A",
    "#FEF2F2": "#F8FAFC",
    "#fef2f2": "#F8FAFC",
    "#FEE2E2": "#F1F5F9",
    "#fee2e2": "#F1F5F9",
    "#FECACA": "#CBD5E1",
    "#fecaca": "#CBD5E1",
    "#FCA5A5": "#CBD5E1",
    "#fca5a5": "#CBD5E1",
}
for k, v in red_map.items():
    content = content.replace(k, v)

# Literal 'red' en estilos
content = re.sub(r':\s*red\b', ': #334155', content)

# 3. Azul Marino y Fondos Oscuros
content = content.replace("#002B49", "#00A896")
content = content.replace("#002b49", "#00A896")
content = content.replace("#1E3A8A", "#00A896")
content = content.replace("#1e3a8a", "#00A896")
content = content.replace("#172554", "#0F172A")
content = content.replace("#172554", "#0F172A")
content = content.replace("#0A192F", "#0F172A")
content = content.replace("#0a192f", "#0F172A")
content = content.replace("#1E40AF", "#334155")
content = content.replace("#1e40af", "#334155")
content = content.replace("#1D4ED8", "#00A896")
content = content.replace("#1d4ed8", "#00A896")

# Reemplazar colores saturados no Quantux mostrados por el usuario
content = content.replace("#00875A", "#00A896")
content = content.replace("#00875a", "#00A896")
content = content.replace("#0052CC", "#00A896")
content = content.replace("#0052cc", "#00A896")
content = content.replace("#10B981", "#00A896")
content = content.replace("#10b981", "#00A896")
content = content.replace("#059669", "#00A896")
content = content.replace("#059669", "#00A896")

# Fondos oscuros en elementos visuales
content = re.sub(r'background(?:-color)?\s*:\s*#0F172A\s*;?', 'background: #F8FAFC;', content, flags=re.IGNORECASE)
content = re.sub(r'background(?:-color)?\s*:\s*#1E293B\s*;?', 'background: #FFFFFF;', content, flags=re.IGNORECASE)
content = re.sub(r'background(?:-color)?\s*:\s*#000000\s*;?', 'background: #FFFFFF;', content, flags=re.IGNORECASE)
content = re.sub(r'background(?:-color)?\s*:\s*black\b\s*;?', 'background: #FFFFFF;', content, flags=re.IGNORECASE)

# 4. Términos Clínicos en index.html
# Guardia -> Mesa de Ayuda / Soporte Operativo
content = re.sub(r'\bguardia\b', 'soporte operativo', content, flags=re.IGNORECASE)
content = re.sub(r'\bguardias\b', 'soportes operativos', content, flags=re.IGNORECASE)
# Bypass -> Derivación directa
content = re.sub(r'\bbypass\b', 'derivación directa', content, flags=re.IGNORECASE)
# Asistencial -> Técnico-operativo
content = re.sub(r'\basistencial\b', 'técnico-operativo', content, flags=re.IGNORECASE)
content = re.sub(r'\basistenciales\b', 'técnico-operativos', content, flags=re.IGNORECASE)
# Triage -> Clasificación técnica
content = re.sub(r'\btriage\b', 'clasificación técnica', content, flags=re.IGNORECASE)

# 5. Widgets Vetados
content = re.sub(r'paciente\s+conectado', 'prestador en línea', content, flags=re.IGNORECASE)
content = re.sub(r'11m\s*45s', 'En Gestión', content, flags=re.IGNORECASE)
content = re.sub(r'resoluci[oó]n\s+oficial', 'Dictamen N1', content, flags=re.IGNORECASE)
content = re.sub(r'plan\s+6-030', 'Prestación Estándar', content, flags=re.IGNORECASE)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("index.html procesado.")
