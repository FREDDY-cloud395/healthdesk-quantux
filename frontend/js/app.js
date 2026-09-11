/**
 * HealthDesk Quantux — Controlador SPA Integral
 * Menú de Navegación Visual, Tableros de Control y Mesa de Ayuda
 */

// ESTADO GLOBAL DE LA APLICACIÓN
const AppState = {
  currentView: 'dashboard', // 'dashboard' | 'tickets' | 'users' | 'articles' | 'platforms' | 'config'
  currentUser: null, // Null por defecto si no hay sesión autenticada
  platforms: [],
  institutions: [],
  operators: [],
  users: [],
  tickets: [],
  metrics: null,
  selectedTicket: null,
  activeDetailTab: 'comments', // 'comments' | 'notifications' | 'audit'
  ticketFilterPreset: 'all', // 'all' | 'mine' | 'new' | 'in_progress' | 'p1' | 'resolved'
  currentDashInst: '',
  userFilterLevel: 'all',
  helpdeskLevels: []
};

// INICIALIZACIÓN
document.addEventListener('DOMContentLoaded', async () => {
  // 1. Cargar usuario guardado en localStorage si existe, o inicializar sesión por defecto
  try {
    const savedUser = localStorage.getItem('quantux_healthdesk_user');
    if (savedUser) {
      const parsed = JSON.parse(savedUser);
      if (parsed && parsed.username && parsed.role) {
        AppState.currentUser = parsed;
      }
    }
  } catch (e) {
    console.warn('No se pudo recuperar usuario de localStorage:', e);
  }

  // Si no hay usuario en sesión, iniciar por defecto con Freddy Cortés (Admin)
  if (!AppState.currentUser) {
    AppState.currentUser = {
      id: 1,
      username: 'admin',
      full_name: 'Freddy Cortés',
      email: 'fcortes@quantux.salud.ar',
      role: 'ADMIN',
      institution_code: 'OSDE'
    };
    try {
      localStorage.setItem('quantux_healthdesk_user', JSON.stringify(AppState.currentUser));
    } catch (e) {}
  }

  initNavigationHub();
  initResponsiveDrawer();
  initCockpitMobileNav();
  initAuthModalListeners();
  initModalListeners();
  initEditModalListeners();
  initUserModalListeners();
  initArticleModalListeners();
  initEscalateModalListeners();
  initHelpdeskTeamModalListeners();
  initFilterListeners();
  
  updateUserProfileUI();

  await checkApiConnection();
  await loadMasterData();
  await loadUsersList();
  await loadDashboardMetrics();
  switchView('tickets');
});

// =============================================================================
// 1. NAVEGACIÓN PRINCIPAL (HUB TABS & SUB-RIBBON)
// =============================================================================
function initNavigationHub() {
  const tabs = document.querySelectorAll('.nav-hub-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetView = tab.dataset.view;
      switchView(targetView);
    });
  });

  // Botón refrescar dashboard
  const btnRefDash = document.getElementById('btn-refresh-dash');
  if (btnRefDash) {
    btnRefDash.addEventListener('click', async () => {
      const origHtml = btnRefDash.innerHTML;
      btnRefDash.innerHTML = '⏳ Actualizando...';
      const dashInst = document.getElementById('dash-filter-inst');
      const instCode = dashInst ? dashInst.value : '';
      await loadDashboardMetrics(instCode);
      await loadTickets();
      btnRefDash.innerHTML = origHtml;
      showToast('Tablero de control y métricas actualizadas con éxito', 'success');
    });
  }

  // Filtro institucional en dashboard
  const dashInstSelect = document.getElementById('dash-filter-inst');
  if (dashInstSelect) {
    dashInstSelect.addEventListener('change', async () => {
      const instCode = dashInstSelect.value;
      await loadDashboardMetrics(instCode);
    });
  }

  // Botón rápida creación de solicitud en barra superior (UH-05)
  const btnTopNew = document.getElementById('btn-top-new-ticket');
  const modalTicket = document.getElementById('modal-ticket');
  if (btnTopNew && modalTicket) {
    btnTopNew.addEventListener('click', () => {
      resetTicketModalForm();
      modalTicket.classList.add('active');
    });
  }

  // Exportar full DB desde config
  const btnExportDb = document.getElementById('btn-export-full-db');
  if (btnExportDb) {
    btnExportDb.addEventListener('click', () => {
      window.location.href = `${API_BASE}/api/v1/tickets/export/csv`;
    });
  }
}

// CONTROL DEL DRAWER RESPONSIVO Y MENU LATERAL
function initResponsiveDrawer() {
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  const toggleBtn = document.getElementById('btn-sidebar-toggle');
  const closeBtn = document.getElementById('btn-sidebar-close');

  const openDrawer = () => {
    if (sidebar) sidebar.classList.add('open');
    if (backdrop) backdrop.classList.add('active');
  };

  const closeDrawer = () => {
    if (sidebar) sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('active');
  };

  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  // Cerrar drawer al hacer clic en un enlace de navegación en pantallas móviles
  document.querySelectorAll('.nav-hub-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        closeDrawer();
      }
    });
  });
}

// CONTROL DE COLUMNAS COCKPIT EN PANTALLAS MÓVILES
function initCockpitMobileNav() {
  const tabs = document.querySelectorAll('.mobile-cockpit-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetCol = tab.dataset.col;
      switchMobileCockpitTab(targetCol);
    });
  });
}

function switchMobileCockpitTab(colId) {
  document.querySelectorAll('.mobile-cockpit-tab').forEach(t => {
    if (t.dataset.col === colId) {
      t.classList.add('active');
    } else {
      t.classList.remove('active');
    }
  });

  document.querySelectorAll('.cockpit-column').forEach(col => {
    if (col.id === colId) {
      col.classList.add('mobile-active');
    } else {
      col.classList.remove('mobile-active');
    }
  });
}

function switchView(viewName) {
  AppState.currentView = viewName;

  // Actualizar Título y Subtítulo Dinámicos del Topbar
  const titleContainer = document.getElementById('top-view-title');
  const titleEl = document.getElementById('top-view-title-text');
  const subEl = document.getElementById('top-view-subtitle');
  const titles = {
    'dashboard': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
      title: 'Panel de Control y Monitoreo',
      sub: 'Métricas en tiempo real, SLAs y distribución de incidentes'
    },
    'tickets': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>',
      title: 'Mesa de Ayuda',
      sub: 'Bandeja operativa de solicitudes de soporte y seguimiento de SLA'
    },
    'users': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
      title: 'Directorio de Usuarios y Roles',
      sub: 'Gestión de personal operativo y perfiles de acceso (RBAC)'
    },
    'articles': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>',
      title: 'Base de Conocimiento y Procedimientos',
      sub: 'Guías de resolución rápida, contingencias y procedimientos'
    },
    'platforms': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>',
      title: 'Catálogo de Plataformas e Instituciones',
      sub: '9 plataformas de software y 14 clientes institucionales'
    },
    'config': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',
      title: 'Configuración y Auditoría Legal',
      sub: 'Matriz de priorización ITIL, políticas de SLA y bitácora de trazabilidad inmutable'
    }
  };

  if (titles[viewName]) {
    if (titleContainer) {
      titleContainer.innerHTML = `<span style="display:flex; align-items:center; color:var(--q-teal);">${titles[viewName].icon}</span> <span id="top-view-title-text">${titles[viewName].title}</span>`;
    } else if (titleEl) {
      titleEl.textContent = titles[viewName].title;
    }
    if (subEl) subEl.textContent = titles[viewName].sub;
  }

  // Actualizar Enlaces del Sidebar Lateral
  document.querySelectorAll('.nav-hub-tab').forEach(t => {
    if (t.dataset.view === viewName) {
      t.classList.add('active');
    } else {
      t.classList.remove('active');
    }
  });

  // Ocultar todas las secciones y mostrar la activa
  document.querySelectorAll('.app-view').forEach(v => {
    v.classList.remove('active');
  });
  const activeSection = document.getElementById(`view-${viewName}`);
  if (activeSection) {
    activeSection.classList.add('active');
  }

  // Actualizar Título Dinámico Superior (Estilo OSDE PAU)
  const viewTitles = {
    'tickets': AppState.selectedTicket ? `SOLICITUD #${AppState.selectedTicket.id}` : 'SOLICITUDES',
    'dashboard': 'TABLERO DE CONTROL',
    'users': 'DIRECTORIO DE USUARIOS',
    'articles': 'BASE DE CONOCIMIENTO',
    'platforms': 'PLATAFORMAS & CLIENTES',
    'config': 'CONFIGURACIÓN DEL SISTEMA'
  };
  const topTitle = document.getElementById('top-view-title-text');
  if (topTitle && viewTitles[viewName]) {
    topTitle.textContent = viewTitles[viewName];
  }

  // Control de visibilidad de las herramientas superiores según la vista
  const searchBox = document.getElementById('ribbon-search-box');
  const btnCsv = document.getElementById('btn-export-csv');
  const btnRefresh = document.getElementById('btn-refresh');

  if (viewName === 'tickets') {
    if (searchBox) searchBox.style.display = 'block';
    if (btnCsv) btnCsv.style.display = 'inline-flex';
    if (btnRefresh) btnRefresh.style.display = 'inline-flex';
  } else {
    if (searchBox) searchBox.style.display = 'block';
    if (btnCsv) btnCsv.style.display = 'none';
    if (btnRefresh) btnRefresh.style.display = 'none';
  }

  // Renderizar Sub-Ribbon Contextual
  renderSubNavRibbon(viewName);

  // Acciones por Vista
  if (viewName === 'dashboard') {
    const dashInst = document.getElementById('dash-filter-inst');
    const instCode = dashInst ? dashInst.value : '';
    loadDashboardMetrics(instCode);
  } else if (viewName === 'tickets') {
    loadTickets();
  } else if (viewName === 'users') {
    loadUsersList();
  } else if (viewName === 'articles') {
    loadKnowledgeBase();
  } else if (viewName === 'platforms') {
    renderPlatformsCatalog();
  } else if (viewName === 'config') {
    loadSystemConfig();
    loadHelpdeskLevelsConfig();
  }
}

function renderSubNavRibbon(viewName) {
  const container = document.getElementById('sub-nav-pills-container');
  if (!container) return;

  if (viewName === 'dashboard') {
    container.innerHTML = `
      <button class="pill-filter-btn active" onclick="switchView('dashboard')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
        <span>Resumen Ejecutivo</span>
      </button>
      <button class="pill-filter-btn" onclick="scrollToSection('table-active-sla')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <span>Monitoreo Incidentes Críticos</span>
      </button>
      <button class="pill-filter-btn" onclick="scrollToSection('chart-bars-platforms')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
        <span>Por Plataforma</span>
      </button>
      <button class="pill-filter-btn" onclick="scrollToSection('chart-bars-institutions')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M3 21h18M3 7v14M21 7v14M9 21V11h6v10M9 3l3-2 3 2v4H9V3z"></path></svg>
        <span>Por Institución</span>
      </button>
      <button class="pill-filter-btn" onclick="scrollToSection('feed-audit-logs')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        <span>Auditoría Legal</span>
      </button>
    `;
  } else if (viewName === 'tickets') {
    const preset = AppState.ticketFilterPreset || 'all';
    const isReq = AppState.currentUser && AppState.currentUser.role === 'SOLICITANTE';
    const mineLabel = isReq ? '👤 Mis Solicitudes' : '👤 Asignados a Mí';

    container.innerHTML = `
      <button class="pill-filter-btn ${preset === 'all' ? 'active' : ''}" onclick="applyTicketPreset('all')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
        <span>Todas</span>
      </button>
      <button class="pill-filter-btn ${preset === 'mine' ? 'active' : ''}" onclick="applyTicketPreset('mine')" style="${preset === 'mine' ? 'background:var(--q-primary); color:#FFF; font-weight:800;' : 'background:rgba(37,99,235,0.08); color:var(--q-primary); font-weight:700; border-color:rgba(37,99,235,0.2);'}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <span>${mineLabel}</span>
      </button>
      <button class="pill-filter-btn ${preset === 'new' ? 'active' : ''}" onclick="applyTicketPreset('new')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
        <span>Sin Asignar</span>
      </button>
      <button class="pill-filter-btn ${preset === 'in_progress' ? 'active' : ''}" onclick="applyTicketPreset('in_progress')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        <span>En Diagnóstico</span>
      </button>
      <!-- FILTROS DIRECTOS POR PRIORIDAD ITIL -->
      <button class="pill-filter-btn ${preset === 'p1' ? 'active' : ''}" onclick="applyTicketPreset('p1')" title="Prioridad Crítica (SLA 2h)" style="${preset === 'p1' ? 'background:#DC2626; color:#FFF; border-color:#DC2626; font-weight:800;' : 'background:rgba(239,68,68,0.08); border-color:#FCA5A5; color:#DC2626;'}">
        <span>🚨 P1 Crítico</span>
      </button>
      <button class="pill-filter-btn ${preset === 'p2' ? 'active' : ''}" onclick="applyTicketPreset('p2')" title="Prioridad Alta (SLA 8h)" style="${preset === 'p2' ? 'background:#D97706; color:#FFF; border-color:#D97706; font-weight:800;' : 'background:rgba(217,119,6,0.08); border-color:#FDE68A; color:#D97706;'}">
        <span>⚠️ P2 Alta</span>
      </button>
      <button class="pill-filter-btn ${preset === 'p3' ? 'active' : ''}" onclick="applyTicketPreset('p3')" title="Prioridad Media (SLA 24h)" style="${preset === 'p3' ? 'background:#2563EB; color:#FFF; border-color:#2563EB; font-weight:800;' : 'background:rgba(37,99,235,0.08); border-color:#BFDBFE; color:#2563EB;'}">
        <span>🔷 P3 Media</span>
      </button>
      <button class="pill-filter-btn ${preset === 'p4' ? 'active' : ''}" onclick="applyTicketPreset('p4')" title="Prioridad Baja (SLA 48h)" style="${preset === 'p4' ? 'background:#475569; color:#FFF; border-color:#475569; font-weight:800;' : 'background:#F1F5F9; border-color:#CBD5E1; color:#475569;'}">
        <span>⚪ P4 Baja</span>
      </button>
      <button class="pill-filter-btn ${preset === 'p5' ? 'active' : ''}" onclick="applyTicketPreset('p5')" title="Prioridad Planificada (SLA 72h)" style="${preset === 'p5' ? 'background:#64748B; color:#FFF; border-color:#64748B; font-weight:800;' : 'background:#F8FAFC; border-color:#E2E8F0; color:#64748B;'}">
        <span>📅 P5 Planif.</span>
      </button>
      <button class="pill-filter-btn ${preset === 'resolved' ? 'active' : ''}" onclick="applyTicketPreset('resolved')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <span>Resueltos</span>
      </button>
      <button class="pill-filter-btn ${preset === 'closed' ? 'active' : ''}" onclick="applyTicketPreset('closed')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
        <span>Cerrados</span>
      </button>
    `;
  } else if (viewName === 'users') {
    container.innerHTML = `
      <button class="pill-filter-btn active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        <span>Directorio de Usuarios</span>
      </button>
      <button class="pill-filter-btn" onclick="document.getElementById('btn-open-user-modal').click()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px;"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>➕ Dar de Alta Usuario</span>
      </button>
    `;
  } else if (viewName === 'articles') {
    container.innerHTML = `
      <button class="pill-filter-btn active" onclick="filterKBCategory('')">
        <span>📚 Todos los Protocolos</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('CLINICO')">
        <span>🩺 Asistencial / Clínico</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('DIAGNOSTICO')">
        <span>🔬 Diagnóstico y LIS</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('FARMACIA')">
        <span>💊 Farmacia y Recetas</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('CONTINGENCIA')">
        <span>🚨 Contingencia Crítica</span>
      </button>
    `;
  } else if (viewName === 'platforms') {
    container.innerHTML = `
      <button class="pill-filter-btn active">
        <span>🏥 Configuración Multi-Institucional</span>
      </button>
      <button class="pill-filter-btn" onclick="showToast('Para asignar plataformas, seleccione la institución y active los interruptores correspondientes', 'info')">
        <span>⚙️ Mesas de Ayuda y Plataformas Activas</span>
      </button>
    `;
  } else if (viewName === 'config') {
    container.innerHTML = `
      <button class="pill-filter-btn active">
        <span>⚙️ Parámetros Globales de Servicio y SLA</span>
      </button>
    `;
  }
}

function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// =============================================================================
// 2. GESTIÓN DE SESIÓN, USUARIOS Y AUTENTICACIÓN
// =============================================================================
function setCurrentUser(userData) {
  if (!userData) return;
  AppState.currentUser = {
    id: userData.user_id || userData.id || 1,
    username: userData.username,
    full_name: userData.full_name,
    email: userData.email || '',
    role: userData.role
  };
  try {
    localStorage.setItem('quantux_healthdesk_user', JSON.stringify(AppState.currentUser));
  } catch (e) {}

  updateUserProfileUI();
}

function openAuthModal(isGate = false) {
  const modal = document.getElementById('modal-auth-login');
  if (!modal) return;
  
  populateAuthModalAccounts();
  
  const closeBtn = document.getElementById('modal-auth-login-close');
  const cancelBtn = document.getElementById('btn-cancel-auth-login');
  const errorMsg = document.getElementById('login-error-msg');
  const modalTitle = document.getElementById('auth-modal-title');
  const modalSubtitle = document.getElementById('auth-modal-subtitle');
  
  if (errorMsg) errorMsg.style.display = 'none';

  if (isGate || !AppState.currentUser) {
    modal.classList.add('auth-gate-mode');
    if (closeBtn) closeBtn.style.display = 'none';
    if (cancelBtn) cancelBtn.style.display = 'none';
    if (modalTitle) modalTitle.textContent = 'Control de Acceso • HealthDesk Quantux';
    if (modalSubtitle) modalSubtitle.textContent = 'Autenticación requerida para acceder al sistema asistencial.';
  } else {
    modal.classList.remove('auth-gate-mode');
    if (closeBtn) closeBtn.style.display = 'inline-block';
    if (cancelBtn) cancelBtn.style.display = 'inline-block';
    if (modalTitle) modalTitle.textContent = 'Cambiar de Usuario / Selector de Cuenta';
    if (modalSubtitle) modalSubtitle.textContent = 'Seleccione una cuenta para alternar de perfil operativo.';
  }

  modal.classList.add('active');
  const userInput = document.getElementById('login-username-input');
  if (userInput && !AppState.currentUser) {
    userInput.focus();
  }
}

