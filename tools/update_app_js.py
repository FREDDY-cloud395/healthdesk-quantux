import os

app_path = os.path.join('frontend', 'js', 'app.js')
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update author setup in openAgentWorkspace
target1 = """  // 4. Avatar del Agente en la caja de respuesta
  const elReplyAvatar = document.getElementById('ws-reply-user-avatar');
  if (elReplyAvatar) {
  const uName = AppState.currentUser ? AppState.currentUser.full_name : 'Agente';
  elReplyAvatar.textContent = getInitials(uName);
  }"""

repl1 = """  // 4. Selector de Identidad y Avatar en la caja de respuesta
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

if target1 in js:
    js = js.replace(target1, repl1, 1)
    print("Update 1: Author setup in openAgentWorkspace OK")
else:
    print("Update 1: target1 NOT FOUND")

# 2. Update renderWsWorkflowActions for selfAssignBtn and resolver button
target2 = """    const isAssignedToMe = AppState.currentUser && (ticket.assignee_username === AppState.currentUser.username);
    const selfAssignBtn = isAssignedToMe
      ? `<button type="button" disabled style="width: 100%; padding: 7px 10px; font-weight: 600; font-size: 11.5px; border-radius: 6px; background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; cursor: not-allowed; display: flex; align-items: center; justify-content: center; gap: 4px;">
           <span>Asignado a mí</span>
         </button>`
      : `<button type="button" onclick="quickSelfAssign('${ticketId}')" style="width: 100%; padding: 7px 10px; font-weight: 600; font-size: 11.5px; border-radius: 6px; background: #FFFFFF; color: #0F172A; border: 1px solid #0F172A; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px;">
           <span>Autoasignar (A mí)</span>
         </button>`;"""

repl2 = """    const isAssignedToMe = AppState.currentUser && (ticket.assignee_username === AppState.currentUser.username);
    const selfAssignBtn = isAssignedToMe
      ? `<button type="button" onclick="openReassignModal('${ticketId}')" style="width: 100%; padding: 7px 10px; font-weight: 600; font-size: 11.5px; border-radius: 6px; background: #F1F5F9; color: #0F172A; border: 1px solid #CBD5E1; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px;" title="Ticket en su bandeja. Clic para derivar a otra mesa o prestador">
           <span>✓ En mi bandeja (Reasignar)</span>
         </button>`
      : `<button type="button" onclick="quickSelfAssign('${ticketId}')" style="width: 100%; padding: 7px 10px; font-weight: 600; font-size: 11.5px; border-radius: 6px; background: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 4px;">
           <span>Asignar a mí</span>
         </button>`;"""

if target2 in js:
    js = js.replace(target2, repl2, 1)
    print("Update 2: Workflow selfAssignBtn OK")
else:
    print("Update 2: target2 NOT FOUND")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Saved updates to app.js")
