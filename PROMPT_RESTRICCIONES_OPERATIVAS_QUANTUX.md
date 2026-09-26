# PROMPT DE RESTRICCIONES OPERATIVAS Y REGLAS DE NEGOCIO (OJO - QUANTUX SERVICEDESK)

> **ESTADO:** DOCUMENTO VINCULANTE E INQUEBRANTABLE  
> **APLICACIÓN:** TODAS LAS RESPUESTAS, MOCKUPS, ARCHIVOS HTML/MD/PDF Y ACCIONES DEL AGENTE  
> **ORIGEN:** INSTRUCCIONES FORMALES DEL CLIENTE (OSDE / COMITÉ DE EVALUACIÓN)  

---

## REGLAS FUNDAMENTALES Y RESTRICCIONES NEGATIVAS ("OJO")

---

### REGLA N° 1: PROHIBICIÓN TAXATIVA DE LENGUAJE O CONCEPTOS CLÍNICOS EN EL PRODUCTO
1. **EL SISTEMA ES UNA TICKETERA DE SOPORTE TI Y MESA DE AYUDA (SERVICEDESK):**
   * El producto NO es un software médico, NO diagnostica pacientes, NO tiene guardias médicas, NO gestiona síntomas de salud ni triage clínico.
   * El servicio se denomina oficialmente: **Centro de Soporte Operativo • Mesa de Ayuda N1 / Quantux ServiceDesk**.
2. **TERMINOLOGÍA VETADA:**
   * Prohibido usar: *"triage clínico"*, *"guardia médica"*, *"médico de guardia"*, *"paciente crítico"*, *"síntomas del paciente"*, *"código rojo"*, etc.
   * Términos permitidos y correctos: *triage operativo/técnico*, *analista de soporte N1/N2*, *soporte técnico*, *incidencia técnica*, *afectación del servicio*, *playbook operativo*.
3. **PRACTICAS DE PSICOLOGÍA:**
   * Son *prestaciones profesionales de salud mental*, *videoconsultas*, *encuadre terapéutico* o *actos profesionales*.
   * Nunca deben tratarse como emergencias médicas ni derivarse a guardias hospitalarias.

---

### REGLA N° 2: PROHIBICIÓN DE COLORES ROJOS, FONDOS OSCUROS Y AZUL MARINO (PIZARRA NEUTRAL)
1. **PALETA LUMINOSA Y SILENCIOSA:**
   * Fondo general: `#FFFFFF` y `#F8FAFC`. Superficies de contenido: `#FFFFFF`. Bordes: `#E2E8F0` y `#CBD5E1`.
   * Tipografía: Escala de grises pizarras (`#0F172A`, `#1E293B`, `#334155`, `#64748B`). Acento único: Teal suave (`#00A896` / `#0D9488`).
2. **CERO COLORES ROJOS:**
   * Prohibido cualquier rojo (`#EF4444`, `#DC2626`, badges rojos, bordes rojos o textos de alerta en rojo). Toda urgencia o criticidad se expresa mediante jerarquía tipográfica, pesos de fuente y etiquetas neutras (`#334155` o `#0F172A`).
3. **CERO FONDOS OSCUROS Y CERO AZUL MARINO:**
   * **PROHIBICIÓN TAXATIVA DE AZUL MARINO Y COLORES OSCUROS:** Prohibidos encabezados, barras laterales (sidebars), barras de navegación, modales, tarjetas o botones con fondos negros, azul marino (`#002B49`, `#1E3A8A`, `#172554`, `#0A192F`), azul noche (`#0F172A`, `#1E293B`) o degradados oscuros. Toda la interfaz debe ser 100% limpia, luminosa, blanca y clara (`#FFFFFF`, `#F8FAFC`, `#F1F5F9`).


---

### REGLA N° 3: COMPONENTES NATIVOS Y ESTRUCTURA EN FILAS
1. **NO USAR TARJETAS (CARDS) NI GRILLAS SOBRECARGADAS:**
   * Los 7 árboles técnico-operativos deben renderizarse mediante filas de lista estructuradas (`.tree-node-row`) de estilo nativo.
