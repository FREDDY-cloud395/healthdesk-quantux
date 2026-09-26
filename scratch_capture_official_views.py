import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ARTIFACT_DIR = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\804d2162-904e-4d53-a4d6-31fe80de76a4"
html_path = os.path.join(ARTIFACT_DIR, "Quantux_Reemplazo_N1_Vistas_Oficiales.html").replace("\\", "/")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,920")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
try:
    driver.get(f"file:///{html_path}")
    time.sleep(1.2)
    
    # 1. View 1: Árbol de Consultas & Triage Guiado
    driver.execute_script("switchView('view1');")
    time.sleep(0.5)
    shot1 = os.path.join(ARTIFACT_DIR, "mockup_quantux_arbol_consultas_triage.png")
    driver.save_screenshot(shot1)
    print("Shot 1 saved:", shot1)
    
    # 2. View 2: Formulario de Solicitud (Revisión & Telemetría)
    driver.execute_script("switchView('view2');")
    time.sleep(0.5)
    shot2 = os.path.join(ARTIFACT_DIR, "mockup_quantux_formulario_solicitud_telemetria.png")
    driver.save_screenshot(shot2)
    print("Shot 2 saved:", shot2)

    # 3. View 3: Solicitud Auto-Resuelta por IA (FCR Zero-Touch)
    driver.execute_script("switchView('view3');")
    time.sleep(0.5)
    shot3 = os.path.join(ARTIFACT_DIR, "mockup_quantux_ticket_autoresuelto_fcr.png")
    driver.save_screenshot(shot3)
    print("Shot 3 saved:", shot3)

    # 4. View 4: Solicitud Escalada Directamente a Nivel 2
    driver.execute_script("switchView('view4');")
    time.sleep(0.5)
    shot4 = os.path.join(ARTIFACT_DIR, "mockup_quantux_ticket_escalado_nivel2.png")
    driver.save_screenshot(shot4)
    print("Shot 4 saved:", shot4)

finally:
    driver.quit()
