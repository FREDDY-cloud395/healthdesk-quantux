import os
import sys
import time
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://127.0.0.1:8000/cockpit"
OUT_DIR = r"C:\Users\FERO_ADM\.gemini\antigravity\brain\dd64bbe1-4be7-4c38-a377-1457509582e3"

VIEWPORTS = [
    {"name": "mobile_iphone_se", "width": 375, "height": 667, "is_mobile": True},
    {"name": "mobile_iphone_14", "width": 390, "height": 844, "is_mobile": True},
    {"name": "mobile_pixel_7", "width": 412, "height": 915, "is_mobile": True},
    {"name": "tablet_ipad_portrait", "width": 768, "height": 1024, "is_mobile": False},
    {"name": "tablet_ipad_landscape", "width": 1024, "height": 768, "is_mobile": False},
    {"name": "laptop_1280", "width": 1280, "height": 800, "is_mobile": False},
    {"name": "desktop_1920", "width": 1920, "height": 1080, "is_mobile": False},
]

def create_driver(vp):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    opts.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    w = vp["width"]
    h = vp["height"]
    
    if vp["is_mobile"]:
        mobile_emulation = {
            "deviceMetrics": {
                "width": w,
                "height": h,
                "pixelRatio": 3.0,
                "touch": True
            },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }
        opts.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        opts.add_argument(f"--window-size={w},{h}")
        
    driver = webdriver.Chrome(options=opts)
    if not vp["is_mobile"]:
        driver.set_window_size(w, h)
    return driver

def check_horizontal_overflow(driver):
    script = """
    return (() => {
        const vw = window.innerWidth;
        const bodyScrollWidth = document.body.scrollWidth;
        const htmlScrollWidth = document.documentElement.scrollWidth;
        const overflowing = [];
        
        const elements = document.querySelectorAll('body *');
        for (const el of elements) {
            // Ignore hidden elements, modals when inactive, offscreen sidebar
            if (el.offsetParent === null && !el.classList.contains('active')) continue;
            if (el.classList.contains('app-sidebar') && !el.classList.contains('open')) continue;
            
            // Ignore elements inside intentional scrollable containers
            if (el.closest('.sub-pills-bar') || el.closest('.table-responsive-wrapper')) continue;
            
            const rect = el.getBoundingClientRect();
            // 2px tolerance for subpixel antialiasing/scrollbars
            if (rect.right > vw + 2.0) {
                overflowing.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    right: Math.round(rect.right),
                    vw: vw,
                    diff: Math.round(rect.right - vw)
                });
            }
        }
        return {
            vw: vw,
            bodyScrollWidth: bodyScrollWidth,
            htmlScrollWidth: htmlScrollWidth,
            hasBodyOverflow: bodyScrollWidth > vw + 2.0,
            overflowElements: overflowing.slice(0, 10)
        };
    })();
    """
    return driver.execute_script(script)

def check_browser_console_errors(driver):
    logs = driver.get_log('browser')
    severe = [l for l in logs if l.get('level') in ['SEVERE', 'ERROR']]
    return severe

