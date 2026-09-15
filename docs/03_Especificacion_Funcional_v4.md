# 📑 DOCUMENTO DE ESPECIFICACIÓN FUNCIONAL — PRÓXIMA VERSIÓN (v4.0.0)
**Código:** `DOC-REQ-003` (Nueva Versión Evolutiva — Quantux ServiceDesk Enterprise)  
**Proyecto:** Plataforma Integral de Gestión de Tickets, Servicios e Integraciones  
**Origen de Requerimientos:** Feedback de Gestión (Jess) + Directivas de Ergonomía, Generalización y Reorganización Visual  
**Rol Analista Funcional:** Freddy Cortés  
**Estado:** `BORRADOR TÉCNICO-FUNCIONAL PARA APROBACIÓN`  
**Premisa de Construcción:** Aislamiento total de la versión anterior (v3.2.0-UAT queda 100% congelada).

---

## 🎯 Resumen Ejecutivo del Alcance

Este documento formaliza y desglosa en Historias de Usuario (UH), Criterios de Aceptación (Gherkin) y Reglas de Negocio (RN) los requerimientos de la nueva versión:

1. **Gestión de Incidentes Masivos:** Relación jerárquica de Tickets Padre e Hijos con resolución y cierre en cascada.
2. **Ciclo de Vida de Software y Releases:** Vinculación de tickets a versiones de despliegue (`Release Tags`) con cierre automático al publicar a producción.
3. **Optimización de la Bandeja General:** Grilla simplificada, paginación configurable y filtro directo de tickets sin asignar.
4. **Ergonomía del Área de Trabajo (Workspace Zen):** Rediseño del modal de ticket: cabecera compacta de 48px, notas colapsadas con apertura íntegra (sin truncamientos), Ficha técnica bajo demanda y SLA no invasivo.
5. **Reorganización del Flujo de Alta y Supresión de Ruido Visual:** No se eliminan las 4 dimensiones de clasificación (Organización, Servicio, Criticidad/SLA y Descripción), sino que **se reorganizan armónicamente y se suprime todo el ruido visual** (reemplazo de las 8 macro-tarjetas por selectores compactos y fluidos).
6. **Generalización de Taxonomía y Desacoplamiento Médico (Enterprise Multi-Servicio):** Eliminación definitiva de la palabra *"asistencial"* y ampliación a tickets técnicos, integraciones de APIs, infraestructura y servicios generales.
7. **Simplificación del Tablero de Control (Analytics Zen):** Eliminación de barras horizontales masivas, reducción a 4 métricas de oro y ranking Top 5.
8. **Optimización y Paginación del Directorio de Usuarios (User Management Zen):** Paginación dinámica (10 usuarios/página), eliminación de textos redundantes (*"Servicio Asistencial"*), fusión de Rol con Nivel ITIL, y conversión del botón *"Perfil"* en un **Modal operativo con edición y auditoría**.
9. **Dinámica Ergonómica del Menú Lateral (Sidebar Zen):** Modo mini-barra de 64px para ganar 25% más de espacio de lectura y sub-filtros con contadores en vivo.

---

## 🧘 Principio Rector No Negociable: Ergonomía Visual, Bienestar y Anti-Fatiga Operativa (Jornada Completa)

> **Regla de Oro de Diseño para la v4.0.0:**  
> *"Los analistas de soporte técnico trabajan su jornada completa de 8 horas ininterrumpidas frente a esta interfaz. La pantalla no puede ser un panel de control saturado ni generar fatiga visual. Debe ser un entorno limpio, sereno, profundamente amigable y libre de información innecesaria."*

Para asegurar el bienestar operativo del equipo, cada pantalla implementada debe cumplir estrictamente con los siguientes **4 Mandamientos Ergonómicos Zen**:

1. **🌿 Cero Saturación y Revelación Progresiva (Progressive Disclosure):**  
   * La vista principal muestra **únicamente la información indispensable para accionar el caso actual**.
   * Todo dato técnico denso (payloads JSON/XML, IPs, tokens, bitácoras extensas) debe estar resguardado en acordeones colapsables o paneles laterales bajo demanda, accesible en 1 clic pero invisible por defecto.

2. **👁️ Paleta Anti-Fatiga y Supresión de Alarmismos Cromáticos:**  
   * Se prohíbe el uso de fondos rojos estridentes o parpadeos agresivos que transmitan falso peligro durante la jornada.
   * La navegación y el hover responden con micro-animaciones suaves en tonos descansados (*Soft Ice Blue* `#F0F7FF`, acentos menta y pizarras neutros con certificación de contraste WCAG AAA).

3. **🧹 Fin del "Embrollo a la Vista" (Adiós a las Macro-Tarjetas y Enjambres de Etiquetas):**  
   * Sustitución total de cajas sobredimensionadas con párrafos teóricos por **Segmented Controls compactos de 1 sola línea**.
   * Sustitución de enjambres de 8 o 9 etiquetas apiñadas por barras de cobertura estilizadas y tooltips discretos.

4. **⚡ Espacio de Trabajo Respirable y Productividad sin Tensión:**  
   * Cabeceras compactas (máximo 48px), grillas paginadas ordenadamente (10/25/50 registros) y capacidad de plegar el menú lateral a 64px para disponer del 80% al 90% del ancho del monitor libre para leer y resolver con comodidad mental.

---

## 👥 MATRIZ DE ROLES Y RESPONSABILIDADES OPERATIVAS (RBAC ZEN)

Para garantizar **cero ruido cognitivo** y claridad operativa inmediata a lo largo de una jornada de 8 horas, Quantux ServiceDesk Enterprise v4.0.0 desacopla estrictamente el gobierno de la plataforma de la gestión viva del servicio:

| Dimensión | 👑 Administrador (Admin) | 🎯 Líder de Equipo (Team Leader) | 🎧 Analista de Soporte (N1/N2/N3) | 👤 Solicitante (Usuario Final) |
| :--- | :--- | :--- | :--- | :--- |
| **Misión Principal** | Configuración, seguridad y gobierno global de la plataforma. | Supervisión del turno en vivo, balanceo de carga y rescate de clientes disconformes. | Diagnóstico, resolución técnica y comunicación clara con el solicitante. | Reporte de incidentes o necesidades, seguimiento y aprobación definitiva de cierre. |
| **Foco de su Jornada** | Sistema, catálogo, accesos e integraciones. | Analistas de soporte, colas de trabajo, emergencias P1 y satisfacción (CSAT). | Casos asignados en su cola, resolución técnica y notas de diagnóstico. | Su operación diaria sin trabas tecnológicas; confirmación de servicio resuelto. |
| **Pantalla Clave** | Configuración Global, Usuarios, Catálogos y Releases. | **Torre de Control** (Monitor de Cargas y Mesa de Rescate). | Bandeja General Zen con Filtros Rápidos y Workspace de Caso. | Portal de Autogestión / Mis Solicitudes y Modal CSAT "Buena Onda". |
| **Acciones Exclusivas** | • Alta/Baja de usuarios y roles.<br>• Creación de Clientes y Plataformas.<br>• Despliegue de Releases a Producción.<br>• Exportación de auditoría forense. | • Balanceador de cargas con 1 clic.<br>• Reasignación inmediata de tickets.<br>• Gestión y registro de Rescate CSAT.<br>• Desbloqueo de escalamientos N1-N3. | • Diagnóstico y notas internas (🔒).<br>• Escalamiento justificado N1/N2/N3.<br>• Aplicación de solución técnica.<br>• **Marcar ticket como RESUELTO.** | • Registro rápido en 30 segundos.<br>• Adjuntar evidencias/capturas.<br>• **Cierre definitivo del caso.**<br>• **Calificación CSAT (1 a 5 estrellas + Kudos).** |

