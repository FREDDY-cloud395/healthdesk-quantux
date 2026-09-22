# -*- coding: utf-8 -*-
"""
Test Suite: Bot de Gestión de Incidencias Masivas (MajorIncidentBot)
y Motor Cognitivo N3 (ai_triage.py) - QuantUX HealthDesk ITIL v4
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.db.session import engine, init_db
from app.models.entities import Ticket, TicketStatus, TicketType, PriorityLevel
from app.services.major_incident_bot import MajorIncidentBot
from app.services.ai_triage import N3CognitiveTriageEngine

client = TestClient(app)

def reset_test_environment():
    """Resuelve tickets previos recientes para asegurar un punto de partida limpio sin violar FKs."""
    with Session(engine) as session:
        # Resolver incidentes mayores activos previos
        majors = session.exec(
            select(Ticket)
            .where(Ticket.is_major_incident == True)
            .where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
        ).all()
        for m in majors:
            m.status = TicketStatus.RESUELTO
            session.add(m)
        
        # Resolver tickets de CD2 abiertos creados en la última hora
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_open = session.exec(
            select(Ticket)
            .where(Ticket.created_at >= one_hour_ago)
            .where(Ticket.status.notin_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
        ).all()
        for t in recent_open:
            t.status = TicketStatus.RESUELTO
            session.add(t)
        session.commit()

def test_1_threshold_detection_and_parent_creation():
    print("\n--- TEST 1: Detección de Umbral ITIL (>=3 tickets en <30 min) y Creación de Ticket Padre ---")
    reset_test_environment()
    
    # 1. Crear 2 tickets individuales en la misma plataforma crítica (CAT_CONSULTORIO_DIGITAL)
    payload_1 = {
        "title": "Error 504 Gateway Timeout en Consultorio Digital",
        "description": "Médicos de guardia no pueden abrir historias clínicas",
        "platform_code": "CAT_CONSULTORIO_DIGITAL",
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "ALTO",
        "urgency": "ALTO",
        "requester_username": "solicitante"
    }
    r1 = client.post("/api/v1/tickets", json=payload_1)
    assert r1.status_code == 200, f"Error creando ticket 1: {r1.text}"
    t1 = r1.json()
    assert t1["parent_ticket_id"] is None, "Ticket 1 no debería tener padre aún"
    print("  [OK] Ticket 1 creado sin padre")

    payload_2 = {
        "title": "Pantalla blanca al seleccionar turno en Consultorio",
        "description": "Se queda cargando indefinidamente",
        "platform_code": "CAT_CONSULTORIO_DIGITAL",
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "ALTO",
        "urgency": "ALTO",
        "requester_username": "dra_gomez"
    }
    r2 = client.post("/api/v1/tickets", json=payload_2)
    assert r2.status_code == 200, f"Error creando ticket 2: {r2.text}"
    t2 = r2.json()
    assert t2["parent_ticket_id"] is None, "Ticket 2 no debería tener padre aún"
    print("  [OK] Ticket 2 creado sin padre")

    # 3. Crear el 3er ticket (debe superar el umbral >= 3 y disparar la Incidencia Masiva)
    payload_3 = {
        "title": "Falla general de acceso en CD2",
        "description": "Consultorio Digital no responde peticiones",
        "platform_code": "CD2",  # Alias de CAT_CONSULTORIO_DIGITAL
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "ALTO",
        "urgency": "ALTO",
        "requester_username": "dra_martinez"
    }
    r3 = client.post("/api/v1/tickets", json=payload_3)
    assert r3.status_code == 200, f"Error creando ticket 3: {r3.text}"
    t3 = r3.json()
    
    # Verificar que el ticket 3 quedó asociado al ticket padre
    assert t3["parent_ticket_id"] is not None, "El ticket 3 debe tener un parent_ticket_id asignado"
    parent_id = t3["parent_ticket_id"]
    print(f"  [OK] Ticket 3 asociado exitosamente al Ticket Padre: {parent_id}")

    # Verificar en la base de datos que el ticket padre cumple los criterios ITIL
    with Session(engine) as session:
        parent_ticket = session.get(Ticket, parent_id)
        assert parent_ticket is not None, "El ticket padre debe existir en BD"
        assert parent_ticket.is_major_incident is True, "El ticket padre debe tener is_major_incident=True"
        assert parent_ticket.ticket_type == TicketType.PROBLEMA, f"Tipo de ticket debe ser PROBLEMA, obtenido: {parent_ticket.ticket_type}"
        assert parent_ticket.priority == PriorityLevel.P1, f"Prioridad debe ser P1, obtenido: {parent_ticket.priority}"
        assert parent_ticket.status == TicketStatus.EN_CURSO, "Estado debe ser EN_CURSO"
        
        # Verificar que los tickets 1 y 2 fueron retroactivamente vinculados como hijos
        db_t1 = session.get(Ticket, t1["id"])
        db_t2 = session.get(Ticket, t2["id"])
        assert db_t1.parent_ticket_id == parent_id, f"Ticket 1 no fue vinculado al padre {parent_id}"
        assert db_t2.parent_ticket_id == parent_id, f"Ticket 2 no fue vinculado al padre {parent_id}"
        print(f"  [OK] Tickets previos 1 y 2 retroactivamente vinculados como hijos al padre {parent_id}")
        print("  [OK] Ticket Padre validado: is_major_incident=True, ticket_type=PROBLEMA, priority=P1")

def test_2_child_ticket_auto_association():
    print("\n--- TEST 2: Asociación Automática de Nuevos Tickets Hijos Entrantes ---")
    # Ingresar un 4to ticket en la misma plataforma mientras la incidencia masiva sigue activa
    payload_4 = {
        "title": "Error persistente en Consultorio Digital",
        "description": "Continúa el error 504 al ingresar",
        "platform_code": "CD2",
        "institution_code": "OSDE",
        "ticket_type": "INCIDENTE",
        "impact": "MEDIO",
        "urgency": "ALTO",
        "requester_username": "dr_lopez"
    }
    r4 = client.post("/api/v1/tickets", json=payload_4)
    assert r4.status_code == 200, f"Error creando ticket 4: {r4.text}"
    t4 = r4.json()
    assert t4["parent_ticket_id"] is not None, "Ticket 4 entrante debe asociarse automáticamente al padre activo"
    print(f"  [OK] Ticket 4 entrante asociado automáticamente al padre: {t4['parent_ticket_id']}")

def test_3_endpoint_get_active_major_incident():
    print("\n--- TEST 3: Endpoint GET /api/v1/tickets/major-incidents/active ---")
    resp = client.get("/api/v1/tickets/major-incidents/active")
    assert resp.status_code == 200, f"Error en endpoint active: {resp.text}"
    data = resp.json()
    assert data["has_active_major_incident"] is True, "Debe reportar incidencia masiva activa"
    parent = data["parent_ticket"]
    assert parent is not None, "Debe devolver el ticket padre"
    assert parent["is_major_incident"] is True
    assert parent["ticket_type"] == "PROBLEMA"
    assert parent["priority"] == "P1"
    
    children = data["child_tickets"]
    assert isinstance(children, list), "child_tickets debe ser una lista"
    assert len(children) >= 4, f"Se esperaban al menos 4 tickets hijos, obtenidos: {len(children)}"
    print(f"  [OK] Endpoint GET devolvió ticket padre #{parent['id']} y {len(children)} tickets hijos")

def test_4_endpoint_post_declare_major_incident():
    print("\n--- TEST 4: Endpoint POST /api/v1/tickets/major-incidents/declare ---")
    payload = {
        "title": "Caída del Servidor de Firma Digital PKI y ANMAT",
        "description": "Falla generalizada en servicio de token y firma digital de recetas",
        "platform_code": "CAT_RECETA",
        "institution_code": "OSDE",
        "declared_by": "admin"
    }
    resp = client.post("/api/v1/tickets/major-incidents/declare", json=payload)
    assert resp.status_code == 200, f"Error declarando incidencia masiva: {resp.text}"
    data = resp.json()
    assert data["status"] == "success"
    parent_id = data["parent_ticket_id"]
    parent = data["parent_ticket"]
    assert parent["is_major_incident"] is True
    assert parent["ticket_type"] == "PROBLEMA"
    assert parent["priority"] == "P1"
    print(f"  [OK] Incidencia masiva declarada manualmente exitosa: {parent_id} (PROBLEMA, P1)")

def test_5_ai_triage_greetings_with_active_major_incident():
    print("\n--- TEST 5: ai_triage con Saludos e Incidencia Masiva Activa ---")
    # Actualmente hay incidencia masiva activa (CAT_RECETA / CD2)
    greetings = ["hola", "pepe", "buen dia", "buen día", "hola pepe", "buenas tardes"]
    
    for g in greetings:
        res = N3CognitiveTriageEngine.analyze_incident(
            query_text=g,
            user_role="SOLICITANTE",
            user_fullname="Dr. Fernando Romero",
            platform_code="CD2"
        )
        assert res["is_greeting"] is True, f"'{g}' debe ser reconocido como saludo"
        assert res["is_major_incident_alert"] is True, f"'{g}' debe alertar de corte activo"
        assert "Alerta de Incidencia Masiva Activa" in res["ai_response_text"] or "Ticket de Problema" in res["ai_response_text"]
        assert "Procedimiento estándar de soporte" not in res["recommended_action"], "NUNCA debe devolver plantilla de soporte genérico para saludos"
        assert res["suggest_ticket"] is False, "No debe pedir generar ticket si hay corte masivo"
        print(f"  [OK] Saludo '{g}' -> Alerta inmediata de Incidencia Masiva (sin plantilla de diagnóstico)")

def test_6_ai_triage_greetings_without_major_incident():
    print("\n--- TEST 6: ai_triage con Saludos SIN Incidencia Masiva Activa ---")
    # Marcamos los tickets de incidencia masiva como RESUELTO en la BD
    with Session(engine) as session:
        majors = session.exec(select(Ticket).where(Ticket.is_major_incident == True)).all()
        for m in majors:
            m.status = TicketStatus.RESUELTO
            session.add(m)
        session.commit()

    greetings = ["hola", "pepe", "buen dia", "hola pepe", "buenas noches", "que tal"]
    for g in greetings:
        res = N3CognitiveTriageEngine.analyze_incident(
            query_text=g,
            user_role="SOLICITANTE",
            user_fullname="Dr. Fernando Romero",
            platform_code="CD2"
        )
        assert res["is_greeting"] is True, f"'{g}' debe ser reconocido como saludo"
        assert res.get("is_major_incident_alert") is False, "No debe haber alerta de corte"
        assert "Soporte AI" in res["ai_response_text"] or "Asistente" in res["ai_response_text"]
        assert "¿En qué puedo ayudarte" in res["ai_response_text"] or "asistente" in res["ai_response_text"] or "de inmediato" in res["ai_response_text"]
        assert "Procedimiento estándar de soporte" not in res["recommended_action"], "NUNCA debe devolver plantilla de soporte genérico para saludos"
        assert res["suggest_ticket"] is False
        print(f"  [OK] Saludo '{g}' -> Saludo cálido y cordial personalizado (sin falso diagnóstico)")

def test_7_ai_triage_cefalea_cie10_snomed():
    print("\n--- TEST 7: ai_triage Búsqueda de Diagnóstico Cefalea (CIE-10 / SNOMED CT) ---")
    cefalea_queries = [
        "no encuentro diagnostico cefalea",
        "como codifico cefalea en la consulta",
        "diagnostico cefalea dolor de cabeza",
        "dolor de cabeza en el nomenclador"
    ]
    for q in cefalea_queries:
        res = N3CognitiveTriageEngine.analyze_incident(
            query_text=q,
            user_role="SOLICITANTE",
            user_fullname="Dra. Mariana López",
            platform_code="CD2"
        )
        assert res.get("is_greeting") is not True
        assert res["has_concrete_solution"] is True, "Cefalea debe tener solución concreta"
        
        # Debe contener CIE-10 (G44.2, R51) y SNOMED (25064002)
        response_text = "\n".join(res["solution_steps"]) + " " + res["ai_response_text"]
        assert "G44.2" in response_text, f"Debe contener código CIE-10 G44.2 para '{q}'"
        assert "R51" in response_text, f"Debe contener código CIE-10 R51 para '{q}'"
        assert "25064002" in response_text, f"Debe contener código SNOMED CT 25064002 para '{q}'"
        print(f"  [OK] Consulta '{q}' -> Devuelve CIE-10 (G44.2, R51) y SNOMED CT (25064002)")

def test_8_ai_triage_no_kb_match_suggest_ticket():
    print("\n--- TEST 8: ai_triage Consulta Desconocida sin Match en KB -> Sugerir Ticket ---")
    unknown_query = "zkxpw error criptografico inexplicable en transmutador"
    res = N3CognitiveTriageEngine.analyze_incident(
        query_text=unknown_query,
        user_role="SOLICITANTE",
        user_fullname="Dr. Valenzuela",
        platform_code="CD2"
    )
    assert res.get("is_greeting") is not True
    assert res["has_concrete_solution"] is False, "Consulta desconocida no debe tener solución concreta"
    assert res["suggest_ticket"] is True, "Debe recomendar explícitamente abrir un ticket"
    assert "se recomienda generar un ticket" in res["ai_response_text"].lower() or "generar un ticket de soporte" in res["ai_response_text"].lower()
    assert "Mesa de Guardia Técnica" in res["subsystem"] or "Mesa de Guardia" in res["recommended_action"]
    print("  [OK] Consulta desconocida -> has_concrete_solution=False, suggest_ticket=True, recomienda generar ticket")

if __name__ == "__main__":
    print("======================================================================")
    print("EJECUTANDO SUITE DE VALIDACIÓN ITIL MAJOR INCIDENT & AI TRIAGE")
    print("======================================================================")
    try:
        init_db()
        test_1_threshold_detection_and_parent_creation()
        test_2_child_ticket_auto_association()
        test_3_endpoint_get_active_major_incident()
        test_4_endpoint_post_declare_major_incident()
        test_5_ai_triage_greetings_with_active_major_incident()
        test_6_ai_triage_greetings_without_major_incident()
        test_7_ai_triage_cefalea_cie10_snomed()
        test_8_ai_triage_no_kb_match_suggest_ticket()
        print("\n======================================================================")
        print(">>> TODOS LOS TESTS PASARON EXITOSAMENTE (100% OK) <<<")
        print("======================================================================")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Test falló: {e}")
        sys.exit(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[ERROR] Excepción inesperada: {e}")
        sys.exit(1)