def run_qa_suite():
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "viewports_tested": len(VIEWPORTS),
        "results": []
    }
    
    print("=" * 80)
    print("SUITE QA INTEGRAL: RESPONSIVE DESIGN + INTEGRIDAD SEMÁNTICA + LOGS DE CONSOLA")
    print("=" * 80)

    all_passed = True

    for vp in VIEWPORTS:
        name = vp["name"]
        w = vp["width"]
        h = vp["height"]
        
        print(f"\n[QA AUDIT] Viewport: {name} ({w}x{h})...")
        driver = create_driver(vp)
        vp_result = {
            "viewport": name,
            "width": w,
            "height": h,
            "views_tested": {},
            "console_errors": [],
            "semantic_checks": {},
            "pass": True
        }
        
        try:
            driver.get(BASE_URL)
            time.sleep(2)
            
            # --- 1. DASHBOARD VIEW ---
            overflow_dash = check_horizontal_overflow(driver)
            screenshot_dash = os.path.join(OUT_DIR, f"qa_screenshot_{name}_dashboard.png")
            driver.save_screenshot(screenshot_dash)
            
            dash_semantic = driver.execute_script("""
                return {
                    kpiTotal: document.getElementById('kpi-total-tickets') ? document.getElementById('kpi-total-tickets').innerText : '',
                    slaRows: document.querySelectorAll('#table-active-sla tbody tr').length,
                    auditRows: document.querySelectorAll('#feed-audit-logs > div').length
                };
            """)
            
            has_dash_overflow_pass = not overflow_dash.get("hasBodyOverflow", False) and len(overflow_dash.get("overflowElements", [])) == 0
            has_dash_semantic_pass = int(dash_semantic.get("kpiTotal", "0") or "0") > 0 and dash_semantic.get("slaRows", 0) > 0
            has_dash_pass = has_dash_overflow_pass and has_dash_semantic_pass
            
            vp_result["views_tested"]["dashboard"] = {
                "overflow": overflow_dash,
                "semantic": dash_semantic,
                "screenshot": screenshot_dash,
                "pass": has_dash_pass
            }
            status_str = "PASS" if has_dash_pass else "FAIL"
            print(f"  [{status_str}] Dashboard: ScrollW={overflow_dash['bodyScrollWidth']}px | KPIs={dash_semantic['kpiTotal']} tkts | SLA Rows={dash_semantic['slaRows']}")
            if not has_dash_pass:
                all_passed = False
                vp_result["pass"] = False

            # --- 2. TICKETS VIEW (MESA DE AYUDA) ---
            driver.execute_script("switchView('tickets');")
            time.sleep(1.2)
            overflow_tickets = check_horizontal_overflow(driver)
            screenshot_tickets = os.path.join(OUT_DIR, f"qa_screenshot_{name}_tickets.png")
            driver.save_screenshot(screenshot_tickets)
            
            tickets_semantic = driver.execute_script("""
                const detailEl = document.getElementById('ticket-detail-container');
                const actionsEl = document.getElementById('ticket-actions-container');
                return {
                    selectedTicketId: AppState.selectedTicket ? AppState.selectedTicket.id : null,
                    cardCount: document.querySelectorAll('.ticket-card-item').length,
                    detailHtmlLen: detailEl ? detailEl.innerHTML.length : 0,
                    detailTextLen: detailEl ? detailEl.innerText.trim().length : 0,
                    actionsHtmlLen: actionsEl ? actionsEl.innerHTML.length : 0,
                    actionsTextLen: actionsEl ? actionsEl.innerText.trim().length : 0,
                    hasCommentInput: !!document.getElementById('input-comment'),
                    hasActionButtons: !!document.querySelector('#ticket-actions-container button')
                };
            """)
            
            has_tickets_overflow_pass = not overflow_tickets.get("hasBodyOverflow", False) and len(overflow_tickets.get("overflowElements", [])) == 0
            # CRITICAL ASSERTION: Detail and Actions containers MUST NOT be empty
            has_tickets_semantic_pass = (
                tickets_semantic.get("selectedTicketId") is not None and
                tickets_semantic.get("cardCount", 0) > 0 and
                tickets_semantic.get("detailHtmlLen", 0) > 500 and
                tickets_semantic.get("detailTextLen", 0) > 50 and
                tickets_semantic.get("actionsHtmlLen", 0) > 200 and
                tickets_semantic.get("hasCommentInput", False)
            )
            has_tickets_pass = has_tickets_overflow_pass and has_tickets_semantic_pass
            
            vp_result["views_tested"]["tickets"] = {
                "overflow": overflow_tickets,
                "semantic": tickets_semantic,
                "screenshot": screenshot_tickets,
                "pass": has_tickets_pass
            }
            status_str = "PASS" if has_tickets_pass else "FAIL"
            print(f"  [{status_str}] Mesa de Ayuda: ScrollW={overflow_tickets['bodyScrollWidth']}px | Selected={tickets_semantic['selectedTicketId']} | Detail HTML={tickets_semantic['detailHtmlLen']}b | Actions HTML={tickets_semantic['actionsHtmlLen']}b")
            if not has_tickets_pass:
                all_passed = False
                vp_result["pass"] = False
                print(f"    [!] Error semántico en Tickets:", tickets_semantic)

            # --- 3. DYNAMIC INTERACTION: Click on a specific ticket card ---
            interaction_res = driver.execute_script("""
                const cards = document.querySelectorAll('.ticket-card-item');
                if (cards.length > 1) {
                    cards[1].click(); // Click 2nd ticket
                    return { clicked: true, targetId: AppState.selectedTicket ? AppState.selectedTicket.id : null };
                }
                return { clicked: false };
            """)
            time.sleep(1)
            
            if vp["is_mobile"]:
                shot_detail = os.path.join(OUT_DIR, f"qa_screenshot_{name}_cockpit_detail.png")
                driver.save_screenshot(shot_detail)
                
                driver.execute_script("switchMobileCockpitTab('col-actions');")
                time.sleep(0.5)
                shot_actions = os.path.join(OUT_DIR, f"qa_screenshot_{name}_cockpit_actions.png")
                driver.save_screenshot(shot_actions)
                
                driver.execute_script("switchMobileCockpitTab('col-list');")
                time.sleep(0.5)

            # --- 4. DRAWER TOGGLE ON MOBILE ---
            if vp["is_mobile"]:
                driver.execute_script("document.getElementById('btn-sidebar-toggle').click();")
                time.sleep(0.5)
                sidebar_open = driver.execute_script("return document.getElementById('app-sidebar').classList.contains('open');")
                shot_drawer = os.path.join(OUT_DIR, f"qa_screenshot_{name}_drawer_open.png")
                driver.save_screenshot(shot_drawer)
                
                driver.execute_script("document.getElementById('btn-sidebar-close').click();")
                time.sleep(0.5)
                sidebar_closed = not driver.execute_script("return document.getElementById('app-sidebar').classList.contains('open');")
                
                drawer_pass = sidebar_open and sidebar_closed
                vp_result["drawer_test"] = {
                    "open_success": sidebar_open,
                    "close_success": sidebar_closed,
                    "pass": drawer_pass
                }
                status_str = "PASS" if drawer_pass else "FAIL"
                print(f"  [{status_str}] Drawer Mobile: Open={sidebar_open}, Close={sidebar_closed}")
                if not drawer_pass:
                    all_passed = False
                    vp_result["pass"] = False

            # --- 5. USERS DIRECTORY VIEW ---
            driver.execute_script("switchView('users');")
            time.sleep(0.5)
            overflow_users = check_horizontal_overflow(driver)
            users_count = driver.execute_script("return document.querySelectorAll('#table-users-directory tbody tr').length;")
            has_users_pass = not overflow_users.get("hasBodyOverflow", False) and users_count > 0
            vp_result["views_tested"]["users"] = {
                "overflow": overflow_users,
                "users_count": users_count,
                "pass": has_users_pass
            }
            status_str = "PASS" if has_users_pass else "FAIL"
            print(f"  [{status_str}] Directorio Usuarios: ScrollW={overflow_users['bodyScrollWidth']}px | Users={users_count}")
            if not has_users_pass:
                all_passed = False
                vp_result["pass"] = False

            # --- 6. PLATFORMS & INSTITUTIONS VIEW ---
            driver.execute_script("switchView('platforms');")
            time.sleep(0.5)
            overflow_plat = check_horizontal_overflow(driver)
            plat_count = driver.execute_script("return document.querySelectorAll('#platforms-grid-cards > div').length;")
            has_plat_pass = not overflow_plat.get("hasBodyOverflow", False) and plat_count > 0
            vp_result["views_tested"]["platforms"] = {
                "overflow": overflow_plat,
                "platforms_count": plat_count,
                "pass": has_plat_pass
            }
            status_str = "PASS" if has_plat_pass else "FAIL"
            print(f"  [{status_str}] Plataformas & Sedes: ScrollW={overflow_plat['bodyScrollWidth']}px | Count={plat_count}")
            if not has_plat_pass:
                all_passed = False
                vp_result["pass"] = False

            # --- 7. CONFIGURACIÓN Y ADMINISTRACIÓN VIEW ---
            driver.execute_script("switchView('config');")
            time.sleep(0.5)
            overflow_cfg = check_horizontal_overflow(driver)
            cfg_semantic = driver.execute_script("""
                return {
                    hasSlaCard: !!document.getElementById('config-sla-card'),
                    hasNotificationsCard: !!document.getElementById('config-notifications-card'),
                    hasAuditCard: !!document.getElementById('config-audit-card'),
                    hasBackupCard: !!document.getElementById('config-backup-card')
                };
            """)
            has_cfg_overflow_pass = not overflow_cfg.get("hasBodyOverflow", False) and len(overflow_cfg.get("overflowElements", [])) == 0
            has_cfg_semantic_pass = cfg_semantic.get("hasSlaCard") and cfg_semantic.get("hasNotificationsCard") and cfg_semantic.get("hasAuditCard") and cfg_semantic.get("hasBackupCard")
            has_cfg_pass = has_cfg_overflow_pass and has_cfg_semantic_pass
            vp_result["views_tested"]["config"] = {
                "overflow": overflow_cfg,
                "semantic": cfg_semantic,
                "pass": has_cfg_pass
            }
            status_str = "PASS" if has_cfg_pass else "FAIL"
            print(f"  [{status_str}] Configuración: ScrollW={overflow_cfg['bodyScrollWidth']}px | 4 Módulos Activos={has_cfg_semantic_pass}")
            if not has_cfg_pass:
                all_passed = False
                vp_result["pass"] = False

            # --- 8. BROWSER CONSOLE ERROR CHECK ---
            console_errors = check_browser_console_errors(driver)
            vp_result["console_errors"] = console_errors
            has_no_console_errors = len(console_errors) == 0
            if not has_no_console_errors:
                all_passed = False
                vp_result["pass"] = False
                print(f"  [FAIL] Console Errors ({len(console_errors)}):")
                for err in console_errors:
                    print(f"    - {err.get('message')}")
            else:
                print(f"  [PASS] Consola JS: 0 errores detectados")

        except Exception as ex:
            print(f"  [ERROR FATAL] en viewport {name}: {ex}")
            vp_result["errors"] = [str(ex)]
            all_passed = False
            vp_result["pass"] = False
        finally:
            driver.quit()
            report["results"].append(vp_result)

    report_path = os.path.join(OUT_DIR, "qa_responsive_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 80)
    final_status = "100% EXITOSA - CERO DESBORDES Y 100% INTEGRIDAD SEMÁNTICA" if all_passed else "ERRORES DETECTADOS"
    print(f"RESULTADO FINAL SUITE QA: {final_status}")
    print(f"Reporte guardado en: {report_path}")
    print("=" * 80)

if __name__ == "__main__":
    run_qa_suite()
