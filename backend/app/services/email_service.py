"""
Servicio de Notificaciones y Despacho de Correos Electrónicos
HealthDesk Quantux — Implementación Avanzada Omnicanal Multi-Destinatario (UH-35)
Notifica a TODOS los involucrados (Solicitante, Operador Asignado, Supervisores y Participantes)
ante cualquier novedad o cambio de estado en el ticket.
"""

import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Set
from sqlmodel import Session, select

from app.models.entities import Ticket, User, EmailNotificationLog, PriorityLevel, TicketStatus, TicketComment
from app.db.session import engine

logger = logging.getLogger("healthdesk.email")
logger.setLevel(logging.INFO)

# CONFIGURACIÓN SMTP (Variables de Entorno o Fallback Seguro)
SMTP_HOST = os.getenv("SMTP_HOST", os.getenv("SMTP_SERVER", ""))
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "notificaciones@quantuxsalud.com")
SMTP_ENABLED = bool(SMTP_HOST and SMTP_USER)

# URL Base de la aplicación para enlaces directos en correos
APP_BASE_URL = os.getenv("APP_BASE_URL", "https://healthdesk-quantux.onrender.com")

def _get_user_info(username: Optional[str], session: Session) -> Dict[str, str]:
    """Obtiene email y nombre legible de un usuario, garantizando mapeo exacto para Freddy Cortés."""
    if not username:
        return {"email": "soporte@quantuxsalud.com", "name": "Mesa de Soporte TI", "username": "soporte"}
    
    clean_u = username.strip().lower()
    if clean_u in ["admin", "fcortes", "freddy", "fcortes@quantuxsalud.com"]:
        return {"email": "fcortes@quantuxsalud.com", "name": "Freddy Cortés", "username": username}
    
    # Buscar en base de datos
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        if "freddy" in user.full_name.lower() or user.username == "admin":
            return {"email": "fcortes@quantuxsalud.com", "name": user.full_name, "username": user.username}
        return {"email": user.email, "name": user.full_name, "username": user.username}
    
    return {"email": f"{clean_u}@quantuxsalud.com", "name": username, "username": username}


