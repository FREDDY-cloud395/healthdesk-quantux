# -*- coding: utf-8 -*-
"""
Script de Ingesta y Homologación de Runbooks para la Base de Conocimiento Quantux.
Inserta y estructura las 23 guías operativas entregadas para los Analistas de Soporte.
"""

import sys
import os
import re
from datetime import datetime

# Agregar raíz al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from backend.app.db.session import engine
from backend.app.models.entities import KBArticle

RAW_ARTICLES_TEXT = """
### CD2-MAT-001: Prestador sin matrículas visibles en Consultorio Digital aunque figura habilitado en SISA

* **Módulo / Subsistema:** Gestión de Matrículas / Consultorio Digital / SISA
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** matrícula, matrícula médica, no aparece matrícula, matrícula vacía, SISA, REFEPS, prestador, perfil CD, habilitación

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"La prestadora no tiene ninguna matrícula en su perfil de Consultorio Digital. Cuando presiono sobre la fecha tampoco aparece ninguna para seleccionar."

#### 2. Diagnóstico y Causa Raíz
Se documentó un caso en el que el perfil del prestador en CD no mostraba matrículas, mientras que en SISA figuraban dos matrículas habilitadas. El auditor de CD contenía un JSON con "Matrículas: 0". Esto indica una discrepancia entre la información disponible en SISA y las matrículas efectivamente asociadas/recibidas por el perfil del prestador en Consultorio Digital. No se debe asumir que la ausencia en CD implica que la matrícula no existe en SISA.

#### 3. Procedimiento de Resolución Paso a Paso
1. Verificar en SISA/REFEPS si el prestador posee matrículas habilitadas.
2. Verificar el perfil del prestador en Consultorio Digital.
3. Revisar el auditor para identificar el JSON recibido y confirmar el valor de matrículas.
4. Si SISA posee matrículas habilitadas pero CD recibe "Matrículas: 0", escalar a Soporte N2/N3 para revisar la integración/proceso de actualización de matrículas.
5. No modificar manualmente la matrícula en CD sin confirmar previamente la fuente maestra y la regla de sincronización.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos revisando la información de su matrícula porque en el registro oficial figura habilitada, pero actualmente no se está mostrando correctamente en su perfil de Consultorio Digital. Ya verificamos la información y estamos gestionando la actualización correspondiente. Le avisaremos cuando quede disponible."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
* Comparar matrículas informadas por SISA/REFEPS contra las matrículas persistidas/recibidas por CD.
* Revisar auditoría del prestador.
* Caso documentado con JSON indicando "Matrículas: 0" pese a existir matrículas habilitadas en SISA.

---

### CD2-MAT-002: Matrícula visible en SISA pero no disponible para seleccionar al generar un turno

* **Módulo / Subsistema:** Agenda de Turnos / Matrículas
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** turno, matrícula, seleccionar matrícula, fecha, agenda, matrícula vacía, prestador

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Cuando quiero generar el turno no me aparece ninguna matrícula para seleccionar."

#### 2. Diagnóstico y Causa Raíz
La disponibilidad de una matrícula en SISA no garantiza por sí sola que la matrícula esté disponible para selección dentro de la agenda de CD. Debe existir correctamente la asociación entre prestador, matrícula y configuración de agenda.

#### 3. Procedimiento de Resolución Paso a Paso
1. Confirmar que el prestador tenga una matrícula habilitada.
2. Verificar si la matrícula llega correctamente a CD.
3. Revisar si la agenda/fecha seleccionada está asociada al prestador.
4. Revisar auditoría si la matrícula no aparece.
5. Escalar a N2/N3 cuando exista discrepancia entre la fuente maestra y la información disponible en CD.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos verificando la asociación de su matrícula con la agenda, ya que la información está disponible pero no se está mostrando correctamente para seleccionar el turno. Lo estamos revisando para que pueda operar con normalidad."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Validar la cadena SISA/REFEPS -> integración -> perfil CD -> agenda -> matrícula seleccionable.

---

### CD2-PREST-001: Cambio de CUIT de prestador manteniendo la información asociada

* **Módulo / Subsistema:** Prestadores / Consultorio Digital CD2 / Cartillas / Turnos
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** CUIT, cambiar CUIT, prestador, baja, alta, usuario, cartilla, turnos, datos anteriores

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Hay que cambiar el CUIT del prestador y mantener la información que ya tiene asociada."

#### 2. Diagnóstico y Causa Raíz
El cambio de CUIT implica trabajar sobre la identificación del prestador y su relación con el usuario actual. El procedimiento operativo documentado contempla una baja del usuario actual en CD2, modificación del CUIT desde Cartillas/Turnos y posterior asociación de la información anterior al nuevo registro.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el prestador y el usuario actualmente asociado.
2. Dar de baja el usuario actual en CD2.
3. Realizar el cambio de CUIT desde Cartillas/Turnos.
4. Reenviar un turno de prueba.
5. Asociar los datos del registro anterior al nuevo registro.
6. Validar que el prestador pueda operar nuevamente con su información histórica.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Vamos a realizar la actualización de los datos del prestador para que el nuevo CUIT quede correctamente asociado, procurando conservar la información que ya tenía registrada. Una vez finalizada la actualización, validaremos que pueda operar normalmente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
El procedimiento documentado contempla intervención sobre el usuario de CD2 y posterior asociación de datos. Cualquier modificación directa en BD debe ejecutarse únicamente con los identificadores previamente validados.

---

### CD2-NUT-001: Actualización de Código del Nomenclador de Prestaciones para Videoconsulta de Nutrición (Especialidades 316/317)

* **Módulo / Subsistema:** Nomencladores / Especialidades / Consultorio Digital / proxy-reservas
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** nutrición, videoconsulta nutrición, especialidad 316, especialidad 317, nomenclador, código prestación, prestación 190173, 190173, 420296, proxy-reservas, cartillas

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"La prestación de videoconsulta de nutrición tiene que utilizar el nuevo código 190173" o "No se habilita el flujo de video para nutricionistas en las especialidades 316 y 317".

#### 2. Diagnóstico y Causa Raíz
Se documentó el reemplazo del código de prestación 420296 por el código 190173 — VIDEOCONSULTA NUTRICIÓN para las especialidades 316 y 317.
* **Aclaración crítica de arquitectura de datos**: El código 190173 es un código de prestación del nomenclador de cartillas / proxy-reservas. **NO es un concepto de SNOMED CT**. La terminología SNOMED CT está reservada exclusivamente para diagnósticos, patologías y antecedentes clínicos en la HCE.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar la prestación de videoconsulta correspondiente a nutrición.
2. Verificar la especialidad asociada (316 o 317).
3. Para especialidades 316/317, configurar y vincular el código de prestación 190173 en el nomenclador de cartillas y proxy-reservas.
4. Validar que no continúe utilizándose el código deprecado anterior 420296.
5. Realizar una prueba funcional de generación/uso de la prestación y apertura de sala.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Realizamos la actualización de la prestación de videoconsulta de nutrición para que utilice la codificación correspondiente (190173). La configuración en cartilla ya fue revisada y estamos validando su funcionamiento para que pueda atender normalmente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
* Código de prestación anterior deprecado: 420296.
* Código de prestación vigente documentado: 190173 — VIDEOCONSULTA NUTRICIÓN.
* Especialidades alcanzadas: 316 y 317.
* Microservicio: proxy-reservas / cartilla.
* Regla de interoperabilidad: No mezclar nomenclador de prestaciones con servidor terminológico SNOMED CT.

---

### CD2-LAB-001: Prestación de laboratorio sin codificación SNOMED

* **Módulo / Subsistema:** Nomencladores / Laboratorio
* **Categoría:** HCE
* **Palabras Clave / Tags:** laboratorio, SNOMED, NNO, nomenclador, código de laboratorio, estudio

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Este estudio aparece sin una codificación SNOMED válida."

#### 2. Diagnóstico y Causa Raíz
Se detectó la necesidad de reemplazar una codificación NNO por un concepto SNOMED CT válido. La regla técnica documentada establece que la referencia debe utilizar el sistema: http://snomed.info/sct

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el estudio de laboratorio.
2. Verificar si actualmente está codificado como NNO.
3. Buscar la correspondencia SNOMED CT correspondiente.
4. Configurar el concepto utilizando http://snomed.info/sct como sistema.
5. Validar la prestación en el flujo funcional correspondiente.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos revisando la codificación del estudio para que quede correctamente identificado dentro del sistema. La actualización se realiza sobre la configuración interna y no requiere ninguna acción adicional de su parte."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Sistema SNOMED documentado: http://snomed.info/sct. No asumir correspondencia directa cuando el concepto no haya sido validado.

---

### CD2-USR-001: Corrección del correo electrónico asociado al usuario

* **Módulo / Subsistema:** Usuarios / Datos de contacto / MongoDB
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** email, correo, mail incorrecto, usuario, prestador, corrección de correo

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"El correo electrónico del usuario está mal cargado y hay que corregirlo."

#### 2. Diagnóstico y Causa Raíz
El correo se encuentra almacenado dentro de la estructura telecom del usuario. La corrección requiere actualizar el valor correspondiente al elemento cuyo system sea email.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el _id del usuario.
2. Confirmar cuál elemento de telecom corresponde al correo.
3. Verificar el valor actual.
4. Actualizar únicamente el elemento cuyo system sea email.
5. Validar nuevamente el dato desde la aplicación.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Ya identificamos el inconveniente con la dirección de correo registrada. Estamos realizando la corrección y luego verificaremos que el dato quede actualizado correctamente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Patrón de actualización documentado en MongoDB:
db.users.updateOne({ _id: ObjectId("<USER_ID>") }, { $set: { "telecom.$[email].value": "<CORREO_CORRECTO>" } }, { arrayFilters: [ { "email.system": "email" } ] })

---

### CD2-INST-001: Alta/configuración de prestador y validación del circuito de agenda

* **Módulo / Subsistema:** Prestadores / Cartillas / Agenda de Turnos
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** alta prestador, registrar prestador, agenda, turno, cartilla, configuración, prestador nuevo

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo registrar/usar al prestador en la plataforma digital" o "El prestador está dado de alta pero no puedo operar con sus turnos."

#### 2. Diagnóstico y Causa Raíz
El alta funcional de un prestador involucra más de un componente: identificación del prestador, datos maestros, matrícula, configuración de cartilla y disponibilidad de agenda. Un alta aparentemente correcta no garantiza que todo el circuito esté operativo.

#### 3. Procedimiento de Resolución Paso a Paso
1. Verificar que el prestador exista y esté correctamente identificado.
2. Validar matrícula y habilitación.
3. Verificar configuración en Cartillas.
4. Verificar agenda y disponibilidad.
5. Ejecutar una prueba de generación/gestión de turno.
6. Si alguno de los componentes no coincide, escalar con evidencia del punto donde se produce la inconsistencia.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos verificando la configuración completa del prestador y su agenda, ya que el alta requiere que varios datos queden correctamente vinculados. Vamos a validar el circuito para identificar dónde se está produciendo el inconveniente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Validar como mínimo: Prestador -> usuario -> matrícula -> cartilla -> agenda -> turno.

---

### CD2-PAU-001: Error al registrar una consulta en Consultorio Digital (Atención Rechazada y Registro por Diferido)

* **Módulo / Subsistema:** Consultorio Digital / Registro de atención
* **Categoría:** HCE
* **Palabras Clave / Tags:** PAU, no puede registrar, registrar consulta, consulta rechazada, registrar por diferido, diferido, error al atender, plataforma rechaza, terminal, atención presencial

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo registrar la consulta. Las terminales están funcionando pero la plataforma rechaza la operación." o "El médico no puede registrar la atención."

#### 2. Diagnóstico y Causa Raíz
Regla de Operación Crítica CD2: Si una prestación presencial resulta rechazada por la plataforma, **NO se puede reintentar registrar desde el módulo de Consultorio Digital** (debe gestionarse por diferido o mediante el validador externo del financiador). Para consultas virtuales, se valida sesión y se permite reintento tras recarga.

#### 3. Procedimiento de Resolución Paso a Paso
1. **Determinar Tipo de Atención:** Identificar si la consulta es de modalidad Presencial o Videoconsulta Virtual.
2. **Atención Presencial (Regla de Diferido):** Indicar inmediatamente que no reintente registrar dentro de CD2. Indicar que debe registrar la atención por **diferido** o a través del validador externo para no demorar la atención médica ni afectar honorarios.
3. **Atención Virtual:** Solicitar refrescar pantalla con Ctrl+F5 y reintentar desde el módulo de registración para turnos virtuales.
4. **Verificación de Credenciales:** Confirmar estado de terminales y autenticación del prestador.
5. **Escalamiento:** Si el rechazo de plataforma persiste y no responde a diferido, recopilar captura, timestamp y prestador, escalando a N2/N3.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estimado/a profesional: Si la plataforma le rechaza el registro de una atención presencial, le recordamos que no debe reintentar dentro de Consultorio Digital: puede registrar la consulta por diferido o a través del validador externo para asegurar la atención del paciente y el cobro de honorarios. Ya nos encontramos analizando el motivo del rechazo en el sistema central."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Trazar transacciones en backend de validación (ITC, Activia, APG). Las registraciones en plataformas externas no se reflejan automáticamente en el histórico local de CD2 sin conciliación nocturna.

---

### CD2-PAU-002: Prestador correctamente identificado pero operación rechazada en plataforma

* **Módulo / Subsistema:** Consultorio Digital / Integraciones
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** rechazo, plataforma, credenciales correctas, PAU, integración, error, operación

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Las credenciales son correctas, pero la plataforma igualmente rechaza la operación."

#### 2. Diagnóstico y Causa Raíz
La validación de credenciales no descarta un problema posterior en el flujo. Cuando la autenticación es correcta, debe analizarse la operación concreta y las integraciones involucradas.

#### 3. Procedimiento de Resolución Paso a Paso
1. Confirmar autenticación exitosa.
2. Identificar exactamente qué operación es rechazada.
3. Registrar mensaje/error y horario.
4. Revisar logs de la operación.
5. Comparar con una operación exitosa, si existe.
6. Escalar con evidencias a N2/N3.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Las credenciales fueron verificadas correctamente. El inconveniente parece producirse durante la operación posterior al ingreso, por lo que estamos revisando ese punto específico para identificar la causa."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Priorizar revisión de logs y trazabilidad de la operación antes de modificar datos del prestador.

---

### CD2-INC-001: Rechazo de operación con infraestructura local aparentemente operativa

* **Módulo / Subsistema:** Consultorio Digital / Soporte
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** terminal OK, plataforma caída, rechazo, soporte, PAU, infraestructura

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Las terminales funcionan correctamente, pero la plataforma rechaza la operación."

#### 2. Diagnóstico y Causa Raíz
El hecho de que las terminales funcionen correctamente permite descartar inicialmente una falla local evidente, pero no determina por sí mismo la causa del rechazo. El análisis debe continuar sobre el flujo de aplicación e integración.

#### 3. Procedimiento de Resolución Paso a Paso
1. Confirmar funcionamiento de terminales.
2. Confirmar autenticación.
3. Reproducir la operación.
4. Capturar mensaje de error.
5. Revisar trazas/logs.
6. Escalar con evidencia si el problema continúa.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Verificamos que el equipamiento esté funcionando correctamente. Ahora estamos revisando la operación dentro de la plataforma para identificar por qué se produce el rechazo."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
No confundir infraestructura local operativa con flujo funcional operativo.

---

### SOPORTE-GCP-001: Análisis de solicitudes mediante logs

* **Módulo / Subsistema:** Observabilidad / GCP Logs / Integraciones
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** logs, GCP, request, error, trazabilidad, integración, timestamp, soporte N2

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Necesitamos saber qué está pasando con las solicitudes que recibe el servicio."

#### 2. Diagnóstico y Causa Raíz
Los logs de GCP se utilizan para analizar las solicitudes y respuestas generadas por los servicios, correlacionando los eventos con el horario y el incidente reportado.

#### 3. Procedimiento de Resolución Paso a Paso
1. Obtener fecha y hora aproximada del incidente.
2. Identificar servicio/operación involucrada.
3. Buscar las solicitudes correspondientes en GCP Logs.
4. Revisar request, response y errores asociados.
5. Comparar solicitudes exitosas y fallidas cuando sea posible.
6. Adjuntar la evidencia relevante al ticket antes de escalar.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos revisando el registro de la operación para identificar exactamente en qué punto se produce el inconveniente. Con esa información podremos determinar la corrección necesaria."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Herramientas documentadas para análisis: GCP Logs, Kibana, Apigee y Jira para seguimiento.

---

### CD2-DB-001: Baja lógica de usuario/prestador

* **Módulo / Subsistema:** Usuarios / Prestadores / MongoDB
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** baja, baja lógica, usuario, prestador, isDeleted, desactivar, reactivar

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Hay que dar de baja al usuario/prestador, pero necesitamos conservar sus datos."

#### 2. Diagnóstico y Causa Raíz
En las operaciones de soporte documentadas se contempla el uso de bajas lógicas, evitando eliminar físicamente información cuando el flujo requiere conservar los datos históricos o posteriormente asociarlos a otro registro.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar exactamente el registro a desactivar.
2. Confirmar que corresponde realizar una baja lógica.
3. Aplicar la marca lógica definida por el modelo.
4. Validar que el usuario deje de estar operativo.
5. Verificar que la información histórica permanezca disponible cuando corresponda.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Vamos a actualizar el estado del registro para que deje de estar operativo, conservando la información necesaria para mantener la trazabilidad de los datos."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
La variable isDeleted aparece como bandera lógica relevante en los procedimientos de soporte documentados.

---

### PRESC-001: Validación de nomencladores para prestaciones especiales

* **Módulo / Subsistema:** Prescripción / Nomencladores
* **Categoría:** Receta Digital
* **Palabras Clave / Tags:** receta, prescripción, medicamento, prestación, nutrición, estudio, nomenclador, SNOMED

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"La prestación/estudio no aparece correctamente para utilizarlo en el circuito digital."

#### 2. Diagnóstico y Causa Raíz
Las prestaciones utilizadas en los circuitos digitales dependen de su correcta identificación en los nomencladores. Casos concretos relacionados con la codificación SNOMED de nutrición y laboratorio.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar la prestación afectada.
2. Verificar el código actualmente configurado.
3. Validar el nomenclador correspondiente.
4. Confirmar la codificación SNOMED cuando corresponda.
5. Probar nuevamente la operación.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos revisando la configuración de la prestación para verificar que esté correctamente identificada en el sistema. Una vez validada, podremos confirmar su disponibilidad."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Revisión de nomencladores y homologación SNOMED.

---

### TEL-001: Incidentes de videoconsulta

* **Módulo / Subsistema:** Telemedicina / Videoconsulta
* **Categoría:** Telemedicina
* **Palabras Clave / Tags:** videoconsulta, cámara, micrófono, audio, video, conexión, Jitsi, WebRTC

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo entrar a la videoconsulta" / "No funciona la cámara o el micrófono."

#### 2. Diagnóstico y Causa Raíz
Problemas de acceso a periféricos multimedia en el navegador o bloqueos locales de red hacia los sockets WebRTC.

#### 3. Procedimiento de Resolución Paso a Paso
1. Confirmar que el usuario pueda acceder a la videoconsulta.
2. Verificar permisos de cámara y micrófono del navegador.
3. Verificar si el problema afecta audio, video o conexión completa.
4. Registrar navegador, fecha/hora y mensaje de error.
5. Escalar con evidencia si persiste.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Vamos a revisar el acceso a la videoconsulta y los permisos de cámara y micrófono. Si el inconveniente continúa, necesitaremos algunos datos de la conexión para analizarlo."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Validar permisos en Chrome/Edge y estado del servidor de WebRTC.

---

### IAM-001: Correo principal del prestador

* **Módulo / Subsistema:** Identidad / Usuarios / Datos Maestros
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** correo prestador, email principal, usuario, datos maestros, mail, contacto

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"El correo del prestador está incorrecto" / "Necesitamos cambiar el mail del usuario."

#### 2. Diagnóstico y Causa Raíz
El correo electrónico forma parte de los datos de contacto del usuario. La estructura documentada utiliza telecom y distingue el elemento mediante system: "email".

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar al usuario correcto.
2. Verificar el correo actualmente registrado.
3. Confirmar el nuevo correo.
4. Actualizar únicamente el elemento identificado como email.
5. Validar desde la aplicación.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Vamos a corregir la dirección de correo registrada y verificar que la actualización quede correctamente reflejada en el sistema."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
No confundir el correo del usuario/prestador con datos de contacto de otras entidades.

---

### SOPORTE-001: Clasificación y escalamiento de incidentes

* **Módulo / Subsistema:** Mesa de Ayuda / Soporte N1-N2-N3
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** ticket, soporte, incidente, prioridad, N1, N2, N3, escalamiento, impacto, urgencia

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Tenemos un problema con la plataforma y necesitamos soporte."

#### 2. Diagnóstico y Causa Raíz
El esquema operativo contempla recepción, recopilación de evidencias, clasificación por impacto/urgencia, diagnóstico, escalamiento, solución, pruebas y cierre.

#### 3. Procedimiento de Resolución Paso a Paso
1. Recibir el incidente y registrar la información disponible.
2. Solicitar evidencia suficiente para reproducirlo.
3. Clasificar impacto y urgencia.
4. Diagnosticar en N1.
5. Escalar a N2/N3 cuando corresponda.
6. Registrar diagnóstico y solución.
7. Validar la corrección y cerrar el ticket con la resolución documentada.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Recibimos el inconveniente y estamos revisando la información para identificar la causa. Si necesitamos algún dato adicional para reproducirlo, se lo solicitaremos. Una vez validada la solución, confirmaremos la resolución."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
N1: Lunes a viernes 08:00–20:00 + guardias. N2/N3: 09:00–18:00 + guardias rotativas.

---

### KB-001: Evidencia mínima para escalar un incidente

* **Módulo / Subsistema:** Mesa de Ayuda / Soporte
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** escalar, evidencia, soporte N2, soporte N3, error, logs, ticket, reproducción

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"El problema sigue ocurriendo y necesitamos que lo revise otro equipo."

#### 2. Diagnóstico y Causa Raíz
Un escalamiento sin evidencia suficiente aumenta el tiempo de diagnóstico. El flujo documentado exige recopilar información del incidente antes de derivarlo a niveles superiores.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar usuario/prestador afectado.
2. Registrar operación que falla, fecha y hora.
3. Registrar mensaje de error y capturas disponibles.
4. Indicar pasos para reproducir e incorporar logs cuando estén disponibles.
5. Escalar al nivel correspondiente.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos recopilando la información necesaria para que el equipo técnico pueda analizar el inconveniente sin pedirle nuevamente los mismos datos. En cuanto tengamos la revisión, continuaremos con la resolución."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
La evidencia debe permitir reconstruir qué ocurrió, cuándo ocurrió, con qué usuario y en qué operación.

---

### DOC-001: Descarga de documentación clínica en PDF

* **Módulo / Subsistema:** Documentación Clínica / HCE
* **Categoría:** HCE
* **Palabras Clave / Tags:** PDF, descarga, documento clínico, historia clínica, archivo, link, documentación

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo descargar el PDF de la documentación clínica."

#### 2. Diagnóstico y Causa Raíz
Falla de acceso o generación de enlaces temporales presignados para almacenamiento seguro.

#### 3. Procedimiento de Resolución Paso a Paso
1. Confirmar qué documento se intenta descargar.
2. Verificar si el documento se visualiza correctamente antes de descargarlo.
3. Registrar el mensaje de error, fecha/hora y usuario.
4. Escalar para revisión del almacenamiento/link si el problema persiste.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos verificando el acceso al documento para identificar por qué la descarga no se está completando. Por favor, indíquenos qué documento intenta descargar y qué mensaje aparece."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Política de retención de 6 meses y enlaces presignados temporales.

---

### DOC-002: Documento clínico fuera del período de retención

* **Módulo / Subsistema:** Almacenamiento / Documentación Clínica
* **Categoría:** HCE
* **Palabras Clave / Tags:** PDF, documento antiguo, historia clínica, archivo, seis meses, retención, descarga

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo acceder a un documento clínico antiguo."

#### 2. Diagnóstico y Causa Raíz
La política documentada contempla una retención temporal de 6 meses para determinados documentos/recursos almacenados en storage temporal.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el documento solicitado.
2. Verificar la fecha de generación.
3. Determinar si se encuentra dentro del período de retención de 6 meses.
4. Si está fuera del período, verificar el procedimiento para ese tipo de documentación histórica.
5. Si está dentro del período y no es accesible, escalar como incidente técnico.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Vamos a verificar la fecha del documento y su disponibilidad para determinar si se encuentra dentro del período de conservación establecido. Si corresponde, revisaremos el acceso técnico al archivo."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
6 meses de retención temporal en almacenamiento activo.

---

### PRESC-002: Firma digital y validación criptográfica de recetas

* **Módulo / Subsistema:** Prescripción Electrónica
* **Categoría:** Receta Digital
* **Palabras Clave / Tags:** receta, firma digital, certificado, token, firmar, certificado vencido, firma electrónica

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo firmar la receta."

#### 2. Diagnóstico y Causa Raíz
Inconvenientes al momento de invocar el módulo o servicio de firma criptográfica.

#### 3. Procedimiento de Resolución Paso a Paso
1. Registrar el mensaje exacto que aparece al intentar firmar.
2. Confirmar usuario y operación.
3. Identificar si el rechazo ocurre antes o durante la firma.
4. Registrar fecha/hora y escalar con la evidencia correspondiente.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos revisando el inconveniente que se presenta al momento de firmar la receta. Para poder identificarlo necesitamos analizar el mensaje que aparece durante el intento de firma."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Verificar si el módulo de firma digital responde o si hay errores de socket/agente local.

---

### PRESC-003: Contingencia de receta offline / código de barras

* **Módulo / Subsistema:** Prescripción Electrónica
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** receta offline, contingencia, código de barras, receta electrónica, caída

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"No puedo emitir la receta electrónica y necesito una alternativa."

#### 2. Diagnóstico y Causa Raíz
Indisponibilidad del servicio en línea de prescripción o conectividad.

#### 3. Procedimiento de Resolución Paso a Paso
1. Registrar el motivo por el cual no puede emitirse la receta.
2. Confirmar si se trata de una indisponibilidad general o individual.
3. Registrar evidencia del error y escalar al soporte correspondiente.
4. Aplicar únicamente el mecanismo de contingencia formalmente vigente.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos verificando la disponibilidad del servicio de prescripción para determinar el inconveniente. Le indicaremos el procedimiento correspondiente una vez confirmado el estado del servicio."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Validar canal de contingencia homologado.

---

### IAM-002: Modificación de datos sensibles de afiliados

* **Módulo / Subsistema:** IAM / Extranet / Datos Maestros / CRM
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** afiliado, datos personales, cobertura, obra social, modificación, datos sensibles, CRM

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Necesito modificar los datos del afiliado" / "Los datos de cobertura no coinciden."

#### 2. Diagnóstico y Causa Raíz
Discrepancias entre sistemas sobre la fuente maestra del dato sensible del afiliado.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el afiliado.
2. Determinar qué dato presenta la inconsistencia.
3. Identificar el sistema que informa actualmente el dato.
4. No modificar directamente información sensible sin confirmar la fuente maestra.
5. Escalar al equipo responsable del dato maestro cuando corresponda.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Vamos a verificar el dato en nuestros sistemas para identificar cuál es la información correcta y realizar la actualización por el circuito correspondiente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Validar fuente maestra antes de cualquier intervención.

---

### IAM-003: Diferencia entre datos del prestador y datos del paciente

* **Módulo / Subsistema:** Identidad / Datos Maestros
* **Categoría:** Contingencias
* **Palabras Clave / Tags:** prestador, paciente, email, usuario, datos maestros, identidad, correo

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"El correo/dato que aparece en pantalla no corresponde al prestador."

#### 2. Diagnóstico y Causa Raíz
La plataforma maneja diferentes entidades. Un dato de contacto asociado al prestador no debe confundirse con el del paciente.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar la entidad que presenta el dato incorrecto.
2. Identificar el usuario asociado.
3. Determinar si el dato pertenece al prestador o al paciente.
4. Validar la fuente maestra y corregir únicamente el registro correspondiente.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos verificando a qué registro corresponde el dato que aparece en pantalla para evitar modificar información incorrecta. Una vez identificado, realizaremos la corrección correspondiente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
La identificación de la entidad precede a cualquier modificación.
"""

