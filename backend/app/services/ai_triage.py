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
        subsystem = "Consultorio Digital 2 (CD2)"
        root_cause = "Consulta asistencial estándar en plataforma clínica"
        recommended_action = "Aplicar procedimiento estándar de soporte"
        escalation_circuit = "Mesa de Ayuda N1"
        confidence_score = 85
        solution_steps = []
        requires_pau = False

        # Regla Heurística 1: Matrículas SISA / CRM
        if any(k in query_lower for k in ["matrícula", "matricula", "sisa", "crm", "bloquead"]):
            subsystem = "Gestión de Matrículas (SISA / CRM)"
            root_cause = "Discrepancia entre matrícula configurada por defecto e inhabilitada frente a matrículas activas registradas en SISA, o inconsistencia en CRM por ICs duplicados."
            solution_steps = [
                "1. **Verificación en Pantalla:** El sistema compara automáticamente su matrícula por defecto. Si posee otra matrícula habilitada en diferente jurisdicción o especialidad, el menú desplegable de matrícula se desbloqueará para su selección manual.",
                "2. **Estado en SISA:** Compruebe que la matrícula figure con estado 'Habilitada' en el Registro Federal de Profesionales de Salud (REFEPS/SISA).",
                "3. **Contingencia N3:** Si persiste bloqueada, un analista de soporte aplicará la replicación de matrícula activa hacia defaultMatricula o gestionará la unificación de Identificador Comercial (IC)."
            ]
            escalation_circuit = "MDA-Aplicaciones N1 -> Especialistas N2 CRM/SISA"
            recommended_action = "Verificar estado REFEPS y aplicar query de contingencia en defaultMatricula si hay prescripción pendiente."

        # Regla Heurística 2: Videoconsulta / Jitsi / Permisos / Conectividad
        elif any(k in query_lower for k in ["video", "cámara", "camara", "micrófono", "microfono", "jitsi", "llamada", "spinner", "jointimeout", "conectar"]):
            subsystem = "Motor WebRTC de Videoconsulta (Jitsi Core)"
            root_cause = "Tiempo de espera de sincronización WebRTC agotado (joinTimeout) o permisos de periféricos multimedia bloqueados en el navegador local."
            solution_steps = [
                "1. **Permisos del Navegador:** Haga clic en el ícono de candado junto a la URL del navegador y asegúrese de que Cámara y Micrófono estén en 'Permitir'.",
                "2. **Reconexión Automática:** La plataforma ejecuta 5 reintentos transparentes cada 20 segundos. Si observa el indicador de carga por más de 1 minuto, refresque la página (F5).",
                "3. **Protección de Sesión:** Evite cerrar la pestaña sin confirmar en el cuadro de diálogo para no desconectar involuntariamente al paciente en espera."
            ]
            escalation_circuit = "Soporte N1 Comunicaciones WebRTC"
            recommended_action = "Validar telemetría de socket WebRTC y verificar ancho de banda del prestador."

        # Regla Heurística 3: SNOMED CT / Laboratorios
        elif any(k in query_lower for k in ["laboratorio", "snomed", "estudio", "hepatograma", "hiv", "analisis", "análisis", "orina"]):
            subsystem = "Nomenclador Semántico de Estudios (SNOMED CT)"
            root_cause = "Búsqueda por término coloquial no indexado textualmente en la descripción canónica de SNOMED CT."
            solution_steps = [
                "1. **Búsqueda por Raíz:** Ingrese únicamente las primeras 4 letras de la práctica (por ejemplo, 'hepa' para Pruebas de Función Hepática, o 'inmuno' para HIV).",
                "2. **Sinónimos Homologados:** Se han incorporado las descripciones cotidianas entre paréntesis para facilitar la prescripción ambulatoria.",
                "3. **Solicitud de Incorporación:** Si requiere un panel específico no listado, indíquelo al soporte para incorporar el código SNOMED en la próxima versión."
            ]
            escalation_circuit = "Analista Funcional N3 - Terminología Médica"
            recommended_action = "Mapear término coloquial al código de concepto SNOMED correspondiente en el catálogo local."

        # Regla Heurística 4: PDFs / Documentos 404 / 400
        elif any(k in query_lower for k in ["pdf", "descarga", "404", "400", "vencido", "archivo", "adjunto", "hash"]):
            subsystem = "Servicio Criptográfico de Almacenamiento Seguro (Bucket)"
            root_cause = "Expiración de la política de retención de 6 meses en bucket de almacenamiento (Error 404) o truncamiento de la cadena del hash en la URL (Error 400)."
            solution_steps = [
                "1. **Si el error es 404:** Los documentos con más de 6 meses de emisión son depurados por política de retención. Debe solicitarse una nueva prescripción digital actualizada.",
                "2. **Si el error es 400:** No copie y pegue la dirección web manualmente; haga clic directo en el enlace del correo para evitar cortar el hash de seguridad.",
                "3. **Regeneración:** El equipo de soporte puede emitir un nuevo enlace firmado temporal con hash validado."
            ]
            escalation_circuit = "Mesa de Ayuda N1 - Plataforma de Almacenamiento"
            recommended_action = "Regenerar token temporal presignado con hash SHA-256 verificado."

        # Regla Heurística 5: Datos Maestros / Nombres / SAP / IAM / Turnos
        elif any(k in query_lower for k in ["nombre", "apellido", "iam", "videoconsulta nombre", "cartilla", "prefijo", "dr", "lic", "contrato"]):
            subsystem = "Matriz de Interoperabilidad (IAM / Turnos / CRM Contratos)"
            root_cause = "Desalineación entre la fuente maestra de identidad (IAM en web) versus la tabla transaccional de Turnos/CRM (en videollamada)."
            solution_steps = [
                "1. **En la Web de CD2:** Su nombre proviene del sistema central de identidades (IAM). Si contiene un error, se genera un ticket para corrección en IAM.",
                "2. **En la Videoconsulta:** El nombre se toma del servicio de Turnos/CRM. La actualización se solicita formalmente al equipo de Contratos y CRM.",
                "3. **Prefijo (Dr./Lic.):** Está regulado para respetar campos vacíos y evitar valores forzados; su actualización se gestiona en Cartilla Médica."
            ]
            escalation_circuit = "MDA-Aplicaciones N1 -> Derivación a IAM / CRM"
            recommended_action = "Abrir ticket de corrección de identidad hacia IAM adjuntando comprobante de matrícula y DNI."

        # Regla Heurística 6: Turnos, Mails de Notificación, Prestador y Consultorio
        elif any(k in query_lower for k in ["mail", "email", "correo", "teléfono", "telefono", "notificacion", "notificación", "turno", "consultorio", "sede"]):
            subsystem = "Servicio de Notificaciones y Configuración de Consultorio (SAP / Cartilla / CD2)"
            root_cause = "Reglas de mensajería y configuración del prestador: el correo del profesional no se actualiza de forma automática en los turnos agendados; toma la dirección registrada en el JSON o en la casilla principal de Cartilla Médica."
            solution_steps = [
                "1. **Email del Consultorio / Prestador (Mensajería):** El correo del médico no se actualiza automáticamente desde el turno; toma el mail del JSON original. El prestador lo modifica directamente en Extranet/Mis Datos. Las notificaciones se despachan a 1 sola casilla: la configurada como principal en Cartilla Médica.",
                "2. **Email y Teléfono del Paciente:** Se crean con el primer turno. Al confirmar turnos posteriores, el sistema adopta el mail y teléfono específicos cargados para esa cita.",
                "3. **Baja o Modificación de Consultorio:** La baja de consultorio es una acción administrativa que requiere aplicar la bandera lógica `isDeleted = true` en la base de datos de CD2.",
                "4. **Dirección y Teléfono del Consultorio:** Para actualización, solicitar ticket PAU a Mesa de Ayuda para validación y ejecución pericial en BD."
            ]
            escalation_circuit = "Soporte Operativo N1 -> Especialistas Cartilla / BD CD2"
            recommended_action = "Verificar casilla principal en Cartilla Médica y validar JSON de confirmación del turno o aplicar isDeleted en BD si es baja."

        # Regla Heurística 7: Cierre de Atención y Formularios
        elif any(k in query_lower for k in ["cerrar", "finalizar", "diagnóstico", "diagnostico", "certificado", "evolución", "evolucion"]):
            subsystem = "Motor de Validaciones Clínicas y Cierre de Consulta"
            root_cause = "Omisión del campo mandatorio de Diagnóstico codificado o ingreso de valor '0' en certificados de reposo."
            solution_steps = [
                "1. **Diagnóstico Mandatorio:** La normativa legal exige seleccionar un Diagnóstico Principal (CIE-10/SNOMED) para habilitar el botón 'Finalizar Atención'. Completar la evolución escrita no reemplaza este requisito.",
                "2. **Certificados Médicos:** En certificados que no indican días de reposo, deje el campo numérico vacío o desmarque la opción de reposo para evitar rechazo de validación."
            ]
            escalation_circuit = "Mesa de Ayuda N1"
            recommended_action = "Instruir al profesional sobre la obligatoriedad del diagnóstico codificado para la firma electrónica."

        # Si no coincidió con ninguna regla estricta, recuperar directamente desde el artículo más afín de la KB
        else:
            if top_articles:
                top_art = top_articles[0]
                subsystem = top_art.category or "Consultorio Digital 2 (CD2)"
                root_cause = f"Guía pericial identificada en base de conocimiento: '{top_art.title}'"
                
                # Extraer pasos o recomendaciones útiles del contenido
                content_snippets = [
                    line.strip() for line in top_art.content.split("\n")
                    if line.strip() and not line.strip().startswith("#") and len(line.strip()) > 15
                ]
                if content_snippets:
                    solution_steps = content_snippets[:3]
                else:
                    solution_steps = [
                        f"1. **Procedimiento Validado:** Aplicar el estándar documentado en '{top_art.title}'.",
                        "2. **Acción Asistencial:** Seguir las instrucciones homologadas de la base de conocimiento para evitar demoras de atención.",
                        "3. **Derivación:** Si el caso persiste o requiere intervención en base de datos, genere el ticket en 1 clic."
                    ]
                escalation_circuit = "Mesa de Ayuda N1"
                recommended_action = f"Aplicar procedimiento homologado según guía N3: {top_art.title}"
            else:
                subsystem = "Plataforma Asistencial Integral (CD2)"
                root_cause = "Incidencia operativa o de usabilidad asistencial en proceso de atención"
                solution_steps = [
                    f"1. **Revisión de Parámetros:** Para consultas sobre '{query_text[:50]}...', compruebe que su sesión clínica esté activa y que cuente con conectividad estable al efector.",
                    "2. **Procedimiento Recomendado:** Reinicie la vista del módulo pulsando F5 o cierre la sesión desde la barra superior y vuelva a ingresar para refrescar credenciales de seguridad.",
                    "3. **Asistencia Especializada:** Si el síntoma persiste, el equipo de soporte N1/N2 tomará el caso de forma inmediata con el dictamen técnico precargado."
                ]
                escalation_circuit = "Mesa de Ayuda N1"
                recommended_action = "Analizar traza de logs de frontend y evaluar si requiere intervención de infraestructura o desarrollo."

        # Construcción de la respuesta fluida, empática y pericial (sin plantilla rígida)
        formatted_response = (
            f"Estimado/a {user_fullname},\n\n"
            f"He realizado un **análisis funcional de su consulta** sobre **{subsystem}**:\n\n"
            f"**Causa Raíz Identificada:** {root_cause}\n\n"
            f"**Procedimiento Operativo de Solución:**\n" +
            "\n".join(solution_steps) + "\n\n"
            f"¿Esta indicación resolvió su problema?"
        )

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