def get_all_involved_recipients(ticket: Ticket, session: Session, extra_author: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Identifica a TODOS los usuarios involucrados en un ticket para despacho de novedades:
    1. Solicitante (Médico / Profesional de la salud)
    2. Operador Asignado (Agente de Soporte actual)
    3. Participantes que hayan comentado o interactuado previamente
    4. Supervisor / Lead ITIL (Freddy Cortés: fcortes@quantuxsalud.com) si es P1/P2 o asignado
    5. Guardia de Soporte si el caso no tiene operador
    """
    recipients_map: Dict[str, Dict[str, str]] = {}

    def add_recipient(username: Optional[str], role_label: str):
        if not username:
            return
        info = _get_user_info(username, session)
        email = info["email"].strip().lower()
        if email not in recipients_map:
            recipients_map[email] = {
                "email": info["email"],
                "name": info["name"],
                "username": info["username"],
                "role_label": role_label
            }

    # 1. Solicitante
    if ticket.requester_username:
        add_recipient(ticket.requester_username, "SOLICITANTE")

    # 2. Operador Asignado
    if ticket.assignee_username:
        add_recipient(ticket.assignee_username, "OPERADOR_ASIGNADO")

    # 3. Autor del cambio o comentario actual
    if extra_author:
        add_recipient(extra_author, "PARTICIPANTE")

    # 4. Todos los usuarios que hayan participado en comentarios
    try:
        comments = session.exec(select(TicketComment).where(TicketComment.ticket_id == ticket.id)).all()
        for c in comments:
            if c.author_username:
                add_recipient(c.author_username, "PARTICIPANTE")
    except Exception as e:
        logger.warning(f"Error consultando comentaristas para ticket {ticket.id}: {e}")

    # 5. Si es incidente crítico (P1 o P2), asegurar siempre copia a Freddy Cortés (Lead TI) y Guardia
    prio_str = str(ticket.priority.value if hasattr(ticket.priority, "value") else ticket.priority)
    if prio_str in ["P1", "P2"] or ticket.assignee_username == "admin":
        add_recipient("admin", "SUPERVISIÓN_TI")
        if prio_str == "P1":
            if "guardia.soporte@quantuxsalud.com" not in recipients_map:
                recipients_map["guardia.soporte@quantuxsalud.com"] = {
                    "email": "guardia.soporte@quantuxsalud.com",
                    "name": "Guardia Técnica 24/7",
                    "username": "guardia",
                    "role_label": "GUARDIA_TI"
                }

    # Si no hay operador asignado aún, notificar a la mesa central
    if not ticket.assignee_username and "soporte@quantuxsalud.com" not in recipients_map:
        recipients_map["soporte@quantuxsalud.com"] = {
            "email": "soporte@quantuxsalud.com",
            "name": "Mesa de Ayuda Quantux",
            "username": "soporte",
            "role_label": "MESA_SOPORTE"
        }

    return list(recipients_map.values())


def _render_email_template(
    title: str,
    badge_text: str,
    badge_color: str,
    ticket_id: str,
    ticket_title: str,
    platform: str,
    institution: str,
    priority: str,
    status: str,
    recipient_name: str,
    recipient_role: str,
    main_message: str,
    call_to_action_url: Optional[str] = None
) -> str:
    """Genera la plantilla HTML responsive con branding de Quantux Salud y encabezado personalizado."""
    cta_url = call_to_action_url or f"{APP_BASE_URL}/cockpit"
    
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F1F5F9; margin: 0; padding: 20px; color: #0F172A; }}
    .email-container {{ max-width: 620px; margin: 0 auto; background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    .header {{ background-color: #0F1E36; color: #FFFFFF; padding: 18px 24px; display: flex; align-items: center; justify-content: space-between; }}
    .brand {{ font-size: 18px; font-weight: 800; letter-spacing: -0.5px; }}
    .brand span {{ color: #00C4B4; }}
    .badge {{ background-color: {badge_color}; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; }}
    .content {{ padding: 24px; }}
    .recipient-bar {{ background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px 12px; margin-bottom: 16px; font-size: 12px; color: #475569; }}
    .recipient-bar strong {{ color: #0F172A; }}
    .recipient-tag {{ display: inline-block; background: #E2E8F0; color: #0F172A; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 3px; margin-left: 6px; }}
    .headline {{ font-size: 16px; font-weight: 700; color: #0F1E36; margin-bottom: 12px; }}
    .message-box {{ background-color: #F8FAFC; border-left: 4px solid #00A896; padding: 14px 16px; margin: 16px 0; font-size: 13.5px; line-height: 1.5; color: #334155; border-radius: 0 6px 6px 0; }}
    .ticket-card {{ border: 1px solid #CBD5E1; border-radius: 6px; padding: 14px; margin: 16px 0; background: #FFFFFF; }}
    .ticket-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; }}
    .meta-item strong {{ color: #64748B; font-size: 11px; display: block; text-transform: uppercase; }}
    .btn {{ display: inline-block; background-color: #00A896; color: #FFFFFF; text-decoration: none; padding: 11px 22px; font-weight: 700; font-size: 13px; border-radius: 6px; margin-top: 14px; }}
    .footer {{ background-color: #F8FAFC; border-top: 1px solid #E2E8F0; padding: 14px 24px; font-size: 11px; color: #94A3B8; text-align: center; }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <div class="brand">HEALTHDESK <span>QUANTUX</span></div>
      <div class="badge">{badge_text}</div>
    </div>
    
    <div class="content">
      <div class="recipient-bar">
        Para: <strong>{recipient_name}</strong> <span class="recipient-tag">{recipient_role}</span> • Notificación a Involucrados
      </div>

      <div class="headline">{title}</div>
      
      <div class="message-box">
        {main_message}
      </div>

      <div class="ticket-card">
        <div style="font-weight: 700; font-size: 14px; color: #0F1E36; margin-bottom: 8px;">
          [{ticket_id}] {ticket_title}
        </div>
        <div class="ticket-grid">
          <div class="meta-item"><strong>Plataforma</strong> {platform}</div>
          <div class="meta-item"><strong>Institución</strong> {institution}</div>
          <div class="meta-item"><strong>Prioridad</strong> {priority}</div>
          <div class="meta-item"><strong>Estado Actual</strong> {status}</div>
        </div>
      </div>

      <div style="text-align: center;">
        <a href="{cta_url}" class="btn">Acceder al Ticket en Mesa de Ayuda</a>
      </div>
    </div>

    <div class="footer">
      Quantux Salud • Mesa de Ayuda Centralizada y Soporte Clínico Multi-Institucional<br>
      Notificación automática despachada a todos los miembros y solicitantes vinculados al caso.
    </div>
  </div>
</body>
</html>
"""


def _dispatch_email_record(
    ticket_id: str,
    recipient_email: str,
    recipient_role: str,
    subject: str,
    event_type: str,
    body_html: str
) -> EmailNotificationLog:
    """Envía el correo por SMTP si está configurado y lo registra en la base de datos de auditoría forense."""
    sent_status = "SENT"
    error_msg = None

    if SMTP_ENABLED:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = SMTP_FROM
            msg["To"] = recipient_email
            msg.attach(MIMEText(body_html, "html", "utf-8"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_FROM, [recipient_email], msg.as_string())
            logger.info(f"Correo real enviado exitosamente a {recipient_email} para ticket {ticket_id}")
        except Exception as e:
            sent_status = "FAILED"
            error_msg = str(e)
            logger.error(f"Fallo envío SMTP a {recipient_email}: {e}")
    else:
        # Modo Outbox Simulado de Alta Fidelidad para Desarrollo y Demostración
        sent_status = "SENT (Outbox Simulado)"
        logger.info(f"[OUTBOX EMAIL] Disparado a {recipient_email} [{recipient_role}] - Asunto: {subject}")

    # Guardar en base de datos inmutable de auditoría con reintentos para alta concurrencia
    import time
    for attempt in range(3):
        try:
            with Session(engine) as session:
                log_entry = EmailNotificationLog(
                    ticket_id=ticket_id,
                    recipient_email=recipient_email,
                    recipient_role=recipient_role,
                    subject=subject,
                    event_type=event_type,
                    body_html=body_html,
                    sent_status=sent_status,
                    error_message=error_msg,
                    created_at=datetime.utcnow()
                )
                session.add(log_entry)
                session.commit()
                session.refresh(log_entry)
                return log_entry
        except Exception as e:
            if attempt == 2:
                logger.error(f"Fallo persistencia de EmailNotificationLog tras 3 intentos: {e}")
            else:
                time.sleep(0.05 * (attempt + 1))


# ==============================================================================
# DISPARADORES MULTI-DESTINATARIO DE NOVEDADES EN TICKETS (UH-35)
# ==============================================================================

def notify_ticket_created(ticket: Ticket):
    """Notifica a todos los involucrados (solicitante, guardia y supervisión TI) la creación del ticket."""
    with Session(engine) as session:
        recipients = get_all_involved_recipients(ticket, session)
    
    prio_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)
    badge_color = "#DC2626" if prio_val == "P1" else "#2563EB"
    badge_text = f"NUEVO • {prio_val}"
    subject = f"[{prio_val}] Solicitud Registrada: {ticket.id} - {ticket.title}"

    for r in recipients:
        body = _render_email_template(
            title="Confirmación de Registro de Incidente / Requerimiento",
            badge_text=badge_text,
            badge_color=badge_color,
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority=prio_val,
            status="NUEVO",
            recipient_name=r["name"],
            recipient_role=r["role_label"],
            main_message=f"Estimado/a <strong>{r['name']}</strong>:<br><br>Se ha registrado un nuevo ticket en la plataforma <strong>{ticket.platform_code}</strong> para la institución <strong>{ticket.institution_code}</strong>.<br><br><strong>Descripción:</strong> {ticket.description}<br><br>Un operador tomará el caso según la severidad indicada."
        )
        _dispatch_email_record(ticket.id, r["email"], r["role_label"], subject, "TICKET_CREATED", body)

    # Disparar Alerta Roja Crítica P1 si corresponde (UH-35)
    if prio_val == "P1":
        p1_subject = f"🚨 [ALERTA CRÍTICA P1] Incidente Mayor: {ticket.id} - {ticket.title}"
        body_p1 = _render_email_template(
            title="ALERTA CRÍTICA DE MÁXIMA PRIORIDAD (P1)",
            badge_text="EMERGENCIA CRÍTICA • P1",
            badge_color="#DC2626",
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority="P1",
            status="NUEVO",
            recipient_name="Guardia Técnica y Supervisión TI",
            recipient_role="GUARDIA_TI",
            main_message=f"Se ha detectado la apertura de un incidente de severidad <strong>CRÍTICA (P1)</strong> que impacta directamente en la operación asistencial de <strong>{ticket.institution_code}</strong>.<br><br><strong>Descripción:</strong> {ticket.description}<br><br>Tiempo SLA de Respuesta comprometido: &le; 15 minutos."
        )
        _dispatch_email_record(ticket.id, "guardia.soporte@quantuxsalud.com", "GUARDIA_TI", p1_subject, "P1_ALERT", body_p1)


def notify_ticket_assigned(ticket: Ticket, assignee_username: str, support_level: str):
    """Notifica a todos los involucrados (solicitante, operador asignado y participantes) la asignación del ticket."""
    with Session(engine) as session:
        recipients = get_all_involved_recipients(ticket, session, extra_author=assignee_username)
        assignee_info = _get_user_info(assignee_username, session)

    subject = f"[{ticket.id}] Ticket Asignado a {assignee_info['name']} ({support_level})"
    prio_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)

    for r in recipients:
        is_assignee = (r["email"].lower() == assignee_info["email"].lower())
        if is_assignee:
            msg = f"Estimado/a <strong>{r['name']}</strong>:<br><br>Has sido asignado/a como responsable de atención para este caso en Nivel <strong>{support_level}</strong>.<br><br>Por favor inicia el diagnóstico y avanza el estado a 'En Curso' para cumplir con los acuerdos de nivel de servicio (SLA)."
        else:
            msg = f"Estimado/a <strong>{r['name']}</strong>:<br><br>El ticket ha sido tomado por el operador <strong>{assignee_info['name']}</strong> (Nivel {support_level}), quien se encuentra atendiendo la solicitud."

        body = _render_email_template(
            title="Actualización de Asignación de Soporte",
            badge_text=f"ASIGNADO • {support_level}",
            badge_color="#D97706",
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority=prio_val,
            status=ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status),
            recipient_name=r["name"],
            recipient_role=r["role_label"],
            main_message=msg
        )
        _dispatch_email_record(ticket.id, r["email"], r["role_label"], subject, "TICKET_ASSIGNED", body)


