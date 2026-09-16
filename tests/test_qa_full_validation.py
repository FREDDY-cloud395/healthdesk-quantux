"""
Suite de Pruebas QA Automatizada E2E con Selenium
HealthDesk Quantux — Validación de Funcionalidades del MVP
"""
import time
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:8000"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Habilitar logging de navegador para capturar errores de JS
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    return driver

def run_qa_suite():
    driver = get_driver()
    passed_tests = []
    failed_tests = []

    def assert_test(name, condition, details=""):
        if condition:
            print(f"  [PASS] {name} {details}")
            passed_tests.append(name)
        else:
            print(f"  [FAIL] {name} - {details}")
            failed_tests.append((name, details))

    try:
        print("\n=======================================================")
        print(" INICIANDO SUITE QA AUTOMATIZADA E2E - HEALTHDESK")
        print("=======================================================\n")

        # -------------------------------------------------------------
        # TEST 1: Carga de página y estado de conexión API
        # -------------------------------------------------------------
        print("▶ Test 1: Conectividad y Carga Inicial...")
        driver.get(f"{BASE_URL}/")
        time.sleep(2)
        
        # Verificar título y API status
        title = driver.title
        assert_test("Título de Página", "HealthDesk" in title or "Quantux" in title, f"Título: {title}")
        
        api_status = driver.find_element(By.ID, "api-status-text").text
        assert_test("Conexión API Online", "Online" in api_status, f"Texto API: {api_status}")

        # -------------------------------------------------------------
        # TEST 2: Tablero de Control Operativo (Punto 1 de Paula)
        # -------------------------------------------------------------
        print("\n▶ Test 2: Tablero de Control Operativo...")
        driver.execute_script("switchView('dashboard');")
        time.sleep(1.5)
        
        kpi_open = driver.find_element(By.ID, "kpi-op-open").text.strip()
        kpi_crit = driver.find_element(By.ID, "kpi-op-critical").text.strip()
        kpi_exp = driver.find_element(By.ID, "kpi-op-expiring").text.strip()
        kpi_over = driver.find_element(By.ID, "kpi-op-overdue").text.strip()
        
        assert_test("4 KPIs Operativos en Dashboard", 
                    all(x.isdigit() for x in [kpi_open, kpi_crit, kpi_exp, kpi_over]),
                    f"Abiertos: {kpi_open}, Críticos: {kpi_crit}, Por Vencer: {kpi_exp}, Vencidos: {kpi_over}")

        # Selector de institución
        inst_select_elem = driver.find_element(By.ID, "dash-filter-inst")
        driver.execute_script("arguments[0].scrollIntoView(true);", inst_select_elem)
        time.sleep(0.5)
        inst_select = Select(inst_select_elem)
        inst_select.select_by_value("OSDE")
        time.sleep(1.5)
        
        btn_refresh = driver.find_element(By.ID, "btn-refresh-dash")
        btn_refresh.click()
        time.sleep(1)
        toast = driver.find_elements(By.CLASS_NAME, "toast")
        assert_test("Refresco de Datos en Dashboard", len(toast) > 0, "Toast visible")

        inst_select.select_by_value("")
        time.sleep(1)

        # -------------------------------------------------------------
        # TEST 3: Bandeja de Tickets, Píldoras y 8 Columnas (Punto 5 de Paula)
        # -------------------------------------------------------------
        print("\n▶ Test 3: Bandeja de Tickets y Filtros Rápidos...")
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='tickets']").click()
        time.sleep(1)
        
        # Verificar píldoras de filtros rápidos
        qf_all = driver.find_element(By.ID, "qf-btn-all")
        qf_mine = driver.find_element(By.ID, "qf-btn-mine")
        qf_unassigned = driver.find_element(By.ID, "qf-btn-unassigned")
        qf_crit = driver.find_element(By.ID, "qf-btn-critical")
        assert_test("Píldoras de Filtros Rápidos Disponibles", 
                    all(btn is not None for btn in [qf_all, qf_mine, qf_unassigned, qf_crit]))

        # Verificar filas en la tabla de 8 columnas
        rows = driver.find_elements(By.CSS_SELECTOR, "#ticket-table-body tr")
        assert_test("Tabla de Tickets con Datos", len(rows) > 0, f"Total filas: {len(rows)}")

        # -------------------------------------------------------------
        # TEST 4: Botón "+ Nuevo ticket" y Modal con Dropzone y SLA (Puntos 2, 3, 4)
        # -------------------------------------------------------------
        print("\n▶ Test 4: Modal Crear Ticket con Dropzone y Cálculo de Prioridad...")
        btn_new_ticket = driver.find_element(By.ID, "btn-open-modal")
        btn_new_ticket.click()
        time.sleep(1)

        modal = driver.find_element(By.ID, "modal-ticket")
        assert_test("Apertura Modal '+ Nuevo ticket'", "active" in modal.get_attribute("class"))

        # Paso 1: Seleccionar institución
        inst_select = Select(driver.find_element(By.ID, "modal-institution"))
        inst_select.select_by_value("OSDE")

        # Paso 3: Probar tarjetas de cálculo dinámico
        driver.find_element(By.ID, "step-node-3").click()
        time.sleep(0.5)

        prio_badge = driver.find_element(By.ID, "modal-calculated-priority")
        
        # Probar Crítico x Crítico -> P1
        driver.find_element(By.ID, "impact-card-critico").click()
        driver.find_element(By.ID, "urgency-card-critico").click()
        time.sleep(0.5)
        prio_text_p1 = prio_badge.text
        assert_test("Cálculo Dinámico P1 (Crítico x Crítico con SLA 2h)", "P1" in prio_text_p1, f"Badge: {prio_text_p1}")

        # Probar Bajo x Bajo -> P4
        driver.find_element(By.ID, "impact-card-bajo").click()
        driver.find_element(By.ID, "urgency-card-bajo").click()
        time.sleep(0.5)
        prio_text_p4 = prio_badge.text
        assert_test("Cálculo Dinámico P4 (Bajo x Bajo)", "P4" in prio_text_p4, f"Badge: {prio_text_p4}")

        # Paso 4: Descripción y Dropzone
        driver.find_element(By.ID, "step-node-4").click()
        time.sleep(0.5)

        dropzone = driver.find_element(By.ID, "ticket-attachment-dropzone")
        assert_test("Dropzone de Arrastrar/Subir Archivos", dropzone is not None)

        driver.find_element(By.ID, "modal-title").send_keys("Test QA Selenium - Desafío HealthDesk")
        driver.find_element(By.ID, "modal-description").send_keys("Falla de prescripción médica generada automáticamente en suite QA.")
        
        driver.find_element(By.ID, "btn-submit-ticket").click()
        time.sleep(2)

        modal_after = driver.find_element(By.ID, "modal-ticket")
        assert_test("Cierre de Modal tras Crear Ticket", "active" not in modal_after.get_attribute("class"))

        # -------------------------------------------------------------
        # TEST 5: Ficha del Ticket en 2 Columnas y Dual-Mode Reply (Puntos 7, 8)
        # -------------------------------------------------------------
        print("\n▶ Test 5: Ficha del Ticket Workspace y Respuesta Dual-Mode...")
        ws_modal = driver.find_element(By.ID, "modal-agent-workspace")
        if "active" not in ws_modal.get_attribute("class"):
            first_row_btn = driver.find_elements(By.CSS_SELECTOR, "#ticket-table-body tr button")[0]
            first_row_btn.click()
            time.sleep(1.5)
            ws_modal = driver.find_element(By.ID, "modal-agent-workspace")

        assert_test("Apertura Ficha del Ticket (Workspace)", "active" in ws_modal.get_attribute("class"))

        # Probar conmutación de pestañas de respuesta (Público vs Nota Interna)
        btn_reply_public = driver.find_element(By.ID, "btn-reply-mode-public")
        btn_reply_internal = driver.find_element(By.ID, "btn-reply-mode-internal")
        
        btn_reply_internal.click()
        time.sleep(0.5)
        assert_test("Selector Modo Nota Interna 🔒", "active" in btn_reply_internal.get_attribute("class"))

        # Escribir nota interna
        reply_textarea = driver.find_element(By.ID, "ws-reply-textarea")
        reply_textarea.send_keys("Nota técnica interna automatizada QA.")
        driver.find_element(By.ID, "ws-btn-send-reply").click()
        time.sleep(1.5)

        timeline_text = driver.find_element(By.ID, "ws-timeline-stream").text
        assert_test("Registro de Nota Interna en Línea de Tiempo", "Nota técnica interna automatizada QA" in timeline_text)

        # Cerrar workspace
        driver.execute_script("closeAgentWorkspace();")
        time.sleep(1)

        # -------------------------------------------------------------
        # TEST 6: Directorio de Usuarios y Alta
        # -------------------------------------------------------------
        print("\n▶ Test 6: Directorio de Usuarios y Alta...")
        driver.execute_script("switchView('users');")
        time.sleep(1)

        users_table = driver.find_element(By.ID, "tbody-users-directory")
        users_rows = users_table.find_elements(By.TAG_NAME, "tr")
        assert_test("Listado de Usuarios", len(users_rows) > 0, f"{len(users_rows)} usuarios registrados")

        # Probar Alta de Usuario
        driver.find_element(By.ID, "btn-open-user-modal").click()
        time.sleep(1)
        user_modal = driver.find_element(By.ID, "modal-create-user")
        assert_test("Apertura Modal Usuario", "active" in user_modal.get_attribute("class"))

        timestamp_user = int(time.time())
        driver.find_element(By.ID, "new-user-fullname").send_keys(f"Usuario QA {timestamp_user}")
        driver.find_element(By.ID, "new-user-username").send_keys(f"qa_user_{timestamp_user}")
        Select(driver.find_element(By.ID, "new-user-role")).select_by_value("SOPORTE")
        driver.find_element(By.ID, "new-user-email").send_keys(f"qa_{timestamp_user}@quantux.com")
        Select(driver.find_element(By.ID, "new-user-institution")).select_by_value("OSDE")
        
        driver.find_element(By.CSS_SELECTOR, "#form-create-user button[type='submit']").click()
        time.sleep(2)

        users_table_updated = driver.find_element(By.ID, "tbody-users-directory").text
        assert_test("Creación y Persistencia de Usuario", f"qa_user_{timestamp_user}" in users_table_updated)

        # -------------------------------------------------------------
        # TEST 7: Base de Conocimiento y Catálogos Clínicos
        # -------------------------------------------------------------
        print("\n▶ Test 7: Base de Conocimiento y Clientes/Plataformas...")
        driver.execute_script("switchView('articles');")
        time.sleep(1)
        articles_text = driver.find_element(By.ID, "view-articles").text
        assert_test("Base de Conocimiento Activa", "Historia Clínica Electrónica" in articles_text or "Protocolo" in articles_text)

        driver.execute_script("switchView('platforms');")
        time.sleep(1)
        plat_grid = driver.find_element(By.ID, "view-platforms").text
        assert_test("Clientes & Plataformas Clínicas", "Receta Electrónica" in plat_grid or "OSDE" in plat_grid or "Swiss Medical" in plat_grid)

        # -------------------------------------------------------------
        # TEST 8: Configuración y Respaldos CSV
        # -------------------------------------------------------------
        print("\n▶ Test 8: Configuración y Exportaciones CSV...")
        driver.execute_script("switchView('config');")
        time.sleep(1)
        config_view = driver.find_element(By.ID, "view-config").text
        assert_test("Módulo Configuración y SLAs", "Configuración Operativa" in config_view or "ITIL" in config_view)
        
        # Verificar que los enlaces de descarga directa son válidos
        csv_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/api/v1/tickets/export/csv')]")
        assert_test("Enlace de Respaldo CSV de Base de Tickets", len(csv_links) > 0)
        
        audit_csv_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/api/v1/tickets/audit/export/csv')]")
        assert_test("Enlace de Respaldo CSV de Auditoría", len(audit_csv_links) > 0)

        # -------------------------------------------------------------
        # TEST 9: Inspección de Logs de Consola del Navegador
        # -------------------------------------------------------------
        print("\n▶ Test 9: Inspección de Consola JS...")
        browser_logs = driver.get_log('browser')
        severe_errors = [log for log in browser_logs if log['level'] == 'SEVERE']
        
        # Filtrar posibles ruidos no críticos como favicon
        real_errors = [log for log in severe_errors if 'favicon' not in log['message'].lower()]
        assert_test("Cero Errores SEVERE en Consola JavaScript", len(real_errors) == 0, f"Errores encontrados: {real_errors}")

        # -------------------------------------------------------------
        # RESUMEN DE RESULTADOS
        # -------------------------------------------------------------
        print("\n=======================================================")
        print(f" RESUMEN QA: {len(passed_tests)} APROBADOS, {len(failed_tests)} FALLIDOS")
        print("=======================================================")

        if failed_tests:
            print("\n❌ FALLOS:")
            for name, err in failed_tests:
                print(f"  - {name}: {err}")
            return False
        else:
            print("\n✅ TODAS LAS PRUEBAS QA PASARON AL 100% DE FORMA EXITOSA.")
            return True

    finally:
        driver.quit()

if __name__ == "__main__":
    success = run_qa_suite()
    sys.exit(0 if success else 1)
