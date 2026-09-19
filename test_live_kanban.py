import time
import sys
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
    
    # Click on Kanban tab
    kanban_tab = driver.find_element(By.ID, 'tab-kanban')
    kanban_tab.click()
    time.sleep(2)
    
    driver.save_screenshot('screenshot_kanban_rendered.png')
    
    col_plan = driver.find_element(By.ID, 'kanban-col-planificada')
    col_dev = driver.find_element(By.ID, 'kanban-col-desarrollo')
    col_stg = driver.find_element(By.ID, 'kanban-col-staging')
    col_dep = driver.find_element(By.ID, 'kanban-col-desplegada')
    title = driver.find_element(By.ID, 'top-view-title-text').text
    
    print(f"Top Title: {title}")
    print(f"Planificada HTML length: {len(col_plan.get_attribute('innerHTML'))}")
    print(f"Desarrollo HTML length: {len(col_dev.get_attribute('innerHTML'))}")
    print(f"Staging HTML length: {len(col_stg.get_attribute('innerHTML'))}")
    print(f"Desplegada HTML length: {len(col_dep.get_attribute('innerHTML'))}")
    print("SUCCESS: Tablero Kanban N3 rendered with all 4 columns!")
finally:
    driver.quit()
