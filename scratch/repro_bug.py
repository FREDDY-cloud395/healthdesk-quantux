import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set utf-8 output encoding for windows console
sys.stdout.reconfigure(encoding='utf-8')

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1920,1080")
opts.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(options=opts)
try:
    driver.get("http://127.0.0.1:8000/cockpit")
    time.sleep(3) # Wait for startup
    
    # Click on "Mesa de Ayuda" nav tab
    driver.execute_script("""
        const tab = document.querySelector('.nav-hub-tab[data-view="tickets"]');
        if (tab) tab.click();
    """)
    time.sleep(2)
    
    # Check browser console logs
    logs = driver.get_log('browser')
    print("=== BROWSER LOGS ===")
    for l in logs:
        print(l)
    
    # Check AppState and DOM contents
    res = driver.execute_script("""
        return {
            currentView: AppState.currentView,
            selectedTicket: AppState.selectedTicket ? AppState.selectedTicket.id : null,
            detailHtmlLen: document.getElementById('ticket-detail-container').innerHTML.length,
            actionsHtmlLen: document.getElementById('ticket-actions-container').innerHTML.length,
            ticketCardsCount: document.querySelectorAll('.ticket-card-item').length
        };
    """)
    print("=== DOM INSPECTION ===")
    print(res)
    
    out_dir = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\dd64bbe1-4be7-4c38-a377-1457509582e3"
    screenshot_path = os.path.join(out_dir, "repro_user_empty_tickets_FIXED.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")
finally:
    driver.quit()
