"""
backend/app/services/ticket_manager_bot.py
==========================================
Bot Gestor de Tickets Automatizado con Diálogo Multi-Rol, Sectores y Enriquecimiento de Base de Conocimiento (KCS v6 / ITIL 4).

Responsabilidades:
1. Avanzar tickets en su ciclo de vida ITIL (NUEVO -> ASIGNADO -> EN_CURSO -> ESPERANDO -> RESUELTO -> CERRADO).
2. Generar interacción conversacional auténtica y contextual entre todos los roles:
   - SOLICITANTE (Médicos, Profesionales Asistenciales, Jefes de Servicio)
   - SOPORTE_N1 (Mesa de Ayuda Central, Operadores de Turno)
   - ESPECIALISTA_N2 (Infraestructura, Pasarelas OSDE/SISA, DICOM, Aplicaciones)
   - ADMIN_INFRAESTRUCTURA_N3 (DevOps, Cloud, DBAs)
   - TEAM_LEADER (Supervisores de Mesa de Ayuda)
   - PASARELA_TERCEROS (Servicios Externos POS/SISA)
   Y sus respectivos sectores (Guardia, Consultorios, Farmacia, Infraestructura, etc.).
3. Registrar cada mensaje y transición en el timeline del ticket (TicketComment y TicketAuditLog).
4. Al momento de resolver según la información del negocio:
   - Determinar si el ticket aporta o no conocimiento técnico transferible a la Base de Conocimiento.
   - Si aporta: Asocia formalmente al artículo correspondiente en KBArticle, persiste el aporte en KBArticleContribution,
     con el resumen de lo aprendido, autor, sector y pasos de solución.
   - Si no aporta (rutina administrativa, duplicado): Resuelve sin asociar a KB con justificación explícita.
5. Permitir la consulta desde la Base de Conocimiento mostrando todos los tickets que contribuyeron con información
   al resolverse.
"""

import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from sqlmodel import Session, select

from app.models.entities import (
    Ticket, TicketStatus, TicketComment, TicketAuditLog,
    KBArticle, KBArticleContribution, SupportLevel, PriorityLevel
)

# Catálogo de Sectores y Roles
SECTORS_CATALOG = {
    "SOLICITANTE": [
        "Guardia Médica y Urgencias",
        "Consultorios Externos y Turnos",
        "Farmacia y Prescripciones Digitales",
        "Internación y Terapia Intensiva",
        "Diagnóstico por Imágenes (DICOM)"
    ],
    "SOPORTE_N1": [
        "Mesa de Ayuda Central",
        "Atención a Profesionales OSDE",
        "Centro de Recepción de Incidencias"
    ],
    "ESPECIALISTA_N2": [
        "Integraciones y Pasarelas OSDE/SISA",
        "Soporte de Consultorio Digital & Telemedicina",
        "Sistemas de Historias Clínicas (HCE)",
        "Diagnóstico por Imágenes y PACS"
    ],
    "ADMIN_INFRAESTRUCTURA_N3": [
        "Infraestructura, Servidores y Cloud",
        "Redes, Seguridad y Conectividad VPN",
        "Base de Datos y Rendimiento Transaccional"
    ],
    "TEAM_LEADER": [
        "Supervisión y Control de Calidad ITIL",
        "Jefatura de Operaciones Mesa de Ayuda"
    ],
    "PASARELA_TERCEROS": [
        "Pasarela SISA Transaccional",
        "Validador POS de Prestaciones OSDE"
    ]
}

