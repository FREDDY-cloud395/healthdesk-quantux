# HealthDesk Quantux — Notas de Versión v4.3.0
**Fecha:** 26 de Septiembre de 2026  
**Rama:** `v4.2-dev` (Promovida a `v4.3.0-rc1`)  
**Autoridad y Aprobación Final:** Solution Owner  
**Marco Metodológico:** Scrumban Adaptativo (PMI + IA) con Regla OJO / Pizarra Neutral  

---

## 1. Directiva Rectora de Gobernanza: Alcance Cerrado (Scope Freeze)

> [!IMPORTANT]
> **POLÍTICA MANDATORIA DEL SOLUTION OWNER**:
> *"El alcance del Sprint está estrictamente cerrado. Todo requerimiento, sugerencia, idea o ítem por fuera del alcance definido debe registrarse obligatoriamente en el **Product Backlog**."*
> 
> En cumplimiento estricto de esta directiva:
> - Ningún nuevo desarrollo no planificado ingresará a ejecución activa.
> - Se incorporó un banner permanente de alerta en el encabezado del Tablero Scrumban recordando el principio de **Scope Freeze**.
> - El ítem **`ISSUE-19`** (*Inmutabilidad y Congelamiento de Botones en Tickets Cerrados*) fue registrado con estatus `backlog` en el Product Backlog para su evaluación en futuros Sprints.

---

## 2. Resumen Ejecutivo del Sprint y Estado de Tarjetas

| ID Tarjeta | Tipo | SP | Estado en Tablero | Título / Alcance Técnico |
| :--- | :--- | :---: | :---: | :--- |
| **`MEJ-08`** | MEJORA | 2 | ⚙️ **En Curso (progress)** | **Supresión de Botonera de Acciones Administrativas en Toolbar del Tablero Scrumban** (*"quita esto, pon la tarjeta en curso"*). |
| **`MEJ-04`** | MEJORA | 2 | 🔍 **En Revisión (qa)** | Eliminación de Barra Explicativa Superior Verde en Matriz Multi-Tenant. |
| **`MEJ-05`** | MEJORA | 3 | 🔍 **En Revisión (qa)** | Simetría y Normalización de Cápsulas Activo/Inactivo (82px x 26px, sin `[OK]`). |
| **`MEJ-06`** | MEJORA | 2 | 🔍 **En Revisión (qa)** | Supresión de Botones Redundantes de Categoría en Toolbar de Matriz. |
| **`ISSUE-20`** | ISSUE | 3 | 🔍 **En Revisión (qa)** | Buscador Predictivo con Autocompletado, Opción "Mostrar Todas" y Supresión de Doble Lupa. |
| **`MEJ-07`** | MEJORA | 3 | 🔍 **En Revisión (qa)** | Rediseño Senior UX y Nomenclatura Descriptiva de Sub-pestañas y Botones de Catálogo. |
| **`UH-67`** | UH | 5 | ❌ **En Retrabajo (rework)** | Subniveles Interactivos de Navegabilidad N1 (A la espera de orden de intervención técnica). |
| **`ISSUE-19`** | ISSUE | 3 | 📋 **Product Backlog (backlog)** | Inmutabilidad de Acciones en Tickets Cerrados (Fuera de Alcance — Aislada en Backlog). |

---

## 3. Detalle de Intervenciones Técnicas en Esta Versión

### 3.1. `MEJ-08`: Supresión de Botonera Administrativa en Toolbar del Tablero Scrumban (En Curso)
- **Solicitud del Solution Owner:** *"quita esto, pon la tarjeta en curso"* con captura de la botonera (`media_1790460842977.png`).
- **Implementación:**
  - Se removieron los 4 botones redundantes: `[📥 Exportar CSV]`, `[🖨️ Imprimir / PDF]`, `[🔄 Restaurar Base]`, `[💾 Guardar]` del DOM en [`docs/00_Tablero_Scrumban_Quantux.html`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/docs/00_Tablero_Scrumban_Quantux.html) y [`scripts/build_full_scrumban_board.py`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/scripts/build_full_scrumban_board.py).
  - La persistencia del tablero opera ahora de forma transparente y reactiva ante cada movimiento (drag-and-drop), eliminando la necesidad de acciones manuales que sobrecargaban la barra.
  - La tarjeta `MEJ-08` fue situada expresamente en la columna **`col-progress` (`⚙️ En Desarrollo / En Curso`)**.