2. **BOTONERAS TIPOGRÁFICAS:**
   * Acciones resolutivas con botones de texto limpios (*Ver Solución*, *Crear Ticket N2*, *Copiar Guía*), sin iconos flotantes ni decoraciones innecesarias.

---

### REGLA N° 4: PROHIBICIÓN DE INVENTAR ELEMENTOS O CAMPOS NO SOLICITADOS
1. **NUNCA AGREGAR ELEMENTOS POR INFERENCIA:**
   * No inventar campos, checkboxes, contadores ni botones que el usuario no haya solicitado de forma taxativa.
2. **ELEMENTOS RETIRADOS Y PROHIBIDOS EXPLÍCITAMENTE:**
   * Prohibido el checkbox inventado: `[x] El paciente se encuentra conectado en consulta...`.
   * Prohibido el temporizador regresivo inventado: `11m 45s RESTANTES` o badges regresivos.
   * Prohibida la leyenda de pie de página: `SLA garantizado para Prestadores en Consulta: < 15 min`.
   * Prohibido el badge de cabecera de chat: `RESOLUCIÓN OFICIAL (NODO 2.1)`.
   * Prohibido el bloque redundante: `COMPROMISO SLA ITIL / < 15 min (P1 Crítica)`.

---

### REGLA N° 5: BUSCADOR PREDICTIVO Y FILTRADO DINÁMICO
1. **TYPEAHEAD EN TIEMPO REAL (>= 2 CARACTERES):**
   * El buscador central y la cápsula superior despliegan sugerencias predictivas con los nodos de los 7 árboles y playbooks al escribir 2 o más letras.
2. **FILTRADO VISUAL DINÁMICO:**
   * Al buscar, las filas de los árboles que no coinciden se ocultan dinámicamente, manteniendo sólo las coincidencias.

---

### REGLA N° 6: FORMATO OBLIGATORIO DE CIERRE DE TICKETS (KCS® v6 & ITIL 4)
1. **ESTÁNDARES DE CALIDAD Y BENCHMARK:**
   * Basado en **KCS® (Knowledge-Centered Service) v6**, **ITIL 4 Incident & Knowledge Management** e **ISO/IEC 20000-1**.
2. **ESQUEMA NORMALIZADO DE CIERRE (JSON PARA BASE DE CONOCIMIENTO):**
   * El cierre exige obligatoriamente estructurar: `cierre_ticket_metadata`, `clasificacion_itil`, `diagnostico_causa_raiz` (RCA), `procedimiento_resolutivo_secuencial` y `articulo_kcs_candidato` para auto-alimentar la KB de IA.

---

### REGLA N° 7: PROTOCOLO OBLIGATORIO DE CALIFICACIÓN NEGATIVA Y RESCATE POR LÍDER
1. **JUSTIFICACIÓN MANDATORIA EN CALIFICACIÓN BAJA:**
   * Calificación deficiente (1 o 2 estrellas / Insatisfecho) **exige obligatoriamente** ingresar una nota detallando el motivo.
2. **VISIBILIDAD EN EL TICKET:**
   * La calificación y la nota justificativa deben ser visibles en el ticket.
3. **MANDO UNIFICADO DEL LÍDER DE SOPORTE:**
   * Alerta al Líder de Soporte con **enlace directo al ticket**.
4. **REGISTRO INMUTABLE DEL RESCATE:**
   * El Líder redacta obligatoriamente el comentario describiendo lo que ejecutó en el rescate; este comentario queda registrado de forma inmutable en el ticket.

---

### REGLA N° 8: GESTIÓN DE INCIDENCIAS MAYORES (MIM) Y VINCULACIÓN PADRE-HIJO DISCRETA
1. **CARTEL DISCRETO DE INCIDENCIA MAYOR (PIZARRA NEUTRAL):**
   * Cartel sobrio (blanco, borde gris sutil `#CBD5E1`, texto `#0F172A`, cero rojos) para asociar tickets secundarios al Padre en 1 clic.
