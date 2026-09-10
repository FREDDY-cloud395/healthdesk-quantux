# HealthDesk Quantux — Configuración del Sistema y Parámetros Técnicos

Este documento detalla toda la configuración interna del sistema **HealthDesk Quantux v2.5.0**, asegurando que el entorno pueda levantarse, replicarse y migrarse sin inconsistencias.

---

## 1. Parámetros del Entorno de Ejecución

```ini
[RUNTIME]
APP_NAME=HealthDesk Quantux
ORGANIZATION=Quantux Salud
VERSION=2.5.0
EDITION=ITIL Tiered Support (N1/N2/N3)
PYTHON_MIN_VERSION=3.10
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///backend/healthdesk.db
CORS_ORIGINS=*
```

---

## 2. Dependencias del Backend (`backend/requirements.txt`)

```text
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
sqlmodel>=0.0.16
sqlalchemy>=2.0.28
python-multipart>=0.0.9
```

---

## 3. Esquema y Migraciones de Base de Datos SQLite

La función `init_db()` en `backend/app/db/session.py` realiza automáticamente las siguientes comprobaciones de esquema al arrancar:

1. Creación de tablas base:
   - `users`: ID, nombre, usuario, rol, nivel ITIL (`N1`, `N2`, `N3`), institución.
   - `platforms`: 9 plataformas médicas (Receta Digital, Telemedicina, HCE, etc.).
   - `institutions`: 14 prestadores de salud (OSDE, Swiss Medical, Galeno, etc.).
   - `tickets`: ID correlativo (`TICK-YYYYMM-XXXX`), título, plataforma, institución, prioridad ITIL (P1 a P5), estado (FSM), nivel asignado (`support_level`).
   - `comments`: Hilo de comentarios públicos y notas internas de soporte.
   - `audit_logs`: Registro inmutable de transiciones y cambios de estado.
   - `email_logs`: Registro simulado de notificaciones por correo institucional.
   - `kb_articles`: Artículos de base de conocimiento con versionado semántico (`v1.0`, `v2.0`, etc.).
   - `kb_article_history`: Snapshot histórico de revisiones de cada artículo.
   - `helpdesk_level_configs`: Configuración ITIL de N1, N2 y N3 (nombre, descripción, SLA, canales, equipos especializados).

2. Migraciones automáticas no destructivas:
   - `ALTER TABLE users ADD COLUMN support_level TEXT`
   - `ALTER TABLE tickets ADD COLUMN support_level TEXT DEFAULT 'N1'`
   - `ALTER TABLE tickets ADD COLUMN attachment_url TEXT`
   - `ALTER TABLE kb_articles ADD COLUMN version TEXT DEFAULT 'v1.0'`
   - `ALTER TABLE kb_articles ADD COLUMN changelog TEXT DEFAULT 'Versión inicial homologada'`
   - `ALTER TABLE kb_articles ADD COLUMN view_count INTEGER DEFAULT 0`
   - `ALTER TABLE kb_articles ADD COLUMN source_ticket_id TEXT`

---

## 4. Matriz de Prioridad ITIL y SLAs Asistenciales

| Urgencia \ Impacto | CRITICO | ALTO | MEDIO | BAJO | SLA Respuesta | SLA Resolución |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CRITICA** | **P1** | **P1** | **P2** | **P3** | 15 min | 2 horas |
| **ALTA** | **P1** | **P2** | **P3** | **P4** | 30 min | 8 horas |
| **MEDIA** | **P2** | **P3** | **P4** | **P5** | 1 hora | 24 horas |
| **BAJA** | **P3** | **P4** | **P5** | **P5** | 2 horas | 48 horas |

---

## 5. Protocolo de Inicio Limpio (Troubleshooting)

Si en algún momento el servidor no responde o el puerto 8000 queda tomado por un proceso huérfano:

1. Ejecutar en PowerShell:
   ```powershell
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   ```
2. Ejecutar el lanzador verificado:
   ```powershell
   python run_server.py
   ```
   o bien:
   ```cmd
   iniciar_healthdesk.bat
   ```
