import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=1920,1080')
opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(options=opts)

try:
    driver.get('http://127.0.0.1:8000/cockpit')
    time.sleep(2)
    driver.execute_script("switchView('config');")
    time.sleep(1)
    driver.save_screenshot(r'C:\Users\FERO_ADM\.gemini\antigravity\brain\dd64bbe1-4be7-4c38-a377-1457509582e3\config_view_fixed.png')
    print('CONFIG SCREENSHOT CAPTURED!')
finally:
    driver.quit()
