import re

file_path = 'frontend/js/app.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. bot_quantux emoji removal
content = re.sub(
    r'<option value="bot_quantux">.*?Bot Quantux \(Asistencia Operativa\)</option>',
    r'<option value="bot_quantux">Bot Quantux (Asistencia Operativa)</option>',
    content
)

# 2. calculateTicketSLA emoji removal and parseTicketDate usage
content = re.sub(
    r"const createdAt = ticket\.created_at \? new Date\(ticket\.created_at\) : new Date\(\);",
    r"const createdAt = ticket.created_at ? parseTicketDate(ticket.created_at) : new Date();",
    content
)
content = re.sub(
    r"const resolvedAt = ticket\.updated_at \? new Date\(ticket\.updated_at\) : now;",
    r"const resolvedAt = ticket.updated_at ? parseTicketDate(ticket.updated_at) : now;",
    content
)
content = content.replace("statusText = '⏸️ SLA Pausado';", "statusText = 'SLA Pausado';")

# 3. renderWsWorkflowActions: Inmutabilidad estricta CERRADO
# Search for CERRADO branch in renderWsWorkflowActions
pattern_cerrado = r"(\} else if \(status === 'CERRADO'\) \{\s*actionsHtml \+= `)([\s\S]*?)(`;\s*\} else \{)"
replacement_cerrado = r"""} else if (status === 'CERRADO') {
    actionsHtml += `
      <div style="background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: 8px; padding: 14px 12px; text-align: center;">
        <div style="font-weight: 800; font-size: 11.5px; color: #334155; text-transform: uppercase; letter-spacing: 0.5px;">Registro Cerrado e Inmutable (ITIL)</div>
        <div style="font-size: 11px; color: #64748B; margin-top: 5px; line-height: 1.45;">Conforme a las directivas ITIL v4 de gobernanza, el ciclo de vida de este caso ha finalizado con conformidad. No se admiten modificaciones, reaperturas ni cambios de estado posteriores.</div>
      </div>
    `;
    container.innerHTML = actionsHtml;
    return;
  } else {"""

content = re.sub(pattern_cerrado, replacement_cerrado, content, count=1)

# 4. openAgentWorkspace: toggle ws-reply-container vs ws-closed-immutable-banner
toggle_logic = """
  // Toggle inmutabilidad caso cerrado ITIL (ISSUE-71)
  const elReplyBox = document.getElementById('ws-reply-container');
  const elClosedBanner = document.getElementById('ws-closed-immutable-banner');
  if (ticket.status === 'CERRADO') {
    if (elReplyBox) elReplyBox.style.display = 'none';
    if (elClosedBanner) elClosedBanner.style.display = 'block';
  } else {
    if (elReplyBox) elReplyBox.style.display = 'flex';
    if (elClosedBanner) elClosedBanner.style.display = 'none';
  }

  // 5. Renderizar Secciones Específicas"""

if "ws-closed-immutable-banner" not in content:
    content = content.replace("// 5. Renderizar Secciones Específicas", toggle_logic, 1)

# 5. renderWsMetricsPanel: calculo exacto y visualizacion de tiempo transcurrido
old_metrics_pattern = r"function renderWsMetricsPanel\(ticket\) \{[\s\S]*?const elapsedHours = \(elapsedMinutes / 60\)\.toFixed\(1\);"
new_metrics_code = """function renderWsMetricsPanel(ticket) {
  const container = document.getElementById('ws-metrics-panel-content');
  if (!container) return;

  const sla = calculateTicketSLA(ticket);
  const prio = ticket.priority || 'P3';
  const hoursTarget = prio === 'P1' ? 1 : prio === 'P2' ? 4 : prio === 'P3' ? 24 : 72;
  const isFinished = ticket.status === 'RESUELTO' || ticket.status === 'CERRADO';
  const createdDate = parseTicketDate(ticket.created_at);
  const endDate = isFinished ? parseTicketDate(ticket.updated_at || ticket.resolved_at || ticket.closed_at) : new Date();
  const elapsedMs = Math.max(0, endDate.getTime() - createdDate.getTime());
  const elapsedMinutes = Math.floor(elapsedMs / 60000);
  
  let elapsedFormatted = '';
  if (elapsedMinutes < 60) {
    elapsedFormatted = `${elapsedMinutes} min`;
  } else {
    const hrs = Math.floor(elapsedMinutes / 60);
    const mins = elapsedMinutes % 60;
    elapsedFormatted = mins > 0 ? `${hrs}h ${mins}m` : `${hrs} h`;
  }
  const elapsedSubtext = elapsedMinutes >= 60 ? `(${elapsedMinutes} min totales)` : '';"""

content = re.sub(old_metrics_pattern, new_metrics_code, content, count=1)

# Also update the card display in renderWsMetricsPanel
old_card_pattern = r'<div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">\s*Tiempo Transcurrido</div>[\s\S]*?Desde creaci[oó]n del caso</div>'
new_card_code = """<div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Tiempo Transcurrido</div>
        <div style="font-size: 18px; font-weight: 800; color: #0F172A; margin-top: 4px;">${elapsedFormatted} <span style="font-size: 12px; color: #94A3B8; font-weight: 600;">${elapsedSubtext}</span></div>
        <div style="font-size: 10.5px; color: #64748B; margin-top: 2px;">${isFinished ? 'Duración total del ciclo de atención' : 'Desde creación del caso'}</div>"""

content = re.sub(old_card_pattern, new_card_code, content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully to frontend/js/app.js!")
