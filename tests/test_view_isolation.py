import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

ARTIFACT_DIR = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\804d2162-904e-4d53-a4d6-31fe80de76a4"

def verify_isolation():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        print("[1] Conectando a Quantux Enterprise...")
        driver.get("http://127.0.0.1:8000/")
        time.sleep(2)

        # Login si es necesario
        username_inputs = driver.find_elements(By.ID, "login-username")
        if username_inputs and username_inputs[0].is_displayed():
            username_inputs[0].send_keys("admin")
            driver.find_element(By.ID, "login-password").send_keys("admin123")
            driver.find_element(By.ID, "btn-login-submit").click()
            time.sleep(2)

        # Vistas a auditar
        views_to_test = [
            ("tickets", "Mesa de Ayuda"),
            ("dashboard", "Tablero de Control"),
            ("team-leader", "Torre de Control"),
            ("kanban", "Tablero Kanban N3"),
            ("users", "Usuarios y Roles"),
            ("articles", "Base de Conocimiento"),
            ("platforms", "Clientes y Plataformas")
        ]

        print("\n[2] AUDITORÍA DE AISLAMIENTO: Verificar que #view-unified-hub NO se muestre en ningún otro módulo...")
        for vname, label in views_to_test:
            driver.execute_script(f"switchView('{vname}');")
            time.sleep(1)

            view_elem = driver.find_element(By.ID, f"view-{vname}")
            uh_elem = driver.find_element(By.ID, "view-unified-hub")

            is_active_view_displayed = view_elem.is_displayed()
            is_uh_displayed = uh_elem.is_displayed()

            print(f"  -> Vista '{label}' ({vname}):")
            print(f"     Visible activa: {is_active_view_displayed}")
            print(f"     Mando Unificado visible: {is_uh_displayed}")

            assert is_active_view_displayed, f"ERROR: Vista {vname} no se visualiza"
            assert not is_uh_displayed, f"ERROR CRÍTICO: #view-unified-hub sigue visible en {vname}!"

            if vname == "tickets":
                shot_tickets = os.path.join(ARTIFACT_DIR, "mesa_de_ayuda_blindada_isolated.png")
                driver.save_screenshot(shot_tickets)
                print(f"     [OK] Captura de Mesa de Ayuda aislada guardada en: {shot_tickets}")

        print("\n[3] AUDITORÍA DE ACTIVACIÓN: Verificar que #view-unified-hub se muestre SOLO al seleccionarlo...")
        driver.execute_script("switchView('unified-hub');")
        time.sleep(1)

        uh_elem = driver.find_element(By.ID, "view-unified-hub")
        assert uh_elem.is_displayed(), "ERROR: #view-unified-hub no se muestra al seleccionarlo"
        
        # Validar que tickets, dashboard y team-leader estén ocultos
        assert not driver.find_element(By.ID, "view-tickets").is_displayed(), "ERROR: tickets no se ocultó"
        assert not driver.find_element(By.ID, "view-dashboard").is_displayed(), "ERROR: dashboard no se ocultó"
        assert not driver.find_element(By.ID, "view-team-leader").is_displayed(), "ERROR: team-leader no se ocultó"

        shot_uh = os.path.join(ARTIFACT_DIR, "mando_unificado_blindado_isolated.png")
        driver.save_screenshot(shot_uh)
        print(f"  -> [OK] Captura de Mando Unificado aislado guardada en: {shot_uh}")

        print("\n=========================================================")
        print("BLINDAJE DE AISLAMIENTO 100% CONFIRMADO Y EXITOSO")
        print("=========================================================\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    verify_isolation()