> 🧠 **Principio de Ergonomía Cognitiva por Rol:**  
> Ningún usuario debe ver botones, métricas o campos que no pertenecen a su esfera operativa. El analista no debe ver controles de infraestructura del admin; el líder no debe lidiar con código o base de datos; y el solicitante nunca debe verse expuesto a jerga técnica o notas internas.

---

## 🧩 MÓDULO 1: Gestión de Incidentes Masivos (Tickets Padre / Hijos)

### 🔹 UH-33: Vinculación Jerárquica a Ticket Padre (Incidente Masivo)
* **Narrativa:**
  > **Como** Operador de Soporte,  
  > **Quiero** vincular tickets derivados a un Ticket Padre designado como Incidente Masivo,  
  > **Para** centralizar la atención técnica en un único caso y evitar duplicación de tareas.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** un ticket de impacto general (ej. caída de pasarela de pagos o API de integración),
  * **Cuando** el operador activa *"Declarar Incidente Masivo (Ticket Padre)"*,
  * **Entonces** el ticket muestra una insignia `[PADRE / INCIDENTE MASIVO]` y habilita la asociación de tickets hijos subordinados.

### 🔹 UH-34: Resolución y Cierre Automatizado en Cascada
* **Narrativa:**
  > **Como** Operador o Ingeniero N3,  
  > **Quiero** que al resolver el Ticket Padre, todos los tickets hijos se resuelvan y cierren automáticamente,  
  > **Para** notificar a todos los clientes y organizaciones afectadas en una sola acción.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** un Ticket Padre con 20 tickets vinculados,
  * **Cuando** se documenta la solución y se pasa a `Resuelto` o `Cerrado`,
  * **Entonces** todos los tickets asociados pasan al mismo estado, heredan la descripción de la solución y envían el aviso automático a cada solicitante.

### 🔹 UH-35: Desvinculación por Excepción
* **Narrativa:**
  > **Como** Operador de Soporte,  
  > **Quiero** desvincular un ticket de un Ticket Padre si su falla no correspondía al incidente masivo,  
  > **Para** continuar su gestión individual de forma independiente.

---

## 🚀 MÓDULO 2: Tickets de Implementación / Release de Software

### 🔹 UH-36: Catálogo y Asociación de Versiones de Release
* **Narrativa:**
  > **Como** Analista o Líder de Soporte,  
  > **Quiero** asociar tickets a una versión de despliegue planificada (ej. `v3.12.2`),  
  > **Para** enlazar las correcciones y requerimientos con el ciclo de despliegue de desarrollo.

### 🔹 UH-37: Cierre Automático por Despliegue en Producción
* **Narrativa:**
  > **Como** Equipo de Operaciones,  
  > **Quiero** que al marcar una Release como "Desplegada en Producción" se cierren todos sus tickets asociados,  
  > **Para** evitar la actualización manual de casos resueltos por actualización de software.

---

## 🖥️ MÓDULO 3: Bandeja de Entrada General y Paginación

### 🔹 UH-38: Grilla Despejada y Filtro por Defecto de Tickets Cerrados
* **Narrativa:**
  > **Como** Operador de Mesa de Ayuda,  
  > **Quiero** que la grilla oculte por defecto los tickets finalizados (`Cerrado`),  
  > **Para** enfocar la visión exclusivamente en los casos abiertos que requieren acción.

### 🔹 UH-39: Paginación Dinámica (10 / 25 / 50 registros)
* **Narrativa:**
  > **Como** Usuario del sistema,  
  > **Quiero** ver la bandeja paginada en bloques de 10 registros,  
  > **Para** una lectura ordenada y carga ultrarrápida sin desbordar la pantalla.

### 🔹 UH-40: Filtro Prominente "⚡ Sin Asignar"
* **Narrativa:**
  > **Como** Operador N1 / Guardia,  
  > **Quiero** un acceso directo destacado con contador de casos sin responsable (ej. `⚡ Sin Asignar (12)`),  
  > **Para** realizar el triage y tomar tickets de inmediato en un solo clic.

### 🔹 UH-41: Ergonomía de Grilla — Hover Amigable y Libre de Tinte de Alarma (Anti-Estrés)
* **Narrativa:**
  > **Como** Operador de soporte que trabaja toda la jornada frente a la bandeja,  
  > **Quiero** que al pasar el ratón (hover) sobre cualquier ticket la fila responda con un tono amigable, relajante y una micro-animación elegante,  
  > **Para** eliminar la tonalidad rojiza actual que transmite falsa sensación de alarma o peligro.
* **Criterios de Aceptación (Gherkin):**
  * **Escenario 1: Supresión de Tonalidad Rojiza en Hover**
    * **Dado** un ticket de prioridad Crítica (P1),
    * **Cuando** el usuario posa el ratón sobre la fila,
    * **Entonces** la fila **NO** se tiñe de color rojizo ni rosado de advertencia.
  * **Escenario 2: Tonalidad Amigable y Micro-animación Fluida**
    * **Dado** cualquier fila de ticket en la grilla,
    * **Cuando** se produce el hover,
    * **Entonces** el fondo adquiere un tono suave y agradable (*Soft Ice Blue* `#F0F7FF` o cian traslúcido al 4%), con un desplazamiento sutil de `translateY(-1px)` y sombra flotante `box-shadow: 0 4px 14px rgba(10, 28, 62, 0.06)` con transición de `150ms`.

---

## 🧘 MÓDULO 4: Rediseño Ergonómico del Área de Trabajo del Ticket (Workspace Zen)

### 🔹 UH-42: Cabecera Minimalista y Jerarquía Esencial
* **Narrativa:**
  > **Como** Operador trabajando toda la jornada,  
  > **Quiero** una cabecera compacta de 1 sola fila (48px) con ID, título, estado y cliente/solicitante,  
  > **Para** disponer del 80% del espacio para leer y trabajar sin fatiga visual.

### 🔹 UH-43: Metadatos Secundarios y Ficha Técnica en Acordeones Desplegables
* **Narrativa:**
  > **Como** Operador,  
  > **Quiero** que los datos técnicos (Payloads JSON/XML, IPs, tokens, logs de integración) estén colapsados en un acordeón bajo demanda.

### 🔹 UH-44: Indicador de SLA Ergonómico y Anti-Estrés
* **Narrativa:**
  > **Como** Operador,  
  > **Quiero** un badge sutil `⏱️ SLA: 2h` en lugar de barras rojas estridentes de alerta,  
  > **Para** operar con tranquilidad y profesionalismo.

### 🔹 UH-45: Separación de Vista de Conversación vs. Auditoría
* **Narrativa:**
  > **Como** Operador,  
  > **Quiero** un toggle para ver solo mensajes humanos o la bitácora técnica completa.