function closeAuthModal() {
  const modal = document.getElementById('modal-auth-login');
  if (!modal) return;
  // No permitir cerrar si no hay sesión activa
  if (!AppState.currentUser) {
    showToast('Debe ingresar sus credenciales para acceder al sistema', 'info');
    return;
  }
  modal.classList.remove('active');
  modal.classList.remove('auth-gate-mode');
}

function handleLogout() {
  AppState.currentUser = null;
  AppState.selectedTicket = null;
  try {
    localStorage.removeItem('quantux_healthdesk_user');
  } catch (e) {}

  updateUserProfileUI();
  
  // Limpiar panel de tickets
  const detailCont = document.getElementById('ticket-detail-container');
  if (detailCont) {
    detailCont.innerHTML = `
      <div class="empty-detail-state" style="padding: 40px 20px; text-align: center; color: #64748B;">
        <div style="font-size: 36px; margin-bottom: 12px;">🔒</div>
        <h3 style="font-size: 15px; color: #0F172A; font-weight: 700; margin-bottom: 6px;">Sesión Finalizada</h3>
        <p style="font-size: 12px; max-width: 320px; margin: 0 auto;">Inicie sesión con sus credenciales institucionales para visualizar y gestionar las solicitudes de asistencia técnica.</p>
      </div>
    `;
  }

  showToast('Has cerrado sesión correctamente.', 'info');
  openAuthModal(true);
}

function initAuthModalListeners() {
  const modal = document.getElementById('modal-auth-login');
  const btnSidebarProfile = document.getElementById('btn-sidebar-user-profile');
  const btnSidebarLogout = document.getElementById('btn-sidebar-logout');
  const btnTopSwitchUser = document.getElementById('btn-top-switch-user');
  const btnClose = document.getElementById('modal-auth-login-close');
  const btnCancel = document.getElementById('btn-cancel-auth-login');
  const form = document.getElementById('form-auth-login');
  const inputUser = document.getElementById('login-username-input');
  const inputPassword = document.getElementById('login-password-input');

  if (btnSidebarProfile) {
    btnSidebarProfile.addEventListener('click', () => {
      if (AppState.currentUser) {
        openAuthModal(false);
      } else {
        openAuthModal(true);
      }
    });
  }

  if (btnSidebarLogout) {
    btnSidebarLogout.addEventListener('click', (e) => {
      e.stopPropagation();
      handleLogout();
    });
  }

  if (btnTopSwitchUser) {
    btnTopSwitchUser.addEventListener('click', () => {
      if (AppState.currentUser) {
        handleLogout();
      } else {
        openAuthModal(true);
      }
    });
  }

  if (btnClose) btnClose.addEventListener('click', closeAuthModal);
  if (btnCancel) btnCancel.addEventListener('click', closeAuthModal);

  // Evitar cerrar modal haciendo clic en backdrop si no hay sesión activa
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal && AppState.currentUser) {
        closeAuthModal();
      }
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const uname = inputUser ? inputUser.value.trim() : '';
      const pwd = inputPassword ? inputPassword.value : '';
      if (!uname) {
        showToast('Por favor ingrese un nombre de usuario', 'error');
        return;
      }
      await loginAsUser(uname, pwd);
    });
  }
}

async function loginAsUser(username, password = null, role = null) {
  const errorMsg = document.getElementById('login-error-msg');
  if (errorMsg) errorMsg.style.display = 'none';

  const pwdInput = document.getElementById('login-password-input');
  const pwd = (password !== null && password !== undefined && password !== '') ? password : (pwdInput ? pwdInput.value : 'quantux123');

  try {
    const res = await API.login(username, pwd, role);
    setCurrentUser(res);
    showToast(`✅ Acceso concedido: ${res.full_name} (${res.role})`, 'success');
    
    const modal = document.getElementById('modal-auth-login');
    if (modal) {
      modal.classList.remove('active');
      modal.classList.remove('auth-gate-mode');
    }

    await loadMasterData();
    await loadDashboardMetrics(AppState.currentDashInst);
    await loadTickets();
    await loadUsersList();
    
    if (AppState.currentView === 'tickets') {
      renderTicketList(AppState.tickets);
    }
  } catch (err) {
    console.error('Error al iniciar sesión:', err);
    const detail = (err && err.detail) || 'Credenciales inválidas: usuario no encontrado o contraseña incorrecta.';
    if (errorMsg) {
      errorMsg.textContent = `❌ ${detail}`;
      errorMsg.style.display = 'block';
    }
    showToast(detail, 'error');
  }
}

function populateAuthModalAccounts() {
  const container = document.getElementById('quick-login-accounts-list');
  if (!container) return;

  const users = (AppState.users && AppState.users.length > 0) ? AppState.users : [
    { username: 'admin', full_name: 'Freddy Cortés (Admin General)', role: 'ADMIN', institution_code: 'OSDE' },
    { username: 'soporte', full_name: 'Laura Benítez (Soporte N2)', role: 'SOPORTE', institution_code: 'OSDE' },
    { username: 'solicitante', full_name: 'Lic. Martín Gómez (Solicitante)', role: 'SOLICITANTE', institution_code: 'SWISS_MEDICAL' }
  ];

  container.innerHTML = users.map(u => {
    const isCurrent = AppState.currentUser && AppState.currentUser.username === u.username;
    const roleBadgeClass = u.role === 'ADMIN' ? 'badge-role-admin' : (u.role.includes('SOPORTE') || u.role === 'SOPORTE' ? 'badge-role-soporte' : 'badge-role-solicitante');
    const initials = (u.full_name || u.username).split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

    return `
      <div class="quick-login-item ${isCurrent ? 'active-user' : ''}" onclick="selectQuickUser('${u.username}')">
        <div class="quick-login-left">
          <div class="user-avatar-sm" style="width: 28px; height: 28px; font-size: 10px; font-weight: 800;">${initials}</div>
          <div class="quick-login-info">
            <span class="quick-login-name">${u.full_name} ${isCurrent ? '<strong style="color:#10B981; font-size:10px;">(Activo)</strong>' : ''}</span>
            <span class="quick-login-meta">@${u.username} • ${formatInstitutionName(u.institution_code)}</span>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <span class="quick-login-badge ${roleBadgeClass}">${u.role}</span>
          <button type="button" class="btn-sec btn-sm" onclick="event.stopPropagation(); loginAsUser('${u.username}', 'quantux123')" style="font-size:10px; padding:3px 8px; font-weight:700;">Ingresar</button>
        </div>
      </div>
    `;
  }).join('');
}

function selectQuickUser(username) {
  const inputUser = document.getElementById('login-username-input');
  const inputPassword = document.getElementById('login-password-input');
  if (inputUser) inputUser.value = username;
  if (inputPassword && !inputPassword.value) inputPassword.value = 'quantux123';
}

async function fillLoginForm(username, password = 'quantux123', autoSubmit = true) {
  const inputUser = document.getElementById('login-username-input');
  const inputPassword = document.getElementById('login-password-input');
  if (inputUser) inputUser.value = username;
  if (inputPassword) inputPassword.value = password;
  
  if (autoSubmit) {
    await loginAsUser(username, password);
  }
}

function togglePasswordVisibility() {
  const pwdInput = document.getElementById('login-password-input');
  const btn = document.getElementById('btn-toggle-pwd');
  if (!pwdInput) return;
  if (pwdInput.type === 'password') {
    pwdInput.type = 'text';
    if (btn) btn.textContent = '🙈';
  } else {
    pwdInput.type = 'password';
    if (btn) btn.textContent = '👁️';
  }
}

function openNewTicketModal() {
  resetTicketModalForm();
  const modal = document.getElementById('modal-ticket');
  if (modal) {
    modal.classList.add('active');
  }
}

function updateUserProfileUI() {
  const topUser = document.getElementById('top-username');
  const topRole = document.getElementById('top-role-badge');
  const topAvatar = document.getElementById('top-user-avatar');
  const profName = document.getElementById('profile-full-name');
  const profRole = document.getElementById('profile-role-sub');
  const profAvatar = document.getElementById('profile-avatar');
  const currUserName = document.getElementById('current-user-name');
  const currUserRole = document.getElementById('current-user-role');
  const currUserAvatar = document.getElementById('current-user-avatar');
  const topSwitchText = document.querySelector('#btn-top-switch-user .role-btn-text');

  if (!AppState.currentUser) {
    if (topUser) topUser.textContent = 'Sin Sesión';
    if (topRole) {
      topRole.textContent = 'BLOQUEADO';
      topRole.style.background = '#64748B';
    }
    if (topAvatar) topAvatar.textContent = '🔒';
    if (profName) profName.textContent = 'Sesión Cerrada';
    if (profRole) profRole.textContent = 'Haga clic para ingresar';
    if (profAvatar) profAvatar.textContent = '🔒';
    if (currUserName) currUserName.textContent = 'Invitado';
    if (currUserRole) currUserRole.textContent = 'Sin acceso';
    if (currUserAvatar) currUserAvatar.textContent = '🔒';
    if (topSwitchText) topSwitchText.textContent = 'Iniciar Sesión';
    return;
  }

  const initials = (AppState.currentUser.full_name || AppState.currentUser.username)
    .split(' ')
    .map(n => n[0])
    .join('')
    .substring(0, 2)
    .toUpperCase();

  if (topUser) topUser.textContent = AppState.currentUser.full_name || AppState.currentUser.username;
  if (topRole) {
    topRole.textContent = AppState.currentUser.role;
    topRole.style.background = '#0284C7';
  }
  if (topAvatar) topAvatar.textContent = initials;
  if (profName) profName.textContent = AppState.currentUser.full_name;
  if (profRole) profRole.textContent = `ROL: ${AppState.currentUser.role}`;
  if (profAvatar) profAvatar.textContent = initials;
  if (currUserName) currUserName.textContent = AppState.currentUser.full_name;
  if (currUserRole) currUserRole.textContent = `Rol: ${AppState.currentUser.role}`;
  if (currUserAvatar) currUserAvatar.textContent = initials;
  if (topSwitchText) topSwitchText.textContent = 'Cerrar Sesión';
}

// =============================================================================
// 3. TABLEROS DE SEGUIMIENTO Y CONTROL (DASHBOARD ANALYTICS)
// =============================================================================
async function loadDashboardMetrics(institutionCode = '') {
  try {
    const params = institutionCode ? { institution_code: institutionCode } : {};
    const data = await API.getMetrics(params);
    AppState.metrics = data;
    AppState.currentDashInst = institutionCode;
    renderDashboard(institutionCode);
  } catch (err) {
    console.error('Error cargando métricas:', err);
  }
}