def parse_and_ingest():
    articles_raw = RAW_ARTICLES_TEXT.strip().split("\n---\n")
    print(f"Total articulos detectados en el lote: {len(articles_raw)}")

    with Session(engine) as session:
        created_count = 0
        updated_count = 0

        for block in articles_raw:
            block = block.strip()
            if not block or not block.startswith("###"):
                continue

            lines = block.split("\n")
            title_line = lines[0].replace("###", "").strip()
            
            # Extraer categoria y tags
            category = "Consultorio Digital"
            tags = ""
            for line in lines[1:10]:
                if "**Categoría:**" in line:
                    category = line.split("**Categoría:**")[1].strip()
                elif "**Palabras Clave / Tags:**" in line:
                    tags = line.split("**Palabras Clave / Tags:**")[1].strip()

            # Normalizar categoria segun filtros
            cat_normalized = category
            if "Consultorio" in category:
                cat_normalized = "Consultorio Digital"
            elif "Receta" in category:
                cat_normalized = "Receta Digital"
            elif "Telemedicina" in category:
                cat_normalized = "Telemedicina"
            elif "HCE" in category:
                cat_normalized = "Historia Clínica"
            elif "Contingencia" in category:
                cat_normalized = "Contingencias"

            # Buscar si ya existe por titulo o codigo
            code_prefix = title_line.split(":")[0].strip()
            existing = session.exec(
                select(KBArticle).where(
                    (KBArticle.title == title_line) | 
                    (KBArticle.title.like(f"{code_prefix}:%"))
                )
            ).first()

            if existing:
                existing.title = title_line
                existing.category = cat_normalized
                existing.tags = tags
                existing.content = block
                existing.author_username = "Soporte N3 CD2"
                existing.version = "v1.1-Homologado"
                existing.changelog = "Estructuración operativa homologada para analistas de soporte"
                existing.space_name = "Runbooks de Soporte"
                existing.is_published = True
                existing.updated_at = datetime.utcnow()
                session.add(existing)
                updated_count += 1
            else:
                new_art = KBArticle(
                    title=title_line,
                    category=cat_normalized,
                    tags=tags,
                    content=block,
                    author_username="Soporte N3 CD2",
                    version="v1.0-Homologado",
                    changelog="Alta inicial de runbook operativo para analistas",
                    space_name="Runbooks de Soporte",
                    view_count=10,
                    requests_deflected=5,
                    helpful_score=98,
                    is_published=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(new_art)
                created_count += 1

        session.commit()
        print(f"Ingesta finalizada: {created_count} creados, {updated_count} actualizados.")

if __name__ == "__main__":
    parse_and_ingest()
