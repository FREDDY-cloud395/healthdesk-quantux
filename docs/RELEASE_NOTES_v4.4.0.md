# 🚀 NOTAS DE VERSIÓN: HEALTHDESK QUANTUX v4.4.0
**Fecha de Publicación:** 27 de Septiembre de 2026  
**Entorno de Producción Cloud:** [https://healthdesk-quantux.onrender.com/](https://healthdesk-quantux.onrender.com/)  
**Entorno de Desarrollo Local:** `http://127.0.0.1:8000/`  
**Responsable Técnico / Solution Owner:** Freddy Cortés (Analista Funcional)  
**Facilitador Técnico:** Diego Martínez  
**Estado:** CERTIFICADO & DESPLEGADO EN PRODUCCIÓN (SPRINT 6 CERRADO / SPRINT 7 INICIADO)  

---

## 1. RESUMEN EJECUTIVO DE LA VERSIÓN v4.4.0

La versión **v4.4.0** de **HealthDesk Quantux** marca la culminación formal y el cierre notarial del **Sprint 6 (Hardening)** con el **100% de sus 93 tareas aprobadas y certificadas en estado `done`**, el resguardo criptográfico bajo el protocolo de **Siete Llaves**, y la activación del **Sprint 7 (35 Story Points, 13 tareas priorizadas)** rumbo a la Demostración Oficial ante el Comité Evaluador el 01 de Octubre de 2026.

Asimismo, consolida el despliegue continuo en la nube de producción sobre **Render Cloud**, garantizando compatibilidad nativa con entornos Linux / Python 3.11 y eliminando cualquier fricción de despliegue.

---

## 2. PRINCIPALES CARACTERÍSTICAS Y MEJORAS

### 2.1. Experiencia de Usuario & Pizarra Neutral Quantux (OJO Compliance)
* **Erradicación de Sombras y Tarjetas Pesadas:** Transición integral hacia un diseño plano y sereno de alta densidad de información, reduciendo la fatiga cognitiva del operador y del personal de salud.
* **Erradicación de Alertas Rojas Agresivas:** Sustitución de colores `#DC2626` y `#EF4444` en estados operativos habituales por la paleta institucional Slate `#334155`, Warm Amber y Teal Quantux `#00A896`.
* **Modal Ergonómico "Mis Solicitudes":**
  * Rediseño en formato tabular con columnas proporcionales fijas.
  * Eliminación de espacios en blanco desproporcionados al centro.
  * Agrupación visual de botones de acción inmediata ("Ver Detalle", "Conformidad").
  * Badge de código de ticket (`#TICK-...`) con enlace interactivo directo a la traza completa.
* **Menú Lateral Zen:** Ocultamiento total y permanente de los accesos a "Tablero de Control" (`#tab-dashboard`) y "Torre de Control" (`#tab-team-leader`) en la barra lateral de navegación para todos los perfiles, manteniendo la operatividad interna por API intacta.

### 2.2. Asistente Clínico Inteligente (Doctor Chat)
* **Sanitización Terminológica Asistencial:** El personal médico y asistencial ya no es expuesto a tecnicismos de infraestructura (N3, servidores, puertos, bases de datos o números de ticket) en las respuestas automáticas.
* **Guía Clínica Determinista:** Respuestas orientadas a la acción asistencial en Consultorio Digital (CD2), guiando al médico paso a paso hacia la pestaña *Documentos* para adjuntar análisis de laboratorio o registrar recetas en diferido.
* **Resolución en Primer Contacto (FCR) Invisible:** Cuando el asistente resuelve la duda clínica, genera de forma silenciosa la constancia técnica oficial para auditoría de backoffice y la exhibe en "Mis Solicitudes".

### 2.3. Infraestructura Cloud en Render & Compatibilidad Python 3.11
* **Resolución de Dependencias de Tipado:** Inclusión de `from __future__ import annotations` e importaciones explícitas desde `typing` en todos los módulos de servicios (`ai_triage.py`, `ai_assistant.py`), solventando la evaluación en tiempo de definición de tipos en Linux / Python 3.11.
* **Depuración de Encoding UTF-8:** Eliminación de firmas Byte Order Mark (`\ufeff`) en archivos fuente para garantizar ejecución silenciosa y limpia.
* **Verificación de Salud Continua:** Endpoint `/health` con validación de persistencia relacional SQLite WAL (`PRAGMA integrity_check = 'ok'`).

---

## 3. PROTOCOLO NOTARIAL DE CIERRE "BAJO SIETE LLAVES" (SPRINT 6)

Para proteger los activos funcionales y asegurar inmutabilidad ante auditorías formales, se ejecutó el protocolo notarial de resguardo:
1. **Llave 1 (Golden Database Snapshot):** `backups/healthdesk_v4.4.0_sprint6_closed_golden.db` (Verificada con `PRAGMA integrity_check = 'ok'`).
2. **Llave 2 (Bóveda Criptográfica ZIP):** `backups/quantux_v4.4.0_sprint6_closed_vault.zip` (80.74 MB).
3. **Llave 3 (Firma Criptográfica SHA-256):** `dcc097d7023b30e2d000f840cabc901db9d89553180bcae3dfab1d6c37b94cbd`.
4. **Llave 4 (Acta Notarial de Cierre):** `backups/ACTA_CIERRE_SIETE_LLAVES_SPRINT_6.txt`.
5. **Llave 5 (Informe Formal de Cierre y Kickoff):** `docs/INFORME_CIERRE_SPRINT_6_Y_KICKOFF_SPRINT_7.md`.
6. **Llave 6 (Tag Inmutable Git):** `v4.3.0-sprint6-cierre`.
7. **Llave 7 (Branch Protegido Sprint 7):** Rama de trabajo aislada `v4.4-sprint7-dev`.

---

## 4. BATERÍA DE PRUEBAS Y QUALITY GATES (100% PASSED)

* **Regla OJO y Pizarra Neutral:** `python validate_ojo_compliance.py` ➔ **100% OK (Exit Code 0)**.
* **Cumplimiento Visual DOM:** `python tests/test_dom_visual_compliance.py` ➔ **6 de 6 pruebas aprobadas (100%)**.
* **Suite Backend ITIL 4:** `backend/tests/test_reemplazo_n1_suite.py` ➔ **5 de 5 pruebas aprobadas (100%)**.
* **Suite Golden CD2 Triage:** `backend/tests/golden_test_cd2_suite.py` ➔ **8 de 8 pruebas aprobadas (100%)**.

---

## 5. PLAN DE EJECUCIÓN SPRINT 7 (KICKOFF LUNES 28-SEP)

El Sprint 7 cuenta con **13 tareas priorizadas (35 Story Points)** en el Sprint Backlog oficial:
* `ISSUE-65` [P1 - 3 SP]: Persistencia de configuración SLA en caliente sin cierre de diálogo (Prioridad 1).
* `ISSUE-55` [P1 - 2 SP]: Enlace interactivo en badge de ticket en constancia FCR.
* `ISSUE-56` [P1 - 3 SP]: Disponibilidad y persistencia de ticket FCR en historial del solicitante.
* `MEJ-13` a `MEJ-15`: Depuración de acciones redundantes, descripción de estado y diferenciación cromática.
* `MEJ-16`: Directiva de Diseño Quantux: Erradicación de tonos rojizos en barras e interfaz.
* `ISSUE-78` a `ISSUE-83`: Contador dinámico de SLA, impacto de negocio, visor lightbox con escape y ocultamiento de configuración ITIL por BBDD.
* `PWA-01` [P1 - 4 SP]: App descargable PWA mobile responsive.

**Hito Rector:** 🛑 **Corte Técnico Definitivo: Lunes 28-Sep a las 18:00 hs**, garantizando 48 horas exclusivas de preparación al Solution Owner para la presentación final del **01 de Octubre de 2026**.