def notify_ticket_status_change(ticket: Ticket, old_status: str, new_status: str, reason: str, changed_by_username: Optional[str] = None):
    """Notifica a todos los involucrados cualquier mutación de estado en el ciclo de vida del ticket."""
    with Session(engine) as session:
        recipients = get_all_involved_recipients(ticket, session, extra_author=changed_by_username)

    subject = f"[{ticket.id}] Actualización de Estado: {new_status}"
    prio_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)

    for r in recipients:
        body = _render_email_template(
            title=f"Novedad en Ticket: Transición a {new_status}",
            badge_text=new_status,
            badge_color="#0284C7",
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority=prio_val,
            status=new_status,
            recipient_name=r["name"],
            recipient_role=r["role_label"],
            main_message=f"Estimado/a <strong>{r['name']}</strong>:<br><br>El ticket ha cambiado de estado de <strong>{old_status}</strong> a <strong>{new_status}</strong>.<br><br><strong>Motivo / Observación operativa:</strong> {reason}"
        )
        _dispatch_email_record(ticket.id, r["email"], r["role_label"], subject, "STATUS_CHANGED", body)


def notify_ticket_comment(ticket: Ticket, author_username: str, comment_text: str, is_internal: bool):
    """Notifica a todos los involucrados la publicación de una nueva nota o mensaje en la conversación del ticket."""
    with Session(engine) as session:
        recipients = get_all_involved_recipients(ticket, session, extra_author=author_username)
        author_info = _get_user_info(author_username, session)

    prio_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)
    vis_badge = "NOTA INTERNA" if is_internal else "NUEVO MENSAJE"
    vis_color = "#6366F1" if is_internal else "#0EA5E9"
    subject = f"[{ticket.id}] Mensaje de {author_info['name']} en conversación"

    for r in recipients:
        # Si es nota interna y el destinatario es solicitante puro, no enviar notas internas
        if is_internal and r["role_label"] == "SOLICITANTE":
            continue

        body = _render_email_template(
            title=f"Nueva Interacción en Ticket {ticket.id}",
            badge_text=vis_badge,
            badge_color=vis_color,
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority=prio_val,
            status=ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status),
            recipient_name=r["name"],
            recipient_role=r["role_label"],
            main_message=f"Estimado/a <strong>{r['name']}</strong>:<br><br><strong>{author_info['name']}</strong> ({author_username}) ha agregado un mensaje al ticket:<br><br><blockquote style='margin: 8px 0; padding: 10px; background: #FFFFFF; border-left: 3px solid #0EA5E9; font-style: italic;'>{comment_text}</blockquote>"
        )
        _dispatch_email_record(ticket.id, r["email"], r["role_label"], subject, "COMMENT_ADDED", body)


