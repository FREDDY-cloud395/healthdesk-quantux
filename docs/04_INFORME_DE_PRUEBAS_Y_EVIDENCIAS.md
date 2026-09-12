# QUANTUX SALUD • HEALTHDESK
## DOC-QA-004: INFORME DE PRUEBAS FUNCIONALES, VALIDACIÓN Y EVIDENCIAS DE CALIDAD

**Código Documental:** DOC-QA-004  
**Versión:** 1.0 (Línea Base Oficial de Cierre - Sprint 4/5)  
**Fecha:** Agosto 2026  
**Líder Funcional / Solution Owner:** Freddy Cortés (Analista Funcional)  
**Facilitador Técnico:** Diego Martínez  
**Comité Evaluador:** Paula Sbarbati, Diego Martínez, Carolina Brizuela, Nicolás Sánchez  
**Estado:** APROBADO (100% de Pruebas Exitosas)

---

## 1. RESUMEN EJECUTIVO DE ASEGURAMIENTO DE CALIDAD (QA)

El presente informe consolida los resultados y evidencias formales de la ejecución de pruebas funcionales automatizadas End-to-End (E2E), validación de reglas de negocio en el motor de estados finitos (FSM), verificación de seguridad y aislamiento de permisos por perfil (RBAC), e integridad de la auditoría sanitaria para la solución **HealthDesk Quantux**.

### Indicadores Clave de Calidad
* **Casos de Prueba E2E Ejecutados:** 7 de 7 (100% de Cobertura de Flujos Críticos).
* **Tasa de Éxito de Ejecución:** **100% PASSED** (0 Defectos Críticos o Bloqueantes).
* **Historias de Usuario Validadas:** 32 UHs distribuidas en 6 Épicas funcionales.
* **Tiempo Promedio de Respuesta de API:** **4.13 ms** (Umbral máximo tolerado: 50 ms).
* **Integridad de Catálogos Sanitarios:** 100% verificado en 9 plataformas asistenciales y 14 clientes institucionales.

---

## 2. MATRIZ DE COBERTURA Y RESULTADOS DE PRUEBAS FUNCIONALES E2E

| Código | Dimensión de Prueba | Caso de Prueba Funcional | Criterio de Aceptación | Resultado |
| :--- | :--- | :--- | :--- | :---: |
| **QA-E2E-01** | Creación & Priorización | Alta de ticket y cálculo reactivo de prioridad ($P = I \times U$) | Fórmula $P = I \times U$ evaluada en 8 combinaciones; ticket creado en `NUEVO` con código institucional y de plataforma válidos. | 🟢 **PASSED** |
| **QA-E2E-02** | Triage & Asignación | Autoasignación, derivación a Nivel N2/N3 y confidencialidad de notas | Transición a `ASIGNADO` y `EN_CURSO`; notas internas aisladas para soporte y comentarios públicos visibles para el solicitante. | 🟢 **PASSED** |
| **QA-E2E-03** | Reglas de Resolución | Guardrail de resolución técnica obligatoria ($\ge 8$ caracteres) y Workaround | Rechazo HTTP 400 ante soluciones vacías o menores a 8 caracteres; guardado exitoso de soluciones válidas con flag de Workaround y timestamp. | 🟢 **PASSED** |
| **QA-E2E-04** | Cierre & Inmutabilidad | Cierre con feedback de conformidad del solicitante y bloqueo de tickets cerrados | Registro de `closed_at` y comentarios de conformidad; bloqueo estricto (HTTP 400) ante intentos de reapertura o modificación FSM en `CERRADO`. | 🟢 **PASSED** |
| **QA-E2E-05** | Auditoría & Trazabilidad | Caja Negra de Auditoría inmutable y no repudio profesional de la salud | Inserción automática de al menos 5 eventos en `ticket_audit_log` con autor, timestamp ISO, campo modificado y motivo de cambio. | 🟢 **PASSED** |
| **QA-E2E-06** | Catálogos & Integración | Cobertura total de 9 plataformas asistenciales y 14 instituciones | Respuesta HTTP 200 en catálogos y filtrado relacional exacto sin inconsistencias de claves foráneas. | 🟢 **PASSED** |
| **QA-E2E-07** | Rendimiento & Carga | Benchmark de latencia de endpoints REST bajo concurrencia | Latencia media de **4.13 ms** en 30 iteraciones secuenciales de consulta y procesamiento de bandejas. | 🟢 **PASSED** |

---

## 3. EVIDENCIAS TÉCNICAS Y LOGS DE EJECUCIÓN DEL MOTOR FSM

A continuación se detalla la traza real de ejecución obtenida de la suite oficial `backend/test_functional_e2e.py`:

