# -*- coding: utf-8 -*-
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire view-requester-portal section
start_marker = '<section class="app-view" id="view-requester-portal">'
end_marker = '</section>'

start_pos = html.find(start_marker)
if start_pos != -1:
    end_pos = html.find(end_marker, start_pos) + len(end_marker)
    
    new_portal_html = '''<section class="app-view" id="view-requester-portal">
          <div class="users-board-wrapper" id="requester-clinical-portal" style="max-width: 1040px; margin: 0 auto; padding: 18px 24px; display: flex; flex-direction: column; min-height: calc(100vh - 80px);">
            
            <!-- Encabezado Corporativo Quantux HealthDesk -->
            <div style="background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; padding: 16px 22px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);">
              <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: linear-gradient(135deg, #0A1C3E 0%, #00A896 100%); display: flex; align-items: center; justify-content: center; color: #FFFFFF; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0, 168, 150, 0.25);">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 22px; height: 22px;"><path d="M3 18v-6a9 9 0 0 1 18 0v6"></path><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path></svg>
                </div>
                <div>
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <h2 style="margin: 0; font-size: 16.5px; font-weight: 800; color: #0A1C3E; font-family: 'Outfit', sans-serif; letter-spacing: -0.2px;">Centro de Asistencia Asistencial & Soporte TI</h2>
                    <span style="display: inline-flex; align-items: center; gap: 5px; background: #E6FBF9; color: #008F80; font-size: 11px; font-weight: 800; padding: 2.5px 9px; border-radius: 9999px; border: 1px solid #A7F3D0;">
                      <span style="width: 6px; height: 6px; border-radius: 50%; background: #00A896; box-shadow: 0 0 6px #00A896;"></span> Guardia en Línea
                    </span>
                  </div>
                  <p style="margin: 3px 0 0 0; font-size: 12px; color: #64748B;">
                    Hola, <strong id="req-portal-user-name" style="color: #0F172A;">Dr. Martín Gómez</strong> &bull; <span id="req-portal-user-inst" style="color: #00A896; font-weight: 700;">Swiss Medical</span>
                  </p>
                </div>
              </div>

              <!-- Acciones Superiores -->
              <div style="display: flex; align-items: center; gap: 12px;">
                <button type="button" onclick="openRequesterHistoryModal()" title="Ver historial de mis solicitudes previas" style="background: #F8FAFC; border: 1px solid #CBD5E1; color: #334155; font-size: 12px; font-weight: 700; cursor: pointer; padding: 8px 14px; border-radius: 8px; display: inline-flex; align-items: center; gap: 6px; transition: all 0.15s ease;" onmouseover="this.style.background='#F1F5F9'; this.style.borderColor='#94A3B8';" onmouseout="this.style.background='#F8FAFC'; this.style.borderColor='#CBD5E1';">
                  <svg viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" style="width: 14px; height: 14px;"><path d="M12 8v4l3 3"></path><circle cx="12" cy="12" r="9"></circle></svg>
                  <span>Mis Solicitudes (<strong id="req-history-badge" style="color: #00A896;">0</strong>)</span>
                </button>

                <button type="button" onclick="openFastTicketModal()" title="Generar un ticket directo sin interactuar con el chat" style="display: flex; align-items: center; gap: 6px; background: #00A896; color: #FFFFFF; border: none; padding: 8px 16px; border-radius: 8px; font-size: 12.5px; font-weight: 700; cursor: pointer; transition: all 0.15s ease; box-shadow: 0 2px 6px rgba(0, 168, 150, 0.3);" onmouseover="this.style.background='#008F80'" onmouseout="this.style.background='#00A896'">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width: 14px; height: 14px;"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span>+ Crear Solicitud Directa</span>
                </button>
              </div>
            </div>

            <!-- Interfaz Principal: CHAT DE IA CONVERSACIONAL QUANTUX -->
            <div style="flex: 1; background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 20px -2px rgba(10, 28, 62, 0.05); min-height: 540px;">
              
              <!-- Stream de Mensajes del Chat Asistencial -->
              <div id="requester-inline-chat-stream" style="flex: 1; overflow-y: auto; padding: 24px 28px; display: flex; flex-direction: column; gap: 16px; scroll-behavior: smooth; background: #FAFAFC;">
                
                <!-- Estado Inicial / Hero de Bienvenida Quantux -->
                <div id="requester-chat-hero" style="margin: auto 0; text-align: center; max-width: 680px; align-self: center; padding: 28px 16px;">
                  <div style="width: 54px; height: 54px; border-radius: 14px; background: linear-gradient(135deg, #E6FBF9 0%, #CCF7F3 100%); border: 1.5px solid #99EFE7; color: #00A896; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0, 168, 150, 0.15);">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 28px; height: 28px;"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path><circle cx="9" cy="10" r="1"></circle><circle cx="15" cy="10" r="1"></circle></svg>
                  </div>
                  <h3 style="font-family: 'Outfit', sans-serif; font-size: 21px; font-weight: 800; color: #0A1C3E; margin: 0 0 8px 0; letter-spacing: -0.3px;">
                    ¿En qué podemos asistirte en tu consultorio hoy?
                  </h3>
                  <p style="font-size: 13.5px; color: #64748B; margin: 0 0 24px 0; line-height: 1.55;">
                    Consulta al motor de IA médica, transcribe tu reporte por voz en tiempo real o selecciona uno de los accesos rápidos a continuación:
                  </p>

                  <!-- 4 Accesos Rápidos Frecuentes Quantux -->
                  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; text-align: left;">
                    <button type="button" onclick="sendRequesterPrompt('No puedo firmar receta digital ni validar token')" style="padding: 14px 16px; border-radius: 10px; border: 1.5px solid #E2E8F0; background: #FFFFFF; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);" onmouseover="this.style.borderColor='#00A896'; this.style.background='#F0FDFB'; this.style.transform='translateY(-1px)';" onmouseout="this.style.borderColor='#E2E8F0'; this.style.background='#FFFFFF'; this.style.transform='none';">
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 30px; height: 30px; border-radius: 6px; background: #E6FBF9; display: flex; align-items: center; justify-content: center; color: #00A896; flex-shrink: 0;">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                        </div>
                        <span style="font-weight: 800; color: #0A1C3E; font-size: 13px;">Receta & Firma Digital</span>
                      </div>
                      <div style="font-size: 11.5px; color: #64748B; margin-top: 6px; line-height: 1.4;">Validación de firma, token criptográfico o padrón SISA</div>
                    </button>

                    <button type="button" onclick="sendRequesterPrompt('Error 500 / Timeout al guardar en Consultorio Digital')" style="padding: 14px 16px; border-radius: 10px; border: 1.5px solid #E2E8F0; background: #FFFFFF; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);" onmouseover="this.style.borderColor='#00A896'; this.style.background='#F0FDFB'; this.style.transform='translateY(-1px)';" onmouseout="this.style.borderColor='#E2E8F0'; this.style.background='#FFFFFF'; this.style.transform='none';">
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 30px; height: 30px; border-radius: 6px; background: #FEF3C7; display: flex; align-items: center; justify-content: center; color: #D97706; flex-shrink: 0;">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                        </div>
                        <span style="font-weight: 800; color: #0A1C3E; font-size: 13px;">Error de Sistema / Timeout 500</span>
                      </div>
                      <div style="font-size: 11.5px; color: #64748B; margin-top: 6px; line-height: 1.4;">Desbloqueo de concurrencia y reintento seguro en HCE</div>
                    </button>

                    <button type="button" onclick="sendRequesterPrompt('Desbloqueo de clave o restablecimiento de acceso')" style="padding: 14px 16px; border-radius: 10px; border: 1.5px solid #E2E8F0; background: #FFFFFF; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);" onmouseover="this.style.borderColor='#00A896'; this.style.background='#F0FDFB'; this.style.transform='translateY(-1px)';" onmouseout="this.style.borderColor='#E2E8F0'; this.style.background='#FFFFFF'; this.style.transform='none';">
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 30px; height: 30px; border-radius: 6px; background: #EEF2FF; display: flex; align-items: center; justify-content: center; color: #4338CA; flex-shrink: 0;">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        </div>
                        <span style="font-weight: 800; color: #0A1C3E; font-size: 13px;">Acceso, Matrícula & Claves</span>
                      </div>
                      <div style="font-size: 11.5px; color: #64748B; margin-top: 6px; line-height: 1.4;">Restablecimiento exprés de usuario asistencial</div>
                    </button>

                    <button type="button" onclick="sendRequesterPrompt('Problema de impresión o exportación de PDF de historia clínica')" style="padding: 14px 16px; border-radius: 10px; border: 1.5px solid #E2E8F0; background: #FFFFFF; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);" onmouseover="this.style.borderColor='#00A896'; this.style.background='#F0FDFB'; this.style.transform='translateY(-1px)';" onmouseout="this.style.borderColor='#E2E8F0'; this.style.background='#FFFFFF'; this.style.transform='none';">
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 30px; height: 30px; border-radius: 6px; background: #F1F5F9; display: flex; align-items: center; justify-content: center; color: #475569; flex-shrink: 0;">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                        </div>
                        <span style="font-weight: 800; color: #0A1C3E; font-size: 13px;">Impresión & Exportación PDF</span>
                      </div>
                      <div style="font-size: 11.5px; color: #64748B; margin-top: 6px; line-height: 1.4;">Atasco de cola o formato no generado</div>
                    </button>
                  </div>
                </div>

              </div>

              <!-- Indicador de Dictado por Voz Activo Quantux -->
              <div id="voice-recording-indicator" style="display: none; padding: 10px 20px; background: #FEF2F2; border-top: 1.5px solid #FECACA; color: #B91C1C; font-size: 12.5px; font-weight: 700; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <span style="width: 10px; height: 10px; border-radius: 50%; background: #EF4444; animation: pulse 1s infinite;"></span>
                  <span>Escuchando dictado por voz asistencial... hable con naturalidad</span>
                </div>
                <button type="button" onclick="stopVoiceRecording()" style="background: #EF4444; color: #FFF; border: none; padding: 4px 12px; border-radius: 6px; font-size: 11.5px; font-weight: 800; cursor: pointer;">Detener</button>
              </div>

              <!-- Barra Inferior de Entrada Quantux -->
              <div style="padding: 16px 20px; border-top: 1.5px solid #E2E8F0; background: #FFFFFF; display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px; background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 10px; padding: 6px 8px 6px 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); transition: all 0.2s ease;" id="requester-input-container">
                  
                  <!-- Input de texto -->
                  <input type="text" id="requester-chat-input" placeholder="Escribe tu consulta o pulsa el micrófono para dictar el problema..." onkeydown="handleRequesterChatKey(event)" style="flex: 1; border: none; outline: none; font-size: 13.5px; color: #0F172A; background: transparent; padding: 8px 0;">
                  
                  <!-- Botón de Micrófono (Dictado por Voz) -->
                  <button type="button" id="btn-requester-voice" onclick="toggleVoiceRecording()" title="Dictar consulta o ticket por voz (Micrófono)" aria-label="Dictar por voz" style="width: 36px; height: 36px; border-radius: 8px; background: #E6FBF9; border: 1px solid #99EFE7; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #00A896; transition: all 0.15s ease;" onmouseover="this.style.background='#CCF7F3'" onmouseout="this.style.background='#E6FBF9'">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width: 18px; height: 18px;"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
                  </button>

                  <!-- Botón Enviar Consulta -->
                  <button type="button" id="btn-requester-send" onclick="sendRequesterChatMessage()" title="Enviar mensaje" aria-label="Enviar" style="width: 36px; height: 36px; border-radius: 8px; background: #00A896; border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #FFFFFF; transition: all 0.15s ease; box-shadow: 0 2px 4px rgba(0, 168, 150, 0.25);" onmouseover="this.style.background='#008F80'" onmouseout="this.style.background='#00A896'">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                  </button>
                </div>

                <!-- Barra de atajos para médico en consultorio -->
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #64748B; padding: 0 4px;">
                  <span>Presiona <strong>Enter</strong> para enviar &bull; Micrófono para dictado inteligente</span>
                  <div style="display: flex; gap: 8px;">
                    <button type="button" onclick="createTicketFromCurrentInput()" style="background: none; border: none; color: #00A896; font-weight: 800; cursor: pointer; text-decoration: underline; padding: 0;" onmouseover="this.style.color='#008F80'" onmouseout="this.style.color='#00A896'">
                      Generar ticket inmediato con este texto &rarr;
                    </button>
                  </div>
                </div>
              </div>

            </div>

          </div>
        </section>'''
    
    html = html[:start_pos] + new_portal_html + html[end_pos:]
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('[OK] Portal del Solicitante rediseñado con el estilo oficial Quantux.')
else:
    print('[ERROR] start_marker not found')
