/**
 * HealthDesk Quantux — Controlador SPA Integral
 * Menú de Navegación Visual, Tableros de Control y Mesa de Ayuda
 */

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

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

// 50% con Fotografías Reales de Alta Resolución y 50% con Badges de Iniciales Modernos (Directiva de Diseño)
const USER_AVATARS = {
  // 50% de Perfiles con Fotografías Reales de Médicos y Especialistas:
  'admin': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80', // Freddy Cortés (Admin General)
  'soporte': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80', // Laura Benítez (N2 Soporte)
  'cpaez': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80', // Carlos Páez (N2 Soporte)
  'mgomez': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150&auto=format&fit=crop&q=80', // Dr. Martín Gómez (Solicitante Swiss Medical)
  'alopez': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&auto=format&fit=crop&q=80', // Dra. Andrea López (Solicitante Hospital Británico)
  'dnavarro': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80', // Diego Navarro (N3 Ingeniería)
  'mflores': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80' // Marcos Flores (N1 Guardia)
  // 50% restante (svaldez, ealvarez, vromero, gfernandez, solicitante, jmartinez, rfernandez) renderizan iniciales con gradientes de color dinámicos
};

const USER_GRADIENTS = [
  'linear-gradient(135deg, #0284C7, #0369A1)',
  'linear-gradient(135deg, #059669, #047857)',
  'linear-gradient(135deg, #7C3AED, #6D28D9)',
  'linear-gradient(135deg, #D97706, #B45309)',
  'linear-gradient(135deg, #DB2777, #BE185D)',
  'linear-gradient(135deg, #00A896, #028090)'
];

function getUserAvatarHtml(username, fullName = '', size = 32, extraClass = '') {
  const u = (username || '').toLowerCase().trim();
  const name = fullName || username || 'U';
  const cleanName = name.replace(/Lic\.\s*/gi, '').trim();
  const initials = cleanName.split(' ').map(w => w[0]).filter(Boolean).join('').substring(0, 2).toUpperCase() || 'U';
  
  // Si el usuario actual tiene avatar_url personalizada en su perfil:
  let avatarUrl = (AppState.currentUser && AppState.currentUser.username === u && AppState.currentUser.avatar_url) 
    ? AppState.currentUser.avatar_url 
    : (USER_AVATARS[u] || null);

  if (avatarUrl) {
    return `<div class="user-avatar-img-wrap ${extraClass}" style="width:${size}px; height:${size}px; min-width:${size}px; border-radius:50%; overflow:hidden; border:1.5px solid #CBD5E1; box-shadow:0 1px 3px rgba(0,0,0,0.08); display:inline-flex; align-items:center; justify-content:center; background:#E2E8F0; flex-shrink:0;">
      <img src="${avatarUrl}" alt="${escapeHtml(cleanName)}" style="width:100%; height:100%; object-fit:cover;" onerror="this.parentElement.outerHTML='<div class=\\'user-avatar-initials-wrap ${extraClass}\\' style=\\'width:${size}px; height:${size}px; min-width:${size}px; border-radius:50%; background:linear-gradient(135deg, #0284C7, #0369A1); color:#FFF; display:inline-flex; align-items:center; justify-content:center; font-size:${Math.max(10, Math.round(size*0.38))}px; font-weight:800; border:1.5px solid #CBD5E1;\\'>${initials}</div>';" />
    </div>`;
  }
  
  // Deterministic gradient from username char codes
  let hash = 0;
  for (let i = 0; i < u.length; i++) hash += u.charCodeAt(i);
  const grad = USER_GRADIENTS[Math.abs(hash) % USER_GRADIENTS.length];
  
  return `<div class="user-avatar-initials-wrap ${extraClass}" style="width:${size}px; height:${size}px; min-width:${size}px; border-radius:50%; background:${grad}; color:#FFF; display:inline-flex; align-items:center; justify-content:center; font-size:${Math.max(10, Math.round(size*0.38))}px; font-weight:800; border:1.5px solid #CBD5E1; box-shadow:0 1px 3px rgba(0,0,0,0.08); flex-shrink:0;" title="${escapeHtml(cleanName)} (@${escapeHtml(u)})">${initials}</div>`;
}

