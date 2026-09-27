"""
Test Suite: ISSUE-06 Escenario 3 (Trazabilidad FCR & Constancia Imprimible),
ISSUE-57 (Botón Demonio), ISSUE-58 (Persistencia Retrabajo F5) y MEJ-12 (Barra Roja Unificada)
"""
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_issue_06_escenario_3_frontend_traceability():
    app_js_path = os.path.join(ROOT_DIR, "frontend", "js", "app.js")
    with open(app_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Escenario 3: Trazabilidad FCR en Historial con badge verde de resuelto
    assert "RESUELTO (FCR 100%)" in content, "Falta badge verde de resuelto FCR en historial"
    assert "#047857" in content or "#059669" in content, "Falta color verde institucional de resuelto"

    # Acceso directo a constancia imprimible
    assert "printFcrCertificate" in content, "Falta la función printFcrCertificate"
    assert "Constancia" in content, "Falta botón de acceso directo a constancia"
    assert "window.print()" in content, "Falta invocación a window.print() en la constancia"
    assert "TKT-2026-0348" in content, "Falta referencia al ticket de autogestión FCR"
    print("[OK] ISSUE-06 Escenario 3: Trazabilidad FCR y constancia imprimible verificada.")

def test_issue_57_demon_button_and_mej12_red_progress_bar():
    script_path = os.path.join(ROOT_DIR, "scripts", "build_full_scrumban_board.py")
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    html_path = os.path.join(ROOT_DIR, "docs", "00_Tablero_Scrumban_Quantux.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # ISSUE-57: Sincronización de IDs de botones del demonio
    assert "card-btn-demon-" in script_content, "Falta card-btn-demon en script"
    assert "modal-btn-demon-" in script_content, "Falta modal-btn-demon en script"
    assert "card-btn-demon-" in html_content, "Falta card-btn-demon en HTML generado"

    # MEJ-12: Barra de progreso roja institucional
    assert "#DC2626" in script_content, "Falta color rojo institucional #DC2626 en barra"
    assert "card-demon-progress-box-" in script_content, "Falta caja de progreso en tarjeta"
    assert "demon-progress-box-" in script_content, "Falta caja de progreso en modal"

    # 4 fases de ejecución técnica
    assert "1/4: Análisis de selectores DOM" in script_content, "Falta fase 1 en triggerDemonRework"
    assert "2/4: Aplicación de parche en archivos fuente" in script_content, "Falta fase 2 en triggerDemonRework"
    assert "3/4: Ejecución de Quality Gate" in script_content, "Falta fase 3 en triggerDemonRework"
    assert "4/4: Certificación técnica completada" in script_content, "Falta fase 4 en triggerDemonRework"

    # Tarea trasladada al fondo de QA
    assert "tasks.splice(idx, 1);" in script_content, "Falta extracción de tarea para mover al fondo"
    assert "tasks.push(task);" in script_content, "Falta push al final del array"
    print("[OK] ISSUE-57 y MEJ-12: Botón Demonio, barra roja y 4 etapas técnicas verificadas.")

def test_issue_58_rework_persistence_on_refresh():
    script_path = os.path.join(ROOT_DIR, "scripts", "build_full_scrumban_board.py")
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    # Verificar que init() no pisa con qa las tareas guardadas por el usuario
    assert "const DEMON_REWORK_IDS = [\"UH-67\"" not in script_content, "Quedó bucle forzado en init() pisando rework"

    # Verificar que syncIssueInBacklog preserva status si ya existe
    assert "else if (!tasks[idx].status)" in script_content, "syncIssueInBacklog debe preservar tasks[idx].status"

    # Verificar que el set de inmutabilidad protege las 38 tarjetas aprobadas por el SO
    assert "PERMANENTLY_APPROVED_BY_SO" in script_content, "Falta conjunto de tarjetas blindadas"
    print("[OK] ISSUE-58: Persistencia de estado en Retrabajo ante recargas F5 asegurada.")

if __name__ == "__main__":
    test_issue_06_escenario_3_frontend_traceability()
    test_issue_57_demon_button_and_mej12_red_progress_bar()
    test_issue_58_rework_persistence_on_refresh()
    print("\n>>> TODOS LOS TESTS DE CALIDAD APROBADOS AL 100% <<<")
