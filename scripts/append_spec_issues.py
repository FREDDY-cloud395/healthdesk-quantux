NEW_SPEC_CONTENT = """
### 3.4. Incidencias y Mejoras de Gobernanza y Calidad Visual (Sprint 6)

* <a id="issue-59"></a>**ISSUE-59 [P1 - 3 SP]:** Restricción RBAC Perfil Analista de Soporte: Ocultamiento de 'Centro de Ayuda' y 'Mando Operativo' (Sprint 6, estado `sprint`).
  * *Narrativa:* **Como** Administrador de Seguridad, **quiero** que los analistas de soporte técnico no visualicen módulos de gestión directiva ni centros de autogestión de usuario final, **para** focalizar su rol operativo en la resolución de incidentes clínicos.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** una sesión iniciada con rol `analista`, **cuando** se carga el menú lateral, **entonces** las opciones 'Centro de Ayuda' y 'Mando Operativo' quedan totalmente ocultas.

* <a id="issue-60"></a>**ISSUE-60 [P1 - 3 SP]:** Persistencia Integral y Actualización Reactiva de la Configuración de SLA Institucional en la Tarjeta 360° (Sprint 6, estado `sprint`).
  * *Narrativa:* **Como** Gestor de Cuentas Hospitalarias, **quiero** configurar y persistir los tiempos de respuesta y resolución en la Ficha 360° de cada institución sin recargar la página, **para** garantizar la vigencia de los acuerdos de nivel de servicio.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el modal de configuración de SLA, **cuando** el gestor actualiza los tiempos y presiona 'Guardar', **entonces** los datos se persisten en base de datos y la ficha 360° se actualiza de manera reactiva inmediata.

* <a id="issue-61"></a>**ISSUE-61 [P1 - 5 SP]:** Motor Real de Simulación de Sobrecarga y Rebalanceo Algorítmico Efectivo en Mando Operativo (Sprint 6, estado `sprint`).
  * *Narrativa:* **Como** Jefe de Mesa de Ayuda, **quiero** disparar escenarios de estrés asistencial y rebalancear automáticamente las cargas de trabajo de los operadores, **para** evitar cuellos de botella y burnout operativo.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** un escenario de sobrecarga clínica simulada, **cuando** se activa el rebalanceo algorítmico, **entonces** los tickets se redistribuyen de forma equitativa minimizando la desviación estándar de carga por analista.

* <a id="issue-62"></a>**ISSUE-62 [P1 - 2 SP]:** Supresión y Ocultamiento de la Sub-Vista Confusa 'Niveles ITIL' (N1/N2/N3) en el Centro de Administración (Sprint 6, estado `sprint`).
  * *Narrativa:* **Como** Solution Owner, **quiero** remover interfaces abstractas no operativas que confunden la parametrización institucional, **para** mantener una experiencia de usuario clara y concisa.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el Centro de Plataformas, **cuando** se navegan las sub-pestañas, **entonces** ya no figura 'Niveles ITIL' y el foco se concentra en Instituciones, Módulos y Matriz.

* <a id="issue-63"></a>**ISSUE-63 [P0 - 5 SP]:** Motor del Demonio de Retrabajo: Ejecución Real de Desarrollo y Parches de Código desde el Tablero (Sprint 6, estado `sprint`).
  * *Narrativa:* **Como** Solution Owner, **quiero** que al pulsar el Demonio en una tarjeta de retrabajo se apliquen correcciones reales en el backend y frontend, **para** auditar la remediación automática sin simulaciones.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** una tarea observada, **cuando** se invoca `/api/v1/demon/execute/{taskId}`, **entonces** el backend ejecuta los parches de código, traslada la tarjeta al fondo de En Revisión y notifica al usuario.

* <a id="issue-64"></a>**ISSUE-64 [P1 - 2 SP]:** Regla FIFO Estricta en Retrabajo: Toda Tarjeta que Pase a Retrabajo Debe Quedar al Fondo de la Pila (Sprint 6, estado `sprint`).
  * *Narrativa:* **Como** Solution Owner, **quiero** que las tarjetas observadas se ubiquen estrictamente al fondo de la columna de Retrabajo, **para** respetar el orden de llegada y auditoría.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** una tarjeta rechazada en revisión, **cuando** pasa a la columna Retrabajo, **entonces** se añade al final de la lista visual sin desplazar las preexistentes.

* <a id="issue-65"></a>**ISSUE-65 [P1 - 3 SP]:** Persistencia de Configuración de SLA sin Cierre de Diálogo y Actualización Reactiva en Ficha 360° (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Administrador, **quiero** guardar cambios de SLA conservando el contexto de trabajo, **para** verificar de inmediato su reflejo visual.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el formulario de SLA, **cuando** se confirma el guardado, **entonces** se muestra feedback de éxito y la tarjeta institucional refleja los nuevos valores.

* <a id="issue-66"></a>**ISSUE-66 [P1 - 2 SP]:** Erradicación Integral de Colores Pesados y Oscuros en Modales y Ficha 360° (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Solution Owner, **quiero** que todos los modales utilicen fondos claros y tipografías limpias de la paleta Quantux, **para** evitar contrastes agresivos.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** cualquier modal de la aplicación, **cuando** se despliega en pantalla, **entonces** su fondo es claro (#FFFFFF / #F8FAFC) y carece de negros planos pesados.

* <a id="issue-67"></a>**ISSUE-67 [P1 - 2 SP]:** Unificación Terminológica de Pestañas y Eliminación Integral de Iconos/Emojis (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Solution Owner, **quiero** textos limpios y sobrios sin emojis en las pestañas del sistema, **para** asegurar un estándar hospitalario profesional.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el encabezado de navegación, **cuando** se renderizan las pestañas, **entonces** se exhibe texto puro institucional sin pictogramas UTF-8.

* <a id="issue-68"></a>**ISSUE-68 [P0 - 3 SP]:** Registro Previo de Tarjetas Scrumban para Toda Solicitud del Solution Owner (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Solution Owner, **quiero** que cada requerimiento o corrección solicitada genere de inmediato su correspondiente tarjeta en el tablero Scrumban, **para** contar con auditoría y trazabilidad histórica completa de las decisiones.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** una instrucción o feedback del Solution Owner, **cuando** se procesa la solicitud, **entonces** se crea una tarjeta formal con ID unívoco, criterios DoD e impacto de negocio en el tablero Scrumban y CSV.

* <a id="issue-69"></a>**ISSUE-69 [P1 - 3 SP]:** Preservación Estricta del Estado Operativo en Rollover de Tareas al Siguiente Sprint (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Solution Owner, **quiero** que las tareas que migran de sprint conserven exactamente su estado operativo (revisión/qa o curso/progress), **para** evitar reseteos artificiales a backlog y preservar la realidad de la mesa.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** una tarjeta en estado `qa`, `progress` o `rework`, **cuando** se efectúa la transición al siguiente sprint, **entonces** mantiene su columna operativa intacta en la nueva iteración.

* <a id="issue-70"></a>**ISSUE-70 [P1 - 2 SP]:** Ocultamiento de Ficha FHIR R4 y Payload JSON Crudo en Detalle del Ticket (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Analista de Mesa de Ayuda, **quiero** que el detalle del ticket clínico no exhiba bloques técnicos crudos de JSON ni fichas FHIR extensas, **para** centrar la atención en la evolución médica del incidente.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** la vista de un ticket de soporte, **cuando** se carga el panel técnico, **entonces** la ficha FHIR R4 y el preformateado de JSON crudo quedan completamente ocultos.

* <a id="issue-71"></a>**ISSUE-71 [P1 - 5 SP]:** Inmutabilidad Absoluta en Frontend y Backend para Tickets en Estado CERRADO (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Auditor TI y Oficial de Cumplimiento ITIL, **quiero** que un caso en estado CERRADO sea estrictamente inmutable tanto en la interfaz como en la API REST, **para** impedir modificaciones post-cierre o reaperturas no autorizadas.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** un ticket con estado `CERRADO`, **cuando** un operador intenta enviar un comentario o modificar su estado vía API, **entonces** el backend responde con HTTP 400 y la UI muestra exclusivamente el banner de inmutabilidad ITIL.

* <a id="issue-72"></a>**ISSUE-72 [P1 - 3 SP]:** Corrección de Parseo UTC Naive y Visualización Natural de Tiempo Transcurrido (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Supervisor de Mesa de Ayuda, **quiero** que el tiempo transcurrido de los incidentes refleje su duración exacta y no '0.0 h (1 min)' por desfase de huso horario local, **para** auditar con precisión los SLAs hospitalarios.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** un ticket creado hace 25 minutos, **cuando** se consulta su ficha métrica, **entonces** el tiempo transcurrido indica '25 min' sin desfases negativos ni lecturas en el futuro.

* <a id="issue-73"></a>**ISSUE-73 [P2 - 2 SP]:** Unificación y Claridad de Acciones de Asignación y Derivación (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Operador de Mesa, **quiero** una botonera limpia de acciones sin duplicidades entre 'En mi bandeja' y 'Asignar a...', **para** ejecutar la derivación de casos sin dudas cognitivas.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** un ticket asignado al usuario actual, **cuando** visualiza las acciones, **entonces** se muestra un único botón 'Reasignar / Derivar Caso'; si está desasignado, se muestran 'Asignar a mí' y 'Derivar a otro...'.

* <a id="issue-74"></a>**ISSUE-74 [P1 - 3 SP]:** Erradicación de Botones Negros y Corrección de Desaparición Visual en Hover (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Solution Owner, **quiero** erradicar el color negro en los botones de acción y asegurar que permanezcan visibles al posicionar el mouse, **para** garantizar la sobriedad y estabilidad visual del sistema.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el botón 'Abrir Caso' y demás botones de acción, **cuando** el usuario pasa el mouse sobre ellos (hover), **entonces** el botón no desaparece y mantiene fondo y texto en contraste institucional.

* <a id="issue-75"></a>**ISSUE-75 [P1 - 3 SP]:** Acotamiento Estricto de la Matriz Institucional a Exactamente 8 Módulos de Soporte (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Administrador de Plataformas, **quiero** que la matriz de habilitación y su exportación a CSV contengan exactamente los 8 módulos clínicos oficiales, **para** reflejar el alcance real contratado.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** la vista de Matriz de Soporte, **cuando** se renderiza la tabla o se exporta a CSV, **entonces** la grilla presenta exactamente 8 columnas de plataformas institucionales.

* <a id="issue-76"></a>**ISSUE-76 [P1 - 2 SP]:** Eliminación Total de Íconos y Emojis en Matriz de Soporte, Barra de Herramientas y CSV (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Solution Owner, **quiero** suprimir de inmediato emojis e iconos no autorizados (como el rayo ⚡ o íconos en botones de toolbar), **para** mantener la sobriedad corporativa del producto.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** los botones 'Mostrar Todas' y 'Exportar CSV' y el título 'Acciones del Ticket', **cuando** se inspecciona su contenido, **entonces** están compuestos exclusivamente por texto limpio sin pictogramas UTF-8.

* <a id="issue-77"></a>**ISSUE-77 [P1 - 2 SP]:** Contraste Visual Óptimo en Cierre 'X' de Modales y Tipografía 'Módulos de soporte' (Sprint 6, estado `qa`).
  * *Narrativa:* **Como** Usuario del Sistema, **quiero** que la 'X' para cerrar modales sea fácilmente distinguible y que la pestaña de navegación lea 'Módulos de soporte' en plural, **para** cumplir con accesibilidad visual y corrección gramatical.
  * *Criterios de Aceptación Gherkin:*
    * **Dado** el modal de participantes u otros modales, **cuando** se examina el botón de cierre, **entonces** la 'X' presenta un contraste superior a 4.5:1 sobre fondo blanco con borde delimitador, y la pestaña de módulos finaliza con la letra 's'.
"""

with open('docs/02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md', 'r', encoding='utf-8') as f:
    doc = f.read()

target = '*(El detalle completo de narrativas, escenarios Gherkin y criterios de adaptación se encuentra en el Documento DOC-GOV-008, DOC-QA-004 y en el Tablero Scrumban interactivo docs/00_Tablero_Scrumban_Quantux.html).*'

if target in doc:
    doc = doc.replace(target, NEW_SPEC_CONTENT + "\n" + target)
    print("Replaced target with NEW_SPEC_CONTENT successfully!")
else:
    doc += "\n" + NEW_SPEC_CONTENT
    print("Appended NEW_SPEC_CONTENT at the end of file!")

with open('docs/02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md', 'w', encoding='utf-8') as f:
    f.write(doc)

print("Updated docs/02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md successfully!")