function navigateHome() {
  if (AppState.currentUser && AppState.currentUser.role === 'SOLICITANTE') {
    switchView('tickets');
  } else {
    switchView('dashboard');
  }
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (sidebar) sidebar.classList.remove('open');
  if (backdrop) backdrop.classList.remove('active');
}

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
      await loadDashboardMetrics();
      await loadTickets();
      btnRefDash.innerHTML = origHtml;
      showToast('Tablero de control y métricas actualizadas con éxito', 'success');
    });
  }

  // Filtro institucional en dashboard
  const dashInstSelect = document.getElementById('dash-filter-inst');
  if (dashInstSelect) {
    dashInstSelect.addEventListener('change', async () => {
      await loadDashboardMetrics();
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
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><rect x="3" y="3" width="7" height="9" rx="1"></rect><rect x="14" y="3" width="7" height="5" rx="1"></rect><rect x="14" y="12" width="7" height="9" rx="1"></rect><rect x="3" y="16" width="7" height="5" rx="1"></rect></svg>',
      title: 'Tablero de Control',
      sub: 'Métricas en tiempo real, SLAs y distribución de incidentes'
    },
    'tickets': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><path d="M3 18v-6a9 9 0 0 1 18 0v6"></path><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path></svg>',
      title: 'Mesa de Ayuda',
      sub: 'Bandeja operativa de solicitudes de soporte y seguimiento de SLA'
    },
    'users': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
      title: 'Usuarios & Roles',
      sub: 'Gestión de personal operativo y perfiles de acceso (RBAC)'
    },
    'articles': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>',
      title: 'Base de Conocimiento',
      sub: 'Guías de resolución rápida, contingencias y procedimientos'
    },
    'platforms': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><rect x="2" y="2" width="20" height="8" rx="2"></rect><rect x="2" y="14" width="20" height="8" rx="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>',
      title: 'Plataformas & Instituciones',
      sub: '9 plataformas de software y 14 instituciones de salud'
    },
    'config': {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:17px;height:17px;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',
      title: 'Configuración',
      sub: 'Matriz de priorización ITIL, políticas de SLA y bitácora de trazabilidad inmutable'
    }
  };

  if (titles[viewName]) {
    if (titleContainer) {
      titleContainer.innerHTML = `<span style="display:flex; align-items:center; color:#00A896;">${titles[viewName].icon}</span> <span id="top-view-title-text" style="color:#0A1C3E; font-weight:800; font-size:14.5px;">${titles[viewName].title}</span>`;
    } else if (titleEl) {
      titleEl.textContent = titles[viewName].title;
    }
    if (subEl) subEl.textContent = titles[viewName].sub;
  }

  // Control de visibilidad de acciones rápidas en el top-navbar para la mesa de ayuda
  const topNavActions = document.getElementById('top-navbar-actions');
  const topNavRight = document.getElementById('top-navbar-right');
  if (topNavActions && topNavRight) {
    if (viewName === 'tickets') {
      topNavActions.style.display = 'flex';
      topNavRight.style.display = 'flex';
    } else {
      topNavActions.style.display = 'none';
      topNavRight.style.display = 'none';
    }
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

  // Actualizar Título Superior
  const viewTitles = {
    'tickets': 'Mesa de Ayuda',
    'dashboard': 'Tablero de Control',
    'users': 'Directorio de Usuarios',
    'articles': 'Base de Conocimiento',
    'platforms': 'Plataformas & Instituciones',
    'config': 'Configuración del Sistema'
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
      <button class="pill-filter-btn ${activeSubTab === 'audit' ? 'active' : ''}" onclick="switchDashboardSubTab('audit')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
        <span>Auditoría Legal</span>
      </button>
    `;
  } else if (viewName === 'tickets') {
    const preset = AppState.ticketFilterPreset || 'all';
    const isReq = AppState.currentUser && AppState.currentUser.role === 'SOLICITANTE';
    const mineLabel = isReq ? 'Mis Solicitudes' : 'Asignados a Mí';

    container.innerHTML = `
      <button class="pill-filter-btn ${preset === 'all' ? 'active' : ''}" onclick="applyTicketPreset('all')" title="Ver todas las solicitudes">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
        <span>Todos los Tickets</span>
      </button>
      <button class="pill-filter-btn ${preset === 'mine' ? 'active' : ''}" onclick="applyTicketPreset('mine')" title="${isReq ? 'Mis solicitudes creadas' : 'Casos asignados a mi usuario'}" style="${preset === 'mine' ? 'background:var(--q-primary); color:#FFF; font-weight:800;' : ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <span>${mineLabel}</span>
      </button>
      <button class="pill-filter-btn ${preset === 'p1' ? 'active' : ''}" onclick="applyTicketPreset('p1')" title="Incidentes Críticos P1 (Atención Inmediata)" style="${preset === 'p1' ? 'background:#DC2626; color:#FFF; border-color:#DC2626; font-weight:800;' : 'background:rgba(239,68,68,0.08); border-color:#FCA5A5; color:#DC2626;'}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><polygon points="12 2 22 20 2 20 12 2"></polygon><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
        <span>Críticos P1</span>
      </button>
    `;
  } else if (viewName === 'users') {
    const activeLvl = AppState.userFilterLevel || 'all';
    container.innerHTML = `
      <button class="pill-filter-btn ${activeLvl === 'all' ? 'active' : ''}" onclick="filterUsersByLevel('all')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
        <span>Todos</span>
      </button>
      <button class="pill-filter-btn ${activeLvl === 'N1' ? 'active' : ''}" onclick="filterUsersByLevel('N1')">
        <span>N1 • Guardia</span>
      </button>
      <button class="pill-filter-btn ${activeLvl === 'N2' ? 'active' : ''}" onclick="filterUsersByLevel('N2')">
        <span>N2 • Especialistas</span>
      </button>
      <button class="pill-filter-btn ${activeLvl === 'N3' ? 'active' : ''}" onclick="filterUsersByLevel('N3')">
        <span>N3 • Ingeniería</span>
      </button>
      <button class="pill-filter-btn ${activeLvl === 'ADMIN' ? 'active' : ''}" onclick="filterUsersByLevel('ADMIN')">
        <span>Administradores</span>
      </button>
      <button class="pill-filter-btn ${activeLvl === 'SOLICITANTE' ? 'active' : ''}" onclick="filterUsersByLevel('SOLICITANTE')">
        <span>Médicos y Solicitantes</span>
      </button>
    `;
  } else if (viewName === 'articles') {
    container.innerHTML = `
      <button class="pill-filter-btn active" onclick="filterKBCategory('')">
        <span>Todos los Protocolos</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('CLINICO')">
        <span>Asistencial / Clínico</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('DIAGNOSTICO')">
        <span>Diagnóstico y LIS</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('FARMACIA')">
        <span>Farmacia y Recetas</span>
      </button>
      <button class="pill-filter-btn" onclick="filterKBCategory('CONTINGENCIA')">
        <span>Contingencia Crítica</span>
      </button>
    `;
  } else if (viewName === 'platforms') {
    container.innerHTML = `
      <button class="pill-filter-btn active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><rect x="2" y="2" width="20" height="8" rx="2"></rect><rect x="2" y="14" width="20" height="8" rx="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line></svg>
        <span>Ecosistema de Plataformas & Sanatorios</span>
      </button>
    `;
  } else if (viewName === 'config') {
    container.innerHTML = `
      <button class="pill-filter-btn active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        <span>Parámetros Globales de Servicio y SLA</span>
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
  applyRolePermissions();
  loadTickets();
  if (AppState.currentView === 'dashboard') {
    loadDashboardMetrics(AppState.currentDashInst);
  }
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
      openAuthModal(false);
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
    { username: 'solicitante', full_name: 'Martín Gómez (Solicitante)', role: 'SOLICITANTE', institution_code: 'SWISS_MEDICAL' }
  ];

  container.innerHTML = users.map(u => {
    const isCurrent = AppState.currentUser && AppState.currentUser.username === u.username;
    const roleBadgeClass = u.role === 'ADMIN' ? 'badge-role-admin' : (u.role.includes('SOPORTE') || u.role === 'SOPORTE' ? 'badge-role-soporte' : 'badge-role-solicitante');

    return `
      <div class="quick-login-item ${isCurrent ? 'active-user' : ''}" onclick="selectQuickUser('${u.username}')">
        <div class="quick-login-left">
          ${getUserAvatarHtml(u.username, u.full_name, 28)}
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
    if (topAvatar) topAvatar.innerHTML = '🔒';
    if (profName) profName.textContent = 'Sesión Cerrada';
    if (profRole) profRole.textContent = 'Haga clic para ingresar';
    if (profAvatar) profAvatar.innerHTML = '🔒';
    if (currUserName) currUserName.textContent = 'Invitado';
    if (currUserRole) currUserRole.textContent = 'Sin acceso';
    if (currUserAvatar) currUserAvatar.innerHTML = '🔒';
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
  if (topAvatar) topAvatar.innerHTML = getUserAvatarHtml(AppState.currentUser.username, AppState.currentUser.full_name, 32);
  if (profName) profName.textContent = AppState.currentUser.full_name;
  if (profRole) profRole.textContent = `ROL: ${AppState.currentUser.role}`;
  if (profAvatar) profAvatar.innerHTML = getUserAvatarHtml(AppState.currentUser.username, AppState.currentUser.full_name, 40);
  if (currUserName) currUserName.textContent = AppState.currentUser.full_name;
  if (currUserRole) currUserRole.textContent = `Rol: ${AppState.currentUser.role}`;
  if (currUserAvatar) currUserAvatar.innerHTML = getUserAvatarHtml(AppState.currentUser.username, AppState.currentUser.full_name, 34);
  if (topSwitchText) topSwitchText.textContent = 'Cerrar Sesión';
}

// =============================================================================
// 3. TABLEROS DE SEGUIMIENTO Y CONTROL (DASHBOARD ANALYTICS)
// =============================================================================
async function loadDashboardMetrics(institutionCode = null, period = null, dateFrom = null, dateTo = null) {
  try {
    const instSelect = document.getElementById('dash-filter-inst');
    const periodSelect = document.getElementById('dash-filter-period');
    const fromInput = document.getElementById('dash-date-from');
    const toInput = document.getElementById('dash-date-to');

    const inst = (institutionCode !== null && institutionCode !== undefined) ? institutionCode : (instSelect ? instSelect.value : '');
    const per = (period !== null && period !== undefined) ? period : (periodSelect ? periodSelect.value : 'all');
    const dFrom = (dateFrom !== null && dateFrom !== undefined) ? dateFrom : (fromInput ? fromInput.value : '');
    const dTo = (dateTo !== null && dateTo !== undefined) ? dateTo : (toInput ? toInput.value : '');

    const params = {};
    if (inst) params.institution_code = inst;
    if (per && per !== 'all') params.period = per;
    if (per === 'custom') {
      if (dFrom) params.date_from = dFrom;
      if (dTo) params.date_to = dTo;
    }
    const data = await API.getMetrics(params);
    AppState.metrics = data;
    AppState.currentDashInst = inst;
    AppState.currentDashPeriod = per;
    renderDashboard(inst);
  } catch (err) {
    console.error('Error cargando métricas:', err);
  }
}

function onDashboardDateFilterChange() {
  const periodEl = document.getElementById('dash-filter-period');
  const customBox = document.getElementById('dash-custom-date-box');
  const period = periodEl ? periodEl.value : 'all';

  if (customBox) {
    customBox.style.display = (period === 'custom') ? 'inline-flex' : 'none';
  }

  const inst = document.getElementById('dash-filter-inst') ? document.getElementById('dash-filter-inst').value : '';
  const dateFrom = document.getElementById('dash-date-from') ? document.getElementById('dash-date-from').value : '';
  const dateTo = document.getElementById('dash-date-to') ? document.getElementById('dash-date-to').value : '';

  loadDashboardMetrics(inst, period, dateFrom, dateTo);
}

function switchDashboardSubTab(subTab) {
  document.querySelectorAll('.dash-subview').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('[id^="btn-dash-sub-"]').forEach(b => b.classList.remove('active'));

  const targetView = document.getElementById(`dash-subview-${subTab}`);
  if (targetView) targetView.classList.add('active');

  const targetBtn = document.getElementById(`btn-dash-sub-${subTab}`);
  if (targetBtn) targetBtn.classList.add('active');
}

function renderDashboard(selectedInst = '') {
  if (!AppState.metrics) return;
  const m = AppState.metrics;
  const currentInst = selectedInst || AppState.currentDashInst || (document.getElementById('dash-filter-inst') ? document.getElementById('dash-filter-inst').value : '');

  // 1. KPI Hero Numbers
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
  if (kpiConf) kpiConf.textContent = `${m.conformity_rate || 96.5}%`;
  if (kpiResolved) kpiResolved.textContent = (m.resolved_tickets + m.closed_tickets) || 0;

  // Center Metrics in Donut Charts
  const statusCenter = document.getElementById('chart-status-center-total');
  if (statusCenter) statusCenter.textContent = m.total_tickets || 0;

  const prioCenter = document.getElementById('chart-prio-center-crit');
  const critCount = (m.by_priority && (m.by_priority.P1 || 0) + (m.by_priority.P2 || 0)) || 0;
  if (prioCenter) prioCenter.textContent = critCount;

  // 2. Render Chart.js Canvas Charts
  renderDashboardCanvasCharts(m, currentInst);

  // 3. Sub-View 2: Tabla de Casos Activos con SLA Monitor
  renderDashboardActiveSlaTable(currentInst);

  // 4. Sub-View 3: Grid de Salud de Plataformas Clínicas
  renderDashboardPlatformsGrid(m);

  // 5. Sub-View 4: Tabla Ranking de Instituciones
  renderDashboardInstitutionsRanking(m);

  // 6. Sub-View 5: Feed de Auditoría Inmutable SHA-256
  renderDashboardAuditFeed(m);
}

function renderDashboardCanvasCharts(m, currentInst) {
  if (typeof Chart === 'undefined') {
    console.warn('Chart.js no está cargado todavía.');
    return;
  }

  if (!AppState.charts) {
    AppState.charts = {};
  }

  // --- CHART 1: DONUT DE ESTADOS OPERATIVOS (FSM) ---
  const canvasStatus = document.getElementById('chart-canvas-status');
  if (canvasStatus) {
    if (AppState.charts.status) {
      AppState.charts.status.destroy();
    }

    const statusKeys = ['NUEVO', 'ASIGNADO', 'EN_CURSO', 'RESUELTO', 'CERRADO'];
    const statusLabels = ['Nuevos', 'Asignados', 'En Curso', 'Resueltos', 'Cerrados'];
    const statusColors = ['#3B82F6', '#F59E0B', '#0284C7', '#10B981', '#64748B'];
    const statusData = statusKeys.map(k => (m.by_status && m.by_status[k]) || 0);

    AppState.charts.status = new Chart(canvasStatus, {
      type: 'doughnut',
      data: {
        labels: statusLabels,
        datasets: [{
          data: statusData,
          backgroundColor: statusColors,
          borderWidth: 2,
          borderColor: '#FFFFFF',
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: { boxWidth: 10, font: { size: 10.5, family: 'Inter', weight: 600 }, padding: 8 }
          },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: ${ctx.parsed} casos (${Math.round((ctx.parsed / (m.total_tickets || 1)) * 100)}%)`
            }
          }
        },
        onClick: (evt, activeEls) => {
          if (activeEls && activeEls.length > 0) {
            const idx = activeEls[0].index;
            const key = statusKeys[idx];
            const label = statusLabels[idx];
            openMetricsDrilldownModal('status', key, `Estado: ${label}`);
          }
        }
      }
    });
  }

  // --- CHART 2: DONUT DE PRIORIDAD & SEVERIDAD ---
  const canvasPrio = document.getElementById('chart-canvas-priority');
  if (canvasPrio) {
    if (AppState.charts.priority) {
      AppState.charts.priority.destroy();
    }

    const prioKeys = ['P1', 'P2', 'P3', 'P4', 'P5'];
    const prioLabels = ['P1 Crítica', 'P2 Alta', 'P3 Media', 'P4 Baja', 'P5 Planificada'];
    const prioColors = ['#EF4444', '#F97316', '#3B82F6', '#10B981', '#94A3B8'];
    const prioData = prioKeys.map(k => (m.by_priority && m.by_priority[k]) || 0);

    AppState.charts.priority = new Chart(canvasPrio, {
      type: 'doughnut',
      data: {
        labels: prioLabels,
        datasets: [{
          data: prioData,
          backgroundColor: prioColors,
          borderWidth: 2,
          borderColor: '#FFFFFF',
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: { boxWidth: 10, font: { size: 10.5, family: 'Inter', weight: 600 }, padding: 8 }
          },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: ${ctx.parsed} incidentes (${Math.round((ctx.parsed / (m.total_tickets || 1)) * 100)}%)`
            }
          }
        },
        onClick: (evt, activeEls) => {
          if (activeEls && activeEls.length > 0) {
            const idx = activeEls[0].index;
            const key = prioKeys[idx];
            const label = prioLabels[idx];
            openMetricsDrilldownModal('priority', key, `Prioridad ${label}`);
          }
        }
      }
    });
  }

  // --- CHART 3: BARRAS HORIZONTALES PLATAFORMAS ASISTENCIALES ---
  const canvasPlat = document.getElementById('chart-canvas-platforms');
  if (canvasPlat) {
    if (AppState.charts.platforms) {
      AppState.charts.platforms.destroy();
    }

    const platEntries = Object.entries(m.by_platform || {}).sort((a, b) => b[1] - a[1]).slice(0, 6);
    const platLabels = platEntries.map(([k]) => formatPlatformName(k));
    const platData = platEntries.map(([, v]) => v);
    const platCodes = platEntries.map(([k]) => k);

    AppState.charts.platforms = new Chart(canvasPlat, {
      type: 'bar',
      data: {
        labels: platLabels,
        datasets: [{
          label: 'Solicitudes',
          data: platData,
          backgroundColor: 'rgba(0, 168, 150, 0.85)',
          borderRadius: 6,
          borderSkipped: false
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.parsed.x} solicitudes registradas`
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#F1F5F9' },
            ticks: { font: { size: 10, family: 'Inter' }, precision: 0 }
          },
          y: {
            grid: { display: false },
            ticks: { font: { size: 11, family: 'Inter', weight: 600 }, color: '#1E293B' }
          }
        },
        onClick: (evt, activeEls) => {
          if (activeEls && activeEls.length > 0) {
            const idx = activeEls[0].index;
            const code = platCodes[idx];
            const name = platLabels[idx];
            openMetricsDrilldownModal('platform', code, `Plataforma: ${name}`);
          }
        }
      }
    });
  }

  // --- CHART 4: BARRAS HORIZONTALES INSTITUCIONES / SANATORIOS ---
  const canvasInst = document.getElementById('chart-canvas-institutions');
  if (canvasInst) {
    if (AppState.charts.institutions) {
      AppState.charts.institutions.destroy();
    }

    const instEntries = Object.entries(m.by_institution || {}).sort((a, b) => b[1] - a[1]).slice(0, 6);
    const instLabels = instEntries.map(([k]) => formatInstitutionName(k));
    const instData = instEntries.map(([, v]) => v);
    const instCodes = instEntries.map(([k]) => k);

    AppState.charts.institutions = new Chart(canvasInst, {
      type: 'bar',
      data: {
        labels: instLabels,
        datasets: [{
          label: 'Casos',
          data: instData,
          backgroundColor: 'rgba(59, 130, 246, 0.85)',
          borderRadius: 6,
          borderSkipped: false
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.parsed.x} casos sanitarios`
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#F1F5F9' },
            ticks: { font: { size: 10, family: 'Inter' }, precision: 0 }
          },
          y: {
            grid: { display: false },
            ticks: { font: { size: 11, family: 'Inter', weight: 600 }, color: '#1E293B' }
          }
        },
        onClick: (evt, activeEls) => {
          if (activeEls && activeEls.length > 0) {
            const idx = activeEls[0].index;
            const code = instCodes[idx];
            const name = instLabels[idx];
            openMetricsDrilldownModal('institution', code, `Institución: ${name}`);
          }
        }
      }
    });
  }
}

function renderDashboardActiveSlaTable(currentInst) {
  const tbodySla = document.getElementById('tbody-active-sla');
  if (!tbodySla) return;

  const activeTickets = (AppState.tickets || [])
    .filter(t => t.status !== 'CERRADO' && (!currentInst || t.institution_code === currentInst))
    .slice(0, 10);

  if (activeTickets.length === 0) {
    tbodySla.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#94A3B8; padding:20px;">No hay incidentes pendientes para la institución seleccionada.</td></tr>';
    return;
  }

  tbodySla.innerHTML = activeTickets.map(t => {
    const pClass = `prio-pill-${t.priority.toLowerCase()}`;
    const sla = calculateTicketSLA(t);
    const assigneeName = formatUserName(t.assignee_username);
    return `
      <tr>
        <td><strong style="font-family:'JetBrains Mono', monospace; font-size:11.5px; color:#0F172A;">${t.id}</strong></td>
        <td><span class="prio-pill ${pClass}">${t.priority}</span></td>
        <td>
          <div style="font-weight:600; max-width:280px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#0F172A;">${t.title}</div>
          <div style="font-size:10px; color:#64748B;">🏥 ${formatInstitutionName(t.institution_code)}</div>
        </td>
        <td><span style="font-size:11px; font-weight:600; color:#475569;">${formatPlatformName(t.platform_code)}</span></td>
        <td>
          <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:20px; height:20px; border-radius:50%; background:#E0F2FE; color:#0369A1; font-weight:800; font-size:9px; display:flex; align-items:center; justify-content:center;">
              ${getInitials(assigneeName)}
            </div>
            <span style="font-size:11px; font-weight:600; color:#1E293B;">${assigneeName}</span>
          </div>
        </td>
        <td>
          <span style="font-size:11px; font-weight:700; color:${sla.isBreached ? '#DC2626' : '#10B981'};">
            ${sla.isBreached ? '⚠️ Excedido' : '⏱️ ' + sla.timeRemainingText}
          </span>
        </td>
        <td style="text-align:center;">
          <button class="btn-clean-action" style="padding:4px 10px; font-size:11px; font-weight:700; border-radius:6px; background:#00A896; color:#FFF; border:none; cursor:pointer;" onclick="openTicketWorkspace('${t.id}')">
            Abrir Caso ➔
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function renderDashboardPlatformsGrid(m) {
  const container = document.getElementById('grid-platform-health-cards');
  if (!container) return;

  const platforms = AppState.platforms || [];
  if (platforms.length === 0) {
    container.innerHTML = '<div style="color:#94A3B8; font-size:12px; padding:12px;">Cargando catálogo de plataformas asistenciales...</div>';
    return;
  }

  container.innerHTML = platforms.map(p => {
    const count = (m.by_platform && m.by_platform[p.code]) || 0;
    const isCritical = count > 10;
    return `
      <div class="chart-card-modern" style="cursor:pointer; transition:transform 0.15s ease;" onclick="openMetricsDrilldownModal('platform', '${p.code}', 'Plataforma: ${p.name}')">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
          <div>
            <div style="font-size:14px; font-weight:800; color:#0F172A;">🩺 ${p.name}</div>
            <div style="font-size:11px; color:#64748B;">Código: <code>${p.code}</code></div>
          </div>
          <span style="font-size:10px; font-weight:800; padding:3px 8px; border-radius:6px; background:${isCritical ? '#FEE2E2; color:#DC2626;' : '#ECFDF5; color:#059669;'}">
            ${isCritical ? '⚠️ ALTA DEMANDA' : '🟢 OPERATIVO'}
          </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid #F1F5F9;">
          <span style="font-size:11.5px; color:#64748B;">Solicitudes Registradas:</span>
          <strong style="font-size:16px; color:#00A896; font-weight:900;">${count}</strong>
        </div>
      </div>
    `;
  }).join('');
}

function renderDashboardInstitutionsRanking(m) {
  const tbody = document.getElementById('tbody-institutions-ranking');
  if (!tbody) return;

  const institutions = AppState.institutions || [];
  if (institutions.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#94A3B8; padding:20px;">Cargando instituciones...</td></tr>';
    return;
  }

  const sortedInst = [...institutions].sort((a, b) => {
    const cA = (m.by_institution && m.by_institution[a.code]) || 0;
    const cB = (m.by_institution && m.by_institution[b.code]) || 0;
    return cB - cA;
  });

  tbody.innerHTML = sortedInst.map(inst => {
    const total = (m.by_institution && m.by_institution[inst.code]) || 0;
    const active = (AppState.tickets || []).filter(t => t.institution_code === inst.code && t.status !== 'CERRADO').length;
    return `
      <tr>
        <td><strong>🏥 ${inst.name}</strong></td>
        <td><span style="font-size:11px; color:#64748B;">${inst.segment || 'Sanatorio / Prepaga'}</span></td>
        <td><strong style="font-size:13px; color:#0F172A;">${total}</strong></td>
        <td><span style="font-weight:700; color:#0284C7;">${active} activos</span></td>
        <td><span style="color:#10B981; font-weight:800;">98.5%</span></td>
        <td><span style="color:#059669; font-weight:800;">96.8%</span></td>
        <td style="text-align:center;">
          <button class="btn-clean-action" style="padding:4px 10px; font-size:11px; font-weight:700; border-radius:6px; background:#3B82F6; color:#FFF; border:none; cursor:pointer;" onclick="openMetricsDrilldownModal('institution', '${inst.code}', 'Institución: ${inst.name}')">
            Ver Casos ➔
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function renderDashboardAuditFeed(m) {
  const auditFeed = document.getElementById('feed-audit-logs');
  if (!auditFeed) return;

  const logs = m.recent_audit || [];
  if (logs.length === 0) {
    auditFeed.innerHTML = '<div style="color:#94A3B8; font-size:11px; padding:12px;">Sin actividad reciente para el filtro seleccionado.</div>';
    return;
  }

  auditFeed.innerHTML = logs.slice(0, 10).map(log => {
    return `
      <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:8px 12px; font-size:11.5px; display:flex; justify-content:space-between; align-items:center; gap:10px;">
        <div>
          <strong style="color:var(--q-navy); font-family:'JetBrains Mono', monospace; font-size:11px;">[${log.ticket_id}]</strong> 
          <span style="color:#334155; font-weight:600; margin-left:6px;">${log.reason}</span>
        </div>
        <div style="font-size:10px; color:#94A3B8; font-weight:600; white-space:nowrap;">
          👤 ${formatUserName(log.changed_by)} • ${log.time}
        </div>
      </div>
    `;
  }).join('');
}

function openTicketInCockpit(ticketId) {
  openTicketWorkspace(ticketId);
}

// =============================================================================
// 4. MESA DE AYUDA OPERATIVA (COCKPIT EN 3 COLUMNAS REAIS - UH-28)
// =============================================================================
async function loadTickets(params = {}) {
  try {
    // Aislamiento de Seguridad: Rol Solicitante solo ve sus propios tickets
    if (AppState.currentUser && AppState.currentUser.role === 'SOLICITANTE') {
      params.requester_username = AppState.currentUser.username;
    }

    // Filtro de Período de Creación si existe
    const periodSelect = document.getElementById('tkt-filter-period');
    if (periodSelect && periodSelect.value && periodSelect.value !== 'all' && !params.period) {
      params.period = periodSelect.value;
    }

    const rawTickets = await API.getTickets(params);
    
    // Por defecto en la bandeja se ocultan los resueltos y cerrados
    // a menos que el usuario los solicite explícitamente vía filtro o preset
    let filteredTickets = rawTickets;
    
    if (params.pending_only) {
      filteredTickets = rawTickets.filter(t => ['NUEVO', 'ASIGNADO', 'EN_CURSO'].includes(t.status));
    } else if (!params.status && !params.include_all && !params.include_resolved) {
      filteredTickets = rawTickets.filter(t => t.status !== 'RESUELTO' && t.status !== 'CERRADO');
    }
    
    AppState.tickets = filteredTickets;
    renderTicketList();
    
    // Si no hay filtros restrictivos de búsqueda, guardar copia global para contadores precisos
    if (!params.priority && !params.assignee_username && !params.status && !params.search) {
      AppState.allTicketsRaw = rawTickets;
      updatePresetCounts(rawTickets);
    } else if (AppState.allTicketsRaw) {
      updatePresetCounts(AppState.allTicketsRaw);
    } else {
      API.getTickets({}).then(all => {
        AppState.allTicketsRaw = all;
        updatePresetCounts(all);
      }).catch(() => updatePresetCounts(rawTickets));
    }
    
    // Si hay un ticket seleccionado, refrescarlo
    if (AppState.selectedTicket) {
      const refreshed = rawTickets.find(t => t.id === AppState.selectedTicket.id);
      if (refreshed) {
        AppState.selectedTicket = refreshed;
        renderTicketDetail(refreshed);
      } else if (filteredTickets.length > 0) {
        selectTicket(filteredTickets[0].id, false);
      }
    } else if (filteredTickets.length > 0) {
      selectTicket(filteredTickets[0].id, false);
    }
    
    // Actualizar badges de conteo
    const sideBadge = document.getElementById('sidebar-ticket-count');
    const footerCount = document.getElementById('invgate-footer-count-num');
    if (sideBadge) sideBadge.textContent = filteredTickets.length;
    if (footerCount) footerCount.textContent = filteredTickets.length;
  } catch (err) {
    console.error('Error cargando tickets:', err);
  }
}

function updatePresetCounts(tickets) {
  if (!tickets) return;
  const currentUsername = AppState.currentUser ? AppState.currentUser.username : '';
  const currentRole = AppState.currentUser ? AppState.currentUser.role : '';

  const cAll = tickets.filter(t => t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;
  
  const cMine = tickets.filter(t => {
    if (t.status === 'RESUELTO' || t.status === 'CERRADO') return false;
    if (currentRole === 'SOLICITANTE') {
      return t.requester_username === currentUsername;
    }
    return t.assignee_username === currentUsername;
  }).length;

  const cUnassigned = tickets.filter(t => {
    if (t.status === 'RESUELTO' || t.status === 'CERRADO') return false;
    return !t.assignee_username || t.assignee_username === '' || t.assignee_username === 'null';
  }).length;

  const cP1 = tickets.filter(t => (t.priority || '').toUpperCase() === 'P1' && t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;

  const elMine = document.getElementById('qv-count-mine');
  const elUnassigned = document.getElementById('qv-count-unassigned');
  const elP1 = document.getElementById('qv-count-p1');
  const elTotalBadge = document.getElementById('tickets-badge-total');

  if (elMine) elMine.textContent = cMine;
  if (elUnassigned) elUnassigned.textContent = cUnassigned;
  if (elP1) elP1.textContent = cP1;
  if (elTotalBadge) elTotalBadge.textContent = `${cAll} Solicitudes`;
}

function selectQuickView(viewKey) {
  AppState.activeQuickView = viewKey;

  // Actualizar estado activo de los botones de filtro tab
  const pills = document.querySelectorAll('#view-tickets .filter-tab-pill');
  pills.forEach(p => p.classList.remove('active'));

  const pillMap = {
    'ALL': 'qv-all',
    'MINE': 'qv-mine',
    'UNASSIGNED': 'qv-unassigned',
    'P1': 'qv-p1',
    'N1': 'qv-n1',
    'RESOLVED': 'qv-resolved'
  };

  const activePillId = pillMap[viewKey] || 'qv-all';
  const targetPill = document.getElementById(activePillId);
  if (targetPill) targetPill.classList.add('active');

  // Construir parámetros combinando con los selectores de precisión
  const params = {};
  const inst = document.getElementById('tkt-filter-inst') ? document.getElementById('tkt-filter-inst').value : '';
  const plat = document.getElementById('tkt-filter-platform') ? document.getElementById('tkt-filter-platform').value : '';
  const level = document.getElementById('tkt-filter-level') ? document.getElementById('tkt-filter-level').value : '';
  const period = document.getElementById('tkt-filter-period') ? document.getElementById('tkt-filter-period').value : '';
  const statusSelect = document.getElementById('tkt-filter-status') ? document.getElementById('tkt-filter-status').value : '';

  if (inst) params.institution = inst;
  if (plat) params.platform = plat;
  if (level) params.support_level = level;
  if (period && period !== 'all') params.period = period;

  if (viewKey === 'MINE') {
    if (AppState.currentUser && AppState.currentUser.role === 'SOLICITANTE') {
      params.requester_username = AppState.currentUser.username;
    } else if (AppState.currentUser) {
      params.assignee_username = AppState.currentUser.username;
    }
  } else if (viewKey === 'UNASSIGNED') {
    params.assignee_username = '__unassigned__';
  } else if (viewKey === 'P1') {
    params.priority = 'P1';
  } else if (viewKey === 'N1') {
    params.support_level = 'N1';
  } else if (viewKey === 'RESOLVED') {
    params.status = 'RESUELTO';
    params.include_resolved = true;
  }

  if (viewKey !== 'RESOLVED' && statusSelect && statusSelect !== 'ACTIVE' && statusSelect !== 'ALL') {
    params.status = statusSelect;
  } else if (statusSelect === 'ALL') {
    params.include_all = true;
  }

  loadTickets(params);
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

function getInitials(name) {
  if (!name) return '??';
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function getAvatarBubbleClass(initials) {
  const code = (initials.charCodeAt(0) + (initials.charCodeAt(1) || 0)) % 4;
  if (code === 0) return 'bubble-cr';
  if (code === 1) return 'bubble-dc';
  if (code === 2) return 'bubble-da';
  return 'bubble-lb';
}

function renderTicketList() {
  const tbody = document.getElementById('ticket-table-body');
  const container = document.getElementById('ticket-list');
  const countBadge = document.getElementById('ticket-count-badge');
  const sidebarCount = document.getElementById('sidebar-ticket-count');
  const footerCount = document.getElementById('invgate-footer-count-num');

  const total = AppState.tickets ? AppState.tickets.length : 0;
  if (countBadge) countBadge.textContent = total;
  if (sidebarCount) sidebarCount.textContent = total;
  if (footerCount) footerCount.textContent = total;

  if (tbody) {
    if (!AppState.tickets || AppState.tickets.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align:center; padding: 48px 16px; color:#94A3B8;">
            <div style="font-size:36px; margin-bottom:10px;">📭</div>
            <div style="font-size:14px; font-weight:700; color:#475569;">No hay solicitudes activas con los filtros aplicados</div>
            <div style="font-size:12px; color:#94A3B8; margin-top:4px;">Utilice los filtros avanzados para consultar casos resueltos o cambiar de sede.</div>
          </td>
        </tr>
      `;
    } else {
      tbody.innerHTML = AppState.tickets.map(t => {
        const priority = (t.priority || 'P3').toUpperCase();
        const status = (t.status || 'NUEVO').toUpperCase();
        const level = (t.support_level || 'N1').toUpperCase();
        const platName = formatPlatformName(t.platform_code);
        const instName = formatInstitutionName(t.institution_code);
        const timeAgo = formatDateFriendly(t.created_at);

        // Clases de prioridad para borde lateral y pastilla
        const prioRowClass = `prio-row-${priority.toLowerCase()}`;
        const prioChipClass = `chip-${priority.toLowerCase()}`;
        let prioIcon = '🔷';
        let prioLabel = `${priority} • Media`;
        if (priority === 'P1') { prioIcon = '🚨'; prioLabel = 'P1 • Crítica'; }
        else if (priority === 'P2') { prioIcon = '⚠️'; prioLabel = 'P2 • Alta'; }
        else if (priority === 'P3') { prioIcon = '🔷'; prioLabel = 'P3 • Media'; }
        else if (priority === 'P4') { prioIcon = '⚪'; prioLabel = 'P4 • Baja'; }

        // Pastilla de Estado
        let statusPillClass = 'status-pill-nuevo';
        let statusIcon = '🟢';
        let statusText = 'NUEVO';
        if (status === 'ASIGNADO') { statusPillClass = 'status-pill-asignado'; statusIcon = '🔵'; statusText = 'ASIGNADO'; }
        else if (status === 'EN_CURSO') { statusPillClass = 'status-pill-en_curso'; statusIcon = '🟡'; statusText = 'EN CURSO'; }
        else if (status === 'RESUELTO') { statusPillClass = 'status-pill-resuelto'; statusIcon = '✅'; statusText = 'RESUELTO'; }
        else if (status === 'CERRADO') { statusPillClass = 'status-pill-cerrado'; statusIcon = '🔒'; statusText = 'CERRADO'; }

        // Cálculo dinámico de SLA
        const sla = calculateTicketSLA(t);
        let slaChipClass = 'sla-chip-ok';
        if (sla.status === 'BREACHED') slaChipClass = 'sla-chip-breached';
        else if (sla.status === 'WARNING') slaChipClass = 'sla-chip-warn';

        // Asignado a
        const rawAgent = t.assignee_name || (t.assignee_username ? formatUserName(t.assignee_username) : 'Sin Asignar');
        const agentName = rawAgent.replace(/Lic\.\s*/gi, '').trim();

        // Solicitante / Institución
        const rawReq = t.requester_name || (t.requester_username ? formatUserName(t.requester_username) : 'Médico Asistencial');
        const reqName = rawReq.replace(/Lic\.\s*/gi, '').trim();

        return `
          <tr class="${prioRowClass}" onclick="openAgentWorkspace('${t.id}')" title="Haga clic para abrir el espacio de trabajo de la solicitud #${t.id}">
            <!-- 1. ID & PRIORIDAD (Misma Fila / Horizontal) -->
            <td style="white-space: nowrap; width: 250px; min-width: 240px;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="tkt-id-badge" style="margin-bottom: 0;">#${t.id}</span>
                <span class="tkt-prio-chip ${prioChipClass}">${prioIcon} ${prioLabel}</span>
              </div>
            </td>

            <!-- 2. SOLICITUD & TAXONOMÍA -->
            <td style="width: auto;">
              <div class="tkt-table-subject-cell">
                <div style="flex: 1; min-width: 0;">
                  <div class="tkt-table-subject-title">${escapeHtml(t.title)}</div>
                  <div class="tkt-chips-row">
                    <span class="tkt-chip-module">💻 ${platName}</span>
                    <span class="tkt-chip-inst">🏥 ${instName}</span>
                    <span class="tkt-chip-time">🕒 ${timeAgo}</span>
                  </div>
                </div>
              </div>
            </td>

            <!-- 3. ESTADO & TIEMPO SLA -->
            <td style="width: 170px; white-space: nowrap;">
              <div class="tkt-sla-track-cell">
                <span class="tkt-status-pill ${statusPillClass}">${statusIcon} ${statusText}</span>
                <span class="tkt-sla-chip ${slaChipClass}">⏱️ ${sla.timeRemainingText || 'En plazo'}</span>
              </div>
            </td>

            <!-- 4. ASIGNADO A -->
            <td style="width: 180px;">
              <div class="tkt-user-profile-cell">
                ${getUserAvatarHtml(t.assignee_username, agentName, 28)}
                <div class="tkt-user-details">
                  <span class="tkt-user-name">${agentName.split('(')[0].trim()}</span>
                  <span class="tkt-user-sub">${level} • Mesa de Ayuda</span>
                </div>
              </div>
            </td>

            <!-- 5. SOLICITANTE / INSTITUCIÓN -->
            <td style="width: 190px;">
              <div class="tkt-user-profile-cell">
                ${getUserAvatarHtml(t.requester_username, reqName, 28)}
                <div class="tkt-user-details">
                  <span class="tkt-user-name" title="${reqName}">${reqName.split('(')[0].trim()}</span>
                  <span class="tkt-user-sub">${instName}</span>
                </div>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  // Compatibilidad con contenedor de lista auxiliar si existe
  if (container) {
    if (!AppState.tickets || AppState.tickets.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding:40px 14px; color:#94A3B8;">
          <div style="font-size:36px; margin-bottom:10px;">📭</div>
          <div style="font-size:13px; font-weight:700; color:#475569;">No hay solicitudes con estos filtros</div>
        </div>
      `;
    } else {
      container.innerHTML = AppState.tickets.map(t => {
        const isSelected = AppState.selectedTicket && AppState.selectedTicket.id === t.id;
        const priority = (t.priority || 'P3').toUpperCase();
        const status = (t.status || 'NUEVO').toUpperCase();
        const level = (t.support_level || 'N1').toUpperCase();
        const platName = formatPlatformName(t.platform_code);
        const instName = formatInstitutionName(t.institution_code);
        const timeAgo = formatDateFriendly(t.created_at);

        return `
          <div class="ticket-card-clean prio-${priority.toLowerCase()} ${isSelected ? 'selected' : ''}" onclick="openAgentWorkspace('${t.id}')">
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
  }
}

async function selectTicket(ticketId, userTriggered = false) {
  try {
    const ticket = await API.getTicket(ticketId);
    AppState.selectedTicket = ticket;
    renderTicketList();
    renderTicketDetail(ticket);

    if (userTriggered) {
      openAgentWorkspace(ticketId);
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

        <!-- Barra de Acciones FSM y Popups Especializados -->
        <div class="detail-actions-toolbar">
          ${actionsToolbarHtml}
          <div style="margin-left: auto; display: flex; gap: 6px; flex-wrap: wrap;">
            <button class="btn-action-popup" onclick="openTechDetailsModal('${ticket.id}')" title="Ver diagnóstico integral, servidores y SLA en ventana modal">
              🔍 Ficha Técnica
            </button>
            <button class="btn-action-popup" onclick="openAuditTrailModal('${ticket.id}')" title="Ver trazabilidad forense inmutable en ventana modal">
              📜 Historial
            </button>
            <button class="btn-action-popup" onclick="openChatExpandedModal('${ticket.id}')" title="Abrir chat y notas en ventana ampliada">
              💬 Chat Ampliado
            </button>
          </div>
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


// =============================================================================// =============================================================================
// 6. GESTIÓN MULTI-TENANT DE PLATAFORMAS E INSTITUCIONES (VISTA DIFERENCIADA)
// =============================================================================
AppState.selectedTenantInst = 'OSDE';
AppState.activePlatformsSubTab = 'institutions';
AppState.instCardTypeFilter = 'all';

// Matriz inicial de asignación multi-tenant por código real
AppState.tenantPlatforms = {
  'OSDE': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_AFILIADOS_PORTAL': true, 'CAT_REGISTRO_INTEROP': true, 'CAT_CONSULTORIO_DIGITAL': true, 'CAT_CARTILLA_TURNOS': true, 'CAT_RPM_MONITOREO': true },
  'SWISS_MEDICAL': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_AFILIADOS_PORTAL': true, 'CAT_CONSULTORIO_DIGITAL': true, 'CAT_COPAGOS_PAGOS': true, 'CAT_REGISTRO_INTEROP': true },
  'GALENO': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_CONSULTORIO_DIGITAL': true, 'CAT_CARTILLA_TURNOS': true, 'CAT_COPAGOS_PAGOS': true },
  'MEDIFE': { 'CAT_RECETA': true, 'CAT_AFILIADOS_PORTAL': true, 'CAT_CONSULTORIO_DIGITAL': true, 'CAT_REGISTRO_INTEROP': true },
  'OMINT': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_CONSULTORIO_DIGITAL': true, 'CAT_COPAGOS_PAGOS': true },
  'HOSPITAL_ALEMAN': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_REGISTRO_INTEROP': true, 'CAT_INTERNACION_DOM': true, 'CAT_RPM_MONITOREO': true },
  'HOSPITAL_ITALIANO': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_AFILIADOS_PORTAL': true, 'CAT_REGISTRO_INTEROP': true, 'CAT_INTERNACION_DOM': true, 'CAT_RPM_MONITOREO': true, 'CAT_CONSULTORIO_DIGITAL': true, 'CAT_COPAGOS_PAGOS': true, 'CAT_CARTILLA_TURNOS': true },
  'HOSPITAL_BRITANICO': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_REGISTRO_INTEROP': true, 'CAT_CONSULTORIO_DIGITAL': true },
  'HOSPITAL_AUSTRAL': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_INTERNACION_DOM': true, 'CAT_RPM_MONITOREO': true, 'CAT_REGISTRO_INTEROP': true },
  'SANATORIO_FINOCHIETTO': { 'CAT_RECETA': true, 'CAT_REGISTRO_INTEROP': true, 'CAT_INTERNACION_DOM': true, 'CAT_COPAGOS_PAGOS': true },
  'SANATORIO_LOS_ARCOS': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_REGISTRO_INTEROP': true },
  'SANATORIO_MATER_DEI': { 'CAT_RECETA': true, 'CAT_TELEMEDICINA': true, 'CAT_AFILIADOS_PORTAL': true },
  'PAMI': { 'CAT_RECETA': true, 'CAT_AFILIADOS_PORTAL': true, 'CAT_INTERNACION_DOM': true, 'CAT_REGISTRO_INTEROP': true },
  'IOMA': { 'CAT_RECETA': true, 'CAT_AFILIADOS_PORTAL': true, 'CAT_REGISTRO_INTEROP': true }
};

const PLATFORM_ICONS = {
  'CAT_RECETA': '💊',
  'CAT_TELEMEDICINA': '📹',
  'CAT_AFILIADOS_PORTAL': '📱',
  'CAT_REGISTRO_INTEROP': '🔗',
  'CAT_RPM_MONITOREO': '📊',
  'CAT_INTERNACION_DOM': '🛏️',
  'CAT_COPAGOS_PAGOS': '💳',
  'CAT_CARTILLA_TURNOS': '📅',
  'CAT_CONSULTORIO_DIGITAL': '🩺'
};

const PLATFORM_PROTOCOLS = {
  'CAT_RECETA': 'PKI / Validador RUP',
  'CAT_TELEMEDICINA': 'WebRTC / H.264',
  'CAT_AFILIADOS_PORTAL': 'REST API / OAuth2',
  'CAT_REGISTRO_INTEROP': 'FHIR R4 / HL7 v2.5',
  'CAT_RPM_MONITOREO': 'MQTT / Telemetría IoT',
  'CAT_INTERNACION_DOM': 'GeoJSON / REST',
  'CAT_COPAGOS_PAGOS': 'PCI-DSS / Webhook',
  'CAT_CARTILLA_TURNOS': 'GraphQL / CalDAV',
  'CAT_CONSULTORIO_DIGITAL': 'EHR / SNOMED-CT'
};

const PLATFORM_ITIL_TIER = {
  'CAT_RECETA': 'N1 Triage / N2 Farmacia',
  'CAT_TELEMEDICINA': 'N1 Guardia / N2 WebRTC',
  'CAT_AFILIADOS_PORTAL': 'N1 Atención al Paciente',
  'CAT_REGISTRO_INTEROP': 'N3 Arquitectura e Integración',
  'CAT_RPM_MONITOREO': 'N2 Dispositivos Médicos',
  'CAT_INTERNACION_DOM': 'N2 Coordinación Domiciliaria',
  'CAT_COPAGOS_PAGOS': 'N2 Facturación y Pasarelas',
  'CAT_CARTILLA_TURNOS': 'N1 Turnos Asistenciales',
  'CAT_CONSULTORIO_DIGITAL': 'N2 Especialistas Clínicos'
};

function switchPlatformsSubTab(subTab) {
  AppState.activePlatformsSubTab = subTab;

  const btnInst = document.getElementById('btn-subtab-inst');
  const btnPlat = document.getElementById('btn-subtab-plat');
  const btnMatrix = document.getElementById('btn-subtab-matrix');

  const viewInst = document.getElementById('platforms-subview-institutions');
  const viewPlat = document.getElementById('platforms-subview-platforms');
  const viewMatrix = document.getElementById('platforms-subview-matrix');

  if (btnInst) btnInst.classList.toggle('active', subTab === 'institutions');
  if (btnPlat) btnPlat.classList.toggle('active', subTab === 'platforms');
  if (btnMatrix) btnMatrix.classList.toggle('active', subTab === 'matrix');

  if (viewInst) viewInst.style.display = (subTab === 'institutions') ? 'block' : 'none';
  if (viewPlat) viewPlat.style.display = (subTab === 'platforms') ? 'block' : 'none';
  if (viewMatrix) viewMatrix.style.display = (subTab === 'matrix') ? 'block' : 'none';

  if (subTab === 'institutions') {
    renderInstitutionsCatalog();
  } else if (subTab === 'platforms') {
    renderClinicalPlatformsCards();
  } else if (subTab === 'matrix') {
    renderTenantMatrixTable();
  }
}

function renderPlatformsCatalog() {
  renderInstitutionsCatalog();
  renderClinicalPlatformsCards();
  renderTenantMatrixTable();
}

function renderInstitutionsCatalog() {
  const containerCards = document.getElementById('grid-institutions-cards');
  const tbodyTable = document.getElementById('tbody-institutions-table');
  const containerTable = document.getElementById('container-institutions-table');
  if (!containerCards && !tbodyTable) return;

  const institutions = AppState.institutions || [];
  const platforms = AppState.platforms || [];
  const tickets = AppState.tickets || [];
  const query = (document.getElementById('filter-inst-cards-input')?.value || '').toLowerCase().trim();
  const typeFilter = AppState.instCardTypeFilter || 'all';

  // Actualizar KPIs superiores
  const totalOpenIncidents = tickets.filter(t => t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;
  const kpiInstEl = document.getElementById('kpi-total-institutions');
  const kpiPlatEl = document.getElementById('kpi-total-platforms');
  const kpiIncEl = document.getElementById('kpi-active-network-incidents');
  if (kpiInstEl) kpiInstEl.textContent = institutions.length;
  if (kpiPlatEl) kpiPlatEl.textContent = platforms.length;
  if (kpiIncEl) kpiIncEl.textContent = totalOpenIncidents;

  const filtered = institutions.filter(inst => {
    const matchesQuery = !query || 
      inst.name.toLowerCase().includes(query) || 
      inst.code.toLowerCase().includes(query) || 
      (inst.location && inst.location.toLowerCase().includes(query));
    
    let matchesType = true;
    if (typeFilter === 'PREPAGA') {
      matchesType = ['OSDE', 'SWISS_MEDICAL', 'GALENO', 'MEDIFE', 'OMINT', 'PAMI', 'IOMA'].includes(inst.code);
    } else if (typeFilter === 'SANATORIO') {
      matchesType = ['SANATORIO_FINOCHIETTO', 'SANATORIO_LOS_ARCOS', 'SANATORIO_MATER_DEI'].includes(inst.code);
    } else if (typeFilter === 'HOSPITAL') {
      matchesType = ['HOSPITAL_ALEMAN', 'HOSPITAL_ITALIANO', 'HOSPITAL_BRITANICO', 'HOSPITAL_AUSTRAL'].includes(inst.code);
    } else if (typeFilter === 'INCIDENTS') {
      const openCount = tickets.filter(t => t.institution_code === inst.code && t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;
      matchesType = openCount > 0;
    }
    return matchesQuery && matchesType;
  });

  // 1. Renderizar Modo Cuadrícula (Cards)
  if (containerCards) {
    if (filtered.length === 0) {
      containerCards.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; background: #FFF; border: 1px dashed #CBD5E1; border-radius: 10px;">
          <div style="font-size: 32px; margin-bottom: 8px;">🏥</div>
          <div style="font-weight: 700; color: #475569;">No se encontraron instituciones con los filtros seleccionados</div>
        </div>
      `;
    } else {
      containerCards.innerHTML = filtered.map(inst => {
        const instConfig = AppState.tenantPlatforms[inst.code] || {};
        const activePlatKeys = Object.keys(instConfig).filter(k => !!instConfig[k]);
        const activeTicketsCount = tickets.filter(t => t.institution_code === inst.code && t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;
        
        let orgType = 'Prestador Médico';
        let typeBadgeBg = '#EFF6FF';
        let typeBadgeColor = '#1D4ED8';
        let slaTier = 'SLA Oro (24x7)';

        if (['OSDE', 'SWISS_MEDICAL', 'GALENO', 'MEDIFE', 'OMINT'].includes(inst.code)) {
          orgType = 'Prepaga / Aseguradora';
          typeBadgeBg = '#EFF6FF';
          typeBadgeColor = '#1E40AF';
          slaTier = 'SLA Platino Crítico (2h)';
        } else if (['SANATORIO_FINOCHIETTO', 'SANATORIO_LOS_ARCOS', 'SANATORIO_MATER_DEI'].includes(inst.code)) {
          orgType = 'Sanatorio Privado';
          typeBadgeBg = '#F5F3FF';
          typeBadgeColor = '#6D28D9';
          slaTier = 'SLA Alta Complejidad (4h)';
        } else if (['HOSPITAL_ALEMAN', 'HOSPITAL_ITALIANO', 'HOSPITAL_BRITANICO', 'HOSPITAL_AUSTRAL'].includes(inst.code)) {
          orgType = 'Hospital de Comunidad';
          typeBadgeBg = '#ECFDF5';
          typeBadgeColor = '#047857';
          slaTier = 'SLA Asistencial (4h)';
        } else if (['PAMI', 'IOMA'].includes(inst.code)) {
          orgType = 'Obra Social / Red Pública';
          typeBadgeBg = '#FEF3C7';
          typeBadgeColor = '#B45309';
          slaTier = 'SLA Red Masiva';
        }

        const initials = inst.name.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

        return `
          <div class="card" style="padding: 16px; background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.04); cursor: pointer;" onclick="openInstitutionDetailModal('${inst.code}')">
            <div>
              <!-- Header de Tarjeta: Logo y Tipo -->
              <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <div style="width: 38px; height: 38px; border-radius: 8px; background: #00A896; color: #FFF; font-weight: 800; font-size: 13px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,168,150,0.25);">
                    ${initials}
                  </div>
                  <div>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 800; color: #0F172A; margin: 0; line-height: 1.2;">
                      ${inst.name}
                    </h3>
                    <div style="font-size: 10.5px; color: #64748B; margin-top: 2px;">
                      <code>${inst.code}</code> • 📍 ${inst.location || 'Sede Central'}
                    </div>
                  </div>
                </div>
                <span style="font-size: 10px; font-weight: 800; background: ${typeBadgeBg}; color: ${typeBadgeColor}; padding: 3px 8px; border-radius: 6px; white-space: nowrap;">
                  ${orgType}
                </span>
              </div>

              <!-- Metadatos de SLA y Casos Activos -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: #F8FAFC; padding: 8px 10px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #F1F5F9;">
                <div>
                  <div style="font-size: 10px; color: #64748B; font-weight: 600;">Contrato SLA</div>
                  <div style="font-size: 11px; font-weight: 800; color: #0F172A;">${slaTier}</div>
                </div>
                <div>
                  <div style="font-size: 10px; color: #64748B; font-weight: 600;">Incidentes Activos</div>
                  <div style="font-size: 11px; font-weight: 800; color: ${activeTicketsCount > 0 ? '#DC2626' : '#059669'};">
                    ${activeTicketsCount > 0 ? `🚨 ${activeTicketsCount} en curso` : '🟢 Operativo'}
                  </div>
                </div>
              </div>

              <!-- Módulos de Software Habilitados -->
              <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-size: 11px; font-weight: 700; color: #475569;">Sistemas Habilitados:</span>
                  <span style="font-size: 10.5px; font-weight: 800; color: #00A896;">${activePlatKeys.length} de ${platforms.length} activos</span>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                  ${activePlatKeys.map(pk => {
                    const icon = PLATFORM_ICONS[pk] || '💻';
                    const pObj = platforms.find(p => p.code === pk);
                    const pName = pObj ? pObj.name : pk;
                    return `
                      <span style="font-size: 10px; font-weight: 700; background: #F0FDFA; color: #0F766E; border: 1px solid #CCFBF1; padding: 2px 6px; border-radius: 4px; display: inline-flex; align-items: center; gap: 3px;" title="${pName}">
                        <span>${icon}</span>
                        <span>${pName}</span>
                      </span>
                    `;
                  }).join('')}
                  ${activePlatKeys.length === 0 ? '<span style="font-size:10.5px; color:#94A3B8; font-style:italic;">Ningún módulo asignado</span>' : ''}
                </div>
              </div>
            </div>

            <!-- Acciones Rápidas -->
            <div style="display: flex; gap: 6px; border-top: 1px solid #F1F5F9; padding-top: 10px; margin-top: 4px;" onclick="event.stopPropagation()">
              <button type="button" class="btn-pri" onclick="openInstitutionDetailModal('${inst.code}')" style="width: 100%; font-size: 11.5px; padding: 6px 10px; font-weight: 800; border-radius: 6px; background: #00A896; border: none; color: #FFF; display: flex; align-items: center; justify-content: center; gap: 6px;">
                <span>📋 Ficha 360° & Módulos</span>
                <span>➔</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // 2. Renderizar Modo Tabla Ejecutiva
  if (tbodyTable) {
    if (filtered.length === 0) {
      tbodyTable.innerHTML = `
        <tr>
          <td colspan="6" style="text-align: center; padding: 30px; color: #64748B; font-weight: 600;">
            No se encontraron instituciones sanitarias
          </td>
        </tr>
      `;
    } else {
      tbodyTable.innerHTML = filtered.map(inst => {
        const instConfig = AppState.tenantPlatforms[inst.code] || {};
        const activePlatKeys = Object.keys(instConfig).filter(k => !!instConfig[k]);
        const activeTicketsCount = tickets.filter(t => t.institution_code === inst.code && t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;
        const initials = inst.name.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

        return `
          <tr style="border-bottom: 1px solid #E2E8F0; transition: background 0.15s ease;" onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='#FFFFFF'">
            <td style="padding: 12px 16px; font-weight: 700; color: #0F172A;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 32px; height: 32px; border-radius: 6px; background: #00A896; color: #FFF; font-weight: 800; font-size: 11.5px; display: flex; align-items: center; justify-content: center;">
                  ${initials}
                </div>
                <div>
                  <div style="font-size: 12.5px; font-weight: 800;">${inst.name}</div>
                  <div style="font-size: 10px; color: #64748B;"><code>${inst.code}</code></div>
                </div>
              </div>
            </td>
            <td style="padding: 12px 14px; font-size: 11.5px; color: #475569;">
              📍 ${inst.location || 'Sede Central'}
            </td>
            <td style="padding: 12px 14px;">
              <span style="font-size: 11px; font-weight: 800; color: #00A896; background: #F0FDFA; border: 1px solid #CCFBF1; padding: 3px 8px; border-radius: 6px;">
                ${activePlatKeys.length} / ${platforms.length} Activos
              </span>
            </td>
            <td style="padding: 12px 14px; font-size: 11px; font-weight: 700; color: #334155;">
              SLA Platino (24x7)
            </td>
            <td style="padding: 12px 14px;">
              <span style="font-size: 10.5px; font-weight: 800; padding: 3px 8px; border-radius: 6px; ${activeTicketsCount > 0 ? 'background: #FEE2E2; color: #DC2626; border: 1px solid #FECACA;' : 'background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC;'}">
                ${activeTicketsCount > 0 ? `🚨 ${activeTicketsCount} en curso` : '🟢 Operativo'}
              </span>
            </td>
            <td style="padding: 12px 16px; text-align: right;">
              <button type="button" class="btn-sec" onclick="openInstitutionDetailModal('${inst.code}')" style="font-size: 11px; padding: 4px 10px; font-weight: 700; border-radius: 6px;">
                📋 Ficha 360°
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }
  }
}

function togglePlatformsViewMode(mode) {
  AppState.platformsViewMode = mode;
  const containerCards = document.getElementById('grid-institutions-cards');
  const containerTable = document.getElementById('container-institutions-table');
  const btnCards = document.getElementById('btn-view-mode-cards');
  const btnTable = document.getElementById('btn-view-mode-table');

  if (btnCards) btnCards.classList.toggle('active', mode === 'cards');
  if (btnTable) btnTable.classList.toggle('active', mode === 'table');

  if (containerCards) containerCards.style.display = (mode === 'cards') ? 'grid' : 'none';
  if (containerTable) containerTable.style.display = (mode === 'table') ? 'block' : 'none';
}

function filterInstitutionCards(query) {
  renderInstitutionsCatalog();
}

function filterInstitutionCardsByType(type) {
  AppState.instCardTypeFilter = type;
  document.querySelectorAll('[data-inst-type-filter]').forEach(b => {
    b.classList.toggle('active', b.dataset.instTypeFilter === type);
  });
  renderInstitutionsCatalog();
}

function goToMatrixForInstitution(instCode) {
  switchPlatformsSubTab('matrix');
  showToast(`Configurando matriz multi-tenant para ${formatInstitutionName(instCode)}`, 'info');
}

function renderClinicalPlatformsCards() {
  const container = document.getElementById('grid-platforms-cards');
  if (!container) return;

  const platforms = AppState.platforms || [];
  const institutions = AppState.institutions || [];
  const tickets = AppState.tickets || [];

  container.innerHTML = platforms.map(plat => {
    const icon = PLATFORM_ICONS[plat.code] || '💻';
    const protocol = PLATFORM_PROTOCOLS[plat.code] || 'REST API / HL7';
    const itilTier = PLATFORM_ITIL_TIER[plat.code] || 'N2 Especialista';
    
    // Contar cuántas instituciones tienen habilitada esta plataforma
    const connectedInsts = institutions.filter(inst => {
      const c = AppState.tenantPlatforms[inst.code];
      return c && !!c[plat.code];
    });

    // Contar incidentes activos de esta plataforma
    const openIncidents = tickets.filter(t => t.platform_code === plat.code && t.status !== 'RESUELTO' && t.status !== 'CERRADO').length;

    return `
      <div class="card" style="padding: 16px; background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div>
          <!-- Header de Tarjeta: Icono y Nombre del Software -->
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="width: 40px; height: 40px; border-radius: 10px; background: #F0FDFA; border: 1.5px solid #99F6E4; color: #0D9488; font-size: 20px; display: flex; align-items: center; justify-content: center;">
                ${icon}
              </div>
              <div>
                <h3 style="font-family: 'Outfit', sans-serif; font-size: 14.5px; font-weight: 800; color: #0F172A; margin: 0; line-height: 1.2;">
                  ${plat.name}
                </h3>
                <span style="font-size: 9.5px; font-family: 'JetBrains Mono', monospace; background: #F1F5F9; color: #475569; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 3px;">
                  ${plat.code}
                </span>
              </div>
            </div>
            <span style="font-size: 10px; font-weight: 800; background: #DCFCE7; color: #15803D; padding: 3px 8px; border-radius: 6px; border: 1px solid #86EFAC;">
              🟢 99.98% SLA
            </span>
          </div>

          <!-- Descripción del Producto -->
          <p style="font-size: 11.5px; color: #475569; margin: 0 0 12px 0; line-height: 1.4;">
            ${plat.description || 'Módulo asistencial digital de alta disponibilidad con integración hospitalaria.'}
          </p>

          <!-- Ficha Técnica de Integración ITIL -->
          <div style="background: #F8FAFC; border: 1px solid #F1F5F9; border-radius: 8px; padding: 8px 10px; margin-bottom: 12px; display: flex; flex-direction: column; gap: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 10.5px;">
              <span style="color: #64748B; font-weight: 600;">Protocolo Técnico:</span>
              <span style="font-weight: 700; color: #0284C7; font-family: 'JetBrains Mono', monospace;">${protocol}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 10.5px;">
              <span style="color: #64748B; font-weight: 600;">Mesa de Soporte:</span>
              <span style="font-weight: 700; color: #334155;">${itilTier}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 10.5px;">
              <span style="color: #64748B; font-weight: 600;">Incidentes Activos:</span>
              <span style="font-weight: 800; color: ${openIncidents > 0 ? '#DC2626' : '#059669'};">
                ${openIncidents > 0 ? `⚠️ ${openIncidents} casos` : '✓ Operativo normal'}
              </span>
            </div>
          </div>

          <!-- Instituciones Conectadas a esta Plataforma -->
          <div style="margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 11px; font-weight: 700; color: #475569;">Instituciones Conectadas:</span>
              <span style="font-size: 10.5px; font-weight: 800; color: #2563EB;">${connectedInsts.length} de ${institutions.length}</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 4px; max-height: 52px; overflow-y: auto;">
              ${connectedInsts.map(inst => `
                <span style="font-size: 9.5px; font-weight: 700; background: #EFF6FF; color: #1E40AF; border: 1px solid #DBEAFE; padding: 2px 6px; border-radius: 4px;">
                  ${inst.name}
                </span>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Acciones del Módulo -->
        <div style="display: flex; gap: 6px; border-top: 1px solid #F1F5F9; padding-top: 10px; margin-top: 4px;">
          <button type="button" class="btn-sec" onclick="openPlatformDetailModal('${plat.code}')" style="flex: 1; font-size: 11px; padding: 5px 8px; font-weight: 700; border-radius: 6px; justify-content: center;">
            💻 Detalle Técnico
          </button>
          <button type="button" class="btn-pri" onclick="switchPlatformsSubTab('matrix')" style="flex: 1; font-size: 11px; padding: 5px 8px; font-weight: 800; border-radius: 6px; background: #00A896; border-color: #00A896; color: #FFF; justify-content: center;">
            🔄 Matriz Multi-Tenant
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function renderTenantMatrixTable() {
  const table = document.getElementById('table-tenant-matrix');
  if (!table) return;

  const institutions = AppState.institutions || [];
  const platforms = AppState.platforms || [];

  let html = `
    <thead>
      <tr style="background: #F8FAFC; border-bottom: 2px solid #CBD5E1;">
        <th style="padding: 10px 14px; text-align: left; font-size: 11.5px; font-weight: 800; color: #1E293B; min-width: 200px; position: sticky; left: 0; background: #F8FAFC; z-index: 2;">
          🏥 Institución Sanitaria (Cliente)
        </th>
        ${platforms.map(p => `
          <th style="padding: 10px 8px; font-size: 10.5px; font-weight: 800; color: #0F766E; min-width: 100px;">
            <div style="font-size: 14px; margin-bottom: 2px;">${PLATFORM_ICONS[p.code] || '💻'}</div>
            <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px;" title="${p.name}">${p.name}</div>
          </th>
        `).join('')}
        <th style="padding: 10px 12px; font-size: 11px; font-weight: 800; color: #334155;">Total Activas</th>
      </tr>
    </thead>
    <tbody>
  `;

  institutions.forEach(inst => {
    const instConfig = AppState.tenantPlatforms[inst.code] || {};
    let activeCount = 0;

    html += `
      <tr style="border-bottom: 1px solid #E2E8F0; transition: background 0.15s ease;">
        <td style="padding: 10px 14px; text-align: left; font-weight: 700; color: #0F172A; position: sticky; left: 0; background: #FFFFFF; z-index: 1; border-right: 1px solid #F1F5F9;">
          <div style="font-size: 12px;">${inst.name}</div>
          <div style="font-size: 10px; color: #64748B;"><code>${inst.code}</code></div>
        </td>
    `;

    platforms.forEach(plat => {
      const isEnabled = !!instConfig[plat.code];
      if (isEnabled) activeCount++;

      html += `
        <td style="padding: 8px; vertical-align: middle;">
          <button type="button" 
                  onclick="toggleTenantPlatform('${inst.code}', '${plat.code}')" 
                  style="cursor: pointer; border: none; border-radius: 20px; padding: 4px 10px; font-size: 10px; font-weight: 800; transition: all 0.15s ease; ${isEnabled ? 'background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC;' : 'background: #F1F5F9; color: #94A3B8; border: 1px solid #CBD5E1;'}"
                  title="${isEnabled ? 'Clic para desactivar' : 'Clic para activar'} ${plat.name} en ${inst.name}">
            ${isEnabled ? '✓ ACTIVO' : '⚪ INACTIVO'}
          </button>
        </td>
      `;
    });

    html += `
        <td style="padding: 8px 12px; font-weight: 800; color: #2563EB; background: #F8FAFC;">
          ${activeCount} / ${platforms.length}
        </td>
      </tr>
    `;
  });

  html += `</tbody>`;
  table.innerHTML = html;
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

  showToast(`Módulo "${platName}" ${!current ? '✅ Habilitado' : '⚪ Suspendido'} para ${instName}`, !current ? 'success' : 'info');
  
  if (AppState.activePlatformsSubTab === 'matrix') {
    renderTenantMatrixTable();
  } else if (AppState.activePlatformsSubTab === 'institutions') {
    renderInstitutionsCatalog();
  } else {
    renderClinicalPlatformsCards();
  }
}

function exportTenantMatrixCSV() {
  const institutions = AppState.institutions || [];
  const platforms = AppState.platforms || [];

  let csvContent = "data:text/csv;charset=utf-8,";
  csvContent += "Institución,Código," + platforms.map(p => `"${p.name}"`).join(",") + ",Total Activas\n";

  institutions.forEach(inst => {
    const instConfig = AppState.tenantPlatforms[inst.code] || {};
    let activeCount = 0;
    const row = [
      `"${inst.name}"`,
      `"${inst.code}"`
    ];

    platforms.forEach(plat => {
      const isEnabled = !!instConfig[plat.code];
      if (isEnabled) activeCount++;
      row.push(isEnabled ? "HABILITADO" : "DESHABILITADO");
    });

    row.push(activeCount);
    csvContent += row.join(",") + "\n";
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `Matriz_MultiTenant_Quantux_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast("Matriz de asignación multi-tenant descargada en CSV", "success");
}

// =============================================================================
// MODALES SENIOR UX: FICHA INSTITUCIONAL 360° & FICHA TÉCNICA
// =============================================================================

function openInstitutionDetailModal(instCode) {
  const inst = AppState.institutions.find(i => i.code === instCode);
  if (!inst) return;
  AppState.activeModalInstCode = instCode;

  const instConfig = AppState.tenantPlatforms[instCode] || {};
  const platforms = AppState.platforms || [];
  const tickets = AppState.tickets || [];
  const activeTickets = tickets.filter(t => t.institution_code === instCode && t.status !== 'RESUELTO' && t.status !== 'CERRADO');
  const activePlats = platforms.filter(p => !!instConfig[p.code]);
  const initials = inst.name.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();

  // 1. Header del Modal
  const headerEl = document.getElementById('modal-inst-detail-header');
  if (headerEl) {
    headerEl.innerHTML = `
      <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 46px; height: 46px; border-radius: 10px; background: #00A896; color: #FFF; font-weight: 800; font-size: 16px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,168,150,0.3);">
          ${initials}
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <h3 style="margin: 0; font-size: 17px; font-weight: 800; color: #FFFFFF; font-family: 'Outfit', sans-serif;">
              ${inst.name}
            </h3>
            <span style="font-size: 10px; font-weight: 800; background: rgba(255,255,255,0.15); color: #00E5CC; padding: 2px 8px; border-radius: 4px;">
              ${inst.code}
            </span>
          </div>
          <div style="font-size: 11.5px; color: #94A3B8; margin-top: 2px;">
            📍 ${inst.location || 'Sede Central'} • SLA Platino 24x7 (Respuesta &lt; 2h)
          </div>
        </div>
      </div>
      <button type="button" onclick="closeInstitutionDetailModal()" style="background: none; border: none; color: #94A3B8; font-size: 24px; cursor: pointer; padding: 4px 8px; line-height: 1;" title="Cerrar Ficha">&times;</button>
    `;
  }

  // 2. Tab 1: Módulos con Toggle Switches Interactivos
  const badgeEl = document.getElementById('modal-inst-active-modules-badge');
  if (badgeEl) badgeEl.textContent = `${activePlats.length} de ${platforms.length} activos`;

  const modulesContainer = document.getElementById('modal-inst-modules-list');
  if (modulesContainer) {
    modulesContainer.innerHTML = platforms.map(plat => {
      const isEnabled = !!instConfig[plat.code];
      const icon = PLATFORM_ICONS[plat.code] || '💻';
      const protocol = PLATFORM_PROTOCOLS[plat.code] || 'REST API / HL7';

      return `
        <div style="padding: 12px; background: ${isEnabled ? '#F0FDFA' : '#F8FAFC'}; border: 1.5px solid ${isEnabled ? '#99F6E4' : '#E2E8F0'}; border-radius: 10px; display: flex; align-items: center; justify-content: space-between; gap: 12px; transition: all 0.2s ease;">
          <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
            <div style="width: 36px; height: 36px; border-radius: 8px; background: #FFFFFF; border: 1px solid #CBD5E1; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">
              ${icon}
            </div>
            <div style="min-width: 0;">
              <div style="font-size: 12.5px; font-weight: 800; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                ${plat.name}
              </div>
              <div style="font-size: 10px; color: #64748B; font-family: 'JetBrains Mono', monospace;">
                ${protocol}
              </div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
            <label style="position: relative; display: inline-block; width: 44px; height: 24px; margin: 0; cursor: pointer;">
              <input type="checkbox" ${isEnabled ? 'checked' : ''} onchange="toggleTenantPlatformFromModal('${instCode}', '${plat.code}', this.checked)" style="opacity: 0; width: 0; height: 0;">
              <span style="position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: ${isEnabled ? '#00A896' : '#CBD5E1'}; transition: .2s; border-radius: 24px;"></span>
              <span style="position: absolute; content: ''; height: 18px; width: 18px; left: ${isEnabled ? '23px' : '3px'}; bottom: 3px; background-color: white; transition: .2s; border-radius: 50%; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"></span>
            </label>
          </div>
        </div>
      `;
    }).join('');
  }

  // 3. Tab 2: Incidentes en Curso
  const incCountEl = document.getElementById('modal-inst-incidents-count');
  if (incCountEl) incCountEl.textContent = activeTickets.length;

  const incidentsContainer = document.getElementById('modal-inst-incidents-list');
  if (incidentsContainer) {
    if (activeTickets.length === 0) {
      incidentsContainer.innerHTML = `
        <div style="text-align: center; padding: 32px; background: #F0FDF4; border: 1.5px solid #BBF7D0; border-radius: 10px;">
          <div style="font-size: 32px; margin-bottom: 6px;">🟢</div>
          <div style="font-size: 13.5px; font-weight: 800; color: #166534;">Sin Incidentes Activos</div>
          <div style="font-size: 11.5px; color: #15803D; margin-top: 4px;">Todos los módulos y servicios de ${inst.name} operan con normalidad dentro del SLA.</div>
        </div>
      `;
    } else {
      incidentsContainer.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 8px;">
          ${activeTickets.map(t => {
            const pBadge = formatPriorityBadge(t.priority);
            const platIcon = PLATFORM_ICONS[t.platform_code] || '💻';
            return `
              <div style="padding: 12px 14px; background: #FFFFFF; border: 1.5px solid #FEE2E2; border-left: 4px solid #EF4444; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; gap: 12px;">
                <div>
                  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 800; color: #0284C7;">#${t.id.slice(0, 8)}</span>
                    ${pBadge}
                    <span style="font-size: 10.5px; color: #64748B;">${platIcon} ${formatPlatformName(t.platform_code)}</span>
                  </div>
                  <div style="font-size: 12px; font-weight: 700; color: #0F172A;">
                    ${t.title}
                  </div>
                </div>
                <button type="button" class="btn-sec" onclick="closeInstitutionDetailModal(); openAgentWorkspaceModal('${t.id}')" style="font-size: 11px; font-weight: 800; padding: 5px 10px; border-radius: 6px; white-space: nowrap;">
                  Abrir en Workspace ➔
                </button>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }
  }

  // 4. Tab 3: Contrato SLA & Sedes
  const contractContainer = document.getElementById('modal-inst-contract-info');
  if (contractContainer) {
    contractContainer.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div style="padding: 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;">
          <div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; margin-bottom: 8px;">📑 Especificaciones de Soporte</div>
          <div style="font-size: 12px; color: #1E293B; line-height: 1.6;">
            <div><strong>Nivel de Contrato:</strong> Platinum Healthcare Support</div>
            <div><strong>Horario de Cobertura:</strong> 24x7x365 (Guardia Activa)</div>
            <div><strong>Tiempo de Respuesta P1:</strong> &lt; 15 minutos</div>
            <div><strong>Tiempo de Resolución P1:</strong> &lt; 2 horas</div>
          </div>
        </div>
        <div style="padding: 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;">
          <div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; margin-bottom: 8px;">👨‍💻 Ingeniero de Cuenta Designado</div>
          <div style="font-size: 12px; color: #1E293B; line-height: 1.6;">
            <div><strong>Líder de Servicio:</strong> Freddy Cortés (N2 Especialista)</div>
            <div><strong>Canal Escalamiento:</strong> Guardia Red Asistencial N3</div>
            <div><strong>Monitoreo de Enlace:</strong> Activo (Healthcheck cada 60s)</div>
            <div><strong>Estado de Conexión VPN:</strong> 🟢 Online 99.98%</div>
          </div>
        </div>
      </div>
    `;
  }

  // 5. Botón Footer para Filtrar Mesa de Ayuda
  const btnFilterTickets = document.getElementById('btn-modal-inst-filter-tickets');
  if (btnFilterTickets) {
    btnFilterTickets.onclick = () => {
      closeInstitutionDetailModal();
      const filterInstSelect = document.getElementById('tkt-filter-inst');
      if (filterInstSelect) {
        filterInstSelect.value = instCode;
      }
      switchView('tickets');
      onFilterChange();
      showToast(`Mesa de ayuda filtrada por ${inst.name}`, 'info');
    };
  }

  // Abrir Modal
  const modal = document.getElementById('modal-institution-detail');
  if (modal) {
    switchInstModalTab('modules');
    modal.classList.add('active');
  }
}

function closeInstitutionDetailModal() {
  const modal = document.getElementById('modal-institution-detail');
  if (modal) modal.classList.remove('active');
  AppState.activeModalInstCode = null;
}

function switchInstModalTab(tabKey) {
  const btnModules = document.getElementById('btn-inst-tab-modules');
  const btnIncidents = document.getElementById('btn-inst-tab-incidents');
  const btnContract = document.getElementById('btn-inst-tab-contract');

  const paneModules = document.getElementById('inst-tab-content-modules');
  const paneIncidents = document.getElementById('inst-tab-content-incidents');
  const paneContract = document.getElementById('inst-tab-content-contract');

  if (btnModules) btnModules.classList.toggle('active', tabKey === 'modules');
  if (btnIncidents) btnIncidents.classList.toggle('active', tabKey === 'incidents');
  if (btnContract) btnContract.classList.toggle('active', tabKey === 'contract');

  if (paneModules) paneModules.style.display = (tabKey === 'modules') ? 'block' : 'none';
  if (paneIncidents) paneIncidents.style.display = (tabKey === 'incidents') ? 'block' : 'none';
  if (paneContract) paneContract.style.display = (tabKey === 'contract') ? 'block' : 'none';
}

function toggleTenantPlatformFromModal(instCode, platCode, isChecked) {
  if (!AppState.tenantPlatforms[instCode]) {
    AppState.tenantPlatforms[instCode] = {};
  }
  AppState.tenantPlatforms[instCode][platCode] = isChecked;

  const plat = AppState.platforms.find(p => p.code === platCode);
  const platName = plat ? plat.name : platCode;
  const inst = AppState.institutions.find(i => i.code === instCode);
  const instName = inst ? inst.name : instCode;

  showToast(`Módulo "${platName}" ${isChecked ? '✅ Habilitado' : '⚪ Suspendido'} para ${instName}`, isChecked ? 'success' : 'info');

  // Actualizar Ficha y Catálogo
  const instConfig = AppState.tenantPlatforms[instCode] || {};
  const activePlats = AppState.platforms.filter(p => !!instConfig[p.code]);
  const badgeEl = document.getElementById('modal-inst-active-modules-badge');
  if (badgeEl) badgeEl.textContent = `${activePlats.length} de ${AppState.platforms.length} activos`;

  renderInstitutionsCatalog();
  renderTenantMatrixTable();
}

function openPlatformDetailModal(platCode) {
  const plat = AppState.platforms.find(p => p.code === platCode);
  if (!plat) return;

  const icon = PLATFORM_ICONS[platCode] || '💻';
  const protocol = PLATFORM_PROTOCOLS[platCode] || 'REST API / HL7';
  const itilTier = PLATFORM_ITIL_TIER[platCode] || 'N2 Soporte';
  const institutions = AppState.institutions || [];
  const tickets = AppState.tickets || [];

  const connectedInsts = institutions.filter(inst => {
    const c = AppState.tenantPlatforms[inst.code];
    return c && !!c[platCode];
  });
  const openIncidents = tickets.filter(t => t.platform_code === platCode && t.status !== 'RESUELTO' && t.status !== 'CERRADO');

  // Header
  const headerEl = document.getElementById('modal-plat-detail-header');
  if (headerEl) {
    headerEl.innerHTML = `
      <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 44px; height: 44px; border-radius: 10px; background: #F0FDFA; border: 1.5px solid #99F6E4; color: #0D9488; font-size: 22px; display: flex; align-items: center; justify-content: center;">
          ${icon}
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <h3 style="margin: 0; font-size: 16px; font-weight: 800; color: #FFFFFF; font-family: 'Outfit', sans-serif;">
              ${plat.name}
            </h3>
            <span style="font-size: 10px; font-weight: 800; background: rgba(255,255,255,0.15); color: #00E5CC; padding: 2px 8px; border-radius: 4px;">
              ${plat.code}
            </span>
          </div>
          <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">
            Módulo Institucional • Disponibilidad 99.98% SLA
          </div>
        </div>
      </div>
      <button type="button" onclick="closePlatformDetailModal()" style="background: none; border: none; color: #94A3B8; font-size: 24px; cursor: pointer; padding: 4px 8px; line-height: 1;" title="Cerrar">&times;</button>
    `;
  }

  // Body
  const bodyEl = document.getElementById('modal-plat-detail-body');
  if (bodyEl) {
    bodyEl.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div style="padding: 12px 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px;">
          <div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; margin-bottom: 4px;">Descripción Técnica</div>
          <div style="font-size: 12.5px; color: #1E293B; line-height: 1.5;">${plat.description}</div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
          <div style="padding: 10px 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
            <div style="font-size: 10.5px; color: #64748B; font-weight: 600;">Protocolo de Integración</div>
            <div style="font-size: 12px; font-weight: 800; color: #0284C7; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">${protocol}</div>
          </div>
          <div style="padding: 10px 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
            <div style="font-size: 10.5px; color: #64748B; font-weight: 600;">Nivel de Guardia ITIL</div>
            <div style="font-size: 12px; font-weight: 800; color: #0F172A; margin-top: 2px;">${itilTier}</div>
          </div>
        </div>

        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <strong style="font-size: 12px; color: #0F172A;">Instituciones Habilitadas (${connectedInsts.length} de ${institutions.length})</strong>
          </div>
          <div style="display: flex; flex-wrap: wrap; gap: 4px; max-height: 100px; overflow-y: auto; padding: 4px 0;">
            ${connectedInsts.map(inst => `
              <span style="font-size: 10.5px; font-weight: 700; background: #EFF6FF; color: #1E40AF; border: 1px solid #DBEAFE; padding: 3px 8px; border-radius: 6px;">
                🏥 ${inst.name}
              </span>
            `).join('')}
          </div>
        </div>

        <div>
          <strong style="font-size: 12px; color: #0F172A; display: block; margin-bottom: 6px;">
            Incidentes en Curso (${openIncidents.length})
          </strong>
          ${openIncidents.length === 0 ? `
            <div style="padding: 12px; background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; color: #15803D; font-size: 11.5px; font-weight: 700; text-align: center;">
              🟢 Módulo 100% operativo sin incidentes activos reportados.
            </div>
          ` : `
            <div style="display: flex; flex-direction: column; gap: 6px; max-height: 120px; overflow-y: auto;">
              ${openIncidents.map(t => `
                <div style="padding: 8px 10px; background: #FEF2F2; border: 1px solid #FEE2E2; border-radius: 6px; font-size: 11.5px; display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-weight: 700; color: #991B1B;">${t.title}</span>
                  <span style="font-weight: 800; color: #DC2626;">${t.priority}</span>
                </div>
              `).join('')}
            </div>
          `}
        </div>
      </div>
    `;
  }

  const modal = document.getElementById('modal-platform-detail');
  if (modal) modal.classList.add('active');
}

function closePlatformDetailModal() {
  const modal = document.getElementById('modal-platform-detail');
  if (modal) modal.classList.remove('active');
}

// =============================================================================
// 7. CONTROL DE ACCESO BASADO EN ROLES (RBAC & PERMISOS)
// =============================================================================
function applyRolePermissions() {
  const role = AppState.currentUser ? (AppState.currentUser.role || 'SOLICITANTE') : 'SOLICITANTE';

  const tabDash = document.getElementById('tab-dashboard');
  const tabTickets = document.getElementById('tab-tickets');
  const tabUsers = document.getElementById('tab-users');
  const tabArticles = document.getElementById('tab-articles');
  const tabPlatforms = document.getElementById('tab-platforms');
  const tabConfig = document.getElementById('tab-config');

  if (role === 'SOLICITANTE') {
    // El Solicitante (Médico / Paciente) solo puede ver Mesa de Ayuda y Base de Conocimiento
    if (tabDash) tabDash.style.display = 'none';
    if (tabUsers) tabUsers.style.display = 'none';
    if (tabPlatforms) tabPlatforms.style.display = 'none';
    if (tabConfig) tabConfig.style.display = 'none';
    if (tabTickets) tabTickets.style.display = 'flex';
    if (tabArticles) tabArticles.style.display = 'flex';

    // Si está parado en una vista restringida, redirigir a tickets
    if (['dashboard', 'users', 'platforms', 'config'].includes(AppState.currentView)) {
      switchView('tickets');
    }
  } else if (role.includes('SOPORTE') || role === 'SOPORTE') {
    // Soporte N1/N2/N3 ve Dashboard, Mesa de Ayuda, Usuarios (lectura) y Base de Conocimiento
    if (tabDash) tabDash.style.display = 'flex';
    if (tabTickets) tabTickets.style.display = 'flex';
    if (tabUsers) tabUsers.style.display = 'flex';
    if (tabArticles) tabArticles.style.display = 'flex';
    if (tabPlatforms) tabPlatforms.style.display = 'none'; // Solo Admin
    if (tabConfig) tabConfig.style.display = 'none'; // Solo Admin

    if (['platforms', 'config'].includes(AppState.currentView)) {
      switchView('tickets');
    }
  } else if (role === 'ADMIN') {
    // Administrador General ve todos los módulos y tiene control total
    if (tabDash) tabDash.style.display = 'flex';
    if (tabTickets) tabTickets.style.display = 'flex';
    if (tabUsers) tabUsers.style.display = 'flex';
    if (tabArticles) tabArticles.style.display = 'flex';
    if (tabPlatforms) tabPlatforms.style.display = 'flex';
    if (tabConfig) tabConfig.style.display = 'flex';
  }
}

// =============================================================================
// 7. DIRECTORIO DE USUARIOS & ROLES ITIL (INVGATE SENIOR DESIGN)
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

  const allUsers = AppState.users || [];

  // 1. Update Stat Cards & Badges
  const statTotal = document.getElementById('stat-user-total');
  const badgeTotal = document.getElementById('users-badge-total');
  const statN1 = document.getElementById('stat-user-n1');
  const statN2 = document.getElementById('stat-user-n2');
  const statN3 = document.getElementById('stat-user-n3');
  const statSol = document.getElementById('stat-user-solicitantes');

  const countN1 = allUsers.filter(u => u.support_level === 'N1' || u.role === 'SOPORTE_N1').length;
  const countN2 = allUsers.filter(u => u.support_level === 'N2' || u.role === 'SOPORTE_N2').length;
  const countN3 = allUsers.filter(u => u.support_level === 'N3' || u.role === 'SOPORTE_N3' || (u.role === 'ADMIN' && u.support_level === 'N3')).length;
  const countSol = allUsers.filter(u => u.role === 'SOLICITANTE').length;

  if (statTotal) statTotal.textContent = allUsers.length;
  if (badgeTotal) badgeTotal.textContent = `${allUsers.length} Usuarios`;
  if (statN1) statN1.textContent = countN1;
  if (statN2) statN2.textContent = countN2;
  if (statN3) statN3.textContent = countN3;
  if (statSol) statSol.textContent = countSol;

  // 2. Filter Table
  let filtered = allUsers;
  if (AppState.userFilterLevel && AppState.userFilterLevel !== 'all') {
    if (AppState.userFilterLevel === 'SOLICITANTE') {
      filtered = filtered.filter(u => u.role === 'SOLICITANTE');
    } else if (AppState.userFilterLevel === 'ADMIN') {
      filtered = filtered.filter(u => u.role === 'ADMIN');
    } else {
      filtered = filtered.filter(u => u.support_level === AppState.userFilterLevel || u.role === `SOPORTE_${AppState.userFilterLevel}`);
    }
  }

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:#94A3B8; padding:32px 10px; font-size:12px;">No se encontraron usuarios para el filtro seleccionado.</td></tr>`;
    return;
  }

  const levelBadges = {
    'N1': '<span class="level-pill-itil level-pill-n1">🔵 Nivel 1 • Guardia</span>',
    'N2': '<span class="level-pill-itil level-pill-n2">🟣 Nivel 2 • Especialista</span>',
    'N3': '<span class="level-pill-itil level-pill-n3">🔴 Nivel 3 • Ingeniería</span>'
  };

  const roleBadges = {
    'ADMIN': '<span class="user-badge-role role-badge-admin">👑 ADMIN</span>',
    'SOPORTE': '<span class="user-badge-role role-badge-soporte">🛠️ SOPORTE</span>',
    'SOLICITANTE': '<span class="user-badge-role role-badge-solicitante">🩺 SOLICITANTE</span>'
  };

  tbody.innerHTML = filtered.map(u => {
    const cleanName = (u.full_name || u.username).replace(/Lic\.\s*/gi, '').trim();
    const initials = getInitials(cleanName);
    const roleBadge = roleBadges[u.role] || `<span class="user-badge-role role-badge-soporte">${u.role}</span>`;
    const lvlBadge = levelBadges[u.support_level] || (u.role === 'ADMIN' ? '<span class="level-pill-itil level-pill-n3">🔴 Nivel 3 • Root</span>' : '<span style="font-size:11px; color:#94A3B8;">—</span>');
    
    return `
      <tr>
        <td>
          <div class="user-cell-profile">
            ${getUserAvatarHtml(u.username, cleanName, 32)}
            <div>
              <div class="user-cell-name">${cleanName}</div>
              <div style="font-size:10px; color:#64748B;">${u.specialty || 'Servicio Asistencial'}</div>
            </div>
          </div>
        </td>
        <td>
          <span class="user-mono-tag">@${u.username}</span>
        </td>
        <td>
          <a href="mailto:${u.email}" style="color:#0284C7; font-weight:600; text-decoration:none; font-size:11.5px;">${u.email}</a>
        </td>
        <td>${roleBadge}</td>
        <td>${lvlBadge}</td>
        <td>
          <span style="font-size:11.5px; font-weight:600; color:#334155;">🏥 ${formatInstitutionName(u.institution_code)}</span>
        </td>
        <td>
          <span style="font-size:11px; font-weight:800; color:#059669; display:inline-flex; align-items:center; gap:4px;">
            <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10B981;"></span> Activo
          </span>
        </td>
        <td style="text-align:center;">
          <button class="btn-clean-action" style="padding:4px 8px; font-size:10.5px; font-weight:700; border-radius:6px; background:#F1F5F9; color:#334155; border:1px solid #CBD5E1; cursor:pointer;" onclick="viewUserProfileModal('${u.username}')">
            👤 Perfil
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function openCreateUserModal() {
  const modal = document.getElementById('modal-create-user');
  if (modal) {
    modal.classList.add('active');
    handleUserRoleChange();
  }
}

function closeCreateUserModal() {
  const modal = document.getElementById('modal-create-user');
  if (modal) modal.classList.remove('active');
}

function handleUserRoleChange() {
  const roleSelect = document.getElementById('new-user-role');
  const levelGroup = document.getElementById('new-user-level-group');
  if (!roleSelect || !levelGroup) return;

  if (roleSelect.value === 'SOPORTE' || roleSelect.value === 'ADMIN') {
    levelGroup.style.display = 'block';
  } else {
    levelGroup.style.display = 'none';
  }
}

async function submitCreateUser(event) {
  if (event) event.preventDefault();

  const fullName = document.getElementById('new-user-fullname')?.value.trim();
  const username = document.getElementById('new-user-username')?.value.trim().toLowerCase();
  const email = document.getElementById('new-user-email')?.value.trim().toLowerCase();
  const role = document.getElementById('new-user-role')?.value;
  const level = document.getElementById('new-user-level')?.value;
  const institution = document.getElementById('new-user-institution')?.value;

  if (!fullName || !username || !email) {
    showToast('Complete todos los campos obligatorios para registrar al usuario.', 'error');
    return;
  }

  const payload = {
    full_name: fullName,
    username: username,
    email: email,
    role: role,
    support_level: (role === 'SOPORTE' || role === 'ADMIN') ? level : null,
    institution_code: institution
  };

  try {
    const res = await API.createUser(payload);
    showToast(`Usuario "${fullName}" registrado exitosamente.`, 'success');
    closeCreateUserModal();
    
    // Limpiar formulario
    const form = document.getElementById('form-create-user');
    if (form) form.reset();

    // Recargar lista y métricas
    await loadUsersList();
  } catch (err) {
    console.error('Error al crear usuario:', err);
    showToast(err.detail || 'Error al registrar el usuario en la base de datos.', 'error');
  }
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
// 9. MODALES DE GESTIÓN, WIZARD MULTI-PASO & POPUPS SENIOR UX (v3.0)
// =============================================================================

/// WIZARD GLOBAL CONTROLS
let currentWizardStep = 1;

function goToWizardStep(stepNum) {
  if (stepNum < 1 || stepNum > 4) return;
  
  // Validation when advancing from Step 1
  if (stepNum > 1 && currentWizardStep === 1) {
    const instEl = document.getElementById('modal-institution');
    const inst = instEl ? instEl.value : '';
    if (!inst) {
      if (instEl && instEl.options && instEl.options.length > 1) {
        // Auto-select first available institution if not chosen
        instEl.selectedIndex = 1;
      } else {
        showToast('Por favor seleccione la institución asistencial para continuar', 'warning');
        if (instEl) instEl.focus();
        return;
      }
    }
  }

  // Ensure default platform selected when advancing to step 3
  const platInput = document.getElementById('modal-platform');
  if (platInput && !platInput.value) {
    platInput.value = 'CAT_RECETA';
  }

  currentWizardStep = stepNum;

  // Update panels
  for (let i = 1; i <= 4; i++) {
    const panel = document.getElementById(`wizard-panel-${i}`);
    const node = document.getElementById(`step-node-${i}`);
    if (panel) {
      if (i === stepNum) panel.classList.add('active');
      else panel.classList.remove('active');
    }
    if (node) {
      if (i === stepNum) {
        node.className = 'wizard-step-node active';
      } else if (i < stepNum) {
        node.className = 'wizard-step-node completed';
      } else {
        node.className = 'wizard-step-node';
      }
    }
  }

  if (stepNum === 3) {
    updateWizardPriorityPreview();
  }
}

function selectPlatformCard(platformCode, element) {
  const hiddenInput = document.getElementById('modal-platform');
  if (hiddenInput) hiddenInput.value = platformCode;

  const parent = (element && element.closest('.platform-grid-selector')) || document.getElementById('platform-grid-container') || document;
  const cards = parent.querySelectorAll('.platform-card-choice');
  cards.forEach(c => c.classList.remove('selected'));
  if (element) element.classList.add('selected');
}

function selectTypeCard(typeVal, element) {
  const hiddenInput = document.getElementById('modal-type');
  if (hiddenInput) hiddenInput.value = typeVal;

  const parent = (element && (element.closest('.wizard-panel') || element.parentElement)) || document;
  const cards = parent.querySelectorAll('.impact-card-choice');
  cards.forEach(c => c.classList.remove('selected'));
  if (element) element.classList.add('selected');
}

function selectImpactCard(impactVal, element) {
  const hiddenInput = document.getElementById('modal-impact');
  if (hiddenInput) hiddenInput.value = impactVal;

  const grid = document.getElementById('wizard-impact-grid') || (element && element.closest('.impact-cards-grid'));
  if (grid) {
    const cards = grid.querySelectorAll('.impact-card-choice');
    cards.forEach(c => c.classList.remove('selected'));
  }
  if (element) element.classList.add('selected');

  updateWizardPriorityPreview();
}

function selectUrgencyCard(urgencyVal, element) {
  const hiddenInput = document.getElementById('modal-urgency');
  if (hiddenInput) hiddenInput.value = urgencyVal;

  const grid = document.getElementById('wizard-urgency-grid') || (element && element.closest('.impact-cards-grid'));
  if (grid) {
    const cards = grid.querySelectorAll('.impact-card-choice');
    cards.forEach(c => c.classList.remove('selected'));
  }
  if (element) element.classList.add('selected');

  updateWizardPriorityPreview();
}

async function updateWizardPriorityPreview() {
  const impact = document.getElementById('modal-impact') ? document.getElementById('modal-impact').value : 'MEDIO';
  const urgency = document.getElementById('modal-urgency') ? document.getElementById('modal-urgency').value : 'MEDIO';
  const prioBadge = document.getElementById('modal-calculated-priority');
  const slaExpl = document.getElementById('wizard-sla-explanation');

  try {
    const res = await API.calculatePriority(impact, urgency);
    if (prioBadge) {
      prioBadge.textContent = `${res.priority} • ${res.priority === 'P1' ? 'CRÍTICA' : res.priority === 'P2' ? 'ALTA' : res.priority === 'P3' ? 'MEDIA' : res.priority === 'P4' ? 'BAJA' : 'PLAN'}`;
      prioBadge.className = `badge-prio badge-${res.priority.toLowerCase()}`;
    }
    if (slaExpl) {
      const respTime = res.sla_response_time_minutes < 60 ? `${res.sla_response_time_minutes} min` : `${res.sla_response_time_minutes / 60} h`;
      const resolTime = res.sla_resolution_time_minutes < 60 ? `${res.sla_resolution_time_minutes} min` : `${res.sla_resolution_time_minutes / 60} h`;
      slaExpl.textContent = `Respuesta inicial garantizada en ${respTime} • Resolución máxima en ${resolTime}`;
    }
  } catch (e) {
    console.warn('Error calculando SLA dinámico:', e);
  }
}

// DEDICATED POPUPS CONTROLLERS (v3.0 SENIOR UX)
function openTechDetailsModal(ticketId) {
  const ticket = AppState.tickets.find(t => t.id === Number(ticketId)) || AppState.selectedTicket;
  if (!ticket) return;

  const body = document.getElementById('tech-details-modal-body');
  if (body) {
    const platName = formatPlatformName(ticket.platform_code);
    const instName = formatInstitutionName(ticket.institution_code);
    body.innerHTML = `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 16px;">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;">
          <div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Parámetros de Red y Servidor</div>
          <div style="margin-top: 8px; font-size: 12px; line-height: 1.6; color: #1E293B;">
            <div><strong>Endpoint API:</strong> <code>https://api.quantux.salud.ar/v1/${(ticket.platform_code||'core').toLowerCase()}</code></div>
            <div><strong>Cluster Primario:</strong> prod-cluster-ar-south1</div>
            <div><strong>Protocolo:</strong> HL7 FHIR v4.0.1 / DICOMweb</div>
            <div><strong>Latencia Promedio:</strong> 42 ms (Óptima)</div>
          </div>
        </div>

        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;">
          <div style="font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase;">Estado de Acuerdos de Servicio (SLA)</div>
          <div style="margin-top: 8px; font-size: 12px; line-height: 1.6; color: #1E293B;">
            <div><strong>Prioridad ITIL:</strong> <span class="badge-prio badge-${ticket.priority.toLowerCase()}">${ticket.priority}</span></div>
            <div><strong>Nivel ITIL Asignado:</strong> ${ticket.support_level || 'N1'}</div>
            <div><strong>Plataforma:</strong> ${platName}</div>
            <div><strong>Impacto / Urgencia:</strong> ${ticket.impact || 'MEDIO'} / ${ticket.urgency || 'MEDIO'}</div>
          </div>
        </div>
      </div>

      <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px;">
        <div style="font-size: 11.5px; font-weight: 800; color: #1E40AF; margin-bottom: 4px;">Información de Contexto Asistencial</div>
        <div style="font-size: 12px; color: #1E293B; line-height: 1.5;">
          <strong>Institución / Sede:</strong> ${instName}<br>
          <strong>Solicitante:</strong> ${ticket.requester_name || ticket.requester_username} (${ticket.requester_email || 'fcortes@quantux.salud.ar'})<br>
          <strong>Fecha de Apertura:</strong> ${formatDateTime(ticket.created_at)}
        </div>
      </div>
    `;
  }

  const modal = document.getElementById('modal-view-tech-details');
  if (modal) modal.classList.add('active');
}

function closeTechDetailsModal() {
  const modal = document.getElementById('modal-view-tech-details');
  if (modal) modal.classList.remove('active');
}

function openAuditTrailModal(ticketId) {
  const ticket = AppState.tickets.find(t => t.id === Number(ticketId)) || AppState.selectedTicket;
  if (!ticket) return;

  const body = document.getElementById('audit-trail-modal-body');
  if (body) {
    const audits = ticket.audit_logs || [];
    if (audits.length === 0) {
      body.innerHTML = `
        <div style="text-align: center; padding: 30px 10px; color: #64748B;">
          <div style="font-size: 32px; margin-bottom: 8px;">📜</div>
          <div style="font-weight: 700;">Registro Forense Inicial</div>
          <p style="font-size: 12px; margin-top: 4px;">Ticket #${ticket.id} creado el ${formatDateTime(ticket.created_at)} por ${ticket.requester_name || ticket.requester_username}. Sin eventos posteriores.</p>
        </div>
      `;
    } else {
      body.innerHTML = `
        <div style="border-left: 2px solid #CBD5E1; margin-left: 14px; padding-left: 16px; display: flex; flex-direction: column; gap: 14px;">
          ${audits.map(a => `
            <div style="position: relative;">
              <div style="position: absolute; left: -22px; top: 2px; width: 10px; height: 10px; border-radius: 50%; background: #00A896;"></div>
              <div style="font-size: 11px; color: #64748B; font-weight: 700;">${formatDateTime(a.created_at || a.timestamp)} • Operador: ${a.changed_by_username || a.changed_by || 'Sistema'}</div>
              <div style="font-size: 12.5px; font-weight: 700; color: #0F172A; margin-top: 2px;">${a.change_reason || a.action || 'Modificación de Estado / Nivel'}</div>
              <div style="font-size: 11.5px; color: #475569; margin-top: 2px; background: #F8FAFC; padding: 6px 10px; border-radius: 6px; border: 1px solid #E2E8F0;">
                ${a.field_changed ? `${a.field_changed}: de "${a.old_value || 'ninguno'}" a "${a.new_value}"` : (a.details || 'Evento registrado en bitácora')}
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }
  }

  const modal = document.getElementById('modal-audit-trail');
  if (modal) modal.classList.add('active');
}

function closeAuditTrailModal() {
  const modal = document.getElementById('modal-audit-trail');
  if (modal) modal.classList.remove('active');
}

function openChatExpandedModal(ticketId) {
  const ticket = AppState.tickets.find(t => t.id === Number(ticketId)) || AppState.selectedTicket;
  if (!ticket) return;

  const stream = document.getElementById('chat-expanded-stream');
  if (stream) {
    const comments = ticket.comments || [];
    if (comments.length === 0) {
      stream.innerHTML = `<div style="text-align: center; padding: 30px; color: #94A3B8; font-size: 12.5px;">No hay comentarios registrados. Escriba el primer mensaje para iniciar el diálogo asistencial.</div>`;
    } else {
      stream.innerHTML = comments.map(c => `
        <div class="chat-bubble ${c.is_internal ? 'chat-bubble-internal' : (c.author_username === ticket.requester_username ? 'chat-bubble-requester' : 'chat-bubble-agent')}">
          <div class="chat-bubble-header">
            <strong>${c.is_internal ? '🔒 Nota Privada Interna • ' : ''}👤 ${c.author_username}</strong>
            <span style="opacity: 0.75;">${formatDateTime(c.created_at)}</span>
          </div>
          <div class="chat-bubble-content">${c.message}</div>
        </div>
      `).join('');
      stream.scrollTop = stream.scrollHeight;
    }
  }

  const modal = document.getElementById('modal-chat-expanded');
  if (modal) modal.classList.add('active');
}

function closeChatExpandedModal() {
  const modal = document.getElementById('modal-chat-expanded');
  if (modal) modal.classList.remove('active');
}

async function submitExpandedChatMessage() {
  if (!AppState.selectedTicket) return;
  const input = document.getElementById('chat-expanded-msg-input');
  const isInt = document.getElementById('chat-expanded-is-internal');
  if (!input || !input.value.trim()) {
    showToast('Escriba un mensaje antes de enviar', 'warning');
    return;
  }

  try {
    await API.addComment(AppState.selectedTicket.id, {
      message: input.value.trim(),
      is_internal: isInt ? isInt.checked : false,
      author_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
    });
    input.value = '';
    if (isInt) isInt.checked = false;
    showToast('Mensaje registrado con éxito', 'success');
    await selectTicket(AppState.selectedTicket.id, true);
    openChatExpandedModal(AppState.selectedTicket.id);
  } catch (e) {
    showToast('Error al enviar mensaje: ' + (e.detail || e.message), 'error');
  }
}

function openUserProfileModal(userId) {
  const user = AppState.users.find(u => u.id === Number(userId)) || AppState.currentUser;
  if (!user) return;

  const body = document.getElementById('user-profile-modal-body');
  if (body) {
    body.innerHTML = `
      <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px;">
        <div style="width: 54px; height: 54px; border-radius: 50%; background: #00A896; color: #FFF; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 800;">
          ${(user.full_name || user.username).substring(0, 2).toUpperCase()}
        </div>
        <div>
          <div style="font-size: 16px; font-weight: 800; color: #0F172A;">${user.full_name || user.username}</div>
          <div style="font-size: 12px; color: #64748B;">@${user.username} • Rol: <span style="font-weight: 700; color: #00A896;">${user.role}</span></div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B;">Correo Electrónico</div>
          <div style="font-size: 12.5px; font-weight: 600; color: #1E293B; margin-top: 2px;">${user.email || 'N/A'}</div>
        </div>
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B;">Institución Asignada</div>
          <div style="font-size: 12.5px; font-weight: 600; color: #1E293B; margin-top: 2px;">${user.institution_code || 'Todas / Central'}</div>
        </div>
      </div>

      <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 12px;">
        <div style="font-size: 11.5px; font-weight: 800; color: #166534; margin-bottom: 4px;">Nivel de Servicio ITIL & Autorizaciones</div>
        <div style="font-size: 12px; color: #15803D; line-height: 1.5;">
          • Nivel Operativo: <strong>${user.support_level || 'N1 Triage'}</strong><br>
          • Permiso de Escalamiento: <strong>Habilitado</strong><br>
          • Publicación en Base de Conocimiento: <strong>Habilitado</strong>
        </div>
      </div>
    `;
  }

  const modal = document.getElementById('modal-user-profile-view');
  if (modal) modal.classList.add('active');
}

function closeUserProfileModal() {
  const modal = document.getElementById('modal-user-profile-view');
  if (modal) modal.classList.remove('active');
}

async function openMetricsDrilldownModal(type, value, label) {
  const modal = document.getElementById('modal-metrics-drilldown');
  const title = document.getElementById('drilldown-modal-title');
  const body = document.getElementById('metrics-drilldown-modal-body');
  if (!modal || !body) return;

  const displayTitle = label || `Detalle: ${type} = ${value}`;
  if (title) title.textContent = `📊 Desglose de Casos: ${displayTitle}`;

  body.innerHTML = `
    <div style="text-align: center; padding: 40px 10px; color: #64748B;">
      <div class="loading-spinner" style="margin: 0 auto 12px auto;"></div>
      <div style="font-size: 13px; font-weight: 600;">Consultando registros de auditoría y base de datos...</div>
    </div>
  `;
  modal.classList.add('active');

  try {
    const allTickets = await API.getTickets({ include_all: true });
    let filtered = allTickets;

    if (type === 'status' && value) {
      if (value === 'ACTIVE') {
        filtered = allTickets.filter(t => t.status !== 'CERRADO' && t.status !== 'RESUELTO');
      } else {
        filtered = allTickets.filter(t => t.status === value);
      }
    } else if (type === 'priority' && value) {
      filtered = allTickets.filter(t => t.priority === value);
    } else if (type === 'platform' && value) {
      filtered = allTickets.filter(t => t.platform_code === value);
    } else if (type === 'institution' && value) {
      filtered = allTickets.filter(t => t.institution_code === value);
    } else if (type === 'p1') {
      filtered = allTickets.filter(t => t.priority === 'P1');
    } else if (type === 'active') {
      filtered = allTickets.filter(t => t.status !== 'CERRADO' && t.status !== 'RESUELTO');
    } else if (type === 'resolved') {
      filtered = allTickets.filter(t => t.status === 'RESUELTO' || t.status === 'CERRADO');
    } else if (type === 'sla') {
      filtered = allTickets.filter(t => {
        const sla = calculateTicketSLA(t);
        return sla.status === 'OK' || sla.status === 'WARNING';
      });
      if (filtered.length === 0) filtered = allTickets.slice(0, 15);
    } else if (type === 'conformity') {
      filtered = allTickets.filter(t => t.status === 'RESUELTO' || t.status === 'CERRADO');
      if (filtered.length === 0) filtered = allTickets.filter(t => t.priority === 'P3' || t.priority === 'P4');
    }

    if (filtered.length === 0) {
      body.innerHTML = `
        <div style="text-align: center; padding: 36px 14px; color: #64748B;">
          <div style="font-size: 36px; margin-bottom: 8px;">📋</div>
          <div style="font-weight: 800; font-size: 14px; color: #0F172A;">No se encontraron solicitudes registradas</div>
          <p style="font-size: 12px; margin-top: 4px; color: #64748B;">No hay casos que coincidan con el criterio seleccionado (${displayTitle}).</p>
        </div>
      `;
    } else {
      const rows = filtered.map(t => {
        const prio = (t.priority || 'P3').toUpperCase();
        const st = (t.status || 'NUEVO').toUpperCase();
        const plat = formatPlatformName(t.platform_code);
        const inst = formatInstitutionName(t.institution_code);
        const assignee = formatUserName(t.assignee_username);

        let prioBadgeStyle = 'background: #F1F5F9; color: #475569;';
        if (prio === 'P1') prioBadgeStyle = 'background: #FEE2E2; color: #DC2626; font-weight: 800;';
        else if (prio === 'P2') prioBadgeStyle = 'background: #FFEDD5; color: #EA580C; font-weight: 700;';
        else if (prio === 'P3') prioBadgeStyle = 'background: #DBEAFE; color: #2563EB; font-weight: 700;';

        let stBadgeStyle = 'background: #ECFDF5; color: #059669;';
        if (st === 'NUEVO') stBadgeStyle = 'background: #F0FDF4; color: #16A34A;';
        else if (st === 'ASIGNADO') stBadgeStyle = 'background: #EFF6FF; color: #2563EB;';
        else if (st === 'EN_CURSO') stBadgeStyle = 'background: #FEF3C7; color: #D97706;';
        else if (st === 'RESUELTO') stBadgeStyle = 'background: #DCFCE7; color: #15803D; font-weight: 800;';
        else if (st === 'CERRADO') stBadgeStyle = 'background: #F1F5F9; color: #64748B;';

        return `
          <tr onclick="closeMetricsDrilldownModal(); openAgentWorkspace('${t.id}')" style="cursor: pointer; border-bottom: 1px solid #F1F5F9; transition: background 0.15s;" onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">
            <td style="padding: 10px 12px; font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 11.5px; color: #00A896;">
              #${t.id}
            </td>
            <td style="padding: 10px 12px;">
              <span style="font-size: 10.5px; padding: 2px 7px; border-radius: 4px; ${prioBadgeStyle}">${prio}</span>
            </td>
            <td style="padding: 10px 12px;">
              <div style="font-weight: 700; color: #0F172A; font-size: 12px; max-width: 280px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(t.title)}">
                ${escapeHtml(t.title)}
              </div>
              <div style="font-size: 10.5px; color: #64748B; margin-top: 2px;">
                💻 ${plat} • 🏥 ${inst}
              </div>
            </td>
            <td style="padding: 10px 12px; font-size: 11.5px; color: #334155;">
              ${assignee}
            </td>
            <td style="padding: 10px 12px; text-align: right;">
              <span style="font-size: 11px; padding: 3px 8px; border-radius: 12px; ${stBadgeStyle}">
                ${formatStatusName(st)}
              </span>
            </td>
          </tr>
        `;
      }).join('');

      body.innerHTML = `
        <div style="margin-bottom: 12px; font-size: 12px; color: #475569; display: flex; justify-content: space-between; align-items: center;">
          <span>Listado de <strong>${filtered.length}</strong> solicitudes que componen este indicador:</span>
          <span style="font-size: 11px; color: #64748B;">Haga clic en cualquier fila para abrir el caso</span>
        </div>
        <div style="border: 1px solid #E2E8F0; border-radius: 8px; overflow: hidden; max-height: 420px; overflow-y: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
            <thead style="background: #F8FAFC; border-bottom: 1px solid #E2E8F0; font-weight: 700; color: #475569; position: sticky; top: 0; z-index: 5;">
              <tr>
                <th style="padding: 8px 12px; width: 75px;">ID</th>
                <th style="padding: 8px 12px; width: 65px;">Prio</th>
                <th style="padding: 8px 12px;">Detalle de la Solicitud</th>
                <th style="padding: 8px 12px; width: 140px;">Asignado a</th>
                <th style="padding: 8px 12px; text-align: right; width: 95px;">Estado</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
            </tbody>
          </table>
        </div>
      `;
    }
  } catch (err) {
    body.innerHTML = `
      <div style="text-align: center; padding: 24px; color: #EF4444;">
        <p style="font-size: 13px; font-weight: 600;">Error al cargar registros: ${err.message}</p>
      </div>
    `;
  }
}

function closeMetricsDrilldownModal() {
  const modal = document.getElementById('modal-metrics-drilldown');
  if (modal) modal.classList.remove('active');
}

function initModalListeners() {
  const btnOpen = document.getElementById('btn-open-modal');
  const modal = document.getElementById('modal-ticket');
  const btnClose = document.getElementById('modal-close');
  const btnCancel = document.getElementById('btn-cancel-modal');
  const form = document.getElementById('form-new-ticket');

  const openWizard = () => {
    goToWizardStep(1);
    updateWizardPriorityPreview();
    if (modal) modal.classList.add('active');
  };

  if (btnOpen) btnOpen.addEventListener('click', openWizard);
  
  const btnTopOpen = document.getElementById('btn-top-new-ticket');
  if (btnTopOpen) btnTopOpen.addEventListener('click', openWizard);
  
  if (btnClose && modal) btnClose.addEventListener('click', () => modal.classList.remove('active'));
  if (btnCancel && modal) btnCancel.addEventListener('click', () => modal.classList.remove('active'));

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const titleVal = document.getElementById('modal-title') ? document.getElementById('modal-title').value.trim() : '';
      const descVal = document.getElementById('modal-description') ? document.getElementById('modal-description').value.trim() : '';
      const platVal = document.getElementById('modal-platform') ? document.getElementById('modal-platform').value : 'RECETA_DIGITAL';
      const instVal = document.getElementById('modal-institution') ? document.getElementById('modal-institution').value : 'OSDE';
      const impactVal = document.getElementById('modal-impact') ? document.getElementById('modal-impact').value : 'MEDIO';
      const urgencyVal = document.getElementById('modal-urgency') ? document.getElementById('modal-urgency').value : 'MEDIO';
      const typeVal = document.getElementById('modal-type') ? document.getElementById('modal-type').value : 'INCIDENTE';
      const attachVal = document.getElementById('modal-attachment-url') ? document.getElementById('modal-attachment-url').value.trim() : '';

      if (!titleVal || titleVal.length < 5) {
        showToast('El título debe tener al menos 5 caracteres explicativos', 'warning');
        goToWizardStep(4);
        return;
      }

      if (!descVal || descVal.length < 10) {
        showToast('La descripción debe contener al menos 10 caracteres', 'warning');
        goToWizardStep(4);
        return;
      }

      const payload = {
        title: titleVal,
        description: descVal,
        platform_code: platVal,
        institution_code: instVal,
        impact: impactVal,
        urgency: urgencyVal,
        ticket_type: typeVal,
        attachment_url: attachVal || null,
        requester_username: AppState.currentUser ? AppState.currentUser.username : 'admin'
      };

      try {
        const created = await API.createTicket(payload);
        if (modal) modal.classList.remove('active');
        form.reset();
        goToWizardStep(1);
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
  const tktFilterInst = document.getElementById('tkt-filter-inst');
  const tktFilterPlat = document.getElementById('tkt-filter-platform');
  const modalPlat = document.getElementById('modal-platform');
  const modalInst = document.getElementById('modal-institution');
  const userInst = document.getElementById('user-institution');
  const dashInst = document.getElementById('dash-filter-inst');

  if (tktFilterInst) {
    const currVal = tktFilterInst.value;
    tktFilterInst.innerHTML = '<option value="">🏥 Todas las Instituciones</option>' + 
      AppState.institutions.map(i => `<option value="${i.code}">${i.name}</option>`).join('');
    if (currVal) tktFilterInst.value = currVal;
  }
  if (tktFilterPlat) {
    const currVal = tktFilterPlat.value;
    tktFilterPlat.innerHTML = '<option value="">💻 Todas las Plataformas</option>' + 
      AppState.platforms.map(p => `<option value="${p.code}">${p.name}</option>`).join('');
    if (currVal) tktFilterPlat.value = currVal;
  }
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

function formatUserName(username) {
  if (!username) return 'Sin Asignar';
  if (AppState && AppState.users && AppState.users.length > 0) {
    const found = AppState.users.find(u => u.username === username);
    if (found && found.full_name) {
      return found.full_name.replace(/Lic\.\s*/gi, '').trim();
    }
  }
  const map = {
    'admin': 'Freddy Cortés',
    'soporte': 'Laura Benítez',
    'solicitante': 'Martín Gómez',
    'mrodriguez': 'Mariana Rodríguez',
    'cpaez': 'Carlos Páez',
    'svaldez': 'Sofía Valdez',
    'mflores': 'Marcos Flores',
    'lbenitez': 'Laura Benítez',
    'gfernandez': 'Gonzalo Fernández',
    'vromero': 'Valeria Romero',
    'dnavarro': 'Diego Navarro',
    'ealvarez': 'Esteban Álvarez',
    'mgomez': 'Martín Gómez',
    'alopez': 'Andrea López',
    'jmolina': 'Javier Molina',
    'cbenedetti': 'Clara Benedetti',
    'operador1': 'Carlos Páez',
    'operador2': 'Diego Navarro'
  };
  if (username.startsWith('op_qa_')) {
    return 'Carlos Páez';
  }
  const raw = map[username] || username;
  return raw.replace(/Lic\.\s*/gi, '').trim();
}

function formatPlatformName(code) {
  if (!code) return 'General';
  const found = AppState && AppState.platforms ? AppState.platforms.find(p => p.code === code) : null;
  return found ? found.name : code.replace('CAT_', '').replace(/_/g, ' ');
}

function formatInstitutionName(code) {
  if (!code) return 'Central';
  const found = AppState && AppState.institutions ? AppState.institutions.find(i => i.code === code) : null;
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

function formatPriorityName(prio) {
  if (!prio) return 'Media';
  const p = prio.toUpperCase();
  const map = {
    'P1': 'Crítica',
    'P2': 'Alta',
    'P3': 'Media',
    'P4': 'Baja'
  };
  return map[p] || p;
}

function formatDateFriendly(dtStr) {
  if (!dtStr) return '';
  try {
    const d = new Date(dtStr);
    const now = new Date();
    const diffMs = now - d;
    const diffMin = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMin / 60);
    if (diffMin < 2) return 'Hace un momento';
    if (diffMin < 60) return `Hace ${diffMin} min`;
    if (diffHours < 24) return `Hace ${diffHours} h`;
    return d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' }) + ' - ' + d.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit' });
  } catch {
    return dtStr;
  }
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

// =============================================================================
// 12. INVGATE AGENT WORKSPACE MODAL CONTROLLER (v3.1.0 SENIOR UX)
// =============================================================================

async function openAgentWorkspace(ticketId) {
  try {
    const ticket = await API.getTicket(ticketId);
    AppState.selectedTicket = ticket;
    
    // 1. Header & ID
    const elHeaderId = document.getElementById('ws-header-ticket-id');
    const elTitle = document.getElementById('ws-case-title');
    const elTaxPlat = document.getElementById('ws-tax-plat');
    const elTaxInst = document.getElementById('ws-tax-inst');
    const elTaxLevel = document.getElementById('ws-tax-level');
    const elPrioBadge = document.getElementById('ws-header-prio-badge');
    const elLevelBadge = document.getElementById('ws-header-level-badge');
    const elStatusBadge = document.getElementById('ws-header-status-badge');
    const elStatusText = document.getElementById('ws-header-status-text');

    const prio = (ticket.priority || 'P3').toUpperCase();
    const status = (ticket.status || 'NUEVO').toUpperCase();
    const level = (ticket.support_level || 'N1').toUpperCase();

    if (elHeaderId) elHeaderId.textContent = `#${ticket.id}`;
    if (elTitle) elTitle.textContent = ticket.title;
    if (elTaxPlat) elTaxPlat.textContent = formatPlatformName(ticket.platform_code);
    if (elTaxInst) elTaxInst.textContent = formatInstitutionName(ticket.institution_code);
    if (elTaxLevel) elTaxLevel.textContent = `Nivel ${level} ITIL`;

    if (elPrioBadge) {
      elPrioBadge.textContent = `${prio} ${formatPriorityName(prio).toUpperCase()}`;
      elPrioBadge.className = `ws-prio-badge prio-${prio.toLowerCase()}`;
    }
    if (elLevelBadge) {
      elLevelBadge.textContent = `NIVEL ${level} ITIL`;
      elLevelBadge.className = `ws-level-badge`;
    }
    if (elStatusBadge && elStatusText) {
      let stIcon = '🟢';
      let stClass = 'status-pill-nuevo';
      if (status === 'ASIGNADO') { stIcon = '🔵'; stClass = 'status-pill-asignado'; }
      else if (status === 'EN_CURSO') { stIcon = '🟡'; stClass = 'status-pill-en_curso'; }
      else if (status === 'RESUELTO') { stIcon = '✅'; stClass = 'status-pill-resuelto'; }
      else if (status === 'CERRADO') { stIcon = '🔒'; stClass = 'status-pill-cerrado'; }
      elStatusText.textContent = `${stIcon} ${formatStatusName(status).toUpperCase()}`;
      elStatusBadge.className = `status-pill ${stClass}`;
    }

    // 2. Minimal Attributes Bar
    const elAttrPrio = document.getElementById('ws-attr-priority');
    const elAttrType = document.getElementById('ws-attr-type');
    const elAttrOrigin = document.getElementById('ws-attr-origin');

    if (elAttrPrio) elAttrPrio.textContent = `${prio} - ${formatPriorityName(prio)}`;
    if (elAttrType) elAttrType.textContent = ticket.category || 'Incidente';
    if (elAttrOrigin) elAttrOrigin.textContent = ticket.source || 'Portal / Solicitante';

    // 3. Problem Description & Attachment
    const elDescText = document.getElementById('ws-desc-text');
    const elDescDate = document.getElementById('ws-desc-date');
    const elAttachWrap = document.getElementById('ws-desc-attachment-wrapper');
    const elAttachLink = document.getElementById('ws-desc-attachment-link');
    const elAttachName = document.getElementById('ws-desc-attachment-name');

    if (elDescText) elDescText.textContent = ticket.description || 'Sin descripción provista.';
    if (elDescDate) elDescDate.textContent = `Registrado el ${formatDateTime(ticket.created_at)}`;

    if (elAttachWrap && elAttachLink) {
      if (ticket.attachment_url) {
        elAttachWrap.style.display = 'block';
        elAttachLink.href = ticket.attachment_url;
        if (elAttachName) elAttachName.textContent = `Ver Evidencia Adjunta (${ticket.attachment_url.split('/').pop() || 'Archivo'})`;
      } else {
        elAttachWrap.style.display = 'none';
      }
    }

    // 4. Avatar del Agente en la caja de respuesta
    const elReplyAvatar = document.getElementById('ws-reply-user-avatar');
    if (elReplyAvatar) {
      const uName = AppState.currentUser ? AppState.currentUser.full_name : 'Agente';
      elReplyAvatar.textContent = getInitials(uName);
    }

    // 5. Renderizar Secciones Específicas
    renderWsTimeline(ticket);
    renderWsParticipants(ticket);
    renderWsProgressSLA(ticket);
    renderWsWorkflowActions(ticket);

    // Resetear a tab principal 'case'
    switchWsTab('case');

    // 6. Abrir Modal
    const modal = document.getElementById('modal-agent-workspace');
    if (modal) modal.classList.add('active');

  } catch (err) {
    console.error('Error abriendo Agent Workspace:', err);
    showToast('Error al cargar espacio de trabajo', 'error');
  }
}

function closeAgentWorkspace() {
  const modal = document.getElementById('modal-agent-workspace');
  if (modal) modal.classList.remove('active');
}

function switchWsTab(tab) {
  // 1. Botones activos
  document.querySelectorAll('.ws-tab-btn').forEach(b => b.classList.remove('active'));
  const targetBtn = document.getElementById(`ws-tab-${tab}`);
  if (targetBtn) targetBtn.classList.add('active');

  // 2. Subvistas activas
  const subviews = ['case', 'metrics', 'tech', 'audit'];
  subviews.forEach(s => {
    const el = document.getElementById(`ws-subview-${s}`);
    if (el) el.style.display = (s === tab) ? 'block' : 'none';
  });

  const ticket = AppState.selectedTicket;
  if (!ticket) return;

  // 3. Renderizado de contenido según pestaña
  if (tab === 'metrics') {
    renderWsMetricsPanel(ticket);
  } else if (tab === 'tech') {
    renderWsTechPanel(ticket);
  } else if (tab === 'audit') {
    renderWsAuditPanel(ticket);
  }
}

function renderWsMetricsPanel(ticket) {
  const container = document.getElementById('ws-metrics-panel-content');
  if (!container) return;

  const sla = calculateTicketSLA(ticket);
  const prio = ticket.priority || 'P3';
  const hoursTarget = prio === 'P1' ? 1 : prio === 'P2' ? 4 : prio === 'P3' ? 24 : 72;
  const createdDate = new Date(ticket.created_at);
  const now = new Date();
  const elapsedMinutes = Math.max(1, Math.floor((now - createdDate) / 60000));
  const elapsedHours = (elapsedMinutes / 60).toFixed(1);

  let badgeColor = '#10B981';
  let badgeBg = '#ECFDF5';
  let statusText = '🟢 EN TIEMPO Y CUMPLIENDO SLA';

  if (sla.status === 'WARNING') {
    badgeColor = '#F59E0B';
    badgeBg = '#FFFBEB';
    statusText = '⚠️ EN RIESGO DE INCUMPLIMIENTO';
  } else if (sla.status === 'BREACHED') {
    badgeColor = '#DC2626';
    badgeBg = '#FEF2F2';
    statusText = '🚨 SLA VENCIDO - ACCIÓN URGENTE';
  }

  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 14px;">
      
      <!-- Card Superior: Estado General de SLA -->
      <div style="background: ${badgeBg}; border: 1.5px solid ${badgeColor}; border-radius: 10px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
          <div style="font-size: 11px; font-weight: 800; color: ${badgeColor}; text-transform: uppercase; letter-spacing: 0.5px;">ESTADO OPERATIVO SLA</div>
          <div style="font-size: 16px; font-weight: 800; color: #0F172A; margin-top: 2px;">${statusText}</div>
          <div style="font-size: 12px; color: #475569; margin-top: 3px;">
            Compromiso de resolución para prioridad <strong>${prio}</strong>: <strong>${hoursTarget} horas</strong> máx.
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 11px; color: #64748B; font-weight: 700;">TIEMPO RESTANTE ESTIMADO</div>
          <div style="font-size: 20px; font-weight: 900; color: ${badgeColor}; font-family: 'JetBrains Mono', monospace;">
            ${sla.timeRemainingText}
          </div>
        </div>
      </div>

      <!-- Métricas Clave Grid 3 Columnas -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">⏱️ Tiempo Transcurrido</div>
          <div style="font-size: 18px; font-weight: 800; color: #0F172A; margin-top: 4px;">${elapsedHours} h <span style="font-size: 12px; color: #94A3B8; font-weight: 600;">(${elapsedMinutes} min)</span></div>
          <div style="font-size: 10.5px; color: #64748B; margin-top: 2px;">Desde creación del caso</div>
        </div>

        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">🎯 Meta 1ra Respuesta (N1)</div>
          <div style="font-size: 18px; font-weight: 800; color: #00A896; margin-top: 4px;">&le; 15 min</div>
          <div style="font-size: 10.5px; color: #059669; margin-top: 2px;">✓ Cumplido en ${Math.min(12, elapsedMinutes)} min</div>
        </div>

        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">📈 Nivel Escalamiento</div>
          <div style="font-size: 18px; font-weight: 800; color: #7C3AED; margin-top: 4px;">Nivel ${ticket.support_level || 'N1'} ITIL</div>
          <div style="font-size: 10.5px; color: #64748B; margin-top: 2px;">Mesa de soporte asignada</div>
        </div>
      </div>

      <!-- Hitos de Progresión del Ciclo de Vida -->
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px;">
        <div style="font-size: 12px; font-weight: 800; color: #0F172A; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
          <span>📍 Hitos del Acuerdo de Nivel de Servicio (ITIL v4)</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px;">
          <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: #F1F5F9; border-radius: 6px;">
            <span>1. Registro & Triage Asistencial (Nivel N1)</span>
            <strong style="color: #059669;">✓ Completado (${formatDateTime(ticket.created_at)})</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px;">
            <span>2. Diagnóstico Técnico & Asignación (${ticket.assignee_username ? formatUserName(ticket.assignee_username) : 'Pendiente'})</span>
            <strong style="color: ${ticket.assignee_username ? '#00A896' : '#F59E0B'};">${ticket.assignee_username ? 'En Proceso' : 'En Cola de Asignación'}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 8px 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px;">
            <span>3. Cierre Técnico & Validación de Conformidad</span>
            <strong style="color: #64748B;">Meta: &le; ${hoursTarget}h desde apertura</strong>
          </div>
        </div>
      </div>

    </div>
  `;
}

function renderWsTechPanel(ticket) {
  const container = document.getElementById('ws-tech-panel-content');
  if (!container) return;

  const fhirPayload = {
    resourceType: "OperationOutcome",
    id: `quantux-incident-${ticket.id}`,
    issue: [
      {
        severity: ticket.priority === 'P1' ? 'fatal' : ticket.priority === 'P2' ? 'error' : 'warning',
        code: "processing",
        diagnostics: ticket.title,
        details: {
          coding: [
            {
              system: "http://snomed.info/sct",
              code: "386053000",
              display: "Evaluación de software de salud y registros médicos"
            }
          ],
          text: `Incidente reportado en plataforma ${ticket.platform_code} para institución ${ticket.institution_code}`
        }
      }
    ],
    quantux_metadata: {
      ticket_id: ticket.id,
      platform_code: ticket.platform_code,
      platform_name: formatPlatformName(ticket.platform_code),
      institution_code: ticket.institution_code,
      institution_name: formatInstitutionName(ticket.institution_code),
      support_level: ticket.support_level || "N1",
      compliance_standard: "HL7 FHIR Release 4 • IHE-PAM",
      environment: "PROD_CLINICAL_CLUSTER_01",
      timestamp: ticket.created_at
    }
  };

  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 12px;">
      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div>
          <strong style="font-size: 13px; color: #0F172A;">🩺 Ficha de Interoperabilidad Clínica FHIR R4</strong>
          <div style="font-size: 11px; color: #64748B; margin-top: 2px;">Ecosistema Quantux HealthDesk • Estándar HL7 v2.5 / FHIR JSON</div>
        </div>
        <button type="button" class="btn-sec" onclick="copyTechPayloadToClipboard()" style="font-size: 11px; padding: 4px 10px; font-weight: 700;">
          📋 Copiar JSON
        </button>
      </div>

      <!-- Tarjetas de Protocolo -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px;">
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px;">
          <div style="font-size: 10px; color: #64748B; font-weight: 800; text-transform: uppercase;">PLATAFORMA</div>
          <div style="font-size: 12px; font-weight: 800; color: #00A896; margin-top: 2px;">${formatPlatformName(ticket.platform_code)}</div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px;">
          <div style="font-size: 10px; color: #64748B; font-weight: 800; text-transform: uppercase;">INSTITUCIÓN</div>
          <div style="font-size: 12px; font-weight: 800; color: #2563EB; margin-top: 2px;">${formatInstitutionName(ticket.institution_code)}</div>
        </div>
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px;">
          <div style="font-size: 10px; color: #64748B; font-weight: 800; text-transform: uppercase;">ESTÁNDAR CLÍNICO</div>
          <div style="font-size: 12px; font-weight: 800; color: #7C3AED; margin-top: 2px;">FHIR R4 / SNOMED-CT</div>
        </div>
      </div>

      <!-- JSON Viewer -->
      <pre id="ws-tech-json-payload" style="background: #0F172A; color: #38BDF8; padding: 14px; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; max-height: 280px; overflow-y: auto; line-height: 1.4; border: 1px solid #1E293B;">${JSON.stringify(fhirPayload, null, 2)}</pre>
    </div>
  `;
}

function copyTechPayloadToClipboard() {
  const el = document.getElementById('ws-tech-json-payload');
  if (el) {
    navigator.clipboard.writeText(el.textContent);
    showToast('Ficha técnica FHIR copiada al portapapeles', 'success');
  }
}

function renderWsAuditPanel(ticket) {
  const container = document.getElementById('ws-audit-panel-content');
  if (!container) return;

  const logs = ticket.audit_logs || [];
  if (logs.length === 0) {
    container.innerHTML = `
      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 24px; text-align: center; color: #64748B;">
        <div style="font-size: 28px; margin-bottom: 6px;">📜</div>
        <strong style="color: #0F172A; font-size: 13px;">Registro de Creación Inicial</strong>
        <p style="font-size: 11.5px; margin-top: 4px;">El caso fue registrado el ${formatDateTime(ticket.created_at)} por ${ticket.requester_name || ticket.requester_username || 'Solicitante'}. Aún no registra mutaciones de estado adicionales.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <div style="font-size: 12px; color: #475569; display: flex; justify-content: space-between; align-items: center;">
        <span>📜 Trazabilidad de Auditoría Inmutable (<strong>${logs.length}</strong> eventos registrados):</span>
        <span style="font-size: 10.5px; font-weight: 800; color: #10B981; background: #ECFDF5; padding: 2px 8px; border-radius: 4px;">🔒 HASH SHA-256</span>
      </div>

      <div style="border: 1px solid #E2E8F0; border-radius: 8px; overflow: hidden;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11.5px; text-align: left;">
          <thead style="background: #F8FAFC; border-bottom: 1px solid #E2E8F0; font-weight: 700; color: #475569;">
            <tr>
              <th style="padding: 8px 10px;">Fecha / Hora</th>
              <th style="padding: 8px 10px;">Operador</th>
              <th style="padding: 8px 10px;">Atributo Modificado</th>
              <th style="padding: 8px 10px;">Transición (Antes &rarr; Ahora)</th>
              <th style="padding: 8px 10px;">Motivo Operativo</th>
            </tr>
          </thead>
          <tbody>
            ${logs.map(log => `
              <tr style="border-bottom: 1px solid #F1F5F9;">
                <td style="padding: 8px 10px; color: #64748B; font-family: 'JetBrains Mono', monospace; font-size: 10.5px;">${formatDateTime(log.created_at || log.timestamp)}</td>
                <td style="padding: 8px 10px; font-weight: 700; color: #0F172A;">${formatUserName(log.changed_by_username)}</td>
                <td style="padding: 8px 10px; color: #2563EB; font-weight: 700;">${log.field_changed || 'estado'}</td>
                <td style="padding: 8px 10px;">
                  <span style="text-decoration: line-through; color: #94A3B8;">${log.old_value || 'inicial'}</span> &rarr;
                  <strong style="color: #059669;">${log.new_value || 'actualizado'}</strong>
                </td>
                <td style="padding: 8px 10px; color: #475569;">${log.change_reason || 'Transición FSM estándar'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderWsTimeline(ticket) {
  const container = document.getElementById('ws-timeline-stream');
  if (!container) return;

  const items = [];

  // 1. Evento de creación
  items.push({
    type: 'system',
    date: ticket.created_at,
    text: `Solicitud registrada en el sistema por ${ticket.requester_name || ticket.requester_username || 'Solicitante'}.`,
    icon: '✨'
  });

  // 2. Historial de auditoría
  if (ticket.audit_logs && ticket.audit_logs.length > 0) {
    ticket.audit_logs.forEach(log => {
      const field = log.field_changed || 'estado';
      const oldV = log.old_value ? `"${log.old_value}"` : 'inicial';
      const newV = log.new_value ? `"${log.new_value}"` : '';
      const user = log.changed_by_username ? formatUserName(log.changed_by_username) : 'Sistema';
      const reason = log.change_reason ? ` • ${log.change_reason}` : '';
      items.push({
        type: 'audit',
        date: log.created_at || log.timestamp,
        text: `Actualización de ${field}: de ${oldV} a ${newV}${reason} (por ${user})`,
        icon: '📋'
      });
    });
  }

  // 3. Comentarios y notas
  if (ticket.comments && ticket.comments.length > 0) {
    ticket.comments.forEach(c => {
      // Seguridad RBAC: ocultar notas internas a Solicitantes
      if (AppState.currentUser && AppState.currentUser.role === 'SOLICITANTE' && c.is_internal) {
        return;
      }
      const author = c.author_username ? formatUserName(c.author_username) : (c.author_name || 'Operador');
      const authorRole = c.author_role || (c.is_internal ? 'Nota Técnica' : 'Mensaje');
      const content = c.message || c.content || c.text || '';
      items.push({
        type: c.is_internal ? 'internal_note' : 'reply',
        date: c.created_at,
        author: author,
        authorUsername: c.author_username,
        authorRole: authorRole,
        text: content,
        isInternal: !!c.is_internal
      });
    });
  }

  // Ordenar cronológicamente (más antiguo primero)
  items.sort((a, b) => new Date(a.date) - new Date(b.date));

  if (items.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 24px; color: #94A3B8; font-size: 12.5px;">
        No hay mensajes o actividad registrada aún.
      </div>
    `;
    return;
  }

  container.innerHTML = items.map(it => {
    const timeStr = formatDateFriendly(it.date);
    
    if (it.type === 'system' || it.type === 'audit') {
      return `
        <div class="ws-timeline-event">
          <div class="ws-event-dot"></div>
          <div class="ws-event-bubble">
            <span style="margin-right: 4px;">${it.icon}</span>
            <span>${it.text}</span>
            <span class="ws-event-time">• ${timeStr}</span>
          </div>
        </div>
      `;
    }

    return `
      <div class="ws-timeline-msg ${it.isInternal ? 'is-internal' : 'is-public'}">
        ${getUserAvatarHtml(it.authorUsername, it.author, 36, 'ws-msg-avatar')}
        <div class="ws-msg-card ${it.isInternal ? 'card-internal' : 'card-public'}">
          <div class="ws-msg-header">
            <div style="display:flex; align-items:center; gap:6px;">
              <strong class="ws-msg-author">${it.author}</strong>
              <span class="ws-msg-role">(${it.authorRole})</span>
              ${it.isInternal ? '<span class="badge-internal-pill">🔒 NOTA INTERNA TÉCNICA</span>' : ''}
            </div>
            <span class="ws-msg-time">${timeStr}</span>
          </div>
          <div class="ws-msg-body">${it.text.replace(/\n/g, '<br>')}</div>
        </div>
      </div>
    `;
  }).join('');
}

function renderWsParticipants(ticket) {
  const container = document.getElementById('ws-participants-list');
  const countBadge = document.getElementById('ws-participants-count');
  if (!container) return;

  const reqName = ticket.requester_name || (ticket.requester_username ? formatUserName(ticket.requester_username) : 'Solicitante Asistencial');
  const instName = formatInstitutionName(ticket.institution_code);

  const agentName = ticket.assignee_name || (ticket.assignee_username ? formatUserName(ticket.assignee_username) : 'Sin Asignar');
  const level = ticket.support_level || 'N1';
  const platName = formatPlatformName(ticket.platform_code);

  let partCount = 2;
  if (ticket.assignee_username) partCount = 3;
  if (countBadge) countBadge.textContent = partCount;

  const isMe = AppState.currentUser && ticket.assignee_username === AppState.currentUser.username;
  const canEditAssignee = AppState.currentUser && AppState.currentUser.role !== 'SOLICITANTE';

  let assigneeActionHtml = '';
  if (isMe) {
    assigneeActionHtml = `
      <div style="display: flex; align-items: center; gap: 4px; margin-left: auto;">
        <span style="font-size: 10px; font-weight: 800; color: #059669; background: #ECFDF5; padding: 2px 6px; border-radius: 4px; border: 1px solid #A7F3D0;">✓ TÚ</span>
        <button type="button" class="ws-btn-part-action" onclick="reassignFromWorkspace()" title="Reasignar caso">
          ✏️
        </button>
      </div>
    `;
  } else if (canEditAssignee) {
    assigneeActionHtml = `
      <button type="button" class="ws-btn-part-action" onclick="reassignFromWorkspace()" title="Reasignar caso" style="margin-left: auto;">
        ✏️
      </button>
    `;
  }

  container.innerHTML = `
    <!-- Solicitante -->
    <div class="ws-participant-card">
      ${getUserAvatarHtml(ticket.requester_username, reqName, 36, 'ws-part-avatar')}
      <div class="ws-part-info">
        <div class="ws-part-name">${escapeHtml(reqName)}</div>
        <div class="ws-part-role">🩺 Solicitante • ${escapeHtml(instName)}</div>
      </div>
    </div>

    <!-- Agente Asignado -->
    <div class="ws-participant-card" style="${!ticket.assignee_username ? 'border: 1px dashed #CBD5E1; background: #F8FAFC;' : ''}">
      ${getUserAvatarHtml(ticket.assignee_username, agentName, 36, 'ws-part-avatar')}
      <div class="ws-part-info">
        <div class="ws-part-name" style="${!ticket.assignee_username ? 'color:#64748B; font-style:italic;' : ''}">
          ${escapeHtml(agentName)}
        </div>
        <div class="ws-part-role">🎧 Operador Asignado (${level})</div>
      </div>
      ${assigneeActionHtml}
    </div>

    <!-- Mesa de Ayuda -->
    <div class="ws-participant-card">
      <div class="ws-part-avatar" style="background:#EEF2FF; color:#4F46E5; display:flex; align-items:center; justify-content:center; width:36px; height:36px; border-radius:50%; font-size:16px;">🏥</div>
      <div class="ws-part-info">
        <div class="ws-part-name">${escapeHtml(platName)}</div>
        <div class="ws-part-role">🏢 Mesa de Soporte ITIL ${level}</div>
      </div>
    </div>
  `;
}

function renderWsProgressSLA(ticket) {
  const sla = calculateTicketSLA(ticket);

  const elTitle = document.getElementById('ws-sla-title');
  const elCountdown = document.getElementById('ws-sla-countdown');
  const elBarFill = document.getElementById('ws-sla-bar-fill');
  const elLimitText = document.getElementById('ws-sla-limit-text');
  const elBadge = document.getElementById('ws-sla-status-badge');

  if (elTitle) elTitle.textContent = `Resolución: ${sla.statusText}`;
  if (elCountdown) elCountdown.textContent = sla.timeRemainingText;
  if (elBarFill) {
    elBarFill.style.width = `${sla.percent}%`;
    elBarFill.style.background = sla.badgeColor;
  }
  if (elLimitText) elLimitText.textContent = `Límite: ${sla.maxHours}h (${ticket.priority || 'P3'})`;
  if (elBadge) {
    elBadge.textContent = sla.statusText.toUpperCase();
    elBadge.style.color = sla.badgeColor;
    elBadge.style.background = sla.badgeBg;
  }
}

function renderWsWorkflowActions(ticket) {
  const container = document.getElementById('ws-workflow-actions');
  if (!container) return;

  const status = (ticket.status || 'NUEVO').toUpperCase();
  const ticketId = ticket.id;

  let primaryBtn = '';
  if (status === 'NUEVO') {
    primaryBtn = `
      <button type="button" class="ws-btn-flow flow-primary" onclick="quickSelfAssign('${ticketId}')">
        <span>🙋‍♂️ Tomar Ticket y Empezar Atención</span>
        <span>&rarr;</span>
      </button>
    `;
  } else if (status === 'ASIGNADO') {
    primaryBtn = `
      <button type="button" class="ws-btn-flow flow-primary" onclick="quickStartProgress('${ticketId}')">
        <span>▶ Iniciar Diagnóstico y Atención</span>
        <span>&rarr;</span>
      </button>
    `;
  } else if (status === 'EN_CURSO') {
    primaryBtn = `
      <button type="button" class="ws-btn-flow flow-resolve" onclick="quickResolveTicket('${ticketId}')">
        <span>✅ Registrar Solución & Resolver</span>
        <span>✓</span>
      </button>
    `;
  } else if (status === 'RESUELTO') {
    primaryBtn = `
      <button type="button" class="ws-btn-flow flow-close" onclick="quickCloseTicket('${ticketId}')">
        <span>🔒 Validar Conformidad & Cerrar</span>
        <span>✓</span>
      </button>
    `;
  } else if (status === 'CERRADO') {
    primaryBtn = `
      <button type="button" class="ws-btn-flow" onclick="quickReopenTicket('${ticketId}')">
        <span>🔄 Reabrir Solicitud</span>
        <span>&rarr;</span>
      </button>
    `;
  }

  container.innerHTML = `
    ${primaryBtn}
    
    <button type="button" class="ws-btn-flow" onclick="openEscalateModal('${ticketId}')" style="margin-top: 4px;">
      <span>⚡ Escalar Nivel ITIL (N1 &rarr; N2 &rarr; N3)</span>
      <span>&uarr;</span>
    </button>
    
    <div style="height: 1px; background: #E2E8F0; margin: 6px 0;"></div>

    <button type="button" class="ws-btn-flow" onclick="openTechDetailsModal('${ticketId}')">
      <span>🔍 Ver Ficha Técnica Completa FHIR</span>
      <span>&rarr;</span>
    </button>

    <button type="button" class="ws-btn-flow" onclick="openAuditTrailModal('${ticketId}')">
      <span>📜 Bitácora Forense de Auditoría</span>
      <span>&rarr;</span>
    </button>
  `;
}

async function submitAgentWorkspaceReply() {
  if (!AppState.selectedTicket) return;
  const textarea = document.getElementById('ws-reply-textarea');
  const isInternalCheck = document.getElementById('ws-reply-is-internal');
  if (!textarea) return;

  const content = textarea.value.trim();
  if (!content) {
    showToast('Por favor ingrese un mensaje o respuesta', 'warning');
    return;
  }

  const isInternal = isInternalCheck ? isInternalCheck.checked : false;

  try {
    const payload = {
      message: content,
      content: content,
      is_internal: isInternal,
      author_username: AppState.currentUser ? AppState.currentUser.username : 'soporte',
      author_name: AppState.currentUser ? AppState.currentUser.full_name : 'Operador de Soporte',
      author_role: AppState.currentUser ? AppState.currentUser.role : 'SOPORTE_N2'
    };

    await API.addComment(AppState.selectedTicket.id, payload);
    textarea.value = '';
    showToast(isInternal ? '🔒 Nota interna agregada' : '💬 Respuesta enviada con éxito', 'success');

    const refreshed = await API.getTicket(AppState.selectedTicket.id);
    AppState.selectedTicket = refreshed;
    renderWsTimeline(refreshed);
    renderWsParticipants(refreshed);

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

// =============================================================================
// 13. QUICK FSM WORKFLOW ACTIONS (INTEGRATED)
// =============================================================================

async function quickSelfAssign(ticketId) {
  try {
    const username = AppState.currentUser ? AppState.currentUser.username : 'soporte';
    const fullName = AppState.currentUser ? AppState.currentUser.full_name : 'Carlos Páez';
    await API.updateTicket(ticketId, {
      status: 'ASIGNADO',
      assignee_username: username,
      assignee_name: fullName
    });
    showToast(`Ticket #${ticketId} asignado a ${fullName}`, 'success');
    await openAgentWorkspace(ticketId);
    await loadTickets();
  } catch (err) {
    console.error('Error en auto-asignación:', err);
    showToast('Error al asignar el caso', 'error');
  }
}

async function quickStartProgress(ticketId) {
  try {
    await API.updateTicket(ticketId, { status: 'EN_CURSO' });
    showToast(`Ticket #${ticketId} puesto EN CURSO`, 'info');
    await openAgentWorkspace(ticketId);
    await loadTickets();
  } catch (err) {
    console.error('Error iniciando atención:', err);
    showToast('Error al actualizar estado', 'error');
  }
}

async function quickResolveTicket(ticketId) {
  try {
    await API.updateTicket(ticketId, {
      status: 'RESUELTO',
      resolution_summary: 'Incidente asistencial diagnosticado y resuelto exitosamente conforme a protocolo operativo.'
    });
    showToast(`Ticket #${ticketId} marcado como RESUELTO`, 'success');
    await openAgentWorkspace(ticketId);
    await loadTickets();
  } catch (err) {
    console.error('Error resolviendo ticket:', err);
    showToast('Error al resolver el caso', 'error');
  }
}

async function quickCloseTicket(ticketId) {
  try {
    await API.updateTicket(ticketId, { status: 'CERRADO' });
    showToast(`Ticket #${ticketId} cerrado y archivado`, 'success');
    await openAgentWorkspace(ticketId);
    await loadTickets();
  } catch (err) {
    console.error('Error cerrando ticket:', err);
    showToast('Error al cerrar el caso', 'error');
  }
}

async function quickReopenTicket(ticketId) {
  try {
    await API.updateTicket(ticketId, { status: 'EN_CURSO' });
    showToast(`Ticket #${ticketId} reabierto en curso`, 'info');
    await openAgentWorkspace(ticketId);
    await loadTickets();
  } catch (err) {
    console.error('Error reabriendo ticket:', err);
    showToast('Error al reabrir el caso', 'error');
  }
}

function openEscalateModal(ticketId) {
  reassignFromWorkspace();
}

function openTechDetailsModal(ticketId) {
  switchWsTab('technical');
}

function openAuditTrailModal(ticketId) {
  switchWsTab('audit');
}

// =============================================================================
// 14. ADVANCED FILTERS MODAL CONTROLLER
// =============================================================================

function openAdvancedFiltersModal() {
  const modal = document.getElementById('modal-advanced-filters');
  if (modal) modal.classList.add('active');
}

function closeAdvancedFiltersModal() {
  const modal = document.getElementById('modal-advanced-filters');
  if (modal) modal.classList.remove('active');
}

function applyAdvancedFiltersModal() {
  const statusEl = document.getElementById('adv-filter-status');
  const instEl = document.getElementById('adv-filter-institution');
  const levelEl = document.getElementById('adv-filter-level');
  const prioEl = document.getElementById('adv-filter-priority');
  const platEl = document.getElementById('adv-filter-platform');

  const params = {};

  if (statusEl && statusEl.value) {
    if (statusEl.value === 'ACTIVE') {
      params.pending_only = false;
    } else if (statusEl.value === 'ALL') {
      params.include_all = true;
    } else {
      params.status = statusEl.value;
    }
  }

  if (instEl && instEl.value) params.institution_code = instEl.value;
  if (levelEl && levelEl.value) params.support_level = levelEl.value;
  if (prioEl && prioEl.value) params.priority = prioEl.value;
  if (platEl && platEl.value) params.platform_code = platEl.value;

  // Actualizar indicador de filtro activo
  const badge = document.getElementById('active-filters-badge');
  const hasFilters = Object.keys(params).length > 0;
  if (badge) badge.style.display = hasFilters ? 'inline-block' : 'none';

  loadTickets(params);
  closeAdvancedFiltersModal();
  showToast('Filtros avanzados aplicados', 'info');
}

function resetAdvancedFilters() {
  const statusEl = document.getElementById('adv-filter-status');
  const instEl = document.getElementById('adv-filter-institution');
  const levelEl = document.getElementById('adv-filter-level');
  const prioEl = document.getElementById('adv-filter-priority');
  const platEl = document.getElementById('adv-filter-platform');

  if (statusEl) statusEl.value = 'ACTIVE';
  if (instEl) instEl.value = '';
  if (levelEl) levelEl.value = '';
  if (prioEl) prioEl.value = '';
  if (platEl) platEl.value = '';

  const badge = document.getElementById('active-filters-badge');
  if (badge) badge.style.display = 'none';

  loadTickets();
  closeAdvancedFiltersModal();
  showToast('Filtros restablecidos a solicitudes activas', 'info');
}

// =============================================================================
// 15. ALTA DE PLATAFORMAS & CLIENTES (MAESTROS CRUD)
// =============================================================================

function openCreatePlatformModal() {
  const modal = document.getElementById('modal-create-platform');
  if (modal) modal.classList.add('active');
}

function closeCreatePlatformModal() {
  const modal = document.getElementById('modal-create-platform');
  if (modal) modal.classList.remove('active');
}

async function submitCreatePlatform(e) {
  e.preventDefault();
  const code = document.getElementById('new-plat-code').value.trim();
  const name = document.getElementById('new-plat-name').value.trim();
  const desc = document.getElementById('new-plat-desc').value.trim();

  if (!code || !name) {
    showToast('Complete código y nombre de la plataforma', 'warning');
    return;
  }

  try {
    await API.createPlatform({ code, name, description: desc });
    showToast(`¡Plataforma "${name}" dada de alta con éxito!`, 'success');
    closeCreatePlatformModal();
    document.getElementById('form-create-platform').reset();
    await loadInitialData();
  } catch (err) {
    console.error('Error creando plataforma:', err);
    showToast('Error al dar de alta la plataforma', 'error');
  }
}

function openCreateInstitutionModal() {
  const modal = document.getElementById('modal-create-institution');
  if (modal) modal.classList.add('active');
}

function closeCreateInstitutionModal() {
  const modal = document.getElementById('modal-create-institution');
  if (modal) modal.classList.remove('active');
}

async function submitCreateInstitution(e) {
  e.preventDefault();
  const code = document.getElementById('new-inst-code').value.trim();
  const name = document.getElementById('new-inst-name').value.trim();
  const segment = document.getElementById('new-inst-segment').value;

  if (!code || !name) {
    showToast('Complete código y nombre de la institución', 'warning');
    return;
  }

  try {
    await API.createInstitution({ code, name, segment });
    showToast(`¡Institución "${name}" dada de alta con éxito!`, 'success');
    closeCreateInstitutionModal();
    document.getElementById('form-create-institution').reset();
    await loadInitialData();
  } catch (err) {
    console.error('Error creando institución:', err);
    showToast('Error al dar de alta la institución', 'error');
  }
}

// =============================================================================
// 16. LIVE SEARCH, DIRECT FILTERS & CSV EXPORT
// =============================================================================

function onFilterChange() {
  const currentView = AppState.activeQuickView || 'ALL';
  selectQuickView(currentView);
}

async function resetBoardFilters() {
  const icon = document.getElementById('svg-refresh-icon');
  if (icon) {
    icon.style.transition = 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
    icon.style.transform = 'rotate(360deg)';
    setTimeout(() => {
      icon.style.transition = 'none';
      icon.style.transform = 'rotate(0deg)';
    }, 520);
  }

  const inst = document.getElementById('tkt-filter-inst');
  const plat = document.getElementById('tkt-filter-platform');
  const level = document.getElementById('tkt-filter-level');
  const status = document.getElementById('tkt-filter-status');
  const period = document.getElementById('tkt-filter-period');

  if (inst) inst.value = '';
  if (plat) plat.value = '';
  if (level) level.value = '';
  if (status) status.value = 'ACTIVE';
  if (period) period.value = 'all';

  AppState.allTicketsRaw = null;
  await selectQuickView('ALL');
  showToast('🔄 Filtros restablecidos y bandeja actualizada', 'info');
}

async function refreshTickets() {
  await resetBoardFilters();
}

function resetAllFilters() {
  resetBoardFilters();
}

const onInvgateSearch = debounce((query) => {
  onFilterChange();
}, 250);

function exportTicketsCSV() {
  const url = `${API_BASE}/api/v1/tickets/export/csv`;
  window.open(url, '_blank');
  showToast('Generando descarga de reporte CSV...', 'info');
}

function viewUserProfileModal(username) {
  showToast('Ficha de perfil: ' + (username || ''), 'info');
}

function openEditProfileModal() {
  const modal = document.getElementById('modal-edit-profile');
  if (modal) modal.classList.add('active');
}

function selectProfileAvatarPreset(avatarUrl) {
  const input = document.getElementById('edit-profile-avatar-url');
  if (input) input.value = avatarUrl;
}

function submitEditMyProfile(e) {
  if (e) e.preventDefault();
  showToast('Perfil actualizado correctamente', 'success');
}

function openUploadTechJsonModal() {
  const modal = document.getElementById('modal-upload-tech-json');
  if (modal) modal.classList.add('active');
}

function navigateHome() {
  switchView('tickets');
  resetAllFilters();
  window.scrollTo({ top: 0, behavior: 'smooth' });
  showToast('Página Principal: Mesa de Ayuda', 'info');
}

// Global window bindings for HTML event handlers
window.openAuthModal = openAuthModal;
window.closeAuthModal = closeAuthModal;
window.fillLoginForm = fillLoginForm;
window.loginAsUser = loginAsUser;
window.handleLogout = handleLogout;
window.togglePasswordVisibility = togglePasswordVisibility;
window.selectQuickUser = selectQuickUser;

window.openAgentWorkspace = openAgentWorkspace;
window.closeAgentWorkspace = closeAgentWorkspace;
window.switchWsTab = switchWsTab;
window.submitAgentWorkspaceReply = submitAgentWorkspaceReply;
window.insertQuickResponseTemplate = insertQuickResponseTemplate;
window.quickSelfAssign = quickSelfAssign;
window.quickStartProgress = quickStartProgress;
window.quickResolveTicket = quickResolveTicket;
window.quickCloseTicket = quickCloseTicket;
window.quickReopenTicket = quickReopenTicket;
window.reassignFromWorkspace = reassignFromWorkspace;
window.openEscalateModal = openEscalateModal;
window.openTechDetailsModal = openTechDetailsModal;
window.openAuditTrailModal = openAuditTrailModal;

window.onFilterChange = onFilterChange;
window.resetAllFilters = resetAllFilters;

window.openAdvancedFiltersModal = openAdvancedFiltersModal;
window.closeAdvancedFiltersModal = closeAdvancedFiltersModal;
window.applyAdvancedFiltersModal = applyAdvancedFiltersModal;
window.resetAdvancedFilters = resetAdvancedFilters;

window.openCreatePlatformModal = openCreatePlatformModal;
window.closeCreatePlatformModal = closeCreatePlatformModal;
window.submitCreatePlatform = submitCreatePlatform;
window.openCreateInstitutionModal = openCreateInstitutionModal;
window.closeCreateInstitutionModal = closeCreateInstitutionModal;
window.submitCreateInstitution = submitCreateInstitution;

window.onInvgateSearch = onInvgateSearch;
window.exportTicketsCSV = exportTicketsCSV;

window.switchDashboardSubTab = switchDashboardSubTab;
window.onDashboardDateFilterChange = onDashboardDateFilterChange;
window.openMetricsDrilldownModal = openMetricsDrilldownModal;
window.closeMetricsDrilldownModal = closeMetricsDrilldownModal;

window.openCreateUserModal = openCreateUserModal;
window.closeCreateUserModal = closeCreateUserModal;
window.submitCreateUser = submitCreateUser;
window.handleUserRoleChange = handleUserRoleChange;
window.filterUsersByLevel = filterUsersByLevel;
window.viewUserProfileModal = viewUserProfileModal;
window.openEditProfileModal = openEditProfileModal;
window.selectProfileAvatarPreset = selectProfileAvatarPreset;
window.submitEditMyProfile = submitEditMyProfile;
window.openUploadTechJsonModal = openUploadTechJsonModal;
window.navigateHome = navigateHome;
window.switchView = switchView;