```
================================================================================
  HEALTHDESK QUANTUX • SUITE OFICIAL DE PRUEBAS FUNCIONALES E2E Y QA (SPRINT 4)
================================================================================

>> Ejecutando: QA-E2E-01 (Alta Solicitante & Matriz P=IxU) ...
[OK QA-E2E-01] Ticket Creado: TICK-202608-0020 con Prioridad P1 y Estado NUEVO
   [PASSED] QA-E2E-01 (Alta Solicitante & Matriz P=IxU)

>> Ejecutando: QA-E2E-02 (Triage Soporte N2 & Notas Internas) ...
[OK QA-E2E-02] Triage, Asignación N2 y Notas registradas en TICK-202608-0021
   [PASSED] QA-E2E-02 (Triage Soporte N2 & Notas Internas)

>> Ejecutando: QA-E2E-03 (Guardrail Resolucion >=8 car & Workaround) ...
[OK QA-E2E-03] Guardrail de Resolución validado en TICK-202608-0022 (Rechazo < 8 car y Aceptación con Workaround)
   [PASSED] QA-E2E-03 (Guardrail Resolucion >=8 car & Workaround)

>> Ejecutando: QA-E2E-04 (Cierre Definitivo & Inmutabilidad FSM) ...
[OK QA-E2E-04] Cierre e Inmutabilidad verificada exitosamente en TICK-202608-0023
   [PASSED] QA-E2E-04 (Cierre Definitivo & Inmutabilidad FSM)

>> Ejecutando: QA-E2E-05 (Caja Negra Auditoria Inmutable) ...
[OK QA-E2E-05] Caja Negra de Auditoría: 5 eventos inmutables validados para TICK-202608-0024
   [PASSED] QA-E2E-05 (Caja Negra Auditoria Inmutable)

>> Ejecutando: QA-E2E-06 (Integridad 9 Plataformas & 14 Clientes) ...
[OK QA-E2E-06] Integridad de 9 Plataformas y 14 Instituciones validada al 100%
   [PASSED] QA-E2E-06 (Integridad 9 Plataformas & 14 Clientes)

>> Ejecutando: QA-E2E-07 (Benchmark Rendimiento API <15ms) ...
[OK QA-E2E-07] Rendimiento de API: 4.13 ms promedio por consulta (30 iteraciones)
   [PASSED] QA-E2E-07 (Benchmark Rendimiento API <15ms)

================================================================================
  RESUMEN EJECUTIVO QA: 7/7 PRUEBAS FUNCIONALES PASADAS (100% EXITO)
================================================================================
```

---

## 4. VALIDACIÓN DE REGLAS DE NEGOCIO Y GUARDRAILS SANITARIOS

### 4.1. Guardrail de Solución Técnica Obligatoria ($\ge 8$ Caracteres)
* **Objetivo de Negocio:** Evitar resoluciones vacías o ambiguas (ej: "ok", "listo", "arreglado") que degraden la base de conocimiento y la calidad de atención a profesionales de la salud y sanatorios.
* **Comportamiento Validado:**
  * Si el operador intenta resolver un ticket con un texto como `"Listo"` (5 caracteres), la API rechaza la solicitud retornando `HTTP 400 Bad Request` con el mensaje:  
    `"La solución técnica debe contener al menos 8 caracteres explicativos."`
  * Si el operador proporciona una explicación técnica estructurada (ej: `"Se configuró fallback a codec H.264 compatible con WebKit iOS."`), la API valida la entrada, actualiza el estado a `RESUELTO`, guarda el flag `is_workaround` y estampa el timestamp de resolución.

### 4.2. Inmutabilidad Terminal del Estado CERRADO
* **Objetivo de Negocio:** Asegurar la consistencia de los Acuerdos de Nivel de Servicio (SLA) y prevenir adulteraciones posteriores en incidentes que ya contaron con la conformidad del solicitante.
* **Comportamiento Validado:**
  * Un ticket solo puede pasar a `CERRADO` si se encuentra previamente en estado `RESUELTO`.
  * Cualquier intento de reabrir, reasignar o modificar el estado de un ticket cerrado es interceptado por el motor FSM, bloqueando la acción con `HTTP 400 Bad Request`.

### 4.3. Aislamiento y Confidencialidad de Notas Internas (RBAC)
* **Objetivo de Negocio:** Permitir que los equipos de soporte N1, N2 y N3 registren diagnósticos técnicos de infraestructura sin generar alarma innecesaria en el personal de salud asistencial.
* **Comportamiento Validado:**
  * Comentarios marcados con `is_internal = True` son visibles únicamente para usuarios con roles de `SOPORTE` y `ADMIN`.
  * Los usuarios con perfil `SOLICITANTE` reciben exclusivamente los comentarios públicos (`is_internal = False`).

---

## 5. VALIDACIÓN DEL PANEL DE CONTROL OPERATIVO (INTERFAZ DE USUARIO)

Se llevaron a cabo pruebas de usabilidad e interactividad sobre la consola web en pantalla única (`/cockpit`), verificando los siguientes puntos de control:

1. **Selector Rápido de Roles en 1 Clic (UH-29):** Conmutación instantánea entre perfiles (*Profesional de la Salud Solicitante*, *Operador de Soporte*, *Administrador*) adaptando la botonera operativa y la visibilidad de notas en tiempo real sin recargar la página.
2. **Formulario de Alta con Priorización Reactiva en Vivo (UH-05, UH-09):** Al seleccionar el Impacto y la Urgencia en el modal, la pastilla de prioridad se recalcula en tiempo real en la pantalla antes del envío.
3. **Flujo Operativo de 3 Columnas sin Salto de Pestañas (UH-28):** Triage de tickets a la izquierda, detalle/chat al centro y acciones de resolución a la derecha en una sola pantalla de alta densidad.
4. **Trazabilidad y Feed de Auditoría Visual (UH-27):** Cada transición genera un ítem en la línea de tiempo del ticket mostrando autor, fecha/hora y detalle del cambio.

---

## 6. DICTAMEN FINAL DE ACEPTACIÓN FUNCIONAL

Habiéndose ejecutado satisfactoriamente el 100% de los casos de prueba previstos, sin que se hayan detectado desvíos funcionales ni defectos bloqueantes, se emite el presente **DICTAMEN DE APROBACIÓN Y CONFORMIDAD FUNCIONAL** para el pase a producción del MVP de **HealthDesk Quantux**.

**Firmado en conformidad:**
* **Freddy Cortés** — Solution Owner / Analista Funcional
* **Diego Martínez** — Facilitador Técnico
* **Comité Evaluador:** Paula Sbarbati • Diego Martínez • Carolina Brizuela • Nicolás Sánchez
