# -*- coding: utf-8 -*-
"""
Script de Ingesta del Manual Maestro Consolidado CD2: Verdad Única y Escenarios Críticos.
Registra los 10 escenarios críticos [MAT-001] a [BIO-010] y el Manual Maestro de Verdad Única (SSOT).
"""

import sys
import os
from datetime import datetime

# Agregar raíz al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session, select
from backend.app.db.session import engine
from backend.app.models.entities import KBArticle

ARTICLES_DATA = [
    {
        "code": "MAT-001",
        "title": "MAT-001: Módulo de Matrículas - Selectores Bloqueados en Consultorio Digital",
        "category": "Consultorio Digital",
        "tags": "matrícula, selector bloqueado, no aparece matrícula, SISA, CRM, consultorio-digital-cliente, IC, habilitación",
        "content": """### MAT-001: Módulo de Matrículas - Selectores Bloqueados en Consultorio Digital

* **Módulo / Subsistema:** consultorio-digital-cliente / Gestión de Matrículas (SISA / CRM)
* **Categoría:** Consultorio Digital
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** matrícula, selector bloqueado, no aparece matrícula, SISA, CRM, consultorio-digital-cliente, IC, habilitación

#### 1. Síntoma Reportado por el Usuario
"El médico no puede seleccionar una matrícula válida en el menú desplegable de su perfil o al iniciar una atención."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Discrepancia de Identificadores de Consulta (ICs) entre CRM y SISA. Caso resuelto en v3.9.0 mediante fix en la renderización de selectores.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Confirmar si el médico posee más de una matrícula registrada y habilitada en SISA/REFEPS.
2. **Acción de Resolución:** Si la matrícula por defecto está inhabilitada en el desplegable, indicar al médico que seleccione manualmente la matrícula alternativa válida. Si persiste, instruir a refrescar la caché de sesión del navegador (Ctrl+F5).
3. **Verificación de Éxito:** El selector se desbloquea y permite avanzar al registro o consulta médica.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si ambas matrículas figuran habilitadas en SISA pero el selector continúa vacío o bloqueado tras Ctrl+F5, derivar a N2 para verificar sincronización de ICs.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Verificamos que su matrícula está habilitada en los registros oficiales. Por favor seleccione la opción alternativa en el menú desplegable o refresque su navegador con las teclas Ctrl+F5 para actualizar los datos. Ya estamos asegurando que pueda operar con normalidad."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `consultorio-digital-cliente`. Verificar conciliación de ICs entre CRM y SISA.
"""
    },
    {
        "code": "VID-002",
        "title": "VID-002: Videoconsulta Jitsi - Latencia de Servidores y Parámetros de Red",
        "category": "Telemedicina",
        "tags": "videoconsulta, Jitsi, latencia, joinTimeout, self-view, sa-east1, eco, retardo, proxy-reservas",
        "content": """### VID-002: Videoconsulta Jitsi - Latencia de Servidores y Parámetros de Red

* **Módulo / Subsistema:** proxy-reservas / Jitsi Infrastructure
* **Categoría:** Telemedicina
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** videoconsulta, Jitsi, latencia, joinTimeout, self-view, sa-east1, eco, retardo, proxy-reservas

#### 1. Síntoma Reportado por el Usuario
"Se percibe una latencia considerable (~0.5 segundos), retardo en el audio o falla en la conexión inicial de la videoconsulta."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Despliegue accidental de instancias Jitsi en servidores de US Central en lugar de la región designada South America (San Pablo, Brasil - `sa-east1`), o agotamiento del timeout de handshake.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Confirmar la conectividad del médico y paciente y comprobar si el problema es de audio, video o conexión total.
2. **Acción de Resolución:** El sistema aplica automáticamente el ajuste de `joinTimeout` (5 intentos x 20 segundos). Indicar al médico verificar permisos de cámara/micrófono en la barra de navegación y activar la función "Self-View".
3. **Verificación de Éxito:** La sala establece comunicación bidireccional fluida con latencia menor a 150ms.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si la latencia alta afecta a múltiples consultorios concurrentes, escalar inmediatamente a Infraestructura N3 para verificar ruteo a región San Pablo.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Estamos monitoreando la calidad de conexión de su sala de videoconsulta. Por favor verifique que su navegador tenga concedidos los permisos de cámara y micrófono y que la vista propia ('Self-View') esté habilitada. El sistema optimizará el enlace en breves segundos."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Infraestructura: Jitsi desplegado en Google Cloud (`sa-east1`). Parámetro frontend: `joinTimeout: 20000`, `maxRetries: 5`.
"""
    },
    {
        "code": "SNM-003",
        "title": "SNM-003: Servidor Terminológico SNOMED CT - Mapeo de Términos Coloquiales",
        "category": "Historia Clínica",
        "tags": "SNOMED, nomenclador, terminología, laboratorio, búsqueda de estudios, hepatograma, ofuscación",
        "content": """### SNM-003: Servidor Terminológico SNOMED CT - Mapeo de Términos Coloquiales

* **Módulo / Subsistema:** Servidor de Terminología / IPS / Prescripción HCE
* **Categoría:** Historia Clínica
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** SNOMED, nomenclador, terminología, laboratorio, búsqueda de estudios, hepatograma, ofuscación

#### 1. Síntoma Reportado por el Usuario
"No se encuentran estudios habituales de laboratorio o diagnóstico por imágenes al buscarlos en el buscador de la consulta."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Falta de coincidencia exacta entre la descripción técnica canónica de SNOMED CT y el término coloquial médico habitual.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Preguntar al médico qué estudio exacto está intentando prescribir.
2. **Acción de Resolución:** Solicitar al médico que busque por el nombre coloquial simple (ej. "Hepatograma" en lugar de "Procedimiento hepático") o ingrese únicamente las primeras 4 letras de la práctica. Si el servidor central no responde, el sistema activará automáticamente el fallback de caché local.
3. **Verificación de Éxito:** El estudio aparece listado y se agrega a la prescripción.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si un estudio habitual no figura en la base de sinónimos, transferir a N2 para solicitar la incorporación del sinónimo en el nomenclador semántico.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Por favor pruebe buscar la práctica utilizando su denominación habitual más simple o las primeras cuatro letras (por ejemplo, 'Hepatograma'). El sistema incluye mecanismos de autocompletado rápido para facilitar su prescripción."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Servidor de Terminología / IPS. Sistema URI: `http://snomed.info/sct`. Nota de seguridad: Al emitir el registro, los datos clínicos se ofuscan en el PDF final para garantizar privacidad.
"""
    },
    {
        "code": "REG-004",
        "title": "REG-004: Integración CRM y Conciliación de Regiones / Filiales",
        "category": "Consultorio Digital",
        "tags": "CRM, región, filial, efector, región 17, región 22, desalineación, consultorio, permisos",
        "content": """### REG-004: Integración CRM y Conciliación de Regiones / Filiales

* **Módulo / Subsistema:** Integración CRM / Módulo de Sedes y Consultorios
* **Categoría:** Consultorio Digital
* **Nivel de Resolución Inicial:** N1 / N2
* **Palabras Clave / Tags:** CRM, región, filial, efector, región 17, región 22, desalineación, consultorio, permisos

#### 1. Síntoma Reportado por el Usuario
"Error al intentar operar en una filial, consultorio físico o región asistencial específica."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Desalineación entre los atributos de Efector, Filial, Región administrativa (ej. Región 17 vs Región 22) y Estado en la base de datos de CRM.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Identificar la sede y efector donde el médico intenta atender y su perfil en el CRM.
2. **Acción de Resolución:** Validar con Administración Regional que el usuario tenga asignada la región exacta correspondiente al efector donde desea operar.
3. **Verificación de Éxito:** El prestador visualiza la agenda y consultorio habilitado para la sede requerida.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si la administración confirma la asignación pero la plataforma persiste con error, escalar a N2 para verificar sincronización batch del maestro.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Estamos regularizando la asignación de su perfil con la sede y región asistencial correspondiente. Una vez confirmada la vinculación administrativa, podrá operar con normalidad."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Validar coherencia de cuádrupla: `Efector - Filial - Región (ej. Región 17 vs 22) - Estado`. Sincronización batch nocturna entre CRM y MongoDB.
"""
    },
    {
        "code": "PDF-005",
        "title": "PDF-005: Descarga y Cifrado de Documentos Clínicos y Recetas - Diagnóstico Errores 404 y 400",
        "category": "Historia Clínica",
        "tags": "PDF, descarga, descargar receta, error al descargar receta, receta, receta digital, prescripción, error 404, error 400, hash, enlace presignado, 6 meses, GCS, consultorio-cifrado",
        "content": """### PDF-005: Descarga y Cifrado de Documentos Clínicos y Recetas - Diagnóstico Errores 404 y 400

* **Módulo / Subsistema:** consultorio-cifrado / Google Cloud Storage (GCS)
* **Categoría:** Historia Clínica
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** PDF, descarga, descargar receta, error al descargar receta, receta, receta digital, prescripción, error 404, error 400, hash, enlace presignado, 6 meses, GCS, consultorio-cifrado

#### 1. Síntoma Reportado por el Usuario
"Aparece un error 404 o 400 al intentar abrir o descargar el enlace de una prescripción, receta médica o estudio en PDF." o "Error al descargar receta."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
* **Error 404:** El archivo excedió los 6 meses de la política de retención activa en Google Cloud Storage (GCS) y ha sido purgado.
* **Error 400:** Hash criptográfico truncado o corrupto por copia incompleta del enlace por parte del usuario.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Solicitar al usuario el enlace que intenta abrir y verificar el código de error devuelto (404 o 400).
2. **Acción de Resolución:**
   * **Si es 404:** Verificar la fecha de emisión. Si supera 6 meses, informar que el enlace temporal expiró según normativa de retención.
   * **Si es 400:** Solicitar que copie y pegue la URL completa y sin cortes directamente desde el correo original.
3. **Verificación de Éxito:** El PDF se visualiza y descarga correctamente con los datos descifrados.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si un documento emitido hace menos de 6 meses arroja 404 con enlace completo, escalar a N2 para revisar el bucket de almacenamiento seguro en GCS.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Para error 400, por favor asegúrese de copiar la dirección completa del enlace desde el mensaje original sin omitir caracteres. Si el documento fue emitido hace más de 6 meses (error 404), su período de descarga directa ha caducado según las políticas de almacenamiento seguro."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `consultorio-cifrado`. Retención GCS: 6 meses. Los datos del documento permanecen ofuscados y protegidos hasta la validación completa del hash presignado.
"""
    },
    {
        "code": "MED-006",
        "title": "MED-006: Repositorio de Medicamentos y Receta Digital - Error 500 por Jurisdicción",
        "category": "Receta Digital",
        "tags": "receta, prescripción, error 500, jurisdicción, farmacia, receta-digital-backend, código numérico",
        "content": """### MED-006: Repositorio de Medicamentos y Receta Digital - Error 500 por Jurisdicción

* **Módulo / Subsistema:** receta-digital-backend / Repositorio Nacional de Prescripciones
* **Categoría:** Receta Digital
* **Nivel de Resolución Inicial:** N1 / N2
* **Palabras Clave / Tags:** receta, prescripción, error 500, jurisdicción, farmacia, receta-digital-backend, código numérico

#### 1. Síntoma Reportado por el Usuario
"Error 500 en pantalla al intentar emitir o confirmar una receta electrónica."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Ausencia del código numérico de jurisdicción provincial en el perfil del prestador dentro de la base de datos maestra.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Identificar al prestador emisor y verificar si su perfil tiene configurada la jurisdicción geográfica correspondiente.
2. **Acción de Resolución:** Actualizar el código numérico de jurisdicción en el sistema de origen (CRM/SISA) para habilitar la interoperabilidad con el repositorio farmacéutico.
3. **Verificación de Éxito:** La receta se emite con éxito y genera el identificador único de prescripción.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si el código de jurisdicción está presente y persiste el Error 500, escalar a N2 para revisar logs del microservicio `receta-digital-backend`.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Estamos actualizando la configuración de jurisdicción en su perfil profesional para habilitar la compatibilidad con el repositorio de recetas. En unos minutos podrá emitir sus prescripciones normalmente."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `receta-digital-backend`. Verificar campo `jurisdiction_id` en la entidad de prestador.
"""
    },
    {
        "code": "FORM-007",
        "title": "FORM-007: Formulario y Certificados - Validación Obligatoria de Diagnóstico RUSS",
        "category": "Historia Clínica",
        "tags": "formulario, evolución, certificado, RUSS, valor 0, bloqueo, consultorio-digital-forms, guardado",
        "content": """### FORM-007: Formulario y Certificados - Validación Obligatoria de Diagnóstico RUSS

* **Módulo / Subsistema:** consultorio-digital-forms / Cierre de Consulta HCE
* **Categoría:** Historia Clínica
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** formulario, evolución, certificado, RUSS, valor 0, bloqueo, consultorio-digital-forms, guardado

#### 1. Síntoma Reportado por el Usuario
"El botón de guardar queda bloqueado o el sistema rechaza la evolución/certificado médico al intentar cerrar la consulta."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Obligatoriedad del diagnóstico principal bajo estándar RUSS e incompatibilidad detectada en campos numéricos con valor "0" o evoluciones clínicas vacías.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Verificar si el médico completó tanto el diagnóstico como el texto de la evolución clínica.
2. **Acción de Resolución:** Indicar al médico que debe completar obligatoriamente el campo de diagnóstico RUSS y asegurarse de que el campo de evolución contenga texto descriptivo (no dejar en blanco ni con caracteres únicos).
3. **Verificación de Éxito:** El botón de firma y guardado se habilita en verde y la consulta queda registrada.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si todos los campos mandatorios están completos y la pantalla no avanza, derivar a N2 con captura del formulario.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Para habilitar el guardado de la atención, es indispensable seleccionar el diagnóstico principal (RUSS) e ingresar una descripción en la evolución clínica. Por favor corrobore estos campos y podrá cerrar la consulta con éxito."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `consultorio-digital-forms`. Validación estricta de esquema: `diagnosis_code` NOT NULL y `evolution_text.length > 5`.
"""
    },
    {
        "code": "NUT-008",
        "title": "NUT-008: Videoconsulta de Nutrición - Habilitación de Prestación 190173",
        "category": "Telemedicina",
        "tags": "nutrición, videoconsulta, 190173, 420296, especialidad 316, especialidad 317, proxy-reservas",
        "content": """### NUT-008: Videoconsulta de Nutrición - Habilitación de Prestación 190173

* **Módulo / Subsistema:** proxy-reservas / Módulo de Nutrición
* **Categoría:** Telemedicina
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** nutrición, videoconsulta, 190173, 420296, especialidad 316, especialidad 317, proxy-reservas

#### 1. Síntoma Reportado por el Usuario
"No se habilita la videoconsulta ni el botón de atender para profesionales de la especialidad de nutrición."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Falta de vinculación de la prestación SNOMED 190173 (Videoconsulta Nutrición) para las especialidades 316 y 317, o uso del código anterior obsoleto 420296.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Confirmar la especialidad del prestador (código 316 o 317) y el turno asignado.
2. **Acción de Resolución:** Verificar que el turno se encuentre registrado bajo el concepto 190173. Si fue agendado con el código anterior 420296, reasignar la prestación desde el sistema de reservas.
3. **Verificación de Éxito:** El botón de iniciar videoconsulta se activa de inmediato en el panel del nutricionista.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Escalar a N2 si el turno ya cuenta con la prestación 190173 pero el proxy no levanta la sesión.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Estamos actualizando la prestación de su turno al código vigente de videoconsulta nutricional (190173). La sala quedará disponible en instantes para que pueda atender a su paciente."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `proxy-reservas`. Mapeo obligatorio: Especialidades 316 y 317 -> SNOMED 190173. Código anterior deprecado: 420296.
"""
    },
    {
        "code": "CON-009",
        "title": "CON-009: Tiempos de Espera y Reconexión en Videoconsulta - Manejo de Sockets",
        "category": "Telemedicina",
        "tags": "spinner eterno, reconexión, socket, timeout, consultorio-digital-cliente, loop reintentos",
        "content": """### CON-009: Tiempos de Espera y Reconexión en Videoconsulta - Manejo de Sockets

* **Módulo / Subsistema:** consultorio-digital-cliente / Conectividad WebRTC
* **Categoría:** Telemedicina
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** spinner eterno, reconexión, socket, timeout, consultorio-digital-cliente, loop reintentos

#### 1. Síntoma Reportado por el Usuario
"La pantalla muestra un ícono de carga girando de forma continua ('spinner eterno') al intentar ingresar a la videoconsulta."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Bucle de reintentos generado por falla de apertura en el WebSocket de señalización o inestabilidad transitoria del enlace.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Consultar si el usuario lleva más de 60 segundos esperando la conexión.
2. **Acción de Resolución:** El sistema cuenta con un límite de 5 reintentos automáticos. Instruir al usuario a refrescar la pestaña del navegador (Ctrl+F5) o salir de la sala e ingresar nuevamente.
3. **Verificación de Éxito:** El WebSocket se reestablece y el usuario ingresa a la sala virtual.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si múltiples pacientes y médicos reportan el spinner de carga al mismo tiempo, reportar como posible caída del servicio de WebSockets a N3.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"El sistema está reintentando establecer el enlace de su sala. Si la espera supera un minuto, por favor refresque su navegador con las teclas Ctrl+F5 o vuelva a presionar el enlace de ingreso para reanudar la comunicación."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `consultorio-digital-cliente`. Límite de reintentos frontend: 5 ciclos de sondeo antes del fallback a reconexión manual.
"""
    },
    {
        "code": "BIO-010",
        "title": "BIO-010: Biometría y Validación OTP - Requisitos de Seguridad IPS y Ministerio",
        "category": "Contingencias",
        "tags": "biometría, OTP, token, seguridad, ministerio de salud, IPS, iam-integration, validación sesión",
        "content": """### BIO-010: Biometría y Validación OTP - Requisitos de Seguridad IPS y Ministerio

* **Módulo / Subsistema:** iam-integration / Ministerio de Salud / Seguridad IPS
* **Categoría:** Contingencias
* **Nivel de Resolución Inicial:** N1
* **Palabras Clave / Tags:** biometría, OTP, token, seguridad, ministerio de salud, IPS, iam-integration, validación sesión

#### 1. Síntoma Reportado por el Usuario
"El sistema solicita reiteradamente validar la identidad mediante código OTP o validación biométrica al ingresar o atender."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Requerimiento de seguridad obligatorio dispuesto por el Ministerio de Salud para el acceso a datos sensibles de salud. El enrolamiento biométrico es de registro único, mientras que el código de un solo uso (OTP) es exigido por cada sesión activa.

#### 3. Guía de Acción Paso a Paso para el Analista de Soporte
1. **Validación:** Confirmar si el médico completó el enrolamiento biométrico inicial y si está recibiendo el SMS/correo con el OTP.
2. **Acción de Resolución:** Aclarar al profesional que la solicitud de OTP es una exigencia legal de protección de datos clínicos por sesión. Si no recibe el código, verificar y actualizar su número de teléfono celular en el maestro de usuarios.
3. **Verificación de Éxito:** El médico ingresa el código OTP recibido y accede a su panel asistencial.

#### 4. Criterio de Escalamiento a N2 / N3 (Si aplica)
Si el gateway de SMS no entrega los códigos OTP a nivel general, escalar de urgencia a N2/Seguridad.

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"La validación mediante código OTP es un requerimiento regulatorio y de seguridad obligatorio del Ministerio de Salud para salvaguardar la privacidad de las historias clínicas. Por favor ingrese el código que le llegó por mensaje para continuar con su atención."

#### 6. Datos Técnicos / Queries de Backoffice (Solo para N2 / N3)
Microservicio: `iam-integration`. Biometría: Enrolamiento único persistido en backend. OTP: Expiración de 5 minutos por sesión activa.
"""
    },
    {
        "code": "CD2-SSOT-001",
        "title": "CD2-SSOT-001: Manual Maestro y Biblia de Datos CD2 - Verdad Única y Scripts N2/N3",
        "category": "Consultorio Digital",
        "tags": "Biblia de datos, SSOT, verdad única, MongoDB, scripts N2, scripts N3, baja lógica, isDeleted, prefijo Dr, SAP, CRM, SISA",
        "content": """### CD2-SSOT-001: Manual Maestro y Biblia de Datos CD2 - Verdad Única y Scripts N2/N3

* **Módulo / Subsistema:** Arquitectura CD2 / Gobernanza de Datos Maestros / SSOT
* **Categoría:** Consultorio Digital
* **Nivel de Resolución Inicial:** N2 / N3
* **Palabras Clave / Tags:** Biblia de datos, SSOT, verdad única, MongoDB, scripts N2, scripts N3, baja lógica, isDeleted, prefijo Dr, SAP, CRM, SISA

#### 1. Síntoma Reportado por el Usuario
"Deriva de datos (Data Drift), inconsistencia entre SAP/CRM y MongoDB, o necesidad de intervención autorizada de soporte avanzado en base de datos."

#### 2. Diagnóstico Técnico para el Analista (Causa Raíz)
Desalineación de información entre los sistemas corporativos de origen y el almacenamiento local de CD2, requiriendo aplicar las reglas de Verdad Única (SSOT) o ejecutar los procedimientos operativos autorizados en MongoDB.

#### 3. Matriz de Verdad Única (SSOT) y Frecuencias
* **Socio / Paciente:** Origen en `IAM / CRM` -> Destino en `MongoDB Local` (Tiempo Real / Sincronización Diaria).
* **Prestador / Médico:** Origen en `SISA / CRM / IAM` -> Destino en `MongoDB Local` (Batch Nocturno / Real-Time).
* **Institución / Consultorio:** Origen en `SAP / Extranet` -> Destino en `MongoDB Local` (Batch Diario).
* **Seguridad y Acceso:** Origen en `AFIP / IAM` -> Destino en `Sesión Activa` (Por Evento de Login/OTP).

#### 4. Repositorio Oficial de Scripts Autorizados para Soporte N2 / N3 (MongoDB)
Las siguientes operaciones son las **únicas intervenciones manuales autorizadas** en la base de datos de CD2:

1. **Baja Lógica de Consultorios / Instituciones (Gobernanza de Integridad):**
   Inhabilita la institución sin eliminar los registros históricos de atención:
   ```javascript
   db.institutions.updateOne(
     { _id: ObjectId("ID_INSTITUCION") },
     { $set: { isDeleted: true } }
   )
   ```

2. **Inhabilitación de Acceso de Emergencia por IC:**
   El prefijo "1000" bloquea inmediatamente el acceso del profesional en el microservicio de autenticación:
   ```javascript
   db.practitioners.updateOne(
     { ic: "IC_MEDICO" },
     { $set: { icPractitioner: "1000" + "IC_MEDICO" } }
   )
   ```

3. **Actualización de Datos de Contacto de Institución:**
   ```javascript
   db.institutions.updateOne(
     { _id: ObjectId("ID_INSTITUCION") },
     { $set: { contact: "NUEVO_TELEFONO_O_MAIL" } }
   )
   ```

#### 5. Respuesta Sugerida que el Analista debe brindar al Usuario
"Se ha validado la consistencia de los datos maestros en la plataforma central. La actualización ha quedado regularizada conforme a los estándares de integridad y trazabilidad del sistema."

#### 6. Especificación del Payload Técnico para Escalado Silencioso (Deflection Bot)
Al transferir a N2/N3, el bot captura obligatoriamente:
* `IC`: Identificador de Consulta único.
* `CUIT/CUIL`: Identificación fiscal del prestador.
* `User-Agent`: Navegador y OS del puesto de trabajo.
* `Room ID / Hash de Turno`: Identificador único de la sala en Jitsi.
* `Console Logs`: Captura de errores y excepciones frontend previas.
* `Timestamp`: Fecha y hora exacta con precisión de milisegundos.
"""
    }
]

