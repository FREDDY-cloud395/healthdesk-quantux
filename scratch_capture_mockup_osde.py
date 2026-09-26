import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ARTIFACT_DIR = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\804d2162-904e-4d53-a4d6-31fe80de76a4"
html_path = os.path.join(ARTIFACT_DIR, "Propuesta_Soporte_Inteligente_OSDE.html").replace("\\", "/")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,960")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
try:
    driver.get(f"file:///{html_path}")
    time.sleep(1)
    
    # 1. Salud Mental - Fase 1: Antes
    shot1 = os.path.join(ARTIFACT_DIR, "mockup_soporte_osde_sm_fase1_antes.png")
    driver.save_screenshot(shot1)
    print("Shot 1 saved:", shot1)
    
    # 2. Salud Mental - Fase 2: Durante
    driver.execute_script("switchView('durante');")
    time.sleep(0.5)
    shot2 = os.path.join(ARTIFACT_DIR, "mockup_soporte_osde_sm_fase2_durante.png")
    driver.save_screenshot(shot2)
    print("Shot 2 saved:", shot2)

    # 3. Salud Mental - Fase 3: Después
    driver.execute_script("switchView('despues');")
    time.sleep(0.5)
    shot3 = os.path.join(ARTIFACT_DIR, "mockup_soporte_osde_sm_fase3_despues.png")
    driver.save_screenshot(shot3)
    print("Shot 3 saved:", shot3)

    # 4. Matriz Comparativa
    driver.execute_script("switchView('matriz');")
    time.sleep(0.5)
    shot4 = os.path.join(ARTIFACT_DIR, "mockup_soporte_osde_matriz_comparativa.png")
    driver.save_screenshot(shot4)
    print("Shot 4 saved:", shot4)

finally:
    driver.quit()
