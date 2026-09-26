import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

out_dir = r'C:\Users\FERO_ADM\.gemini\antigravity\scratch\quantux-v4-dev\product_screenshots'
os.makedirs(out_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1400,900')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--force-device-scale-factor=1.25')

driver = webdriver.Chrome(options=chrome_options)

try:
    url = r'file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/frontend/reemplazo-n1.html'
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(1)

    # Hide the dev screen selector bar for pure native look
    driver.execute_script("const el = document.getElementById('dev-screen-selector'); if(el) el.style.display = 'none';")

    screens = [
        (1, 'captura_figura_1_portal_centrado.png', 'Figura 1: Portal Centrado con Árbol de Decisión Técnico-Operativo'),
        (2, 'captura_figura_2_chat_stream.png', 'Figura 2: Chat Stream Resolutivo con Protocolo Oficial (Pág. 23)'),
        (3, 'captura_figura_3_modal_crear_solicitud.png', 'Figura 3: Modal Nativo Crear Solicitud con Telemetría Pre-cargada'),
        (4, 'captura_figura_4_historial_mis_solicitudes.png', 'Figura 4: Historial de Mis Solicitudes con Ciclo de Vida ITIL 4'),
        (5, 'captura_figura_5_detalle_n2_mim.png', 'Figura 5: Detalle N2 con Cartel de Incidencia Mayor, Padre-Hijo y Acciones de Estado'),
        (6, 'captura_figura_6_mando_lider_rescate.png', 'Figura 6: Mando Unificado del Líder de Soporte (Rescate CSAT)'),
        (7, 'captura_figura_7_configuracion_itil_slas.png', 'Figura 7: Módulo Colaborativo de Configuración de Tickets y SLAs ITIL 4')
    ]

    for idx, fname, title in screens:
        driver.execute_script(f"selectScreen({idx});")
        time.sleep(0.5)
        out_path = os.path.join(out_dir, fname)
        driver.save_screenshot(out_path)
        print(f"Saved [{idx}] {title} -> {fname}")

finally:
    driver.quit()

print("All 7 product screenshots successfully captured!")
