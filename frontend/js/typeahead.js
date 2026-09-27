// -*- coding: utf-8 -*-
/**
 * Módulo de Búsqueda Predictiva Oficial (Typeahead) para Quantux CD2
 * Conecta los 38 Runbooks y Casos Oficiales en tiempo real directamente con el operador.
 */

const KB_OFFICIAL_TOPICS = [
  // 1-23: Casos Operativos Reales CD2
  {
    code: "CD2-MAT-001",
    title: "Prestador sin matrículas visibles en CD (Matrículas: 0 en JSON vs SISA habilitado)",
    query: "matricula no aparece en CD pero figura habilitada en SISA",
    category: "Consultorio Digital",
    keywords: ["matricula", "sisa", "refeps", "matriculas 0", "no aparece matricula", "matricula vacia", "auditor"]
  },
  {
    code: "CD2-MAT-002",
    title: "Matrícula en SISA pero no disponible para seleccionar al generar un turno",
    query: "matricula visible en SISA no aparece disponible para seleccionar turno",
    category: "Consultorio Digital",
    keywords: ["turno", "matricula", "seleccionar matricula", "agenda", "fecha", "no disponible"]
  },
  {
    code: "CD2-PREST-001",
    title: "Cambio de CUIT de prestador manteniendo la información asociada",
    query: "cambio de cuit manteniendo la informacion asociada",
    category: "Consultorio Digital",
    keywords: ["cuit", "cambiar cuit", "cambio de cuit", "prestador", "baja usuario", "cartilla", "historial"]
  },
  {
    code: "CD2-NUT-001",
    title: "Videoconsulta Nutrición: Prestación 190173 en nomenclador (Especialidades 316/317)",
    query: "videoconsulta nutricion prestacion 190173 especialidades 316 y 317",
    category: "Consultorio Digital",
    keywords: ["nutricion", "190173", "420296", "especialidad 316", "especialidad 317", "nomenclador", "prestacion", "proxy-reservas"]
  },
  {
    code: "CD2-LAB-001",
    title: "Prestación de laboratorio sin codificación SNOMED (Reemplazo NNO por http://snomed.info/sct)",
    query: "laboratorio sin codificacion snomed reemplazar nno",
    category: "Historia Clínica",
    keywords: ["laboratorio", "snomed", "nno", "snomed ct", "estudio", "http://snomed.info/sct"]
  },
  {
    code: "CD2-USR-001",
    title: "Corrección del correo electrónico asociado al usuario en MongoDB (telecom)",
    query: "correccion de correo electronico telecom en mongodb",
    category: "Contingencias",
    keywords: ["correo", "mail", "cambio de mail", "cambiar correo", "telecom", "mongodb", "user"]
  },
  {
    code: "CD2-INST-001",
    title: "Alta y configuración de prestador con validación del circuito de agenda",
    query: "alta de prestador y validacion de circuito de agenda",
    category: "Consultorio Digital",
    keywords: ["alta prestador", "configurar prestador", "circuito agenda", "cartilla", "agenda", "matricula"]
  },
  {
    code: "CD2-PAU-001",
    title: "Error al registrar una consulta (Atención Rechazada y Registro por Diferido)",
    query: "error al registrar consulta registro por diferido atencion rechazada",
    category: "Historia Clínica",
    keywords: ["diferido", "registro por diferido", "rechazo", "no puedo registrar", "consulta rechazada", "error al registrar"]
  },
  {
    code: "CD2-PAU-002",
    title: "Prestador correctamente identificado pero operación rechazada en plataforma",
    query: "operacion rechazada con prestador correctamente identificado",
    category: "Contingencias",
    keywords: ["operacion rechazada", "rechazo", "prestador identificado", "rechazo plataforma"]
  },
  {
    code: "CD2-INC-001",
    title: "Rechazo de operación con infraestructura local aparentemente operativa",
    query: "rechazo de operacion con infraestructura local operativa",
    category: "Contingencias",
    keywords: ["infraestructura local", "terminal operativa", "rechazo operacion"]
  },
  {
    code: "SOPORTE-GCP-001",
    title: "Análisis de solicitudes mediante logs (GCP Logs, Kibana, Apigee, Jira)",
    query: "analisis de solicitudes mediante logs en gcp y kibana",
    category: "Contingencias",
    keywords: ["gcp logs", "kibana", "apigee", "logs", "correlacion", "trazabilidad"]
  },
  {
    code: "CD2-DB-001",
    title: "Baja lógica de usuario/prestador (isDeleted: true en MongoDB)",
    query: "baja logica usuario prestador mongodb isDeleted",
    category: "Contingencias",
    keywords: ["baja logica", "isDeleted", "eliminar usuario", "eliminar prestador", "mongodb"]
  },
  {
    code: "PRESC-001",
    title: "Validación de nomencladores para prestaciones especiales (Nutrición y Laboratorio)",
    query: "validacion de nomencladores para prestaciones especiales",
    category: "Receta Digital",
    keywords: ["nomenclador", "prestaciones especiales", "receta", "prescripcion"]
  },
  {
    code: "TEL-001",
    title: "Incidentes de videoconsulta (Cámara, Micrófono, Audio, Permisos de Navegador)",
    query: "problemas de camara microfono o audio en videoconsulta",
    category: "Telemedicina",
    keywords: ["camara", "microfono", "audio", "videoconsulta", "permisos", "webrtc"]
  },
  {
    code: "IAM-001",
    title: "Correo principal del prestador (telecom con system: email en IAM)",
    query: "cambio de mail de login o correo principal del prestador en IAM",
    category: "Contingencias",
    keywords: ["mail de login", "correo principal", "iam", "credenciales", "login prestador"]
  },
  {
    code: "SOPORTE-001",
    title: "Clasificación y escalamiento de incidentes (Mesa de Ayuda N1 / N2 / N3 y Soporte Operativo)",
    query: "clasificacion y escalamiento de incidentes mesa de ayuda",
    category: "Contingencias",
    keywords: ["escalamiento", "soporte operativo", "mesa de ayuda", "n1", "n2", "n3", "horarios"]
  },
  {
    code: "KB-001",
    title: "Evidencia mínima para escalar un incidente (Usuario, Operación, Timestamp, Error, Logs)",
    query: "evidencia minima requerida para escalar un incidente",
    category: "Contingencias",
    keywords: ["evidencia minima", "escalar ticket", "captura", "payload", "timestamp", "logs"]
  },
  {
    code: "DOC-001",
    title: "Descarga de documentación clínica en PDF (Links presignados y visualización)",
    query: "error al descargar documentacion clinica pdf o receta",
    category: "Historia Clínica",
    keywords: ["descargar pdf", "descarga", "documentacion clinica", "receta pdf", "links presignados"]
  },
  {
    code: "DOC-002",
    title: "Documento clínico fuera del período de retención (Retención 6 meses en GCS)",
    query: "documento clinico fuera de periodo de retencion 6 meses gcs",
    category: "Historia Clínica",
    keywords: ["retencion 6 meses", "gcs", "documento vencido", "periodo de retencion", "404 retencion"]
  },
  {
    code: "PRESC-002",
    title: "Firma digital y validación criptográfica de recetas",
    query: "firma digital y validacion criptografica de recetas",
    category: "Receta Digital",
    keywords: ["firma digital", "certificado", "token", "criptografia", "receta"]
  },
  {
    code: "PRESC-003",
    title: "Contingencia de receta offline / código de barras",
    query: "contingencia de receta offline o codigo de barras",
    category: "Contingencias",
    keywords: ["receta offline", "codigo de barras", "contingencia receta"]
  },
  {
    code: "IAM-002",
    title: "Modificación de datos sensibles de afiliados (Fuente maestra SAP / CRM / IAM)",
    query: "modificacion de datos sensibles de afiliados y validacion de fuentes",
    category: "Contingencias",
    keywords: ["datos sensibles", "afiliados", "modificar paciente", "sap", "crm", "fuente maestra"]
  },
  {
    code: "IAM-003",
    title: "Diferencia entre datos del prestador y datos del paciente",
    query: "diferencia entre datos de contacto del prestador y del paciente",
    category: "Contingencias",
    keywords: ["datos prestador", "datos paciente", "confusion de contacto", "contacto prestador"]
  },

  // 24-33: Escenarios Críticos MAT-001 a BIO-010
  {
    code: "MAT-001",
    title: "Módulo de Matrículas: Selectores Bloqueados en Consultorio Digital (v3.9.0)",
    query: "selectores de matricula bloqueados en consultorio digital",
    category: "Consultorio Digital",
    keywords: ["selector bloqueado", "selectores bloqueados", "desbloquear selector", "matricula bloqueada", "v3.9.0"]
  },
  {
    code: "VID-002",
    title: "Videoconsulta Jitsi: Latencia de Servidores San Pablo y Parámetros de Red",
    query: "pantalla blanca o latencia en videoconsulta jitsi servidores san pablo",
    category: "Telemedicina",
    keywords: ["jitsi", "pantalla blanca", "latencia", "san pablo", "jointimeout", "webrtc"]
  },
  {
    code: "SNM-003",
    title: "Servidor Terminológico SNOMED CT: Mapeo de Términos Coloquiales vs Técnicos",
    query: "servidor terminologico snomed ct lenguaje coloquial",
    category: "Historia Clínica",
    keywords: ["snomed", "snomed ct", "terminologico", "lenguaje coloquial", "diagnostico", "ips"]
  },
  {
    code: "REG-004",
    title: "Integración CRM y Conciliación de Regiones / Filiales (Región 17 vs 22)",
    query: "discrepancia de region crm filial 17 vs 22",
    category: "Consultorio Digital",
    keywords: ["crm", "region", "filial", "region 17", "region 22", "efector"]
  },
  {
    code: "PDF-005",
    title: "Descarga y Cifrado de Documentos Clínicos y Recetas: Errores 404 y 400",
    query: "error 404 o 400 en descarga de recetas y documentos cifrados",
    category: "Historia Clínica",
    keywords: ["404", "400", "error 404", "error 400", "hash corrupto", "retencion", "cifrado", "receta"]
  },
  {
    code: "MED-006",
    title: "Repositorio de Medicamentos y Receta Digital: Error 500 por Jurisdicción",
    query: "error 500 en receta digital por codigo de jurisdiccion de medicamentos",
    category: "Receta Digital",
    keywords: ["error 500", "jurisdiccion", "medicamentos", "receta digital", "vademecum"]
  },
  {
    code: "FORM-007",
    title: "Formulario y Certificados: Validación Obligatoria de Diagnóstico RUSS (Valor '0')",
    query: "validacion obligatoria diagnostico russ en formularios y certificados",
    category: "Historia Clínica",
    keywords: ["russ", "diagnostico russ", "formulario", "certificado", "valor 0", "evolucion vacia"]
  },
  {
    code: "NUT-008",
    title: "Videoconsulta de Nutrición: Habilitación de Prestación 190173 (Especialidades 316 y 317)",
    query: "habilitacion de prestacion 190173 para nutricion especialidades 316 y 317",
    category: "Telemedicina",
    keywords: ["nutricion 190173", "prestacion 190173", "190173", "especialidad 316", "especialidad 317", "proxy-reservas"]
  },
  {
    code: "CON-009",
    title: "Tiempos de Espera y Reconexión en Videoconsulta: Manejo de Sockets y Spinner Eterno",
    query: "spinner eterno o reconexion de sockets en videoconsulta",
    category: "Telemedicina",
    keywords: ["spinner eterno", "reconexion", "sockets", "timeout", "loop", "5 reintentos"]
  },
  {
    code: "BIO-010",
    title: "Biometría y Validación OTP: Requisitos de Seguridad IPS y Ministerio de Salud",
    query: "biometria y validacion otp token ips ministerio",
    category: "Contingencias",
    keywords: ["biometria", "otp", "token", "ips", "ministerio", "seguridad"]
  },

  // 34-38: Biblia de Datos SSOT y Casos Estructurales
  {
    code: "CD2-SSOT-001",
    title: "Manual Maestro y Biblia de Datos CD2: Verdad Única y Scripts N2/N3",
    query: "scripts de soporte n2 n3 mongodb verdad unica cd2",
    category: "Consultorio Digital",
    keywords: ["biblia de datos", "ssot", "verdad unica", "mongodb", "scripts n2", "scripts n3", "baja logica"]
  },
  {
    code: "CD2-SOC-001",
    title: "Módulo Socio: Persistencia de Contacto y Reclamos de Notificaciones no Recibidas",
    query: "notificaciones no recibidas persistencia de contacto socio 1er turno",
    category: "Consultorio Digital",
    keywords: ["notificaciones no recibidas", "persistencia de contacto", "contacto socio", "mail socio", "telefono socio", "sap cache", "1er turno"]
  },
  {
    code: "CD2-SEDE-001",
    title: "Módulo Consultorio: Mail de Sede, Teléfono e Inhabilitación por IC (Prefijo 1000)",
    query: "inhabilitar sede por IC prefijo 1000 o mail de consultorio",
    category: "Consultorio Digital",
    keywords: ["inhabilitar sede", "prefijo 1000", "1000 + ic", "mail consultorio", "correo sede", "telefono consultorio", "activia", "sale and brick"]
  },
  {
    code: "CD2-PREST-002",
    title: "Identidad de Prestador, Prefijos Dr/Lic y Reglas de Matrícula CABA/PBA (Padding Roxana Fuentes)",
    query: "padding de matricula caba pba caso roxana fuentes y prefijos",
    category: "Consultorio Digital",
    keywords: ["padding", "roxana fuentes", "matricula caba", "matricula buenos aires", "prefijo dr", "prefijo lic", "nombre en web", "nombre en videoconsulta"]
  },
  {
    code: "CD2-ESC-001",
    title: "Circuito de Derivación Inteligente (IAM/CRM/SAP) y Atenciones Modulares DW",
    query: "circuito de derivacion inteligente iam crm sap o atenciones modulares dw",
    category: "Consultorio Digital",
    keywords: ["derivacion inteligente", "atencion modular", "demanda espontanea", "dw", "data warehouse", "nec-6838", "nec-6836", "get date_from"]
  },

  // 39-47: Lote 1 Funcional CD2 (Vistas DW, Matrículas SISA, Alta CD, No Socios, Registraciones, Errores Medicamentos, Psicopatología Virtual)
  {
    code: "CD2-DW-001",
    title: "Adecuación de Vistas DW: Desacople de Consultorio (institution) y Turno (appointment) para Filial y Contrato",
    query: "desacople de institution y appointment en vistas dw filial contrato",
    category: "Data Warehouse / Vistas",
    keywords: ["vistas dw", "dw", "institution", "appointment", "desacople", "filial", "contrato", "atencion modular", "recetas", "indicaciones", "evoluciones"]
  },
  {
    code: "CD2-DW-002",
    title: "Adecuación de Vistas DW: Construcción de Vista Atenciones e Indicadores Fuera de Consulta",
    query: "vista atenciones data warehouse indicadores demandas espontaneas y prescripciones fuera de consulta",
    category: "Data Warehouse / Vistas",
    keywords: ["vista atenciones", "indicadores dw", "socios unicos", "fuera de consulta", "demanda espontanea", "medicationrequest", "imageservicerequest", "practiceservicerequest", "labservicerequest", "note", "certificate"]
  },
  {
    code: "CD2-SISA-001",
    title: "Restricción Regulatoria SISA: Eliminación de CRM, Bloqueo de Prescripción (01/06) y 8 Escenarios del Selector",
    query: "restriccion de matriculas sisa baja crm y bloqueo de prescripcion 01/06",
    category: "Matrículas / SISA",
    keywords: ["sisa", "matricula sisa", "matriculas crm", "baja crm", "bloqueo 01/06", "prescribir", "receta bloqueada", "selector matricula", "refeps@msal.gov.ar", "escenarios selector"]
  },
  {
    code: "CD2-ALTA-001",
    title: "Optimización del Flujo de Alta de Prestador en CD: Menú Lateral, Justificación Celular/Email y Transición de Sala de Espera",
    query: "flujo de alta prestador menu lateral justificacion celular whatsapp email bienvenida",
    category: "Onboarding / Alta Prestador",
    keywords: ["alta prestador", "alta consultorio digital", "menu lateral", "mis datos", "tuerca", "celular whatsapp", "correo no compartido", "enlace primer login", "cartillas", "sala de espera a consultorio digital"]
  },
  {
    code: "CD2-NOSOC-001",
    title: "Pacientes No Socios en CD: Atención Integral, Branding Neutro, Bloqueo Filiatorio Obligatorio y Restricciones",
    query: "paciente no socio bloqueo filiatorio primera atencion branding neutro",
    category: "Pacientes No Socios",
    keywords: ["no socio", "paciente no socio", "otra cobertura", "branding neutro", "bloqueo datos filiatorios", "primera atencion", "desde aca", "editar datos", "restricciones psicopatologia nutricion fonoaudiologia"]
  },
  {
    code: "CD2-NOSOC-002",
    title: "Pacientes No Socios en CD: Arquitectura Dual, Recetas INNOVAMED sin Diagnóstico, API Render y MongoDB Atlas",
    query: "arquitectura no socios recetas innovamed sin diagnostico api render mongodb atlas",
    category: "Pacientes No Socios / Arquitectura",
    keywords: ["innovamed", "receta no socios", "recetas sin diagnostico", "ofuscacion diagnostico", "mongodb atlas", "render api", "registro de salud dual", "jitsi osde", "jitsi quantux"]
  },
  {
    code: "CD2-REG-001",
    title: "Módulo Registraciones: Exposición Multirregistro OK, Consolidación de Rechazos, Estado 'Sin Registraciones' y Regla Virtual",
    query: "visualizar todas las registraciones ok consolidacion de rechazos esta atencion no tiene registraciones asociadas",
    category: "Registración de Prestaciones",
    keywords: ["modulo registraciones", "todas las registraciones", "registrado ok", "consolidacion rechazos", "420296 rechazada", "anular prestacion", "esta atencion no tiene registraciones asociadas", "validado ok", "regla virtual maximo 1"]
  },
  {
    code: "CD2-MED-001",
    title: "Manejo de Errores del Repositorio de Medicamentos: Clasificación en 3 Categorías, Reenvío 5xx vs Reemisión",
    query: "manejo de errores repositorio medicamentos reenvio 500 al 599 o reemision credencial 11 caracteres",
    category: "Prescripción / Repositorio Medicamentos",
    keywords: ["repositorio de medicamentos", "receta no generada", "error 500", "error 599", "credencial 11 caracteres", "socio inexistente", "reenviar receta atenciones realizadas", "nueva receta medicamentos", "alfabeta"]
  },
  {
    code: "CD2-PSICO-001",
    title: "Registro de Prestaciones en Psicopatología Virtual: Restricción a Lista Cerrada (330384, 330385, 330386)",
    query: "limite de prestacion en virtuales de psicopatologia codigos 330384 330385 330386",
    category: "Psicopatología / Prestaciones Virtuales",
    keywords: ["psicopatologia virtual", "prestaciones virtuales psicopatologia", "330384", "330385", "330386", "entrevista de orientacion on line", "terapia individual on line", "control farmacologico on line"]
  },
  {
    code: "CD2-IPS-001",
    title: "Info del Paciente en Atención (IPS): Registro de Alergias e Intolerancias, Catálogo SNOMED y Validación de Duplicados",
    query: "registro de alergias e intolerancias catalogo snomed validacion duplicados carrito atencion",
    category: "Historia Clínica / IPS",
    keywords: ["alergia", "alergias", "intolerancia", "intolerancias", "snomed", "snomed ct", "duplicado", "alergia ya cargada", "carrito atencion", "clinicalstatus", "verificationstatus", "active", "confirmed", "ips"]
  },
  {
    code: "CD2-IPS-002",
    title: "Interoperabilidad RUSS: Envío FHIR AllergyIntolerance ($register) desde Consultorio Digital",
    query: "interoperabilidad russ envio fhir allergyintolerance register interlocutor comercial ic",
    category: "Interoperabilidad / RUSS",
    keywords: ["russ", "fhir", "allergyintolerance", "$register", "interlocutor comercial", "ic", "russ-facade", "appname", "allergyid", "recordeddate", "sincronizacion russ"]
  },
  {
    code: "CD2-IPS-003",
    title: "Info del Paciente en Atención (IPS): Variables Antropométricas (Peso/Estatura), Cálculo de IMC y Cabecera Dinámica",
    query: "variables antropometricas peso estatura calculo de imc cabecera dinamica registro de salud",
    category: "Consultorio Digital / IPS",
    keywords: ["antropometria", "peso", "estatura", "talla", "imc", "indice de masa corporal", "peso kg", "estatura cm", "cabecera dinamica", "colapsada", "desplegada", "read-only", "solo lectura"]
  },
  {
    code: "CD2-IPS-004",
    title: "Restricción de Aplicabilidad IPS: Exclusión Taxativa de Especialidades de Psicología (23 Códigos) y Fonoaudiología (305)",
    query: "exclusion de especialidades ips psicologia 23 codigos y fonoaudiologia 305 no aparece alergias ni antropometria",
    category: "Consultorio Digital / Especialidades",
    keywords: ["psicologia", "fonoaudiologia", "305", "319", "810", "841", "850", "870", "926", "927", "893", "894", "1026", "1024", "1025", "1027", "especialidad excluida", "no aparece alergias", "no aparece peso", "exclusion taxativa", "ips"]
  }
];

