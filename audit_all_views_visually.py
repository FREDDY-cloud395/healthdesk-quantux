import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=chrome_options)
try:
    driver.get('http://127.0.0.1:8005/')
    time.sleep(2)
    
    views = [
        ('tab-dashboard', 'screenshot_view_dashboard.png', 'Tablero de Control'),
        ('tab-tickets', 'screenshot_view_tickets.png', 'Mesa de Ayuda'),
        ('tab-team-leader', 'screenshot_view_team_leader.png', 'Torre de Control'),
        ('tab-kanban', 'screenshot_view_kanban.png', 'Tablero Kanban N3'),
        ('tab-users', 'screenshot_view_users.png', 'Usuarios y Roles'),
        ('tab-platforms', 'screenshot_view_platforms.png', 'Plataformas & Instituciones'),
        ('tab-articles', 'screenshot_view_kb.png', 'Base de Conocimiento'),
        ('tab-config', 'screenshot_view_config.png', 'Configuración'),
    ]
    
    for tab_id, filename, name in views:
        try:
            tab = driver.find_element(By.ID, tab_id)
            tab.click()
            time.sleep(1.2)
            driver.save_screenshot(filename)
            top_title = driver.find_element(By.ID, 'top-view-title-text').text
            print(f"[PASS] Vista '{name}' cargada con éxito. Título en Topbar: '{top_title}'. Screenshot: {filename}")
        except Exception as e:
            print(f"[FAIL] Error en vista '{name}': {e}")
            
    # Also test switching to Solicitante role
    print("\n--- Probando Vista Solicitante (Centro de Asistencia) ---")
    driver.execute_script("setCurrentUser({ id: 9, username: 'solicitante', full_name: 'Dr. Martín Gómez', email: 'martin.gomez@clinica.com', role: 'SOLICITANTE', institution_code: 'OSDE' }); switchView('requester-portal');")
    time.sleep(1.5)
    driver.save_screenshot('screenshot_view_requester_portal.png')
    top_title_req = driver.find_element(By.ID, 'top-view-title-text').text
    print(f"[PASS] Vista Solicitante cargada. Título: '{top_title_req}'. Screenshot: screenshot_view_requester_portal.png")
    
finally:
    driver.quit()
