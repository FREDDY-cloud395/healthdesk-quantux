from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, delete
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import unicodedata

from app.db.session import get_session
from app.models.entities import Platform, Institution, ImpactLevel, UrgencyLevel, PriorityLevel, KBArticle, KBArticleHistory, Ticket
from app.core.fsm import calculate_priority

router = APIRouter()

def normalize_text(s: str) -> str:
    if not s:
        return ""
    nfkd = unicodedata.normalize('NFKD', s)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

@router.get("/platforms", response_model=List[Platform])
def list_platforms(session: Session = Depends(get_session)):
    return session.exec(select(Platform).where(Platform.is_active == True)).all()

class PlatformCreateRequest(BaseModel):
    code: str
    name: str
    description: Optional[str] = ""

@router.post("/platforms", response_model=Platform)
def create_platform(req: PlatformCreateRequest, session: Session = Depends(get_session)):
    clean_code = req.code.strip().upper()
    if not clean_code or not req.name.strip():
        raise HTTPException(status_code=400, detail="El código y nombre de la plataforma son obligatorios.")
    existing = session.exec(select(Platform).where(Platform.code == clean_code)).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Ya existe una plataforma con el código '{clean_code}'.")
    plat = Platform(
        code=clean_code,
        name=req.name.strip(),
        description=req.description.strip() if req.description else "",
        is_active=True
    )
    session.add(plat)
    session.commit()
    session.refresh(plat)
    return plat

@router.get("/institutions", response_model=List[Institution])
def list_institutions(session: Session = Depends(get_session)):
    return session.exec(select(Institution).where(Institution.is_active == True)).all()

class InstitutionCreateRequest(BaseModel):
    code: str
    name: str
    segment: Optional[str] = "Sanatorio / Clínica"

@router.post("/institutions", response_model=Institution)
def create_institution(req: InstitutionCreateRequest, session: Session = Depends(get_session)):
    clean_code = req.code.strip().upper()
    if not clean_code or not req.name.strip():
        raise HTTPException(status_code=400, detail="El código y nombre de la institución son obligatorios.")
    existing = session.exec(select(Institution).where(Institution.code == clean_code)).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Ya existe una institución/cliente con el código '{clean_code}'.")
    inst = Institution(
        code=clean_code,
        name=req.name.strip(),
        segment=req.segment.strip() if req.segment else "Sanatorio / Clínica",
        is_active=True
    )
    session.add(inst)
    session.commit()
    session.refresh(inst)
    return inst

class PriorityCalculationResponse(BaseModel):
    impact: ImpactLevel
    urgency: UrgencyLevel
    priority: PriorityLevel
    sla_response_time_minutes: int
    sla_resolution_time_minutes: int

@router.get("/calculate-priority", response_model=PriorityCalculationResponse)
def get_calculated_priority(impact: ImpactLevel, urgency: UrgencyLevel):
    priority = calculate_priority(impact, urgency)
    p_val = priority.value if hasattr(priority, "value") else str(priority)
    sla_map = {
        "P1": (15, 60),
        "P2": (30, 120),
        "P3": (60, 240),
        "P4": (120, 480),
        "P5": (240, 1440)
    }
    resp_m, resol_m = sla_map.get(p_val, (60, 240))
    return {
        "impact": impact,
        "urgency": urgency,
        "priority": priority,
        "sla_response_time_minutes": resp_m,
        "sla_resolution_time_minutes": resol_m
    }

# =============================================================================
# BASE DE CONOCIMIENTO (KNOWLEDGE BASE ARTICLES - CRUD, VERSIONING & HISTORIAL)
# =============================================================================
class ArticleCreateRequest(BaseModel):
    title: str
    category: str
    content: str
    author_username: Optional[str] = "admin"
    tags: Optional[str] = None
    version: Optional[str] = "v1.0"
    changelog: Optional[str] = "Versión inicial homologada"
    source_ticket_id: Optional[str] = None
    space_name: Optional[str] = "Guías y Documentación de Soporte Asistencial"
    requests_deflected: Optional[int] = 0
    helpful_score: Optional[int] = 95

class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    author_username: Optional[str] = "admin"
    tags: Optional[str] = None
    version: Optional[str] = None
    changelog: Optional[str] = "Actualización de protocolo"
    increment_type: Optional[str] = "minor" # "patch", "minor", "major"

class ArticleFromTicketRequest(BaseModel):
    ticket_id: str
    title: str
    category: str
    content: str
    author_username: Optional[str] = "soporte"
    tags: Optional[str] = None
    changelog: Optional[str] = "Promovido desde resolución de ticket asistencial"

