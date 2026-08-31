import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")
opts.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
mobile_emulation = {
    "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0, "touch": True},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
}
opts.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=opts)
try:
    driver.get("http://127.0.0.1:8000/cockpit")
    time.sleep(2.5) # Wait for initial DOM & API loads
    driver.execute_script("switchView('tickets');")
    time.sleep(1)
    
    # Select first ticket and wait for detail rendering
    driver.execute_script("""
        selectTicket(AppState.tickets[0].id, true);
    """)
    time.sleep(1.5)
    
    out_dir = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\dd64bbe1-4be7-4c38-a377-1457509582e3"
    driver.save_screenshot(os.path.join(out_dir, "qa_screenshot_mobile_iphone_14_cockpit_detail.png"))
    
    # Switch to Actions
    driver.execute_script("switchMobileCockpitTab('col-actions');")
    time.sleep(1)
    driver.save_screenshot(os.path.join(out_dir, "qa_screenshot_mobile_iphone_14_cockpit_actions.png"))
    
    # Switch back to List
    driver.execute_script("switchMobileCockpitTab('col-list');")
    time.sleep(1)
    driver.save_screenshot(os.path.join(out_dir, "qa_screenshot_mobile_iphone_14_tickets.png"))
    
    print("Screenshots taken with selected ticket!")
finally:
    driver.quit()
