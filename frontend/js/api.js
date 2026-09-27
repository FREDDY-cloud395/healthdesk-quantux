/**
 * API Client para HealthDesk Quantux
 * Conexión directa a endpoints FastAPI (/api/v1/...)
 */
const API_BASE = (typeof window !== 'undefined' && window.location && window.location.origin && window.location.origin.startsWith('http')) 
  ? window.location.origin 
  : 'http://127.0.0.1:8000';

const API = {
  // 1. AUTENTICACION Y ROLES
  async login(username, password = "quantux123", selectedRole = null) {
    const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, selected_role: selectedRole })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async switchRole(role) {
    const res = await fetch(`${API_BASE}/api/v1/auth/switch-role/${role}`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 2. TABLAS MAESTRAS
  async getPlatforms() {
    const res = await fetch(`${API_BASE}/api/v1/platforms`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createPlatform(payload) {
    const res = await fetch(`${API_BASE}/api/v1/platforms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getInstitutions() {
    const res = await fetch(`${API_BASE}/api/v1/institutions`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createInstitution(payload) {
    const res = await fetch(`${API_BASE}/api/v1/institutions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async calculatePriority(impact, urgency) {
    const res = await fetch(`${API_BASE}/api/v1/calculate-priority?impact=${encodeURIComponent(impact)}&urgency=${encodeURIComponent(urgency)}`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getOperators() {
    const res = await fetch(`${API_BASE}/api/v1/users/operators`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getUsers() {
    const res = await fetch(`${API_BASE}/api/v1/users`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createUser(payload) {
    const res = await fetch(`${API_BASE}/api/v1/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async updateUser(userId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/users/${userId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async updateUserByUsername(username, payload) {
    const res = await fetch(`${API_BASE}/api/v1/users/by-username/${encodeURIComponent(username)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 3. BANDEJA Y GESTION DE TICKETS
  async getTickets(params = {}) {
    const url = new URL(`${API_BASE}/api/v1/tickets`);
    Object.keys(params).forEach(k => {
      if (params[k]) url.searchParams.append(k, params[k]);
    });
    const res = await fetch(url);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getTicket(ticketId) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}`);
    if (!res.ok) throw await res.json();
    const data = await res.json();
    if (data && data.ticket) {
      return {
        ...data.ticket,
        comments: data.comments || [],
        audit_logs: data.audit_logs || [],
        email_logs: data.email_logs || []
      };
    }
    return data;
  },

  // PASO 1 FSM: REGISTRAR
  async createTicket(payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createIaResolvedTicket(payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/ia-resolved`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // EDICION DE TICKET EN ESTADO NUEVO (UH-11)
  async updateTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // PASO 2 FSM: ASIGNAR
  async assignTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/assign`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // PASO 3 FSM: GESTIONAR ESTADO
  async updateStatus(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // PASO 4 FSM: RESOLVER
  async resolveTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // PASO 5 FSM: CERRAR
  async closeTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/close`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // CAMBIO DE ESTADO (7 ESTADOS ITIL 4 INCLUYENDO ESPERAS Y PAUSA DE SLA)
  async changeTicketStatus(ticketId, status, note = null) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, note })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // CIERRE ESTRUCTURADO KCS v6
  async kcsCloseTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/kcs-close`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // VINCULAR A INCIDENTE MAESTRO (PADRE)
  async linkParentTicket(ticketId, parentTicketId) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/link-parent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ parent_ticket_id: parentTicketId })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // VINCULAR HIJOS A INCIDENTE MAESTRO
  async linkChildrenTickets(ticketId, childTicketIds) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/link-children`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ child_ticket_ids: childTicketIds })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // RESCATE DIRECTO CSAT
  async rescueTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/rescue`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // COMENTARIOS Y NOTAS
  async addComment(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // METRICAS GLOBALES
  async getMetrics(params = {}) {
    const url = new URL(`${API_BASE}/api/v1/tickets/metrics/summary`);
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
        url.searchParams.append(key, params[key]);
      }
    });
    const res = await fetch(url.toString());
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getNotifications(ticketId) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/notifications`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 4. BASE DE CONOCIMIENTO (KNOWLEDGE BASE & HISTÓRICO DE VERSIONES)
  async getArticles(categoryOrParams = 'all', searchParam = '') {
    let category = 'all';
    let search = '';
    if (typeof categoryOrParams === 'object' && categoryOrParams !== null) {
      category = categoryOrParams.category || 'all';
      search = categoryOrParams.search || '';
    } else {
      category = categoryOrParams || 'all';
      search = searchParam || '';
    }

    const url = new URL(`${API_BASE}/api/v1/articles`);
    if (category && category !== 'all') url.searchParams.append('category', category);
    if (search && search.trim()) url.searchParams.append('search', search.trim());
    const res = await fetch(url.toString());
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getArticle(articleId) {
    const res = await fetch(`${API_BASE}/api/v1/articles/${articleId}`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getArticleHistory(articleId) {
    const res = await fetch(`${API_BASE}/api/v1/articles/${articleId}/history`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getCategoriesCount() {
    const res = await fetch(`${API_BASE}/api/v1/articles/categories-count`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getArticleContributingTickets(articleId) {
    const res = await fetch(`${API_BASE}/api/v1/articles/${articleId}/contributing-tickets`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async queryKBCopilot(query, ticketId = null) {
    const res = await fetch(`${API_BASE}/api/v1/articles/copilot-chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, ticket_id: ticketId })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async botAdvanceCycle(count = 3) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/bot/advance-cycle?count=${count}`, {
      method: 'POST'
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async botStepTicket(ticketId) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/bot/step`, {
      method: 'POST'
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async botAdvanceToResolution(ticketId) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/bot/advance-to-resolution`, {
      method: 'POST'
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getTicketKBContribution(ticketId) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/kb-contribution`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createArticle(payload) {
    const res = await fetch(`${API_BASE}/api/v1/articles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async updateArticle(articleId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/articles/${articleId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async promoteTicketToKB(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/articles/from-ticket/${ticketId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async registerArticleView(articleId) {
    try {
      const res = await fetch(`${API_BASE}/api/v1/articles/${articleId}/view`, { method: 'POST' });
      return res.json();
    } catch {
      return null;
    }
  },

  async deleteArticle(articleId) {
    const res = await fetch(`${API_BASE}/api/v1/articles/${articleId}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 4.1 ESCALAMIENTO ITIL (N1 ➔ N2 ➔ N3)
  async escalateTicket(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/escalate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 5. CONFIGURACIÓN DEL SISTEMA & NIVELES DE ATENCIÓN (N1/N2/N3)
  async getConfig() {
    const res = await fetch(`${API_BASE}/api/v1/config`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async updateConfig(payload) {
    const res = await fetch(`${API_BASE}/api/v1/config`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getHelpdeskLevels() {
    const res = await fetch(`${API_BASE}/api/v1/config/levels`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getHelpdeskLevel(levelCode) {
    const res = await fetch(`${API_BASE}/api/v1/config/levels/${levelCode}`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async updateHelpdeskLevel(levelCode, payload) {
    const res = await fetch(`${API_BASE}/api/v1/config/levels/${levelCode}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async addTeamToHelpdeskLevel(levelCode, payload) {
    const res = await fetch(`${API_BASE}/api/v1/config/levels/${levelCode}/teams`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 7. V4.0.0 TEAM LEADER & TORRE DE CONTROL
  async getTeamLeaderOverview() {
    const res = await fetch(`${API_BASE}/api/v1/team-leader/overview`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async reassignTicket(ticketId, assignedToUsername, reason = "Rebalanceo operativo") {
    const res = await fetch(`${API_BASE}/api/v1/team-leader/reassign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ticket_id: ticketId,
        assigned_to_username: assignedToUsername,
        reason: reason
      })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async rebalanceWorkload(analystUsernames, strategy = "even", institutionCode = "all", teamLeaderUsername = "cdaneri") {
    const res = await fetch(`${API_BASE}/api/v1/team-leader/custom-rebalance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        analyst_usernames: analystUsernames,
        strategy: strategy,
        institution_code: institutionCode,
        team_leader_username: teamLeaderUsername
      })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async rescueClient(ticketId, payload) {
    const cleanId = String(ticketId || '').replace(/#/g, '').replace(/%23/g, '').trim();
    const res = await fetch(`${API_BASE}/api/v1/team-leader/rescue/${encodeURIComponent(cleanId)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async autoRebalanceWorkload() {
    const res = await fetch(`${API_BASE}/api/v1/team-leader/auto-rebalance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async stressTestImbalance() {
    const res = await fetch(`${API_BASE}/api/v1/team-leader/stress-test-imbalance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 8. V4.0.0 RELEASES DE SOFTWARE & DESPLIEGUE EN CASCADA
  async getReleases() {
    const res = await fetch(`${API_BASE}/api/v1/releases`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createRelease(payload) {
    const res = await fetch(`${API_BASE}/api/v1/releases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async deployRelease(tag, payload = {}) {
    const res = await fetch(`${API_BASE}/api/v1/releases/${encodeURIComponent(tag)}/deploy`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async updateReleaseStatus(tag, status, updatedBy = 'admin') {
    const res = await fetch(`${API_BASE}/api/v1/releases/${encodeURIComponent(tag)}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 9. V4.0.0 INCIDENTES MAYORES (MAJOR INCIDENT)
  async declareMajorIncident(ticketId, isMajor = true) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/major-incident?is_major=${Boolean(isMajor)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async setMajorIncident(ticketId, isMajor = true) {
    return this.declareMajorIncident(ticketId, isMajor);
  },

  async getActiveMajorIncident() {
    const res = await fetch(`${API_BASE}/api/v1/tickets/major-incidents/active`);
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async linkChildrenTickets(ticketId, childIds, linkedBy = 'soporte') {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/link-children`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ child_ids: childIds, linked_by: linkedBy })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 10. V4.0.0 INGESTA AUTOMÁTICA POR EMAIL & EMAIL THREADING (MÓDULO 9)
  async ingestEmail(payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/email-ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 11. V4.0.0 COPILOT N1 RESOLUTIVO (MÓDULO 13)
  async runCopilotAction(ticketId, actionType, executedBy = 'soporte', parameters = null) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/copilot/auto-fix`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: actionType, executed_by: executedBy, parameters: parameters })
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  // 12. V4.0.0 IA Y AUTOGESTIÓN TÉCNICA (PORTAL SOLICITANTE)
  async aiClassify(payload) {
    const res = await fetch(`${API_BASE}/api/v1/ai/classify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },
  async aiTriage(payload) {
    return this.aiClassify(payload);
  },

  async aiResolveIncident(payload) {
    const res = await fetch(`${API_BASE}/api/v1/ai/resolve-incident`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async aiEscalateIncident(payload) {
    const res = await fetch(`${API_BASE}/api/v1/ai/escalate-incident`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async botTicketInteract(ticketId, payload) {
    const res = await fetch(`${API_BASE}/api/v1/tickets/${ticketId}/bot-interact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      let errMsg = 'Error al interactuar con el bot';
      try { const errData = await res.json(); errMsg = errData.detail || errMsg; } catch(e){}
      throw new Error(errMsg);
    }
    return res.json();
  },

  async uploadFile(file, ticketId = null, uploadedBy = 'soporte') {
    const formData = new FormData();
    formData.append('file', file);
    if (ticketId) formData.append('ticket_id', ticketId);
    if (uploadedBy) formData.append('uploaded_by', uploadedBy);
    const res = await fetch(`${API_BASE}/api/v1/files/upload`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      let errMsg = 'Error al subir el archivo';
      try { const errData = await res.json(); errMsg = errData.detail || errMsg; } catch(e){}
      throw new Error(errMsg);
    }
    return res.json();
  },

  async request(endpoint, options = {}) {
    const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}/api/v1${path}`;
    const headers = options.headers || {};
    if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      let errMsg = `HTTP ${res.status}`;
      try { const errData = await res.json(); errMsg = errData.detail || errMsg; } catch(e){}
      throw new Error(errMsg);
    }
    return res.json();
  },

  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/`);
      return res.ok;
    } catch {
      return false;
    }
  }
};
