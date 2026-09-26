import os

app_path = os.path.join('frontend', 'js', 'app.js')
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Author selector in openAgentWorkspace
target_open_ws = """ // 4. Avatar del Agente en la caja de respuesta
 const elReplyAvatar = document.getElementById('ws-reply-user-avatar');
 if (elReplyAvatar) {
 const uName = AppState.currentUser ? AppState.currentUser.full_name : 'Agente';
 elReplyAvatar.textContent = getInitials(uName);
 }"""

repl_open_ws = """ // 4. Selector de Identidad y Avatar en la caja de respuesta
 const authorSelect = document.getElementById('ws-reply-author-select');
 if (authorSelect) {
   const opDisplay = ticket.assignee_name || (ticket.assignee_username ? formatUserName(ticket.assignee_username) : 'Laura Benítez (Soporte N2)');
   const reqDisplay = ticket.requester_name || (ticket.requester_username ? formatUserName(ticket.requester_username) : 'Dr. Martín Gómez (Solicitante)');
   authorSelect.innerHTML = `
     <option value="operador">Operador Asignado: ${escapeHtml(opDisplay)}</option>
     <option value="solicitante">Prestador / Solicitante: ${escapeHtml(reqDisplay)}</option>
     <option value="bot_quantux">🤖 Bot Quantux (Asistencia Operativa)</option>
   `;
   authorSelect.value = 'operador';
   onWsReplyAuthorChange();
 } else {
   const elReplyAvatar = document.getElementById('ws-reply-user-avatar');
   if (elReplyAvatar) {
     const uName = AppState.currentUser ? AppState.currentUser.full_name : 'Agente';
     elReplyAvatar.textContent = getInitials(uName);
   }
 }"""

if target_open_ws in js:
    js = js.replace(target_open_ws, repl_open_ws, 1)
    print("openAgentWorkspace authorSelect injected OK")
else:
    print("target_open_ws NOT found")

# 2. Complete block from submitAgentWorkspaceReply to confirmReassign
# Find start of submitAgentWorkspaceReply
start_idx = js.find("async function submitAgentWorkspaceReply() {")
end_idx = js.find("async function quickSelfAssign(ticketId) {")

