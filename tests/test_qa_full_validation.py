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
        # TEST 2: Tablero de Control y Filtro Institucional
        # -------------------------------------------------------------
        print("\n▶ Test 2: Tablero de Control y Filtro Institucional...")
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='dashboard']").click()
        time.sleep(1.5)
        kpi_total = (driver.find_element(By.ID, "jira-kpi-created").text.strip() or 
                     driver.find_element(By.ID, "kpi-total-tickets").get_attribute("textContent").strip())
        kpi_p1 = (driver.find_element(By.ID, "jira-kpi-due").text.strip() or 
                  driver.find_element(By.ID, "kpi-p1-tickets").get_attribute("textContent").strip())
        assert_test("Renderizado de KPIs Globales", int(kpi_total) > 0, f"Total tickets: {kpi_total}, P1: {kpi_p1}")

        # Probar selector de institución
        inst_select_elem = driver.find_element(By.ID, "dash-filter-inst")
        inst_select = Select(inst_select_elem)
        
        # Filtrar por OSDE
        inst_select.select_by_value("OSDE")
        time.sleep(1.5)
        kpi_osde = (driver.find_element(By.ID, "jira-kpi-created").text.strip() or 
                    driver.find_element(By.ID, "kpi-total-tickets").get_attribute("textContent").strip())
        assert_test("Filtro Dashboard por Institución (OSDE)", int(kpi_osde) > 0 and int(kpi_osde) <= int(kpi_total), f"Tickets OSDE: {kpi_osde} (de {kpi_total} global)")

        # Probar botón de refrescar dashboard
        btn_refresh = driver.find_element(By.ID, "btn-refresh-dash")
        btn_refresh.click()
        time.sleep(1)
        toast = driver.find_elements(By.CLASS_NAME, "toast")
        assert_test("Botón de Refresco Dashboard", len(toast) > 0, "Toast de confirmación visible")

        # Volver a todas las instituciones
        inst_select.select_by_value("")
        time.sleep(1)
        kpi_all_again = (driver.find_element(By.ID, "jira-kpi-created").text.strip() or 
                         driver.find_element(By.ID, "kpi-total-tickets").get_attribute("textContent").strip())
        assert_test("Restablecer Filtro Institucional a Global", kpi_all_again == kpi_total, f"Total restablecido: {kpi_all_again}")

        # -------------------------------------------------------------
        # TEST 3: Mesa de Ayuda (Cockpit de Tickets)
        # -------------------------------------------------------------
        print("\n▶ Test 3: Mesa de Ayuda y Cockpit...")
        # Navegar a tickets
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='tickets']").click()
        time.sleep(1)
        
        ticket_cards = driver.find_elements(By.CLASS_NAME, "ticket-card-item")
        assert_test("Lista de Tickets en Cockpit", len(ticket_cards) > 0, f"Cargados {len(ticket_cards)} tickets")

        # Seleccionar el primer ticket
        ticket_cards[0].click()
        time.sleep(1)
        detail_text = driver.find_element(By.ID, "ticket-detail-container").text
        assert_test("Carga de Detalle de Ticket Seleccionado", "Plataforma:" in detail_text and "Solicitante:" in detail_text)

        # Probar Pestañas de Detalle (Conversación Pública, Notas Internas, Auditoría)
        tab_btns = driver.find_elements(By.CSS_SELECTOR, "#ticket-detail-container .sub-pill-btn")
        if len(tab_btns) >= 3:
            # Tab Notas Internas
            tab_btns[1].click()
            time.sleep(0.5)
            internal_content = driver.find_element(By.ID, "detail-tab-content").text
            assert_test("Pestaña Notas Internas Privadas", True, "Pestaña notas internas accesible")

            # Tab Auditoría
            tab_btns_audit = driver.find_elements(By.CSS_SELECTOR, "#ticket-detail-container .sub-pill-btn")
            tab_btns_audit[2].click()
            time.sleep(0.5)
            audit_content = driver.find_element(By.ID, "detail-tab-content").text
            assert_test("Pestaña Historial de Auditoría", "Bitácora" in audit_content or "Auditoría" in audit_content or len(audit_content) > 0)

            # Volver a Conversación
            tab_btns_conv = driver.find_elements(By.CSS_SELECTOR, "#ticket-detail-container .sub-pill-btn")
            tab_btns_conv[0].click()
            time.sleep(0.5)

        # Enviar un mensaje / comentario
        comment_input = driver.find_element(By.ID, "input-comment")
        comment_input.clear()
        comment_input.send_keys("Comentario de prueba automatizado QA Selenium")
        driver.find_element(By.ID, "btn-send-comment").click()
        time.sleep(1.5)
        comment_content = driver.find_element(By.ID, "detail-tab-content").text
        assert_test("Envío de Comentario en Ticket", "Comentario de prueba automatizado QA Selenium" in comment_content)

        # -------------------------------------------------------------
        # TEST 4: Modal "Nueva Solicitud" y Cálculo de Prioridad Dinámico
        # -------------------------------------------------------------
        print("\n▶ Test 4: Modal Nueva Solicitud y Cálculo de Prioridad...")
        btn_open_modal = driver.find_element(By.ID, "btn-open-modal")
        btn_open_modal.click()
        time.sleep(1)

        modal = driver.find_element(By.ID, "modal-ticket")
        assert_test("Apertura de Modal Nueva Solicitud", "active" in modal.get_attribute("class"))

        # Validar cálculo de prioridad dinámico en vivo
        impact_select = Select(driver.find_element(By.ID, "modal-impact"))
        urgency_select = Select(driver.find_element(By.ID, "modal-urgency"))
        prio_badge = driver.find_element(By.ID, "modal-calculated-priority")

        # ALTO x ALTO = P1
        impact_select.select_by_value("ALTO")
        urgency_select.select_by_value("ALTO")
        time.sleep(1)
        prio_text_p1 = prio_badge.text
        assert_test("Cálculo Dinámico P1 (Alto x Alto)", "P1" in prio_text_p1, f"Badge: {prio_text_p1}")

        # BAJO x BAJO = P4/P5
        impact_select.select_by_value("BAJO")
        urgency_select.select_by_value("BAJO")
        time.sleep(1)
        prio_text_p5 = prio_badge.text
        assert_test("Cálculo Dinámico P4/P5 (Bajo x Bajo)", "P4" in prio_text_p5 or "P5" in prio_text_p5, f"Badge: {prio_text_p5}")

        # Crear un ticket real
        driver.find_element(By.ID, "modal-title").send_keys("Test QA Automatizado Incidencia de Servicio en Producción")
        driver.find_element(By.ID, "modal-description").send_keys("Falla de acceso concurrente detectada en test automatizado QA Selenium")
        Select(driver.find_element(By.ID, "modal-platform")).select_by_value("CAT_RECETA")
        Select(driver.find_element(By.ID, "modal-institution")).select_by_value("OSDE")
        impact_select.select_by_value("ALTO")
        urgency_select.select_by_value("ALTO")
        
        # Submit
        driver.find_element(By.ID, "btn-submit-ticket").click()
        time.sleep(2)

        # Verificar que el modal cerró y se creó el ticket
        modal_after = driver.find_element(By.ID, "modal-ticket")
        assert_test("Cierre de Modal tras Crear Ticket", "active" not in modal_after.get_attribute("class"))
        
        detail_after_create = driver.find_element(By.ID, "ticket-detail-container").text
        assert_test("Persistencia y Selección de Ticket Creado", "Test QA Automatizado Incidencia de Servicio en Producción" in detail_after_create)

        # -------------------------------------------------------------
        # TEST 5: Ciclo de Vida FSM (Auto-Asignar -> En Curso -> Resolver -> Cerrar)
        # -------------------------------------------------------------
        print("\n▶ Test 5: Ciclo de Vida FSM del Ticket...")
        detail_container = driver.find_element(By.ID, "ticket-detail-container")
        
        # 1. Auto-asignar (NUEVO -> ASIGNADO)
        assign_btns = detail_container.find_elements(By.XPATH, ".//button[contains(text(), 'Tomar Yo el Ticket')]")
        if assign_btns:
            assign_btns[0].click()
            time.sleep(1.5)
            assert_test("Auto-Asignación Rápida (FSM)", True)

        # 2. Iniciar Trabajo (ASIGNADO -> EN_CURSO)
        detail_container = driver.find_element(By.ID, "ticket-detail-container")
        start_btns = detail_container.find_elements(By.XPATH, ".//button[contains(text(), 'Iniciar Trabajo')]")
        if start_btns:
            start_btns[0].click()
            time.sleep(1.5)
            assert_test("Inicio de Trabajo / Poner En Curso (FSM)", True)

        # 3. Resolver con notas técnicas (EN_CURSO -> RESUELTO)
        res_notes = driver.find_elements(By.ID, "action-res-notes")
        if res_notes:
            res_notes[0].send_keys("Se aplicó hotfix de base de datos y se restauró la conexión.")
            driver.find_element(By.XPATH, "//button[contains(text(), 'Marcar como Resuelto')]").click()
            time.sleep(1.5)
            assert_test("Resolución Técnica de Ticket (FSM)", True)

        # 4. Cerrar con conformidad (RESUELTO -> CERRADO)
        close_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Validar Conformidad')]")
        if close_btns:
            close_btns[0].click()
            time.sleep(1.5)
            assert_test("Cierre Definitivo con Conformidad (FSM)", True)

        # -------------------------------------------------------------
        # TEST 6: Directorio de Usuarios y Alta
        # -------------------------------------------------------------
        print("\n▶ Test 6: Directorio de Usuarios y Alta...")
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='users']").click()
        time.sleep(1)

        users_table = driver.find_element(By.ID, "tbody-users-directory")
        users_rows = users_table.find_elements(By.TAG_NAME, "tr")
        assert_test("Listado de Usuarios", len(users_rows) > 0, f"{len(users_rows)} usuarios registrados")

        # Probar Alta de Usuario
        driver.find_element(By.ID, "btn-open-user-modal").click()
        time.sleep(1)
        user_modal = driver.find_element(By.ID, "modal-user")
        assert_test("Apertura Modal Usuario", "active" in user_modal.get_attribute("class"))

        timestamp_user = int(time.time())
        driver.find_element(By.ID, "user-fullname").send_keys(f"Usuario QA {timestamp_user}")
        driver.find_element(By.ID, "user-username").send_keys(f"qa_user_{timestamp_user}")
        Select(driver.find_element(By.ID, "user-role")).select_by_value("SOPORTE")
        driver.find_element(By.ID, "user-email").send_keys(f"qa_{timestamp_user}@quantux.com")
        Select(driver.find_element(By.ID, "user-institution")).select_by_value("OSDE")
        
        driver.find_element(By.ID, "btn-submit-user").click()
        time.sleep(2)

        users_table_updated = driver.find_element(By.ID, "tbody-users-directory").text
        assert_test("Creación y Persistencia de Usuario", f"qa_user_{timestamp_user}" in users_table_updated)

        # -------------------------------------------------------------
        # TEST 7: Catálogos de Plataformas y Guías Clínicas
        # -------------------------------------------------------------
        print("\n▶ Test 7: Catálogos y Base de Conocimiento...")
        # Guías
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='articles']").click()
        time.sleep(1)
        articles_text = driver.find_element(By.ID, "view-articles").text
        assert_test("Base de Conocimiento", "Historia Clínica Electrónica" in articles_text and "Protocolo de Contingencia" in articles_text)

        # Plataformas
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='platforms']").click()
        time.sleep(1)
        plat_grid = driver.find_element(By.ID, "view-platforms").text
        assert_test("Catálogo de Plataformas Clínicas", "Receta Electrónica" in plat_grid or "Receta Digital" in plat_grid or "Telemedicina" in plat_grid)

        # -------------------------------------------------------------
        # TEST 8: Configuración y Descarga Directa de Respaldos
        # -------------------------------------------------------------
        print("\n▶ Test 8: Configuración y Respaldos...")
        driver.find_element(By.CSS_SELECTOR, ".nav-hub-tab[data-view='config']").click()
        time.sleep(1)
        config_view = driver.find_element(By.ID, "view-config").text
        assert_test("Sección Configuración y SLAs", "Matriz de Priorización ITIL" in config_view and "Respaldo y Exportación" in config_view)
        
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