function renderDashboard(selectedInst = '') {
  if (!AppState.metrics) return;
  const m = AppState.metrics;
  const currentInst = selectedInst || AppState.currentDashInst || (document.getElementById('dash-filter-inst') ? document.getElementById('dash-filter-inst').value : '');

  // 1. KPI Cards
  const kpiTotal = document.getElementById('kpi-total-tickets');
  const kpiP1 = document.getElementById('kpi-p1-tickets');
  const kpiActive = document.getElementById('kpi-active-tickets');
  const kpiSla = document.getElementById('kpi-sla-rate');
  const kpiConf = document.getElementById('kpi-conformity-rate');
  const kpiResolved = document.getElementById('kpi-resolved-tickets');
  const ribbonP1 = document.getElementById('ribbon-p1-count');

  if (kpiTotal) kpiTotal.textContent = m.total_tickets || 0;
  if (kpiP1) kpiP1.textContent = m.p1_critical_tickets || 0;
  if (ribbonP1) ribbonP1.textContent = m.p1_critical_tickets || 0;
  if (kpiActive) kpiActive.textContent = m.active_tickets || 0;
  if (kpiSla) kpiSla.textContent = `${m.sla_compliance_pct || 98.4}%`;
  if (kpiConf) kpiConf.textContent = `${m.conformity_rate || 96.2}%`;
  if (kpiResolved) kpiResolved.textContent = (m.resolved_tickets + m.closed_tickets) || 0;

  // 2. Gráfico 1: Barras de Estado
  const statusCont = document.getElementById('chart-bars-status');
  if (statusCont && m.by_status) {
    const total = m.total_tickets || 1;
    const statusMap = [
      { key: 'NUEVO', label: 'Nuevos (Sin Asignar)', color: '#3B82F6' },
      { key: 'ASIGNADO', label: 'Asignados a Especialista', color: '#F59E0B' },
      { key: 'EN_CURSO', label: 'En Diagnóstico / Trabajo', color: '#0284C7' },
      { key: 'RESUELTO', label: 'Solucionados (Espera Cierre)', color: '#10B981' },
      { key: 'CERRADO', label: 'Cerrados con Conformidad', color: '#64748B' }
    ];

    statusCont.innerHTML = statusMap.map(st => {
      const count = m.by_status[st.key] || 0;
      const pct = total > 0 ? Math.round((count / total) * 100) : 0;
      return `
        <div class="bar-row">
          <div class="bar-row-info">
            <span>${st.label}</span>
            <span style="color: ${st.color}; font-weight:700;">${count} (${pct}%)</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${pct}%; background-color: ${st.color};"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  // 3. Gráfico 2: Plataformas Asistenciales
  const platCont = document.getElementById('chart-bars-platforms');
  if (platCont && m.by_platform) {
    const total = m.total_tickets || 1;
    const sortedPlats = Object.entries(m.by_platform).sort((a, b) => b[1] - a[1]);
    
    if (sortedPlats.length === 0) {
      platCont.innerHTML = '<div style="color:#94A3B8; font-size:11px; padding:8px;">Sin solicitudes registradas para esta sede.</div>';
    } else {
      platCont.innerHTML = sortedPlats.slice(0, 5).map(([plat, count]) => {
        const pct = total > 0 ? Math.round((count / total) * 100) : 0;
        const platName = formatPlatformName(plat);
        return `
          <div class="bar-row">
            <div class="bar-row-info">
              <span>🩺 ${platName}</span>
              <span style="font-weight:700; color:var(--q-teal-dark);">${count} solicitudes</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width: ${pct}%; background: linear-gradient(90deg, #00A896, #00E5CC);"></div>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // 4. Gráfico 3: Instituciones de Salud
  const instCont = document.getElementById('chart-bars-institutions');
  if (instCont && m.by_institution) {
    const total = m.total_tickets || 1;
    const sortedInst = Object.entries(m.by_institution).sort((a, b) => b[1] - a[1]);
    
    if (sortedInst.length === 0) {
      instCont.innerHTML = '<div style="color:#94A3B8; font-size:11px; padding:8px;">Sin registros para el filtro seleccionado.</div>';
    } else {
      instCont.innerHTML = sortedInst.slice(0, 5).map(([inst, count]) => {
        const pct = total > 0 ? Math.round((count / total) * 100) : 0;
        const instName = formatInstitutionName(inst);
        const isSelected = currentInst && currentInst === inst;
        return `
          <div class="bar-row" style="${isSelected ? 'background:rgba(59,130,246,0.08); padding:2px 4px; border-radius:4px;' : ''}">
            <div class="bar-row-info">
              <span>🏥 ${instName} ${isSelected ? '<strong>(Filtro Activo)</strong>' : ''}</span>
              <span style="font-weight:700; color:#1E3A8A;">${count} casos</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width: ${pct}%; background: linear-gradient(90deg, #3B82F6, #60A5FA);"></div>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // 5. Gráfico 4: Matriz de Prioridad (P1 a P5)
  const prioCont = document.getElementById('chart-bars-priorities');
  if (prioCont && m.by_priority) {
    const total = m.total_tickets || 1;
    const prioMap = [
      { key: 'P1', label: 'P1 - Crítica (Incidentes Críticos / Quirófano)', color: '#EF4444' },
      { key: 'P2', label: 'P2 - Alta (Severa con contingencia)', color: '#F59E0B' },
      { key: 'P3', label: 'P3 - Media (Puntual en puesto)', color: '#3B82F6' },
      { key: 'P4', label: 'P4 - Baja (Consultas de uso)', color: '#64748B' },
      { key: 'P5', label: 'P5 - Planificada / Accesos', color: '#94A3B8' }
    ];

    prioCont.innerHTML = prioMap.map(pr => {
      const count = m.by_priority[pr.key] || 0;
      const pct = total > 0 ? Math.round((count / total) * 100) : 0;
      return `
        <div class="bar-row">
          <div class="bar-row-info">
            <span>${pr.label}</span>
            <span style="color: ${pr.color}; font-weight:700;">${count} (${pct}%)</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${pct}%; background-color: ${pr.color};"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  // 6. Tabla de Monitor de Casos Activos con SLA
  const tbodySla = document.getElementById('tbody-active-sla');
  if (tbodySla && AppState.tickets) {
    const activeTickets = AppState.tickets
      .filter(t => t.status !== 'CERRADO' && (!currentInst || t.institution_code === currentInst))
      .slice(0, 6);

    if (activeTickets.length === 0) {
      tbodySla.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#94A3B8; padding:12px;">No hay casos pendientes para la institución seleccionada.</td></tr>';
    } else {
      tbodySla.innerHTML = activeTickets.map(t => {
        const pClass = `badge-${t.priority.toLowerCase()}`;
        return `
          <tr>
            <td><strong style="font-family:'JetBrains Mono'; font-size:11px;">${t.id}</strong></td>
            <td><span class="badge-prio ${pClass}">${t.priority}</span></td>
            <td><div style="font-weight:600; max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${t.title}</div></td>
            <td><span style="font-size:10px; color:#475569;">${formatPlatformName(t.platform_code)}</span></td>
            <td><span style="font-size:10.5px; font-weight:600;">${t.assignee_username || '<em style="color:#F59E0B;">Sin Asignar</em>'}</span></td>
            <td>
              <button class="sub-pill-btn active" style="padding:2px 8px; font-size:10px; background:var(--q-teal);" onclick="openTicketInCockpit('${t.id}')">
                Ver Caso ➔
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  // 7. Feed de Auditoría Inmutable
  const auditFeed = document.getElementById('feed-audit-logs');
  if (auditFeed && m.recent_audit) {
    if (m.recent_audit.length === 0) {
      auditFeed.innerHTML = '<div style="color:#94A3B8; font-size:11px; padding:8px;">Sin actividad reciente para el filtro seleccionado.</div>';
    } else {
      auditFeed.innerHTML = m.recent_audit.slice(0, 6).map(log => {
        return `
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:6px 10px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <strong style="color:var(--q-navy); font-family:'JetBrains Mono'; font-size:10.5px;">[${log.ticket_id}]</strong> 
              <span style="color:#475569;">${log.reason}</span>
            </div>
            <div style="font-size:9.5px; color:#94A3B8; font-weight:600;">
              👤 ${log.changed_by} • ${log.time}
            </div>
          </div>
        `;
      }).join('');
    }
  }
}

function openTicketInCockpit(ticketId) {
  switchView('tickets');
  selectTicket(ticketId, true);
}

// =============================================================================
// 4. MESA DE AYUDA OPERATIVA (COCKPIT EN 3 COLUMNAS REAIS - UH-28)
// =============================================================================
async function loadTickets(params = {}) {
  try {
    const tickets = await API.getTickets(params);
    AppState.tickets = tickets;
    renderTicketList();
    
    // Actualizar contadores de presets si es consulta general
    if (Object.keys(params).length === 0) {
      updatePresetCounts(tickets);
    }
    
    // Si hay un ticket seleccionado, refrescarlo
    if (AppState.selectedTicket) {
      const refreshed = tickets.find(t => t.id === AppState.selectedTicket.id);
      if (refreshed) {
        AppState.selectedTicket = refreshed;
        renderTicketDetail(refreshed);
      } else if (tickets.length > 0) {
        selectTicket(tickets[0].id, false);
      }
    } else if (tickets.length > 0) {
      selectTicket(tickets[0].id, false);
    } else {
      const container = document.getElementById('ticket-detail-container');
      if (container) {
        container.innerHTML = `
          <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color:#94A3B8; text-align:center; padding:40px 20px;">
            <div style="font-size:40px; margin-bottom:12px;">📋</div>
            <h3 style="font-size:15px; font-weight:700; color:#64748B;">Ningún ticket seleccionado</h3>
            <p style="font-size:12px; max-width:320px; margin-top:6px;">Seleccione una solicitud de la bandeja para ver su detalle integral, gestión FSM y bitácora de trazabilidad.</p>
          </div>
        `;
      }
    }
    
    // Actualizar badges de conteo
    const badge = document.getElementById('ticket-count-badge');
    const sideBadge = document.getElementById('sidebar-ticket-count');
    if (badge) badge.textContent = tickets.length;
    if (sideBadge) sideBadge.textContent = tickets.length;
  } catch (err) {
    console.error('Error cargando tickets:', err);
  }
}

function updatePresetCounts(tickets) {
  if (!tickets) return;
  const cAll = tickets.length;
  const cNew = tickets.filter(t => t.status === 'NUEVO').length;
  const cProg = tickets.filter(t => t.status === 'EN_CURSO' || t.status === 'ASIGNADO').length;
  const cP1 = tickets.filter(t => t.priority === 'P1').length;
  const cRes = tickets.filter(t => t.status === 'RESUELTO').length;
  const cCls = tickets.filter(t => t.status === 'CERRADO').length;

  const elAll = document.getElementById('preset-count-all');
  const elNew = document.getElementById('preset-count-new');
  const elProg = document.getElementById('preset-count-prog');
  const elP1 = document.getElementById('preset-count-p1');
  const elRes = document.getElementById('preset-count-res');
  const elCls = document.getElementById('preset-count-cls');

  if (elAll) elAll.textContent = cAll;
  if (elNew) elNew.textContent = cNew;
  if (elProg) elProg.textContent = cProg;
  if (elP1) elP1.textContent = cP1;
  if (elRes) elRes.textContent = cRes;
  if (elCls) elCls.textContent = cCls;
}

function calculateTicketSLA(ticket) {
  const prio = (ticket.priority || 'P3').toUpperCase();
  const slaHoursMap = { 'P1': 2, 'P2': 8, 'P3': 24, 'P4': 48, 'P5': 72 };
  const maxHours = slaHoursMap[prio] || 24;

  const createdAt = ticket.created_at ? new Date(ticket.created_at) : new Date();
  const deadline = new Date(createdAt.getTime() + maxHours * 60 * 60 * 1000);
  const now = new Date();

  const isCompleted = ticket.status === 'RESUELTO' || ticket.status === 'CERRADO';
  const resolvedAt = ticket.updated_at ? new Date(ticket.updated_at) : now;

  let status = 'ON_TIME';
  let statusText = 'En Tiempo';
  let badgeColor = '#059669';
  let badgeBg = '#ECFDF5';
  let percent = 0;
  let timeRemainingText = '';

  const totalDuration = maxHours * 60 * 60 * 1000;
  const elapsed = (isCompleted ? resolvedAt : now).getTime() - createdAt.getTime();
  percent = Math.min(100, Math.max(0, Math.round((elapsed / totalDuration) * 100)));

  if (isCompleted) {
    if (elapsed <= totalDuration) {
      status = 'MET';
      statusText = 'Cumplido';
      badgeColor = '#059669';
      badgeBg = '#D1FAE5';
      timeRemainingText = `Cumplido en ${Math.max(1, Math.round(elapsed / (1000 * 60)))} min`;
    } else {
      status = 'BREACHED';
      statusText = 'Incumplido';
      badgeColor = '#DC2626';
      badgeBg = '#FEE2E2';
      timeRemainingText = `Fuera de tiempo (+${Math.round((elapsed - totalDuration) / (1000 * 60 * 60))}h)`;
    }
  } else {
    const remainingMs = deadline.getTime() - now.getTime();
    if (remainingMs <= 0) {
      status = 'BREACHED';
      statusText = 'Vencido';
      badgeColor = '#DC2626';
      badgeBg = '#FEE2E2';
      const overHours = Math.max(1, Math.abs(Math.round(remainingMs / (1000 * 60 * 60))));
      timeRemainingText = `Vencido hace ${overHours}h`;
      percent = 100;
    } else {
      const remHours = Math.floor(remainingMs / (1000 * 60 * 60));
      const remMins = Math.floor((remainingMs % (1000 * 60 * 60)) / (1000 * 60));
      timeRemainingText = `${remHours}h ${remMins}m restantes`;
      if (percent >= 75) {
        status = 'AT_RISK';
        statusText = 'En Riesgo';
        badgeColor = '#D97706';
        badgeBg = '#FEF3C7';
      } else {
        status = 'ON_TIME';
        statusText = 'En Tiempo';
        badgeColor = '#059669';
        badgeBg = '#ECFDF5';
      }
    }
  }

  return {
    maxHours,
    deadlineFormatted: formatDateTime(deadline.toISOString()),
    status,
    statusText,
    badgeColor,
    badgeBg,
    percent,
    timeRemainingText
  };
}

function renderTicketList() {
  const container = document.getElementById('ticket-list');
  if (!container) return;

  const countBadge = document.getElementById('ticket-count-badge');
  if (countBadge) {
    countBadge.textContent = AppState.tickets ? AppState.tickets.length : 0;
  }
  const sidebarCount = document.getElementById('sidebar-ticket-count');
  if (sidebarCount && AppState.tickets) {
    sidebarCount.textContent = AppState.tickets.length;
  }

  if (!AppState.tickets || AppState.tickets.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:40px 14px; color:#94A3B8;">
        <div style="font-size:36px; margin-bottom:10px;">📭</div>
        <div style="font-size:13px; font-weight:700; color:#475569;">No hay solicitudes con estos filtros</div>
        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Pruebe cambiando el filtro de estado o sede.</div>
      </div>
    `;
    return;
  }

  container.innerHTML = AppState.tickets.map(t => {
    const isSelected = AppState.selectedTicket && AppState.selectedTicket.id === t.id;
    const priority = (t.priority || 'P3').toUpperCase();
    const status = (t.status || 'NUEVO').toUpperCase();
    const level = (t.support_level || 'N1').toUpperCase();
    const platName = formatPlatformName(t.platform_code);
    const instName = formatInstitutionName(t.institution_code);
    const timeAgo = formatDateFriendly(t.created_at);

    return `
      <div class="ticket-card-clean prio-${priority.toLowerCase()} ${isSelected ? 'selected' : ''}" onclick="selectTicket('${t.id}', true)">
        <div class="card-row-top">
          <div class="card-id-prio">
            <span class="prio-chip prio-chip-${priority.toLowerCase()}">${priority}</span>
            <span class="ticket-id-clean">#${t.id}</span>
          </div>
          <span class="ticket-time-clean">${timeAgo}</span>
        </div>
        <div class="ticket-subject-clean">${t.title}</div>
        <div class="card-row-bottom">
          <div class="card-tags-group">
            <span class="pill-tag" title="${platName}">🩺 ${platName}</span>
            <span class="pill-tag" title="${instName}">🏥 ${instName}</span>
          </div>
          <div class="card-status-group">
            <span class="badge-tier badge-tier-${level.toLowerCase()}" style="font-size:9.5px; padding:2px 6px;">${level}</span>
            <span class="badge-status st-${status}" style="font-size:9.5px; padding:2px 6px;">${formatStatusName(status)}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

async function selectTicket(ticketId, userTriggered = false) {
  try {
    const ticket = await API.getTicket(ticketId);
    AppState.selectedTicket = ticket;
    renderTicketList();
    renderTicketDetail(ticket);

    const topTitle = document.getElementById('top-view-title-text');
    if (topTitle && AppState.currentView === 'tickets') {
      topTitle.textContent = `SOLICITUD #${ticket.id}`;
    }

    if (userTriggered && window.innerWidth <= 768) {
      switchMobileCockpitTab('col-detail');
    }
  } catch (err) {
    console.error('Error seleccionando ticket:', err);
  }
}

function renderTicketDetail(rawTicket) {
  const container = document.getElementById('ticket-detail-container');
  if (!container) return;

  if (!rawTicket) {
    container.innerHTML = `
      <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color:#94A3B8; text-align:center; padding:40px 20px;">
        <div style="font-size:48px; margin-bottom:12px; opacity:0.8;">📋</div>
        <h3 style="font-size:16px; font-weight:800; color:#334155; margin-bottom:6px;">Seleccione una Solicitud</h3>
        <p style="font-size:12.5px; color:#64748B; max-width:320px;">Haga clic en una solicitud de la bandeja izquierda para ver su diagnóstico, actividad y trazabilidad.</p>
      </div>
    `;
    return;
  }

  const ticket = rawTicket;
  const status = (ticket.status || 'NUEVO').toUpperCase();
  const priority = (ticket.priority || 'P3').toUpperCase();
  const level = (ticket.support_level || 'N1').toUpperCase();
  const platName = formatPlatformName(ticket.platform_code);
  const instName = formatInstitutionName(ticket.institution_code);
  const sla = calculateTicketSLA(ticket);

  const reqUser = (AppState.users || []).find(u => u.username === ticket.requester_username);
  const reqFullName = reqUser ? reqUser.full_name : (ticket.requester_name || ticket.requester_username || 'Solicitante Asistencial');

  const asgUser = (AppState.operators || []).find(u => u.username === ticket.assignee_username) || (AppState.users || []).find(u => u.username === ticket.assignee_username);
  const asgFullName = asgUser ? asgUser.full_name : (ticket.assignee_username ? `@${ticket.assignee_username}` : 'Sin Asignar');

  if (!AppState.activeDetailTab) {
    AppState.activeDetailTab = 'comments';
  }

  // Generar Botones de Acción Contextuales Limpios
  let actionsToolbarHtml = '';
  if (status === 'NUEVO') {
    actionsToolbarHtml = `
      <button class="btn-action-primary" onclick="actionAssignSelf('${ticket.id}')">
        👤 Auto-Asignarme
      </button>
      <button class="btn-action-secondary" onclick="openReassignModal('${ticket.id}')">
        👥 Asignar Operador...
      </button>
      <button class="btn-action-escalate" onclick="openEscalateModal('${ticket.id}', '${level}')">
        ⚡ Escalar Nivel ITIL...
      </button>
      <button class="btn-action-secondary" onclick="openEditTicketModal('${ticket.id}')">
        ✏️ Editar
      </button>
    `;
  } else if (status === 'ASIGNADO') {
    actionsToolbarHtml = `
      <button class="btn-action-primary" onclick="actionStartProgress('${ticket.id}')">
        ▶ Iniciar Diagnóstico
      </button>
      <button class="btn-action-resolve" onclick="openResolveModal('${ticket.id}')">
        ✅ Resolver Ticket...
      </button>
      <button class="btn-action-secondary" onclick="openReassignModal('${ticket.id}')">
        👥 Reasignar...
      </button>
      <button class="btn-action-escalate" onclick="openEscalateModal('${ticket.id}', '${level}')">
        ⚡ Escalar Nivel...
      </button>
    `;
  } else if (status === 'EN_CURSO') {
    actionsToolbarHtml = `
      <button class="btn-action-resolve" onclick="openResolveModal('${ticket.id}')">
        ✅ Registrar Solución & Resolver
      </button>
      <button class="btn-action-secondary" onclick="openReassignModal('${ticket.id}')">
        👥 Reasignar...
      </button>
      <button class="btn-action-escalate" onclick="openEscalateModal('${ticket.id}', '${level}')">
        ⚡ Escalar Nivel...
      </button>
    `;
  } else if (status === 'RESUELTO') {
    actionsToolbarHtml = `
      <button class="btn-action-resolve" onclick="actionCloseTicket('${ticket.id}')">
        🔒 Cerrar con Conformidad (100%)
      </button>
      <button class="btn-action-secondary" onclick="actionStartProgress('${ticket.id}')">
        ↩️ Reabrir Incidente
      </button>
      <button class="btn-action-escalate" onclick="promoteCurrentTicketToKB('${ticket.id}')">
        📚 Promover a Base de Conocimiento
      </button>
    `;
  } else if (status === 'CERRADO') {
    actionsToolbarHtml = `
      <span style="font-size:12px; font-weight:800; color:#059669; background:#ECFDF5; border:1px solid #A7F3D0; padding:6px 12px; border-radius:8px;">
        🔒 Incidente Cerrado con Conformidad
      </span>
      <button class="btn-action-escalate" onclick="promoteCurrentTicketToKB('${ticket.id}')">
        📚 Ver / Publicar en Base de Conocimiento
      </button>
    `;
  }

  const commentsCount = (ticket.comments || []).filter(c => !c.is_internal).length;
  const internalCount = (ticket.comments || []).filter(c => c.is_internal).length;
  const totalComments = (ticket.comments || []).length;
  const auditCount = (ticket.audit_logs || []).length;

  container.innerHTML = `
    <div class="detail-container-clean">
      
      <!-- 1. Encabezado Limpio y Ejecutivo -->
      <div class="detail-header-card">
        <div class="detail-top-bar">
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="prio-chip prio-chip-${priority.toLowerCase()}" style="font-size:11px; padding:3px 8px;">${priority}</span>
            <span style="font-family:'JetBrains Mono'; font-weight:800; font-size:13px; color:#475569;">#${ticket.id}</span>
            <span style="font-size:11.5px; color:#94A3B8; font-weight:600;">• ${formatDateTime(ticket.created_at)}</span>
          </div>

          <div style="display:flex; align-items:center; gap:6px;">
            <span style="font-size:11px; font-weight:700; color:${sla.badgeColor}; background:${sla.badgeBg}; padding:3px 8px; border-radius:6px; border:1px solid ${sla.badgeColor}33;">
              ⏱️ SLA: ${sla.statusText} (${sla.timeRemainingText})
            </span>
            <span class="badge-tier badge-tier-${level.toLowerCase()}" style="font-size:10.5px; padding:3px 8px;">${level}</span>
            <span class="badge-status st-${status}" style="font-size:10.5px; padding:3px 8px;">${formatStatusName(status)}</span>
          </div>
        </div>

        <h1 class="detail-title-h1">${ticket.title}</h1>

        <div class="detail-meta-pills">
          <span class="detail-meta-item">
            👤 <strong>Solicitante:</strong> ${reqFullName} (${instName})
          </span>
          <span class="detail-meta-item">
            🩺 <strong>Plataforma:</strong> ${platName}
          </span>
          <span class="detail-meta-item">
            👨‍💻 <strong>Asignado a:</strong> ${asgFullName}
          </span>
        </div>

        <!-- Barra de Acciones FSM -->
        <div class="detail-actions-toolbar">
          ${actionsToolbarHtml}
        </div>
      </div>

      <!-- 2. Barra de Pestañas de Navegación -->
      <div class="detail-tabs-bar">
        <button class="detail-tab-btn-clean ${AppState.activeDetailTab === 'comments' ? 'active' : ''}" onclick="switchDetailTab('comments')">
          💬 Actividad & Notas (${totalComments})
        </button>
        <button class="detail-tab-btn-clean ${AppState.activeDetailTab === 'technical' ? 'active' : ''}" onclick="switchDetailTab('technical')">
          📋 Ficha Técnica & Diagnóstico
        </button>
        <button class="detail-tab-btn-clean ${AppState.activeDetailTab === 'audit' ? 'active' : ''}" onclick="switchDetailTab('audit')">
          📜 Historial & Trazabilidad (${auditCount})
        </button>
        <button class="detail-tab-btn-clean ${AppState.activeDetailTab === 'kb' ? 'active' : ''}" onclick="switchDetailTab('kb')">
          📚 Base de Conocimiento Sugerida
        </button>
      </div>

      <!-- 3. Contenedor de Contenido de la Pestaña Activa -->
      <div class="detail-tab-content-area" id="detail-tab-content">
        ${renderDetailTabContent(ticket)}
      </div>

    </div>
  `;
}

function switchDetailTab(tabName) {
  AppState.activeDetailTab = tabName;
  if (AppState.selectedTicket) {
    renderTicketDetail(AppState.selectedTicket);
  }
}

function renderDetailTabContent(ticket) {
  const platName = formatPlatformName(ticket.platform_code);
  const instName = formatInstitutionName(ticket.institution_code);
  const sla = calculateTicketSLA(ticket);

  if (AppState.activeDetailTab === 'comments') {
    const comments = ticket.comments || [];
    
    let commentsListHtml = '';
    if (comments.length === 0) {
      commentsListHtml = `
        <div style="text-align:center; color:#64748B; padding:30px 10px; font-size:12px; background:#FFFFFF; border-radius:10px; border:1px dashed #CBD5E1; margin-bottom:16px;">
          <div style="font-size:24px; margin-bottom:6px;">💬</div>
          <div style="font-weight:700; color:#334155;">Sin comentarios aún</div>
          <div style="font-size:11px; color:#94A3B8; margin-top:2px;">Utilice el recuadro inferior para responder al solicitante o agregar una nota interna.</div>
        </div>
      `;
    } else {
      commentsListHtml = `
        <div class="chat-stream-clean">
          ${comments.map(c => {
            const isInternal = c.is_internal;
            const isRequester = c.author_username === ticket.requester_username;
            const bubbleClass = isInternal ? 'chat-bubble-internal' : (isRequester ? 'chat-bubble-requester' : 'chat-bubble-agent');

            return `
              <div class="chat-bubble ${bubbleClass}">
                <div class="chat-bubble-header">
                  <span style="display:flex; align-items:center; gap:6px;">
                    ${isInternal ? '🔒 <strong>Nota Privada Interna</strong> •' : ''}
                    <strong>👤 ${c.author_username}</strong>
                  </span>
                  <span style="opacity:0.75;">${formatDateTime(c.created_at)}</span>
                </div>
                <div style="white-space:pre-wrap;">${c.message}</div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    return `
      <div style="display:flex; flex-direction:column; height:100%;">
        ${commentsListHtml}

        <!-- Caja de Respuesta Rápida -->
        <div class="chat-input-box" style="margin-top:auto;">
          <textarea id="input-comment" class="form-control" rows="3" placeholder="Escriba un mensaje para el solicitante o una nota de trabajo para el equipo..." style="font-size:12.5px;"></textarea>
          
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <label style="font-size:11.5px; color:#475569; display:flex; align-items:center; gap:6px; cursor:pointer;">
              <input type="checkbox" id="check-is-internal" style="width:15px; height:15px; accent-color:#00A896;"> 
              <span><strong>Nota Privada Interna</strong> (Visible solo para operadores)</span>
            </label>
            <button class="btn-action-primary" id="btn-send-comment" onclick="submitComment('${ticket.id}')">
              <span>Enviar Mensaje</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px;"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
          </div>
        </div>
      </div>
    `;
  } else if (AppState.activeDetailTab === 'technical') {
    return `
      <div class="diagnostic-grid-clean">
        
        <!-- Tarjeta 1: Solicitante & Sede -->
        <div class="info-card-clean">
          <div class="info-card-clean-title">
            <span>👤</span>
            <span>Datos del Solicitante</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Nombre:</span>
            <span class="info-field-val">${ticket.requester_name || ticket.requester_username}</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Usuario:</span>
            <span class="info-field-val"><code>@${ticket.requester_username}</code></span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Institución / Sede:</span>
            <span class="info-field-val">🏥 ${instName}</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Email de Notificación:</span>
            <span class="info-field-val"><a href="mailto:${ticket.requester_email || ''}" style="color:#2563EB;">${ticket.requester_email || 'Sin email'}</a></span>
          </div>
        </div>

        <!-- Tarjeta 2: Clasificación & SLA ITIL -->
        <div class="info-card-clean">
          <div class="info-card-clean-title">
            <span>🩺</span>
            <span>Clasificación Asistencial & SLA</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Plataforma Afectada:</span>
            <span class="info-field-val">${platName}</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Tipo de Solicitud:</span>
            <span class="info-field-val">${ticket.ticket_type || 'INCIDENTE'}</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Impacto Asistencial:</span>
            <span class="info-field-val">${ticket.impact || 'MEDIO'}</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Urgencia:</span>
            <span class="info-field-val">${ticket.urgency || 'MEDIO'}</span>
          </div>
          <div class="info-field-row">
            <span class="info-field-label">Nivel de Soporte ITIL:</span>
            <span class="info-field-val"><span class="badge-tier badge-tier-${(ticket.support_level || 'N1').toLowerCase()}">${ticket.support_level || 'N1'}</span></span>
          </div>
        </div>

        <!-- Tarjeta 3: Diagnóstico Detallado & Evidencia -->
        <div class="info-card-clean" style="grid-column: 1 / -1;">
          <div class="info-card-clean-title">
            <span>📝</span>
            <span>Descripción del Problema & Evidencia</span>
          </div>
          <div style="font-size:12.5px; color:#1E293B; line-height:1.5; white-space:pre-wrap; background:#F8FAFC; padding:12px 14px; border-radius:8px; border:1px solid #E2E8F0;">${ticket.description || 'Sin descripción ingresada.'}</div>
          
          ${ticket.attachment_url ? `
            <div style="margin-top:10px; display:flex; align-items:center; justify-content:space-between; background:#EFF6FF; border:1px solid #BFDBFE; padding:8px 12px; border-radius:8px;">
              <span style="font-size:12px; color:#1E40AF;"><strong>🔗 Evidencia Adjunta:</strong> ${ticket.attachment_url}</span>
              <a href="${ticket.attachment_url}" target="_blank" rel="noopener noreferrer" class="btn-action-primary" style="font-size:11px; padding:4px 10px; text-decoration:none;">
                Abrir Enlace
              </a>
            </div>
          ` : ''}
        </div>

        <!-- Tarjeta 4: Solución Técnica (si existe) -->
        ${ticket.resolution_notes ? `
          <div class="info-card-clean" style="grid-column: 1 / -1; border-color:#86EFAC; background:#F0FDF4;">
            <div class="info-card-clean-title" style="color:#065F46; border-bottom-color:#A7F3D0;">
              <span>✅</span>
              <span>Solución Técnica Registrada</span>
            </div>
            ${ticket.root_cause ? `
              <div class="info-field-row" style="margin-bottom:6px;">
                <span class="info-field-label" style="color:#047857;">Diagnóstico / Causa Raíz:</span>
                <span class="info-field-val" style="color:#065F46;">${ticket.root_cause}</span>
              </div>
            ` : ''}
            <div style="font-size:12.5px; color:#065F46; line-height:1.5; white-space:pre-wrap; background:#FFFFFF; padding:12px 14px; border-radius:8px; border:1px solid #A7F3D0;">${ticket.resolution_notes}</div>
            <div style="font-size:11px; color:#059669; margin-top:6px; display:flex; justify-content:space-between;">
              <span><strong>Resuelto por:</strong> 👤 ${ticket.resolved_by_username || 'Operador'}</span>
              <span>${ticket.is_workaround ? '⚠️ Solución Temporal (Workaround)' : '🟢 Solución Definitiva'}</span>
            </div>
          </div>
        ` : ''}

      </div>
    `;
  } else if (AppState.activeDetailTab === 'audit') {
    const logs = ticket.audit_logs || [];
    if (logs.length === 0) {
      return `
        <div style="text-align:center; color:#64748B; padding:30px 10px; font-size:12px; background:#FFFFFF; border-radius:10px; border:1px dashed #CBD5E1;">
          <div style="font-size:24px; margin-bottom:6px;">📜</div>
          <div style="font-weight:700; color:#334155;">Sin eventos de auditoría registrados</div>
          <div style="font-size:11px; color:#94A3B8; margin-top:2px;">Los cambios de estado y derivaciones se registrarán aquí con sello de tiempo.</div>
        </div>
      `;
    }

    return `
      <div style="display:flex; flex-direction:column; gap:10px;">
        ${logs.map(l => `
          <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:12px 16px; display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
            <div>
              <div style="font-size:12.5px; font-weight:800; color:#0F172A;">
                ${l.change_reason || `Modificación del campo: ${l.field_changed}`}
              </div>
              <div style="font-size:11.5px; color:#64748B; margin-top:2px;">
                Operador: <strong>👤 ${l.changed_by_username}</strong>
              </div>
            </div>
            <span style="font-size:11px; color:#94A3B8; font-family:'JetBrains Mono'; white-space:nowrap;">
              ${formatDateTime(l.created_at)}
            </span>
          </div>
        `).join('')}
      </div>
    `;
  } else if (AppState.activeDetailTab === 'kb') {
    const suggestions = (AppState.kbArticles || []).filter(a => !ticket.platform_code || a.platform_code === ticket.platform_code || a.category === 'CLINICO').slice(0, 4);

    return `
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px;">
          <div>
            <div style="font-size:13.5px; font-weight:800; color:#0F172A;">Artículos & Procedimientos Homologados</div>
            <div style="font-size:11.5px; color:#64748B;">Guías de resolución recomendadas para la plataforma <strong>${platName}</strong>.</div>
          </div>
          <button class="btn-action-primary" onclick="promoteCurrentTicketToKB('${ticket.id}')">
            ➕ Crear Artículo a partir de este Ticket
          </button>
        </div>

        ${suggestions.length === 0 ? `
          <div style="text-align:center; padding:30px 10px; background:#FFFFFF; border-radius:10px; border:1px dashed #CBD5E1; color:#64748B;">
            <div style="font-size:24px; margin-bottom:6px;">📚</div>
            <div style="font-weight:700;">No hay artículos específicos aún para ${platName}</div>
            <div style="font-size:11px; color:#94A3B8; margin-top:2px;">Puede crear el primer protocolo homologado para este módulo asistencial.</div>
          </div>
        ` : `
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px;">
            ${suggestions.map(art => `
              <div class="info-card-clean" style="cursor:pointer;" onclick="openViewArticleModal(${art.id})">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                  <span class="badge-tier badge-tier-n2" style="font-size:9.5px;">${art.category || 'General'}</span>
                  <span style="font-size:10px; color:#64748B;">${art.version || 'v1.0'}</span>
                </div>
                <div style="font-size:13px; font-weight:800; color:#0F172A; line-height:1.3;">${art.title}</div>
                <div style="font-size:11.5px; color:#64748B; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">${art.content}</div>
                <div style="font-size:11px; color:#00A896; font-weight:700; margin-top:auto;">Ver Protocolo Completo ➔</div>
              </div>
            `).join('')}
          </div>
        `}
      </div>
    `;
  }
}

function openResolveModal(ticketId) {
  const modal = document.getElementById('modal-resolve-ticket');
  if (!modal) return;
  const t = AppState.selectedTicket;
  if (!t) return;
  
  document.getElementById('resolve-ticket-id').value = ticketId;
  const disp = document.getElementById('resolve-ticket-id-display');
  if (disp) disp.textContent = ticketId;
  
  const rootEl = document.getElementById('resolve-root-cause');
  if (rootEl) rootEl.value = t.root_cause || '';
  
  const notesEl = document.getElementById('resolve-notes');
  if (notesEl) notesEl.value = t.resolution_notes || '';
  
  const workEl = document.getElementById('resolve-is-workaround');
  if (workEl) workEl.checked = t.is_workaround || false;
  
  modal.classList.add('active');
}

function openReassignModal(ticketId) {
  const modal = document.getElementById('modal-reassign-ticket');
  if (!modal) return;
  const t = AppState.selectedTicket;
  if (!t) return;
  
  document.getElementById('reassign-ticket-id').value = ticketId;
  const disp = document.getElementById('reassign-ticket-id-display');
  if (disp) disp.textContent = ticketId;
  
  const selOp = document.getElementById('reassign-operator-select');
  if (selOp) {
    selOp.innerHTML = '<option value="">Seleccione operador disponible...</option>' + 
      AppState.operators.map(op => `<option value="${op.username}" ${op.username === t.assignee_username ? 'selected' : ''}>${op.full_name} (${op.role} - ${op.support_level || 'N1'})</option>`).join('');
  }
  
  const selLvl = document.getElementById('reassign-level-select');
  if (selLvl) {
    selLvl.value = t.support_level || 'N1';
  }
  
  modal.classList.add('active');
}

async function submitComment(ticketId) {
  const input = document.getElementById('input-comment');
  const isInternal = document.getElementById('check-is-internal').checked;
  if (!input || !input.value.trim()) return;

  try {
    await API.addComment(ticketId, {
      author_username: AppState.currentUser.username,
      message: input.value.trim(),
      is_internal: isInternal
    });
    input.value = '';
    showToast('Mensaje registrado exitosamente', 'success');
    await selectTicket(ticketId);
  } catch (err) {
    showToast('Error al registrar mensaje', 'error');
  }
}

// ACCIONES FSM CONTEXTUALES
async function actionAssignSelf(ticketId) {
  try {
    await API.assignTicket(ticketId, {
      assignee_username: AppState.currentUser.username,
      support_level: 'N1',
      reason: 'Auto-asignación directa desde mesa de ayuda',
      changed_by_username: AppState.currentUser.username
    });
    showToast('Caso asignado correctamente', 'success');
    await selectTicket(ticketId);
    await loadDashboardMetrics(AppState.currentDashInst);
  } catch (err) {
    showToast('Error al auto-asignar', 'error');
  }
}

async function actionAssignOperator(ticketId) {
  const opEl = document.getElementById('action-assignee');
  const lvlEl = document.getElementById('action-support-level');
  const op = opEl ? opEl.value : '';
  const lvl = lvlEl ? lvlEl.value : 'N1';
  if (!op) {
    showToast('Seleccione un operador para derivar el caso', 'error');
    return;
  }
  try {
    await API.assignTicket(ticketId, {
      assignee_username: op,
      support_level: lvl,
      reason: `Derivación operativa a nivel ${lvl}`,
      changed_by_username: AppState.currentUser.username
    });
    showToast('Derivación guardada con éxito', 'success');
    await selectTicket(ticketId);
    await loadDashboardMetrics(AppState.currentDashInst);
  } catch (err) {
    showToast('Error al derivar ticket', 'error');
  }
}

async function actionStartProgress(ticketId) {
  try {
    await API.updateStatus(ticketId, {
      new_status: 'EN_CURSO',
      changed_by_username: AppState.currentUser.username,
      reason: 'Inicio de trabajo activo en la resolución del caso'
    });
    showToast('Estado actualizado a: EN CURSO', 'success');
    await selectTicket(ticketId);
    await loadDashboardMetrics(AppState.currentDashInst);
  } catch (err) {
    showToast('Error al iniciar trabajo', 'error');
  }
}

async function actionResolveTicket(ticketId) {
  const notesEl = document.getElementById('action-res-notes');
  const workEl = document.getElementById('action-is-workaround');
  const notes = notesEl ? notesEl.value.trim() : '';
  const isWorkaround = workEl ? workEl.checked : false;

  if (notes.length < 8) {
    showToast('La solución técnica debe contener al menos 8 caracteres explicativos', 'error');
    return;
  }
  try {
    await API.resolveTicket(ticketId, {
      resolution_notes: notes,
      is_workaround: isWorkaround,
      resolved_by_username: AppState.currentUser.username
    });
    showToast('Ticket marcado como solucionado', 'success');
    await selectTicket(ticketId);
    await loadDashboardMetrics(AppState.currentDashInst);
  } catch (err) {
    showToast('Error al resolver ticket', 'error');
  }
}

async function actionCloseTicket(ticketId) {
  try {
    await API.closeTicket(ticketId, {
      closed_by_username: AppState.currentUser.username,
      feedback: 'Conformidad final registrada por el solicitante'
    });
    showToast('¡Ticket cerrado con éxito! Conformidad registrada.', 'success');
    await selectTicket(ticketId);
    await loadDashboardMetrics(AppState.currentDashInst);
  } catch (err) {
    showToast('Error al cerrar ticket', 'error');
  }
}

// =============================================================================
// 5. BASE DE CONOCIMIENTO (DINÁMICA, VERSIONADA Y CON HISTORIAL DE CAMBIOS)
// =============================================================================

const KB_CAT_ICONS = {
  'Receta Digital': '💊',
  'Telemedicina': '📡',
  'Historia Clínica': '📋',
  'Contingencias': '🚨',
  'Facturación y Pagos': '💳',
  'Interoperabilidad': '🔗',
  'Consultorio Digital': '👨‍⚕️',
  'General': '🏥'
};

const KB_CAT_COLORS = {
  'Receta Digital': { bg: '#F0FDFA', text: '#0D9488', border: '#99F6E4' },
  'Telemedicina': { bg: '#EFF6FF', text: '#2563EB', border: '#BFDBFE' },
  'Historia Clínica': { bg: '#EEF2FF', text: '#4F46E5', border: '#C7D2FE' },
  'Contingencias': { bg: '#FEF2F2', text: '#DC2626', border: '#FECACA' },
  'Facturación y Pagos': { bg: '#FFFBEB', text: '#D97706', border: '#FDE68A' },
  'Interoperabilidad': { bg: '#FAF5FF', text: '#7E22CE', border: '#E9D5FF' },
  'Consultorio Digital': { bg: '#ECFDF5', text: '#059669', border: '#A7F3D0' },
  'General': { bg: '#F8FAFC', text: '#475569', border: '#CBD5E1' }
};

async function loadKnowledgeBase(search = '', category = '') {
  try {
    const activeCat = (category === 'all' || !category) ? '' : category;
    const articles = await API.getArticles({ search, category: activeCat });
    AppState.kbArticles = articles;

    // Actualizar contadores de categorías
    try {
      const stats = await API.getCategoriesCount();
      updateKBCategoryPills(stats, category);
      
      // Actualizar KPIs superiores
      const totalArticlesEl = document.getElementById('kb-kpi-total-articles');
      const totalHistoryEl = document.getElementById('kb-kpi-total-history');
      const contingenciesEl = document.getElementById('kb-kpi-contingencies');
      
      if (totalArticlesEl) totalArticlesEl.textContent = stats.total_articles || articles.length;
      if (totalHistoryEl) totalHistoryEl.textContent = stats.total_history_records || (articles.length * 2);
      if (contingenciesEl) contingenciesEl.textContent = (stats.by_category && stats.by_category['Contingencias']) || 0;
    } catch (e) {
      console.warn('No se pudo cargar estadísticas de categorías KB:', e);
    }

    renderKnowledgeBase(articles);
  } catch (err) {
    console.error('Error cargando base de conocimiento:', err);
    showToast('Error al conectar con la Base de Conocimiento', 'error');
  }
}

function updateKBCategoryPills(stats, activeCategory) {
  const pillsContainer = document.getElementById('kb-category-pills');
  if (!pillsContainer) return;

  const currentCat = activeCategory || AppState.kbSelectedCategory || 'all';

  // Actualizar pill counts
  const byCat = (stats && stats.by_category) || {};
  const allCountEl = document.getElementById('kb-pill-count-all');
  const recetaCountEl = document.getElementById('kb-pill-count-receta');
  const telemedCountEl = document.getElementById('kb-pill-count-telemed');
  const hceCountEl = document.getElementById('kb-pill-count-hce');
  const contCountEl = document.getElementById('kb-pill-count-contingencia');
  const pagosCountEl = document.getElementById('kb-pill-count-pagos');
  const interopCountEl = document.getElementById('kb-pill-count-interop');
  const consultorioCountEl = document.getElementById('kb-pill-count-consultorio');

  if (allCountEl) allCountEl.textContent = stats.total_articles || 0;
  if (recetaCountEl) recetaCountEl.textContent = byCat['Receta Digital'] || 0;
  if (telemedCountEl) telemedCountEl.textContent = byCat['Telemedicina'] || 0;
  if (hceCountEl) hceCountEl.textContent = byCat['Historia Clínica'] || 0;
  if (contCountEl) contCountEl.textContent = byCat['Contingencias'] || 0;
  if (pagosCountEl) pagosCountEl.textContent = byCat['Facturación y Pagos'] || 0;
  if (interopCountEl) interopCountEl.textContent = byCat['Interoperabilidad'] || 0;
  if (consultorioCountEl) consultorioCountEl.textContent = byCat['Consultorio Digital'] || 0;

  // Actualizar active classes
  const buttons = pillsContainer.querySelectorAll('button');
  buttons.forEach(btn => {
    const onclickStr = btn.getAttribute('onclick') || '';
    if (currentCat === 'all' && onclickStr.includes("'all'")) {
      btn.classList.add('active');
    } else if (currentCat !== 'all' && onclickStr.includes(`'${currentCat}'`)) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
}

function filterKBCategory(cat) {
  AppState.kbSelectedCategory = cat;
  const searchInput = document.getElementById('kb-search-input');
  const search = searchInput ? searchInput.value.trim() : '';

  // Toggle active class visualmente
  const container = document.getElementById('kb-category-pills');
  if (container) {
    container.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    const clicked = Array.from(container.querySelectorAll('button')).find(b => {
      const fn = b.getAttribute('onclick') || '';
      return fn.includes(`'${cat}'`);
    });
    if (clicked) clicked.classList.add('active');
  }

  loadKnowledgeBase(search, cat);
}

function renderKnowledgeBase(articles) {
  const container = document.getElementById('kb-articles-grid');
  if (!container) return;

  const list = articles || AppState.kbArticles || [];
  if (list.length === 0) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:48px 24px; background:#FFF; border-radius:12px; border:1px dashed #CBD5E1;">
        <div style="font-size:36px; margin-bottom:10px;">🔍</div>
        <h3 style="font-size:16px; font-weight:800; color:#0F172A; margin:0 0 6px 0;">No se encontraron artículos para este criterio</h3>
        <p style="font-size:12.5px; color:#64748B; margin:0 0 16px 0;">Pruebe cambiando los filtros de categoría o publique un nuevo procedimiento clínico.</p>
        <button class="btn-pri" onclick="document.getElementById('modal-new-article').classList.add('active')" style="font-size:12px; padding:8px 16px; display:inline-flex; align-items:center; gap:6px;">
          <span>➕ Publicar Nuevo Protocolo</span>
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = list.map(a => {
    const icon = KB_CAT_ICONS[a.category] || '📄';
    const col = KB_CAT_COLORS[a.category] || { bg: '#F8FAFC', text: '#475569', border: '#E2E8F0' };
    const versionStr = a.version || 'v1.0';
    const changelogStr = a.changelog || 'Versión inicial homologada';
    const views = a.view_count || 0;
    const author = a.author_username || 'Soporte Clínico';
    const dateStr = formatDateFriendly(a.updated_at || a.created_at);

    return `
      <div class="kb-card">
        <div>
          <div class="kb-card-top">
            <span class="kb-category-tag" style="background:${col.bg}; color:${col.text}; border:1px solid ${col.border};">
              <span>${icon}</span>
              <span>${a.category}</span>
            </span>
            <div style="display:flex; align-items:center; gap:6px;">
              <span class="kb-version-badge" title="Versión activa en producción">
                <span>🏷️</span>
                <span>${versionStr}</span>
              </span>
              ${a.source_ticket_id ? `
                <span style="font-size:9.5px; font-weight:800; background:#EFF6FF; color:#1D4ED8; border:1px solid #BFDBFE; padding:2px 6px; border-radius:10px;" title="Promovido desde el ticket resuelto ${a.source_ticket_id}">
                  🔗 ${a.source_ticket_id}
                </span>
              ` : ''}
            </div>
          </div>

          <h3 class="kb-card-title">${a.title}</h3>

          <div class="kb-changelog-chip" title="Último motivo de modificación">
            <span style="font-weight:700; color:#0F172A; white-space:nowrap;">🔄 ${versionStr}:</span>
            <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${changelogStr}</span>
          </div>

          <div class="kb-card-snippet">
            ${a.content || a.description || 'Sin pasos detallados registrados.'}
          </div>
        </div>

        <div class="kb-card-footer">
          <div style="display:flex; align-items:center; gap:10px; color:#64748B;">
            <span title="Autor y fecha de homologación">👤 <strong>${author}</strong> • ${dateStr}</span>
            <span title="Consultas registradas">👁️ ${views}</span>
          </div>

          <div style="display:flex; align-items:center; gap:6px;">
            <button type="button" class="kb-btn-action" onclick="openViewArticleModal(${a.id})" title="Leer procedimiento completo">
              <span>📖 Leer</span>
            </button>
            <button type="button" class="kb-btn-action" onclick="openArticleHistoryModal(${a.id})" title="Ver histórico y línea de tiempo de cambios">
              <span>📜 Historial</span>
            </button>
            <button type="button" class="kb-btn-action" onclick="openEditArticleModal(${a.id})" title="Modificar y crear nueva versión">
              <span>✏️ Nueva Versión</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// -----------------------------------------------------------------------------
// MODAL: LECTOR DE PROTOCOLO (READING VIEW)
// -----------------------------------------------------------------------------
let currentReadingArticle = null;

async function openViewArticleModal(articleId) {
  const modal = document.getElementById('modal-view-article');
  if (!modal) return;

  try {
    const article = await API.getArticle(articleId);
    currentReadingArticle = article;

    // Registrar vista en backend
    API.registerArticleView(articleId).catch(() => {});

    const iconEl = document.getElementById('view-article-icon');
    const catEl = document.getElementById('view-article-cat');
    const titleEl = document.getElementById('view-article-title');
    const verEl = document.getElementById('view-article-ver');
    const authorEl = document.getElementById('view-article-author');
    const dateEl = document.getElementById('view-article-date');
    const changelogBoxEl = document.getElementById('view-article-changelog-box');
    const contentEl = document.getElementById('view-article-content');

    if (iconEl) iconEl.textContent = KB_CAT_ICONS[article.category] || '📄';
    if (catEl) catEl.textContent = article.category || 'General';
    if (titleEl) titleEl.textContent = article.title;
    if (verEl) verEl.textContent = `Versión: ${article.version || 'v1.0'}`;
    if (authorEl) authorEl.textContent = `Homologado por: ${article.author_username || 'Soporte'}`;
    if (dateEl) dateEl.textContent = `Actualizado: ${formatDateFriendly(article.updated_at || article.created_at)}`;
    
    if (changelogBoxEl) {
      changelogBoxEl.innerHTML = `
        <span style="font-weight:700; color:#0F172A;">🔄 Changelog (${article.version || 'v1.0'}):</span>
        <span>${article.changelog || 'Versión inicial homologada'}</span>
      `;
    }

    if (contentEl) contentEl.textContent = article.content || '';

    modal.classList.add('active');
  } catch (err) {
    console.error('Error abriendo protocolo:', err);
    showToast('No se pudo cargar el detalle del artículo', 'error');
  }
}

function copyArticleContent() {
  if (!currentReadingArticle || !currentReadingArticle.content) {
    showToast('No hay contenido para copiar', 'error');
    return;
  }
  const text = `${currentReadingArticle.title} (${currentReadingArticle.version || 'v1.0'})\n\n${currentReadingArticle.content}`;
  navigator.clipboard.writeText(text).then(() => {
    showToast('📋 Protocolo copiado al portapapeles', 'success');
  }).catch(() => {
    showToast('Error al copiar al portapapeles', 'error');
  });
}

// -----------------------------------------------------------------------------
// MODAL: HISTORIAL DE VERSIONES Y AUDITORÍA DE CAMBIOS
// -----------------------------------------------------------------------------
async function openArticleHistoryModal(articleId) {
  const modal = document.getElementById('modal-article-history');
  const titleEl = document.getElementById('history-modal-article-title');
  const summaryEl = document.getElementById('history-modal-summary');
  const countBadgeEl = document.getElementById('history-count-badge');
  const timelineEl = document.getElementById('history-timeline-container');

  if (!modal || !timelineEl) return;

  // Limpiar y mostrar modal con spinner
  if (titleEl) titleEl.textContent = 'Cargando historial...';
  if (timelineEl) timelineEl.innerHTML = '<div style="padding:20px; text-align:center; color:#64748B;">⏳ Obteniendo registro de versiones y auditoría...</div>';
  modal.classList.add('active');

  try {
    const [article, history] = await Promise.all([
      API.getArticle(articleId),
      API.getArticleHistory(articleId)
    ]);

    if (titleEl) titleEl.textContent = article.title;
    if (countBadgeEl) countBadgeEl.textContent = `${history.length} Versiones Registradas`;

    if (summaryEl) {
      const col = KB_CAT_COLORS[article.category] || { bg: '#F8FAFC', text: '#475569', border: '#CBD5E1' };
      summaryEl.innerHTML = `
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:22px;">${KB_CAT_ICONS[article.category] || '📄'}</span>
          <div>
            <div style="display:flex; align-items:center; gap:6px;">
              <span class="kb-category-tag" style="background:${col.bg}; color:${col.text}; border:1px solid ${col.border}; font-size:9.5px;">${article.category}</span>
              <span class="kb-version-badge" style="font-size:10px;">Versión Actual: ${article.version || 'v1.0'}</span>
            </div>
            <div style="font-size:11px; color:#64748B; margin-top:3px;">
              Creado el ${formatDateFriendly(article.created_at)} • ${article.view_count || 0} lecturas registradas
            </div>
          </div>
        </div>
        <button class="btn-pri" onclick="document.getElementById('modal-article-history').classList.remove('active'); openEditArticleModal(${article.id});" style="font-size:11px; padding:5px 12px;">
          ✏️ Crear Nueva Versión
        </button>
      `;
    }

    if (!history || history.length === 0) {
      timelineEl.innerHTML = `
        <div style="padding:20px; text-align:center; color:#64748B; background:#F8FAFC; border-radius:8px;">
          No hay revisiones históricas anteriores registradas para este artículo.
        </div>
      `;
      return;
    }

    timelineEl.innerHTML = history.map((h, idx) => {
      const isCurrent = (h.version === article.version) || idx === 0;
      const dateStr = formatDateFriendly(h.created_at);
      const changelogText = h.changelog || (idx === history.length - 1 ? 'Versión inicial homologada' : 'Modificación de protocolo');
      const snippet = (h.content || '').substring(0, 200) + ((h.content || '').length > 200 ? '...' : '');

      return `
        <div class="kb-timeline-node">
          <div class="kb-timeline-dot ${isCurrent ? '' : 'past'}"></div>
          <div class="kb-timeline-card ${isCurrent ? 'current' : ''}">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px; flex-wrap:wrap; gap:6px;">
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="kb-version-badge" style="background:${isCurrent ? '#ECFDF5' : '#F1F5F9'}; color:${isCurrent ? '#047857' : '#475569'}; border-color:${isCurrent ? '#A7F3D0' : '#CBD5E1'}; font-size:11px;">
                  🏷️ ${h.version}
                </span>
                ${isCurrent ? '<span style="font-size:10px; font-weight:800; color:#059669; background:#D1FAE5; padding:1px 6px; border-radius:4px;">PRODUCCIÓN ACTIVA</span>' : ''}
              </div>
              <div style="font-size:11px; color:#64748B;">
                📅 <strong>${dateStr}</strong> por 👤 <strong>${h.author_username || 'Soporte'}</strong>
              </div>
            </div>

            <div style="font-size:12px; font-weight:700; color:#0F172A; margin-bottom:4px;">
              Motivo del Cambio: <span style="font-weight:500; color:#334155;">${changelogText}</span>
            </div>

            <div style="font-size:11.5px; color:#475569; background:#FFFFFF; border:1px solid #E2E8F0; border-radius:6px; padding:8px 10px; margin-top:6px; line-height:1.5;">
              <div style="font-weight:700; font-size:10.5px; color:#64748B; margin-bottom:2px; text-transform:uppercase;">Snapshot de Contenido (${h.version}):</div>
              <div style="white-space:pre-wrap; max-height:100px; overflow-y:auto;" id="history-content-${h.id}">${h.content}</div>
            </div>

            <div style="margin-top:8px; display:flex; justify-content:flex-end;">
              <button type="button" class="kb-btn-action" style="font-size:10.5px; padding:3px 8px;" onclick="navigator.clipboard.writeText(document.getElementById('history-content-${h.id}').innerText); showToast('Contenido de versión ${h.version} copiado', 'success');">
                📋 Copiar Texto de esta Versión
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');

  } catch (err) {
    console.error('Error cargando historial:', err);
    if (timelineEl) {
      timelineEl.innerHTML = '<div style="padding:20px; color:#DC2626; text-align:center;">❌ Error al consultar el historial de versiones en la base de datos.</div>';
    }
  }
}

// -----------------------------------------------------------------------------
// MODAL: EDITAR / PUBLICAR NUEVA VERSIÓN DE ARTÍCULO
// -----------------------------------------------------------------------------
let editingArticleOriginal = null;

async function openEditArticleModal(articleId) {
  const modal = document.getElementById('modal-edit-article');
  if (!modal) return;

  try {
    const article = await API.getArticle(articleId);
    editingArticleOriginal = article;

    document.getElementById('edit-article-id').value = article.id;
    document.getElementById('edit-article-title').value = article.title;
    document.getElementById('edit-article-category').value = article.category;
    document.getElementById('edit-article-tags').value = article.tags || '';
    document.getElementById('edit-article-content').value = article.content || '';
    document.getElementById('edit-article-changelog').value = '';

    // Configurar incremento de versión sugerido
    document.getElementById('edit-article-increment').value = 'minor';
    updateNewVersionPreview();

    modal.classList.add('active');
  } catch (err) {
    console.error('Error abriendo modal de edición:', err);
    showToast('No se pudo cargar la información del artículo', 'error');
  }
}

function updateNewVersionPreview() {
  if (!editingArticleOriginal) return;

  const type = document.getElementById('edit-article-increment').value;
  const currentVer = editingArticleOriginal.version || 'v1.0';
  const previewInput = document.getElementById('edit-article-version-preview');
  if (!previewInput) return;

  // Extraer números (ej: 'v2.4' -> major: 2, minor: 4)
  const clean = currentVer.replace(/^v/i, '');
  const parts = clean.split('.').map(p => parseInt(p, 10) || 0);
  let major = parts[0] !== undefined ? parts[0] : 1;
  let minor = parts[1] !== undefined ? parts[1] : 0;

  if (type === 'minor') {
    minor += 1;
    previewInput.value = `v${major}.${minor}`;
    previewInput.readOnly = true;
  } else if (type === 'major') {
    major += 1;
    minor = 0;
    previewInput.value = `v${major}.${minor}`;
    previewInput.readOnly = true;
  } else {
    // Custom
    previewInput.readOnly = false;
    previewInput.value = `v${major}.${minor + 1}`;
  }
}

// -----------------------------------------------------------------------------
// PROMOVER TICKET RESUELTO DIRECTAMENTE A LA BASE DE CONOCIMIENTO
// -----------------------------------------------------------------------------
function promoteCurrentTicketToKB(ticketId) {
  const ticket = (AppState.tickets || []).find(t => t.id === ticketId);
  if (!ticket) {
    showToast('No se encontró el ticket seleccionado', 'error');
    return;
  }

  const modal = document.getElementById('modal-new-article');
  if (!modal) return;

  // Pre-cargar datos del ticket
  const titleInput = document.getElementById('article-title');
  const catSelect = document.getElementById('article-category');
  const contentInput = document.getElementById('article-content');
  const tagsInput = document.getElementById('article-tags');
  const versionInput = document.getElementById('article-initial-version');
  const changelogInput = document.getElementById('article-initial-changelog');

  if (titleInput) titleInput.value = `[Protocolo] Solución para: ${ticket.title || 'Incidente'}`;
  
  // Asignar categoría adecuada según plataforma
  if (catSelect) {
    const plat = (ticket.platform_id || '').toLowerCase();
    if (plat.includes('rec')) catSelect.value = 'Receta Digital';
    else if (plat.includes('tele')) catSelect.value = 'Telemedicina';
    else if (plat.includes('ehr') || plat.includes('hist')) catSelect.value = 'Historia Clínica';
    else if (plat.includes('farm')) catSelect.value = 'Facturación y Pagos';
    else if (plat.includes('lab') || plat.includes('dicom')) catSelect.value = 'Interoperabilidad';
    else catSelect.value = 'General';
  }

  if (tagsInput) tagsInput.value = `${ticket.id}, resolución, soporte-n2`;
  if (versionInput) versionInput.value = 'v1.0';
  if (changelogInput) changelogInput.value = `Promovido desde el ticket resuelto ${ticket.id}`;

  if (contentInput) {
    // Extraer notas de resolución si existen en comentarios
    const resNotes = (ticket.comments || [])
      .filter(c => c.is_internal || (c.content && c.content.toLowerCase().includes('soluci')))
      .map(c => c.content)
      .join('\n\n');

    contentInput.value = `1. DIAGNÓSTICO DEL INCONVENIENTE:\n${ticket.description || 'Problema reportado en producción.'}\n\n2. PROCEDIMIENTO TÉCNICO DE RESOLUCIÓN APLICADO:\n${resNotes || 'Verificación de conectividad y reintento de emisión homologada.'}\n\n3. VALIDACIÓN:\nConfirmación de operatividad con el profesional asistencial.`;
  }

  modal.classList.add('active');
}

// -----------------------------------------------------------------------------
// EVENT LISTENERS DE MODALES KB
// -----------------------------------------------------------------------------
function initArticleModalListeners() {
  const btnOpen = document.getElementById('btn-open-article-modal');
  const modalNew = document.getElementById('modal-new-article');
  const btnCloseNew = document.getElementById('modal-article-close');
  const btnCancelNew = document.getElementById('btn-cancel-article-modal');
  const formNew = document.getElementById('form-new-article');

  const modalEdit = document.getElementById('modal-edit-article');
  const btnCloseEdit = document.getElementById('modal-edit-article-close');
  const btnCancelEdit = document.getElementById('btn-cancel-edit-article-modal');
  const formEdit = document.getElementById('form-edit-article');

  const modalHistory = document.getElementById('modal-article-history');
  const btnCloseHistory = document.getElementById('modal-article-history-close');

  const modalView = document.getElementById('modal-view-article');
  const btnCloseView = document.getElementById('modal-view-article-close');

  const searchInput = document.getElementById('kb-search-input');

  // Modal Nuevo Artículo
  if (btnOpen && modalNew) {
    btnOpen.addEventListener('click', () => {
      if (formNew) formNew.reset();
      const verInp = document.getElementById('article-initial-version');
      const chgInp = document.getElementById('article-initial-changelog');
      if (verInp) verInp.value = 'v1.0';
      if (chgInp) chgInp.value = 'Versión inicial homologada para operación';
      modalNew.classList.add('active');
    });
  }
  if (btnCloseNew && modalNew) {
    btnCloseNew.addEventListener('click', () => modalNew.classList.remove('active'));
  }
  if (btnCancelNew && modalNew) {
    btnCancelNew.addEventListener('click', () => modalNew.classList.remove('active'));
  }

  if (formNew) {
    formNew.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById('article-title').value.trim(),
        category: document.getElementById('article-category').value,
        content: document.getElementById('article-content').value.trim(),
        tags: (document.getElementById('article-tags').value || '').trim(),
        version: (document.getElementById('article-initial-version').value || 'v1.0').trim(),
        changelog: (document.getElementById('article-initial-changelog').value || 'Versión inicial homologada').trim(),
        author_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
      };

      try {
        await API.createArticle(payload);
        modalNew.classList.remove('active');
        formNew.reset();
        showToast('🎉 ¡Protocolo publicado exitosamente en la Base de Conocimiento!', 'success');
        await loadKnowledgeBase('', AppState.kbSelectedCategory || '');
      } catch (err) {
        showToast('Error al publicar artículo en la base', 'error');
      }
    });
  }

  // Modal Editar / Nueva Versión
  if (btnCloseEdit && modalEdit) {
    btnCloseEdit.addEventListener('click', () => modalEdit.classList.remove('active'));
  }
  if (btnCancelEdit && modalEdit) {
    btnCancelEdit.addEventListener('click', () => modalEdit.classList.remove('active'));
  }

  if (formEdit) {
    formEdit.addEventListener('submit', async (e) => {
      e.preventDefault();
      const articleId = document.getElementById('edit-article-id').value;
      const newVersion = document.getElementById('edit-article-version-preview').value.trim() || 'v1.1';
      const changelog = document.getElementById('edit-article-changelog').value.trim();

      if (!changelog) {
        showToast('Debe ingresar un motivo del cambio para el registro histórico', 'error');
        return;
      }

      const payload = {
        title: document.getElementById('edit-article-title').value.trim(),
        category: document.getElementById('edit-article-category').value,
        tags: (document.getElementById('edit-article-tags').value || '').trim(),
        content: document.getElementById('edit-article-content').value.trim(),
        version: newVersion,
        changelog: changelog,
        author_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
      };

      try {
        await API.updateArticle(articleId, payload);
        modalEdit.classList.remove('active');
        showToast(`✨ ¡Nueva versión ${newVersion} guardada y auditada en el histórico!`, 'success');
        await loadKnowledgeBase('', AppState.kbSelectedCategory || '');
      } catch (err) {
        showToast('Error al actualizar versión del artículo', 'error');
      }
    });
  }

  // Modal Historial
  if (btnCloseHistory && modalHistory) {
    btnCloseHistory.addEventListener('click', () => modalHistory.classList.remove('active'));
  }

  // Modal Lector
  if (btnCloseView && modalView) {
    btnCloseView.addEventListener('click', () => modalView.classList.remove('active'));
  }

  // Cerrar modales con ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      [modalNew, modalEdit, modalHistory, modalView].forEach(m => {
        if (m && m.classList.contains('active')) m.classList.remove('active');
      });
    }
  });

  // Búsqueda en tiempo real con debounce
  if (searchInput) {
    searchInput.addEventListener('input', debounce(() => {
      loadKnowledgeBase(searchInput.value.trim(), AppState.kbSelectedCategory || '');
    }, 250));
  }
}


// =============================================================================
// 6. GESTIÓN MULTI-TENANT DE PLATAFORMAS E INSTITUCIONES
// =============================================================================
AppState.selectedTenantInst = 'OSDE';
AppState.tenantPlatforms = {
  'OSDE': { 'REC_DIGITAL': true, 'TELEMED': true, 'PORTAL_PAC': true, 'EHR_CORE': true, 'LAB_HL7': true, 'IMG_DICOM': true },
  'SWISS_MED': { 'REC_DIGITAL': true, 'TELEMED': true, 'PORTAL_PAC': true, 'EHR_CORE': true, 'FARM_HOSP': true },
  'GALENO': { 'REC_DIGITAL': true, 'TELEMED': true, 'EHR_CORE': true, 'LAB_HL7': true },
  'FINOCHIETTO': { 'REC_DIGITAL': true, 'EHR_CORE': true, 'LAB_HL7': true, 'IMG_DICOM': true, 'FARM_HOSP': true },
  'ITALIANO': { 'REC_DIGITAL': true, 'TELEMED': true, 'PORTAL_PAC': true, 'EHR_CORE': true, 'LAB_HL7': true, 'IMG_DICOM': true, 'FARM_HOSP': true, 'HIST_CLIN': true, 'APP_GUARDIA': true },
  'ALEMAN': { 'REC_DIGITAL': true, 'TELEMED': true, 'EHR_CORE': true, 'LAB_HL7': true, 'IMG_DICOM': true }
};

function selectTenantInstitution(instCode) {
  AppState.selectedTenantInst = instCode;
  renderPlatformsCatalog();
}

function toggleTenantPlatform(instCode, platCode) {
  if (!AppState.tenantPlatforms[instCode]) {
    AppState.tenantPlatforms[instCode] = {};
  }
  const current = !!AppState.tenantPlatforms[instCode][platCode];
  AppState.tenantPlatforms[instCode][platCode] = !current;
  
  const plat = AppState.platforms.find(p => p.code === platCode);
  const platName = plat ? plat.name : platCode;
  const inst = AppState.institutions.find(i => i.code === instCode);
  const instName = inst ? inst.name : instCode;

  showToast(`Plataforma "${platName}" ${!current ? 'habilitada' : 'desactivada'} para ${instName}`, !current ? 'success' : 'info');
  renderPlatformsCatalog();
}

function filterTenantInstitutions(query) {
  const q = (query || '').toLowerCase().trim();
  const instItems = document.querySelectorAll('.tenant-inst-item');
  instItems.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(q) ? 'flex' : 'none';
  });
}

function renderPlatformsCatalog() {
  const instListCont = document.getElementById('tenant-institutions-list');
  const platMgrCont = document.getElementById('tenant-platform-manager-panel');
  if (!instListCont || !platMgrCont) return;

  const currentInstCode = AppState.selectedTenantInst || (AppState.institutions[0] ? AppState.institutions[0].code : 'OSDE');
  const currentInst = AppState.institutions.find(i => i.code === currentInstCode) || { code: currentInstCode, name: currentInstCode, location: 'Sede Sanitaria' };

  // 1. Render Selector de Instituciones (Izquierda)
  instListCont.innerHTML = AppState.institutions.map(inst => {
    const isSelected = inst.code === currentInstCode;
    const activeCount = Object.values(AppState.tenantPlatforms[inst.code] || {}).filter(Boolean).length;
    return `
      <div class="tenant-inst-item ${isSelected ? 'active' : ''}" onclick="selectTenantInstitution('${inst.code}')" style="display:flex; align-items:center; justify-content:space-between; padding:12px 14px; border-radius:8px; margin-bottom:6px; cursor:pointer; background:${isSelected ? '#EFF6FF' : '#FFF'}; border:1.5px solid ${isSelected ? '#2563EB' : '#E2E8F0'}; transition:all 0.15s ease;">
        <div>
          <div style="font-size:12.5px; font-weight:800; color:${isSelected ? '#1E40AF' : 'var(--q-navy)'};">${inst.name}</div>
          <div style="font-size:10.5px; color:#64748B; margin-top:2px;"><code>${inst.code}</code> • 📍 ${inst.location || 'Sede Central'}</div>
        </div>
        <span style="font-size:10px; font-weight:800; padding:2px 7px; border-radius:4px; background:${isSelected ? '#DBEAFE' : '#F1F5F9'}; color:${isSelected ? '#1E40AF' : '#475569'};">
          ${activeCount} activas
        </span>
      </div>
    `;
  }).join('');

  // 2. Render Gestor de Plataformas y Mesas de Ayuda para la Institución Seleccionada (Derecha)
  const instConfig = AppState.tenantPlatforms[currentInstCode] || {};
  const activePlatforms = AppState.platforms.filter(p => !!instConfig[p.code]);

  platMgrCont.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid #E2E8F0;">
      <div>
        <div style="font-size:11px; font-weight:800; color:#2563EB; text-transform:uppercase; letter-spacing:0.5px;">Mesas de Ayuda Configuradas</div>
        <h2 style="font-family:'Outfit', sans-serif; font-size:17px; font-weight:800; color:var(--q-navy); margin:2px 0 0 0;">
          ${currentInst.name} (${currentInst.code})
        </h2>
      </div>
      <div style="display:flex; gap:8px; align-items:center;">
        <span style="font-size:11px; font-weight:700; color:#059669; background:#DCFCE7; padding:4px 10px; border-radius:6px; border:1px solid #86EFAC;">
          🟢 ${activePlatforms.length} de ${AppState.platforms.length} Plataformas Habilitadas
        </span>
      </div>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:12px;">
      ${AppState.platforms.map(plat => {
        const isEnabled = !!instConfig[plat.code];
        return `
          <div class="card" style="padding:14px; border-radius:10px; border:1px solid ${isEnabled ? '#99F6E4' : '#E2E8F0'}; background:${isEnabled ? '#F0FDFA' : '#FFF'}; display:flex; flex-direction:column; justify-content:space-between; transition:all 0.15s ease;">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                <strong style="font-size:13px; color:var(--q-navy);">${plat.name}</strong>
                <span style="font-size:9.5px; font-family:'JetBrains Mono'; background:#E2E8F0; padding:2px 6px; border-radius:4px; color:#334155;">${plat.code}</span>
              </div>
              <p style="font-size:11.5px; color:#64748B; line-height:1.4; margin-bottom:10px;">${plat.description || 'Módulo asistencial integrado'}</p>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid ${isEnabled ? '#CCFBF1' : '#F1F5F9'}; padding-top:10px;">
              <span style="font-size:11px; font-weight:700; color:${isEnabled ? '#0F766E' : '#94A3B8'};">
                ${isEnabled ? '🟢 En Producción' : '⚪ Deshabilitada'}
              </span>
              <button class="${isEnabled ? 'btn-pri' : 'btn-sec'}" onclick="toggleTenantPlatform('${currentInstCode}', '${plat.code}')" style="font-size:11px; padding:5px 12px; font-weight:700; ${isEnabled ? 'background:#0D9488;' : ''}">
                ${isEnabled ? '✓ Habilitada' : '+ Activar Mesa'}
              </button>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

// =============================================================================
// 7. DIRECTORIO DE USUARIOS & ROLES ITIL
// =============================================================================
async function loadUsersList() {
  try {
    AppState.users = await API.getUsers();
    renderUsersDirectory();
    populateAuthModalAccounts();
  } catch (err) {
    console.error('Error cargando usuarios:', err);
  }
}

function filterUsersByLevel(lvl) {
  AppState.userFilterLevel = lvl;
  document.querySelectorAll('[data-user-filter]').forEach(btn => {
    if (btn.dataset.userFilter === lvl) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  renderUsersDirectory();
}

function renderUsersDirectory() {
  const tbody = document.getElementById('tbody-users-directory');
  if (!tbody) return;

  let filtered = AppState.users || [];
  if (AppState.userFilterLevel && AppState.userFilterLevel !== 'all') {
    if (AppState.userFilterLevel === 'SOLICITANTE') {
      filtered = filtered.filter(u => u.role === 'SOLICITANTE');
    } else {
      filtered = filtered.filter(u => u.support_level === AppState.userFilterLevel || u.role === `SOPORTE_${AppState.userFilterLevel}`);
    }
  }

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:#94A3B8; padding:24px 10px;">No se encontraron usuarios para el filtro seleccionado.</td></tr>`;
    return;
  }

  const levelBadges = {
    'N1': '<span class="badge-tier badge-tier-n1">🔵 Nivel 1 • Triage</span>',
    'N2': '<span class="badge-tier badge-tier-n2">🟣 Nivel 2 • Especialista</span>',
    'N3': '<span class="badge-tier badge-tier-n3">🔴 Nivel 3 • Ingeniería</span>'
  };

  tbody.innerHTML = filtered.map(u => {
    const lvlBadge = levelBadges[u.support_level] || (u.role && u.role.includes('SOPORTE') ? `<span class="badge-tier badge-tier-${(u.support_level||'n1').toLowerCase()}">${u.support_level || 'N1'}</span>` : '<span style="font-size:10.5px; color:#64748B;">No aplica</span>');
    return `
      <tr>
        <td><strong>${u.full_name}</strong></td>
        <td><code>${u.username}</code></td>
        <td><a href="mailto:${u.email}" style="color:#2563EB;">${u.email}</a></td>
        <td><span class="badge-status st-NUEVO" style="font-size:10px;">${u.role}</span></td>
        <td>${lvlBadge}</td>
        <td>🏥 ${formatInstitutionName(u.institution_code)}</td>
        <td>${u.specialty || 'General / Asistencial'}</td>
        <td><span style="color:#059669; font-weight:800; font-size:11px;">🟢 Activo</span></td>
      </tr>
    `;
  }).join('');
}

// =============================================================================
// 8. CONFIGURACIÓN DEL SISTEMA, SLAS & MESAS DE AYUDA ITIL (N1 / N2 / N3)
// =============================================================================
async function loadSystemConfig() {
  try {
    const cfg = await API.getConfig();
    AppState.systemConfig = cfg;
    renderSystemConfig(cfg);
  } catch (err) {
    console.error('Error cargando configuración global:', err);
  }
}

function renderSystemConfig(cfg) {
  if (!cfg) return;
  const fields = {
    'cfg-sla-p1-resp': cfg.sla_p1_response,
    'cfg-sla-p1-resol': cfg.sla_p1_resolution,
    'cfg-sla-p2-resp': cfg.sla_p2_response,
    'cfg-sla-p2-resol': cfg.sla_p2_resolution,
    'cfg-sla-p3-resp': cfg.sla_p3_response,
    'cfg-sla-p3-resol': cfg.sla_p3_resolution,
    'cfg-sla-p4-resp': cfg.sla_p4_response,
    'cfg-sla-p4-resol': cfg.sla_p4_resolution,
    'cfg-sla-p5-resp': cfg.sla_p5_response,
    'cfg-sla-p5-resol': cfg.sla_p5_resolution
  };

  Object.entries(fields).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.value = val;
  });

  const notifyP1 = document.getElementById('cfg-notify-p1');
  const requireWork = document.getElementById('cfg-require-workaround');
  if (notifyP1 && cfg.notify_p1_critical !== undefined) notifyP1.checked = cfg.notify_p1_critical;
  if (requireWork && cfg.require_resolution_note !== undefined) requireWork.checked = cfg.require_resolution_note;
}

async function saveSystemConfig() {
  const payload = {
    sla_p1_response: parseInt(document.getElementById('cfg-sla-p1-resp').value) || 15,
    sla_p1_resolution: parseInt(document.getElementById('cfg-sla-p1-resol').value) || 120,
    sla_p2_response: parseInt(document.getElementById('cfg-sla-p2-resp').value) || 30,
    sla_p2_resolution: parseInt(document.getElementById('cfg-sla-p2-resol').value) || 480,
    sla_p3_response: parseInt(document.getElementById('cfg-sla-p3-resp').value) || 60,
    sla_p3_resolution: parseInt(document.getElementById('cfg-sla-p3-resol').value) || 1440,
    sla_p4_response: parseInt(document.getElementById('cfg-sla-p4-resp').value) || 120,
    sla_p4_resolution: parseInt(document.getElementById('cfg-sla-p4-resol').value) || 2880,
    sla_p5_response: parseInt(document.getElementById('cfg-sla-p5-resp').value) || 240,
    sla_p5_resolution: parseInt(document.getElementById('cfg-sla-p5-resol').value) || 4320,
    notify_p1_critical: document.getElementById('cfg-notify-p1') ? document.getElementById('cfg-notify-p1').checked : true,
    require_resolution_note: document.getElementById('cfg-require-workaround') ? document.getElementById('cfg-require-workaround').checked : true
  };

  try {
    await API.updateConfig(payload);
    showToast('¡Configuración de SLAs y políticas operativas guardada con éxito!', 'success');
  } catch (err) {
    showToast('Error al guardar configuración de SLAs', 'error');
  }
}

async function loadHelpdeskLevelsConfig() {
  const container = document.getElementById('helpdesk-levels-container');
  try {
    const levels = await API.getHelpdeskLevels();
    AppState.helpdeskLevels = levels;
    renderHelpdeskLevelsConfig(levels);
  } catch (err) {
    console.error('Error cargando configuración de niveles de soporte:', err);
    if (container) {
      container.innerHTML = `<div style="color:#EF4444; padding:12px; font-weight:700;">Error al cargar la configuración de niveles de mesa de ayuda.</div>`;
    }
  }
}

function renderHelpdeskLevelsConfig(levels) {
  const container = document.getElementById('helpdesk-levels-container');
  if (!container || !levels) return;

  const levelStyles = {
    'N1': { border: 'card-n1', badgeClass: 'badge-tier-n1', icon: '🔵', title: 'Nivel 1 • Triage & Recepción Asistencial', badgeText: 'N1 • FIRST CONTACT' },
    'N2': { border: 'card-n2', badgeClass: 'badge-tier-n2', icon: '🟣', title: 'Nivel 2 • Soporte Especializado por Módulo', badgeText: 'N2 • ESPECIALISTAS' },
    'N3': { border: 'card-n3', badgeClass: 'badge-tier-n3', icon: '🔴', title: 'Nivel 3 • Ingeniería de Software, Cloud & DBA', badgeText: 'N3 • INGENIERÍA' }
  };

  container.innerHTML = levels.map(lvl => {
    const style = levelStyles[lvl.code] || levelStyles['N1'];
    const teams = lvl.teams || [];
    const operators = lvl.assigned_operators || [];

    return `
      <div class="level-card ${style.border}" id="level-card-${lvl.code}">
        
        <!-- Header de la Tarjeta del Nivel -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
          <div>
            <div class="badge-tier ${style.badgeClass}" style="margin-bottom:4px;">
              ${style.icon} ${style.badgeText}
            </div>
            <h3 style="font-family:'Outfit', sans-serif; font-size:14px; font-weight:800; color:#0F172A; margin:0;">
              ${lvl.name}
            </h3>
          </div>
          <span style="font-size:11px; font-weight:800; background:#F1F5F9; color:#475569; padding:2px 8px; border-radius:12px;">
            ${teams.length} Mesas Activas
          </span>
        </div>

        <p style="font-size:11.5px; color:#475569; line-height:1.4; margin:0 0 10px 0;">
          ${lvl.description || 'Nivel de atención del servicio de soporte.'}
        </p>

        <!-- Parámetros Operativos Editables -->
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:8px;">
          <div style="font-size:10.5px; font-weight:800; color:#334155; text-transform:uppercase; letter-spacing:0.3px;">
            ⚙️ Parámetros del Nivel
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div>
              <label style="font-size:10px; font-weight:700; color:#64748B; display:block; margin-bottom:2px;">SLA Retención Máx:</label>
              <input type="text" id="cfg-lvl-${lvl.code}-sla" class="form-control" style="font-size:11.5px; height:30px; font-weight:700;" value="${lvl.retention_sla_max || ''}">
            </div>
            <div>
              <label style="font-size:10px; font-weight:700; color:#64748B; display:block; margin-bottom:2px;">Modo de Despacho:</label>
              <select id="cfg-lvl-${lvl.code}-dispatch" class="form-control" style="font-size:11px; height:30px; font-weight:700;">
                <option value="ROUND_ROBIN" ${lvl.dispatch_mode === 'ROUND_ROBIN' ? 'selected' : ''}>🔄 Round Robin</option>
                <option value="SPECIALTY" ${lvl.dispatch_mode === 'SPECIALTY' ? 'selected' : ''}>🩺 Por Especialidad</option>
                <option value="WORKLOAD" ${lvl.dispatch_mode === 'WORKLOAD' ? 'selected' : ''}>⚖️ Menor Carga</option>
                <option value="CRITICALITY" ${lvl.dispatch_mode === 'CRITICALITY' ? 'selected' : ''}>🚨 Severidad P1</option>
              </select>
            </div>
          </div>

          <div>
            <label style="font-size:10px; font-weight:700; color:#64748B; display:block; margin-bottom:2px;">Auto-escalamiento si vence:</label>
            <select id="cfg-lvl-${lvl.code}-auto" class="form-control" style="font-size:11px; height:30px; font-weight:700;">
              <option value="" ${!lvl.auto_escalate_target ? 'selected' : ''}>-- Sin auto-escalamiento --</option>
              <option value="N2" ${lvl.auto_escalate_target === 'N2' ? 'selected' : ''}>🟣 Escalar a Nivel 2 (Especialistas)</option>
              <option value="N3" ${lvl.auto_escalate_target === 'N3' ? 'selected' : ''}>🔴 Escalar a Nivel 3 (Ingeniería)</option>
            </select>
          </div>
        </div>

        <!-- Colas / Mesas Especializadas -->
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:11px; font-weight:800; color:#334155; text-transform:uppercase;">Mesas Especializadas:</span>
            <button type="button" class="btn-sec" onclick="openAddTeamModal('${lvl.code}')" style="font-size:10px; padding:2px 6px; font-weight:700;">+ Mesa</button>
          </div>
          <div style="display:flex; flex-direction:column; gap:4px;">
            ${teams.map(t => `
              <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:6px; padding:6px 10px; display:flex; justify-content:space-between; align-items:center; font-size:11px;">
                <div>
                  <strong style="color:#0F172A;">${t.team_name}</strong>
                  <div style="font-size:10px; color:#64748B;">🕒 ${t.shift || '24/7'} • Resp: ${t.lead || 'Sin Lead'}</div>
                </div>
                <span style="font-size:9.5px; font-weight:800; background:#F1F5F9; color:#475569; padding:2px 6px; border-radius:4px;">
                  ${t.active_operators_count || 1} op.
                </span>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Operadores Asignados -->
        <div>
          <div style="font-size:10.5px; font-weight:800; color:#64748B; text-transform:uppercase; margin-bottom:4px;">
            Operadores Asignados (${operators.length}):
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:4px;">
            ${operators.map(op => `
              <span style="font-size:10px; background:#EFF6FF; color:#1E40AF; border:1px solid #DBEAFE; padding:2px 6px; border-radius:12px; font-weight:700;">
                👤 ${op}
              </span>
            `).join('')}
          </div>
        </div>

        <!-- Botón Guardar Nivel -->
        <div style="margin-top:auto; padding-top:8px; border-top:1px solid #F1F5F9; display:flex; justify-content:flex-end;">
          <button type="button" class="btn-pri" onclick="saveHelpdeskLevelConfig('${lvl.code}')" style="font-size:11px; padding:5px 12px; font-weight:800;">
            💾 Guardar ${lvl.code}
          </button>
        </div>

      </div>
    `;
  }).join('');
}

async function saveHelpdeskLevelConfig(levelCode) {
  const slaInput = document.getElementById(`cfg-lvl-${levelCode}-sla`);
  const dispatchInput = document.getElementById(`cfg-lvl-${levelCode}-dispatch`);
  const autoInput = document.getElementById(`cfg-lvl-${levelCode}-auto`);

  const payload = {
    retention_sla_max: slaInput ? slaInput.value.trim() : '',
    dispatch_mode: dispatchInput ? dispatchInput.value : 'ROUND_ROBIN',
    auto_escalate_target: autoInput ? (autoInput.value || null) : null
  };

  try {
    await API.updateHelpdeskLevel(levelCode, payload);
    showToast(`¡Configuración de ${levelCode} actualizada exitosamente!`, 'success');
    await loadHelpdeskLevelsConfig();
  } catch (err) {
    showToast(`Error al guardar configuración de ${levelCode}`, 'error');
  }
}

async function saveAllHelpdeskLevels() {
  const codes = ['N1', 'N2', 'N3'];
  for (const code of codes) {
    const slaInput = document.getElementById(`cfg-lvl-${code}-sla`);
    const dispatchInput = document.getElementById(`cfg-lvl-${code}-dispatch`);
    const autoInput = document.getElementById(`cfg-lvl-${code}-auto`);
    if (slaInput && dispatchInput) {
      await API.updateHelpdeskLevel(code, {
        retention_sla_max: slaInput.value.trim(),
        dispatch_mode: dispatchInput.value,
        auto_escalate_target: autoInput ? (autoInput.value || null) : null
      });
    }
  }
  showToast('¡Configuración de todos los niveles N1, N2 y N3 guardada con éxito!', 'success');
  await loadHelpdeskLevelsConfig();
}

// =============================================================================
// 9. MODALES DE GESTIÓN, DERIVACIÓN ITIL & OPERADORES
// =============================================================================
function initModalListeners() {
  const btnOpen = document.getElementById('btn-open-modal');
  const modal = document.getElementById('modal-ticket');
  const btnClose = document.getElementById('modal-close');
  const btnCancel = document.getElementById('btn-cancel-modal');
  const form = document.getElementById('form-new-ticket');

  const impactSel = document.getElementById('modal-impact');
  const urgencySel = document.getElementById('modal-urgency');
  const prioBadge = document.getElementById('modal-calculated-priority');

  const updateModalPriority = async () => {
    if (!impactSel || !urgencySel || !prioBadge) return;
    try {
      const res = await API.calculatePriority(impactSel.value, urgencySel.value);
      prioBadge.textContent = `${res.priority} - Resp: ${res.sla_response_time_minutes}m / Resol: ${res.sla_resolution_time_minutes >= 60 ? (res.sla_resolution_time_minutes/60) + 'h' : res.sla_resolution_time_minutes + 'm'}`;
      prioBadge.className = `badge-prio badge-${res.priority.toLowerCase()}`;
    } catch {
      // Fallback
    }
  };

  if (impactSel) impactSel.addEventListener('change', updateModalPriority);
  if (urgencySel) urgencySel.addEventListener('change', updateModalPriority);

  if (btnOpen) {
    btnOpen.addEventListener('click', () => {
      modal.classList.add('active');
      updateModalPriority();
    });
  }
  const btnTopOpen = document.getElementById('btn-top-new-ticket');
  if (btnTopOpen) {
    btnTopOpen.addEventListener('click', () => {
      modal.classList.add('active');
      updateModalPriority();
    });
  }
  if (btnClose) btnClose.addEventListener('click', () => modal.classList.remove('active'));
  if (btnCancel) btnCancel.addEventListener('click', () => modal.classList.remove('active'));

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById('modal-title').value.trim(),
        description: document.getElementById('modal-description').value.trim(),
        platform_code: document.getElementById('modal-platform').value,
        institution_code: document.getElementById('modal-institution').value,
        impact: document.getElementById('modal-impact').value,
        urgency: document.getElementById('modal-urgency').value,
        ticket_type: document.getElementById('modal-type') ? document.getElementById('modal-type').value : 'INCIDENTE',
        attachment_url: (document.getElementById('modal-attachment-url') && document.getElementById('modal-attachment-url').value.trim()) || null,
        requester_username: AppState.currentUser.username
      };

      try {
        const created = await API.createTicket(payload);
        modal.classList.remove('active');
        form.reset();
        showToast(`¡Solicitud #${created.id} creada con éxito! Prioridad asignada: ${created.priority}`, 'success');
        await loadTickets();
        await loadDashboardMetrics(AppState.currentDashInst);
        selectTicket(created.id, true);
        switchView('tickets');
      } catch (err) {
        showToast('Error al crear la solicitud: ' + (err.detail || 'Verifique los campos requeridos'), 'error');
      }
    });
  }

  // Modal Resolver Ticket (Senior UX v3.0)
  const modalResolve = document.getElementById('modal-resolve-ticket');
  const btnCloseResolve = document.getElementById('modal-resolve-close');
  const btnCancelResolve = document.getElementById('btn-cancel-resolve-modal');
  const formResolve = document.getElementById('form-resolve-ticket');

  if (btnCloseResolve && modalResolve) {
    btnCloseResolve.addEventListener('click', () => modalResolve.classList.remove('active'));
  }
  if (btnCancelResolve && modalResolve) {
    btnCancelResolve.addEventListener('click', () => modalResolve.classList.remove('active'));
  }
  if (formResolve) {
    formResolve.addEventListener('submit', async (e) => {
      e.preventDefault();
      const ticketId = document.getElementById('resolve-ticket-id').value;
      const rootCause = document.getElementById('resolve-root-cause').value.trim();
      const notes = document.getElementById('resolve-notes').value.trim();
      const isWorkaround = document.getElementById('resolve-is-workaround').checked;
      const publishKb = document.getElementById('resolve-publish-kb').checked;

      if (notes.length < 8) {
        showToast('La solución técnica debe contener al menos 8 caracteres explicativos', 'error');
        return;
      }

      try {
        await API.resolveTicket(ticketId, {
          root_cause: rootCause || null,
          resolution_notes: notes,
          is_workaround: isWorkaround,
          resolved_by_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
        });

        if (publishKb && AppState.selectedTicket) {
          try {
            await API.createArticle({
              title: `[Solución] ${AppState.selectedTicket.title}`,
              category: 'General',
              content: `1. CAUSA RAÍZ:\n${rootCause || 'Diagnóstico operativo'}\n\n2. PROCEDIMIENTO TÉCNICO:\n${notes}\n\n3. RESULTADO:\nSolución confirmada y homologada.`,
              tags: `${ticketId}, resolucion, itil`,
              version: 'v1.0',
              changelog: `Creado desde ticket #${ticketId}`,
              author_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
            });
            showToast('📚 ¡Protocolo publicado también en la Base de Conocimiento!', 'success');
          } catch (kberr) {
            console.error('Error auto-publicando KB:', kberr);
          }
        }

        modalResolve.classList.remove('active');
        showToast(`✅ ¡Solicitud #${ticketId} marcada como solucionada!`, 'success');
        await loadTickets();
        await selectTicket(ticketId, true);
        await loadDashboardMetrics(AppState.currentDashInst);
      } catch (err) {
        showToast('Error al resolver solicitud: ' + (err.detail || err.message || 'Verifique los datos'), 'error');
      }
    });
  }

  // Modal Reasignar Ticket (Senior UX v3.0)
  const modalReassign = document.getElementById('modal-reassign-ticket');
  const btnCloseReassign = document.getElementById('modal-reassign-close');
  const btnCancelReassign = document.getElementById('btn-cancel-reassign-modal');
  const formReassign = document.getElementById('form-reassign-ticket');

  if (btnCloseReassign && modalReassign) {
    btnCloseReassign.addEventListener('click', () => modalReassign.classList.remove('active'));
  }
  if (btnCancelReassign && modalReassign) {
    btnCancelReassign.addEventListener('click', () => modalReassign.classList.remove('active'));
  }
  if (formReassign) {
    formReassign.addEventListener('submit', async (e) => {
      e.preventDefault();
      const ticketId = document.getElementById('reassign-ticket-id').value;
      const op = document.getElementById('reassign-operator-select').value;
      const lvl = document.getElementById('reassign-level-select').value;
      const reason = document.getElementById('reassign-reason').value.trim() || `Derivación a nivel ${lvl}`;

      if (!op) {
        showToast('Seleccione un operador para derivar la solicitud', 'error');
        return;
      }

      try {
        await API.assignTicket(ticketId, {
          assignee_username: op,
          support_level: lvl,
          reason: reason,
          changed_by_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
        });

        modalReassign.classList.remove('active');
        showToast(`👥 ¡Solicitud #${ticketId} reasignada a @${op} (${lvl})!`, 'success');
        await loadTickets();
        await selectTicket(ticketId, true);
        await loadDashboardMetrics(AppState.currentDashInst);
      } catch (err) {
        showToast('Error al reasignar solicitud: ' + (err.detail || err.message || 'Error en servidor'), 'error');
      }
    });
  }
}

function initEditModalListeners() {
  const modal = document.getElementById('modal-edit-ticket');
  const btnClose = document.getElementById('modal-edit-close');
  const btnCancel = document.getElementById('btn-cancel-edit-modal');
  const form = document.getElementById('form-edit-ticket');
  const impactSel = document.getElementById('edit-impact');
  const urgencySel = document.getElementById('edit-urgency');
  const prioBadge = document.getElementById('edit-calculated-priority');

  const updateEditPriority = async () => {
    if (!impactSel || !urgencySel || !prioBadge) return;
    try {
      const res = await API.calculatePriority(impactSel.value, urgencySel.value);
      prioBadge.textContent = `${res.priority} - Resp: ${res.sla_response_time_minutes}m / Resol: ${res.sla_resolution_time_minutes >= 60 ? (res.sla_resolution_time_minutes/60) + 'h' : res.sla_resolution_time_minutes + 'm'}`;
      prioBadge.className = `badge-prio badge-${res.priority.toLowerCase()}`;
    } catch {
      // Fallback
    }
  };

  if (impactSel) impactSel.addEventListener('change', updateEditPriority);
  if (urgencySel) urgencySel.addEventListener('change', updateEditPriority);

  if (btnClose) btnClose.addEventListener('click', () => modal.classList.remove('active'));
  if (btnCancel) btnCancel.addEventListener('click', () => modal.classList.remove('active'));

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const ticketId = document.getElementById('edit-ticket-id').value;
      const payload = {
        title: document.getElementById('edit-title').value.trim(),
        description: document.getElementById('edit-description').value.trim(),
        platform_code: document.getElementById('edit-platform').value,
        institution_code: document.getElementById('edit-institution').value,
        impact: document.getElementById('edit-impact').value,
        urgency: document.getElementById('edit-urgency').value
      };

      try {
        const updated = await API.updateTicket(ticketId, payload);
        modal.classList.remove('active');
        showToast(`¡Solicitud #${ticketId} actualizada exitosamente! Nueva prioridad: ${updated.priority}`, 'success');
        await loadTickets();
        await selectTicket(ticketId, true);
      } catch (err) {
        showToast('Error al actualizar: ' + (err.detail || 'Solo permitido en estado NUEVO'), 'error');
      }
    });
  }
}

