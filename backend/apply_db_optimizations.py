#!/usr/bin/env python3
"""
================================================================================
Quantux HealthDesk - Script de Migración, Remediación Relacional e Indexación
================================================================================
Aplica de forma transaccional y no destructiva:
1. Respaldo previo de seguridad.
2. Homologación de entidades referenciales faltantes (users, institutions, platforms)
   para erradicar las violaciones de claves foráneas detectadas.
3. Creación de índices estratégicos de alto rendimiento en tickets, logs y usuarios.
4. Recopilación de estadísticas del optimizador (ANALYZE).
5. Verificación de integridad física y lógica al 100%.
================================================================================
"""

import sqlite3
import time
from pathlib import Path
from backup_db import DatabaseMaintenanceManager

BACKEND_DIR = Path(__file__).resolve().parent
DB_PATH = BACKEND_DIR / "healthdesk.db"

def run_migration():
    print("=================================================================")
    print("QUANTUX HEALTHDESK - MIGRACIÓN Y OPTIMIZACIÓN ESTRUCTURAL DBA")
    print("=================================================================")
    
    # 1. Respaldo de seguridad previo
    print("\n[PASO 1] Creando respaldo de seguridad previo a la optimización...")
    mgr = DatabaseMaintenanceManager(db_path=DB_PATH)
    backup_info = mgr.create_online_backup()
    if not backup_info.get("success"):
        raise RuntimeError(f"Fallo al crear respaldo previo: {backup_info.get('error')}")
    print(f"  -> Respaldo exitoso: {backup_info['backup_file']}")

    conn = sqlite3.connect(str(DB_PATH), timeout=20.0)
    cursor = conn.cursor()

    # 2. Remediación de Datos Referenciales (Foreign Keys)
    print("\n[PASO 2] Remediando entidades referenciales para integridad lógica...")
    
    # Catálogo de usuarios faltantes (triage bot, administradores, doctores de guardia)
    missing_users = [
        ("sistema_triage", "Sistema Automatizado de Triage Clínico", "triage-bot@quantuxsalud.com", "ADMIN", "N3", "jira-admins, soporte-n3"),
        ("cdaneri", "Carla Daneri", "cdaneri@quantux.com", "TEAM_LEADER", "N2", "jefatura-guardia, aprobadores-it"),
        ("analista", "Analista de Guardia Asistencial", "analista@quantuxsalud.com", "SOPORTE", "N1", "soporte-n1, guardia-asistencial"),
        ("f.cortes", "Freddy Cortés", "fcortes@quantuxsalud.com", "ADMIN", "N3", "jira-admins, soporte-n3"),
        ("dr_fernandez", "Dr. Roberto Fernández", "rfernandez@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("dra_gomez", "Dra. Lucía Gómez", "lgomez@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("dr_lopez", "Dr. Alejandro López", "alopez@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("dra_martinez", "Dra. Sofía Martínez", "smartinez@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("dr.garcia", "Dr. Carlos García", "cgarcia@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("dra.lopez", "Dra. Andrea López", "andrea.lopez@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("sgomez", "Dr. Sergio Gómez", "sgomez@hospital.org", "SOLICITANTE", None, "medicos-asistenciales, sol-portal"),
        ("op_qa_1788136528", "Operador QA Automatizado 1", "qa1@quantuxsalud.com", "SOPORTE", "N1", "mesa-de-ayuda"),
        ("op_qa_1788180388", "Operador QA Automatizado 2", "qa2@quantuxsalud.com", "SOPORTE", "N1", "mesa-de-ayuda"),
    ]
    for u, name, email, role, sup, grp in missing_users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, full_name, email, role, support_level, is_active, groups, product_access, created_at)
            VALUES (?, ?, ?, ?, ?, 1, ?, 'Mesa de Ayuda, HCE Clínico', datetime('now'))
        """, (u, name, email, role, sup, grp))

    # Catálogo de instituciones faltantes
    missing_institutions = [
        ("ALEMAN", "Hospital Alemán", "Sanatorio / Clínica"),
        ("BRITANICO", "Hospital Británico", "Sanatorio / Clínica"),
        ("CEMIC", "CEMIC - Centro de Educación Médica e Investigaciones Clínicas", "Sanatorio / Clínica"),
        ("ESPANYOL", "Hospital Español", "Sanatorio / Clínica"),
        ("FAVALORO", "Fundación Favaloro", "Sanatorio / Clínica"),
        ("HOSPITAL_ITALIANO", "Hospital Italiano de Buenos Aires", "Sanatorio / Clínica"),
        ("HOSP_ALEMAN", "Hospital Alemán (Sede Central)", "Sanatorio / Clínica"),
        ("HOSP_BRITANICO", "Hospital Británico de Buenos Aires", "Sanatorio / Clínica"),
        ("INST_CENTRAL", "Instituto Médico Central", "Sanatorio / Clínica"),
        ("IOMA", "IOMA - Instituto de Obra Médico Asistencial", "Financiador"),
        ("ITALIANO", "Hospital Italiano", "Sanatorio / Clínica"),
        ("MATER_DEI", "Sanatorio Mater Dei", "Sanatorio / Clínica"),
        ("MEDICUS", "Medicus Medicina Privada", "Financiador"),
        ("OTAMENDI", "Sanatorio Otamendi", "Sanatorio / Clínica"),
        ("PAMI", "PAMI - INSSJP", "Financiador"),
        ("SANAT_FINOCHIETTO", "Sanatorio Finochietto", "Sanatorio / Clínica"),
        ("SANAT_MATER_DEI", "Sanatorio Mater Dei", "Sanatorio / Clínica"),
        ("SANAT_OTAMENDI", "Sanatorio Otamendi y Miroli", "Sanatorio / Clínica"),
        ("SWISS_MED", "Swiss Medical Medicina Privada", "Financiador"),
        ("TRINIDAD_PAL", "Sanatorio de la Trinidad Palermo", "Sanatorio / Clínica")
    ]
    for code, name, segment in missing_institutions:
        cursor.execute("""
            INSERT OR IGNORE INTO institutions (code, name, segment, is_active)
            VALUES (?, ?, ?, 1)
        """, (code, name, segment))

    # Catálogo de plataformas faltantes
    missing_platforms = [
        ("CAT_APIs_EXTERNAS", "APIs Externas y Microservicios", "Integraciones con APIs de terceros y pasarelas"),
        ("CAT_CORE_CLINICO", "Core Clínico y Procesos Asistenciales", "Motor asistencial principal"),
        ("CAT_HCE", "Historia Clínica Electrónica (HCE)", "Historia clínica unificada y evoluciones médicas"),
        ("CAT_INFRA_NUBE", "Infraestructura Cloud y Red Asistencial", "Servicios de nube y redes clínicas"),
        ("CAT_INTEGRACIONES_HL7", "Integraciones HL7 / FHIR", "Pasarela de mensajería HL7 estándar"),
        ("CAT_INTEROPERABILIDAD_HL7", "Interoperabilidad HL7 FHIR v4", "Interoperabilidad nacional HL7 FHIR"),
        ("CAT_LAB", "Sistema de Laboratorio Asistencial (LIS)", "Gestión de analizadores clínicos y resultados de laboratorio"),
        ("CAT_PORTAL", "Portal Web de Profesionales", "Acceso web para médicos y profesionales de guardia"),
        ("CAT_PORTAL_PACIENTE", "Portal del Paciente Web y Móvil", "Portal de pacientes para turnos y recetas"),
        ("CAT_PORTAL_PACIENTES", "Portal Integral de Pacientes", "Plataforma de autogestión para pacientes"),
        ("CAT_RECETA_DIGITAL", "Receta Digital Homologada", "Prescripción electrónica con firma PKI"),
        ("CAT_TELEMED", "Telemedicina y Videoconsultas", "Consultas virtuales y sala de espera digital"),
        ("CAT_TURNO", "Gestión de Turnos y Agendas Médicas", "Cartilla médica y reservas ambulatorias"),
        ("CAT_VALIDA", "Validación de Elegibilidad y Padrón", "Validador en línea de afiliación médica"),
        ("CD2", "Consultorio Digital v2", "Versión avanzada de consultorio médico digital"),
        ("CONSULTORIO_DIGITAL", "Consultorio Digital", "Módulo de atención remota"),
        ("CORE_EMR", "Core EMR / Registro Médico", "Registro médico electrónico central"),
        ("PLAT_RECETA_E", "Plataforma de Receta Electrónica", "Servicio unificado de recetas electrónicas"),
        ("RECETAS_MEDICAS", "Módulo de Prescripciones y Recetas Médicas", "Emisión de recetas y vademécum"),
        ("Receta Digital", "Receta Digital (Módulo Clínico)", "Módulo de emisión asistencial de prescripciones")
    ]
    for code, name, desc in missing_platforms:
        cursor.execute("""
            INSERT OR IGNORE INTO platforms (code, name, description, is_active)
            VALUES (?, ?, ?, 1)
        """, (code, name, desc))

    conn.commit()
    print("  -> Registros referenciales insertados correctamente.")

    # 3. Creación de Índices Estratégicos
    print("\n[PASO 3] Creando índices estratégicos para optimización de consultas...")
    strategic_indexes = [
        ("ix_tickets_created_at", "CREATE INDEX IF NOT EXISTS ix_tickets_created_at ON tickets(created_at DESC);"),
        ("ix_tickets_assignee_username", "CREATE INDEX IF NOT EXISTS ix_tickets_assignee_username ON tickets(assignee_username);"),
        ("ix_tickets_assignee_status", "CREATE INDEX IF NOT EXISTS ix_tickets_assignee_status ON tickets(assignee_username, status);"),
        ("ix_tickets_requester_username", "CREATE INDEX IF NOT EXISTS ix_tickets_requester_username ON tickets(requester_username);"),
        ("ix_tickets_priority_status", "CREATE INDEX IF NOT EXISTS ix_tickets_priority_status ON tickets(priority, status);"),
        ("ix_tickets_status_created_at", "CREATE INDEX IF NOT EXISTS ix_tickets_status_created_at ON tickets(status, created_at DESC);"),
        ("ix_tickets_parent_ticket_id", "CREATE INDEX IF NOT EXISTS ix_tickets_parent_ticket_id ON tickets(parent_ticket_id);"),
        ("ix_tickets_resolved_at", "CREATE INDEX IF NOT EXISTS ix_tickets_resolved_at ON tickets(resolved_at);"),
        ("ix_tickets_release_tag", "CREATE INDEX IF NOT EXISTS ix_tickets_release_tag ON tickets(release_tag);"),
        ("ix_ticket_audit_log_ticket_created", "CREATE INDEX IF NOT EXISTS ix_ticket_audit_log_ticket_created ON ticket_audit_log(ticket_id, created_at ASC);"),
        ("ix_ticket_audit_log_changed_by", "CREATE INDEX IF NOT EXISTS ix_ticket_audit_log_changed_by ON ticket_audit_log(changed_by_username);"),
        ("ix_ticket_comments_ticket_created", "CREATE INDEX IF NOT EXISTS ix_ticket_comments_ticket_created ON ticket_comments(ticket_id, created_at ASC);"),
        ("ix_email_logs_ticket_created", "CREATE INDEX IF NOT EXISTS ix_email_logs_ticket_created ON email_notification_logs(ticket_id, created_at DESC);"),
        ("ix_email_logs_sent_status", "CREATE INDEX IF NOT EXISTS ix_email_logs_sent_status ON email_notification_logs(sent_status);"),
        ("ix_users_role_is_active", "CREATE INDEX IF NOT EXISTS ix_users_role_is_active ON users(role, is_active);")
    ]

    for name, sql in strategic_indexes:
        t0 = time.time()
        cursor.execute(sql)
        dt = round((time.time() - t0) * 1000, 2)
        print(f"  -> Índice {name}: creado/verificado ({dt} ms)")

    conn.commit()

    # 4. Actualización de estadísticas del Optimizador
    print("\n[PASO 4] Ejecutando ANALYZE para estadísticas de distribución del planificador...")
    cursor.execute("ANALYZE;")
    conn.commit()

    # 5. Verificación de Integridad Física y Lógica
    print("\n[PASO 5] Verificando integridad física y lógica post-optimización...")
    cursor.execute("PRAGMA integrity_check;")
    ic = cursor.fetchall()
    print(f"  -> PRAGMA integrity_check: {ic}")

    cursor.execute("PRAGMA foreign_key_check;")
    fks = cursor.fetchall()
    print(f"  -> PRAGMA foreign_key_check: {len(fks)} violaciones restantes")
    if fks:
        for f in fks[:5]:
            print("     Restante:", f)

    conn.close()

    print("\n=================================================================")
    if ic == [("ok",)] and len(fks) == 0:
        print("MIGRACIÓN Y OPTIMIZACIÓN COMPLETADA CON ÉXITO: 100% SALUDABLE")
    else:
        print("ADVERTENCIA: Se encontraron inconsistencias residuales.")
    print("=================================================================")

if __name__ == "__main__":
    run_migration()
