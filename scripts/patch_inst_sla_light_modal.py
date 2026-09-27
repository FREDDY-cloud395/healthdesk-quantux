import re
import sys

def patch_app_js():
    path = 'frontend/js/app.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Patch modal header to light palette
    old_header_pattern = re.compile(
        r'// 1\. Header del Modal Estilo Zendesk / Atlassian\s+const headerEl = document\.getElementById\(\'modal-inst-detail-header\'\);.*?headerEl\.innerHTML = `.*?`;\s+}',
        re.DOTALL
    )
    new_header = """// 1. Header del Modal Estilo Zendesk / Atlassian (Paleta Limpia Quantux - Sin Fondos Oscuros)
  const headerEl = document.getElementById('modal-inst-detail-header');
  if (headerEl) {
    headerEl.innerHTML = `
      <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 42px; height: 42px; border-radius: 8px; background: #00A896; color: #FFF; font-weight: 800; font-size: 15px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,168,150,0.25);">
          ${initials}
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <div style="font-size: 11px; color: #0F766E; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
              Centro de Administración / Directorio / Instituciones
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 2px;">
            <h3 style="margin: 0; font-size: 16px; font-weight: 800; color: #0F172A;">
              ${escapeHtml(inst.name)}
            </h3>
            <span style="font-size: 10px; font-weight: 700; background: #CCFBF1; color: #0D9488; border: 1px solid #99F6E4; padding: 2px 7px; border-radius: 4px;">
              ${escapeHtml(inst.code)}
            </span>
          </div>
        </div>
      </div>
      <button type="button" onclick="closeInstitutionDetailModal()" style="background: none; border: none; color: #64748B; font-size: 24px; cursor: pointer; padding: 4px 8px; line-height: 1;" title="Cerrar">&times;</button>
    `;
  }"""

    content, n1 = old_header_pattern.subn(new_header, content)
    print(f"Header replaced: {n1} occurrences")

    # 2. Patch openInstitutionDetailModal to restore saved SLA
    old_sla_init = re.compile(
        r'if \(zdSlaSelect\) zdSlaSelect\.value = inst\.sla_policy \|\| \'SLA Platino VIP - 15m Respuesta\';'
    )
    new_sla_init = """try {
    const savedSla = localStorage.getItem('quantux_sla_' + inst.code);
    if (savedSla) inst.sla_policy = savedSla;
  } catch(e) {}
  if (zdSlaSelect) zdSlaSelect.value = inst.sla_policy || 'SLA Platino VIP - 15m Respuesta';"""
    content, n2 = old_sla_init.subn(new_sla_init, content)
    print(f"SLA init replaced: {n2} occurrences")

    # 3. Patch saveZdOrgSettings to NOT close modal, persist to localStorage, and give button feedback
    old_save_pattern = re.compile(
        r'function saveZdOrgSettings\(\)\s*\{.*?closeInstitutionDetailModal\(\);\s*\}',
        re.DOTALL
    )
    new_save = """function saveZdOrgSettings() {
  const instCode = AppState.activeModalInstCode;
  const inst = (AppState.institutions || []).find(i => i.code === instCode);
  if (!inst) return;

  const nameVal = document.getElementById('zd-org-name')?.value.trim();
  const descVal = document.getElementById('zd-org-desc')?.value.trim();
  const domainsVal = document.getElementById('zd-org-domains')?.value.trim();
  const slaVal = document.getElementById('zd-org-sla')?.value;
  const groupVal = document.getElementById('zd-org-group')?.value;
  const sharedVal = document.getElementById('zd-org-shared-tickets')?.checked;

  if (nameVal) inst.name = nameVal;
  if (descVal !== undefined) inst.description = descVal;
  if (domainsVal !== undefined) inst.domains = domainsVal;
  if (slaVal) {
    inst.sla_policy = slaVal;
    try {
      localStorage.setItem('quantux_sla_' + inst.code, slaVal);
    } catch(e) {}
  }
  if (groupVal) {
    inst.assigned_group = groupVal;
    try {
      localStorage.setItem('quantux_group_' + inst.code, groupVal);
    } catch(e) {}
  }
  if (sharedVal !== undefined) inst.shared_tickets = sharedVal;

  try {
    localStorage.setItem('quantux_institutions_cache', JSON.stringify(AppState.institutions));
  } catch(e) {}

  // Actualizar reactivamente la ficha de la institución en el catálogo y directorio
  renderInstitutionsCatalog();

  // Feedback visual interactivo en el botón de guardar sin cerrar el diálogo
  const btn = (typeof event !== 'undefined' && event && event.currentTarget) ? event.currentTarget : document.querySelector("button[onclick='saveZdOrgSettings()']");
  if (btn) {
    const origHtml = btn.innerHTML;
    const origBg = btn.style.background;
    btn.innerHTML = '<span>✅</span> ¡Configuración de SLA Guardada!';
    btn.style.background = '#0D9488';
    setTimeout(() => {
      btn.innerHTML = origHtml;
      btn.style.background = origBg || '#00A896';
    }, 2500);
  }

  showToast(`Configuración de SLA para "${inst.name}" guardada y reflejada en su ficha.`, 'success');
  // ISSUE-65: Directiva de Producto: NO cerrar la ventana modal
}"""
    content, n3 = old_save_pattern.subn(new_save, content)
    print(f"saveZdOrgSettings replaced: {n3} occurrences")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("frontend/js/app.js patched successfully.")

if __name__ == '__main__':
    patch_app_js()