2. **VISUALIZACIÓN BIDIRECCIONAL PADRE-HIJO:**
   * **Ticket Padre:** Lista los IDs de tickets asociados vinculados (`#TKT-8902, #TKT-8905`).
   * **Ticket Asociado (Hijo):** Exhibe claramente el ID del Padre (`#TKT-8900`) e indica su condición de ticket asociado.

---

### REGLA N° 9: RESTRICCIÓN ESTRICTA DEL BALANCEADOR DE CARGA
1. **PROHIBIDO TOCAR TICKETS "EN CURSO":**
   * Prohibido redistribuir o modificar tickets en estado **"EN CURSO"**.
2. **ALCANCE EXCLUSIVO SOBRE TICKETS "ASIGNADO":**
   * El balanceador **únicamente tomará tickets en estado "ASIGNADO"**.

---

### REGLA N° 10: MÓDULO COLABORATIVO DE CONFIGURACIÓN DE TICKETS Y SLAS ITIL 4
1. **COLABORACIÓN:** Co-resolución, notas privadas entre analistas, @menciones y bitácora ITIL.
2. **MATRIZ ITIL Y REGLAS DE PAUSA DE RELOJ SLA:** Impacto x Urgencia = Prioridad P1-P4. Pausas de SLA automáticas ante esperas justificadas.

---

### REGLA N° 11: CICLO DE VIDA OFICIAL DEL TICKET (7 ESTADOS FORMALES ITIL 4)
Todo ticket de soporte en Quantux ServiceDesk debe transitar estrictamente por los siguientes 7 estados formales:
1. **NUEVO / REGISTRADO:** Ticket ingresado, pendiente de clasificación/triaje. (Reloj SLA ACTIVO).
2. **ASIGNADO:** Asignado a cola/analista. *Único estado sujeto a balanceo automático*. (Reloj SLA ACTIVO).
3. **EN CURSO:** Analista ha iniciado la atención activa. *Prohibido rebalancear o redistribuir*. (Reloj SLA ACTIVO).
4. **ESPERANDO AL PRESTADOR:** En espera de datos o acción solicitada al prestador. **[RELOJ SLA EN PAUSA]**. Reanuda a *EN CURSO* ante interacción del prestador.
5. **EN ESPERA PASARELA OSDE / SISA:** En espera de validación de servicio externo o pasarela. **[RELOJ SLA EN PAUSA]**. Reanuda automáticamente ante respuesta técnica externa.
6. **RESUELTO:** Solución técnica aplicada (FCR o N2). Se emite el esquema KCS v6 para la KB y se dispara encuesta CSAT. (Reloj SLA DETENIDO).
7. **CERRADO:** Conformidad expresa o cierre definitivo tras auditoría/rescate de calidad. (Reloj SLA FINALIZADO).

---

### REGLA N° 12: AUDITORÍA EXHAUSTIVA DE PEDIDOS Y CERO OMISIONES EN ENTREGABLES

1. **COBERTURA 100% DE REQUERIMIENTOS Y OBSERVACIONES:**
   * Antes de entregar cualquier especificación funcional, documento técnico, código o reporte, el asistente DEBE cotejar minuciosamente el contenido contra **todos y cada uno de los pedidos, correcciones y observaciones** expresados por el usuario a lo largo de toda la interacción.
2. **PROHIBICIÓN TAXATIVA DE PUNTOS FALTANTES:**
   * Ningún requerimiento, detalle funcional, restricción operativa o regla de negocio solicitada puede quedar pendiente, olvidada o fuera del alcance del documento.
3. **MOCKEO Y VALIDACIÓN TQM:**
   * Toda propuesta de solución debe incluir su mockup obligatorio, y antes de la entrega final se deben probar el 100% de los criterios de aceptación y realizar pruebas visuales completas.

---

### REGLA N° 13: OBLIGATORIEDAD SUPREMA DE /goal: REVISIÓN DE OJO MANDATORIA SOBRE TODAS LAS TAREAS