function openEditTicketModal(ticketId) {
  const modal = document.getElementById('modal-edit-ticket');
  if (!modal) return;
  const ticket = AppState.tickets.find(t => t.id === ticketId) || AppState.selectedTicket;
  if (!ticket) return;

  if (ticket.status !== 'NUEVO') {
    showToast('Solo es posible editar solicitudes que se encuentren en estado NUEVO', 'error');
    return;
  }

  document.getElementById('edit-ticket-id').value = ticket.id;
  const displayId = document.getElementById('edit-modal-ticket-id-display');
  if (displayId) displayId.textContent = ticket.id;
  
  document.getElementById('edit-title').value = ticket.title || '';
  document.getElementById('edit-description').value = ticket.description || '';
  
  const platSel = document.getElementById('edit-platform');
  const instSel = document.getElementById('edit-institution');
  if (platSel) {
    platSel.innerHTML = AppState.platforms.map(p => `<option value="${p.code}" ${p.code === ticket.platform_code ? 'selected' : ''}>${p.name}</option>`).join('');
  }
  if (instSel) {
    instSel.innerHTML = AppState.institutions.map(i => `<option value="${i.code}" ${i.code === ticket.institution_code ? 'selected' : ''}>${i.name}</option>`).join('');
  }

  document.getElementById('edit-impact').value = ticket.impact || 'MEDIO';
  document.getElementById('edit-urgency').value = ticket.urgency || 'MEDIO';

  const prioBadge = document.getElementById('edit-calculated-priority');
  if (prioBadge) {
    prioBadge.textContent = ticket.priority;
    prioBadge.className = `badge-prio badge-${(ticket.priority || 'P3').toLowerCase()}`;
  }

  modal.classList.add('active');
}

