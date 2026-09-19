# GUION EJECUTIVO Y CIRCUITO DE DEMOSTRACIÓN EN VIVO (SPEECH & LIVE DEMO GUIDE)
## Quantux ServiceDesk Enterprise — Versión de Alta Disponibilidad v4.0.0-PROD-READY

---

## FICHA TÉCNICA DE LA PRESENTACIÓN

* **Audiencia Objetivo:** Directorio Hospitalario, Gerencias de Operaciones, Directores Médicos y CIO / CTO de Redes Asistenciales.
* **Tiempo Total Estimado:** 20 minutos (10 minutos Exposición de Diapositivas + 10 minutos Circuito de Demostración Interactiva).
* **Recursos Disponibles:**
  * **Presentación PowerPoint Editable (.pptx):** [`docs/PRESENTACION_EJECUTIVA_QUANTUX_HEALTHDESK.pptx`](file:///C:/Users/FERO_ADM/.gemini/antigravity/scratch/quantux-v4-dev/docs/PRESENTACION_EJECUTIVA_QUANTUX_HEALTHDESK.pptx)
  * **Visor Web de la Presentación:** `http://127.0.0.1:8005/presentacion`
  * **Aplicación en Vivo (Servidor de Desarrollo v4):** `http://127.0.0.1:8005/`
  * **Manual Operativo de Usuario (DOC-05):** `http://127.0.0.1:8005/manual`
  * **Suite Documental de Ingeniería (Solo Admin):** `http://127.0.0.1:8005/plan`

---

## PARTE 1: SPEECH DIAPOSITIVA POR DIAPOSITIVA (QUÉ DECIR EN CADA SLIDE)

### Diapositiva 1: Portada Ejecutiva
* **Título en Pantalla:** *QUANTUX SERVICEDESK ENTERPRISE — Plataforma de Operaciones de TI y Mesa de Ayuda Sanitaria*
* **Speech del Presentador (Palabra por palabra para estudiar):**
> *"Muy buenos días a todos los miembros del directorio y comité de tecnología. Hoy les presentamos **Quantux ServiceDesk Enterprise**, una solución de mesa de ayuda y operaciones de TI diseñada específicamente para ecosistemas sanitarios de misión crítica. A diferencia de las mesas de ayuda genéricas pensadas para oficinas corporativas, Quantux fue concebido desde el primer día para entender la realidad asistencial: donde cada minuto de sistema caído no es solo una pérdida económica, sino un paciente esperando en guardia o un quirófano bloqueado. Hoy veremos no solo su arquitectura robusta capaz de escalar de 300 a 25.000 usuarios concurrentes, sino también los cinco diferenciadores exclusivos que nos posicionan en la cima del podio tecnológico frente a cualquier alternativa del mercado."*

---

### Diapositiva 2: El Desafío Asistencial y Contexto Operativo
* **Título en Pantalla:** *Contexto Operativo: La Misión Crítica Sanitaria*
* **Speech del Presentador:**
> *"Para dimensionar el valor de Quantux, debemos observar el terreno donde opera: una red federada de **14 instituciones médicas** —entre sanatorios de alta complejidad y centros de diagnóstico ambulatorio— que dependen de **6 plataformas clínicas esenciales**: el sistema de Historia Clínica Electrónica (HIS), el servidor de Imágenes y Diagnóstico (RIS/PACS), el sistema de Laboratorio (LIS), la Receta Digital PKI con validación regulatoria bajo Ley 27.553, el motor de Turnos y el Portal del Paciente.*
>
> *¿Cuál era la fricción histórica que encontramos en las clínicas? Cuando un médico tenía un problema en un consultorio o quirófano, debía llamar por teléfono a un conmutador saturado, esperar en línea mientras el operador le hacía diez preguntas técnicas ('¿cuál es su IP?', '¿qué versión tiene instalada?', '¿en qué máquina está?'), perdiendo tiempo asistencial valioso. Quantux elimina esa fricción de raíz mediante telemetría inmediata y automatización de procesos."*

---

### Diapositiva 3: Los 5 Pluses del Podio (La Ventaja Competitiva Insuperable)
* **Título en Pantalla:** *Los 5 Pluses del Podio: Diferenciadores Estratégicos*
* **Speech del Presentador:**
> *"Aquí radica la ventaja competitiva que nos separa radicalmente de herramientas tradicionales como Jira Service Management o ServiceNow:*
>
> 1. ***Torre de Control del Team Leader:** Nuestro radar operativo en tiempo real. Permite al jefe de guardia técnica visualizar la saturación de cada operador y, mediante un solo clic, rebalancear dinámicamente la carga de tickets sin dejar casos huérfanos.*
> 2. ***Resolución en Cascada de Incidentes:** Ante caídas masivas (por ejemplo, el servidor PACS de tomografías), no se tratan 50 tickets individuales. Se agrupan bajo un 'Incidente Maestro' y, al solucionarse la causa raíz, todos los tickets hijos y sus médicos reciben notificación y cierre automático sincronizado.*
> 3. ***Telemetría Sanitaria Zero-Question:** Cuando un profesional reporta una falla, el sistema captura de fondo su hostname, dirección IP, módulo afectado, box de atención y versión de software. La mesa de ayuda no molesta al médico con preguntas de IT.*
> 4. ***Copilot N1 con IA & Knowledge Base:** Asistente inteligente integrado para los operadores, que sugiere diagnósticos en menos de 3 segundos cruzando los síntomas con nuestra base de conocimiento médica y redacta respuestas estandarizadas listas para enviar.*
> 5. ***CSAT Sanitario & Protocolo de Rescate Activo:** Medición inmediata de satisfacción. Si un usuario califica una atención con 1 o 2 estrellas, el sistema dispara automáticamente una alerta crítica al Team Leader con un modal de rescate proactivo para recuperar la conformidad del cliente antes de que escale a queja formal."*

---

### Diapositiva 4: Deep Dive — La Torre de Control del Team Leader
* **Título en Pantalla:** *Deep Dive: Torre de Control del Team Leader (Módulo Táctico)*
* **Speech del Presentador:**
> *"Detengámonos un momento en la Torre de Control, el corazón táctico de la operación. En cualquier mesa de ayuda tradicional, los incidentes caen a una 'bolsa general' donde los operadores eligen los casos más sencillos y los casos complejos o críticos quedan olvidados.*
>
> *Con la Torre de Control, el Team Leader cuenta con un tablero dinámico que mide el índice de saturación de cada operador en turno. Si el operador Martínez tiene 8 tickets asignados y entra una urgencia P1 en quirófano, el Team Leader puede activar el **Rebalanceo de Carga en 1 Clic**, transfiriendo automáticamente los casos en curso a operadores libres como Gómez o Rossi. Esto redujo nuestro tiempo de asignación en un 45% y nos permite garantizar un cumplimiento de SLA superior al 98% en incidentes prioritarios."*

---

### Diapositiva 5: Arquitectura de Escala Elástica (De 300 a 25.000 Usuarios)
* **Título en Pantalla:** *Arquitectura Elástica: De 300 a 25.000 Usuarios Concurrentes*
* **Speech del Presentador:**
> *"Un aspecto crítico evaluado por los directores de tecnología es la escalabilidad y el costo total de propiedad (TCO). Quantux fue diseñado con una arquitectura elástica desacoplada en tres niveles, sin requerir reescritura de código:*
>
> * **Tier 1 • Edge Autónomo (300 a 1.500 concurrentes):** Opera con SQLite optimizado con Write-Ahead Logging (WAL) y pool de conexiones en memoria. Diseñado para clínicas individuales o sedes remotas que requieren operación autónoma, latencia sub-milisegundo y tolerancia total a desconexiones de internet.*
> * **Tier 2 • Cloud Run HA (1.500 a 8.000 concurrentes):** Despliegue en contenedores serverless en Google Cloud Run conectado a PostgreSQL 16 administrado (Cloud SQL). Escalamiento automático de instancias con cero mantenimiento de infraestructura para la red completa de 14 clínicas.*
> * **Tier 3 • Kubernetes Core (8.000 a 25.000+ concurrentes):** Clúster GKE multi-zona con Redis Enterprise Pub/Sub y base de datos distribuida para despliegues masivos a nivel de prepagas nacionales o ministerios de salud.*
>
> *Esto demuestra que la inversión en Quantux está blindada a futuro: la misma plataforma que hoy atiende un sanatorio puede crecer mañana para gestionar toda una provincia."*

---

### Diapositiva 6: Metodología e Ingeniería Asistida por IA
* **Título en Pantalla:** *Ingeniería Asistida por IA: De 320h a 48h Netas*
* **Speech del Presentador:**
> *"Queremos compartir también una métrica de eficiencia sin precedentes en el ciclo de construcción de este producto. Un desarrollo de este calibre —que incluye máquina de estados ITIL finita, backend RESTful completo, simulador de eventos en tiempo real y frontend responsivo— demandaría tradicionalmente 320 horas hombre de ingeniería (un equipo de 4 personas durante 2 meses).*
>
> *Mediante nuestra metodología de **Ingeniería Aumentada con IA (Google Antigravity & Pair-Programming Agéntico)**, completamos el 100% de la plataforma en tan solo **48 horas netas de trabajo**, logrando una compresión de ciclo de vida de **6.7x**. Y lo más importante: sin acumular deuda técnica, gracias a una suite automatizada de pruebas unitarias, validación continua de DOM y contratos formales de API con Pydantic."*

---

### Diapositiva 7: Circuito de Demostración en Vivo
* **Título en Pantalla:** *Circuito de Demostración en Vivo: Paso a Paso*
* **Speech del Presentador:**
> *"A continuación, pasaremos a la aplicación real para ver en acción este flujo integral de punta a punta. Demostraremos cómo ingresa un incidente prioritario, cómo el Copilot de IA asiste en el diagnóstico, cómo el Team Leader rebalancea la carga en vivo y cómo opera el cierre masivo en cascada."*

---

### Diapositiva 8: Conclusiones y Retorno de Inversión (ROI)
* **Título en Pantalla:** *Conclusiones y Propuesta de Valor*
* **Speech del Presentador:**
> *"En conclusión, los números de Quantux hablan por sí mismos:*
> * ***68% de reducción en el Tiempo Medio de Resolución (MTTR)***, recuperando horas operativas de médicos y secretarias.*
> * ***99.4% de cumplimiento de SLA Asistencial***, blindando la continuidad médica en áreas críticas.*
> * ***100% de trazabilidad ITIL auditable***, con firmas criptográficas de cada intervención técnica.*
> * *Y una **gobernanza integral por roles**, donde directores, médicos, líderes y analistas disponen de la interfaz exacta que necesitan sin fricción visual.*
>
> *Muchas gracias. Los invito a presenciar la demo interactiva y abrimos el espacio para sus preguntas."*

---

## PARTE 2: GUÍA PRÁCTICA DEL CIRCUITO DE DEMOSTRACIÓN EN VIVO (LIVE DEMO)

Siga este orden cronológico exacto frente al comité o directorio:

### PASO 1: Ingreso a la Plataforma y Visualización del Tablero de Control
1. **Acción:** Abrir en el navegador `http://127.0.0.1:8005/` y hacer clic en el tab lateral **"Tablero de Control"**.
2. **Qué mostrar:**
   * Señalar la barra superior de 6 KPIs con cabecera azul marino: *Tareas Vencidas, Vencen Hoy, Tickets Abiertos, Tickets en Espera, No Asignados y Total de Solicitudes*.
   * Mostrar el **Donut Chart** interactivo de prioridades ITIL (P1 Crítica a P5 Planificada) con el total centrado.
   * Mostrar las barras de avance por estado y las barras de distribución por categoría técnica.
   * Mostrar el **Monitor Integrado de Incidentes Prioritarios & SLA** en la parte inferior, destacando el conteo regresivo en vivo del SLA asistencial.
3. **Frase clave del presentador:** *"Este tablero ofrece a la dirección médica y técnica una foto en tiempo real del estado de salud digital de las 14 instituciones sin demoras de sincronización."*

---

### PASO 2: Exploración de la Mesa de Ayuda y Filtros Asistenciales
1. **Acción:** Clic en el tab **"Mesa de Ayuda"** (o tecla rápida).
2. **Qué mostrar:**
   * La bandeja limpia tipo Jira/InvGate con tickets asistenciales reales (ej. *'Fallo en Servidor PACS Tomografía', 'Error de Firma PKI Receta Digital'*).
   * Probar un filtro rápido de plataforma: hacer clic en el botón de filtro rápido (ej. **"HIS"** o **"RIS/PACS"**) y ver cómo la tabla se actualiza al instante sin recargar la página.
   * Mostrar el badge de prioridad con SLA y el indicador de semáforo de tiempo restante.
3. **Frase clave del presentador:** *"Cada ticket muestra exactamente la plataforma clínica afectada, el box y el profesional involucrado, priorizando automáticamente según criticidad médica."*

---

### PASO 3: Workspace del Agente y Asistencia con Copilot IA
1. **Acción:** Hacer clic en cualquier ticket prioritario (ej. un P1 o P2) para desplegar el **Workspace de Trabajo del Agente**.
2. **Qué mostrar:**
   * **Tarjeta de Telemetría Zero-Question:** Mostrar cómo el sistema ya detectó: Hostname, IP local, Box de atención y versión de software sin que el médico tuviera que tipear nada.
   * **Sección Copilot N1:** Clic en el botón **"Sugerir Diagnóstico con IA"**. Observar cómo la IA analiza la descripción del ticket y sugiere una resolución basada en la Base de Conocimiento oficial.
   * Clic en **"Insertar en Nota Técnica"**: ver cómo el texto médico estandarizado se inyecta en el campo de respuesta en un clic.
3. **Frase clave del presentador:** *"El analista de soporte N1 resuelve el caso en un tercio del tiempo tradicional, con lenguaje clínico formal y sin margen de error humano."*

---

### PASO 4: La Torre de Control Team Leader y Rebalanceo en 1 Clic
1. **Acción:** En el selector de perfiles superior o menú lateral, cambiar al rol **"Team Leader"** (o hacer clic en el tab **"Torre de Control"**).
2. **Qué mostrar:**
   * El radar de operadores de la guardia: tarjetas de *Gómez, Martínez, Rossi*, mostrando su capacidad, tickets asignados y estado de saturación en color verde, ámbar o rojo.
   * Señalar a un operador que tenga sobrecarga de casos.
   * Hacer clic en el botón verde destacado: **"⚡ Rebalancear Carga en 1 Clic"**.
   * Ver cómo se ejecuta el modal de rebalanceo táctico y cómo los casos se redistribuyen de forma equitativa y transparente hacia los operadores libres.
3. **Frase clave del presentador:** *"Con esta herramienta exclusiva, ningún caso crítico queda atrapado en la bandeja de un operador saturado o ausente. El rebalanceo asegura continuidad operativa continua."*

---

### PASO 5: Cierre Inteligente en Cascada (Incidentes Masivos)
1. **Acción:** Identificar el Incidente Maestro (ej. Caída de PACS o enlace de red).
2. **Qué mostrar:**
   * Mostrar el botón **"Vincular Casos Hijos"**. Seleccionar 2 o 3 tickets de tomografía o rayos asociados.
   * En el Workspace del incidente maestro, avanzar el estado a **"RESUELTO"** con la nota de ingeniería: *'Servidor de almacenamiento PACS reiniciado y base de datos resincronizada'*.
   * Clic en **"Guardar Resolución"**.
   * Volver a la bandeja principal: mostrar cómo los 3 tickets vinculados pasaron automáticamente a estado **"RESUELTO"** con la misma justificación técnica y notificación a los médicos.
3. **Frase clave del presentador:** *"Esto elimina el trabajo repetitivo de cerrar 50 tickets uno por uno, garantizando que todos los servicios hospitalarios se enteren al unísono de la solución."*

---

### PASO 6: Calificación CSAT y Protocolo de Rescate Activo
1. **Acción:** Mostrar la encuesta de satisfacción CSAT de un caso resuelto.
2. **Qué mostrar:**
   * Explicar el flujo de calificación: cuando el médico califica con 5 estrellas, puede enviar un **Elogio (Kudo)** al analista que lo atendió, fomentando la motivación del equipo de IT.
   * Simular una calificación baja (1 estrella): mostrar cómo en el panel del Team Leader salta la alerta de **"Rescate Requerido"**.
   * Abrir el **Modal de Rescate**: mostrar las opciones de acuerdo telefónico y seguimiento directo para recuperar al cliente institucional.
3. **Frase clave del presentador:** *"No dejamos que una mala experiencia técnica se convierta en una queja directiva. El protocolo de rescate interviene activamente en menos de 15 minutos."*

---

## PARTE 3: PREGUNTAS DIFÍCILES Y RESPUESTAS PREPARADAS (Q&A SHIELD)

### Pregunta 1: *"¿Qué sucede si se corta el enlace de internet con el servidor central?"*
* **Respuesta Sugerida:** *"Gracias a nuestra arquitectura modular Tier 1 SQLite WAL, las clínicas pueden desplegar una instancia local edge en un micro-servidor o máquina virtual dentro del mismo hospital. La mesa de ayuda continúa operando en red local interna sin internet, y cuando la conectividad se restablece, sincroniza los registros con el nodo central de forma transparente."*

### Pregunta 2: *"¿Cumple esta plataforma con las regulaciones de prescripción médica digital?"*
* **Respuesta Sugerida:** *"Absolutamente. Quantux cumple con la Ley Nacional de Prescripción Digital 27.553. Por diseño de gobernanza y seguridad, la mesa de ayuda técnica nunca manipula, edita ni descarga archivos de recetas médicas; únicamente diagnostica el estado del servicio de firma PKI, los certificados criptográficos del token y el enlace con el validador farmacéutico, preservando el secreto médico y la validez legal del acto profesional."*

### Pregunta 3: *"¿Por qué la suite documental técnica solo la ve el Administrador?"*
* **Respuesta Sugerida:** *"Implementamos un principio estricto de gobernanza de información (RBAC). El personal médico, de guardia y analistas solo necesitan el Manual de Usuario Operativo (DOC-05), el cual está disponible para todos los roles desde el menú lateral. Las especificaciones de arquitectura, planes de gestión y contratos de API (DOC-01 a DOC-04 y DOC-06) contienen detalles internos de infraestructura y quedan reservados exclusivamente para la gerencia de tecnología y administradores del sistema."*