### 🔹 UH-46: Barra de Acciones Contextuales Flotante
* **Narrativa:**
  > **Como** Operador,  
  > **Quiero** una barra inferior limpia con el botón principal de avance directo (`Tomar`, `Resolver`, `Cerrar`).

### 🔹 UH-47: Hilo de Respuestas y Notas Colapsables con Expansión Completa
* **Narrativa:**
  > **Como** Operador de Soporte,  
  > **Quiero** que todas las notas y respuestas anteriores aparezcan colapsadas por defecto, y que al hacer clic en cualquiera se despliegue su **contenido 100% completo (sin resúmenes ni textos cortados)**,  
  > **Para** mantener una pantalla despejada pero acceder al texto íntegro en 1 clic, con botones de *"Expandir/Colapsar Todo"*.

---

## ⚡ MÓDULO 5: Reorganización del Flujo de Alta y Supresión de Ruido Visual (Streamlined Creation)

### 5.1. Diagnóstico de la Interfaz Actual de Alta
La pantalla actual de alta no falla en su estructura clasificatoria, sino en su presentación visual y ergonomía:
1. **Sobrecarga de macro-tarjetas:** En la evaluación de afectación y SLA se despliegan **8 bloques gigantes** con íconos sobredimensionados y párrafos explicativos extensos que saturan innecesariamente.
2. **Navegación pesada:** La separación rígida entre pasos interrumpe la fluidez operativa y genera fatiga al usuario.
3. **Objetivo de la v4.0.0:** **No se eliminan las etapas de clasificación** (Organización, Servicio, Criticidad/SLA y Descripción son indispensables para la trazabilidad operativa), sino que **se reorganizan armónicamente y se suprime todo el ruido visual**, logrando una experiencia ágil, fluida y limpia.

### 5.2. Historias de Usuario para el Alta Reorganizada (v4.0.0)

#### 🔹 UH-48: Reorganización Estructurada del Flujo de Alta y Supresión de Ruido Visual
* **Narrativa:**
  > **Como** Usuario u Operador de Soporte,  
  > **Quiero** completar las 4 dimensiones de la solicitud (Organización, Servicio, Criticidad/SLA y Descripción) en un flujo reorganizado, compacto y visualmente despejado,  
  > **Para** registrar incidencias con precisión técnica en pocos segundos sin experimentar sobrecarga cognitiva ni fatiga visual.
* **Criterios de Aceptación (Gherkin):**
  * **Escenario 1: Conservación y Reorganización de las 4 Dimensiones**
    * **Dado** el proceso de alta de una nueva solicitud,
    * **Cuando** se despliega el formulario reorganizado,
    * **Entonces** se preservan estructuradamente las 4 etapas de catalogación:
      1. *Organización Cliente y Tipo de Solicitud*.
      2. *Categoría / Plataforma / Servicio*.
      3. *Criticidad, Impacto y SLA*.
      4. *Título, Descripción y Adjuntos*.
  * **Escenario 2: Depuración Radical de Ruido Visual**
    * **Dado** el paso de selección de criticidad y urgencia,
    * **Cuando** el usuario ingresa a esa sección,
    * **Entonces** ya no se muestran las 8 macro-tarjetas con párrafos teóricos densos, sino controles segmentados y botones compactos de 1 línea con código de color sutil.
  * **Escenario 3: Continuidad y Agilidad Operativa**
    * **Dado** el llenado del formulario,
    * **Cuando** el usuario avanza entre las secciones reorganizadas,
    * **Entonces** la transición es instantánea, con indicadores de avance minimalistas y sin fricción de recargas pesadas.

#### 🔹 UH-49: Segmented Controls Compactos de Prioridad (Fin de las Macro-Tarjetas)
* **Narrativa:**
  > **Como** Usuario,  
  > **Quiero** seleccionar la prioridad con una botonera horizontal limpia (`[🟢 Baja] [🟡 Media] [🟠 Alta] [🔴 Crítica]`),  
  > **Para** no tener que leer 8 bloques con párrafos teóricos.

#### 🔹 UH-50: Preselección Inteligente de Contexto (Smart Defaults)
* **Narrativa:**
  > **Como** Usuario autenticado,  
  > **Quiero** que mi organización/cliente y mis datos vengan precargados automáticamente.

#### 🔹 UH-51: Opciones Técnicas Avanzadas en Acordeón Colapsable
* **Narrativa:**
  > **Como** Operador Técnico,  
  > **Quiero** campos avanzados ocultos bajo el botón `[+ Opciones Técnicas]`.

---

## 🌐 MÓDULO 6: Desacoplamiento de Exclusividad Médica y Taxonomía Enterprise Universal

### 🔹 UH-52: Limpieza Terminológica y Supresión del Vocablo "Asistencial"
* **Narrativa:**
  > **Como** Administrador del Sistema,  
  > **Quiero** que ningún texto de la interfaz mencione la palabra "asistencial" de forma restrictiva.

### 🔹 UH-53: Catálogo Universal de Tipologías y Servicios Técnicos
* **Narrativa:**
  > **Como** Operador o Solicitante,  
  > **Quiero** categorizar tickets en áreas técnicas y de servicios (Integraciones, Infraestructura, Software, Accesos).

---

## 📊 MÓDULO 7: Tablero de Control Zen (Analytics Limpio)

### 🔹 UH-54: Reducción a las 4 Métricas de Oro (North Star KPIs)
* **Narrativa:**
  > **Como** Gerente o Líder de Operaciones,  
  > **Quiero** que la cabecera del tablero presente únicamente los 4 indicadores esenciales del servicio:
  > 1. 🔥 **Críticos Activos**
  > 2. ⏳ **En Gestión**
  > 3. 🎯 **% Cumplimiento SLA**
  > 4. ⏱️ **Tiempo Medio de Resolución (MTTR)**.

### 🔹 UH-55: Reemplazo de Barras Masivas por Ranking Focalizado "Top 5"
* **Narrativa:**
  > **Como** Supervisor de Servicio,  
  > **Quiero** visualizar únicamente el **Top 5 de Clientes con Mayor Demanda** y el **Top 5 de Servicios con Mayor Incidencia** en lugar de gráficos infinitos de 14 barras.

### 🔹 UH-56: Gráficos de Estado Limpios (Dona Unificada con Filtro Rápido)
* **Narrativa:**
  > **Como** Analista de Operaciones,  
  > **Quiero** un único gráfico circular interactivo que muestre el ciclo de vida y prefiltre la bandeja al hacer clic.

### 🔹 UH-57: Lenguaje Neutral y Universal en Gráficos y Reportes
* **Narrativa:**
  > **Como** Usuario corporativo,  
  > **Quiero** que todas las leyendas y métricas empleen terminología neutral, eliminando vocabulario clínico.

---

## 👥 MÓDULO 8: Optimización y Gestión Eficiente del Directorio de Usuarios (User Management Zen)

### 🔹 UH-58: Paginación Dinámica y Buscador Rápido de Usuarios
* **Narrativa:**
  > **Como** Administrador o Supervisor de Mesa,  
  > **Quiero** navegar el directorio paginado en bloques de 10 usuarios y contar con un buscador predictivo,  
  > **Para** encontrar a cualquier miembro del equipo en segundos sin hacer scroll infinito.

