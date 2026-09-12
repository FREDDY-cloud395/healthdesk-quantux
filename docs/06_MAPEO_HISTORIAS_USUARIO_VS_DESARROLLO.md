# QUANTUX SALUD • HEALTHDESK
## DOC-TR-006: MATRIZ DE TRAZABILIDAD Y MAPEO DE 38 HISTORIAS DE USUARIO
### CORRELACIÓN 1-A-1 ENTRE REQUISITOS, DESARROLLO, PRUEBAS TQM Y ESTADO UAT

---

### METADATOS Y CONTROL DOCUMENTAL
* **Código Documental:** DOC-TR-006
* **Versión Oficial:** v3.2.0-UAT
* **Fecha:** Septiembre 2026
* **Responsable:** Freddy Cortés (Analista Funcional)
* **Estado:** 100% CUMPLIMIENTO VERIFICADO (38 / 38 Historias Homologadas)

---

## 1. TABLA EJECUTIVA DE TRAZABILIDAD Y COBERTURA (UH-01 a UH-38)

| ID UH | Épica | Story Points | Componente Backend | Componente Frontend | Caso de Prueba TQM | Estado UAT |
| :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| **UH-01** | EP-01: Acceso | 3 SP | `endpoints/auth.py` | Modal Login & SessionStore | `test_auth_login` | 🟢 Aprobado |
| **UH-02** | EP-01: Acceso | 2 SP | `endpoints/users.py` | Admin Users Table | `test_list_users` | 🟢 Aprobado |
| **UH-03** | EP-01: Acceso | 2 SP | `models/entities.py` | Audit Toast Notification | `test_auth_audit` | 🟢 Aprobado |
| **UH-04** | EP-01: Acceso | 1 SP | `core/security.py` | Bearer Token Handler | `test_security_headers` | 🟢 Aprobado |
| **UH-05** | EP-02: Tickets | 3 SP | `endpoints/tickets.py` | Formulario Nuevo Ticket | `test_create_ticket_id` | 🟢 Aprobado |
| **UH-06** | EP-02: Tickets | 3 SP | `endpoints/masters.py` | Select Plataformas (9) | `test_platforms_catalog` | 🟢 Aprobado |
| **UH-07** | EP-02: Tickets | 3 SP | `endpoints/masters.py` | Select Clientes (14) | `test_institutions_catalog` | 🟢 Aprobado |
| **UH-08** | EP-02: Tickets | 2 SP | `models/entities.py` | Select Tipo Ticket | `test_ticket_type_enum` | 🟢 Aprobado |
| **UH-09** | EP-02: Tickets | 3 SP | `core/fsm.py` | Badges Reactivos P1-P5 | `test_itil_matrix_calc` | 🟢 Aprobado |
| **UH-10** | EP-02: Tickets | 2 SP | `endpoints/tickets.py` | Campo Adjunto URL | `test_attachment_upload` | 🟢 Aprobado |
| **UH-11** | EP-02: Tickets | 2 SP | `endpoints/tickets.py` | Modal Edición en NUEVO | `test_edit_in_nuevo` | 🟢 Aprobado |
| **UH-12** | EP-03: Cockpit | 3 SP | `endpoints/tickets.py` | Tabla Principal Cockpit | `test_inbox_listing` | 🟢 Aprobado |
| **UH-13** | EP-03: Cockpit | 2 SP | `static/css/styles.css` | Badges Semáforo SLA | `test_sla_badges_render` | 🟢 Aprobado |
| **UH-14** | EP-03: Cockpit | 3 SP | `endpoints/tickets.py` | Botón 'Tomar Ticket' | `test_autoassign_ticket` | 🟢 Aprobado |
| **UH-15** | EP-03: Cockpit | 3 SP | `endpoints/tickets.py` | Modal Escalamiento N1-N3 | `test_escalate_level` | 🟢 Aprobado |
| **UH-16** | EP-03: Cockpit | 2 SP | `endpoints/tickets.py` | Select Reasignación | `test_reassign_operator` | 🟢 Aprobado |
| **UH-17** | EP-04: FSM | 3 SP | `endpoints/tickets.py` | Botón 'Iniciar Atención' | `test_status_en_curso` | 🟢 Aprobado |
| **UH-18** | EP-04: FSM | 3 SP | `endpoints/tickets.py` | Botón 'Pausar / Espera' | `test_status_en_espera` | 🟢 Aprobado |
| **UH-19** | EP-04: FSM | 3 SP | `endpoints/tickets.py` | Textarea Solución ($\ge 8$ car) | `test_resolution_guardrail`| 🟢 Aprobado |
| **UH-20** | EP-04: FSM | 3 SP | `endpoints/tickets.py` | Checkbox Workaround | `test_workaround_flag` | 🟢 Aprobado |
| **UH-21** | EP-04: FSM | 2 SP | `endpoints/tickets.py` | Badge Estado RESUELTO | `test_transition_resuelto` | 🟢 Aprobado |
| **UH-22** | EP-04: FSM | 3 SP | `endpoints/tickets.py` | Botón 'Cerrar Solicitud' | `test_close_and_immutable` | 🟢 Aprobado |
| **UH-23** | EP-05: Colaboración | 3 SP | `endpoints/tickets.py` | Hilo Comentarios Públicos | `test_public_comment` | 🟢 Aprobado |
| **UH-24** | EP-05: Colaboración | 3 SP | `endpoints/tickets.py` | Hilo Notas Internas RBAC | `test_private_note_rbac` | 🟢 Aprobado |
| **UH-25** | EP-05: Colaboración | 2 SP | `endpoints/tickets.py` | Timeline Adjuntos | `test_comment_attachment` | 🟢 Aprobado |
| **UH-26** | EP-06: Admin | 2 SP | `endpoints/tickets.py` | Log Notificaciones Email | `test_email_dispatch_log` | 🟢 Aprobado |
| **UH-27** | EP-05: Colaboración | 2 SP | `endpoints/tickets.py` | Pestaña Auditoría Forense | `test_immutable_audit_log`| 🟢 Aprobado |
| **UH-28** | EP-03: Cockpit | 1 SP | `static/js/app.js` | Ordenamiento JS Columnas | `test_table_sorting_js` | 🟢 Aprobado |
| **UH-29** | EP-06: Admin | 1 SP | `endpoints/tickets.py` | Tarjetas KPIs en Header | `test_dashboard_kpis` | 🟢 Aprobado |
| **UH-30** | EP-06: Admin | 2 SP | `endpoints/tickets.py` | Input Búsqueda en Vivo | `test_free_text_search` | 🟢 Aprobado |
| **UH-31** | EP-06: Admin | 2 SP | `endpoints/users.py` | Modal Nuevo Operador | `test_create_user_admin` | 🟢 Aprobado |
| **UH-32** | EP-06: Admin | 1 SP | `endpoints/masters.py` | Vista Config Global | `test_global_config_get` | 🟢 Aprobado |
| **UH-33** | EP-07: KB | 3 SP | `endpoints/masters.py` | Visor KB y Filtros Tags | `test_kb_list_and_filter` | 🟢 Aprobado |
| **UH-34** | EP-07: KB | 3 SP | `endpoints/masters.py` | Editor Publicación KB | `test_kb_create_article` | 🟢 Aprobado |
| **UH-35** | EP-07: KB | 2 SP | `endpoints/masters.py` | Historial Versiones v1.1 | `test_kb_version_history` | 🟢 Aprobado |
| **UH-36** | EP-07: KB | 2 SP | `endpoints/masters.py` | Botón 'Crear KB de Ticket' | `test_kb_from_ticket_auto`| 🟢 Aprobado |
| **UH-37** | EP-08: Multi-Nivel | 3 SP | `endpoints/masters.py` | Tablero Mesas N1/N2/N3 | `test_helpdesk_teams_get` | 🟢 Aprobado |
| **UH-38** | EP-08: Multi-Nivel | 3 SP | `endpoints/tickets.py` | Botón Exportación CSV | `test_export_csv_utf8` | 🟢 Aprobado |

---

### RESUMEN DE CUMPLIMIENTO
* **Total Historias de Usuario:** 38 UHs
* **Total Story Points:** 91 SP
* **Cumplimiento Funcional:** **100.0% Homologado**
* **Aprobación Oficial:** *Freddy Cortés (Solution Owner) & Comité Evaluador*
