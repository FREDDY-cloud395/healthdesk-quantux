# -*- coding: utf-8 -*-
"""
Fuente Oficial Lote 3: Matriz Maestra de Datos por Entidad (Socio, Prestador, Consultorio),
Protocolos de Flujo de Datos, Librería Técnica MongoDB y Glosario Oficial de CD2.
Suministrado por la Supervisión Funcional de CD2.
"""

MATRIZ_MAESTRA_ARTICLES = [
    {
        "code": "CD2-SOC-001",
        "title": "CD2-SOC-001: Módulo Socio - Persistencia de Datos de Contacto y Reclamos de Notificaciones no Recibidas",
        "category": "Consultorio Digital",
        "tags": "contacto de socio, socio, paciente, afiliado, datos de contacto, notificaciones no recibidas, mail de socio, telefono de paciente, cache de socios, sap, turno especifico",
        "content": """### CD2-SOC-001: Módulo Socio - Persistencia de Datos de Contacto y Reclamos de Notificaciones no Recibidas

* **Módulo / Subsistema:** Socio (Paciente/Afiliado) / SAP Caché / Servicio de Socios / Turnos
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** contacto de socio, socio, paciente, afiliado, datos de contacto, notificaciones no recibidas, mail de socio, telefono de paciente, cache de socios, sap, turno especifico

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"contacto de socio" / "El paciente reclama que no le llegan las notificaciones de los turnos" / "Inconsistencia en los datos de contacto o cobertura del afiliado"

#### 2. Diagnóstico y Causa Raíz
La consistencia de los datos del afiliado es fundamental para la validez de las prescripciones y la facturación. La sincronización con SAP y la Caché de Socios garantiza que la información sea fidedigna al momento de la prestación (Nombre, Apellido, Nro Socio OSDE, DNI, Plan, Género, Fecha de Nacimiento).
Regla Crítica de Persistencia de Contacto: El paciente se crea automáticamente en el primer turno utilizando el mail y teléfono cargados en esa instancia. Sin embargo, para turnos posteriores, el sistema prioriza los datos de contacto cargados específicamente para ese turno. Ante reclamos de notificaciones no recibidas, el MDA debe verificar los datos del turno específico y no solo los del perfil base del paciente.

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el turno específico objeto del reclamo de notificación.
2. Verificar los datos de contacto (email y teléfono) registrados puntualmente en el objeto appointment del turno correspondiente.
3. Contrastar dichos datos contra el perfil base del afiliado en Caché de Socios (SAP) / Servicio de Socios.
4. Si la inconsistencia corresponde a datos maestros de cobertura o plan, tramitar la actualización disparada por la notificación de novedades de SAP.
5. Si el mail o teléfono del turno estaban desactualizados, informar al paciente que la notificación se envió a dicho contacto y actualizar los datos para turnos posteriores.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Hemos verificado los datos de contacto registrados para el turno en cuestión para asegurar que las notificaciones lleguen a la casilla y teléfono correspondientes. Para turnos futuros, los datos de contacto quedan regularizados."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Origen del dato por campo:
- Nombre, Apellido, Nro Socio OSDE, Género: Sincronización automática con SAP al solicitar/recargar turnos.
- DNI: Sincronización automática validada contra base local.
- Plan: Novedades de SAP.
- Fecha de Nacimiento: Frontend en solicitud de turno.
Circuito de derivación: Inconsistencias en datos de socios o planes de cobertura se derivan a SAP/Caché de Socios.
"""
    },
    {
        "code": "CD2-SEDE-001",
        "title": "CD2-SEDE-001: Módulo Consultorio - Mail de Sede, Teléfono y Protocolos de Baja / Inhabilitación por IC",
        "category": "Consultorio Digital",
        "tags": "mail de consultorio, correo consultorio, contacto de consultorio, telefono consultorio, email sede, institucion, baja logica, inhabilitacion por ic, prefijo 1000, mongodb, activia, sale and brick, terminal",
        "content": """### CD2-SEDE-001: Módulo Consultorio - Mail de Sede, Teléfono y Protocolos de Baja / Inhabilitación por IC

* **Módulo / Subsistema:** Consultorio (Sede Física/Institución) / Turnos / CRM / MongoDB institutions
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** mail de consultorio, correo consultorio, contacto de consultorio, telefono consultorio, email sede, institucion, baja logica, inhabilitacion por ic, prefijo 1000, mongodb, activia, sale and brick, terminal

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"mail de consultorio" / "Necesitamos cambiar el correo o teléfono de la sede/consultorio" / "Inhabilitar sede por IC" / "Consultorio dado de baja"

#### 2. Diagnóstico y Causa Raíz
La precisión logística depende de la correcta configuración de las sedes.
- Campos Críticos: Dirección, Teléfono y Email se originan en Turnos/CRM. El email es el configurado en Cartilla/Extranet.
- Operador (CRM): Entidades como Activia o Sale & Brick.
- Terminal (CRM): Asignada según la configuración del contrato.
- Reglas de Estado: Se debe distinguir claramente entre la baja operativa (baja lógica con isDeleted: true) y la inhabilitación sistémica administrativa por IC (aplicación de la lógica prefijo 1000 + IC).

#### 3. Procedimiento de Resolución Paso a Paso
1. Identificar el _id del consultorio/sede en la colección institutions.
2. Para actualización de contacto (teléfono y email): ejecutar la plantilla MongoDB autorizada:
   db.institutions.updateOne({ "_id": ObjectId("ID_CONSULTORIO") }, { $set: { "telephone": "NUEVO_TEL", "email": "NUEVO_MAIL" } })
3. Validar que el nuevo correo coincida con el registrado en Cartilla/Extranet.
4. Para inhabilitación administrativa por IC (bloqueo total): aplicar la plantilla MongoDB con prefijo 1000:
   db.institutions.updateOne({ "externalId": "1000" + IC_PRESTADOR }, { $set: { "isDeleted": true } })
5. Validar desde la aplicación que la sede figure actualizada o debidamente inhabilitada.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos actualizando los datos de contacto y correo del consultorio para que la información reflejada en Cartilla y Consultorio Digital sea consistente."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Diferenciar siempre una sede eliminada operativamente (isDeleted: true) de una inhabilitada administrativamente (1000 + IC).
Toda discrepancia en asignación de Operador (Activia, Sale & Brick) o Terminal contractual debe escalarse a CRM.
"""
    },
    {
        "code": "CD2-PREST-002",
        "title": "CD2-PREST-002: Identidad de Prestador, Prefijos Profesionales y Reglas de Matrícula CABA/PBA (Padding CRM)",
        "category": "Consultorio Digital",
        "tags": "nombre en web, videoconsulta, crm, iam, padding matricula, roxana fuentes, matricula caba, matricula buenos aires, prefijo dr lic, contratos",
        "content": """### CD2-PREST-002: Identidad de Prestador, Prefijos Profesionales y Reglas de Matrícula CABA/PBA (Padding CRM)

* **Módulo / Subsistema:** Prestador (Médico/Profesional) / CRM / IAM / Turnos / MongoDB appointments
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** nombre en web, videoconsulta, crm, iam, padding matricula, roxana fuentes, matricula caba, matricula buenos aires, prefijo dr lic, contratos

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"El nombre del médico en la web no coincide con el de la videoconsulta" / "Duplicidad de prestador en CRM" / "Error de matrícula CABA o Provincia de Buenos Aires (padding)" / "Falta prefijo Dr. o Lic."

#### 2. Diagnóstico y Causa Raíz
Existe una distinción técnica obligatoria entre la identidad pública y la identidad de firma legal:
- Nombre en Web (IAM): Nombre de fantasía o visualización que el socio ve en la plataforma.
- Nombre en Videoconsulta (CRM/Turnos): Nombre legal que debe aparecer en toda documentación y recetas.
- CUIT (AFIP): Validado para procesos fiscales.
- Gestión de Matrículas y Duplicidad (Caso Roxana Fuentes): Para evitar errores de duplicidad en CRM cuando los IC no están unificados, se deben aplicar las siguientes reglas de relleno (padding):
  * Matrícula CABA: Agregar un cero (0) a la izquierda (Ej: 0334271).
  * Matrícula Buenos Aires: Agregar un uno (1) al final (Ej: 1276161).
- Atributos Profesionales: El prefijo (Dr./Lic.) se basa en la configuración de CRM/Contratos. Si el campo está vacío, no se deben forzar valores por defecto para no invalidar el título del profesional.

#### 3. Procedimiento de Resolución Paso a Paso
1. Determinar el ámbito de la discrepancia de nombre: si es visualización web, canalizar a IAM; si es documentación legal/recetas, canalizar a CRM.
2. Para duplicidad de matrículas en CRM cuando los IC no están unificados: aplicar regla de relleno (padding CABA: 0 a la izquierda; padding Buenos Aires: 1 al final).
3. Para corrección de prefijos en turnos ya agendados: ejecutar la plantilla MongoDB autorizada:
   db.appointments.updateMany({ "professional.ic": IC_PRESTADOR, "status": "scheduled" }, { $set: { "professional.prefix": "NUEVO_PREFIJO" } })
4. Si el prefijo en CRM/Contratos está vacío, respetar el campo vacío sin forzar valores por defecto.
5. Validar que la visualización y las recetas reflejen los datos contractuales correctos.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Estamos ajustando la configuración de identidad y matrícula del profesional para garantizar la total consistencia legal en recetas y turnos."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Circuito de escalamiento inteligente:
- IAM: Problemas de mail de login o correcciones de Nombre en Web -> derivar a N1-Aplicaciones para que estos escalen al equipo de IAM.
- CRM: Discrepancias en matrículas, prefijos, regiones o asignación de Operador/Terminal.
"""
    },
    {
        "code": "CD2-ESC-001",
        "title": "CD2-ESC-001: Circuito de Derivación Inteligente por Subsistema y Atenciones Modulares (DW)",
        "category": "Consultorio Digital",
        "tags": "derivacion inteligente, escalar, circuito de derivacion, iam, crm, sap cache, atencion modular, demanda espontanea, nec-6838, nec-6836, dw",
        "content": """### CD2-ESC-001: Circuito de Derivación Inteligente por Subsistema y Atenciones Modulares (DW)

* **Módulo / Subsistema:** Arquitectura / Flujo de Datos / Data Warehouse / IAM / CRM / SAP
* **Categoría:** Consultorio Digital
* **Palabras Clave / Tags:** derivacion inteligente, escalar, circuito de derivacion, iam, crm, sap cache, atencion modular, demanda espontanea, nec-6838, nec-6836, dw

#### 1. Síntoma Reportado (Lenguaje del Usuario)
"Circuito de derivación inteligente de incidentes" / "A qué equipo corresponde escalar según el error" / "Extracción de atenciones modulares para Data Warehouse"

#### 2. Diagnóstico y Causa Raíz
Protocolos de flujo de datos y reglas de gobierno del soporte CD2:
1. Circuito de Derivación Inteligente:
   - IAM: Problemas de mail de login o correcciones de Nombre en Web. El MDA debe derivar a N1-Aplicaciones para que estos escalen al equipo de IAM.
   - CRM: Discrepancias en matrículas, prefijos, regiones o asignación de Operador/Terminal.
   - SAP/Caché: Inconsistencias en datos de socios o planes de cobertura.
2. Ingesta e Indexación: Vinculada a proyectos NEC-6838 (Consultorio Digital) o NEC-6836 (Business Intelligence) para trazabilidad en DW.
3. Consumo de Vistas para Atenciones Modulares (demanda espontánea sin cita previa, appointment: null): La información se extrae de la vista de atenciones mediante servicio GET con parámetros date_from y date_to en formato ISO 8601 (YYYY-MM-DDTHH:mm:ssZ). Los datos de Filial y Contrato viajan en el nodo institution por fuera del nodo appointment.

#### 3. Procedimiento de Resolución Paso a Paso
1. Tipificar el origen del incidente según la matriz de derivación por subsistema (IAM, CRM, SAP/Caché).
2. Derivar al circuito correspondiente:
   - Mail de login / Nombre en Web -> N1-Aplicaciones hacia IAM.
   - Matrículas / Prefijos / Operador / Terminal -> CRM.
   - Datos de socios / Coberturas / Planes -> SAP / Caché de Socios.
3. Para consultas no indexadas o sin procedimiento estandarizado:
   Escalar la consulta a Análisis Funcional o para análisis por parte de Desarrollo.
4. Para requerimientos de DW sobre atenciones modulares: validar parámetros de fecha ISO 8601 y lectura del nodo institution.

#### 4. Mensaje Sugerido para Responder al Médico (Tono Empático y No Técnico)
"Su consulta ha sido derivada al equipo especializado responsable del subsistema para su correspondiente intervención y seguimiento."

#### 5. Notas Técnicas para Soporte N2 / N3 (Opcional)
Vigencia y Mantenimiento: Cualquier cambio en la lógica de los sistemas periféricos (SAP, CRM, IAM) requiere actualización de esta especificación para mantener la integridad de la Fuente de Verdad.
"""
    }
]