PERSONAS = {
    "SOLICITANTE": [
        {"username": "dra_martinez", "name": "Dra. Elena Martínez", "sector": "Guardia Médica y Urgencias"},
        {"username": "dr_lopez", "name": "Dr. Juan López", "sector": "Consultorios Externos y Turnos"},
        {"username": "dr_fernandez", "name": "Dr. Roberto Fernández", "sector": "Farmacia y Prescripciones Digitales"},
        {"username": "dra_gomez", "name": "Lic. Marcela Gómez", "sector": "Salud Mental y Psicología"},
        {"username": "solicitante", "name": "Dr. Martín Gómez", "sector": "Internación y Quirófanos"}
    ],
    "SOPORTE_N1": [
        {"username": "cpaez", "name": "Carlos Páez", "sector": "Mesa de Ayuda Central"},
        {"username": "svaldez", "name": "Sofía Valdez", "sector": "Atención a Profesionales OSDE"},
        {"username": "mflores", "name": "Marcos Flores", "sector": "Mesa de Ayuda Central"}
    ],
    "ESPECIALISTA_N2": [
        {"username": "soporte", "name": "Laura Benítez", "sector": "Soporte de Consultorio Digital & Telemedicina"},
        {"username": "gfernandez", "name": "Gonzalo Fernández", "sector": "Integraciones y Pasarelas OSDE/SISA"},
        {"username": "vromero", "name": "Valeria Romero", "sector": "Diagnóstico por Imágenes y PACS"}
    ],
    "ADMIN_INFRAESTRUCTURA_N3": [
        {"username": "dnavarro", "name": "Diego Navarro", "sector": "Infraestructura, Servidores y Cloud"},
        {"username": "ealvarez", "name": "Esteban Álvarez", "sector": "Base de Datos y Rendimiento Transaccional"}
    ],
    "TEAM_LEADER": [
        {"username": "teamleader", "name": "Pablo Giménez", "sector": "Supervisión y Control de Calidad ITIL"},
        {"username": "admin", "name": "Freddy Cortés", "sector": "Jefatura de Operaciones Mesa de Ayuda"}
    ],
    "PASARELA_TERCEROS": [
        {"username": "pasarela_osde", "name": "Sistema Validador POS OSDE", "sector": "Validador POS de Prestaciones OSDE"},
        {"username": "pasarela_sisa", "name": "Servicio Central SISA", "sector": "Pasarela SISA Transaccional"}
    ]
}

# Conocimiento técnico base para asociación a KB
KB_TOPIC_MATCHERS = [
    {
        "keywords": ["receta", "prescripcion", "prescripción", "farmacia", "alfabeta", "vademecum", "vademécum", "medicamento"],
        "category": "Receta Digital",
        "preferred_article_id": 18,
        "default_title": "Resolución de Fallas en Validación de Recetas y Catálogo de Medicamentos",
        "rca": "Incompatibilidad transitoria entre el formato del código alfabeta y la firma digital remota.",
        "solution": "Se sincronizó la tabla local de vademécum y se forzó la re-firma con el certificado SISA vigente."
    },
    {
        "keywords": ["matricula", "matrícula", "sisa", "profesional", "firma digital", "hce"],
        "category": "Interoperabilidad SISA",
        "preferred_article_id": 13,
        "default_title": "Validación de Matrículas Profesionales y Firma Digital en Pasarela SISA",
        "rca": "Timeout en el endpoint de validación biométrica SISA durante picos de concurrencia asistencial.",
        "solution": "Se ajustó el timeout de conexión a 15 segundos y se activó el buffer de contingencia local."
    },
    {
        "keywords": ["videoconsulta", "telemedicina", "jitsi", "camara", "audio", "webrtc", "micrófono", "llamada"],
        "category": "Telemedicina",
        "preferred_article_id": 14,
        "default_title": "Diagnóstico y Normalización de Salas de Telemedicina y Video WebRTC",
        "rca": "Bloqueo de puertos UDP y descarte de paquetes WebRTC en el proxy perimetral de la institución.",
        "solution": "Se habilitó el protocolo TURN sobre TLS (puerto 443) garantizando conectividad transparente."
    },
    {
        "keywords": ["token", "pos", "rechazo", "prestacion", "prestación", "validador", "socio"],
        "category": "Consultorio Digital",
        "preferred_article_id": 16,
        "default_title": "Protocolo de Destrabe de Validaciones de Token y Transacciones POS OSDE",
        "rca": "Error de tipeo de token o expiración de ventana de sesión transaccional de 5 minutos.",
        "solution": "Se instruyó el reingreso del token de 3 dígitos durante la llamada conforme a la guía de Salud Mental (Nodo 2.1)."
    },
    {
        "keywords": ["dicom", "pacs", "visor", "imagen", "estudio", "radiografia", "tac"],
        "category": "Diagnóstico por Imágenes",
        "preferred_article_id": 15,
        "default_title": "Guía de Recuperación y Carga de Visor DICOM para Diagnóstico por Imágenes",
        "rca": "Saturación del almacenamiento temporal de miniaturas DICOM en el nodo local.",
        "solution": "Se ejecutó la purga del cache local y se reindexaron los metadatos de las series radiológicas."
    },
    {
        "keywords": ["agenda", "turno", "calendario", "horario", "sobreturno"],
        "category": "Gestión de Turnos",
        "preferred_article_id": 19,
        "default_title": "Configuración de Franjas y Disponibilidad de Agendas en Portal de Turnos",
        "rca": "Superposición de bloqueos periódicos sobre la matriz de turnos disponibles del profesional.",
        "solution": "Se reconfiguraron los intervalos de atención a 20 minutos y se sincronizó la cartilla online."
    }
]

