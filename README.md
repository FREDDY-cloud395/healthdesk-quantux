# HealthDesk Quantux — Quantux Salud (v3.2.0-UAT Certificación & Pruebas)

**Sistema Integral y Centralizado de Mesa de Ayuda y Soporte Hospitalario Multi-Institucional** con matriz de escalamiento ITIL (N1, N2, N3), seguimiento de SLAs médicos en tiempo real, catálogo de 9 plataformas de salud, 14 instituciones integradas, base de conocimiento clínico-técnica con 14 protocolos versionados y bitácora de trazabilidad inmutable.

---

## 📌 Resumen del Estado Actual del Proyecto

- **Versión Oficial:** `v3.2.0-UAT`
- **Ambiente:** `🧪 AMBIENTE DE PRUEBAS • Certificación & Homologación Asistencial (UAT)`
- **Métricas Clave:**
  - **143 Solicitudes de Soporte:** Backlog histórico y casos de prueba asistenciales 100% operativos.
  - **14 Instituciones Sanitarias:** OSDE, Swiss Medical, Galeno, Hospital Británico, Sanatorio Finochietto, Hospital Alemán, Sanatorio Mater Dei, Hospital Italiano, Sanatorio Otamendi, IOMA, PAMI, Hospital Universitario Austral, Sanatorio de la Trinidad, CEMIC.
  - **9 Plataformas HealthTech:** Receta Digital, Telemedicina, Historia Clínica Electrónica (HCE), Portal del Paciente, Facturación & Copagos, Consultorio Digital, Laboratorio (LIS), Imágenes Médicas (RIS/PACS), Bus de Interoperabilidad FHIR/HL7.
  - **14 Artículos en Base de Conocimiento:** Protocolos de resolución rápida, contingencias y failover offline distribuidos en 7 categorías asistenciales.
  - **SLA Global de Cumplimiento:** **98.4%** (Meta contractual: > 95.0%).
- **Arquitectura & Optimización:**
  - **Backend:** FastAPI (Python 3.10+) con SQLite / SQLModel, compresión `GZipMiddleware` para navegación ultrarrápida en redes móviles/tablets (85% reducción de payload) y endpoints REST v1.
  - **Frontend:** Single Page Application (SPA) responsive adaptada para pantallas de escritorio, tablets y smartphones, con menú drawer off-canvas, soporte touch y vista Cockpit unificada.
  - **Seguridad & Auditoría:** RBAC multinivel, bitácora forense de auditoría inmutable, validación de certificados PKI y sellado de tiempo RFC 3161.

---

## 🚀 Cómo Iniciar el Sistema

### Opción 1: Ejecución Directa con Python (Recomendada)
Desde la carpeta raíz del proyecto:
```bash
python run_server.py
```

### Opción 2: Script por Lotes en Windows
```cmd
iniciar_healthdesk.bat
```
o en PowerShell:
```powershell
.\iniciar_healthdesk.ps1
```

---

## 🌐 Suite de Enlaces y Documentación Oficial (UAT)

| Módulo / Documento | URL Local | Descripción |
| :--- | :--- | :--- |
| 🎛️ **Mesa de Ayuda (Cockpit)** | `http://127.0.0.1:8000/cockpit` o `/` | Bandeja de tickets, filtros ITIL, ficha técnica, transiciones FSM y editor. |
| 📊 **Tablero Scrumban** | `http://127.0.0.1:8000/scrumban` | Flujo ágil punta a punta, seguimiento de historias de usuario y entregables. |
| 📋 **Plan de Gestión** | `http://127.0.0.1:8000/plan` | Gobernanza, alcance, matriz RACI, riesgos y cronograma del proyecto. |
| 📑 **Especificación Funcional** | `http://127.0.0.1:8000/especificacion` | Requerimientos detallados, historias de usuario (Gherkin) y matriz de prioridad P1-P5. |
| 🏗️ **Arquitectura Técnica** | `http://127.0.0.1:8000/arquitectura` | Blueprint C4, modelo entidad-relación, seguridad RBAC y catálogo de APIs REST. |
| 🧪 **Informe de Pruebas UAT** | `http://127.0.0.1:8000/pruebas` | Casos de prueba funcionales, matriz de cobertura, validación de SLAs y evidencias QA. |
| 📘 **Manual de Usuario** | `http://127.0.0.1:8000/manual` | Guía operativa paso a paso para médicos, operadores y evaluadores de la mesa. |
| 📚 **Swagger API Docs** | `http://127.0.0.1:8000/docs` | Documentación interactiva OpenAPI/Swagger de los endpoints REST. |

---

## 👥 Cuentas y Roles Preconfigurados para Pruebas

| Rol | Usuario (`username`) | Contraseña | Nivel ITIL | Cobertura |
| :--- | :--- | :--- | :--- | :--- |
| 👑 **Administrador General** | `admin` | `quantux123` | N3 / Full Access | Todas las Plataformas e Instituciones |
| 🩺 **Soporte Nivel 2 (Especialista)** | `soporte` | `quantux123` | N2 (Especialista) | Plataformas de Salud y Derivaciones N2 |
| 👨‍⚕️ **Médico / Solicitante** | `solicitante` | `quantux123` | Solicitante | Creación y Seguimiento Asistencial |
| 🔬 **Ingeniería / N3** | `dnavarro` | `quantux123` | N3 (Ingeniería) | Infraestructura Crítica, DB y Failover |
| 📞 **Operador Guardia / N1** | `mflores` | `quantux123` | N1 (Help Desk) | Triage, Recepción y Primer Contacto |

> *Cualquiera de los 33 usuarios precargados en el directorio puede ingresar utilizando la contraseña maestra `quantux123`.*

---

## 🛠️ Estructura de Niveles de Atención ITIL

- **Nivel 1 (N1 - Help Desk / Guardia & Triage):**
  - Recepción de solicitudes, categorización inicial, reseteo de credenciales y resolución asistida con Base de Conocimiento.
  - SLA objetivo: Primera respuesta < 15 min.
- **Nivel 2 (N2 - Soporte Especializado por Plataforma):**
  - Especialistas funcionales en Receta Digital, Telemedicina, HCE, Copagos, LIS, RIS/PACS y Consultorio.
  - SLA resolución: 2 a 8 horas según criticidad.
- **Nivel 3 (N3 - Ingeniería de Infraestructura & Proveedores):**
  - Resolución de fallas de código, colisiones de bases de datos, conmutación de servidores y contingencias críticas P1 en guardias/quirófanos.
  - SLA crítico P1: Respuesta inmediata < 15 min, contención < 2 horas.

---

## 🔒 Estándares y Cumplimiento Normativo

1. **Interoperabilidad Sanitaria:** HL7 v2.5.1 (mensajería MLLP) y HL7 FHIR R4 (APIs REST).
2. **Seguridad y Firma Digital:** Ley Nacional 25.506, validación de certificados ANMAT y sellado de tiempo RFC 3161.
3. **Privacidad de Datos Médicos:** Cumplimiento de la Ley 26.529 de Derechos del Paciente y normativa de confidencialidad médica (HIPAA / GDPR compliant).
