"""
SCRIPT FORENSE DE QA Y ANÁLISIS DE DEUDA TÉCNICA
Objetivo: Auditar exhaustivamente la sincronización entre frontend/index.html y frontend/js/app.js.
Detectar:
1. getElementById huérfanos (IDs que el JS busca pero que NO existen en el HTML).
2. addEventListener sobre elementos nulos que rompen la ejecución del script.
3. Conflictos de scroll (overflow: hidden innecesarios, alturas fijas que provocan desborde o corte).
4. Discrepancias de estilo Pizarra Neutral (fondos oscuros, degradados saturados, colores no normalizados).
5. Duplicidad de IDs en el HTML.
6. Variables y llamadas a funciones no definidas en el scope.
"""
import re
from pathlib import Path

def audit_codebase():
    html_text = Path("frontend/index.html").read_text(encoding="utf-8")
    js_text = Path("frontend/js/app.js").read_text(encoding="utf-8")
    css_text = Path("frontend/css/styles.css").read_text(encoding="utf-8")

    findings = []

    # 1. Duplicidad de IDs en index.html
    html_ids = re.findall(r'id=["\']([^"\']+)["\']', html_text)
    seen_ids = set()
    dup_ids = set()
    for i in html_ids:
        if i in seen_ids:
            dup_ids.add(i)
        seen_ids.add(i)
    
    if dup_ids:
        findings.append({
            "modulo": "HTML / DOM",
            "tipo": "IDs Duplicados en DOM",
            "gravedad": "ALTA",
            "descripcion": f"Se encontraron {len(dup_ids)} IDs duplicados en index.html que causan comportamiento impredecible en getElementById",
            "detalles": list(dup_ids)[:15]
        })

    # 2. getElementById en JS que no existen en el HTML
    js_get_ids = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", js_text))
    missing_ids = [gid for gid in js_get_ids if gid not in seen_ids]
    
    # Filtrar IDs dinámicos que se crean por JS
    truly_missing = []
    for mid in missing_ids:
        # si tampoco se crea dinámicamente con innerHTML o createElement
        if f'id="{mid}"' not in js_text and f"id='{mid}'" not in js_text:
            truly_missing.append(mid)

    if truly_missing:
        findings.append({
            "modulo": "JavaScript / DOM Binding",
            "tipo": "Referencias a IDs Inexistentes (getById Fantasmas)",
            "gravedad": "CRÍTICA",
            "descripcion": f"El JS intenta manipular {len(truly_missing)} elementos por ID que NO existen en index.html ni en plantillas dinámicas",
            "detalles": truly_missing[:20]
        })

    # 3. addEventListener sin validación previa (posible Uncaught TypeError: Cannot read properties of null)
    # Buscar patrones: document.getElementById('xyz').addEventListener(...)
    direct_listeners = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)\.addEventListener", js_text)
    unsafe_listeners = [el_id for el_id in direct_listeners if el_id not in seen_ids]
    if unsafe_listeners:
        findings.append({
            "modulo": "JavaScript / Eventos",
            "tipo": "addEventListener sin Null-Check sobre IDs Faltantes",
            "gravedad": "CRÍTICA",
            "descripcion": "Llamadas directas a .addEventListener sobre getElementById que devuelven null y rompen el hilo de JS inicial",
            "detalles": unsafe_listeners
        })

    # 4. Gaps con el estilo Quantux Pizarra Neutral (fondos oscuros, negros o degradados en modales/tarjetas)
    dark_headers = re.findall(r"background:\s*(#[0-9a-fA-F]{3,6}|linear-gradient[^\;]+)", html_text)
    prohibited_colors = ["#0f172a", "#0a1c3e", "#1e293b", "#dc2626", "#b91c1c", "#ef4444", "#991b1b"]
    dark_matches = []
    for line_no, line in enumerate(html_text.splitlines(), 1):
        line_lower = line.lower()
        for pc in prohibited_colors:
            if pc in line_lower and ("modal" in line_lower or "header" in line_lower or "card" in line_lower or "alert" in line_lower):
                dark_matches.append(f"Línea {line_no}: {line.strip()[:90]}")
                break

    if dark_matches:
        findings.append({
            "modulo": "Estilos / Pizarra Neutral",
            "tipo": "Violación de Paleta Neutral (Fondos Oscuros / Rojos Saturados)",
            "gravedad": "ALTA",
            "descripcion": f"Se detectaron {len(dark_matches)} componentes visuales con fondos oscuros (#0A1C3E, #0F172A) o rojos saturados (#DC2626) prohibidos por OJO",
            "detalles": dark_matches[:12]
        })

    # 5. Problemas de Scroll / Desbordes
    scroll_issues = []
    for line_no, line in enumerate(html_text.splitlines(), 1):
        if "overflow: hidden" in line and ("modal-body" in line or "stream" in line or "table" in line or "cockpit" in line):
            scroll_issues.append(f"Línea {line_no}: {line.strip()[:90]}")
    
    # En CSS
    css_scroll_blocks = []
    for match in re.finditer(r"([^{}]+)\{[^}]*overflow:\s*hidden[^}]*\}", css_text):
        selector = match.group(1).strip()
        if any(k in selector for k in ["modal-body", "chat", "stream", "tickets-list", "detail-body", "kanban"]):
            css_scroll_blocks.append(selector)

    if scroll_issues or css_scroll_blocks:
        findings.append({
            "modulo": "Maquetación / Scroll & Overflow",
            "tipo": "Bloqueo de Scroll en Contenedores de Datos",
            "gravedad": "MEDIA",
            "descripcion": "Contenedores que fuerzan overflow: hidden impidiendo el desplazamiento vertical de contenido extenso",
            "detalles": (scroll_issues + css_scroll_blocks)[:10]
        })

    # 6. Funciones invocadas en onclick/oninput del HTML que no están en el JS
    html_on_calls = re.findall(r'on(?:click|change|input|submit|keydown)=["\']([a-zA-Z0-9_]+)\(', html_text)
    missing_functions = []
    for fn in set(html_on_calls):
        if f"function {fn}" not in js_text and f"const {fn} =" not in js_text and f"let {fn} =" not in js_text and f"var {fn} =" not in js_text and f"window.{fn} =" not in js_text:
            missing_functions.append(fn)

    if missing_functions:
        findings.append({
            "modulo": "JavaScript / Invocaciones Inline",
            "tipo": "Funciones en atributos on*() no declaradas en JS",
            "gravedad": "CRÍTICA",
            "descripcion": f"Se encontraron {len(missing_functions)} llamadas onclick/onchange/oninput en el HTML cuyas funciones NO existen en el JS",
            "detalles": missing_functions
        })

    # 7. Duplicación de bloques de código en JS
    # Buscar funciones declaradas dos veces en app.js
    declared_fns = re.findall(r"function\s+([a-zA-Z0-9_]+)\s*\(", js_text)
    fn_counts = {}
    for f in declared_fns:
        fn_counts[f] = fn_counts.get(f, 0) + 1
    duplicated_fns = [f for f, c in fn_counts.items() if c > 1]

    if duplicated_fns:
        findings.append({
            "modulo": "Deuda Técnica / JS",
            "tipo": "Funciones Duplicadas en app.js",
            "gravedad": "ALTA",
            "descripcion": f"Se detectaron {len(duplicated_fns)} funciones redeclaradas múltiples veces en app.js (la última sobreescribe a las anteriores)",
            "detalles": duplicated_fns[:15]
        })

    print(f"\nAUDITORÍA FORENSE COMPLETADA: {len(findings)} CATEGORÍAS DE HALLAZGOS DETECTADAS")
    import json
    out_file = Path("forensic_qa_findings.json")
    out_file.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")
    
    for f in findings:
        print(f"\n[{f['gravedad']}] {f['modulo']} -> {f['tipo']}")
        print(f"  Descripción: {f['descripcion']}")
        print(f"  Muestra de elementos ({len(f['detalles'])}): {f['detalles'][:5]}")

if __name__ == "__main__":
    audit_codebase()