function initUserModalListeners() {
  const btnOpen = document.getElementById('btn-open-user-modal');
  const modal = document.getElementById('modal-user');
  const btnClose = document.getElementById('modal-user-close');
  const btnCancel = document.getElementById('btn-cancel-user-modal');
  const form = document.getElementById('form-new-user');

  if (btnOpen) btnOpen.addEventListener('click', () => modal.classList.add('active'));
  if (btnClose) btnClose.addEventListener('click', () => modal.classList.remove('active'));
  if (btnCancel) btnCancel.addEventListener('click', () => modal.classList.remove('active'));

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        full_name: document.getElementById('user-fullname').value.trim(),
        username: document.getElementById('user-username').value.trim(),
        role: document.getElementById('user-role').value,
        support_level: document.getElementById('user-support-level') ? document.getElementById('user-support-level').value || null : null,
        email: document.getElementById('user-email').value.trim(),
        institution_code: document.getElementById('user-institution').value
      };

      try {
        await API.createUser(payload);
        modal.classList.remove('active');
        form.reset();
        showToast(`Usuario ${payload.full_name} dado de alta exitosamente`, 'success');
        await loadUsersList();
        renderUsersDirectory();
      } catch (err) {
        showToast('Error al dar de alta el usuario', 'error');
      }
    });
  }
}