### 3.2. `MEJ-04`: Remoción de Barra Verde Explicativa en Matriz Multi-Tenant
- Supresión completa de `#tenant-matrix-guide-body` en [`frontend/index.html`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/frontend/index.html), maximizando el espacio vertical útil para los operadores.

### 3.3. `MEJ-05`: Normalización Geométrica de Cápsulas Activo / Inactivo
- Supresión del texto `[OK]`.
- Dimensiones simétricas fijadas en `width: 82px; height: 26px; border-radius: 13px;` con centrado flexbox perfecto en [`frontend/js/app.js`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/frontend/js/app.js).

### 3.4. `MEJ-06`: Supresión de Botones Redundantes de Categoría
- Eliminación de la botonera estática `Todas (14)`, `Prepagas (6)`, `Sanatorios (4)`, `Hospitales (4)`. El filtrado dinámico queda centralizado en el buscador predictivo unificado.

### 3.5. `ISSUE-20`: Buscador Predictivo Inteligente y Supresión de Doble Lupa
- Placeholder limpio sin emoji duplicado de lupa.
- Menú predictivo reactivo con búsqueda por nombre, código y segmento clínico con badges visuales.
- Atajo directo `🌐 Mostrar todas las instituciones (36)` y botón de limpieza interactiva `✕`.

### 3.6. `MEJ-07`: Rediseño Senior UX en Sub-pestañas y Botones de Catálogo
- Nomenclatura asistencial clara con iconografía y badges numéricos dinámicos:
  - `🏥 Instituciones Sanitarias [14]`
  - `💻 Módulos Clínicos [9]`
  - `🎛️ Habilitación Multi-Tenant [En Vivo]`
  - `🛡️ Niveles de Soporte ITIL [N1 / N2 / N3]`
- Botones de acción semánticos: `🧩 + Nuevo Módulo Clínico` y `🏥 + Nueva Institución Sanitaria` con tooltips operativos.

---

## 4. Trazabilidad de Evidencias Fotográficas

| Tarjeta | Archivo de Captura en Repositorio | Descripción de Evidencia |
| :--- | :--- | :--- |
| `MEJ-08` | `assets/capturas/MEJ-08_botones_toolbar_scrumban_eliminar.png` | Botonera de 4 controles en toolbar de Scrumban señalada por el Solution Owner. |
| `MEJ-07` | `assets/capturas/MEJ-07_subpestanias_administracion_ux_senior.png` | Captura de pestañas escuetas y botones sin semántica clara. |
| `ISSUE-20`| `assets/capturas/ISSUE-20_buscador_multitenant_doble_lupa_predictivo.png` | Doble lupa en input de búsqueda y falta de autocompletado predictivo. |
| `MEJ-06` | `assets/capturas/MEJ-06_botones_categoria_multitenant_eliminar.png` | Botones de filtro por categoría estática a suprimir. |
| `MEJ-05` | `assets/capturas/MEJ-05_capsulas_multitenant_activo_inactivo.png` | Asimetría visual y salto de línea en cápsulas `[OK] ACTIVO` vs `INACTIVO`. |
| `MEJ-04` | `assets/capturas/MEJ-04_barra_explicativa_multitenant.png` | Barra verde superior que ocupaba espacio vertical valioso. |

---

## 5. Certificación de Calidad y Suite de Pruebas

- **Quality Gate OJO / Pizarra Neutral:** 100% Cero violaciones certificadas con `validate_ojo_compliance.py`.
- **Suite de Pruebas Automatizadas:** 25 pruebas unitarias ejecutadas con resultado exitoso (`Ran 25 tests ... OK`).
- **Consistencia de Datos:** Sincronización bidireccional perfecta entre [`docs/00_Tablero_Scrumban_Quantux.html`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/docs/00_Tablero_Scrumban_Quantux.html) y [`docs/Backlog_HealthDesk_Quantux.csv`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/docs/Backlog_HealthDesk_Quantux.csv) (103 ítems totales gobernados).
