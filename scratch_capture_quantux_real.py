import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ARTIFACT_DIR = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\804d2162-904e-4d53-a4d6-31fe80de76a4"
html_path = os.path.join(ARTIFACT_DIR, "Propuesta_Soporte_Inteligente_OSDE_Quantux_Real.html").replace("\\", "/")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1260,860")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
try:
    driver.get(f"file:///{html_path}")
    time.sleep(1.2)
    
    # 1. Fase 1: Antes
    shot1 = os.path.join(ARTIFACT_DIR, "mockup_quantux_fase1_antes_sm.png")
    driver.save_screenshot(shot1)
    print("Shot 1 saved:", shot1)
    
    # 2. Fase 2: Durante (Bypass N2)
    driver.execute_script("renderPhase('fase2');")
    time.sleep(0.5)
    shot2 = os.path.join(ARTIFACT_DIR, "mockup_quantux_fase2_durante_bypass_n2.png")
    driver.save_screenshot(shot2)
    print("Shot 2 saved:", shot2)

    # 3. Fase 3: Después (Contingencia)
    driver.execute_script("renderPhase('fase3');")
    time.sleep(0.5)
    shot3 = os.path.join(ARTIFACT_DIR, "mockup_quantux_fase3_despues_contingencia.png")
    driver.save_screenshot(shot3)
    print("Shot 3 saved:", shot3)

finally:
    driver.quit()