// 9.1 MODAL DE ESCALAMIENTO ITIL (N1 ➔ N2 ➔ N3)
function openEscalateModal(ticketId, currentLevel) {
  const modal = document.getElementById('modal-escalate-ticket');
  if (!modal) return;

  document.getElementById('escalate-ticket-id').value = ticketId;
  const displayId = document.getElementById('escalate-modal-ticket-id-display');
  if (displayId) displayId.textContent = ticketId;

  const targetSelect = document.getElementById('escalate-target-level');
  if (targetSelect) {
    if (currentLevel === 'N1') targetSelect.value = 'N2';
    else if (currentLevel === 'N2') targetSelect.value = 'N3';
    else targetSelect.value = 'N1';
    
    // Asignar listener para cambio dinámico de operadores si no está asignado
    targetSelect.onchange = (e) => onEscalateTargetLevelChange(e.target.value);
  }

  onEscalateTargetLevelChange(targetSelect ? targetSelect.value : 'N2');
  const reasonEl = document.getElementById('escalate-reason');
  if (reasonEl) reasonEl.value = '';

  modal.classList.add('active');
}

function onEscalateTargetLevelChange(targetLevel) {
  const opSelect = document.getElementById('escalate-assignee-operator');
  if (!opSelect) return;

  const eligibleOps = (AppState.users || []).filter(u => u.support_level === targetLevel || u.role === `SOPORTE_${targetLevel}` || u.role === 'ADMIN');
  opSelect.innerHTML = '<option value="">-- Asignación automática por Despacho del Nivel --</option>' +
    eligibleOps.map(u => `<option value="${u.username}">👤 ${u.full_name} (@${u.username})</option>`).join('');
}

