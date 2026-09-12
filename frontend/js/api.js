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

  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/`);
      return res.ok;
    } catch {
      return false;
    }
  }
};
