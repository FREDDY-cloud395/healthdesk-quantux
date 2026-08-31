from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_uh01_suite():
    print("================================================================================")
    print("EJECUCIÓN DE PRUEBAS DE ACEPTACIÓN — UH-01: Autenticación de Usuarios por Rol")
    print("================================================================================\n")
    
    # CRITERIO 1: DADO un usuario registrado (Solicitante), CUANDO ingresa credenciales válidas, ENTONCES accede a su bandeja principal
    print("[ESCENARIO 1 - SOLICITANTE]")
    print("GIVEN: Usuario registrado 'solicitante' con rol SOLICITANTE en Quantux Salud")
    print("WHEN: Envía solicitud de login con usuario='solicitante' y rol='SOLICITANTE'")
    r_sol = client.post("/api/v1/auth/login", json={
        "username": "solicitante",
        "selected_role": "SOLICITANTE"
    })
    print(f"HTTP STATUS: {r_sol.status_code}")
    print(f"PAYLOAD RESPONSE: {json.dumps(r_sol.json(), indent=2)}")
    assert r_sol.status_code == 200
    assert r_sol.json()["status"] == "SUCCESS"
    assert r_sol.json()["role"] == "SOLICITANTE"
    assert r_sol.json()["landing_view"] == "mis_solicitudes"
    print("THEN: [PASÓ] Acceso autorizado. Redirigido a 'mis_solicitudes'.\n")

    # CRITERIO 2: DADO un usuario registrado (Operador de Soporte), CUANDO ingresa credenciales válidas, ENTONCES accede a la bandeja de triage / cockpit
    print("[ESCENARIO 2 - OPERADOR DE SOPORTE]")
    print("GIVEN: Usuario registrado 'soporte' con rol SOPORTE")
    print("WHEN: Envía solicitud de login con usuario='soporte' y rol='SOPORTE'")
    r_sop = client.post("/api/v1/auth/login", json={
        "username": "soporte",
        "selected_role": "SOPORTE"
    })
    print(f"HTTP STATUS: {r_sop.status_code}")
    print(f"PAYLOAD RESPONSE: {json.dumps(r_sop.json(), indent=2)}")
    assert r_sop.status_code == 200
    assert r_sop.json()["status"] == "SUCCESS"
    assert r_sop.json()["role"] == "SOPORTE"
    assert r_sop.json()["landing_view"] == "cockpit_soporte"
    print("THEN: [PASÓ] Acceso autorizado. Redirigido a 'cockpit_soporte'.\n")

    # CRITERIO 3: DADO un usuario registrado (Administrador), CUANDO ingresa credenciales válidas, ENTONCES accede al panel de administración
    print("[ESCENARIO 3 - ADMINISTRADOR]")
    print("GIVEN: Usuario registrado 'admin' con rol ADMIN")
    print("WHEN: Envía solicitud de login con usuario='admin' y rol='ADMIN'")
    r_adm = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "selected_role": "ADMIN"
    })
    print(f"HTTP STATUS: {r_adm.status_code}")
    print(f"PAYLOAD RESPONSE: {json.dumps(r_adm.json(), indent=2)}")
    assert r_adm.status_code == 200
    assert r_adm.json()["status"] == "SUCCESS"
    assert r_adm.json()["role"] == "ADMIN"
    assert r_adm.json()["landing_view"] == "panel_administracion"
    print("THEN: [PASÓ] Acceso autorizado. Redirigido a 'panel_administracion'.\n")

    # CRITERIO 4 (CASO NEGATIVO): DADO credenciales inválidas (usuario no existe), CUANDO intenta ingresar, ENTONCES muestra error y deniega el acceso
    print("[ESCENARIO 4 - CASO NEGATIVO: USUARIO INEXISTENTE]")
    print("GIVEN: Usuario 'usuario_fantasma' NO registrado en la base de datos")
    print("WHEN: Intenta autenticarse en el endpoint de login")
    r_inv = client.post("/api/v1/auth/login", json={
        "username": "usuario_fantasma"
    })
    print(f"HTTP STATUS: {r_inv.status_code}")
    print(f"PAYLOAD RESPONSE: {json.dumps(r_inv.json(), indent=2)}")
    assert r_inv.status_code == 401
    assert "Credenciales inválidas" in r_inv.json()["detail"]
    print("THEN: [PASÓ] Acceso rechazado con código HTTP 401 Unauthorized y mensaje de error descriptivo.\n")

    # CRITERIO 5 (CASO NEGATIVO): DADO un usuario que intenta ingresar con un rol que no le corresponde, ENTONCES deniega con 403 Forbidden
    print("[ESCENARIO 5 - CASO NEGATIVO: ROL NO COINCIDENTE]")
    print("GIVEN: Usuario 'solicitante' (cuyo rol real es SOLICITANTE)")
    print("WHEN: Intenta ingresar seleccionando rol 'ADMIN'")
    r_forb = client.post("/api/v1/auth/login", json={
        "username": "solicitante",
        "selected_role": "ADMIN"
    })
    print(f"HTTP STATUS: {r_forb.status_code}")
    print(f"PAYLOAD RESPONSE: {json.dumps(r_forb.json(), indent=2)}")
    assert r_forb.status_code == 403
    assert "Acceso denegado" in r_forb.json()["detail"]
    print("THEN: [PASÓ] Acceso rechazado con código HTTP 403 Forbidden.\n")

    # CRITERIO 6 (UH-29): Selector Rápido de Rol en 1 Clic
    print("[ESCENARIO 6 - SELECTOR RÁPIDO DE ROL (UH-29)]")
    print("GIVEN: Selector rápido en la barra superior")
    print("WHEN: Se solicita alternar al rol 'SOPORTE'")
    r_sw = client.get("/api/v1/auth/switch-role/SOPORTE")
    print(f"HTTP STATUS: {r_sw.status_code}")
    print(f"PAYLOAD RESPONSE: {json.dumps(r_sw.json(), indent=2)}")
    assert r_sw.status_code == 200
    assert r_sw.json()["role"] == "SOPORTE"
    print("THEN: [PASÓ] Contexto de rol alternado en 1 clic.\n")

    print("================================================================================")
    print("RESULTADO FINAL: 6/6 CASOS DE PRUEBA EXITOSOS (100% CUMPLIMIENTO)")
    print("================================================================================")

if __name__ == "__main__":
    test_uh01_suite()