### 🔹 UH-59: Limpieza de Redundancias y Fusión de Rol / Nivel
* **Narrativa:**
  > **Como** Usuario del sistema,  
  > **Quiero** una tabla limpia que suprima textos inútiles (*"Servicio Asistencial"*, sedes duplicadas) y fusione columnas duplicadas (`[🔴 Admin N3]`, `[🔵 Soporte N1]`),  
  > **Para** escanear la lista de usuarios con máxima claridad visual.

### 🔹 UH-60: Modal / Drawer Operativo de Perfil de Usuario (Botón 100% Funcional)
* **Narrativa:**
  > **Como** Administrador,  
  > **Quiero** que al hacer clic en el botón `[ 👤 Perfil ]` se abra un **Modal / Drawer lateral interactivo**,  
  > **Para** ver la información detallada, historial de tickets gestionados y ejecutar acciones reales: `[ ✏️ Editar Datos ]`, `[ 🔑 Restablecer Contraseña ]` y `[ ⛔ Desactivar Cuenta ]`.

### 🔹 UH-61: Neutralización Terminológica del Directorio
* **Narrativa:**
  > **Como** Usuario corporativo,  
  > **Quiero** que el directorio se denomine *"Directorio de Usuarios & Equipo de Soporte"*.

---

## ✉️ MÓDULO 9: Ingesta Automática de Tickets por Correo Electrónico (Email-to-Ticket Omnichannel)

### 9.1. Diagnóstico y Necesidad Operativa
Los usuarios corporativos y clientes frecuentemente reportan problemas enviando un simple correo electrónico (a `soporte@...` o `mesadeayuda@...`) en lugar de ingresar a la web. El sistema debe procesar automáticamente estos correos y convertirlos en tickets formales sin intervención manual.

### 9.2. Historias de Usuario para Ingesta por Email (v4.0.0)

#### 🔹 UH-62: Procesamiento de Correos Entrantes y Alta Automática de Tickets
* **Narrativa:**
  > **Como** Usuario o Cliente,  
  > **Quiero** enviar un correo a la casilla de soporte describiendo mi problema o solicitud,  
  > **Para** que el sistema cree automáticamente un ticket formal sin obligarme a completar formularios web.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** que un usuario envía un correo a la dirección de soporte (ej. `soporte@empresa.com`),
  * **Cuando** el parser de correo entrante (IMAP / Webhook SendGrid/Mailgun) recibe el mensaje,
  * **Entonces**:
    1. **Asunto** se convierte en el **Título del Ticket**.
    2. **Remitente** se mapea al usuario registrado en la base de datos (o crea un contacto externo si es nuevo).
    3. **Cuerpo del Correo** (HTML/Texto) se convierte en la **Descripción inicial del caso**.
    4. **Archivos Adjuntos** (capturas de pantalla, PDFs, logs) se descargan y se enlazan automáticamente como anexos del ticket.
    5. El ticket se crea con estado `Nuevo (Vía Email)` y canal `Email`.

#### 🔹 UH-63: Hilo Bidireccional de Conversación por Correo (Email Threading)
* **Narrativa:**
  > **Como** Solicitante,  
  > **Quiero** responder desde mi cliente de correo (Outlook, Gmail) al mail de notificación de mi ticket,  
  > **Para** agregar comentarios o aclaraciones directamente en el historial sin entrar al portal web.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** un correo entrante cuyo asunto contiene el token de seguimiento (ej. `Re: [#TKT-1042] Error en webhook`),
  * **Cuando** el motor procesa el mensaje,
  * **Entonces** detecta el ID `#TKT-1042`, **no crea un ticket duplicado**, y agrega el contenido como una nueva nota de respuesta en el hilo de conversación del ticket existente.

#### 🔹 UH-64: Notificación Automática de Confirmación (Auto-Reply con Ticket ID)
* **Narrativa:**
  > **Como** Solicitante,  
  > **Quiero** recibir una confirmación inmediata por email tras enviar mi reporte,  
  > **Para** tener certeza de que el caso fue recibido y conocer el número de seguimiento asignado.

---

## 🌟 MÓDULO 10: Ciclo de Resolución por Soporte vs. Cierre Exclusivo por Solicitante & CSAT Gamificado "Buena Onda"

### 10.1. Regla de Negocio ITIL: Separación entre "Resuelto" y "Cerrado"
* **Resolución técnica (Operadores N1/N2/N3):** El equipo técnico tiene potestad para diagnosticar, aplicar el fix y cambiar el estado del ticket a **`Resuelto`**, documentando la solución aplicada.
* **Cierre y Conformidad (SOLO el Solicitante):** **Únicamente el usuario que abrió el ticket** tiene el privilegio de dar por **`Cerrado`** el caso y calificar el servicio recibido. Si la solución no satisface al solicitante, puede reabrir el caso con un solo clic.

### 10.2. Historias de Usuario para Cierre y Calificación Empática (v4.0.0)

#### 🔹 UH-65: Permiso Exclusivo del Solicitante para Cierre y Certificación de Solución
* **Narrativa:**
  > **Como** Solicitante de un ticket,  
  > **Quiero** ser el único facultado para validar que la solución funciona y cerrar formalmente el ticket,  
  > **Para** asegurar que ningún caso se dé por cerrado sin mi consentimiento y verificación efectiva.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** un ticket en estado `Resuelto`,
  * **Cuando** un operador intenta cerrarlo directamente,
  * **Entonces** el sistema le informa que el cierre definitivo requiere la validación del solicitante.
  * **Dado** que el ticket está `Resuelto`,
  * **Cuando** el solicitante ingresa al portal (o pulsa el enlace en el correo de resolución),
  * **Entonces** se le presenta la pantalla interactiva de **Validación de Solución & Calificación**.
  * **Regla de Inactividad:** Si transcurren 5 días hábiles en estado `Resuelto` sin interacción del solicitante, se ejecuta un cierre automático preventivo por tiempo cumplido.

#### 🔹 UH-66: Grilla de Calificación "Buena Onda" (CSAT Gamificado y Emojis Reactivos)
* **Narrativa:**
  > **Como** Solicitante cerrando mi ticket,  
  > **Quiero** encontrarme con una interfaz moderna, divertida, muy copada y empática para calificar la atención,  
  > **Para** reconocer el buen trabajo del equipo de forma rápida, positiva y sin aburrirme con encuestas burocráticas.
* **Criterios de Aceptación (Gherkin):**
  * **Diseño y Micro-interacciones:**
    * Grilla con 5 **Emojis Reactivos Animados** de gran tamaño y código de color:
      * 🤩 **¡Una Maravilla! (5/5)**
      * 😃 **¡Excelente Atención! (4/5)**
      * 🙂 **Bien, Todo Resuelto (3/5)**
      * 😐 **Podría Ser Mejor (2/5)**
      * 🙁 **No Quedé Conforme (1/5)**
  * **Elogios Rápidos ("Kudos"):**
    * Píldoras de 1 clic para destacar lo mejor de la atención:
      * `⚡ Respuesta Ultrarrápida`
      * `🧠 Explicación Súper Clara`
      * `🤝 Mucha Amabilidad y Paciencia`
      * `🎯 Solucionado al Toque`
  * **Experiencia Positiva:** Mensaje de agradecimiento instantáneo con confeti sutil al calificar alto: *"¡Gracias por la buena onda! Le pasamos tus felicitaciones al operador."*