if start_idx != -1 and end_idx != -1:
    new_block = """async function onWsReplyAuthorChange() {
  const select = document.getElementById('ws-reply-author-select');
  const avatar = document.getElementById('ws-reply-user-avatar');
  const hint = document.getElementById('ws-reply-channel-hint');
  if (!select) return;

  const ticket = AppState.selectedTicket;
  const val = select.value;
  if (val === 'solicitante') {
    const name = ticket ? (ticket.requester_name || ticket.requester_username || 'Solicitante') : 'Solicitante';
    if (avatar) avatar.textContent = getInitials(name);
    if (hint) hint.textContent = 'Canal: Portal Clínico Web (Dr. Solicitante)';
  } else if (val === 'bot_quantux') {
    if (avatar) avatar.textContent = 'BQ';
    if (hint) hint.textContent = 'Canal: Mediación Automática Quantux';
  } else {
    const name = ticket ? (ticket.assignee_name || ticket.assignee_username || 'Laura Benítez') : 'Laura Benítez';
    if (avatar) avatar.textContent = getInitials(name);
    if (hint) hint.textContent = 'Canal: Mesa de Operaciones Quantux';
  }
}

async function triggerBotInteraction(actionType = 'request_requester_info') {
  if (!AppState.selectedTicket) return;
  const ticketId = AppState.selectedTicket.id;
  try {
    const res = await API.request(`/tickets/${ticketId}/bot-interact`, {
      method: 'POST',
      body: JSON.stringify({ action_type: actionType })
    });
    showToast(res.message || 'Intervención del Bot Quantux registrada con éxito', 'success');
    const refreshed = await API.getTicket(ticketId);
    AppState.selectedTicket = refreshed;
    renderWsTimeline(refreshed);
    renderWsParticipants(refreshed);
    renderWsProgressSLA(refreshed);
    renderWsWorkflowActions(refreshed);
    loadTickets();
  } catch (err) {
    console.error('Error en interacción del bot:', err);
    showToast('Error al ejecutar la acción del Bot', 'error');
  }
}

async function submitAgentWorkspaceReply() {
  if (!AppState.selectedTicket) return;
  const textarea = document.getElementById('ws-reply-textarea');
  const isInternalCheck = document.getElementById('ws-reply-is-internal');
  const authorSelect = document.getElementById('ws-reply-author-select');
  if (!textarea) return;

  const content = textarea.value.trim();
  if (!content) {
    showToast('Por favor ingrese un mensaje o respuesta', 'warning');
    return;
  }

  const isInternal = isInternalCheck ? isInternalCheck.checked : false;
  const authorMode = authorSelect ? authorSelect.value : 'operador';
  const ticket = AppState.selectedTicket;

  let authorUsername = 'soporte';
  let authorName = 'Laura Benítez';
  let authorRole = 'SOPORTE_N2';

  if (authorMode === 'solicitante') {
    authorUsername = ticket.requester_username || 'solicitante';
    authorName = ticket.requester_name || (ticket.requester_username ? formatUserName(ticket.requester_username) : 'Dr. Martín Gómez (Solicitante)');
    authorRole = 'SOLICITANTE';
  } else if (authorMode === 'bot_quantux') {
    authorUsername = 'bot_quantux';
    authorName = 'Bot Quantux';
    authorRole = 'SISTEMA';
  } else {
    authorUsername = ticket.assignee_username || (AppState.currentUser ? AppState.currentUser.username : 'soporte');
    authorName = ticket.assignee_name || (ticket.assignee_username ? formatUserName(ticket.assignee_username) : (AppState.currentUser ? AppState.currentUser.full_name : 'Laura Benítez (Soporte)'));
    authorRole = (ticket.support_level ? `SOPORTE_${ticket.support_level}` : 'SOPORTE_N2');
  }

  try {
    const payload = {
      message: content,
      content: content,
      is_internal: isInternal,
      author_username: authorUsername,
      author_name: authorName,
      author_role: authorRole
    };

    await API.addComment(ticket.id, payload);
    textarea.value = '';
    showToast(isInternal ? 'Nota interna agregada' : 'Respuesta enviada con éxito', 'success');

    // Refrescar ticket y recalcular SLA
    const refreshed = await API.getTicket(ticket.id);
    AppState.selectedTicket = refreshed;
    renderWsTimeline(refreshed);
    renderWsParticipants(refreshed);
    renderWsProgressSLA(refreshed);
    renderWsWorkflowActions(refreshed);

    loadTickets();
  } catch (err) {
    console.error('Error enviando respuesta:', err);
    showToast('Error al enviar la respuesta', 'error');
  }
}

function insertQuickResponseTemplate() {
  const textarea = document.getElementById('ws-reply-textarea');
  if (!textarea) return;

  const templates = [
    "Estimado/a profesional, hemos tomado intervención en su solicitud asistencial. Se realizaron las validaciones en el módulo clínico y nos encontramos aplicando las correcciones requeridas. Lo mantendremos informado.",
    "Se ha verificado la conectividad y estado del servicio asistencial. Por favor reintente la acción en el sistema y confírmenos si el incidente persiste.",
    "Procedimiento completado conforme a protocolo operativo. Aguardamos su validación para proceder con el cierre de la solicitud."
  ];

  textarea.value = templates[0];
  textarea.focus();
}

function reassignFromWorkspace() {
  if (!AppState.selectedTicket) return;
  openReassignModal(AppState.selectedTicket.id);
}

// Variables globales para la memoria del buscador predictivo
let currentReassignCandidates = [];

async function openReassignModal(ticketId) {
  const ticket = AppState.selectedTicket || (AppState.tickets && AppState.tickets.find(t => String(t.id) === String(ticketId)));
  if (!ticket) return;

  const existingModal = document.getElementById('modal-dynamic-reassign');
  if (existingModal) existingModal.remove();

  // 1. Obtener lista base de operadores
  let operators = [];
  try {
    operators = await API.getOperators();
  } catch (err) {
    console.warn('No se pudo obtener operadores desde API, usando usuarios en memoria:', err);
  }

  if (!operators || operators.length === 0) {
    if (AppState.users && AppState.users.length > 0) {
      operators = AppState.users.filter(u => u.role === 'SOPORTE' || u.role === 'ADMIN');
    }
  }

  if (!operators || operators.length === 0) {
    operators = [
      { username: 'admin', full_name: 'Freddy Cortés', role: 'ADMIN', support_level: 'N3', email: 'fcortes@quantuxsalud.com', sector: 'Ingeniería N3 & Arquitectura' },
      { username: 'soporte', full_name: 'Laura Benítez', role: 'SOPORTE', support_level: 'N2', email: 'soporte@quantuxsalud.com', sector: 'Mesa N2 Pasarelas & Integraciones' },
      { username: 'cpaez', full_name: 'Carlos Páez', role: 'SOPORTE', support_level: 'N2', email: 'cpaez@quantuxsalud.com', sector: 'Mesa N2 Receta Digital & SISA' },
      { username: 'svaldez', full_name: 'Sofía Valdez', role: 'SOPORTE', support_level: 'N1', email: 'svaldez@quantuxsalud.com', sector: 'Mesa N1 Triage & Guardia' },
      { username: 'dnavarro', full_name: 'Diego Navarro', role: 'ADMIN', support_level: 'N3', email: 'dnavarro@quantuxsalud.com', sector: 'Infraestructura Cloud & DBAs' },
      { username: 'mrodriguez', full_name: 'Mariana Rodríguez', role: 'ADMIN', support_level: 'N3', email: 'mrodriguez@quantuxsalud.com', sector: 'Desarrollo Core & APIs' },
      { username: 'mflores', full_name: 'Marcos Flores', role: 'SOPORTE', support_level: 'N1', email: 'mflores@quantuxsalud.com', sector: 'Mesa N1 Atención Inicial' },
      { username: 'ealvarez', full_name: 'Elena Álvarez', role: 'SOPORTE', support_level: 'N2', email: 'ealvarez@quantuxsalud.com', sector: 'Mesa N2 Facturación Asistencial' },
      { username: 'vromero', full_name: 'Valeria Romero', role: 'SOPORTE', support_level: 'N2', email: 'vromero@quantuxsalud.com', sector: 'Mesa N2 Telemedicina & Turnos' },
      { username: 'gfernandez', full_name: 'Gustavo Fernández', role: 'SOPORTE', support_level: 'N1', email: 'gfernandez@quantuxsalud.com', sector: 'Mesa N1 Guardia Médica' }
    ];
  }

  // 2. Incorporar OBLIGATORIAMENTE al Solicitante / Prestador como opción de derivación
  const reqUsername = ticket.requester_username || 'solicitante';
  const reqFullName = ticket.requester_name || (ticket.requester_username ? formatUserName(ticket.requester_username) : 'Dr. Martín Gómez');
  const reqEmail = ticket.requester_email || `${reqUsername}@cemic.edu.ar`;

  const requesterCandidate = {
    username: reqUsername,
    full_name: reqFullName,
    role: 'SOLICITANTE',
    support_level: 'SOLICITANTE',
    email: reqEmail,
    sector: 'Prestador Clínico / Solicitante (Pausa de SLA)'
  };

  // Unificar candidatos: Solicitante primero, luego operadores
  currentReassignCandidates = [
    requesterCandidate,
    ...operators.map(op => ({
      username: op.username,
      full_name: op.full_name || formatUserName(op.username),
      role: op.role || 'SOPORTE',
      support_level: (op.support_level || (op.role === 'ADMIN' ? 'N3' : 'N2')).toUpperCase(),
      email: op.email || `${op.username}@quantuxsalud.com`,
      sector: op.sector || `Mesa ${op.support_level || 'N2'}`
    }))
  ];

  // Default selection: actual assignee o primer operador
  const initialSelected = currentReassignCandidates.find(c => c.username === ticket.assignee_username) || currentReassignCandidates[1] || currentReassignCandidates[0];
  const initialLevel = initialSelected.support_level === 'SOLICITANTE' ? 'SOLICITANTE' : (ticket.support_level || initialSelected.support_level || 'N2');

  const modalHtml = `
    <div id="modal-dynamic-reassign" style="z-index: 10000; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.65); display: flex; align-items: center; justify-content: center; backdrop-filter: blur(4px);">
      <div style="background: #FFFFFF; border-radius: 12px; max-width: 560px; width: 92%; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); overflow: hidden; animation: fadeIn 0.15s ease-out;">
        
        <div style="background: #0F172A; color: #FFF; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between;">
          <h5 style="margin: 0; font-size: 15px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
            <span>⇄</span> Asignar / Derivar Ticket a Mesa o Solicitante
          </h5>
          <button type="button" onclick="closeReassignModal()" style="background: transparent; border: none; color: #94A3B8; font-size: 18px; cursor: pointer; padding: 0 4px;">✕</button>
        </div>

        <div style="padding: 20px;">
          <!-- Ticket Context -->
          <div style="margin-bottom: 14px;">
            <label style="display: block; font-size: 11.5px; font-weight: 700; color: #475569; margin-bottom: 4px; text-transform: uppercase;">Ticket en Gestión:</label>
            <div style="font-size: 13px; font-weight: 600; color: #0F172A; background: #F8FAFC; padding: 9px 12px; border-radius: 6px; border: 1px solid #E2E8F0;">
              #${ticket.id} — ${escapeHtml(ticket.title || '')}
            </div>
          </div>

          <!-- Buscador Predictivo (Typeahead) -->
          <div style="margin-bottom: 14px;">
            <label style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: #475569; margin-bottom: 4px; text-transform: uppercase;">
              <span>Buscar Destinatario (Predictivo)</span>
              <span style="font-weight: normal; color: #64748B;">Filtrar por nombre, usuario, sector o nivel</span>
            </label>
            <div style="position: relative;">
              <input type="text" id="reassign-search-input" placeholder="Escriba para filtrar (ej: Martín, Laura, N3, Facturación, cpaez)..." oninput="filterReassignCandidates(this.value)" autocomplete="off" style="width: 100%; box-sizing: border-box; padding: 10px 12px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 13px; font-weight: 600; color: #0F172A; background: #FFFFFF; outline: none;">
            </div>

            <!-- Contenedor de Resultados Filtrados Dinámicos -->
            <div id="reassign-results-list" style="max-height: 180px; overflow-y: auto; margin-top: 6px; border: 1px solid #E2E8F0; border-radius: 6px; background: #FFFFFF; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
              <!-- Renderizado dinámico -->
            </div>
          </div>

          <!-- Campos Ocultos de Selección -->
          <input type="hidden" id="reassign-selected-username" value="${escapeHtml(initialSelected.username)}">
          <input type="hidden" id="reassign-selected-fullname" value="${escapeHtml(initialSelected.full_name)}">

          <!-- Preview de Selección Actual -->
          <div id="reassign-selected-preview" style="margin-bottom: 14px; padding: 10px 14px; background: #F1F5F9; border-radius: 6px; border: 1px solid #CBD5E1; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div id="reassign-preview-avatar" style="width: 32px; height: 32px; border-radius: 6px; background: #0F172A; color: #FFF; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700;">
                ${getInitials(initialSelected.full_name)}
              </div>
              <div>
                <div id="reassign-preview-name" style="font-size: 13px; font-weight: 700; color: #0F172A;">${escapeHtml(initialSelected.full_name)} (@${initialSelected.username})</div>
                <div id="reassign-preview-sector" style="font-size: 11px; color: #475569;">${escapeHtml(initialSelected.sector)}</div>
              </div>
            </div>
            <span id="reassign-preview-badge" style="font-size: 10.5px; font-weight: 700; padding: 3px 8px; border-radius: 4px; background: #0F172A; color: #FFFFFF;">
              ${initialSelected.support_level}
            </span>
          </div>

          <!-- Selector de Nivel de Atención -->
          <div style="margin-bottom: 14px;">
            <label style="display: block; font-size: 11.5px; font-weight: 700; color: #475569; margin-bottom: 4px; text-transform: uppercase;">Nivel ITIL o Destino:</label>
            <select id="reassign-level-select" style="width: 100%; padding: 9px 12px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 13px; background: #FFF; font-weight: 600; color: #0F172A;">
              <option value="N1" ${initialLevel === 'N1' ? 'selected' : ''}>Nivel N1 — Mesa de Ayuda y Triage</option>
              <option value="N2" ${initialLevel === 'N2' ? 'selected' : ''}>Nivel N2 — Analista Funcional y Soporte Especializado</option>
              <option value="N3" ${initialLevel === 'N3' ? 'selected' : ''}>Nivel N3 — Ingeniería, DBAs y Arquitectura</option>
              <option value="SOLICITANTE" ${initialLevel === 'SOLICITANTE' ? 'selected' : ''}>Solicitante — Prestador Clínico (Pausa de SLA)</option>
            </select>
          </div>

          <!-- Motivo de Derivación -->
          <div style="margin-bottom: 18px;">
            <label style="display: block; font-size: 11.5px; font-weight: 700; color: #475569; margin-bottom: 4px; text-transform: uppercase;">Nota de Derivación / Motivo Operativo:</label>
            <textarea id="reassign-reason-textarea" rows="2" placeholder="Indique motivo técnico o instrucciones para el destinatario..." style="width: 100%; box-sizing: border-box; padding: 8px 12px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 12px; resize: none; font-family: inherit; outline: none;"></textarea>
          </div>

          <!-- Botones de Acción -->
          <div style="display: flex; gap: 8px; justify-content: flex-end;">
            <button type="button" onclick="closeReassignModal()" style="padding: 8px 14px; background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer;">Cancelar</button>
            <button type="button" onclick="confirmReassign('${ticket.id}')" style="padding: 8px 20px; background: #0F172A; color: #FFFFFF; border: none; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; box-shadow: 0 2px 4px rgba(15,23,42,0.25);">Confirmar Derivación</button>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
  renderReassignCandidatesList(currentReassignCandidates);
}

function filterReassignCandidates(query) {
  const cleanQ = (query || '').toLowerCase().trim();
  if (!cleanQ) {
    renderReassignCandidatesList(currentReassignCandidates);
    return;
  }
  const filtered = currentReassignCandidates.filter(c => {
    return c.full_name.toLowerCase().includes(cleanQ) ||
           c.username.toLowerCase().includes(cleanQ) ||
           c.sector.toLowerCase().includes(cleanQ) ||
           c.support_level.toLowerCase().includes(cleanQ) ||
           c.email.toLowerCase().includes(cleanQ);
  });
  renderReassignCandidatesList(filtered);
}

function renderReassignCandidatesList(candidates) {
  const listEl = document.getElementById('reassign-results-list');
  if (!listEl) return;

  if (candidates.length === 0) {
    listEl.innerHTML = `
      <div style="padding: 14px; text-align: center; color: #94A3B8; font-size: 12px;">
        No se encontraron operadores o solicitantes con ese criterio.
      </div>
    `;
    return;
  }

  const selectedUser = document.getElementById('reassign-selected-username')?.value || '';

  listEl.innerHTML = candidates.map(c => {
    const isSel = (c.username === selectedUser);
    const isReq = (c.role === 'SOLICITANTE');
    const badgeColor = isReq ? '#334155' : '#0F172A';
    const badgeBg = isReq ? '#F1F5F9' : '#E2E8F0';

    return `
      <div onclick="selectReassignCandidate('${escapeHtml(c.username)}', '${escapeHtml(c.full_name)}', '${escapeHtml(c.support_level)}', '${escapeHtml(c.sector)}')" 
           style="padding: 8px 12px; border-bottom: 1px solid #F1F5F9; display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: background 0.1s ease; background: ${isSel ? '#F8FAFC' : '#FFFFFF'};" 
           onmouseover="this.style.background='#F1F5F9'" 
           onmouseout="this.style.background='${isSel ? '#F8FAFC' : '#FFFFFF'}'">
        <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
          <div style="width: 28px; height: 28px; border-radius: 4px; background: #0F172A; color: #FFF; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0;">
            ${getInitials(c.full_name)}
          </div>
          <div style="min-width: 0;">
            <div style="font-size: 12.5px; font-weight: 700; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${escapeHtml(c.full_name)} <span style="font-size: 11px; color: #64748B; font-weight: normal;">(@${escapeHtml(c.username)})</span>
            </div>
            <div style="font-size: 10.5px; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${escapeHtml(c.sector)}
            </div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
          <span style="font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; background: ${badgeBg}; color: ${badgeColor};">
            ${c.support_level}
          </span>
          ${isSel ? '<span style="color: #0F172A; font-weight: 800; font-size: 13px;">✓</span>' : ''}
        </div>
      </div>
    `;
  }).join('');
}

function selectReassignCandidate(username, fullName, level, sector) {
  const hiddenUser = document.getElementById('reassign-selected-username');
  const hiddenName = document.getElementById('reassign-selected-fullname');
  const lvlSelect = document.getElementById('reassign-level-select');
  const prevName = document.getElementById('reassign-preview-name');
  const prevSector = document.getElementById('reassign-preview-sector');
  const prevBadge = document.getElementById('reassign-preview-badge');
  const prevAvatar = document.getElementById('reassign-preview-avatar');

  if (hiddenUser) hiddenUser.value = username;
  if (hiddenName) hiddenName.value = fullName;

  if (prevName) prevName.textContent = `${fullName} (@${username})`;
  if (prevSector) prevSector.textContent = sector;
  if (prevBadge) prevBadge.textContent = level;
  if (prevAvatar) prevAvatar.textContent = getInitials(fullName);

  if (lvlSelect) {
    if (level === 'SOLICITANTE') {
      lvlSelect.value = 'SOLICITANTE';
    } else if (level === 'N1' || level === 'N2' || level === 'N3') {
      lvlSelect.value = level;
    }
  }

  // Refrescar lista para mostrar el checkmark en el seleccionado
  const searchInput = document.getElementById('reassign-search-input');
  filterReassignCandidates(searchInput ? searchInput.value : '');
}

function closeReassignModal() {
  const modal = document.getElementById('modal-dynamic-reassign');
  if (modal) modal.remove();
}

async function confirmReassign(ticketId) {
  const usernameInput = document.getElementById('reassign-selected-username');
  const fullnameInput = document.getElementById('reassign-selected-fullname');
  const lvlSelect = document.getElementById('reassign-level-select');
  const reasonText = document.getElementById('reassign-reason-textarea');
  if (!usernameInput || !usernameInput.value) {
    showToast('Seleccione un destinatario para derivar el caso', 'warning');
    return;
  }

  const username = usernameInput.value;
  const fullName = fullnameInput ? fullnameInput.value : username;
  const itilLevel = lvlSelect ? lvlSelect.value : 'N2';
  const reason = reasonText ? reasonText.value.trim() : '';
  const currentActor = AppState.currentUser ? AppState.currentUser.username : 'soporte';

  try {
    await API.assignTicket(ticketId, {
      assignee_username: username,
      support_level: itilLevel,
      reason: reason || `Derivación técnica a ${fullName} (${itilLevel})`,
      changed_by_username: currentActor
    });

    if (reason) {
      await API.addComment(ticketId, {
        message: `📌 Derivación a ${fullName} (${itilLevel}). Motivo: ${reason}`,
        content: `📌 Derivación a ${fullName} (${itilLevel}). Motivo: ${reason}`,
        is_internal: true,
        author_username: currentActor,
        author_name: AppState.currentUser ? AppState.currentUser.full_name : 'Operador',
        author_role: 'SOPORTE'
      });
    }

    closeReassignModal();
    // 1. Cerrar inmediatamente el workspace para que no siga en pantalla
    closeAgentWorkspace();
    // 2. Recargar las bandejas: el ticket desaparecerá de la cola previa
    await loadTickets();
    showToast(`Ticket #${ticketId} derivado exitosamente a ${fullName}. Se removió de la bandeja previa.`, 'success');
  } catch (err) {
    console.error('Error reasignando ticket:', err);
    showToast('Error al reasignar el caso', 'error');
  }
}

"""
    js = js[:start_idx] + new_block + js[end_idx:]
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Reassign and reply block replaced successfully!")
else:
    print(f"Indices error: start_idx={start_idx}, end_idx={end_idx}")
