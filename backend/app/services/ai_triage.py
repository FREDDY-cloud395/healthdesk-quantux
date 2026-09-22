# -*- coding: utf-8 -*-
"""
Motor Pericial de Análisis Cognitivo N3 & Triage Asistencial Inteligente
Rol: Ingeniero de Producto & Analista Funcional N3 Digitalizado
QuantUX v4 - HealthTech ServiceDesk
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from app.db.session import engine
from app.models.entities import Ticket, KBArticle, SupportLevel, TicketStatus

class N3CognitiveTriageEngine:
    """
    Motor analítico que emula el razonamiento pericial de un Ingeniero de Producto
    y Analista Funcional de N3. Cruza síntomas en lenguaje natural con la base de
    conocimiento de CD2, la matriz de interoperabilidad (SAP, CRM, IAM, Turnos, PAU)
    y la casuística de tickets resueltos históricamente en producción.
    """

    @staticmethod
    def analyze_incident(
        query_text: str,
        user_role: str = "SOLICITANTE",
        user_fullname: str = "Profesional de la Salud",
        platform_code: str = "CD2"
    ) -> Dict[str, Any]:
        """
        Ejecuta el análisis cognitivo N3 sobre el texto ingresado.
        Devuelve el análisis pericial, la resolución recomendada y el dictamen técnico forense.
        """
        query_lower = query_text.lower().strip()
        
        # 1. Recuperación de conocimiento pericial en base de datos
        matched_articles = []
        with Session(engine) as session:
            all_articles = session.exec(select(KBArticle)).all()
            for art in all_articles:
                score = 0
                searchable = f"{art.title} {art.tags or ''} {art.category} {art.content}".lower()
                
                # Evaluación de términos clave
                words = [w for w in re.split(r'\W+', query_lower) if len(w) > 3]
                for w in words:
                    if w in searchable:
                        score += 1
                if score > 0:
                    matched_articles.append((score, art))
            
            matched_articles.sort(key=lambda x: x[0], reverse=True)
            top_articles = [art for score, art in matched_articles[:3]]

            # 2. Búsqueda de tickets históricos análogos resueltos
            resolved_tickets = session.exec(
                select(Ticket)
                .where(Ticket.status.in_([TicketStatus.RESUELTO, TicketStatus.CERRADO]))
                .order_by(Ticket.created_at.desc())
            ).all()

            similar_tickets = []
            for t in resolved_tickets:
                t_score = 0
                t_search = f"{t.title} {t.description} {t.resolution_notes or ''}".lower()
                for w in words:
                    if w in t_search:
                        t_score += 1
                if t_score >= 2:
                    similar_tickets.append(t)
                if len(similar_tickets) >= 3:
                    break

        # 3. Razonamiento Pericial y Deducción de Causa Raíz N3
        subsystem = "Consultorio Digital"
        root_cause = "Consulta asistencial estándar en plataforma clínica"
        recommended_action = "Aplicar procedimiento estándar de soporte"
        escalation_circuit = "Mesa de Ayuda N1"
        confidence_score = 85
        solution_steps = []
        requires_pau = False

        # Definición de variables para la resolución unificada de 3 líneas
        resolution_text = ""

        # Reglas Heurísticas Especiales de Fallback (Evaluadas primero para máxima precisión y cero mezcla de temas)
        # Regla Heurística Especial: OSDEPYM
        if "osdepym" in query_lower:
            subsystem = "Nomenclador de Obras Sociales (OSDEPYM)"
            root_cause = "Búsqueda por sigla de obra social bajo nueva razón social."
            resolution_text = "El nomenclador permite buscar por la sigla 'OSDEPYM' o 'Obra Social de Empresarios, Profesionales y Monotributistas de Argentina'."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Actualizar padrón de obras sociales en la base de datos de la plataforma."

        # Regla Heurística Especial: Nutrición
        elif any(k in query_lower for k in ["nutricion", "nutrición", "190173", "420296"]):
            subsystem = "Módulo de Nutrición y Coberturas"
            root_cause = "Rechazo de prestación activa 190173 en atenciones de nutrición virtual."
            resolution_text = "Recargue la pantalla (F5) para aplicar el fix de validación o registre la prestación '420296' por fuera del sistema."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Revisar logs de rechazo de prestación de nutrición y aplicar reintento en base de datos."

        # Regla Heurística Especial: Cambiar datos o mail del paciente (El médico no lo puede solucionar)
        elif any(p in query_lower for p in ["paciente"]) and any(k in query_lower for k in ["mail", "email", "correo", "teléfono", "telefono", "celular", "modificar", "cambiar", "datos"]):
            subsystem = "Servicio de Datos Maestros de Pacientes"
            root_cause = "Modificación de datos de contacto del paciente."
            resolution_text = "Por motivos de seguridad, los profesionales no poseen permisos para editar los datos de contacto del paciente."
            escalation_circuit = "Soporte Técnico N1 -> Gestión de Afiliados / Pacientes"
            recommended_action = "Actualizar datos de contacto del paciente en el maestro de afiliados bajo solicitud formal validada."

        # Regla Heurística 1: Matrículas SISA / CRM
        elif any(k in query_lower for k in ["matrícula", "matricula", "sisa", "crm", "bloquead"]):
            subsystem = "Gestión de Matrículas (SISA / CRM)"
            root_cause = "Discrepancia de matrícula configurada frente a registros activos en SISA."
            resolution_text = "Ingrese su matrícula en el menú de HCE para desbloquear el selector o corrobore su estado habilitado en SISA."
            escalation_circuit = "MDA-Aplicaciones N1 -> Especialistas N2 CRM/SISA"
            recommended_action = "Verificar estado REFEPS y aplicar query de contingencia en defaultMatricula si hay prescripción pendiente."

        # Regla Heurística 2: Videoconsulta / Jitsi / Permisos / Conectividad
        elif any(k in query_lower for k in ["video", "cámara", "camara", "micrófono", "microfono", "jitsi", "llamada", "spinner", "jointimeout", "conectar"]):
            subsystem = "Motor WebRTC de Videoconsulta (Jitsi Core)"
            root_cause = "Permisos de periféricos multimedia bloqueados o tiempo de sincronización WebRTC agotado."
            resolution_text = "Permita el acceso a Cámara/Micrófono desde el candado de la URL o refresque la pantalla (F5) si el spinner no carga."
            escalation_circuit = "Soporte N1 Comunicaciones WebRTC"
            recommended_action = "Validar telemetría de socket WebRTC y verificar ancho de banda del prestador."

        # Regla Heurística 3: SNOMED CT / Laboratorios
        elif any(k in query_lower for k in ["laboratorio", "snomed", "estudio", "hepatograma", "hiv", "analisis", "análisis", "orina"]):
            subsystem = "Nomenclador Semántico de Estudios (SNOMED CT)"
            root_cause = "Búsqueda por término coloquial no indexado en la descripción canónica de SNOMED CT."
            resolution_text = "Ingrese únicamente las primeras 4 letras de la práctica o use sinónimos comunes entre paréntesis."
            escalation_circuit = "Analista Funcional N3 - Terminología Médica"
            recommended_action = "Mapear término coloquial al código de concepto SNOMED correspondiente en el catálogo local."

        # Regla Heurística 4: PDFs / Documentos 404 / 400
        elif any(k in query_lower for k in ["pdf", "descarga", "404", "400", "vencido", "archivo", "adjunto", "hash"]):
            subsystem = "Servicio Criptográfico de Almacenamiento Seguro (Bucket)"
            root_cause = "Expiración de la retención de documentos (404) o truncamiento del hash de URL (400)."
            resolution_text = "Los documentos expiran a los 6 meses (Error 404). Haga clic directo en el enlace del correo para evitar cortar el hash (Error 400)."
            escalation_circuit = "Mesa de Ayuda N1 - Plataforma de Almacenamiento"
            recommended_action = "Regenerar token temporal presignado con hash SHA-256 verificado."

        # Regla Heurística 5: Datos Maestros / Nombres / SAP / IAM / Turnos
        elif any(k in query_lower for k in ["nombre", "apellido", "iam", "videoconsulta nombre", "cartilla", "prefijo", "dr", "lic", "contrato"]):
            subsystem = "Matriz de Interoperabilidad (IAM / Turnos / CRM Contratos)"
            root_cause = "Desalineación entre la fuente maestra de identidad (IAM) y la tabla transaccional de turnos."
            resolution_text = "Su nombre proviene de IAM para la web, o de Cartilla Médica para la videollamada; errores requieren ticket de corrección."
            escalation_circuit = "MDA-Aplicaciones N1 -> Derivación a IAM / CRM"
            recommended_action = "Abrir ticket de corrección de identidad hacia IAM adjuntando comprobante de matrícula y DNI."

        # Regla Heurística Especial: Baja o Modificación de Consultorio/Sede
        elif any(k in query_lower for k in ["consultorio", "sede", "baja"]):
            subsystem = "Configuración de Consultorios y Sedes"
            root_cause = "Solicitud de baja lógica o modificación de sede activa."
            resolution_text = "La baja de un consultorio requiere aplicar isDeleted = true y cambios de dirección requieren actualización en base de datos."
            escalation_circuit = "Soporte Operativo N1 -> Especialistas Cartilla"
            recommended_action = "Aplicar baja lógica (isDeleted) o modificar datos de sede en la base de datos."

        # Regla Heurística Especial: Mail del profesional y Notificaciones
        elif any(k in query_lower for k in ["mail", "email", "correo", "notificacion", "notificación"]):
            subsystem = "Servicio de Notificaciones del Profesional"
            root_cause = "Casilla de correo del profesional desactualizada o notificaciones no recibidas."
            resolution_text = "Modifique su correo de mensajería ingresando directamente a la Extranet de Prestadores (Mis Datos)."
            escalation_circuit = "Soporte Operativo N1 -> Especialistas Cartilla"
            recommended_action = "Verificar casilla principal en Cartilla Médica y validar despacho de notificaciones."

        # Regla Heurística Especial: Extranet
        elif "extranet" in query_lower:
            subsystem = "Autenticación de Extranet de Prestadores (IAM)"
            root_cause = "Credenciales incorrectas, bloqueo de usuario o falta de sincronización en el portal."
            resolution_text = "Intente ingresar usando modo incógnito, verifique que su usuario esté activo o use la opción de recuperar contraseña."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Validar estado del usuario en IAM y blanquear contraseña si es necesario."

        # Regla Heurística Especial: Saludos / Mensajes de cortesía
        elif any(k == query_lower.strip() or query_lower.strip().startswith(k + " ") for k in ["hola", "buenos dias", "buenos días", "buenas tardes", "buenas noches", "saludos", "buen dia", "buen día"]):
            subsystem = "Asistente de Consulta"
            root_cause = "Saludo de cortesía o consulta general de bienvenida."
            resolution_text = "¡Hola! Por favor indique su consulta de soporte o seleccione una de las opciones de ejemplo sugeridas."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Guiar al profesional para que formule su consulta específica de soporte técnico."

        # Regla Heurística Especial: Diagnóstico
        elif any(k in query_lower for k in ["diagnóstico", "diagnostico"]):
            subsystem = "Motor de Validaciones Clínicas"
            root_cause = "Omisión o error en la codificación del Diagnóstico Principal CIE-10 / SNOMED CT."
            resolution_text = "Seleccione un diagnóstico principal codificado del listado desplegable para habilitar el botón 'Finalizar Atención'."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Instruir al profesional sobre la carga obligatoria del diagnóstico codificado para habilitar firma."

        # Regla Heurística Especial: Certificados Médicos
        elif "certificado" in query_lower:
            subsystem = "Módulo de Certificados Médicos"
            root_cause = "Validación de campo numérico de días de reposo o firma de certificado."
            resolution_text = "En certificados que no indican días de reposo, deje el campo numérico completamente vacío para evitar errores."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Instruir al profesional sobre dejar vacíos los días de reposo en certificados sin licencia."

        # Regla Heurística Especial: Cierre de Consulta
        elif any(k in query_lower for k in ["cerrar", "finalizar", "evolución", "evolucion"]):
            subsystem = "Cierre de Consulta y Guardado de Evolución"
            root_cause = "Omisión de campos mandatorios (evolución escrita o diagnóstico principal) para la firma de la consulta."
            resolution_text = "Asegúrese de haber completado tanto la evolución escrita como el diagnóstico principal sin alertas rojas en el formulario."
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Validar integridad del formulario de consulta y destrabar guardado lógico si es necesario."

        # Si no coincidió con ninguna regla heurística, consultar la Base de Conocimiento (KBArticle) si la coincidencia es fuerte (score >= 2)
        else:
            best_match = matched_articles[0] if matched_articles else None
            if best_match and best_match[0] >= 2:
                top_art = best_match[1]
                subsystem = top_art.category or "Consultorio Digital"
                if subsystem.endswith(" (CD2)"):
                    subsystem = subsystem[:-6]
                root_cause = f"Guía homologada: '{top_art.title}'"
                
                # Extraer pasos del contenido del artículo
                content_snippets = [
                    line.strip() for line in top_art.content.split("\n")
                    if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("|") and len(line.strip()) > 15
                ]
                if content_snippets:
                    resolution_text = " ".join(content_snippets[:2])
                else:
                    resolution_text = f"Siga el procedimiento estándar documentado en la guía de asistencia '{top_art.title}'."
                escalation_circuit = "Mesa de Ayuda N1"
                recommended_action = f"Aplicar procedimiento homologado según guía N3: {top_art.title}"
            else:
                if top_articles:
                    top_art = top_articles[0]
                    subsystem = top_art.category or "Consultorio Digital"
                    if subsystem.endswith(" (CD2)"):
                        subsystem = subsystem[:-6]
                    root_cause = f"Guía pericial identificada: '{top_art.title}'"
                    
                    content_snippets = [
                        line.strip() for line in top_art.content.split("\n")
                        if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("|") and len(line.strip()) > 15
                    ]
                    if content_snippets:
                        resolution_text = " ".join(content_snippets[:2])
                    else:
                        resolution_text = f"Siga el procedimiento estándar documentado en la guía de asistencia '{top_art.title}'."
                    escalation_circuit = "Mesa de Ayuda N1"
                    recommended_action = f"Aplicar procedimiento homologado según guía N3: {top_art.title}"
                else:
                    subsystem = "Soporte Técnico General"
                    root_cause = "Consulta fuera de las casuísticas conocidas por el motor."
                    resolution_text = "No dispongo de información sobre esta consulta específica. Por favor, contacte a nuestro equipo de soporte."
                    escalation_circuit = "Mesa de Ayuda N1"
                    recommended_action = "Derivar a soporte técnico general para su análisis y resolución personalizada."

        # Construcción de la respuesta fluida, empática y pericial (Estrictamente de 3 líneas exactas de texto para cumplir con la norma de soporte)
        line1 = f"**Diagnóstico:** {root_cause}"
        line2 = f"**Resolución:** {resolution_text}"
        line3 = "**Soporte:** Si la dificultad persiste, contacte a soporte técnico para asistencia personalizada."
        formatted_response = f"{line1}\n{line2}\n{line3}"

        # Generación del Dictamen Técnico Forense N3 para el Ticket
        forensic_report = (
            f"=== DICTAMEN TÉCNICO PERICIAL DE ANÁLISIS FUNCIONAL N3 ===\n"
            f"• Fecha de Análisis: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"• Analista: Ingeniero de Producto / N3 Cognitive Engine\n"
            f"• Síntoma Reportado: {query_text}\n"
            f"• Subsistema Afectado: {subsystem}\n"
            f"• Causa Raíz Diagnosticada: {root_cause}\n"
            f"• Circuito de Escalamiento / Destino: {escalation_circuit}\n"
            f"• Acción Técnica Recomendada: {recommended_action}\n"
        )
        if similar_tickets:
            forensic_report += f"• Casuística Análoga Previa: {', '.join([t.id for t in similar_tickets])}\n"
        if top_articles:
            forensic_report += f"• Artículos SOP de Referencia: {', '.join([a.title for a in top_articles])}\n"
        forensic_report += "=========================================================="

        return {
            "subsystem": subsystem,
            "root_cause": root_cause,
            "recommended_action": recommended_action,
            "escalation_circuit": escalation_circuit,
            "ai_response_text": formatted_response,
            "forensic_report": forensic_report,
            "suggested_priority": "P2" if any(w in query_lower for w in ["bloquead", "caida", "caída", "error 500", "urgente"]) else "P3",
            "suggested_platform": platform_code,
            "similar_ticket_ids": [t.id for t in similar_tickets],
            "top_articles": [{"id": a.id, "title": a.title, "category": a.category} for a in top_articles]
        }
