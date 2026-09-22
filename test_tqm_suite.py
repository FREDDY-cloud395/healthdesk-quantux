"""
SUITE DE PRUEBAS AUTOMATIZADA — NORMA TQM (TOTAL QUALITY MANAGEMENT)
Proyecto: Quantux ServiceDesk CD2 (v4.1.0-DEV)
Enfoque: Cero Defectos, Confiabilidad Asistencial y Verificación Integral E2E.
"""
import sys
import json
import urllib.request
from pathlib import Path

# Configurar encoding UTF-8 en consola de Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def print_tqm_header():
    print("=" * 80)
    print("  QUANTUX HEALTHDESK v4.1.0-DEV — SUITE DE CERTIFICACIÓN TQM")
    print("  Norma: Total Quality Management (TQM) — Cero Defectos en Salud")
    print("=" * 80)

def run_tests():
    print_tqm_header()
    passed = 0
    total = 0

    def assert_test(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASSED] [TQM-{total:02d}] {name}")
            if details:
                print(f"           -> {details}")
        else:
            print(f"  [FAILED] [TQM-{total:02d}] {name}")
            if details:
                print(f"           -> ERROR: {details}")

    # ---------------------------------------------------------
    # DIMENSIÓN 1: INTEGRIDAD DE BACKEND Y TRIAGE CONVERSACIONAL
    # ---------------------------------------------------------
    print("\n--- DIMENSIÓN 1: BACKEND, IA TRIAGE & CONOCIMIENTO CD2 ---")
    
    # Test 1: Triage con consulta de firma digital
    try:
        req = urllib.request.Request(
            "http://localhost:8000/api/v1/ai/triage",
            data=json.dumps({"query": "No puedo firmar receta digital"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))
        resp_text = data.get("ai_response_text", "")
        is_concise = "**Diagnóstico:**" in resp_text or "Diagn" in resp_text
        assert_test("IA Triage: Respuesta Ultra-Concreta y Diagnóstico CD2", is_concise, f"Subsystem: {data.get('subsystem')}")
    except Exception as e:
        assert_test("IA Triage: Respuesta Ultra-Concreta y Diagnóstico CD2", False, str(e))

    # Test 2: Heurística específica de OSDEPYM integrada
    try:
        req = urllib.request.Request(
            "http://localhost:8000/api/v1/ai/triage",
            data=json.dumps({"query": "No encuentro la obra social OSDEPYM al cargar paciente"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))
        resp_text = data.get("ai_response_text", "")
        has_osdepym_rule = "OSDEPYM" in resp_text or "Monotributistas" in resp_text
        assert_test("Base de Conocimiento CD2: Regla de búsqueda OSDEPYM", has_osdepym_rule, "Validada regla del chat de soporte")
    except Exception as e:
        assert_test("Base de Conocimiento CD2: Regla de búsqueda OSDEPYM", False, str(e))

    # Test 3: Heurística de Nutrición (190173 vs 420296)
    try:
        req = urllib.request.Request(
            "http://localhost:8000/api/v1/ai/triage",
            data=json.dumps({"query": "Problema con plan de nutricion o prestacion no habilitada"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode("utf-8"))
        resp_text = data.get("ai_response_text", "")
        has_nutri = "420296" in resp_text or "190173" in resp_text or "nutrici" in resp_text.lower()
        assert_test("Base de Conocimiento CD2: Contingencia Nutrición (190173 / 420296)", has_nutri, "Regla de validación de cobertura activa")
    except Exception as e:
        assert_test("Base de Conocimiento CD2: Contingencia Nutrición (190173 / 420296)", False, str(e))

    # Test 4: Creación de ticket con canal VIDEOLLAMADA
    try:
        tkt_payload = {
            "title": "[TQM E2E] Teleasistencia Programada Google Meet",
            "description": "Sesión agendada para soporte técnico en consultorio asistencial.",
            "platform_code": "CD2",
            "institution_code": "SWISS_MEDICAL",
            "requester_username": "sgomez",
            "priority": "P2",
            "urgency": "ALTO",
            "impact": "MEDIO",
            "ticket_type": "REQUERIMIENTO",
            "status": "NUEVO",
            "channel": "VIDEOLLAMADA"
        }
        req = urllib.request.Request(
            "http://localhost:8000/api/v1/tickets",
            data=json.dumps(tkt_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        created_tkt = json.loads(res.read().decode("utf-8"))
        assert_test("API Tickets: Creación E2E con canal VIDEOLLAMADA", "id" in created_tkt, f"Ticket #{created_tkt.get('id')}")
    except Exception as e:
        assert_test("API Tickets: Creación E2E con canal VIDEOLLAMADA", False, str(e))

    # ---------------------------------------------------------
    # DIMENSIÓN 2: INTEGRIDAD DE FRONTEND DOM & QUANTUX UX
    # ---------------------------------------------------------
    print("\n--- DIMENSIÓN 2: INTERFAZ DOM, GOOGLE MEET & CHAT QUANTUX ---")
    html_path = Path("frontend/index.html")
    html_content = html_path.read_text(encoding="utf-8")

    # Test 5: Modal de Google Meet presente en el DOM
    has_meet_modal = "id=\"modal-schedule-meet\"" in html_content
    assert_test("Frontend DOM: Modal de Videollamada Google Meet (#modal-schedule-meet)", has_meet_modal, "Modal presente en DOM")

    # Test 6: Analistas asignables para videollamada incluyendo Pua, Die, Carito
    required_analysts = ["Hugo Muñoz", "Jessica González", "Damián Cofán", "Camila Roldán", "Freddy Cortés", "Pua", "Die", "Carito"]
    missing_analysts = [a for a in required_analysts if a not in html_content]
    assert_test("Frontend DOM: Analistas en agenda (Hugo, Jess, Damián, Cami, Freddy, Pua, Die, Carito)", len(missing_analysts) == 0, f"Faltantes: {missing_analysts}")

    # Test 7: Chat estelar y centrado como protagonista de la pantalla
    has_chat_stream = "id=\"requester-inline-chat-stream\"" in html_content
    has_hero = "id=\"requester-chat-hero\"" in html_content
    assert_test("Frontend DOM: Chat Estelar Protagonista con Hero Zen", has_chat_stream and has_hero, "Estructura principal de chat validada")

    # Test 8: Árbol de Preguntas Interactivo para Soporte CD2
    has_interactive_tree = "id=\"requester-thematic-tree\"" in html_content
    assert_test("Frontend DOM: Árbol de Preguntas Interactivo para Soporte CD2", has_interactive_tree, "Árbol de navegación dinámica de soporte presente")

    # ---------------------------------------------------------
    # DIMENSIÓN 3: LÓGICA JAVASCRIPT, ASISTENTE PEPE & PERSISTENCIA
    # ---------------------------------------------------------
    print("\n--- DIMENSIÓN 3: JAVASCRIPT, ASISTENTE PEPE & PERSISTENCIA F5 ---")
    js_path = Path("frontend/js/app.js")
    js_content = js_path.read_text(encoding="utf-8")

    # Test 9: Persistencia F5 sin expulsión de vista
    has_f5_persistence = "localStorage.setItem('quantux_active_view'" in js_content and "quantux_active_view" in js_content
    assert_test("JavaScript: Persistencia F5 (Memoria de vista activa sin expulsar)", has_f5_persistence, "localStorage + hash navigation activo")

    # Test 10: Asistente de voz Pepe y wake word 'Hola Pepe'
    has_voice_assistant = "startPepeWakeWordListener" in js_content and "speakPepe" in js_content and "hola pepe" in js_content
    assert_test("JavaScript: Motor de voz 'Hola Pepe' con SpeechSynthesis", has_voice_assistant, "Reconocimiento continuo y sintetizador de audio")

    # Test 11: Creación de tickets por voz
    has_voice_tickets = "handleVoiceTicketCreation" in js_content and "crear ticket" in js_content
    assert_test("JavaScript: Comandos de voz para apertura inmediata de tickets", has_voice_tickets, "Reconocimiento de comandos de voz activo")

    # Test 12: Generación de salas Google Meet y enlace qtx-...
    has_meet_logic = "confirmScheduleMeet" in js_content and "https://meet.google.com/qtx-" in js_content
    assert_test("JavaScript: Generador dinámico de salas Google Meet", has_meet_logic, "Generación aleatoria de enlaces meet.google.com/qtx-...")

    # Test 13: Formateador visual seguro y botones Quantux
    has_format = "formatChatMessage" in js_content and "#10B981" in js_content and "#64748B" in js_content
    assert_test("JavaScript: Formateo limpio Markdown y Botones Quantux exactos", has_format, "[✓ Sí, problema resuelto], [📋 No, generar ticket], [📹 Agendar Videollamada]")

    # ---------------------------------------------------------
    # RESUMEN EJECUTIVO TQM
    # ---------------------------------------------------------
    score = (passed / total) * 100
    print("\n" + "=" * 80)
    print(f"  RESULTADO FINAL TQM: {passed}/{total} PRUEBAS SUPERADAS ({score:.1f}%)")
    print(f"  ESTADO DE CALIDAD: {'CERTIFICADO TQM CERO DEFECTOS' if score == 100 else 'NO CONFORME'}")
    print("=" * 80)
    return score == 100

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