#### 🔹 UH-67: Protocolo Colaborativo de Queja y Recuperación de Experiencia (Service Recovery)
* **Narrativa:**
  > **Como** Solicitante insatisfecho o con una queja sobre la solución recibida,  
  > **Quiero** un canal constructivo, colaborativo y sin fricciones para explicar qué faltó,  
  > **Para** que el equipo me ayude a dejarlo perfecto sin hacerme perder tiempo ni sentir frustración.
* **Criterios de Aceptación (Gherkin):**
  * **Escenario 1: Detección de Desconformidad y Modo Colaborativo**
    * **Dado** que el usuario selecciona una calificación baja (1 o 2) o presiona *"No quedó resuelto"*,
    * **Cuando** se despliega la sección de observaciones,
    * **Entonces** la interfaz cambia a un tono empático y colaborativo:  
      *"Queremos que tu experiencia sea de 10 puntos. Estamos de tu lado: contanos qué detalle faltó para que lo corrijamos juntos de inmediato."*
  * **Escenario 2: Opciones Asistidas de Corrección Rápida**
    * Se ofrecen motivos asistidos para no tener que escribir tanto:
      * `[ ] La solución técnica no funcionó o volvió a fallar`
      * `[ ] Quedó una consulta importante sin responder`
      * `[ ] El tiempo de atención demoró más de lo debido`
      * `[ ] Necesito asistencia prioritaria de un supervisor`
  * **Escenario 3: Reapertura con Alerta de Rescate (Service Recovery)**
    * Al enviar el comentario, el ticket pasa a estado `Reabierto (Feedback Negativo)` con prioridad máxima.
    * Se dispara una alerta urgente en el panel del Líder de Mesa de Ayuda para contacto proactivo y resolución prioritaria.

---

## 🖥️ Wireframe de la Pantalla de Calificación "Buena Onda" y Cierre (v4.0.0)

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ 🎉 ¡Tu solicitud #TKT-1042 fue Resuelta!                             [ Cerrar ]│
├────────────────────────────────────────────────────────────────────────────────┤
│ Atendido por: 👤 Sofía Valdez (Nivel 1 - Soporte)                              │
│ Solución aplicada: "Se restableció el webhook de integración y se sincronizó el token."│
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│   ¿Cómo calificarías la atención recibida?                                     │
│                                                                                │
│      🤩              😃             🙂             😐             🙁          │
│  ¡Una Maravilla!  ¡Excelente!    ¡Todo Bien!    ¡Puede Mejorar!  ¡Disconforme! │
│     ( 5 )           ( 4 )          ( 3 )          ( 2 )          ( 1 )         │
│                                                                                │
│ ────────────────────────────────────────────────────────────────────────────── │
│ ✨ Dejale un elogio al operador (Kudos):                                        │
│  [ ⚡ Respuesta Ultrarrápida ]   [ 🧠 Explicación Súper Clara ]                 │
│  [ 🤝 Mucha Buena Onda ]        [ 🎯 Solucionado al Toque ]                    │
│                                                                                │
│ 💬 Comentario opcional:                                                        │
│  [ "¡Genial la atención de Sofía, súper rápida y atenta!"                    ] │
│                                                                                │
│             [ 🔄 No funcionó / Tengo una duda ]   [ 🚀 Confirmar y Cerrar ]   │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏢 MÓDULO 11: Descongestión Visual y Rediseño Intuitivo de Organizaciones & Plataformas (Catálogo Multi-Tenant Zen)

### 11.1. Diagnóstico del Ruido Visual Actual
La pantalla actual de *"Plataformas & Instituciones"* presenta una severa sobrecarga cognitiva:
1. **Enjambre de micro-etiquetas:** Cada tarjeta renderiza hasta 8 o 9 píldoras de texto apiñadas (`Receta Electrónica`, `Telemedicina`, `Consultorio Digital`, `Interoperabilidad...`), generando un *"embrollo a la vista"* que dificulta la lectura y satura la pantalla.
2. **Pestañas y botones desalineados:** Existen pestañas superiores gruesas (`Red de Instituciones Sanitarias 14`, `Módulos & Sistemas 9`, `Matriz Multi-Tenant`) y debajo botones flotantes amontonados (`+ Alta Sistema`, `+ Alta Institución`).
3. **Terminología excluyente médica:** Mantiene etiquetas como *"Sanitarias"*, *"Prepagas"*, *"Sanatorios"*, en lugar de la taxonomía universal y multi-propósito requerida para empresas, integraciones y servicios.

### 11.2. Historias de Usuario para el Catálogo Zen (v4.0.0)

#### 🔹 UH-68: Rediseño de Tarjetas Zen (Supresión del Enjambre de Píldoras por Indicador de Cobertura)
* **Narrativa:**
  > **Como** Operador o Administrador de Cuentas,  
  > **Quiero** ver tarjetas de organizaciones limpias, elegantes y sin enjambres de etiquetas amontonadas,  
  > **Para** evaluar el estado de cada cliente de un solo vistazo sin fatiga visual.
* **Criterios de Aceptación (Gherkin):**
  * **Escenario 1: Supresión de Etiquetas Masivas Frontales**
    * **Dado** que una organización tiene habilitados 8 sistemas de software,
    * **Cuando** se visualiza la tarjeta en el catálogo,
    * **Entonces** **NO** se listan las 8 etiquetas completas ocupando media tarjeta.
  * **Escenario 2: Indicador Limpio de Cobertura con Tooltip**
    * En su lugar, se presenta:
      * Una **Barra de Cobertura Visual**: `7 / 11 Servicios Activos (64%)` con barra de progreso estilizada.
      * Máximo **2 micro-chips destacados** de servicios principales + una píldora discreta interactiva: `[ +5 más... ]`.
      * Al pasar el ratón sobre `[ +5 más... ]`, un tooltip interactivo limpio despliega la lista completa sin invadir la grilla.

#### 🔹 UH-69: Ficha 360° en Drawer Lateral Interactivo (Toda la Información sin Embrollo)
* **Narrativa:**
  > **Como** Administrador o Soporte,  
  > **Quiero** hacer clic en la tarjeta o en el botón *"Ficha 360°"* para abrir un panel lateral interactivo (Drawer),  
  > **Para** acceder a la totalidad de los datos (servicios activos, contratos SLA, contactos técnicos, webhooks y credenciales) bajo demanda sin ensuciar la pantalla principal.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** que el usuario hace clic sobre una tarjeta de organización,
  * **Cuando** se abre el Drawer lateral desde la derecha,
  * **Entonces** se accede de forma organizada mediante pestañas internas a:
    1. **Servicios & Módulos:** Lista conmutadores (toggle switches) para activar/desactivar cada servicio.
    2. **Acuerdos SLA & Parámetros:** Niveles de servicio contratados y ventanas de mantenimiento.
    3. **Contactos Clave:** Responsables técnicos y comerciales.
    4. **Incidentes en Curso:** Enlaces directos a los tickets abiertos de esa organización.

#### 🔹 UH-70: Cabecera Unificada y Segmented Control Moderno
* **Narrativa:**
  > **Como** Usuario del sistema,  
  > **Quiero** una barra superior armónica con pestañas integradas tipo Segmented Control y un único botón de acción principal,  
  > **Para** eliminar el desorden de botones y pestañas desalineadas.
