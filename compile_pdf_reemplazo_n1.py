import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ARTIFACT_DIR = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\804d2162-904e-4d53-a4d6-31fe80de76a4"
html_path = os.path.join(ARTIFACT_DIR, "Documento_Propuesta_Solucion_Reemplazo_N1.html").replace("\\", "/")
pdf_path = os.path.join(ARTIFACT_DIR, "Propuesta_Funcional_Reemplazo_N1_OSDE_Quantux.pdf")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--allow-file-access-from-files")

driver = webdriver.Chrome(options=options)
try:
    driver.get(f"file:///{html_path}")
    time.sleep(2)  # Give time to load web fonts and images

    # Execute Chrome DevTools Protocol to print to PDF
    pdf_params = {
        "landscape": False,
        "displayHeaderFooter": False,
        "printBackground": True,
        "preferCSSPageSize": True,
        "marginTop": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "marginRight": 0
    }
    
    result = driver.execute_cdp_cmd("Page.printToPDF", pdf_params)
    pdf_bytes = base64.b64decode(result["data"])
    
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
        
    print(f"PDF successfully generated: {pdf_path} (Size: {len(pdf_bytes)} bytes)")

finally:
    driver.quit()