function initEscalateModalListeners() {
  const modal = document.getElementById('modal-escalate-ticket');
  const btnClose = document.getElementById('modal-escalate-close');
  const btnCancel = document.getElementById('btn-cancel-escalate-modal');
  const form = document.getElementById('form-escalate-ticket');

  if (btnClose && modal) btnClose.addEventListener('click', () => modal.classList.remove('active'));
  if (btnCancel && modal) btnCancel.addEventListener('click', () => modal.classList.remove('active'));

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const ticketId = document.getElementById('escalate-ticket-id').value;
      const targetLevel = document.getElementById('escalate-target-level').value;
      const assignee = document.getElementById('escalate-assignee-operator').value || null;
      const reason = document.getElementById('escalate-reason').value.trim();

      const payload = {
        target_level: targetLevel,
        assignee_username: assignee,
        reason: reason,
        changed_by_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
      };

      try {
        await API.escalateTicket(ticketId, payload);
        modal.classList.remove('active');
        showToast(`⚡ ¡Ticket #${ticketId} derivado exitosamente al Nivel ${targetLevel}!`, 'success');
        await loadTickets();
        await selectTicket(ticketId, true);
      } catch (err) {
        showToast('Error al escalar ticket: ' + (err.detail || 'Operación rechazada'), 'error');
      }
    });
  }
}

