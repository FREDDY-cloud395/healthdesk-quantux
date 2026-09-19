# -*- coding: utf-8 -*-
import re

# 1. Actualizar frontend/js/app.js
with open('frontend/js/app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

if "'kanban': {" not in js_content:
    js_content = js_content.replace(
        "'team-leader': {",
        "'kanban': {\n\t\ticon: '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#4338CA\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" style=\"width:17px;height:17px;\"><path d=\"M6 5v11\"></path><path d=\"M12 5v6\"></path><path d=\"M18 5v14\"></path><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\"></rect></svg>',\n\t\ttitle: 'Tablero Kanban N3 • Releases y Despliegues',\n\t\tsub: 'Gestión ágil de versiones, vinculación de tickets N3 y cierre en cascada a producción'\n\t},\n\t'team-leader': {"
    )

if "'kanban': 'Tablero Kanban N3'" not in js_content:
    js_content = js_content.replace(
        "'dashboard': 'Tablero de Control',",
        "'dashboard': 'Tablero de Control',\n\t\t'team-leader': 'Torre de Control',\n\t\t'kanban': 'Tablero Kanban N3',"
    )

with open('frontend/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("[OK] frontend/js/app.js actualizado.")

# 2. Actualizar frontend/index.html
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

kanban_view_html = '''
        <!-- ===================================================================
             VISTA 2.5: TABLERO KANBAN N3 • RELEASES Y CIERRE EN CASCADA
             =================================================================== -->
        <section class="app-view" id="view-kanban">
          <div class="users-board-wrapper" style="padding: 16px 20px;">
            
            <!-- Toolbar Superior Kanban -->
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px 20px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 38px; height: 38px; border-radius: 9px; background: #EEF2FF; border: 1.5px solid #C7D2FE; display: flex; align-items: center; justify-content: center; color: #4338CA; flex-shrink: 0;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 20px; height: 20px;"><path d="M6 5v11"></path><path d="M12 5v6"></path><path d="M18 5v14"></path><rect x="3" y="3" width="18" height="18" rx="2"></rect></svg>
                </div>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <h2 style="margin: 0; font-size: 16px; font-weight: 800; color: #0F172A; font-family: 'Outfit', sans-serif;">Tablero Kanban N3 • Releases & Despliegues</h2>
                    <span style="display: inline-flex; align-items: center; gap: 4px; background: #EEF2FF; color: #4338CA; font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 9999px; border: 1px solid #C7D2FE;">
                      🚀 Cierre en Cascada
                    </span>
                  </div>
                  <p style="margin: 2px 0 0 0; font-size: 12px; color: #64748B;">
                    Vinculación de incidencias complejas N3 a versiones de desarrollo y cierre automático por despliegue a producción.
                  </p>
                </div>
              </div>

              <div style="display: flex; align-items: center; gap: 10px;">
                <button type="button" class="btn-sec" onclick="loadKanbanBoard()" title="Refrescar tablero Kanban" style="display: flex; align-items: center; gap: 6px; background: #FFFFFF; border: 1px solid #CBD5E1; color: #334155; padding: 7px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
                  <span>Refrescar</span>
                </button>
                <button type="button" onclick="openNewReleaseModal()" style="display: flex; align-items: center; gap: 6px; background: #4338CA; color: #FFFFFF; border: none; padding: 8px 16px; border-radius: 8px; font-size: 12.5px; font-weight: 700; cursor: pointer; box-shadow: 0 1px 3px rgba(67,56,202,0.3); transition: background 0.15s ease;" onmouseover="this.style.background='#3730A3'" onmouseout="this.style.background='#4338CA'">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span>+ Nueva Release / Versión</span>
                </button>
              </div>
            </div>

            <!-- Grilla de 4 Columnas Kanban -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; align-items: flex-start;">
              
              <!-- Columna 1: Planificadas -->
              <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column;">
                <div style="padding: 10px 14px; background: #F1F5F9; border-bottom: 1.5px solid #CBD5E1; display: flex; justify-content: space-between; align-items: center;">
                  <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 800; color: #475569;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #94A3B8;"></span>
                    <span>PLANIFICADAS</span>
                  </div>
                  <span id="kanban-count-planificada" style="font-size: 11px; font-weight: 800; background: #FFFFFF; border: 1px solid #CBD5E1; color: #475569; padding: 1px 7px; border-radius: 10px;">0</span>
                </div>
                <div id="kanban-col-planificada" style="padding: 10px; display: flex; flex-direction: column; gap: 10px; min-height: 480px; max-height: 720px; overflow-y: auto;">
                  <!-- Renderizado dinámico -->
                </div>
              </div>

              <!-- Columna 2: En Desarrollo -->
              <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column;">
                <div style="padding: 10px 14px; background: #E0F2FE; border-bottom: 1.5px solid #7DD3FC; display: flex; justify-content: space-between; align-items: center;">
                  <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 800; color: #0369A1;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #0284C7;"></span>
                    <span>EN DESARROLLO (N3)</span>
                  </div>
                  <span id="kanban-count-desarrollo" style="font-size: 11px; font-weight: 800; background: #FFFFFF; border: 1px solid #7DD3FC; color: #0369A1; padding: 1px 7px; border-radius: 10px;">0</span>
                </div>
                <div id="kanban-col-desarrollo" style="padding: 10px; display: flex; flex-direction: column; gap: 10px; min-height: 480px; max-height: 720px; overflow-y: auto;">
                  <!-- Renderizado dinámico -->
                </div>
              </div>

              <!-- Columna 3: Staging / QA -->
              <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column;">
                <div style="padding: 10px 14px; background: #FEF3C7; border-bottom: 1.5px solid #FCD34D; display: flex; justify-content: space-between; align-items: center;">
                  <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 800; color: #B45309;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #D97706;"></span>
                    <span>STAGING / PRUEBAS</span>
                  </div>
                  <span id="kanban-count-staging" style="font-size: 11px; font-weight: 800; background: #FFFFFF; border: 1px solid #FCD34D; color: #B45309; padding: 1px 7px; border-radius: 10px;">0</span>
                </div>
                <div id="kanban-col-staging" style="padding: 10px; display: flex; flex-direction: column; gap: 10px; min-height: 480px; max-height: 720px; overflow-y: auto;">
                  <!-- Renderizado dinámico -->
                </div>
              </div>

              <!-- Columna 4: Desplegadas a Producción -->
              <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column;">
                <div style="padding: 10px 14px; background: #DCFCE7; border-bottom: 1.5px solid #86EFAC; display: flex; justify-content: space-between; align-items: center;">
                  <div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 800; color: #15803D;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #16A34A;"></span>
                    <span>DESPLEGADAS (PROD)</span>
                  </div>
                  <span id="kanban-count-desplegada" style="font-size: 11px; font-weight: 800; background: #FFFFFF; border: 1px solid #86EFAC; color: #15803D; padding: 1px 7px; border-radius: 10px;">0</span>
                </div>
                <div id="kanban-col-desplegada" style="padding: 10px; display: flex; flex-direction: column; gap: 10px; min-height: 480px; max-height: 720px; overflow-y: auto;">
                  <!-- Renderizado dinámico -->
                </div>
              </div>

            </div>

          </div>
        </section>
'''

kanban_modals_html = '''
  <!-- MODAL: NUEVA RELEASE / VERSIÓN EN KANBAN -->
  <div class="modal-overlay" id="modal-new-release" style="display: none; align-items: center; justify-content: center; background: rgba(15,23,42,0.65); z-index: 9999;">
    <div style="background: #FFFFFF; border-radius: 12px; width: 100%; max-width: 480px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2);">
      <div style="padding: 16px 20px; background: #4338CA; color: #FFFFFF; display: flex; justify-content: space-between; align-items: center;">
        <h3 style="margin: 0; font-size: 15px; font-weight: 800;">+ Crear Nueva Release de Software</h3>
        <button type="button" onclick="closeNewReleaseModal()" style="background: none; border: none; color: #FFFFFF; font-size: 20px; cursor: pointer;">&times;</button>
      </div>
      <form id="form-new-release" onsubmit="submitNewRelease(event)" style="padding: 20px; display: flex; flex-direction: column; gap: 14px;">
        <div>
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">Etiqueta / Tag (SemVer):</label>
          <input type="text" id="new-rel-tag" placeholder="Ej: v4.1.0 o hotfix-202609-01" required style="width: 100%; padding: 8px 12px; border-radius: 6px; border: 1.5px solid #CBD5E1; font-size: 12.5px; font-family: monospace;">
        </div>
        <div>
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">Nombre del Release / Objetivo:</label>
          <input type="text" id="new-rel-name" placeholder="Ej: Fix masivo pasarela de pagos e interoperabilidad" required style="width: 100%; padding: 8px 12px; border-radius: 6px; border: 1.5px solid #CBD5E1; font-size: 12.5px;">
        </div>
        <div>
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">Notas Técnicas / Alcance (Opcional):</label>
          <textarea id="new-rel-notes" rows="3" placeholder="Detalles del despliegue, ramas o componentes afectados..." style="width: 100%; padding: 8px 12px; border-radius: 6px; border: 1.5px solid #CBD5E1; font-size: 12px;"></textarea>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 6px;">
          <button type="button" onclick="closeNewReleaseModal()" style="padding: 8px 14px; border-radius: 6px; border: 1px solid #CBD5E1; background: #FFFFFF; font-size: 12px; font-weight: 700; cursor: pointer;">Cancelar</button>
          <button type="submit" style="padding: 8px 16px; border-radius: 6px; border: none; background: #4338CA; color: #FFFFFF; font-size: 12px; font-weight: 700; cursor: pointer;">Guardar Release</button>
        </div>
      </form>
    </div>
  </div>

  <!-- MODAL: ESCALAR TICKET A N3 Y VINCULAR A KANBAN -->
  <div class="modal-overlay" id="modal-escalate-n3-kanban" style="display: none; align-items: center; justify-content: center; background: rgba(15,23,42,0.65); z-index: 9999;">
    <div style="background: #FFFFFF; border-radius: 12px; width: 100%; max-width: 500px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.2);">
      <div style="padding: 16px 20px; background: #0F172A; color: #FFFFFF; display: flex; justify-content: space-between; align-items: center;">
        <h3 style="margin: 0; font-size: 15px; font-weight: 800;">⚡ Escalar a Ingeniería N3 & Vincular a Release</h3>
        <button type="button" onclick="closeEscalateN3Modal()" style="background: none; border: none; color: #FFFFFF; font-size: 20px; cursor: pointer;">&times;</button>
      </div>
      <div style="padding: 20px; display: flex; flex-direction: column; gap: 14px;">
        <input type="hidden" id="escalate-n3-ticket-id">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 14px;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B;">Solicitud Seleccionada:</div>
          <div id="escalate-n3-ticket-title" style="font-size: 13px; font-weight: 800; color: #0F172A; margin-top: 2px;">-</div>
        </div>
        <div>
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">Seleccionar Release de Software:</label>
          <select id="escalate-n3-release-select" onchange="if(this.value==='__NEW__'){document.getElementById('escalate-n3-new-tag-box').style.display='block';}else{document.getElementById('escalate-n3-new-tag-box').style.display='none';}" style="width: 100%; padding: 8px 12px; border-radius: 6px; border: 1.5px solid #CBD5E1; font-size: 12.5px;">
            <!-- Poblado dinámicamente -->
          </select>
        </div>
        <div id="escalate-n3-new-tag-box" style="display: none;">
          <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 4px;">Nueva Etiqueta de Release:</label>
          <input type="text" id="escalate-n3-new-tag" placeholder="Ej: v4.0.2-patch" style="width: 100%; padding: 8px 12px; border-radius: 6px; border: 1.5px solid #CBD5E1; font-size: 12.5px; font-family: monospace;">
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 6px;">
          <button type="button" onclick="closeEscalateN3Modal()" style="padding: 8px 14px; border-radius: 6px; border: 1px solid #CBD5E1; background: #FFFFFF; font-size: 12px; font-weight: 700; cursor: pointer;">Cancelar</button>
          <button type="button" onclick="submitEscalateN3()" style="padding: 8px 16px; border-radius: 6px; border: none; background: #16A34A; color: #FFFFFF; font-size: 12px; font-weight: 700; cursor: pointer;">Vincular y Escalar a N3</button>
        </div>
      </div>
    </div>
  </div>
'''

if 'id="view-kanban"' not in html_content:
    target_pos = html_content.find('id="view-team-leader"')
    if target_pos != -1:
        end_section = html_content.find('</section>', target_pos) + len('</section>')
        html_content = html_content[:end_section] + '\n' + kanban_view_html + html_content[end_section:]
        print("[OK] view-kanban inyectado en frontend/index.html")

if 'id="modal-new-release"' not in html_content:
    body_end = html_content.rfind('</body>')
    if body_end != -1:
        html_content = html_content[:body_end] + '\n' + kanban_modals_html + '\n' + html_content[body_end:]
        print("[OK] modales de kanban inyectados en frontend/index.html")

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("[OK] frontend/index.html actualizado exitosamente.")
