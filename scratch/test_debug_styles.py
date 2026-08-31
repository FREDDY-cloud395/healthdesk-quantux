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
    time.sleep(2)
    res = driver.execute_script("""
        return {
            innerWidth: window.innerWidth,
            clientWidth: document.documentElement.clientWidth,
            outerWidth: window.outerWidth,
            mediaQueryMatches: window.matchMedia('(max-width: 768px)').matches
        };
    """)
    print("Window metrics:", res)
    
    driver.execute_script("switchView('tickets');")
    time.sleep(0.5)
    driver.execute_script("switchMobileCockpitTab('col-detail');")
    time.sleep(0.5)
    
    classes = driver.execute_script("""
        return {
            col_list: document.getElementById('col-list').className,
            col_detail: document.getElementById('col-detail').className,
            col_actions: document.getElementById('col-actions').className,
            display_list: window.getComputedStyle(document.getElementById('col-list')).display,
            display_detail: window.getComputedStyle(document.getElementById('col-detail')).display,
            detail_children: document.getElementById('ticket-detail-container').innerHTML.length
        };
    """)
    print("Classes & Computed Styles:", classes)
finally:
    driver.quit()