def ingest_master_articles():
    print(f"Iniciando ingesta de {len(ARTICLES_DATA)} articulos del Manual Maestro Consolidado...")
    with Session(engine) as session:
        created = 0
        updated = 0
        for item in ARTICLES_DATA:
            code = item["code"]
            title = item["title"]
            category = item["category"]
            tags = item["tags"]
            content = item["content"]

            existing = session.exec(
                select(KBArticle).where(
                    (KBArticle.title == title) |
                    (KBArticle.title.like(f"{code}:%")) |
                    (KBArticle.title.like(f"[{code}]%"))
                )
            ).first()

            if existing:
                existing.title = title
                existing.category = category
                existing.tags = tags
                existing.content = content
                existing.author_username = "Arquitectura CD2"
                existing.version = "v2.0-ManualMaestro"
                existing.changelog = "Homologación con Manual Maestro Consolidado CD2 - Verdad Única"
                existing.space_name = "Runbooks de Soporte"
                existing.is_published = True
                existing.updated_at = datetime.utcnow()
                session.add(existing)
                updated += 1
            else:
                new_art = KBArticle(
                    title=title,
                    category=category,
                    tags=tags,
                    content=content,
                    author_username="Arquitectura CD2",
                    version="v2.0-ManualMaestro",
                    changelog="Alta desde Manual Maestro Consolidado CD2 - Verdad Única",
                    space_name="Runbooks de Soporte",
                    view_count=15,
                    requests_deflected=8,
                    helpful_score=99,
                    is_published=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(new_art)
                created += 1

        session.commit()
        print(f"Manual Maestro Ingestado: {created} nuevos creados, {updated} actualizados.")

if __name__ == "__main__":
    ingest_master_articles()
