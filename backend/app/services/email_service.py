"""
Servicio de Notificaciones y Despacho de Correos Electrónicos
HealthDesk Quantux — Implementación de UH-35
"""

import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from sqlmodel import Session, create_engine

from app.models.entities import Ticket, User, EmailNotificationLog, PriorityLevel, TicketStatus
from app.db.session import engine

logger = logging.getLogger("healthdesk.email")
logger.setLevel(logging.INFO)

# CONFIGURACIÓN SMTP (Variables de Entorno o Fallback Seguro)
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "notificaciones@quantuxsalud.com")
SMTP_ENABLED = bool(SMTP_HOST and SMTP_USER)


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
    main_message: str,
    call_to_action_url: str = "http://127.0.0.1:8000/cockpit"
) -> str:
    """Genera la plantilla HTML responsive con branding de Quantux Salud."""
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F1F5F9; margin: 0; padding: 20px; color: #0F172A; }}
    .email-container {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    .header {{ background-color: #0F1E36; color: #FFFFFF; padding: 18px 24px; display: flex; align-items: center; justify-content: space-between; }}
    .brand {{ font-size: 18px; font-weight: 800; letter-spacing: -0.5px; }}
    .brand span {{ color: #00C4B4; }}
    .badge {{ background-color: {badge_color}; color: #FFFFFF; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; }}
    .content {{ padding: 24px; }}
    .headline {{ font-size: 16px; font-weight: 700; color: #0F1E36; margin-bottom: 12px; }}
    .message-box {{ background-color: #F8FAFC; border-left: 4px solid #00A896; padding: 14px 16px; margin: 16px 0; font-size: 13.5px; line-height: 1.5; color: #334155; border-radius: 0 6px 6px 0; }}
    .ticket-card {{ border: 1px solid #CBD5E1; border-radius: 6px; padding: 14px; margin: 16px 0; background: #FFFFFF; }}
    .ticket-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; }}
    .meta-item strong {{ color: #64748B; font-size: 11px; display: block; text-transform: uppercase; }}
    .btn {{ display: inline-block; background-color: #00A896; color: #FFFFFF; text-decoration: none; padding: 10px 20px; font-weight: 700; font-size: 13px; border-radius: 6px; margin-top: 14px; }}
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
        <a href="{call_to_action_url}" class="btn">Ver en Consola de Mesa de Ayuda</a>
      </div>
    </div>

    <div class="footer">
      Quantux Salud • Sistema Centralizado de Mesa de Ayuda y Soporte Clínico<br>
      Este es un correo automático de notificación asistencial. Por favor no responder directamente a esta casilla.
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
    """Envía el correo por SMTP si está configurado y lo registra en la base de datos de auditoría."""
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
            logger.info(f"Correo real enviado a {recipient_email} para ticket {ticket_id}")
        except Exception as e:
            sent_status = "FAILED"
            error_msg = str(e)
            logger.error(f"Fallo envío SMTP a {recipient_email}: {e}")
    else:
        # Modo Outbox Simulado de Alta Fidelidad para Desarrollo y Demostración
        sent_status = "SENT (Outbox Simulado)"
        logger.info(f"[OUTBOX EMAIL] Disparado a {recipient_email} [{recipient_role}] - Asunto: {subject}")

    # Guardar en base de datos
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


# ==============================================================================
# DISPARADORES ESPECÍFICOS DE NOTIFICACIÓN ASISTENCIAL (UH-35)
# ==============================================================================

def notify_ticket_created(ticket: Ticket, requester_email: Optional[str] = None):
    """Notifica al solicitante la creación del ticket y dispara alerta P1 si es crítico."""
    email = requester_email or f"{ticket.requester_username}@quantuxsalud.com"
    subject = f"[{ticket.priority}] Solicitud Registrada: {ticket.id} - {ticket.title}"
    
    badge_color = "#DC2626" if ticket.priority == PriorityLevel.P1 else "#2563EB"
    badge_text = f"NUEVO • {ticket.priority}"
    
    body = _render_email_template(
        title="Confirmación de Registro de Incidente / Requerimiento",
        badge_text=badge_text,
        badge_color=badge_color,
        ticket_id=ticket.id,
        ticket_title=ticket.title,
        platform=ticket.platform_code,
        institution=ticket.institution_code,
        priority=ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority),
        status="NUEVO",
        main_message=f"Estimado/a <strong>{ticket.requester_username}</strong>:<br><br>Su solicitud ha sido registrada exitosamente en HealthDesk Quantux. Un operador de soporte tomará el caso según la severidad indicada."
    )
    _dispatch_email_record(ticket.id, email, "SOLICITANTE", subject, "TICKET_CREATED", body)

    # Disparar alerta a servicio en producción técnica si es P1
    if ticket.priority == PriorityLevel.P1:
        notify_p1_critical_alert(ticket)


def notify_p1_critical_alert(ticket: Ticket):
    """Alerta roja inmediata para la servicio en producción técnica de soporte ante incidentes P1."""
    guard_email = "servicio en producción.soporte@quantuxsalud.com"
    subject = f"🚨 ALERTA ROJA P1: {ticket.id} en {ticket.platform_code} ({ticket.institution_code})"
    
    body = _render_email_template(
        title="🚨 ALERTA ROJA DE PRODUCCIÓN ASISTENCIAL",
        badge_text="P1 CRÍTICA",
        badge_color="#DC2626",
        ticket_id=ticket.id,
        ticket_title=ticket.title,
        platform=ticket.platform_code,
        institution=ticket.institution_code,
        priority="P1 - Crítica",
        status=ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status),
        main_message=f"<strong>ATENCIÓN PRODUCCIÓN TÉCNICA:</strong><br>Se ha registrado un incidente con impacto asistencial crítico en la plataforma <strong>{ticket.platform_code}</strong> para el cliente <strong>{ticket.institution_code}</strong>.<br><br><strong>Descripción:</strong> {ticket.description}<br><br><em>SLA de Respuesta Inmediata: &lt; 15 minutos.</em>"
    )
    _dispatch_email_record(ticket.id, guard_email, "PRODUCCIÓN_SOPORTE", subject, "P1_ALERT", body)


def notify_ticket_assigned(ticket: Ticket, assignee_username: str, support_level: str, requester_email: Optional[str] = None):
    """Notifica al solicitante que un operador tomó su ticket."""
    email = requester_email or f"{ticket.requester_username}@quantuxsalud.com"
    subject = f"[{ticket.id}] Ticket Tomado por Soporte ({support_level})"
    
    body = _render_email_template(
        title="Operador Asignado a su Solicitud",
        badge_text=f"ASIGNADO • {support_level}",
        badge_color="#D97706",
        ticket_id=ticket.id,
        ticket_title=ticket.title,
        platform=ticket.platform_code,
        institution=ticket.institution_code,
        priority=ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority),
        status="ASIGNADO",
        main_message=f"El operador <strong>{assignee_username}</strong> (Nivel {support_level}) ha tomado su ticket y se encuentra diagnosticando el incidente técnico."
    )
    _dispatch_email_record(ticket.id, email, "SOLICITANTE", subject, "TICKET_ASSIGNED", body)


def notify_ticket_status_change(ticket: Ticket, old_status: str, new_status: str, reason: str, requester_email: Optional[str] = None):
    """Notifica al solicitante cualquier transición de estado del ticket."""
    email = requester_email or f"{ticket.requester_username}@quantuxsalud.com"
    subject = f"[{ticket.id}] Actualización de Estado: {new_status}"
    
    body = _render_email_template(
        title=f"Actualización en su Ticket de Soporte",
        badge_text=new_status,
        badge_color="#0284C7",
        ticket_id=ticket.id,
        ticket_title=ticket.title,
        platform=ticket.platform_code,
        institution=ticket.institution_code,
        priority=ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority),
        status=new_status,
        main_message=f"Su ticket ha cambiado de estado de <strong>{old_status}</strong> a <strong>{new_status}</strong>.<br><br><strong>Motivo / Observación:</strong> {reason}"
    )
    _dispatch_email_record(ticket.id, email, "SOLICITANTE", subject, "STATUS_CHANGED", body)


def notify_ticket_resolved(ticket: Ticket, resolution_notes: str, is_workaround: bool, requester_email: Optional[str] = None):
    """Notifica al solicitante que el ticket fue resuelto para solicitar su conformidad."""
    email = requester_email or f"{ticket.requester_username}@quantuxsalud.com"
    subject = f"✅ [{ticket.id}] Solución Documentada - Conformidad Requerida"
    
    workaround_badge = "<span style='color: #D97706; font-weight: bold;'>[Workaround Provisorio]</span> " if is_workaround else ""
    
    body = _render_email_template(
        title="Incidente Resuelto por el Equipo Técnico",
        badge_text="RESUELTO",
        badge_color="#16A34A",
        ticket_id=ticket.id,
        ticket_title=ticket.title,
        platform=ticket.platform_code,
        institution=ticket.institution_code,
        priority=ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority),
        status="RESUELTO",
        main_message=f"El equipo de soporte ha resuelto su incidente técnico.<br><br><strong>Solución Aplicada:</strong><br>{workaround_badge}{resolution_notes}<br><br><em>Por favor ingrese al sistema para validar el servicio y presionar el botón de Confirmar y Cerrar Ticket.</em>"
    )
    _dispatch_email_record(ticket.id, email, "SOLICITANTE", subject, "TICKET_RESOLVED", body)


def notify_ticket_closed(ticket: Ticket, conformity_feedback: str, requester_email: Optional[str] = None):
    """Notifica el cierre formal y definitivo del ticket."""
    email = requester_email or f"{ticket.requester_username}@quantuxsalud.com"
    subject = f"🔒 [{ticket.id}] Ticket Cerrado Definitivamente"
    
    body = _render_email_template(
        title="Cierre Formal y Archivo de Ticket",
        badge_text="CERRADO",
        badge_color="#64748B",
        ticket_id=ticket.id,
        ticket_title=ticket.title,
        platform=ticket.platform_code,
        institution=ticket.institution_code,
        priority=ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority),
        status="CERRADO",
        main_message=f"El ticket <strong>{ticket.id}</strong> ha sido cerrado definitivamente con su conformidad.<br><br><strong>Comentario de Cierre:</strong> {conformity_feedback}<br><br>Gracias por colaborar con la mejora continua de los servicios asistenciales de Quantux."
    )
    _dispatch_email_record(ticket.id, email, "SOLICITANTE", subject, "TICKET_CLOSED", body)