// 9.2 MODAL DE NUEVA MESA ESPECIALIZADA POR NIVEL
function openAddTeamModal(levelCode = 'N2') {
  const modal = document.getElementById('modal-new-helpdesk-team');
  if (!modal) return;
  const targetSel = document.getElementById('team-target-level');
  if (targetSel) targetSel.value = levelCode;
  const form = document.getElementById('form-new-helpdesk-team');
  if (form) form.reset();
  if (targetSel) targetSel.value = levelCode;
  modal.classList.add('active');
}

function initHelpdeskTeamModalListeners() {
  const modal = document.getElementById('modal-new-helpdesk-team');
  const btnClose = document.getElementById('modal-new-team-close');
  const btnCancel = document.getElementById('btn-cancel-team-modal');
  const form = document.getElementById('form-new-helpdesk-team');

  if (btnClose && modal) btnClose.addEventListener('click', () => modal.classList.remove('active'));
  if (btnCancel && modal) btnCancel.addEventListener('click', () => modal.classList.remove('active'));

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const levelCode = document.getElementById('team-target-level').value;
      const rawPlats = document.getElementById('team-platforms').value;
      const platformsList = rawPlats ? rawPlats.split(',').map(s => s.trim().toUpperCase()).filter(Boolean) : [];

      const payload = {
        team_name: document.getElementById('team-name').value.trim(),
        shift: document.getElementById('team-shift').value,
        lead: document.getElementById('team-lead').value.trim() || 'Supervisor del Nivel',
        platforms: platformsList,
        active_operators_count: 1
      };

      try {
        await API.addTeamToHelpdeskLevel(levelCode, payload);
        modal.classList.remove('active');
        form.reset();
        showToast(`¡Mesa "${payload.team_name}" creada en ${levelCode}!`, 'success');
        await loadHelpdeskLevelsConfig();
      } catch (err) {
        showToast('Error al crear mesa especializada', 'error');
      }
    });
  }
}

// =============================================================================
// 10. FILTROS DE BANDEJA & PRESETS ITIL
// =============================================================================
function applyTicketPreset(preset) {
  AppState.ticketFilterPreset = preset;
  renderSubNavRibbon('tickets');

  const params = {};

  // Mapeo de presets de estado
  if (preset === 'new') params.status = 'NUEVO';
  else if (preset === 'in_progress') params.status = 'EN_CURSO';
  else if (preset === 'resolved') params.status = 'RESUELTO';
  else if (preset === 'closed') params.status = 'CERRADO';
  else if (preset === 'mine' && AppState.currentUser) {
    if (AppState.currentUser.role === 'SOLICITANTE') {
      params.requester_username = AppState.currentUser.username;
    } else {
      params.assignee_username = AppState.currentUser.username;
    }
  }

  // Mapeo de presets directos de prioridad ITIL (P1 a P5)
  const prioPills = ['p1', 'p2', 'p3', 'p4', 'p5'];
  const filterPrio = document.getElementById('filter-priority');
  const colFilterPrio = document.getElementById('col-filter-priority');

  if (prioPills.includes(preset)) {
    params.priority = preset.toUpperCase();
    if (filterPrio) filterPrio.value = params.priority;
    if (colFilterPrio) colFilterPrio.value = params.priority;
  } else {
    const selectedPrio = (filterPrio && filterPrio.value) || (colFilterPrio && colFilterPrio.value);
    if (selectedPrio) {
      params.priority = selectedPrio;
    }
  }

  const search = document.getElementById('search-input');
  if (search && search.value.trim()) {
    params.search = search.value.trim();
  }

  const plat = document.getElementById('filter-platform');
  const inst = document.getElementById('filter-institution');
  const colInst = document.getElementById('col-filter-institution');
  const colFilterLevel = document.getElementById('col-filter-level');
  const selectedInst = (inst && inst.value) || (colInst && colInst.value);

  if (plat && plat.value) params.platform_code = plat.value;
  if (selectedInst) params.institution_code = selectedInst;
  if (colFilterLevel && colFilterLevel.value) params.support_level = colFilterLevel.value;

  loadTickets(params);
}

function initFilterListeners() {
  const search = document.getElementById('search-input');
  const btnCsv = document.getElementById('btn-export-csv');
  const btnRefresh = document.getElementById('btn-refresh');

  const filterInst = document.getElementById('filter-institution');
  const colFilterInst = document.getElementById('col-filter-institution');
  const filterPrio = document.getElementById('filter-priority');
  const colFilterPrio = document.getElementById('col-filter-priority');
  const colFilterLevel = document.getElementById('col-filter-level');
  const filterPlat = document.getElementById('filter-platform');

  const applyFilters = () => {
    const params = {};
    const preset = AppState.ticketFilterPreset || 'all';

    if (preset === 'new') params.status = 'NUEVO';
    else if (preset === 'in_progress') params.status = 'EN_CURSO';
    else if (preset === 'p1') params.priority = 'P1';
    else if (preset === 'p2') params.priority = 'P2';
    else if (preset === 'p3') params.priority = 'P3';
    else if (preset === 'p4') params.priority = 'P4';
    else if (preset === 'p5') params.priority = 'P5';
    else if (preset === 'resolved') params.status = 'RESUELTO';
    else if (preset === 'closed') params.status = 'CERRADO';
    else if (preset === 'mine' && AppState.currentUser) {
      if (AppState.currentUser.role === 'SOLICITANTE') {
        params.requester_username = AppState.currentUser.username;
      } else {
        params.assignee_username = AppState.currentUser.username;
      }
    }

    // Prioridad explícita desde los dropdowns
    const selectedPrio = (filterPrio && filterPrio.value) || (colFilterPrio && colFilterPrio.value);
    if (selectedPrio) {
      params.priority = selectedPrio;
    }

    // Institución explícita desde los dropdowns
    const selectedInst = (filterInst && filterInst.value) || (colFilterInst && colFilterInst.value);
    if (selectedInst) {
      params.institution_code = selectedInst;
    }

    // Filtro de Nivel de Atención ITIL (N1 / N2 / N3)
    if (colFilterLevel && colFilterLevel.value) {
      params.support_level = colFilterLevel.value;
    }

    // Plataforma
    if (filterPlat && filterPlat.value) {
      params.platform_code = filterPlat.value;
    }

    // Búsqueda de texto
    if (search && search.value.trim()) {
      params.search = search.value.trim();
    }

    loadTickets(params);
  };

  if (search) {
    search.addEventListener('input', debounce(applyFilters, 250));
  }

  // Sincronización y disparo de filtros de Institución
  if (filterInst) {
    filterInst.addEventListener('change', () => {
      if (colFilterInst) colFilterInst.value = filterInst.value;
      applyFilters();
    });
  }
  if (colFilterInst) {
    colFilterInst.addEventListener('change', () => {
      if (filterInst) filterInst.value = colFilterInst.value;
      applyFilters();
    });
  }

  // Sincronización y disparo de filtros de Prioridad
  if (filterPrio) {
    filterPrio.addEventListener('change', () => {
      if (colFilterPrio) colFilterPrio.value = filterPrio.value;
      applyFilters();
    });
  }
  if (colFilterPrio) {
    colFilterPrio.addEventListener('change', () => {
      if (filterPrio) filterPrio.value = colFilterPrio.value;
      applyFilters();
    });
  }

  // Filtro de Nivel ITIL
  if (colFilterLevel) {
    colFilterLevel.addEventListener('change', applyFilters);
  }

  if (filterPlat) {
    filterPlat.addEventListener('change', applyFilters);
  }

  if (btnRefresh) {
    btnRefresh.addEventListener('click', () => {
      applyFilters();
      showToast('Bandeja actualizada', 'info');
    });
  }

  if (btnCsv) {
    btnCsv.addEventListener('click', () => {
      const url = new URL(`${API_BASE}/api/v1/tickets/export/csv`);
      const preset = AppState.ticketFilterPreset || 'all';
      if (preset === 'new') url.searchParams.append('status', 'NUEVO');
      else if (preset === 'in_progress') url.searchParams.append('status', 'EN_CURSO');
      else if (preset === 'p1') url.searchParams.append('priority', 'P1');
      else if (preset === 'p2') url.searchParams.append('priority', 'P2');
      else if (preset === 'p3') url.searchParams.append('priority', 'P3');
      else if (preset === 'p4') url.searchParams.append('priority', 'P4');
      else if (preset === 'p5') url.searchParams.append('priority', 'P5');
      else if (preset === 'resolved') url.searchParams.append('status', 'RESUELTO');
      else if (preset === 'closed') url.searchParams.append('status', 'CERRADO');

      const selectedPrio = (filterPrio && filterPrio.value) || (colFilterPrio && colFilterPrio.value);
      if (selectedPrio) url.searchParams.append('priority', selectedPrio);

      const selectedInst = (filterInst && filterInst.value) || (colFilterInst && colFilterInst.value);
      if (selectedInst) url.searchParams.append('institution_code', selectedInst);

      if (colFilterLevel && colFilterLevel.value) url.searchParams.append('support_level', colFilterLevel.value);

      window.location.href = url.toString();
    });
  }
}

// =============================================================================
// 7. UTILS & HELPERS
// =============================================================================
async function checkApiConnection() {
  const isOnline = await API.checkHealth();
  const dot = document.getElementById('api-status-dot');
  const text = document.getElementById('api-status-text');
  if (isOnline) {
    if (dot) dot.style.backgroundColor = '#10B981';
    if (text) text.textContent = 'API Online (FastAPI)';
  } else {
    if (dot) dot.style.backgroundColor = '#EF4444';
    if (text) text.textContent = 'API Desconectada';
  }
}

async function loadMasterData() {
  try {
    const [plats, insts, ops] = await Promise.all([
      API.getPlatforms(),
      API.getInstitutions(),
      API.getOperators()
    ]);
    AppState.platforms = plats;
    AppState.institutions = insts;
    AppState.operators = ops;

    populateSelects();
  } catch (err) {
    console.error('Error cargando maestros:', err);
  }
}

function populateSelects() {
  const filterPlat = document.getElementById('filter-platform');
  const filterInst = document.getElementById('filter-institution');
  const colFilterInst = document.getElementById('col-filter-institution');
  const modalPlat = document.getElementById('modal-platform');
  const modalInst = document.getElementById('modal-institution');
  const userInst = document.getElementById('user-institution');
  const dashInst = document.getElementById('dash-filter-inst');

  if (filterPlat) {
    filterPlat.innerHTML = '<option value="">Todas las Plataformas</option>' + 
      AppState.platforms.map(p => `<option value="${p.code}">${p.name}</option>`).join('');
  }
  if (modalPlat) {
    modalPlat.innerHTML = '<option value="">Seleccione Plataforma...</option>' + 
      AppState.platforms.map(p => `<option value="${p.code}">${p.name}</option>`).join('');
  }
  if (filterInst) {
    filterInst.innerHTML = '<option value="">Todas las Instituciones</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
  }
  if (colFilterInst) {
    colFilterInst.innerHTML = '<option value="">🏥 Todas las Sedes</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
  }
  if (dashInst) {
    dashInst.innerHTML = '<option value="">🏥 Todas las Instituciones</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
  }
  if (modalInst) {
    modalInst.innerHTML = '<option value="">Seleccione Institución...</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
  }
  const editPlat = document.getElementById('edit-platform');
  const editInst = document.getElementById('edit-institution');
  if (editPlat) {
    editPlat.innerHTML = '<option value="">Seleccione Plataforma...</option>' + 
      AppState.platforms.map(p => `<option value="${p.code}">${p.name}</option>`).join('');
  }
  if (editInst) {
    editInst.innerHTML = '<option value="">Seleccione Institución...</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
  }
  if (userInst) {
    userInst.innerHTML = '<option value="">Seleccione Institución...</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
  }
}

function formatPlatformName(code) {
  if (!code) return 'General';
  const found = AppState.platforms.find(p => p.code === code);
  return found ? found.name : code.replace('CAT_', '').replace(/_/g, ' ');
}

function formatInstitutionName(code) {
  if (!code) return 'Central';
  const found = AppState.institutions.find(i => i.code === code);
  return found ? found.name : code.replace(/_/g, ' ');
}

function formatStatusName(st) {
  const map = {
    'NUEVO': 'Nuevo',
    'ASIGNADO': 'Asignado',
    'EN_CURSO': 'En Curso',
    'RESUELTO': 'Resuelto',
    'CERRADO': 'Cerrado'
  };
  return map[st] || st;
}

function formatDateTime(dtStr) {
  if (!dtStr) return '';
  try {
    const d = new Date(dtStr);
    return d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' }) + ' - ' + d.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit' });
  } catch {
    return dtStr;
  }
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  if (type === 'error') toast.style.borderLeftColor = '#EF4444';
  if (type === 'success') toast.style.borderLeftColor = '#10B981';
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

function formatDateFriendly(dtStr) {
  if (!dtStr) return 'Fecha no disp.';
  try {
    const d = new Date(dtStr);
    const now = new Date();
    const diffMs = now - d;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Hace instantes';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h (${d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })})`;
    if (diffDays === 1) return `Ayer ${d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}`;
    return d.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' }) + ' ' + d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
  } catch {
    return dtStr;
  }
}

function toggleTicketActionMenu(ticketId) {
  const menu = document.getElementById(`tkt-action-menu-${ticketId}`);
  if (!menu) return;
  const isVisible = menu.classList.contains('active') || menu.style.display === 'block';
  document.querySelectorAll('.tkt-dropdown-menu').forEach(m => {
    m.classList.remove('active');
    m.style.display = 'none';
  });
  if (!isVisible) {
    menu.classList.add('active');
    menu.style.display = 'block';
  }
}

function resetTicketModalForm() {
  const form = document.getElementById('form-new-ticket');
  if (form) form.reset();
  const calculatedBadge = document.getElementById('modal-calculated-priority');
  if (calculatedBadge) {
    calculatedBadge.textContent = 'P3 - Media';
    calculatedBadge.className = 'badge-priority badge-p3';
  }
}

function debounce(fn, delay) {
  let timer = null;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