class TicketManagerBot:
    """Motor automatizado de gestión de tickets, diálogo multi-rol y contribución KCS."""

    @staticmethod
    def _add_comment(
        session: Session,
        ticket_id: str,
        author: Dict[str, str],
        message: str,
        is_internal: bool = False,
        timestamp: Optional[datetime] = None
    ) -> TicketComment:
        ts = timestamp or datetime.utcnow()
        comment = TicketComment(
            ticket_id=ticket_id,
            author_username=author.get("username", "bot_gestor"),
            author_role=author.get("role", "SOPORTE_N1"),
            author_sector=author.get("sector", "Mesa de Ayuda"),
            message=message,
            is_internal=is_internal,
            created_at=ts
        )
        session.add(comment)
        return comment

    @staticmethod
    def _add_audit(
        session: Session,
        ticket_id: str,
        actor: str,
        field: str,
        old_val: Optional[str],
        new_val: Optional[str],
        reason: str,
        timestamp: Optional[datetime] = None
    ):
        audit = TicketAuditLog(
            ticket_id=ticket_id,
            changed_by_username=actor,
            field_changed=field,
            old_value=old_val,
            new_value=new_val,
            change_reason=reason,
            created_at=timestamp or datetime.utcnow()
        )
        session.add(audit)

    @classmethod
    def evaluate_business_kb_qualification(cls, ticket: Ticket) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Evalúa según las reglas de negocio si el ticket aporta o no información
        reutilizable y transferible a la Base de Conocimiento (KCS v6).
        """
        text = f"{ticket.title} {ticket.description}".lower()
        
        # Casos que NO deben asociarse a KB (rutinas administrativas, consultas simples, cancelaciones, duplicados)
        non_kb_triggers = [
            "olvido de contraseña", "cambio de clave", "reseteo simple",
            "consulta de horario", "felicitacion", "prueba de mesa",
            "cancelacion solicitada", "duplicado", "anulación por error"
        ]
        if any(trigger in text for trigger in non_kb_triggers):
            return False, None

        # Evaluar contra la matriz de conocimiento técnico
        for matcher in KB_TOPIC_MATCHERS:
            for kw in matcher["keywords"]:
                if kw in text:
                    return True, matcher

        # Si el ticket es un Incidente P1 o P2 con descripción técnica, califica por criticidad
        if ticket.priority in (PriorityLevel.P1, PriorityLevel.P2) or ticket.support_level == SupportLevel.N2:
            return True, {
                "keywords": ["general"],
                "category": "Soporte Asistencial General",
                "preferred_article_id": None,
                "default_title": f"Solución Homologada KCS: {ticket.title}",
                "rca": "Falla técnica operativa identificada y subsanada mediante intervención especializada.",
                "solution": ticket.resolution_notes or "Se aplicó procedimiento de reconfiguración y validación en vivo."
            }

        return False, None

    @classmethod
    def process_ticket_step(cls, session: Session, ticket: Ticket) -> Dict[str, Any]:
        """
        Avanza el ticket un paso en su ciclo de vida ITIL interactuando
        con los roles y sectores pertinentes, registrando los mensajes correspondientes.
        """
        now = datetime.utcnow()
        old_status = ticket.status
        action_summary = ""
        associated_kb = False
        kb_info = None

        # ----------------------------------------------------------------------
        # PASO 1: NUEVO -> ASIGNADO / EN_CURSO
        # ----------------------------------------------------------------------
        if ticket.status == TicketStatus.NUEVO:
            op = random.choice(PERSONAS["SOPORTE_N1"])
            ticket.status = TicketStatus.ASIGNADO
            ticket.assignee_username = op["username"]
            ticket.support_level = SupportLevel.N1
            ticket.updated_at = now

            cls._add_comment(
                session=session,
                ticket_id=ticket.id,
                author={**op, "role": "SOPORTE_N1"},
                message=f"[MESA DE AYUDA] Solicitud tomada por {op['name']} ({op['sector']}). Iniciando triaje técnico inicial y verificación de logs de la plataforma {ticket.platform_code}."
            )
            cls._add_audit(
                session=session,
                ticket_id=ticket.id,
                actor=op["username"],
                field="status",
                old_val="NUEVO",
                new_val="ASIGNADO",
                reason=f"Asignación de caso a operador N1 ({op['name']})."
            )
            action_summary = f"Ticket {ticket.id} asignado a {op['name']} ({op['sector']})."

        # ----------------------------------------------------------------------
        # PASO 2: ASIGNADO -> EN_CURSO (con interacción con Solicitante/Sector)
        # ----------------------------------------------------------------------
        elif ticket.status == TicketStatus.ASIGNADO:
            n1 = random.choice(PERSONAS["SOPORTE_N1"])
            doc = next((p for p in PERSONAS["SOLICITANTE"] if p["username"] == ticket.requester_username), PERSONAS["SOLICITANTE"][0])
            
            ticket.status = TicketStatus.EN_CURSO
            ticket.updated_at = now

            # Interacción 1: N1 consulta al solicitante
            cls._add_comment(
                session=session,
                ticket_id=ticket.id,
                author={**n1, "role": "SOPORTE_N1"},
                message=f"Estimado/a {doc['name']} ({doc['sector']}): Nos encontramos analizando la incidencia reportada en {ticket.platform_code}. ¿Podría indicarnos si el síntoma persiste en este momento o si afecta a otras terminales del sector?"
            )
            
            # Interacción 2: Solicitante responde desde su sector clínico
            cls._add_comment(
                session=session,
                ticket_id=ticket.id,
                author={**doc, "role": "SOLICITANTE"},
                message=f"Buenas tardes Mesa de Ayuda. Confirmo que en el sector {doc['sector']} se reproduce al intentar operar con la plataforma. Aguardamos indicaciones para no demorar la atención asistencial.",
                timestamp=now + timedelta(seconds=2)
            )

            cls._add_audit(
                session=session,
                ticket_id=ticket.id,
                actor=n1["username"],
                field="status",
                old_val="ASIGNADO",
                new_val="EN_CURSO",
                reason="Diagnóstico técnico en curso con intercambio de datos del solicitante."
            )
            action_summary = f"Ticket {ticket.id} puesto EN_CURSO con diálogo entre Mesa de Ayuda y {doc['name']}."

        # ----------------------------------------------------------------------
        # PASO 3: EN_CURSO -> ESPERANDO_AL_PRESTADOR o Intervención N2
        # ----------------------------------------------------------------------
        elif ticket.status == TicketStatus.EN_CURSO and not ticket.is_workaround:
            # Especialista N2 interviene
            n2 = random.choice(PERSONAS["ESPECIALISTA_N2"])
            ticket.is_workaround = True  # Bandera temporal de diagnóstico N2
            ticket.support_level = SupportLevel.N2
            ticket.updated_at = now

            cls._add_comment(
                session=session,
                ticket_id=ticket.id,
                author={**n2, "role": "ESPECIALISTA_N2"},
                message=f"[ESCALAMIENTO N2] Intervención de {n2['name']} ({n2['sector']}). Se inspeccionaron las trazas de comunicación de la pasarela y la base de datos transaccional. Detectada desincronización de sesión y bloqueo transitorio en el nodo regional. Aplicando procedimiento de refresco y purga de socket."
            )

            # Si es pasarela o SISA, se suma mensaje de Terceros
            if "SISA" in ticket.title.upper() or "OSDE" in ticket.title.upper() or "RECETA" in ticket.platform_code:
                ext = PERSONAS["PASARELA_TERCEROS"][0]
                cls._add_comment(
                    session=session,
                    ticket_id=ticket.id,
                    author={**ext, "role": "PASARELA_TERCEROS"},
                    message=f"[SISTEMA EXTERNO] {ext['name']} ({ext['sector']}): Servicio transaccional validado. Latencia normalizada a 42ms. Transacciones autorizadas correctamente.",
                    timestamp=now + timedelta(seconds=3)
                )

            cls._add_audit(
                session=session,
                ticket_id=ticket.id,
                actor=n2["username"],
                field="support_level",
                old_val="N1",
                new_val="N2",
                reason=f"Diagnóstico de segundo nivel y reconfiguración técnica aplicada por {n2['name']}."
            )
            action_summary = f"Ticket {ticket.id} auditado por Especialista N2 ({n2['name']}) y pasarela externa."

        # ----------------------------------------------------------------------
        # PASO 4: EN_CURSO -> RESUELTO (Evaluación de Negocio para Asociación a KB)
        # ----------------------------------------------------------------------
        elif ticket.status in (TicketStatus.EN_CURSO, TicketStatus.ESPERANDO_AL_PRESTADOR):
            n2 = random.choice(PERSONAS["ESPECIALISTA_N2"])
            qualifies_kb, kb_match = cls.evaluate_business_kb_qualification(ticket)

            ticket.status = TicketStatus.RESUELTO
            ticket.resolved_at = now
            ticket.updated_at = now
            ticket.resolved_by = n2["username"]

            if qualifies_kb and kb_match:
                # SE ASOCIA A BASE DE CONOCIMIENTO (KCS v6)
                associated_kb = True
                
                # 1. Buscar o crear el artículo afín en KBArticle
                article = None
                if kb_match.get("preferred_article_id"):
                    article = session.get(KBArticle, kb_match["preferred_article_id"])

                if not article:
                    # Buscar por categoría
                    article = session.exec(
                        select(KBArticle).where(KBArticle.category == kb_match["category"])
                    ).first()

                if not article:
                    # Crear nuevo artículo KCS si no existía
                    article = KBArticle(
                        title=kb_match["default_title"],
                        category=kb_match["category"],
                        content=f"### CAUSA RAÍZ (RCA)\n{kb_match['rca']}\n\n### PROCEDIMIENTO RESOLUTIVO\n1. Verificar conectividad del nodo asistencial.\n2. {kb_match['solution']}\n3. Comprobar confirmación de la transacción en el validador.\n\n### RESULTADO\nSolución validada para reutilización continua.",
                        tags="kcs, itil4, resolucion_bot, oficial",
                        author_username=n2["username"],
                        source_ticket_id=ticket.id,
                        version="v1.0",
                        changelog=f"Generado y alimentado desde resolución de ticket {ticket.id}",
                        view_count=1,
                        is_published=True,
                        created_at=now,
                        updated_at=now
                    )
                    session.add(article)
                    session.flush()

                # 2. Registrar formalmente la contribución del ticket en la tabla de enlace
                contribution_text = f"Causa Raíz identificada: {kb_match['rca']} — Solución técnica aplicada: {kb_match['solution']}"
                contrib = KBArticleContribution(
                    article_id=article.id,
                    ticket_id=ticket.id,
                    ticket_title=ticket.title,
                    contribution_summary=contribution_text,
                    contributor_username=n2["username"],
                    contributor_role="ESPECIALISTA_N2",
                    contributor_sector=n2["sector"],
                    solution_steps=kb_match["solution"],
                    created_at=now
                )
                session.add(contrib)

                # 3. Vincular ticket con el artículo
                ticket.associated_kb_id = article.id
                ticket.contributed_to_kb = True
                ticket.resolution_notes = f"Solución técnica KCS v6 homologada: {kb_match['solution']}"
                article.view_count = (article.view_count or 0) + 1
                article.updated_at = now
                session.add(article)

                # 4. Mensaje con mención explícita al artículo de KB
                cls._add_comment(
                    session=session,
                    ticket_id=ticket.id,
                    author={**n2, "role": "ESPECIALISTA_N2"},
                    message=f"[RESOLUCIÓN EXITOSA KCS v6] Incidencia resuelta satisfactoriamente por {n2['name']} ({n2['sector']}). Se restableció la operación normal. "
                            f"\n\n📚 [APORTE A BASE DE CONOCIMIENTO]: Este ticket sumó información técnica formal al Artículo KB #{article.id} ('{article.title}'). "
                            f"El procedimiento queda registrado para reutilización inmediata por toda la organización."
                )
                cls._add_audit(
                    session=session,
                    ticket_id=ticket.id,
                    actor=n2["username"],
                    field="status",
                    old_val="EN_CURSO",
                    new_val="RESUELTO",
                    reason=f"Resolución técnica con aporte formal a la Base de Conocimiento (Artículo #{article.id})."
                )
                action_summary = f"Ticket {ticket.id} RESUELTO y ASOCIADO a Base de Conocimiento (Artículo KB #{article.id} - '{article.title}')."
                kb_info = {"article_id": article.id, "article_title": article.title, "contributed": True}

            else:
                # NO SE ASOCIA A BASE DE CONOCIMIENTO (Rutina sin nuevo conocimiento)
                associated_kb = False
                ticket.contributed_to_kb = False
                ticket.resolution_notes = "Incidencia procedimental resuelta según el protocolo habitual de Mesa de Ayuda."
                cls._add_comment(
                    session=session,
                    ticket_id=ticket.id,
                    author={**n2, "role": "SOPORTE_N1"},
                    message=f"[RESOLUCIÓN OPERATIVA] Solicitud resuelta por {n2['name']} conforme a directivas estándar. "
                            f"[INFORMACIÓN DE NEGOCIO: No se asocia a la Base de Conocimiento al tratarse de una consulta/operación de rutina sin nuevo conocimiento técnico transferible]."
                )
                cls._add_audit(
                    session=session,
                    ticket_id=ticket.id,
                    actor=n2["username"],
                    field="status",
                    old_val="EN_CURSO",
                    new_val="RESUELTO",
                    reason="Resolución estándar completada sin requerir nuevo artículo en Base de Conocimiento."
                )
                action_summary = f"Ticket {ticket.id} RESUELTO de forma estándar (NO asociado a Base de Conocimiento)."
                kb_info = {"contributed": False, "reason": "Caso de rutina sin nuevo conocimiento"}

        # ----------------------------------------------------------------------
        # PASO 5: RESUELTO -> CERRADO (Conformidad del Solicitante con CSAT)
        # ----------------------------------------------------------------------
        elif ticket.status == TicketStatus.RESUELTO:
            doc = next((p for p in PERSONAS["SOLICITANTE"] if p["username"] == ticket.requester_username), PERSONAS["SOLICITANTE"][0])
            ticket.status = TicketStatus.CERRADO
            ticket.closed_at = now
            ticket.updated_at = now
            ticket.closed_by = doc["username"]
            ticket.rating_stars = 5
            ticket.rating_kudos = "Resolución Técnica Inmediata y Eficaz"
            ticket.rating_feedback = f"El profesional {doc['name']} confirmó que el servicio en el sector {doc['sector']} se encuentra 100% operativo y normalizado."

            cls._add_comment(
                session=session,
                ticket_id=ticket.id,
                author={**doc, "role": "SOLICITANTE"},
                message=f"[CONFORMIDAD ASISTENCIAL] Estimada Mesa de Ayuda: Verificamos en el sector {doc['sector']} que la plataforma opera de forma impecable. Todo el personal puede registrar y validar sin demoras. Calificación CSAT: 5/5 estrellas. ¡Muchas gracias por el soporte!"
            )
            cls._add_audit(
                session=session,
                ticket_id=ticket.id,
                actor=doc["username"],
                field="status",
                old_val="RESUELTO",
                new_val="CERRADO",
                reason=f"Cierre definitivo con conformidad del solicitante y encuesta CSAT de 5 estrellas."
            )
            action_summary = f"Ticket {ticket.id} CERRADO con CSAT 5/5 estrellas por {doc['name']}."

        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        return {
            "ticket_id": ticket.id,
            "previous_status": old_status.value if hasattr(old_status, 'value') else str(old_status),
            "new_status": ticket.status.value if hasattr(ticket.status, 'value') else str(ticket.status),
            "action_summary": action_summary,
            "associated_to_kb": associated_kb,
            "kb_info": kb_info,
            "contributed_to_kb": ticket.contributed_to_kb,
            "associated_kb_id": ticket.associated_kb_id
        }

    @classmethod
    def run_automation_cycle(cls, session: Session, max_tickets: int = 5) -> List[Dict[str, Any]]:
        """
        Ejecuta una ronda de avance automático de tickets activos respetando el flujo de negocio.
        """
        results = []
        # Buscar tickets en diferentes estados para dar fluidez continua
        query = select(Ticket).where(
            Ticket.status.in_([TicketStatus.NUEVO, TicketStatus.ASIGNADO, TicketStatus.EN_CURSO, TicketStatus.RESUELTO])
        ).order_by(Ticket.updated_at.asc()).limit(max_tickets)

        candidates = session.exec(query).all()
        for t in candidates:
            res = cls.process_ticket_step(session, t)
            results.append(res)

        return results

    @classmethod
    def get_article_contributing_tickets(cls, session: Session, article_id: int) -> List[Dict[str, Any]]:
        """
        Consulta y devuelve todos los tickets que sumaron información
        a un artículo específico de la Base de Conocimiento al momento de ser resueltos.
        """
        contributions = session.exec(
            select(KBArticleContribution)
            .where(KBArticleContribution.article_id == article_id)
            .order_by(KBArticleContribution.created_at.desc())
        ).all()

        results = []
        for c in contributions:
            ticket = session.get(Ticket, c.ticket_id)
            results.append({
                "ticket_id": c.ticket_id,
                "title": c.ticket_title or (ticket.title if ticket else "Incidencia Asistencial"),
                "contribution_summary": c.contribution_summary,
                "solution_steps": c.solution_steps,
                "contributor_username": c.contributor_username,
                "contributor_role": c.contributor_role,
                "contributor_sector": c.contributor_sector,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "priority": ticket.priority.value if (ticket and hasattr(ticket.priority, 'value')) else (str(ticket.priority) if ticket else "P3"),
                "platform_code": ticket.platform_code if ticket else "GENERAL",
                "institution_code": ticket.institution_code if ticket else "GENERAL"
            })
        return results