* **Criterios de Aceptación (Gherkin):**
  * Las pestañas se consolidan en un Segmented Control: `[ 🏢 Organizaciones (14) ]`, `[ 📦 Catálogo de Servicios (9) ]`, `[ 🗂️ Matriz de Habilitación ]`.
  * Los botones dispersos de alta se unifican en un único botón principal a la derecha: `[ + Nueva Organización ▾ ]` con menú desplegable para `+ Nuevo Servicio / Módulo`.

#### 🔹 UH-71: Vista de Tabla Maestra de Alta Densidad (List View Zen)
* **Narrativa:**
  > **Como** Administrador corporativo con decenas de clientes,  
  > **Quiero** alternar a una vista tabular minimalista y paginada (10 filas/pág),  
  > **Para** gestionar organizaciones con máxima velocidad y sin scrolling excesivo.

---

## 🖥️ Wireframe Comparativo: Tarjeta Actual vs. Tarjeta Zen (v4.0.0)

```
[ TARJETA ACTUAL - RUIDO VISUAL Y EMBOLLO ]
┌──────────────────────────────────────────────────────────────┐
│ [O] OSDE                     [ Prepaga / Aseguradora ]       │
│     OSDE • Sede Central                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Contrato SLA: Platino 2h   │ Incidentes: 🚨 20 en curso  │ │
│ └──────────────────────────────────────────────────────────┘ │
│ Sistemas Habilitados: 7 de 11 activos                        │
│ [Receta Electrónica] [Telemedicina] [Portal Afiliados]       │
│ [Interoperabilidad y Registro] [Consultorio Digital]         │
│ [Cartilla Médica y Turnos] [Monitoreo Remoto (RPM)]          │  <- 7 etiquetas apiñadas
│ ┌──────────────────────────────────────────────────────────┐ │
│ │                📄 Ficha 360° & Módulos ➔                 │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘

[ NUEVA TARJETA ZEN v4.0.0 - LIMPIA, INTUITIVA Y PROFESIONAL ]
┌──────────────────────────────────────────────────────────────┐
│ [O] OSDE                              [ 🏢 Cliente Corporativo ]│
│     Sede Central • SLA Platino (2h)                          │
├──────────────────────────────────────────────────────────────┤
│ Estado Operativo: 🟡 20 incidentes activos                   │
│                                                              │
│ Cobertura: 7 de 11 servicios activos (64%)                   │
│ [████████████████████████░░░░░░░░░░░░]                       │
│ Chips clave: [ Telemedicina ] [ Portal Clientes ] [ +5 más ] │
├──────────────────────────────────────────────────────────────┤
│                   [ 👁️ Ver Ficha 360° ]                      │
└──────────────────────────────────────────────────────────────┘
```

---

---

## 🎖️ MÓDULO 12: Gobernanza y Supervisión — Rol Nativo Team Leader & Torre de Control

### 12.1. Diagnóstico del Vacío de Gestión
En las mesas de ayuda convencionales existe un salto perjudicial entre el Administrador (perfil técnico con permisos destructivos) y el Operador (abocado a resolver su cola individual de tickets). Se carece de una figura intermedia de **Gestión Operativa y Humana** capaz de intervenir en tiempo real, balancear cargas y rescatar la experiencia de clientes disconformes.

### 12.2. Historias de Usuario para el Team Leader (v4.0.0)

#### 🔹 UH-72: Matriz RBAC con Rol Nativo Team Leader / Supervisor
* **Narrativa:**
  > **Como** Director de Operaciones,  
  > **Quiero** un rol de `Team Leader` con permisos transversales de supervisión, reasignación y auditoría,  
  > **Para** delegar la conducción de la mesa sin otorgar permisos destructivos de infraestructura al supervisor.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** un usuario asignado al rol `Team Leader`,
  * **Cuando** ingresa a la plataforma,
  * **Entonces** tiene acceso de solo lectura/escritura a tickets de todas las instituciones y operadores, potestad de reasignación y bypass de escalamientos, pero **no tiene acceso a borrar tablas maestras ni variables de entorno del servidor**.

#### 🔹 UH-73: Torre de Control del Team Leader & Protocolo de Rescate de Quejas
* **Narrativa:**
  > **Como** Team Leader,  
  > **Quiero** un panel de supervisión en tiempo real con la carga de cada operador y una cola prioritaria de tickets con CSAT bajo (1 o 2 estrellas),  
  > **Para** intervenir de inmediato antes de que la queja escale a niveles directivos.
* **Criterios de Aceptación (Gherkin):**
  * **Escenario 1: Bandeja de Rescate Activo (Service Recovery)**
    * **Dado** que un solicitante califica un ticket con 1 o 2 estrellas o ingresa una queja,
    * **Cuando** se dispara el evento,
    * **Entonces** el ticket se destaca con badge `🚨 RESCATE REQUERIDO` en la Torre de Control del Team Leader con alerta push.
  * **Escenario 2: Balanceador de Carga (Live Dispatcher)**
    * **Dado** un operador sobrecargado o ausente,
    * **Cuando** el Team Leader selecciona sus tickets,
    * **Entonces** puede reasignarlos en lote a otros miembros de la guardia en 2 clics.

---

## 🚀 MÓDULO 13: Las 5 Armas Secretas del Podio (Diferenciadores 10x para el Pitch Ejecutivo)

Para asegurar el éxito comercial y posicionar a Quantux por encima de gigantes como Zendesk, Jira Service Management y ServiceNow, se definen los **5 factores de diferenciación radical**:

1. **🤖 IA Resolutiva Autónoma & Copilot N1 (Zero-Touch):** 
   * Ingesta inteligente que detecta fallas comunes en logs/APIs y ofrece botones de auto-reparación en 1 clic (`[ ⚡ Reintentar Webhook ]`, `[ 🔑 Regenerar Token ]`).
   * Resumen ejecutivo flash de hilos largos para operadores.
2. **🛡️ Mesa Proactiva "Self-Healing" (Detección y Cura Pre-Impacto):** 
   * Detección automática de micro-cortes y generación preventiva de tickets antes de que el cliente note la falla, notificándole con cortesía que el incidente ya fue resuelto.
3. **📸 Telemetría Oculta "Zero-Question" (Fin del "¿Me pasa una captura?"):** 
   * Captura automática y transparente de entorno: versión de app, navegador, resolución, y los últimos errores HTTP de consola en un JSON adjunto.
4. **💖 CSAT Gamificado "Buena Onda" & Muro de la Fama:** 
   * Calificación empática con emojis vivos y píldoras de elogios (*Kudos*), transformando el feedback en reconocimiento medible y motivación para los operadores.
5. **⚡ Cockpit Zen con Shortcuts de Teclado (<50ms):** 
   * Interfaz ultraliviana navegable al 100% por teclado (`j`/`k`, `r`, `e`, `c`), eliminando el síndrome de burnout y la fatiga visual.

---

## 🩺 MÓDULO 14: Suite Asistencial de Alta Prioridad — Exclusiva para Médicos y Profesionales de la Salud (Modo Clínico)

