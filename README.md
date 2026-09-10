# HealthDesk Quantux — Quantux Salud (v2.5.0 ITIL Edition)

**Sistema Integral y Centralizado de Mesa de Ayuda y Soporte Hospitalario Multi-Institucional** con matriz de escalamiento ITIL (N1, N2, N3), seguimiento de SLAs médicos y bitácora de trazabilidad inmutable.

---

## 📌 Resumen de la Versión Actual

- **Versión Oficial:** `v2.5.0`
- **Edición:** *ITIL Tiered Support & Multi-Helpdesk Edition (N1 / N2 / N3)*
- **Arquitectura:**
  - **Backend:** FastAPI (Python 3.10+) con SQLite / SQLModel, migraciones automáticas en arranque y validación de esquemas.
  - **Frontend:** Single Page Application (SPA) en Vanilla HTML5, CSS3 Grid/Flexbox y JavaScript nativo sin dependencias pesadas ni compilación.
  - **Documentación & API:** Swagger UI interactivo en `/docs`, Redoc en `/redoc`, y endpoints de estado en `/api`.

---

## 🚀 Cómo Iniciar el Sistema (Sin Errores ni Bloqueos)

### Opción 1: Doble clic en Windows (Recomendada)
Ejecuta el script por lotes:
```cmd
iniciar_healthdesk.bat
```
o en PowerShell:
```powershell
.\iniciar_healthdesk.ps1
```

### Opción 2: Ejecución Directa con Python
Desde la carpeta raíz del proyecto:
```bash
python run_server.py
```

### Opción 3: Uvicorn directo
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --app-dir backend
```

---

## 🌐 URLs y Módulos Principales

| Módulo | URL Local | Descripción |
| :--- | :--- | :--- |
| 🎛️ **Cockpit Central** | `http://127.0.0.1:8000/` o `/cockpit` | Bandeja de tickets, filtros ITIL, ficha técnica y editor. |
| 📊 **Tablero Scrumban** | `http://127.0.0.1:8000/scrumban` | Estado ágil del proyecto y backlog de historias. |
| 📋 **Plan de Gestión** | `http://127.0.0.1:8000/plan` | Gobernanza, matriz RACI, riesgos y SLAs asistenciales. |
| 📑 **Especificación Funcional** | `http://127.0.0.1:8000/especificacion` | Reglas de negocio y matriz de prioridad ITIL P1-P5. |
| 📊 **Presentación Ejecutiva** | `http://127.0.0.1:8000/presentacion` | Deck ejecutivo para directores y comités de salud. |
| 📚 **Swagger API Docs** | `http://127.0.0.1:8000/docs` | Documentación interactiva de todos los endpoints REST. |

---

## 👥 Cuentas y Roles Preconfigurados para Pruebas

| Rol | Usuario (`username`) | Contraseña | Nivel ITIL | Institución |
| :--- | :--- | :--- | :--- | :--- |
| 👑 **Administrador General** | `admin` | `quantux123` | N3 / Todos | OSDE (Central) |
| 🩺 **Soporte Nivel 2 (Especialista)** | `soporte` | `quantux123` | N2 (Plataformas) | OSDE |
| 👨‍⚕️ **Médico / Solicitante** | `solicitante` | `quantux123` | Solicitante | Swiss Medical |

> *Cualquiera de los 33 usuarios del directorio puede ingresar utilizando la contraseña maestra `quantux123`.*

---

## 🛠️ Estructura de Niveles de Atención ITIL

- **Nivel 1 (N1 - Help Desk / Triage):**
  - Recepción de llamadas, categorización inicial, reseteo de claves y resolución con base de conocimiento.
  - SLA objetivo: Primera respuesta < 15 min.
- **Nivel 2 (N2 - Soporte Especializado de Plataformas):**
  - Especialistas por aplicativo (Receta Digital, Telemedicina, HCE, Facturación, LIS, RIS/PACS).
  - SLA resolución: 2 a 8 horas según prioridad.
- **Nivel 3 (N3 - Ingeniería & Proveedores Críticos):**
  - Bugs de código, bases de datos corruptas, servidores caídos y caídas masivas P1 en quirófanos/guardias.
  - SLA crítico P1: Respuesta < 15 min, resolución < 2 horas.

---

## 🔒 Prevención de Errores y Notas Técnicas de Configuración

1. **Migraciones Automáticas (`backend/app/db/session.py`):**
   - El archivo `session.py` ejecuta sentencias seguras `ALTER TABLE ... ADD COLUMN` envueltas en bloques `try/except` para garantizar que la base de datos `healthdesk.db` siempre se sincronice sin perder datos ni arrojar `OperationalError`.
2. **Cero Middleware Bloqueante:**
   - Se eliminó el wrapper `BaseHTTPMiddleware` que provocaba deadlocks en asyncio sobre Windows.
3. **Manejo de Puertos:**
   - Los scripts `iniciar_healthdesk.bat` y `iniciar_healthdesk.ps1` liberan automáticamente el puerto 8000 si existiera algún proceso huérfano.
