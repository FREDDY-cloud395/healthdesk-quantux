from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
try:
    print("Navigating to http://127.0.0.1:8000/ ...")
    driver.get("http://127.0.0.1:8000/")
    time.sleep(3)
    
    print("Logging in as mgomez (Dr. Martín Gómez)...")
    driver.execute_script("loginAsUser('mgomez', 'quantux123')")
    time.sleep(2)
    
    print("\n--- FINDING AND CLICKING AGENDAR VIDEOLLAMADA BUTTON ---")
    buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Agendar Videollamada')]")
    if not buttons:
        print("Error: Could not find 'Agendar Videollamada' button!")
    else:
        btn = buttons[0]
        print(f"Button found! Display style: {btn.value_of_css_property('display')}")
        # Let's check modal display before click
        modal = driver.find_element(By.ID, "modal-schedule-meet")
        print(f"Modal display style BEFORE click: {modal.value_of_css_property('display')}")
        
        # Click the button
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
        
        # Check modal display after click
        print(f"Modal display style AFTER click: {modal.value_of_css_property('display')}")
        if modal.value_of_css_property('display') == 'flex':
            print("SUCCESS! The 'Agendar Videollamada' modal is visible and display is flex!")
        else:
            print("FAIL: Modal display style is still not flex!")

except Exception as e:
    print(f"An error occurred during verification: {e}")
finally:
    driver.quit()