1. **MANDATO SUPREMO E INELUDIBLE SOBRE AGENTES Y SUBAGENTES:**
   * Cada vez que se invoque el comando `/goal`, **es mandatorio y prioritario sobre cualquier otra tarea** que el agente principal y todos los subagentes invoquen, repasen y declaren el cumplimiento del prompt **OJO** antes de iniciar cualquier labor.
   * Ningún agente o subagente puede saltarse esta revisión previa bajo ninguna circunstancia.
2. **ALCANCE UNIVERSAL DE LAS RESTRICCIONES:**
   * Las restricciones de OJO (cero tarjetas/cards, cero rojos, cero azul marino o fondos oscuros, cero terminología clínica, filas continuas `.tree-node-row` de 1px) aplican con carácter obligatorio y vinculante a **TODO el universo de agentes y subagentes** que operen en el proyecto.
3. **VALIDACIÓN EJECUTABLE OBLIGATORIA:**
   * Ninguna tarea de desarrollo en `/goal` se considera finalizada hasta ejecutar y pasar con cero errores los scripts de validación:
     * `python validate_ojo_compliance.py`
     * `python tests/test_dom_visual_compliance.py`

---

### CHECKLIST PRE-EJECUCIÓN INQUEBRANTABLE (18 PUNTOS)
1. ¿El usuario pidió esto de forma explícita? → Si no, **CONSULTAR PRIMERO (OJO)**.
2. ¿La tarea proviene de `/goal`? → Si es así, **REPASO PREVIO OBLIGATORIO DE OJO PARA AGENTE Y SUBAGENTES (MANDATORIO SOBRE TODAS LAS TAREAS)**.
3. ¿Se auditaron y cotejaron exhaustivamente TODOS los pedidos, observaciones y comentarios del usuario para asegurar cobertura del 100% sin dejar ningún punto de lado? → **SÍ (Cero Omisiones)**.
4. ¿Se documentó primero en el archivo funcional (.md) antes de tocar código? → **SÍ (Docs-First estricto)**.
5. ¿La propuesta de solución incluye su mockup obligatorio con datos simulados y estilo Pizarra Neutral? → **SÍ**.
6. Antes de la entrega, ¿se probaron todos los criterios de aceptación (Gherkin) y se ejecutaron pruebas visuales? → **SÍ (TQM Gatekeeper)**.
7. ¿Hay algún término clínico o de guardia en el producto? → **ELIMINARLO**.
8. ¿Hay alguna tarjeta (*card*) o grilla pesada? → **ELIMINARLA**.
9. ¿Hay algún color rojo, fondo oscuro o azul marino en la interfaz? → **CAMBIARLO A NEUTRO/BLANCO**.
10. ¿Se incluyeron los 7 árboles técnico-operativos completos? → **SÍ**.
11. ¿Se incluyeron las 20 Historias de Usuario formales con Gherkin? → **SÍ**.
12. ¿El cierre de ticket incluye el estándar KCS v6 y el esquema JSON para KB? → **SÍ**.
13. ¿La calificación baja (1-2 estrellas) exige justificación obligatoria y reporte de rescate del líder en el ticket? → **SÍ**.
14. ¿La Incidencia Mayor tiene cartel discreto y vinculación Padre-Hijo con IDs cruzados? → **SÍ**.
15. ¿El balanceador de carga tiene estrictamente prohibido tocar tickets EN CURSO y solo toma ASIGNADO? → **SÍ**.
16. ¿El módulo de configuración de tickets incluye matriz ITIL y pausas de reloj SLA? → **SÍ**.
17. ¿Están formalizados en el ciclo de vida los estados "Esperando al Prestador" y "En Espera Pasarela OSDE / SISA" con pausa de reloj SLA? → **SÍ**.
18. ¿Se ejecutaron y pasaron al 100% los validadores automatizados `validate_ojo_compliance.py` y `test_dom_visual_compliance.py`? → **SÍ (Cero Errores)**.