### 14.1. Principio Rector de Segregación de Roles (RBAC Clínico vs. Mesa de Ayuda)
* **Exclusividad para Médicos y Personal Asistencial:** Las capacidades de este módulo están concebidas y reservadas **únicamente para profesionales de la salud** en ejercicio asistencial directo (médicos de consultorio, cirujanos en quirófano, enfermeros de shock-room y médicos de guardia).
* **Invisibilidad Total para la Mesa de Ayuda (Soporte N1/N2/N3 y Admins):** Los operadores de soporte técnico y administradores **NO** tienen acceso a estos botones de emisión ni a los protocolos de contingencia médica en su interfaz. Agregar botones de "Paciente en Box" o "Talonario de Recetas" a un analista de soporte introduciría ruido visual y confusión que violaría los principios Zen de la v4.
* **Modelo Emisor/Receptor:**
  * **El Médico es el Emisor:** Emite una alerta de 1 solo toque o activa la contingencia médica en segundos desde su consultorio.
  * **La Mesa de Ayuda es el Receptor de Rescate:** En el Cockpit de soporte entra un ticket de emergencia con alarma sonora y badge pulsante `🚨 PACIENTE EN BOX • INTERNO 204`, obligando a una respuesta en menos de 3 minutos.

---

### 14.2. Historias de Usuario Asistenciales (v4.0.0)

#### 🔹 UH-74: Botón de Emergencia Asistencial "Paciente en Espera / Box Bloqueado" (1-Tap Emergency)
* **Narrativa:**
  > **Como** Médico o Profesional de Salud con un paciente presente en la consulta o guardia,  
  > **Quiero** presionar un único botón de emergencia asistencial (`[ 🚨 Paciente en Espera ]`),  
  > **Para** levantar un ticket P1 Crítico en menos de 5 segundos sin tener que completar formularios extensos con jerga de sistemas.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** un usuario autenticado con rol de profesional asistencial (`Dr.` / `Dra.` / `Médico`),
  * **Cuando** se encuentra en el portal y presiona `[ 🚨 Paciente en Box ]`,
  * **Entonces**:
    1. Se abre un diálogo instantáneo de 1 solo paso con selector rápido del Consultorio/Box actual y motivo asistencial preconfigurado:
       * `[ Receta Digital no valida / Bloqueada ]`
       * `[ Historia Clínica no abre / Bloqueada por concurrencia ]`
       * `[ Falla Visor de Placas DICOM / Rayos ]`
       * `[ Paciente en Box / Caída General de Consulta ]`
    2. Al confirmar (o tras 5 segundos de inactividad con confirmación automática), se genera un ticket P1 inmediato con bandera de impacto clínico.
    3. El sistema captura la estación de trabajo, IP local e interno telefónico del consultorio sin preguntarle al médico.

#### 🔹 UH-75: Protocolo de Contingencia Asistencial Inmediato (Plan B Offline)
* **Narrativa:**
  > **Como** Médico con el sistema de prescripción o HCE caído,  
  > **Quiero** recibir en pantalla de inmediato la herramienta de contingencia autorizada por la dirección médica,  
  > **Para** continuar atendiendo al paciente y emitir la receta o indicación en soporte alternativo sin paralizar la consulta.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** que un médico reporta una falla crítica en receta digital o HCE,
  * **Cuando** se confirma el incidente,
  * **Entonces** la plataforma le presenta una barra de herramientas de contingencia con acceso directo a:
    * `[ 📄 Descargar Talonario de Recetas Digital de Contingencia (PDF Oficial) ]`
    * `[ 🌐 Acceso al Validador de Emergencia Web ]`
    * `[ 📋 Ficha de Evolución Médica de Respaldo ]`
  * **Resultado:** La atención del paciente nunca se detiene mientras el equipo técnico soluciona la falla de fondo.

#### 🔹 UH-76: Audio-Ticket Clínico Asistencial (Dictado por Voz con IA)
* **Narrativa:**
  > **Como** Profesional de Salud habituado al dictado clínico,  
  > **Quiero** presionar un botón de micrófono y relatar la falla en un audio de 8 a 15 segundos,  
  > **Para** no perder tiempo tipeando frente a la computadora mientras examino o asisto a un paciente.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** el modal de reporte para médicos,
  * **Cuando** el profesional pulsa `[ 🎙️ Dictar Incidencia ]` y habla (ej: *"Se cayó la firma digital de Osde en el consultorio 3 con el paciente esperando"*),
  * **Entonces** el modelo de IA transcribe el audio, identifica la plataforma (`Receta Digital / Firma`), extrae la ubicación (`Consultorio 3`), detecta el financiador (`OSDE`) y auto-completa el ticket sin requerir escritura manual.

#### 🔹 UH-77: Receptor Crítico en Consola de Soporte (Alerta Visual y Sonora de Rescate Asistencial)
* **Narrativa:**
  > **Como** Operador de Soporte de Guardia o Nivel 1 en el Cockpit,  
  > **Quiero** recibir una alerta visual prominente y sonido de prioridad cuando un médico activa la emergencia de "Paciente en Box",  
  > **Para** comunicarme de inmediato por interno o tomar control remoto de la terminal en menos de 2 minutos.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** el Cockpit de soporte operado por un técnico,
  * **Cuando** ingresa un ticket originado por la Suite Asistencial Médica (UH-74),
  * **Entonces**:
    1. La fila en la grilla se destaca con un borde rojo pulsante y badge `🚨 PACIENTE EN BOX • URGENCIA CLÍNICA`.
    2. Se reproduce un tono sutil pero inconfundible de alerta asistencial.
    3. En el panel lateral se despliega el botón `[ 📞 Llamar a Consultorio ]` y `[ 🖥️ Conectar Asistencia Remota ]`.

---

## 🧭 MÓDULO 15: Dinámica Ergonómica del Menú Lateral Izquierdo (Sidebar Zen & Quick-Filters)

### 15.1. Diagnóstico del Menú Izquierdo Estático
En la versión actual, el panel lateral izquierdo (*Sidebar*) es estático y monolítico:
1. **Pérdida de Espacio de Trabajo:** Ocupa permanentemente 240px de ancho fijo, quitándole espacio a las tablas y a la lectura de incidentes complejos, sin posibilidad de plegarse cuando el técnico necesita concentración total.
2. **Ausencia de Ramificación Dinámica:** La opción *"Mesa de Ayuda"* es una sola entrada rígida; el técnico debe entrar a la grilla y luego aplicar filtros manualmente para saber cuántos tickets tiene asignados o cuántos casos críticos están sin resolver.
3. **Falta de Adaptación por Rol:** Muestra opciones que no corresponden a todos los perfiles, requiriendo validaciones dispersas en lugar de una reorganización limpia del menú lateral.

---

### 15.2. Historias de Usuario para el Menú Dinámico (v4.0.0)