def notify_ticket_resolved(ticket: Ticket, resolution_notes: str, is_workaround: bool, resolved_by_username: Optional[str] = None):
    """Notifica a todos los involucrados que el caso fue resuelto y se solicita conformidad."""
    with Session(engine) as session:
        recipients = get_all_involved_recipients(ticket, session, extra_author=resolved_by_username)

    prio_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)
    workaround_badge = "<span style='color: #D97706; font-weight: bold;'>[Workaround Provisorio]</span> " if is_workaround else ""
    subject = f"✅ [{ticket.id}] Incidente Resuelto - Conformidad Solicitada"

    for r in recipients:
        body = _render_email_template(
            title="Incidente Resuelto por el Equipo Técnico",
            badge_text="RESUELTO",
            badge_color="#16A34A",
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority=prio_val,
            status="RESUELTO",
            recipient_name=r["name"],
            recipient_role=r["role_label"],
            main_message=f"Estimado/a <strong>{r['name']}</strong>:<br><br>El equipo de soporte ha registrado la solución técnica para este incidente.<br><br><strong>Solución Aplicada:</strong><br>{workaround_badge}{resolution_notes}<br><br><em>Por favor acceda a la plataforma para validar el funcionamiento y confirmar el cierre definitivo.</em>"
        )
        _dispatch_email_record(ticket.id, r["email"], r["role_label"], subject, "TICKET_RESOLVED", body)