function normalizeText(text) {
  return (text || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();
}

function searchKbOfficialTopics(rawQuery) {
  const qNorm = normalizeText(rawQuery);
  if (!qNorm || qNorm.length < 2) return [];

  const words = qNorm.split(/\s+/).filter(w => w.length > 1);

  const scored = [];
  KB_OFFICIAL_TOPICS.forEach(item => {
    let score = 0;
    const codeNorm = normalizeText(item.code);
    const titleNorm = normalizeText(item.title);
    const catNorm = normalizeText(item.category);
    const kwNorm = item.keywords.map(k => normalizeText(k));

    if (codeNorm.includes(qNorm)) score += 120;
    if (titleNorm.includes(qNorm)) score += 80;

    words.forEach(w => {
      if (codeNorm.includes(w)) score += 40;
      if (titleNorm.includes(w)) score += 25;
      if (catNorm.includes(w)) score += 15;
      kwNorm.forEach(kw => {
        if (kw.includes(w)) score += 30;
      });
    });

    if (score > 0) {
      scored.push({ item, score });
    }
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, 6).map(s => s.item);
}

// Variables de estado para navegación accesible del Typeahead
let requesterTypeaheadSelectedIndex = -1;
let requesterTypeaheadMatches = [];

// Manejo del Typeahead para el Portal del Solicitante / Médico
function handleRequesterTypeahead(val) {
  const dropdown = document.getElementById('requester-typeahead-dropdown');
  if (!dropdown) return;

  const matches = searchKbOfficialTopics(val);
  requesterTypeaheadMatches = matches;
  requesterTypeaheadSelectedIndex = -1;

  if (matches.length === 0) {
    dropdown.style.display = 'none';
    dropdown.innerHTML = '';
    return;
  }

  let html = `
    <div style="padding: 6px 12px; background: #F8FAFC; border-bottom: 1px solid #E2E8F0; font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; position: sticky; top: 0; z-index: 10;">
      Temas Oficiales Homologados de Consultorio Digital 2:
    </div>
  `;

  matches.forEach((m, idx) => {
    html += `
      <div id="requester-typeahead-item-${idx}" onclick="selectRequesterTypeahead('${encodeURIComponent(m.query)}')" style="padding: 10px 14px; border-bottom: 1px solid #F1F5F9; cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 10px; transition: background 0.15s ease;" onmouseover="highlightRequesterTypeaheadItem(${idx})" onmouseout="this.classList.remove('typeahead-item-highlighted')">
        <div style="display: flex; align-items: center; gap: 8px; overflow: hidden;">
          <span style="font-size: 10.5px; font-weight: 800; background: rgba(0, 168, 150, 0.1); color: #00A896; border: 1px solid rgba(0, 168, 150, 0.25); padding: 2px 7px; border-radius: 6px; white-space: nowrap;">
            ${m.code}
          </span>
          <span style="font-size: 12.5px; color: #1E293B; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${m.title}
          </span>
        </div>
        <span style="font-size: 11px; color: #94A3B8; white-space: nowrap;">
          ${m.category}
        </span>
      </div>
    `;
  });

  dropdown.innerHTML = html;
  dropdown.style.display = 'block';
}

function highlightRequesterTypeaheadItem(idx) {
  requesterTypeaheadSelectedIndex = idx;
  const dropdown = document.getElementById('requester-typeahead-dropdown');
  if (!dropdown) return;
  const items = dropdown.querySelectorAll('[id^="requester-typeahead-item-"]');
  items.forEach((el, i) => {
    if (i === idx) {
      el.classList.add('typeahead-item-highlighted');
      el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    } else {
      el.classList.remove('typeahead-item-highlighted');
    }
  });
}

function handleRequesterTypeaheadKeydown(event) {
  const dropdown = document.getElementById('requester-typeahead-dropdown');
  if (!dropdown || dropdown.style.display === 'none' || requesterTypeaheadMatches.length === 0) {
    return false;
  }

  if (event.key === 'ArrowDown') {
    event.preventDefault();
    let nextIdx = requesterTypeaheadSelectedIndex + 1;
    if (nextIdx >= requesterTypeaheadMatches.length) nextIdx = 0;
    highlightRequesterTypeaheadItem(nextIdx);
    return true;
  }

  if (event.key === 'ArrowUp') {
    event.preventDefault();
    let prevIdx = requesterTypeaheadSelectedIndex - 1;
    if (prevIdx < 0) prevIdx = requesterTypeaheadMatches.length - 1;
    highlightRequesterTypeaheadItem(prevIdx);
    return true;
  }

  if (event.key === 'Enter') {
    if (requesterTypeaheadSelectedIndex >= 0 && requesterTypeaheadSelectedIndex < requesterTypeaheadMatches.length) {
      event.preventDefault();
      const selected = requesterTypeaheadMatches[requesterTypeaheadSelectedIndex];
      selectRequesterTypeahead(encodeURIComponent(selected.query));
      return true;
    }
  }

  if (event.key === 'Escape') {
    event.preventDefault();
    dropdown.style.display = 'none';
    requesterTypeaheadSelectedIndex = -1;
    return true;
  }

  return false;
}

function selectRequesterTypeahead(encodedQuery) {
  const query = decodeURIComponent(encodedQuery);
  const input = document.getElementById('requester-chat-input');
  const dropdown = document.getElementById('requester-typeahead-dropdown');
  if (dropdown) dropdown.style.display = 'none';
  requesterTypeaheadSelectedIndex = -1;
  if (input) {
    input.value = query;
    if (typeof sendRequesterChatMessage === 'function') {
      sendRequesterChatMessage();
    }
  }
}

// Manejo del Typeahead para la Base de Conocimiento (Chat Operador)
function handleKbTypeahead(val) {
  const dropdown = document.getElementById('kb-typeahead-dropdown');
  if (!dropdown) return;

  const matches = searchKbOfficialTopics(val);
  if (matches.length === 0) {
    dropdown.style.display = 'none';
    dropdown.innerHTML = '';
    return;
  }

  let html = `
    <div style="padding: 6px 12px; background: #F8FAFC; border-bottom: 1px solid #E2E8F0; font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">
      Temas Oficiales Homologados de Consultorio Digital 2:
    </div>
  `;

  matches.forEach((m, idx) => {
    html += `
      <div onclick="selectKbTypeahead('${encodeURIComponent(m.query)}')" style="padding: 10px 14px; border-bottom: 1px solid #F1F5F9; cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 10px; transition: background 0.15s ease;" onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='#FFFFFF'">
        <div style="display: flex; align-items: center; gap: 8px; overflow: hidden;">
          <span style="font-size: 10.5px; font-weight: 800; background: #E8F0FE; color: #1A73E8; padding: 2px 7px; border-radius: 6px; white-space: nowrap;">
            ${m.code}
          </span>
          <span style="font-size: 12.5px; color: #1E293B; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${m.title}
          </span>
        </div>
        <span style="font-size: 11px; color: #94A3B8; white-space: nowrap;">
          ${m.category}
        </span>
      </div>
    `;
  });

  dropdown.innerHTML = html;
  dropdown.style.display = 'block';
}

function selectKbTypeahead(encodedQuery) {
  const query = decodeURIComponent(encodedQuery);
  const input = document.getElementById('kb-ai-chat-input');
  const dropdown = document.getElementById('kb-typeahead-dropdown');
  if (dropdown) dropdown.style.display = 'none';
  if (input) {
    input.value = query;
    if (typeof submitKbAiQuestion === 'function') {
      submitKbAiQuestion();
    }
  }
}

// Cierre automático al hacer clic afuera
document.addEventListener('click', function(e) {
  const reqDrop = document.getElementById('requester-typeahead-dropdown');
  const reqInput = document.getElementById('requester-chat-input');
  if (reqDrop && reqInput && !reqDrop.contains(e.target) && e.target !== reqInput) {
    reqDrop.style.display = 'none';
  }

  const kbDrop = document.getElementById('kb-typeahead-dropdown');
  const kbInput = document.getElementById('kb-ai-chat-input');
  if (kbDrop && kbInput && !kbDrop.contains(e.target) && e.target !== kbInput) {
    kbDrop.style.display = 'none';
  }
});

// Exportar explícitamente a window
window.handleRequesterTypeahead = handleRequesterTypeahead;
window.selectRequesterTypeahead = selectRequesterTypeahead;
window.handleRequesterTypeaheadKeydown = handleRequesterTypeaheadKeydown;
window.highlightRequesterTypeaheadItem = highlightRequesterTypeaheadItem;
window.handleKbTypeahead = handleKbTypeahead;
window.selectKbTypeahead = selectKbTypeahead;
window.KB_OFFICIAL_TOPICS = KB_OFFICIAL_TOPICS;
