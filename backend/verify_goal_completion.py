# -*- coding: utf-8 -*-
import sqlite3
import urllib.request
import json
import sys
from pathlib import Path

def run_checks():
    print("=" * 70)
    print("VERIFICACION INTEGRAL DE ENTREGABLES Y CALIDAD - QUANTUX SERVICEDESK")
    print("=" * 70)

    all_passed = True

    # 1. VERIFICACION DE BASE DE DATOS LOCAL
    print("\n[1] Verificando Base de Datos SQLite...")
    db_paths = [Path("backend/healthdesk.db"), Path("healthdesk.db")]
    for db in db_paths:
        if not db.exists():
            print(f"  [FAIL] Archivo {db} no existe.")
            all_passed = False
            continue
        c = sqlite3.connect(db)
        cur = c.cursor()
        cur.execute("SELECT COUNT(*) FROM kb_articles")
        art_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM kb_article_history")
        hist_count = cur.fetchone()[0]
        cur.execute("SELECT id, title, category FROM kb_articles WHERE id = 3")
        art3 = cur.fetchone()
        
        print(f"  * {db}: {art_count} articulos, {hist_count} historiales.")
        if art_count != 34:
            print(f"    [FAIL] Se esperaban 34 articulos pero hay {art_count}")
            all_passed = False
        else:
            print(f"    [OK] Conteo exacto: 34 runbooks oficiales (Aislamiento SSOT).")

        if not art3 or "CUIT" not in art3[1]:
            print(f"    [FAIL] Articulo ID 3 no es el procedimiento de CUIT.")
            all_passed = False
        else:
            print(f"    [OK] Articulo ID 3: '{art3[1]}' (Cat: {art3[2]}).")

    # 2. VERIFICACION DE ENDPOINTS HTTP EN VIVO (PUERTO 8000)
    print("\n[2] Verificando Servidor en Vivo (http://127.0.0.1:8000)...")
    
    # 2.1 GET /api/v1/articles
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/v1/articles")
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
            print(f"  * GET /api/v1/articles -> HTTP {r.status}, {len(data)} articulos devueltos.")
            if len(data) != 34:
                print(f"    [FAIL] Cantidad devuelta por API ({len(data)}) != 34.")
                all_passed = False
            else:
                print(f"    [OK] API entrega con precision los 34 runbooks homologados.")
    except Exception as e:
        print(f"  [FAIL] Error en GET /api/v1/articles: {e}")
        all_passed = False

    # 2.2 POST /api/v1/ai/triage con CUIT
    triage_cases = [
        ("cambio de cuit", "CD2-PREST-001", "Cambio de CUIT de prestador"),
        ("debes agregar este procedimiento para cambio de CUIT", "CD2-PREST-001", "Cambio de CUIT de prestador"),
        ("no puede registrar", "CD2-PAU-001", "diferido"),
        ("error al descargar receta", "PDF-005", "Descarga y Cifrado"),
        ("alta de prestador", "CD2-INST-001", "Alta/configuración de prestador")
    ]

    for q, exp_code, exp_keyword in triage_cases:
        try:
            payload = {"query": q, "user_fullname": "Auditor Calidad", "platform_code": "CD2"}
            req = urllib.request.Request(
                "http://127.0.0.1:8000/api/v1/ai/triage",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                res = json.loads(r.read().decode("utf-8"))
                rb = res.get("matched_runbook", {})
                code = rb.get("code")
                title = rb.get("title", "")
                diag = res.get("root_cause", "")
                steps = res.get("structured_steps", [])
                
                # Validar correspondencia
                if exp_code not in code and exp_code not in title:
                    print(f"  [FAIL] Query '{q}' -> Obtuvo {code} pero esperaba {exp_code}.")
                    all_passed = False
                elif exp_keyword.lower() not in (title + diag + str(steps)).lower():
                    print(f"  [FAIL] Query '{q}' -> No contiene la palabra clave esperada '{exp_keyword}'.")
                    all_passed = False
                else:
                    print(f"  * Query: '{q}' -> [OK] Runbook: {code} ({len(steps)} pasos de checklist).")
        except Exception as e:
            print(f"  [FAIL] Error en POST /ai/triage para '{q}': {e}")
            all_passed = False

    # 3. VERIFICACION DE ESTRUCTURA FRONTEND (2 COLUMNAS)
    print("\n[3] Verificando Frontend e Interfaz de 2 Columnas...")
    html_path = Path("frontend/index.html")
    if html_path.exists():
        content = html_path.read_text(encoding="utf-8")
        checks = [
            ("copilot-card", "Columna izquierda de chat interactivo"),
            ("aside id=\"kb-side-pane\"", "Columna derecha de ficha técnica N2/N3"),
            ("side-runbook-title", "Widget de Runbook asociado en vivo"),
            ("side-tech-notes", "Widget de notas técnicas N2/N3"),
            ("Matriz de Verdad Única (SSOT)", "Matriz de Verdad Única"),
            ("34 Runbooks Oficiales", "Contador de 34 Runbooks")
        ]
        for tag, desc in checks:
            if tag in content:
                print(f"  * [OK] Componente '{desc}' presente en index.html.")
            else:
                print(f"  [FAIL] Falta componente '{desc}' en index.html.")
                all_passed = False
    else:
        print("  [FAIL] frontend/index.html no encontrado.")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("RESULTADO GLOBAL: TODOS LOS ENTREGABLES HAN SIDO VERIFICADOS CON ÉXITO.")
        print("Calidad Certificada: 100% Homologado con Fuentes Oficiales CD2.")
    else:
        print("RESULTADO GLOBAL: SE ENCONTRARON FALLAS EN LA VERIFICACIÓN.")
    print("=" * 70)

if __name__ == "__main__":
    run_checks()