def _ensure_kb_seed(session: Session):
    existing_count = len(session.exec(select(KBArticle)).all())
    if existing_count < 20:
        seed_data = [
            {
                "article": KBArticle(
                    id=1,
                    title="Procedimiento ante Caída del WS de Firma Digital de Recetas (OSDE / Swiss Medical)",
                    category="Receta Digital",
                    content="1. Validar estado del WebService del Colegio de Farmacéuticos y certificadora de firma electrónica.\n2. En caso de timeout > 30 seg, conmutar al modo de emisión con Código Seguro de Verificación (CSV) y QR offline homologado.\n3. Notificar a las farmacias de la red el uso del talonario de contingencia según resolución sanitaria 2026-MSAL.\n4. Registrar ticket en N2 para seguimiento de reconexión y conciliación de recetas en cola.",
                    author_username="admin",
                    tags="receta,firma-digital,farmacia,osde,swiss_medical,contingencia,v2.4",
                    version="v2.4",
                    changelog="Actualización del fallback a código seguro CSV homologado con farmacias de la red",
                    view_count=142,
                    created_at=datetime(2026, 8, 25, 10, 30),
                    updated_at=datetime(2026, 8, 30, 16, 20)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=1,
                        version="v1.0",
                        title="Procedimiento ante Caída del WS de Firma de Recetas",
                        category="Receta Digital",
                        content="1. Validar estado del WS de firma.\n2. Notificar a farmacias el uso de talonario manual.\n3. Abrir ticket en mesa de ayuda.",
                        author_username="admin",
                        tags="receta,firma-digital,v1.0",
                        changelog="Creación inicial del protocolo de recetas digitales",
                        created_at=datetime(2026, 8, 10, 9, 0)
                    ),
                    KBArticleHistory(
                        article_id=1,
                        version="v2.0",
                        title="Procedimiento ante Caída del WS de Firma Digital de Recetas (OSDE / Swiss)",
                        category="Receta Digital",
                        content="1. Validar estado del WebService de certificadora.\n2. Activar modo contingencia QR.\n3. Notificar farmacias de red OSDE y Swiss Medical.",
                        author_username="soporte",
                        tags="receta,firma-digital,contingencia,v2.0",
                        changelog="Inclusión de soporte multi-entidad (OSDE / Swiss Medical)",
                        created_at=datetime(2026, 8, 18, 11, 45)
                    ),
                    KBArticleHistory(
                        article_id=1,
                        version="v2.4",
                        title="Procedimiento ante Caída del WS de Firma Digital de Recetas (OSDE / Swiss Medical)",
                        category="Receta Digital",
                        content="1. Validar estado del WebService del Colegio de Farmacéuticos y certificadora de firma electrónica.\n2. En caso de timeout > 30 seg, conmutar al modo de emisión con Código Seguro de Verificación (CSV) y QR offline homologado.\n3. Notificar a las farmacias de la red el uso del talonario de contingencia según resolución sanitaria 2026-MSAL.\n4. Registrar ticket en N2 para seguimiento de reconexión y conciliación de recetas en cola.",
                        author_username="admin",
                        tags="receta,firma-digital,farmacia,osde,swiss_medical,contingencia,v2.4",
                        changelog="Actualización del fallback a código seguro CSV homologado con farmacias de la red",
                        created_at=datetime(2026, 8, 25, 10, 30)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=2,
                    title="Diagnóstico WebRTC y Fallo de Audio/Video en Consultas de Telemedicina",
                    category="Telemedicina",
                    content="1. Verificar permisos de cámara y micrófono en el navegador (Chrome, Safari iOS, Edge).\n2. Si el paciente experimenta pantalla negra en Safari, forzar codec de video H.264 fallback.\n3. Validar prueba de velocidad (requerimiento mínimo: 3 Mbps simétricos y jitter < 30ms).\n4. Si persiste desconexión, derivar a la sala de espera alternativa o llamada telefónica de respaldo.",
                    author_username="soporte",
                    tags="telemedicina,webrtc,audio,video,safari,chrome,v1.8",
                    version="v1.8",
                    changelog="Añadido paso para forzar codec H.264 en Safari iOS 19",
                    view_count=98,
                    created_at=datetime(2026, 8, 26, 14, 15),
                    updated_at=datetime(2026, 8, 29, 12, 10)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=2,
                        version="v1.0",
                        title="Diagnóstico WebRTC en Telemedicina",
                        category="Telemedicina",
                        content="1. Verificar permisos de micrófono y cámara en Chrome.\n2. Reiniciar pestaña del navegador.",
                        author_username="soporte",
                        tags="telemedicina,webrtc",
                        changelog="Creación de guía básica para agentes de soporte N1",
                        created_at=datetime(2026, 8, 12, 15, 0)
                    ),
                    KBArticleHistory(
                        article_id=2,
                        version="v1.8",
                        title="Diagnóstico WebRTC y Fallo de Audio/Video en Consultas de Telemedicina",
                        category="Telemedicina",
                        content="1. Verificar permisos de cámara y micrófono en el navegador (Chrome, Safari iOS, Edge).\n2. Si el paciente experimenta pantalla negra en Safari, forzar codec de video H.264 fallback.\n3. Validar prueba de velocidad (requerimiento mínimo: 3 Mbps simétricos y jitter < 30ms).\n4. Si persiste desconexión, derivar a la sala de espera alternativa o llamada telefónica de respaldo.",
                        author_username="soporte",
                        tags="telemedicina,webrtc,audio,video,safari,chrome,v1.8",
                        changelog="Añadido paso para forzar codec H.264 en Safari iOS 19",
                        created_at=datetime(2026, 8, 26, 14, 15)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=3,
                    title="Historia Clínica Electrónica: Liberación de Bloqueo Concurrente y Consultorio",
                    category="Historia Clínica",
                    content="1. Las fichas ambulatorias y evoluciones de internación cuentan con bloqueo por concurrencia médica con TTL de 5 minutos.\n2. Si el profesional cerró la ventana sin guardar o se cortó el suministro, el candado se libera automáticamente al expirar el TTL.\n3. Para desbloqueo forzado inmediato, el operador N2 con rol ADMIN puede ingresar a Supervisión de Sesiones y presionar 'Liberar Bloqueo'.",
                    author_username="admin",
                    tags="hce,consultorio,bloqueo,candado,concurrencia,v3.1",
                    version="v3.1",
                    changelog="Reducción de TTL de candado de 15 min a 5 min y habilitación de botón de desbloqueo N2",
                    view_count=215,
                    created_at=datetime(2026, 8, 27, 9, 0),
                    updated_at=datetime(2026, 8, 31, 8, 40)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=3,
                        version="v1.0",
                        title="Historia Clínica: Desbloqueo de Fichas",
                        category="Historia Clínica",
                        content="1. Esperar 30 minutos a que expire el candado de base de datos.",
                        author_username="admin",
                        tags="hce,bloqueo",
                        changelog="Guía inicial de soporte HCE",
                        created_at=datetime(2026, 8, 14, 10, 0)
                    ),
                    KBArticleHistory(
                        article_id=3,
                        version="v2.0",
                        title="Historia Clínica: Bloqueo de Concurrencia Médica",
                        category="Historia Clínica",
                        content="1. TTL reducido a 15 min.\n2. Contactar a DBA para kill session.",
                        author_username="soporte",
                        tags="hce,concurrencia",
                        changelog="Optimización con scripts automáticos DBA",
                        created_at=datetime(2026, 8, 20, 16, 30)
                    ),
                    KBArticleHistory(
                        article_id=3,
                        version="v3.1",
                        title="Historia Clínica Electrónica: Liberación de Bloqueo Concurrente y Consultorio",
                        category="Historia Clínica",
                        content="1. Las fichas ambulatorias y evoluciones de internación cuentan con bloqueo por concurrencia médica con TTL de 5 minutos.\n2. Si el profesional cerró la ventana sin guardar o se cortó el suministro, el candado se libera automáticamente al expirar el TTL.\n3. Para desbloqueo forzado inmediato, el operador N2 con rol ADMIN puede ingresar a Supervisión de Sesiones y presionar 'Liberar Bloqueo'.",
                        author_username="admin",
                        tags="hce,consultorio,bloqueo,candado,concurrencia,v3.1",
                        changelog="Reducción de TTL de candado de 15 min a 5 min y habilitación de botón de desbloqueo N2",
                        created_at=datetime(2026, 8, 27, 9, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=4,
                    title="Protocolo de Contingencia Mayor P1 en Guardias Hospitalarias y Quirófanos",
                    category="Contingencias",
                    content="1. TIEMPO MÁXIMO DE RESPUESTA: 15 minutos.\n2. Abrir canal de crisis en equipo de guardia #911-SOPORTE-CRITICO.\n3. Activar cluster de respaldo en caliente (Hot Standby) y desviar tráfico de admisión a servidores locales.\n4. Emitir comunicado formal al Jefe de Guardia y Dirección Médica cada 30 minutos hasta el cierre definitivo.",
                    author_username="admin",
                    tags="p1,emergencia,quirofano,guardia,alta-disponibilidad,v4.0",
                    version="v4.0",
                    changelog="Inclusión de canal de crisis automatizado #911 y bypass de admisión hospitalaria",
                    view_count=312,
                    created_at=datetime(2026, 8, 28, 16, 45),
                    updated_at=datetime(2026, 8, 31, 11, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=4,
                        version="v1.0",
                        title="Protocolo de Incidentes Críticos en Guardia",
                        category="Contingencias",
                        content="1. Comunicar al facilitador técnico de guardia en menos de 30 minutos.",
                        author_username="admin",
                        tags="p1,guardia",
                        changelog="Línea base de incidentes mayores",
                        created_at=datetime(2026, 8, 15, 8, 0)
                    ),
                    KBArticleHistory(
                        article_id=4,
                        version="v4.0",
                        title="Protocolo de Contingencia Mayor P1 en Guardias Hospitalarias y Quirófanos",
                        category="Contingencias",
                        content="1. TIEMPO MÁXIMO DE RESPUESTA: 15 minutos.\n2. Abrir canal de crisis en equipo de guardia #911-SOPORTE-CRITICO.\n3. Activar cluster de respaldo en caliente (Hot Standby) y desviar tráfico de admisión a servidores locales.\n4. Emitir comunicado formal al Jefe de Guardia y Dirección Médica cada 30 minutos hasta el cierre definitivo.",
                        author_username="admin",
                        tags="p1,emergencia,quirofano,guardia,alta-disponibilidad,v4.0",
                        changelog="Inclusión de canal de crisis automatizado #911 y bypass de admisión hospitalaria",
                        created_at=datetime(2026, 8, 28, 16, 45)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=5,
                    title="Pasarela de Copagos y Pagos Online: Conciliación de Transacciones y Reintentos",
                    category="Facturación y Pagos",
                    content="1. Verificar estado de la pasarela de pagos (Gateway status code 200/402).\n2. Si el paciente fue debitado pero el coseguro figura 'Pendiente', ejecutar reconciliación manual mediante webhook de auditoría.\n3. No generar doble cargo: el sistema reintenta la validación bancaria automáticamente en ventanas de 15 minutos.",
                    author_username="soporte",
                    tags="copagos,pagos,coseguro,pasarela,tarjetas,v2.0",
                    version="v2.0",
                    changelog="Integración con webhook de conciliación bancaria instantánea",
                    view_count=84,
                    created_at=datetime(2026, 8, 29, 11, 20),
                    updated_at=datetime(2026, 8, 30, 14, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=5,
                        version="v1.0",
                        title="Pasarela de Copagos: Errores Comunes",
                        category="Facturación y Pagos",
                        content="1. Revisar estado bancario en el panel de la pasarela.",
                        author_username="soporte",
                        tags="copagos,pagos",
                        changelog="Publicación inicial",
                        created_at=datetime(2026, 8, 16, 12, 0)
                    ),
                    KBArticleHistory(
                        article_id=5,
                        version="v2.0",
                        title="Pasarela de Copagos y Pagos Online: Conciliación de Transacciones y Reintentos",
                        category="Facturación y Pagos",
                        content="1. Verificar estado de la pasarela de pagos (Gateway status code 200/402).\n2. Si el paciente fue debitado pero el coseguro figura 'Pendiente', ejecutar reconciliación manual mediante webhook de auditoría.\n3. No generar doble cargo: el sistema reintenta la validación bancaria automáticamente en ventanas de 15 minutos.",
                        author_username="soporte",
                        tags="copagos,pagos,coseguro,pasarela,tarjetas,v2.0",
                        changelog="Integración con webhook de conciliación bancaria instantánea",
                        created_at=datetime(2026, 8, 29, 11, 20)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=6,
                    title="Interoperabilidad HL7 / FHIR: Trazabilidad y Sincronización con Financiadores",
                    category="Interoperabilidad",
                    content="1. Inspeccionar logs de mensajes FHIR Bundle (Resource: Patient / Encounter / MedicationRequest).\n2. Errores 422 (Unprocessable Entity) indican falta de mapeo SNOMED-CT o identificador de prestador inválido.\n3. Reencolar mensajes fallidos desde la cola de reintentos (Dead Letter Queue) una vez corregido el maestro.",
                    author_username="admin",
                    tags="hl7,fhir,interoperabilidad,snomed,financiadores,v1.9",
                    version="v1.9",
                    changelog="Mapeo ampliado de terminologías clínicas SNOMED-CT a CIE-10",
                    view_count=110,
                    created_at=datetime(2026, 8, 30, 8, 10),
                    updated_at=datetime(2026, 8, 31, 9, 15)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=6,
                        version="v1.0",
                        title="Interoperabilidad HL7 FHIR: Diagnóstico de Errores",
                        category="Interoperabilidad",
                        content="1. Verificar logs del motor de mensajería.",
                        author_username="admin",
                        tags="hl7,fhir",
                        changelog="Línea base de interoperabilidad",
                        created_at=datetime(2026, 8, 17, 10, 0)
                    ),
                    KBArticleHistory(
                        article_id=6,
                        version="v1.9",
                        title="Interoperabilidad HL7 / FHIR: Trazabilidad y Sincronización con Financiadores",
                        category="Interoperabilidad",
                        content="1. Inspeccionar logs de mensajes FHIR Bundle (Resource: Patient / Encounter / MedicationRequest).\n2. Errores 422 (Unprocessable Entity) indican falta de mapeo SNOMED-CT o identificador de prestador inválido.\n3. Reencolar mensajes fallidos desde la cola de reintentos (Dead Letter Queue) una vez corregido el maestro.",
                        author_username="admin",
                        tags="hl7,fhir,interoperabilidad,snomed,financiadores,v1.9",
                        changelog="Mapeo ampliado de terminologías clínicas SNOMED-CT a CIE-10",
                        created_at=datetime(2026, 8, 30, 8, 10)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=7,
                    title="Consultorio Digital: Alta de Prestadores Médicos y Matrículas Provinciales",
                    category="Consultorio Digital",
                    content="1. Validar matrícula nacional / provincial en el Registro Federal de Profesionales de la Salud (REFEPS).\n2. Cargar especialidad homologada y asociar la cartilla del financiador correspondiente.\n3. Enviar credenciales temporales con doble factor de autenticación (2FA) por SMS/Email institucional.",
                    author_username="soporte",
                    tags="consultorio,medicos,matricula,refeps,alta-usuarios,v2.2",
                    version="v2.2",
                    changelog="Validación automática con base REFEPS y enrolamiento 2FA",
                    view_count=76,
                    created_at=datetime(2026, 8, 30, 18, 0),
                    updated_at=datetime(2026, 8, 31, 10, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=7,
                        version="v1.0",
                        title="Alta de Médicos en Consultorio Digital",
                        category="Consultorio Digital",
                        content="1. Cargar datos personales del profesional y asignar rol.",
                        author_username="soporte",
                        tags="consultorio,alta",
                        changelog="Procedimiento inicial",
                        created_at=datetime(2026, 8, 19, 14, 0)
                    ),
                    KBArticleHistory(
                        article_id=7,
                        version="v2.2",
                        title="Consultorio Digital: Alta de Prestadores Médicos y Matrículas Provinciales",
                        category="Consultorio Digital",
                        content="1. Validar matrícula nacional / provincial en el Registro Federal de Profesionales de la Salud (REFEPS).\n2. Cargar especialidad homologada y asociar la cartilla del financiador correspondiente.\n3. Enviar credenciales temporales con doble factor de autenticación (2FA) por SMS/Email institucional.",
                        author_username="soporte",
                        tags="consultorio,medicos,matricula,refeps,alta-usuarios,v2.2",
                        changelog="Validación automática con base REFEPS y enrolamiento 2FA",
                        created_at=datetime(2026, 8, 30, 18, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=8,
                    title="Procedimiento de Rollback y Modo Autónomo ante Interrupción de Base de Datos",
                    category="Contingencias",
                    content="1. Si la réplica principal de base de datos no responde, conmutar a lectura en nodo secundario.\n2. Las estaciones locales de guardia entran automáticamente en Modo Autónomo SQLite con sincronización diferida.\n3. Al restablecer conectividad, el servicio de sincronización fusiona los registros por vector clock sin pérdida de datos.",
                    author_username="admin",
                    tags="rollback,base-de-datos,contingencia,offline,sqlite,v3.5",
                    version="v3.5",
                    changelog="Fusión por Vector Clock y resguardo de evoluciones médicas offline",
                    view_count=189,
                    created_at=datetime(2026, 8, 31, 7, 30),
                    updated_at=datetime(2026, 8, 31, 12, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=8,
                        version="v1.0",
                        title="Modo Autónomo Local por Corte de BD",
                        category="Contingencias",
                        content="1. Cambiar configuración a modo local en cada estación.",
                        author_username="admin",
                        tags="contingencia,offline",
                        changelog="Procedimiento manual de emergencia",
                        created_at=datetime(2026, 8, 16, 8, 0)
                    ),
                    KBArticleHistory(
                        article_id=8,
                        version="v3.5",
                        title="Procedimiento de Rollback y Modo Autónomo ante Interrupción de Base de Datos",
                        category="Contingencias",
                        content="1. Si la réplica principal de base de datos no responde, conmutar a lectura en nodo secundario.\n2. Las estaciones locales de guardia entran automáticamente en Modo Autónomo SQLite con sincronización diferida.\n3. Al restablecer conectividad, el servicio de sincronización fusiona los registros por vector clock sin pérdida de datos.",
                        author_username="admin",
                        tags="rollback,base-de-datos,contingencia,offline,sqlite,v3.5",
                        changelog="Fusión por Vector Clock y resguardo de evoluciones médicas offline",
                        created_at=datetime(2026, 8, 31, 7, 30)
                    )
                ]
            }
            ,
            {
                "article": KBArticle(
                    id=9,
                    title="SOP-CD2-001: Gestión y Selección de Matrículas (SISA / CRM)",
                    category="Consultorio Digital",
                    content="1. Selector Bloqueado en Interfaz: Si el profesional tiene su matrícula por defecto inhabilitada pero cuenta con otra matrícula activa en SISA, la interfaz desbloquea automáticamente el menú desplegable para permitirle elegir la matrícula habilitada para prescribir.\n2. Inconsistencias y Matrículas Ficticias en CRM: Cuando se detecten matrículas con dígitos adicionales (como un 0 adelante o un 1 al final) generadas para saltear duplicados tras cambios de CUIT (nacional vs extranjero), tramitar formalmente la unificación de Identificadores Comerciales (ICs) vía ticket PAU a Soporte CRM/MDA (ej. PAU #895833).\n3. Contingencia Urgente en Base de Datos: Para destrabar bloqueos inmediatos en producción, ejecutar actualización en BD de CD2 replicando de forma exacta los campos del objeto matriculaSISA dentro de defaultMatricula.\n4. Criterio de Habilitación: El sistema toma de forma estricta y exclusiva el estado 'Habilitada' para habilitar recetas, prescindiendo de la fecha de caducidad.",
                    author_username="admin",
                    tags="cd2,sisa,crm,matricula,selector,pau,habilitada,v1.0",
                    version="v1.0",
                    changelog="Protocolo oficial de gestión de matrículas y contingencia SISA/CRM para CD2",
                    view_count=84,
                    created_at=datetime(2026, 9, 10, 10, 0),
                    updated_at=datetime(2026, 9, 15, 14, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=9,
                        version="v1.0",
                        title="SOP-CD2-001: Gestión y Selección de Matrículas (SISA / CRM)",
                        category="Consultorio Digital",
                        content="1. Selector Bloqueado: Desbloqueo automático condicional.\n2. Matrículas Ficticias: Unificación de ICs vía ticket PAU a CRM.\n3. Contingencia BD: Replicar matriculaSISA en defaultMatricula.\n4. Validación: Solo estado Habilitada.",
                        author_username="admin",
                        tags="cd2,sisa,crm,matricula,v1.0",
                        changelog="Creación del protocolo de matrículas CD2",
                        created_at=datetime(2026, 9, 10, 10, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=10,
                    title="SOP-CD2-002: Videoconsulta, Sala de Espera y Conectividad (Jitsi)",
                    category="Consultorio Digital",
                    content="1. Reconexión y joinTimeout (Spinner eterno): El sistema cuenta con algoritmo de reconexión transparente en background limitado a 5 reintentos con intervalos de 20 segundos para prevenir bucles infinitos por microcortes o suspensión en móviles. Si no reconecta al 5to intento, instruir al usuario a refrescar pantalla o reingresar a sala de espera.\n2. Miniatura Propia (Self-view) y Permisos: Ejecutar validación pre-check de hardware. Verificar que la cámara y el micrófono no estén bloqueados por el navegador. Se aplica fix en el iframe de Jitsi para la visualización de la miniatura de video del prestador.\n3. Prevención de Cierre Accidental: Se incluye diálogo modal de confirmación obligatorio antes de cerrar la ventana de atención para evitar expulsar involuntariamente al paciente.",
                    author_username="soporte",
                    tags="cd2,videoconsulta,jitsi,conectividad,jointimeout,permisos,camara,v1.0",
                    version="v1.0",
                    changelog="Protocolo de videoconsulta, reconexión Jitsi y permisos de periféricos",
                    view_count=112,
                    created_at=datetime(2026, 9, 10, 11, 0),
                    updated_at=datetime(2026, 9, 16, 9, 30)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=10,
                        version="v1.0",
                        title="SOP-CD2-002: Videoconsulta, Sala de Espera y Conectividad (Jitsi)",
                        category="Consultorio Digital",
                        content="1. Reconexión Jitsi: 5 reintentos cada 20s.\n2. Permisos y Self-view: Pre-check de periféricos y fix en iframe.\n3. Cierre accidental: Modal de confirmación obligatorio.",
                        author_username="soporte",
                        tags="cd2,videoconsulta,jitsi,v1.0",
                        changelog="Creación de protocolo de videoconsulta CD2",
                        created_at=datetime(2026, 9, 10, 11, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=11,
                    title="SOP-CD2-003: Prescripción de Laboratorios y Búsqueda de Estudios (SNOMED CT)",
                    category="Consultorio Digital",
                    content="1. Términos Coloquiales: El catálogo local incorpora sinonimia entre paréntesis para determinaciones usuales (ej. 'Hepatograma', '(HIV)', 'Orina completa') facilitando la búsqueda y evitando rechazos en efectores externos por falta de concordancia.\n2. Servidor de Terminología Clínica: Búsqueda sincrónica sobre API Tips Salud (POST /os-terminologiaclinica/v2/textos-codificados/terminos-sugeridos) con debounce para optimizar peticiones.\n3. Fallback de Contingencia: Ante caídas de red o errores HTTP 422 o 500 del servidor de terminología, el sistema conmuta automáticamente (try-catch) al catálogo maestro de la base de datos local de CD2 sin interrumpir la atención.",
                    author_username="admin",
                    tags="cd2,laboratorio,snomed,estudios,terminologia,tips_salud,hepatograma,hiv,v1.0",
                    version="v1.0",
                    changelog="Integración SNOMED CT con términos coloquiales y fallback local",
                    view_count=95,
                    created_at=datetime(2026, 9, 11, 9, 0),
                    updated_at=datetime(2026, 9, 16, 11, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=11,
                        version="v1.0",
                        title="SOP-CD2-003: Prescripción de Laboratorios y Búsqueda de Estudios (SNOMED CT)",
                        category="Consultorio Digital",
                        content="1. Términos comunes añadidos.\n2. Integración Tips Salud con debounce.\n3. Fallback local ante 422 o 500.",
                        author_username="admin",
                        tags="cd2,laboratorio,snomed,v1.0",
                        changelog="Creación de protocolo de laboratorios CD2",
                        created_at=datetime(2026, 9, 11, 9, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=12,
                    title="SOP-CD2-004: Medios de Registración y Configuración de Consultorio (CRM / Regiones)",
                    category="Consultorio Digital",
                    content="1. Bloqueo de 'Registrar Prestación' / Falta de Operador y Terminal: Causado por discrepancia en CRM entre la región donde el médico atiende efectivamente y la asignada en su contrato (ej. atención en Mar del Plata - Región 22 con residencia en Bariloche - Región 17).\n2. Auditoría de Concordancia: Validar coincidencia al 100% en efector, filial, región y estado entre CRM y CD2.\n3. Solución Operativa: Tramitar ante el equipo de CRM el alta de la región correspondiente a la sede de atención para habilitar los medios de registración y terminales.",
                    author_username="soporte",
                    tags="cd2,crm,regiones,terminal,operador,registrar_prestacion,efector,v1.0",
                    version="v1.0",
                    changelog="Procedimiento de auditoría regional y desbloqueo de medios de registración",
                    view_count=73,
                    created_at=datetime(2026, 9, 11, 14, 0),
                    updated_at=datetime(2026, 9, 17, 10, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=12,
                        version="v1.0",
                        title="SOP-CD2-004: Medios de Registración y Configuración de Consultorio (CRM / Regiones)",
                        category="Consultorio Digital",
                        content="1. Error de concordancia regional.\n2. Auditoría CRM vs CD2.\n3. Trámite de alta de región.",
                        author_username="soporte",
                        tags="cd2,crm,regiones,v1.0",
                        changelog="Creación de protocolo regional CRM",
                        created_at=datetime(2026, 9, 11, 14, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=13,
                    title="SOP-CD2-005: Descarga y Apertura de Documentos / PDFs (Cifrado y Caducidad)",
                    category="Consultorio Digital",
                    content="1. Error 404 (Documento no encontrado o vencido): Los archivos PDF de recetas y certificados médicos almacenados en los buckets tienen una política de retención máxima de 6 meses (180 días), eliminándose automáticamente tras ese período. Instruir a solicitar reemisión si el documento tiene más de 6 meses.\n2. Error 400 (Bad Request / Hash incompleto): Ocurre cuando el usuario copia manualmente la URL desde el correo electrónico y corta o trunca la cadena del hash. Instruir a hacer clic directo en el enlace del correo o copiar la URL completa sin omitir caracteres.",
                    author_username="soporte",
                    tags="cd2,pdf,receta,certificado,error404,error400,cifrado,bucket,retencion,v1.0",
                    version="v1.0",
                    changelog="Políticas de almacenamiento en buckets y resolución de errores de enlace PDF",
                    view_count=130,
                    created_at=datetime(2026, 9, 12, 11, 0),
                    updated_at=datetime(2026, 9, 17, 16, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=13,
                        version="v1.0",
                        title="SOP-CD2-005: Descarga y Apertura de Documentos / PDFs (Cifrado y Caducidad)",
                        category="Consultorio Digital",
                        content="1. Error 404: Retención máxima de 6 meses en bucket.\n2. Error 400: Hash truncado, cliquear enlace directo.",
                        author_username="soporte",
                        tags="cd2,pdf,cifrado,v1.0",
                        changelog="Creación de protocolo de documentos PDF",
                        created_at=datetime(2026, 9, 12, 11, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=14,
                    title="SOP-CD2-006: Repositorio de Medicamentos y Receta Electrónica (Mi Argentina)",
                    category="Consultorio Digital",
                    content="1. Código de Jurisdicción Sanitaria: Se transmite el código numérico de jurisdicción en lugar del texto libre para asegurar la integración formal con el Repositorio de Medicamentos de Mi Argentina.\n2. Discriminación de Errores: El sistema clasifica el motivo de rechazo informando si proviene de inconsistencias en el padrón del paciente o de fallas de servicio ministerial (HTTP 500 a 599).\n3. Contingencia HTTP 500: Si el repositorio nacional no responde, la receta se encola para reintento y se emite constancia con QR de contingencia.",
                    author_username="admin",
                    tags="cd2,receta,medicamentos,mi_argentina,jurisdiccion,repositorio,v1.0",
                    version="v1.0",
                    changelog="Interoperabilidad con Repositorio de Medicamentos y contingencia de recetas",
                    view_count=108,
                    created_at=datetime(2026, 9, 13, 10, 0),
                    updated_at=datetime(2026, 9, 17, 18, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=14,
                        version="v1.0",
                        title="SOP-CD2-006: Repositorio de Medicamentos y Receta Electrónica (Mi Argentina)",
                        category="Consultorio Digital",
                        content="1. Código numérico de jurisdicción.\n2. Mensajes categorizados.\n3. Encolado de reintentos.",
                        author_username="admin",
                        tags="cd2,receta,mi_argentina,v1.0",
                        changelog="Creación de protocolo de recetas Mi Argentina",
                        created_at=datetime(2026, 9, 13, 10, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=15,
                    title="SOP-CD2-007: Actualización de Prefijos Profesionales en Turnos Futuros",
                    category="Consultorio Digital",
                    content="1. Inconsistencia de Título Profesional (Dr. / Lic.): La actualización del título no impacta turnos futuros ya agendados debido a que el prefijo queda fijado en la base al generarse el primer turno.\n2. Procedimiento de Sincronización: 1) Ejecutar actualización del prefijo en la base de datos de CD2. 2) Correr proceso batch en segundo plano fuera de horario sobre la colección de turnos en MongoDB mediante identificadores de profesional para sincronizar las notificaciones y citas agendadas.",
                    author_username="admin",
                    tags="cd2,turnos,prefijo,dr,lic,mongodb,agenda,v1.0",
                    version="v1.0",
                    changelog="Procedimiento batch de regularización de prefijos académicos en turnos futuros",
                    view_count=67,
                    created_at=datetime(2026, 9, 14, 12, 0),
                    updated_at=datetime(2026, 9, 18, 8, 30)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=15,
                        version="v1.0",
                        title="SOP-CD2-007: Actualización de Prefijos Profesionales en Turnos Futuros",
                        category="Consultorio Digital",
                        content="1. Prefijo fijo en primer turno.\n2. Update en CD2 + proceso batch en MongoDB.",
                        author_username="admin",
                        tags="cd2,turnos,prefijo,v1.0",
                        changelog="Creación de protocolo de prefijos de turnos",
                        created_at=datetime(2026, 9, 14, 12, 0)
                    )
                ]
            },
            {
                "article": KBArticle(
                    id=16,
                    title="SOP-CD2-008: Validaciones de Formulario y Cierre de Consulta (RUSS)",
                    category="Consultorio Digital",
                    content="1. Diagnóstico Obligatorio: Es mandatorio seleccionar un Diagnóstico clínico codificado para finalizar y cerrar la consulta. Si no se selecciona, la atención no puede cerrarse.\n2. Evolución Asistida para RUSS: Si el profesional completa el diagnóstico pero deja la evolución en blanco, el backend autogenera un texto estándar para RUSS ('Turno Presencial / Turno Virtual' + Especialidad), evitando bloqueos operativos.\n3. Certificados con Valor 0: Las reglas de validación aceptan el valor 0 en días u horas en certificados médicos cuando no representen indicación de reposo laboral (ej. certificado de asistencia).",
                    author_username="soporte",
                    tags="cd2,russ,diagnostico,evolucion,certificados,cierre,formulario,v1.0",
                    version="v1.0",
                    changelog="Reglas de validación clínica, evolución automática RUSS y certificados de asistencia",
                    view_count=121,
                    created_at=datetime(2026, 9, 14, 15, 0),
                    updated_at=datetime(2026, 9, 18, 11, 0)
                ),
                "history": [
                    KBArticleHistory(
                        article_id=16,
                        version="v1.0",
                        title="SOP-CD2-008: Validaciones de Formulario y Cierre de Consulta (RUSS)",
                        category="Consultorio Digital",
                        content="1. Diagnóstico mandatorio.\n2. Evolución asistida RUSS si está vacía.\n3. Certificados admiten 0 si no es reposo.",
                        author_username="soporte",
                        tags="cd2,russ,diagnostico,v1.0",
                        changelog="Creación de protocolo de validaciones clínicas CD2",
                        created_at=datetime(2026, 9, 14, 15, 0)
                    )
                ]
            }

        ]
        for item in seed_data:
            a = item["article"]
            exists = session.exec(select(KBArticle).where(KBArticle.id == a.id)).first()
            if not exists:
                session.add(a)
                session.commit()
                session.refresh(a)
            for h in item["history"]:
                h.article_id = a.id
                h_exists = session.exec(select(KBArticleHistory).where(KBArticleHistory.article_id == a.id, KBArticleHistory.version == h.version)).first()
                if not h_exists:
                    session.add(h)
        session.commit()

@router.get("/articles", response_model=List[KBArticle])
def list_articles(
    category: Optional[str] = None,
    search: Optional[str] = None,
    session: Session = Depends(get_session)
):
    _ensure_kb_seed(session)
    query = select(KBArticle).where(KBArticle.is_published == True)
    articles = session.exec(query).all()
    
    if category and category.lower() != "all" and category.strip() != "":
        norm_cat = normalize_text(category)
        articles = [a for a in articles if norm_cat in normalize_text(a.category)]
        
    if search and search.strip():
        s = normalize_text(search)
        articles = [
            a for a in articles 
            if s in normalize_text(a.title) 
            or s in normalize_text(a.content) 
            or s in normalize_text(a.category) 
            or s in normalize_text(a.tags or "")
            or s in normalize_text(a.changelog or "")
        ]
        
    return sorted(articles, key=lambda x: x.created_at, reverse=True)

@router.get("/articles/categories-count")
def get_categories_count(session: Session = Depends(get_session)):
    _ensure_kb_seed(session)
    all_arts = session.exec(select(KBArticle).where(KBArticle.is_published == True)).all()
    all_hist = session.exec(select(KBArticleHistory)).all()
    counts = {"Todos": len(all_arts)}
    for a in all_arts:
        cat = a.category.strip()
        counts[cat] = counts.get(cat, 0) + 1
    return {
        "total_articles": len(all_arts),
        "total_history_records": len(all_hist),
        "by_category": counts
    }

@router.get("/articles/{article_id}", response_model=KBArticle)
def get_article(article_id: int, session: Session = Depends(get_session)):
    article = session.get(KBArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return article

@router.get("/articles/{article_id}/history", response_model=List[KBArticleHistory])
def get_article_history(article_id: int, session: Session = Depends(get_session)):
    _ensure_kb_seed(session)
    article = session.get(KBArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    history_items = session.exec(
        select(KBArticleHistory)
        .where(KBArticleHistory.article_id == article_id)
    ).all()
    
    if not history_items:
        # Fallback histórico si no tenía
        init_history = KBArticleHistory(
            article_id=article.id,
            version=article.version or "v1.0",
            title=article.title,
            category=article.category,
            content=article.content,
            author_username=article.author_username,
            tags=article.tags,
            changelog=article.changelog or "Versión inicial homologada",
            source_ticket_id=article.source_ticket_id,
            created_at=article.created_at
        )
        session.add(init_history)
        session.commit()
        history_items = [init_history]
        
    return sorted(history_items, key=lambda x: x.created_at, reverse=True)

@router.post("/articles", response_model=KBArticle)
def create_article(req: ArticleCreateRequest, session: Session = Depends(get_session)):
    if not req.title.strip() or not req.content.strip():
        raise HTTPException(status_code=400, detail="Título y contenido son obligatorios")
    
    ver = req.version.strip() if req.version else "v1.0"
    log = req.changelog.strip() if req.changelog else "Versión inicial publicada"
    
    article = KBArticle(
        title=req.title.strip(),
        category=req.category.strip() or "General",
        content=req.content.strip(),
        author_username=req.author_username or "admin",
        tags=req.tags,
        version=ver,
        changelog=log,
        view_count=1,
        requests_deflected=req.requests_deflected or 0,
        helpful_score=req.helpful_score or 95,
        space_name=req.space_name or "Guías y Documentación de Soporte Asistencial",
        source_ticket_id=req.source_ticket_id,
        is_published=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(article)
    session.commit()
    session.refresh(article)
    
    # Registro inmutable en el historial
    history = KBArticleHistory(
        article_id=article.id,
        version=ver,
        title=article.title,
        category=article.category,
        content=article.content,
        author_username=article.author_username,
        tags=article.tags,
        changelog=log,
        source_ticket_id=req.source_ticket_id,
        created_at=datetime.utcnow()
    )
    session.add(history)
    session.commit()
    session.refresh(article)
    
    return article

@router.put("/articles/{article_id}", response_model=KBArticle)
def update_article(
    article_id: int, 
    req: ArticleUpdateRequest, 
    session: Session = Depends(get_session)
):
    article = session.get(KBArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    # Determinar nueva versión
    current_ver = article.version or "v1.0"
    new_ver = req.version
    if not new_ver:
        # Calcular siguiente versión
        try:
            clean = current_ver.replace("v", "").strip()
            parts = [int(p) for p in clean.split(".")]
            if len(parts) == 1:
                parts.append(0)
            if req.increment_type == "major":
                parts[0] += 1
                parts[1] = 0
            else:
                parts[1] += 1
            new_ver = f"v{parts[0]}.{parts[1]}"
        except Exception:
            new_ver = "v2.0"
            
    changelog_text = req.changelog.strip() if req.changelog else f"Actualización a versión {new_ver}"
    
    if req.title:
        article.title = req.title.strip()
    if req.category:
        article.category = req.category.strip()
    if req.content:
        article.content = req.content.strip()
    if req.tags is not None:
        article.tags = req.tags
    if req.author_username:
        article.author_username = req.author_username
        
    article.version = new_ver
    article.changelog = changelog_text
    article.updated_at = datetime.utcnow()
    
    session.add(article)
    
    # Guardar nueva snapshot en el historial
    new_history = KBArticleHistory(
        article_id=article.id,
        version=new_ver,
        title=article.title,
        category=article.category,
        content=article.content,
        author_username=req.author_username or article.author_username,
        tags=article.tags,
        changelog=changelog_text,
        source_ticket_id=article.source_ticket_id,
        created_at=datetime.utcnow()
    )
    session.add(new_history)
    session.commit()
    session.refresh(article)
    return article

@router.post("/articles/from-ticket/{ticket_id}", response_model=KBArticle)
def promote_ticket_to_article(
    ticket_id: str,
    req: ArticleFromTicketRequest,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
    title = req.title.strip() if req.title else f"Solución estándar para {ticket.title}"
    category = req.category.strip() if req.category else "Procedimientos Clínicos"
    content = req.content.strip() if req.content else (ticket.resolution_notes or ticket.description)
    
    article = KBArticle(
        title=title,
        category=category,
        content=content,
        author_username=req.author_username or ticket.assignee_username or "soporte",
        tags=req.tags or f"ticket,{ticket.platform_code.lower() if ticket.platform_code else 'general'},solucion",
        version="v1.0",
        changelog=f"Artículo promovido formalmente desde la resolución exitosa del Ticket #{ticket_id}",
        source_ticket_id=ticket_id,
        view_count=1,
        is_published=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(article)
    session.commit()
    session.refresh(article)
    
    # Historial inicial
    history = KBArticleHistory(
        article_id=article.id,
        version="v1.0",
        title=article.title,
        category=article.category,
        content=article.content,
        author_username=article.author_username,
        tags=article.tags,
        changelog=f"Publicación de solución basada en Ticket #{ticket_id}",
        source_ticket_id=ticket_id,
        created_at=datetime.utcnow()
    )
    session.add(history)
    session.commit()
    session.refresh(article)
    return article

@router.post("/articles/{article_id}/view")
def register_article_view(article_id: int, session: Session = Depends(get_session)):
    article = session.get(KBArticle, article_id)
    if article:
        article.view_count = (article.view_count or 0) + 1
        session.add(article)
        session.commit()
    return {"status": "ok", "view_count": article.view_count if article else 0}

@router.delete("/articles/{article_id}")
def delete_article(article_id: int, session: Session = Depends(get_session)):
    article = session.get(KBArticle, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    # Eliminar entradas históricas asociadas primero para respetar FK
    session.exec(delete(KBArticleHistory).where(KBArticleHistory.article_id == article_id))
    session.flush()
        
    session.delete(article)
    session.commit()
    return {"status": "success", "message": f"Artículo {article_id} y su historial eliminados correctamente"}

# =============================================================================
# CONFIGURACIÓN OPERATIVA DEL SISTEMA (SYSTEM CONFIG & SLA PARAMS)
# =============================================================================
_system_config = {
    "sla_p1_response": 15,
    "sla_p1_resolution": 120,
    "sla_p2_response": 30,
    "sla_p2_resolution": 480,
    "sla_p3_response": 60,
    "sla_p3_resolution": 1440,
    "sla_p4_response": 120,
    "sla_p4_resolution": 2880,
    "sla_p5_response": 240,
    "sla_p5_resolution": 4320,
    "sla_p1_response_min": 15,
    "sla_p1_resolve_hours": 2,
    "sla_p2_response_min": 30,
    "sla_p2_resolve_hours": 8,
    "sla_p3_response_min": 60,
    "sla_p3_resolve_hours": 24,
    "sla_p4_response_min": 120,
    "sla_p4_resolve_hours": 48,
    "sla_p5_response_min": 240,
    "sla_p5_resolve_hours": 72,
    "notify_p1_critical": True,
    "notify_email_ticket_created": True,
    "notify_email_sla_warning": True,
    "notify_email_ticket_resolved": True,
    "require_resolution_note": True,
    "require_technical_solution_notes": True,
    "allow_workaround_solutions": True,
    "maintenance_mode": False
}

class SystemConfigUpdate(BaseModel):
    sla_p1_response: Optional[int] = None
    sla_p1_resolution: Optional[int] = None
    sla_p2_response: Optional[int] = None
    sla_p2_resolution: Optional[int] = None
    sla_p3_response: Optional[int] = None
    sla_p3_resolution: Optional[int] = None
    sla_p4_response: Optional[int] = None
    sla_p4_resolution: Optional[int] = None
    sla_p5_response: Optional[int] = None
    sla_p5_resolution: Optional[int] = None
    sla_p1_response_min: Optional[int] = None
    sla_p1_resolve_hours: Optional[int] = None
    sla_p2_response_min: Optional[int] = None
    sla_p2_resolve_hours: Optional[int] = None
    sla_p3_response_min: Optional[int] = None
    sla_p3_resolve_hours: Optional[int] = None
    sla_p4_response_min: Optional[int] = None
    sla_p4_resolve_hours: Optional[int] = None
    sla_p5_response_min: Optional[int] = None
    sla_p5_resolve_hours: Optional[int] = None
    notify_p1_critical: Optional[bool] = None
    notify_email_ticket_created: Optional[bool] = None
    notify_email_sla_warning: Optional[bool] = None
    notify_email_ticket_resolved: Optional[bool] = None
    require_resolution_note: Optional[bool] = None
    require_technical_solution_notes: Optional[bool] = None
    allow_workaround_solutions: Optional[bool] = None
    maintenance_mode: Optional[bool] = None

@router.get("/config")
def get_system_config():
    return _system_config

@router.put("/config")
def update_system_config(req: SystemConfigUpdate):
    for key, val in req.dict(exclude_unset=True).items():
        if val is not None:
            _system_config[key] = val
    return {
        "status": "success",
        "message": "Parámetros de configuración actualizados correctamente",
        "config": _system_config,
        **_system_config
    }

# =============================================================================
# POLÍTICAS DE SLA CONFIGURABLES POR INSTITUCIÓN
# =============================================================================
_institution_slas = {
    "GLOBAL": {
        "n1": {"group": "OP_GUARDIA", "p1": 15, "p2": 30, "p3": 2, "p4": 4},
        "n2": {"group": "ESP_CLINICOS", "p1": 1, "p2": 4, "p3": 8, "p4": 24},
        "n3": {"group": "ING_CORE", "p1": 2, "p2": 8, "p3": 24, "p4": 48}
    }
}

@router.get("/institutions/{institution_code}/sla")
def get_institution_sla(institution_code: str):
    code = institution_code.upper()
    policy = _institution_slas.get(code, _institution_slas.get("GLOBAL"))
    return {
        "institution_code": code,
        "is_custom": code in _institution_slas,
        "policy": policy
    }

@router.put("/institutions/{institution_code}/sla")
def update_institution_sla(institution_code: str, payload: dict):
    code = institution_code.upper()
    policy_data = payload.get("policy", payload)
    _institution_slas[code] = policy_data
    return {
        "status": "success",
        "institution_code": code,
        "is_custom": code != "GLOBAL",
        "message": f"Políticas de SLA actualizadas para {code}",
        "policy": _institution_slas[code]
    }

@router.delete("/institutions/{institution_code}/sla")
def reset_institution_sla(institution_code: str):
    code = institution_code.upper()
    if code in _institution_slas and code != "GLOBAL":
        del _institution_slas[code]
    return {
        "status": "success",
        "institution_code": code,
        "is_custom": False,
        "message": f"SLA de {code} restablecido a la Política Base",
        "policy": _institution_slas.get("GLOBAL")
    }

@router.get("/sla/policies")
def list_sla_policies():
    return {
        "status": "success",
        "policies": _institution_slas
    }


# =============================================================================
# GESTIÓN DE MESAS DE AYUDA Y NIVELES DE ATENCIÓN (ITIL N1, N2, N3)
# =============================================================================

_helpdesk_levels_config = {
    "N1": {
        "code": "N1",
        "name": "Nivel 1 • Mesa Central, Recepción & Triage",
        "short_name": "N1 Triage",
        "badge_label": "N1 • Triage",
        "description": "Atención de primera línea, recepción multicanal, categorización ITIL, validación de credenciales médicas y restablecimiento básico de acceso.",
        "badge_color": "#0284C7",
        "badge_bg": "#EFF6FF",
        "border_color": "#BFDBFE",
        "max_retention_minutes": 30,
        "max_retention_label": "30 minutos",
        "assignment_mode": "ROUND_ROBIN",  # ROUND_ROBIN | SPECIALTY | WORKLOAD | MANUAL
        "auto_escalate_enabled": True,
        "auto_escalate_target": "N2",
        "covered_platforms": ["CAT_CONSULTORIO_DIGITAL", "CAT_RECETA", "CAT_TELEMEDICINA", "CAT_AFILIADOS_PORTAL", "CAT_CARTILLA_TURNOS"],
        "assigned_teams": [
            {
                "id": "team_n1_central",
                "name": "Mesa Central Asistencial & Triage",
                "lead": "Laura Benítez",
                "operators_count": 8,
                "shift": "24/7 Rotativo",
                "platforms": ["CAT_CONSULTORIO_DIGITAL", "CAT_RECETA", "CAT_TELEMEDICINA"]
            },
            {
                "id": "team_n1_pacientes",
                "name": "Mesa de Atención a Afiliados y Turnos",
                "lead": "Carlos Recepción",
                "operators_count": 4,
                "shift": "Lunes a Viernes 08:00 - 20:00",
                "platforms": ["CAT_AFILIADOS_PORTAL", "CAT_CARTILLA_TURNOS"]
            }
        ],
        "escalation_rules": [
            {"condition": "Tiempo en N1 > 30 min sin resolución", "action": "Auto-escalar a N2 Especialista", "target": "N2"},
            {"condition": "Ticket P1 Crítico (Corte total de servicio)", "action": "Escalar inmediatamente a N3", "target": "N3"},
            {"condition": "Error de firma digital o receta bloqueada", "action": "Derivar a Mesa N2 Receta", "target": "N2"}
        ],
        "operators": [
            {"username": "soporte", "name": "Laura Benítez", "role": "Operadora de Soporte N1", "status": "ONLINE", "active_tickets": 3},
            {"username": "triage.n1", "name": "Carlos Triage", "role": "Operador N1", "status": "ONLINE", "active_tickets": 2},
            {"username": "mesa.recepcion", "name": "Martín Recepción", "role": "Operador N1", "status": "BUSY", "active_tickets": 5}
        ]
    },
    "N2": {
        "code": "N2",
        "name": "Nivel 2 • Soporte Especializado por Plataforma Asistencial",
        "short_name": "N2 Especialistas",
        "badge_label": "N2 • Especialista",
        "description": "Diagnóstico funcional avanzado, resolución de inconsistencias en recetas electrónicas, configuración de convenios, validación de agendas y sincronización PACS.",
        "badge_color": "#7C3AED",
        "badge_bg": "#F5F3FF",
        "border_color": "#DDD6FE",
        "max_retention_minutes": 240,
        "max_retention_label": "4 horas",
        "assignment_mode": "SPECIALTY",
        "auto_escalate_enabled": True,
        "auto_escalate_target": "N3",
        "covered_platforms": ["CAT_RECETA", "CAT_HIS_CORE", "CAT_COPAGOS_PAGOS", "CAT_INTERNACION_DOM", "CAT_REGISTRO_INTEROP", "CAT_RPM_MONITOREO"],
        "assigned_teams": [
            {
                "id": "team_n2_his",
                "name": "Mesa Especialista HIS & Consultorio Digital",
                "lead": "Dr. Fernando Ruiz",
                "operators_count": 6,
                "shift": "Guardia Activa 08:00 - 22:00",
                "platforms": ["CAT_CONSULTORIO_DIGITAL", "CAT_HIS_CORE"]
            },
            {
                "id": "team_n2_receta",
                "name": "Mesa Especialista Receta & Firma Digital (PKI)",
                "lead": "Carlos Páez",
                "operators_count": 5,
                "shift": "24/7 Guardia Farmacéutica",
                "platforms": ["CAT_RECETA"]
            },
            {
                "id": "team_n2_interop",
                "name": "Mesa Interoperabilidad HL7/FHIR & Financiadores",
                "lead": "Ing. Sofía Valenzuela",
                "operators_count": 4,
                "shift": "Lunes a Viernes 09:00 - 18:00",
                "platforms": ["CAT_REGISTRO_INTEROP", "CAT_COPAGOS_PAGOS"]
            }
        ],
        "escalation_rules": [
            {"condition": "Tiempo en N2 > 4 horas sin diagnóstico", "action": "Escalar a N3 Ingeniería", "target": "N3"},
            {"condition": "Bug de software validado en API o base de datos", "action": "Crear Issue y derivar a N3 Core Dev", "target": "N3"},
            {"condition": "Falla masiva de WebService externo (OSDE/Swiss)", "action": "Activar protocolo N3 Contingencia", "target": "N3"}
        ],
        "operators": [
            {"username": "sofia.esp", "name": "Ing. Sofía Valenzuela", "role": "Especialista Interoperabilidad N2", "status": "ONLINE", "active_tickets": 2},
            {"username": "carlos.receta", "name": "Carlos Páez", "role": "Especialista Receta Digital N2", "status": "ONLINE", "active_tickets": 4},
            {"username": "fernando.his", "name": "Dr. Fernando Ruiz", "role": "Especialista HIS Core N2", "status": "ONLINE", "active_tickets": 1}
        ]
    },
    "N3": {
        "code": "N3",
        "name": "Nivel 3 • Ingeniería de Software, Infraestructura Cloud & DBA",
        "short_name": "N3 Ingeniería",
        "badge_label": "N3 • Ingeniería",
        "description": "Corrección de código en repositorios, optimización de consultas SQL, clúster de servidores Kubernetes, seguridad de certificados SSL/PKI y gestión con proveedores externos.",
        "badge_color": "#DC2626",
        "badge_bg": "#FEF2F2",
        "border_color": "#FECACA",
        "max_retention_minutes": 480,
        "max_retention_label": "8 horas",
        "assignment_mode": "CRITICALITY",
        "auto_escalate_enabled": False,
        "auto_escalate_target": None,
        "covered_platforms": ["ALL"],
        "assigned_teams": [
            {
                "id": "team_n3_dev",
                "name": "Equipo Core Dev & Arquitectura de Software",
                "lead": "Freddy Cortés (Solution Owner)",
                "operators_count": 4,
                "shift": "On-Call Incidentes Críticos",
                "platforms": ["ALL"]
            },
            {
                "id": "team_n3_infra",
                "name": "Equipo DevOps, Cloud & Base de Datos",
                "lead": "Ing. Martín DBA",
                "operators_count": 3,
                "shift": "24/7 Monitoreo de Infraestructura",
                "platforms": ["ALL"]
            }
        ],
        "escalation_rules": [
            {"condition": "Incidente P1 Crítico sin resolución técnica", "action": "Activar Comité de Crisis y Solution Owner", "target": "ADMIN"},
            {"condition": "Caída de nodo primario de base de datos", "action": "Ejecutar Failover a Nodo Secundario", "target": "N3"}
        ],
        "operators": [
            {"username": "admin", "name": "Freddy Cortés", "role": "Solution Owner & Lead Architect N3", "status": "ONLINE", "active_tickets": 1},
            {"username": "dev.lead", "name": "Ing. Martín Dev", "role": "Senior Backend Developer N3", "status": "ONLINE", "active_tickets": 2},
            {"username": "dba.master", "name": "Ing. Valeria DBA", "role": "Database Administrator N3", "status": "STANDBY", "active_tickets": 0}
        ]
    }
}

class HelpdeskLevelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    max_retention_minutes: Optional[int] = None
    assignment_mode: Optional[str] = None
    auto_escalate_enabled: Optional[bool] = None
    auto_escalate_target: Optional[str] = None
    covered_platforms: Optional[List[str]] = None

class HelpdeskTeamCreate(BaseModel):
    name: str
    lead: str
    operators_count: int = 1
    shift: str = "Lunes a Viernes 09:00 - 18:00"
    platforms: Optional[List[str]] = None

@router.get("/config/levels")
def get_all_helpdesk_levels():
    return list(_helpdesk_levels_config.values())

@router.get("/config/levels/{level_code}")
def get_helpdesk_level(level_code: str):
    code = level_code.upper()
    if code not in _helpdesk_levels_config:
        raise HTTPException(status_code=404, detail=f"Nivel de atención '{level_code}' no existe.")
    return _helpdesk_levels_config[code]

@router.put("/config/levels/{level_code}")
def update_helpdesk_level(level_code: str, req: HelpdeskLevelUpdate):
    code = level_code.upper()
    if code not in _helpdesk_levels_config:
        raise HTTPException(status_code=404, detail=f"Nivel de atención '{level_code}' no existe.")
    
    lvl = _helpdesk_levels_config[code]
    if req.name is not None:
        lvl["name"] = req.name
    if req.description is not None:
        lvl["description"] = req.description
    if req.max_retention_minutes is not None:
        lvl["max_retention_minutes"] = req.max_retention_minutes
        if req.max_retention_minutes >= 60:
            lvl["max_retention_label"] = f"{req.max_retention_minutes // 60} horas"
        else:
            lvl["max_retention_label"] = f"{req.max_retention_minutes} minutos"
    if req.assignment_mode is not None:
        lvl["assignment_mode"] = req.assignment_mode
    if req.auto_escalate_enabled is not None:
        lvl["auto_escalate_enabled"] = req.auto_escalate_enabled
    if req.auto_escalate_target is not None:
        lvl["auto_escalate_target"] = req.auto_escalate_target
    if req.covered_platforms is not None:
        lvl["covered_platforms"] = req.covered_platforms
        
    return {
        "status": "success",
        "message": f"Configuración del {lvl['name']} actualizada correctamente.",
        "level": lvl
    }

@router.post("/config/levels/{level_code}/teams")
def add_team_to_level(level_code: str, team: HelpdeskTeamCreate):
    code = level_code.upper()
    if code not in _helpdesk_levels_config:
        raise HTTPException(status_code=404, detail=f"Nivel de atención '{level_code}' no existe.")
    
    import uuid
    new_team = {
        "id": f"team_{code.lower()}_{uuid.uuid4().hex[:6]}",
        "name": team.name,
        "lead": team.lead,
        "operators_count": team.operators_count,
        "shift": team.shift,
        "platforms": team.platforms or ["CAT_RECETA", "CAT_CONSULTORIO_DIGITAL"]
    }
    _helpdesk_levels_config[code]["assigned_teams"].append(new_team)
    return {
        "status": "success",
        "message": f"Mesa '{team.name}' añadida con éxito al {code}.",
        "team": new_team
    }



# =============================================================================
# COPILOTO IA DE BASE DE CONOCIMIENTO PARA AGENTES DE SOPORTE
# =============================================================================
class CopilotQueryRequest(BaseModel):
    query: str
    ticket_id: Optional[str] = None

class CopilotQueryResponse(BaseModel):
    query: str
    matched_article_id: Optional[int] = None
    article_title: str
    category: str
    diagnostic: str
    client_response: str
    technical_sop: str
    quick_solution: str

@router.post("/articles/copilot-chat", response_model=CopilotQueryResponse)
def copilot_chat_kb(req: CopilotQueryRequest, session: Session = Depends(get_session)):
    """
    Chat Copiloto amigable para agentes de soporte:
    Analiza la consulta en lenguaje natural contra el catálogo unificado de 16 artículos
    y devuelve diagnóstico, respuesta lista para enviar al cliente y SOP técnico N1/N2.
    """
    _ensure_kb_seed(session)
    articles = session.exec(select(KBArticle).where(KBArticle.is_published == True)).all()
    q = (req.query or "").lower().strip()
    
    # Mapeo heurístico inteligente y semántico por palabras clave
    best_article = None
    best_score = 0
    
    for art in articles:
        score = 0
        title_l = art.title.lower()
        content_l = art.content.lower()
        tags_l = (art.tags or "").lower()
        
        # Palabras clave ponderadas
        terms = [t for t in q.replace(",", " ").replace(".", " ").replace("?", " ").split() if len(t) > 2]
        for term in terms:
            if term in title_l:
                score += 5
            if term in tags_l:
                score += 3
            if term in content_l:
                score += 1
                
        # Bonus específicos por conceptos clave
        if ("matrícula" in q or "matricula" in q or "sisa" in q) and art.id == 13:
            score += 20
        elif ("jitsi" in q or "videoconsulta" in q or "spinner" in q or "self-view" in q or "camara" in q) and art.id == 14:
            score += 20
        elif ("laboratorio" in q or "snomed" in q or "hepatograma" in q or "hiv" in q) and art.id == 15:
            score += 20
        elif ("registrar prestación" in q or "crm" in q or "terminal" in q or "operador" in q or "region" in q or "región" in q) and art.id == 16:
            score += 20
        elif ("404" in q or "400" in q or "pdf" in q or "bucket" in q or "caducidad" in q or "retención" in q) and art.id == 17:
            score += 20
        elif ("mi argentina" in q or "repositorio" in q or "medicamentos" in q or "jurisdicción" in q) and art.id == 18:
            score += 20
        elif ("prefijo" in q or "dr" in q or "lic" in q or "titulo" in q or "turnos futuros" in q) and art.id == 19:
            score += 20
        elif ("diagnostico" in q or "diagnóstico" in q or "russ" in q or "certificado" in q or "cierre" in q or "valor 0" in q) and art.id == 20:
            score += 20
        elif ("firma digital" in q or "osde" in q or "swiss" in q) and art.id == 1:
            score += 15
        elif ("webrtc" in q or "safari" in q or "h.264" in q) and art.id == 3:
            score += 15
        elif ("hl7" in q or "desincronizacion" in q or "adt" in q) and art.id == 12:
            score += 15
            
        if score > best_score:
            best_score = score
            best_article = art
            
    if not best_article and articles:
        # Fallback al primer artículo de CD2
        best_article = next((a for a in articles if a.id == 13), articles[0])
        
    # Construcción de respuesta estructurada para el agente
    art_id = best_article.id
    if art_id == 13:
        diag = "Selector de matrícula bloqueado o inconsistencia SISA/CRM por matrícula ficticia o CUIT modificado."
        client_res = "Estimado/a profesional: Si visualiza el selector bloqueado, el sistema ya habilitó la selección manual de su matrícula activa de SISA. Por favor verifique el desplegable. En caso de requerir unificación de matrículas, su caso ha sido derivado para gestión prioritaria."
        tech_sop = "1. Validar que la matrícula figure en estado 'Habilitada'. 2. Si hay ICs duplicados por CUIT extranjero en CRM, solicitar unificación mediante ticket PAU a Soporte CRM/MDA. 3. Para contingencia urgente en BD de CD2: copiar objeto matriculaSISA a defaultMatricula."
        quick = "Desbloquear selector en frontend si difiere de default y unificar ICs vía PAU en CRM."
    elif art_id == 14:
        diag = "Dificultad de enlace Jitsi por joinTimeout, falta de permisos o bloqueo de miniatura self-view."
        client_res = "Estimado/a profesional: El sistema realiza reconexiones automáticas continuas. Por favor asegúrese de tener permitidos cámara y micrófono en el candado de la barra del navegador y refresque la pantalla con F5 si el spinner persiste."
        tech_sop = "1. Reconexión automática limitada a 5 intentos cada 20s. 2. Verificar pre-check de hardware en cliente. 3. El iframe de Jitsi cuenta con fix de renderizado para miniatura de video propia. 4. Se requiere confirmación modal antes de cerrar la sala."
        quick = "Validar permisos en navegador, 5 reintentos automáticos y refrescar con F5."
    elif art_id == 15:
        diag = "Dificultad para localizar análisis clínicos por términos coloquiales bajo catálogo estricto SNOMED CT."
        client_res = "Estimado/a profesional: Para la búsqueda de estudios habituales (ej. hepatograma, HIV, orina), puede escribir el nombre coloquial habitual, ya que el catálogo local cuenta con sinónimos automáticos entre paréntesis."
        tech_sop = "1. Búsqueda sincrónica sobre API Tips Salud con debounce. 2. En caso de HTTP 422 o 500, el sistema conmuta automáticamente (fallback try-catch) al catálogo maestro local de CD2."
        quick = "Usar sinónimos entre paréntesis en catálogo local con fallback automático ante caídas de Tips Salud."
    elif art_id == 16:
        diag = "Botón Registrar Prestación bloqueado por falta de operador/terminal debido a discordancia regional CRM."
        client_res = "Estimado/a profesional: Se detectó una inconsistencia entre la región de atención y su contrato base en CRM. Estamos regularizando la vinculación de su sede de atención para habilitar los medios de registración."
        tech_sop = "1. Auditar coincidencia 100% en efector, filial, región y estado entre CRM y CD2. 2. Tramitar el alta de la región operativa en CRM (ej. Región 22 Mar del Plata vs Región 17 Bariloche)."
        quick = "Validar efector/filial/región al 100% y tramitar alta de región operativa en CRM."
    elif art_id == 17:
        diag = "Error 404 (documento expirado tras 6 meses) o Error 400 (cadena de hash incompleta en URL)."
        client_res = "Estimado/a usuario: Si el enlace indica documento no encontrado (404), la receta/certificado ha superado la política de retención de 6 meses y debe solicitar su reemisión. Si observa error 400, por favor haga clic directamente en el enlace recibido en su correo sin copiar y pegar manualmente."
        tech_sop = "1. Documentos en bucket se purgan a los 180 días por política de retención. 2. Error 400 se debe a truncado de hash en copy-paste; validar enlace completo."
        quick = "Explicar caducidad de 6 meses para 404, y uso de enlace directo original sin truncar hash para 400."
    elif art_id == 18:
        diag = "Rechazo de validación en Repositorio Nacional de Medicamentos (Mi Argentina)."
        client_res = "Estimado/a profesional: La validación de la receta se encuentra en procesamiento asistido. En caso de persistir, el sistema genera la constancia con código QR de contingencia para su dispensación."
        tech_sop = "1. Verificar transmisión de código numérico de jurisdicción para Mi Argentina. 2. Si el fallo es HTTP 500+, la receta se encola para reintento y se emite duplicado de contingencia."
        quick = "Transmitir código numérico de jurisdicción y encolar reintentos ante HTTP 500+."
    elif art_id == 19:
        diag = "Inconsistencia de prefijo profesional (Dr. / Lic.) en turnos futuros ya agendados."
        client_res = "Estimado/a profesional: Su título académico ha sido actualizado en la ficha maestra. Los turnos futuros agendados se sincronizarán en el próximo proceso programado de actualización."
        tech_sop = "1. Actualizar el prefijo en base de datos de CD2. 2. Ejecutar corrida batch programada fuera de horario sobre la colección de turnos en MongoDB mediante los IDs del profesional."
        quick = "Actualizar en BD CD2 y sincronizar turnos futuros mediante proceso batch en MongoDB."
    elif art_id == 20:
        diag = "Bloqueo de cierre de atención por Diagnóstico obligatorio o error en certificado médico."
        client_res = "Estimado/a profesional: Recuerde que es mandatorio seleccionar un Diagnóstico codificado para finalizar la consulta. Si no requiere ingresar Evolución, el sistema generará automáticamente la constancia clínica para RUSS."
        tech_sop = "1. Diagnóstico es campo mandatorio ineludible. 2. Evolución vacía autogenera texto estandarizado RUSS ('Turno Presencial/Virtual' + Especialidad). 3. Certificados médicos aceptan valor 0 cuando no es reposo laboral."
        quick = "Seleccionar Diagnóstico obligatorio, evolución asistida RUSS autogenerada y valor 0 permitido en certificados sin reposo."
        diag = "Bloqueo de cierre de atención por Diagnóstico obligatorio o error en certificado médico."
        client_res = "Estimado/a profesional: Recuerde que es mandatorio seleccionar un Diagnóstico codificado para finalizar la consulta. Si no requiere ingresar Evolución, el sistema generará automáticamente la constancia clínica para RUSS."
        tech_sop = "1. Diagnóstico es campo mandatorio ineludible. 2. Evolución vacía autogenera texto estandarizado RUSS ('Turno Presencial/Virtual' + Especialidad). 3. Certificados médicos aceptan valor 0 cuando no es reposo laboral."
        quick = "Seleccionar Diagnóstico obligatorio, evolución asistida RUSS autogenerada y valor 0 permitido en certificados sin reposo."
    else:
        diag = f"Procedimiento estándar para {best_article.category} ({best_article.title})."
        client_res = f"Estimado/a usuario: Respecto a su consulta sobre {best_article.title}, le informamos los pasos recomendados según nuestro protocolo oficial:\n{best_article.content}"
        tech_sop = f"Consultar artículo oficial #{best_article.id} en Base de Conocimiento para pasos detallados de N1/N2."
        quick = best_article.title

    return CopilotQueryResponse(
        query=req.query,
        matched_article_id=best_article.id,
        article_title=best_article.title,
        category=best_article.category,
        diagnostic=diag,
        client_response=client_res,
        technical_sop=tech_sop,
        quick_solution=quick
    )