def notify_ticket_closed(ticket: Ticket, conformity_feedback: str, closed_by_username: Optional[str] = None):
    """Notifica el cierre formal y definitivo a todos los involucrados."""
    with Session(engine) as session:
        recipients = get_all_involved_recipients(ticket, session, extra_author=closed_by_username)

    prio_val = ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority)
    subject = f"🔒 [{ticket.id}] Ticket Cerrado Definitivamente"

    for r in recipients:
        body = _render_email_template(
            title="Cierre Formal y Archivo de Solicitud",
            badge_text="CERRADO",
            badge_color="#64748B",
            ticket_id=ticket.id,
            ticket_title=ticket.title,
            platform=ticket.platform_code,
            institution=ticket.institution_code,
            priority=prio_val,
            status="CERRADO",
            recipient_name=r["name"],
            recipient_role=r["role_label"],
            main_message=f"Estimado/a <strong>{r['name']}</strong>:<br><br>El ticket <strong>{ticket.id}</strong> ha sido cerrado formalmente en el sistema con conformidad asistencial.<br><br><strong>Comentario de Cierre:</strong> {conformity_feedback}<br><br>Gracias por confiar en Quantux Salud."
        )
        _dispatch_email_record(ticket.id, r["email"], r["role_label"], subject, "TICKET_CLOSED", body)