#### 🔹 UH-78: Colapso y Expansión Dinámica del Sidebar (Modo Mini-Barra 64px con Tooltips Flotantes)
* **Narrativa:**
  > **Como** Operador o Administrador trabajando en monitores estándar o portátiles,  
  > **Quiero** poder plegar el menú lateral izquierdo mediante un botón conmutador `[ ◀ / ▶ ]` a un modo compacto de 64px,  
  > **Para** ganar un 25% más de espacio de pantalla en la grilla de tickets y fichas técnicas, manteniendo el acceso a los módulos mediante íconos y tooltips flotantes.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** el menú lateral desplegado en su ancho habitual (240px),
  * **Cuando** el usuario hace clic en el conmutador de colapso (o presiona la tecla de acceso directo `[`),
  * **Entonces**:
    1. El sidebar se contrae suavemente (transición de 200ms) a **64px** de ancho.
    2. Los textos de las opciones se ocultan armónicamente, permaneciendo centrados los íconos svg oficiales.
    3. El área principal de trabajo (`main-content`) se expande automáticamente ocupando todo el ancho liberado.
    4. Al posar el ratón (hover) sobre cualquier ícono en modo contraído, se despliega un **Tooltip Flotante elegante** con el nombre del módulo y atajo de teclado.
    5. El estado colapsado/expandido se guarda en `localStorage` del navegador para mantenerse tras recargas.

#### 🔹 UH-79: Árbol Dinámico de Vistas Rápidas con Contadores Vivos (Sub-Filtros de Mesa de Ayuda)
* **Narrativa:**
  > **Como** Operador de Soporte o Guardia,  
  > **Quiero** que bajo el menú *"Mesa de Ayuda"* se ramifiquen sub-vistas operativas directas con contadores en vivo,  
  > **Para** evaluar de un solo vistazo el volumen de casos y acceder a mi cola personal o a los incidentes urgentes en 1 clic.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** el ítem de navegación *"Mesa de Ayuda"*,
  * **Cuando** se encuentra activo o expandido,
  * **Entonces** despliega un sub-árbol indentado con los siguientes accesos inteligentes:
    * `⚡ Sin Asignar (X)`: Con badge ámbar en vivo que indica cuántos tickets esperan triage.
    * `👤 Mis Asignados (X)`: Con badge azul que contabiliza los casos abiertos asignados al usuario logueado.
    * `🔥 Críticos P1 (X)`: Con badge rojo pulsante que alerta sobre emergencias sin resolver.
    * `⏳ En Espera (X)`: Casos pausados a la espera de terceros o clientes.
    * `📥 Todos los Activos`: Grilla general estándar.
  * Al hacer clic en cualquiera de estos sub-ítems, la bandeja filtra automáticamente la vista sin requerir manipulación de filtros superiores.

#### 🔹 UH-80: Reconfiguración Contextual Dinámica por Rol (RBAC Zen del Menú Lateral)
* **Narrativa:**
  > **Como** Usuario autenticado en el sistema,  
  > **Quiero** que el menú izquierdo adapte automáticamente su estructura, enlaces y accesos según mi rol de negocio,  
  > **Para** interactuar únicamente con los módulos pertinentes a mi función, eliminando el ruido visual de accesos prohibidos o irrelevantes.
* **Criterios de Aceptación (Gherkin):**
  * **Dado** que inicia sesión un **Médico o Profesional de Salud (`SOLICITANTE`)**,
  * **Entonces** el menú izquierdo se limpia radicalmente y presenta únicamente:
    * `📋 Mis Solicitudes (X activas)`
    * `📚 Base de Conocimiento & Guías`
    *(Se ocultan Tablero, Usuarios, Plataformas y Configuración técnica)*.
  * **Dado** que inicia sesión un **Team Leader (`SUPERVISOR`)**,
  * **Entonces** se inyecta en el menú lateral la pestaña destacada:
    * `🎖️ Torre de Control & Despacho en Vivo` (Módulo 12).
  * **Dado** que inicia sesión un **Operador N1/N2/N3 (`SOPORTE`)**,
  * **Entonces** el menú prioriza la bandeja de triage, sub-filtros operativos y artículos de resolución.

---

## 📊 Matriz de Estimación del Backlog Completo (v4.0.0)

| Módulo | Historias de Usuario | Estimación |
| :--- | :--- | :---: |
| **1. Incidentes Masivos (Padre/Hijos)** | `UH-33`, `UH-34`, `UH-35` | 12 SP |
| **2. Releases y Despliegues** | `UH-36`, `UH-37` | 8 SP |
| **3. Bandeja General & Paginación** | `UH-38`, `UH-39`, `UH-40`, `UH-41` | 9 SP |
| **4. Workspace Zen (Área de Trabajo)** | `UH-42`, `UH-43`, `UH-44`, `UH-45`, `UH-46`, `UH-47` | 16 SP |
| **5. Reorganización del Flujo de Alta (Sin Ruido)** | `UH-48`, `UH-49`, `UH-50`, `UH-51` | 10 SP |
| **6. Generalización Enterprise (Multi-Servicio)** | `UH-52`, `UH-53` | 6 SP |
| **7. Tablero de Control Zen (Analytics Limpio)** | `UH-54`, `UH-55`, `UH-56`, `UH-57` | 9 SP |
| **8. Directorio de Usuarios Zen & Perfil Activo** | `UH-58`, `UH-59`, `UH-60`, `UH-61` | 10 SP |
| **9. Ingesta Automática por Correo (Email-to-Ticket)** | `UH-62`, `UH-63`, `UH-64` | 12 SP |
| **10. Cierre por Solicitante & CSAT Buena Onda** | `UH-65`, `UH-66`, `UH-67` | 12 SP |
| **11. Catálogo Zen de Organizaciones & Plataformas** | `UH-68`, `UH-69`, `UH-70`, `UH-71` | 11 SP |
| **12. Rol Team Leader & Torre de Control** | `UH-72`, `UH-73` | 10 SP |
| **14. Suite Asistencial Exclusiva Médicos (Modo Clínico)** | `UH-74`, `UH-75`, `UH-76`, `UH-77` | 25 SP |
| **15. Dinámica Ergonómica del Menú Lateral (Sidebar Zen)** | `UH-78`, `UH-79`, `UH-80` | 15 SP |
| **TOTAL BACKLOG v4.0.0** | **48 Historias de Usuario** | **165 Story Points** |

---

## 🌐 Suite de Enlaces y Entorno de Desarrollo Cloud Activo (v4.0.0-DEV)

| Recurso | URL Cloud / Acceso | Estado |
| :--- | :--- | :---: |
| 🌍 **URL Pública Cloud (HTTPS)** | `https://excerpt-honor-attempts-sen.trycloudflare.com` | **🟢 ONLINE (Activo)** |
| 🎛️ **Cockpit Mesa de Ayuda v4** | `https://excerpt-honor-attempts-sen.trycloudflare.com/cockpit` | **🟢 ONLINE (Activo)** |
| 📊 **Tablero Scrumban v4** | `https://excerpt-honor-attempts-sen.trycloudflare.com/scrumban` | **🟢 ONLINE (Activo)** |
| 📑 **Especificación Funcional v4** | `https://excerpt-honor-attempts-sen.trycloudflare.com/especificacion` | **🟢 ONLINE (Activo)** |
| 📚 **Swagger API Docs v4** | `https://excerpt-honor-attempts-sen.trycloudflare.com/docs` | **🟢 ONLINE (Activo)** |
| 🐙 **Repositorio GitHub (Rama v4-dev)** | `https://github.com/FREDDY-cloud395/healthdesk-quantux/tree/v4-dev` | **🟢 SINCRONIZADO** |
| 🔒 **Versión Anterior (v3.2.0-UAT)** | `https://healthdesk-quantux.onrender.com` | **🔒 CONGELADA / INTACTA** |



