from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
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

@router.get("/institutions", response_model=List[Institution])
def list_institutions(session: Session = Depends(get_session)):
    return session.exec(select(Institution).where(Institution.is_active == True)).all()

@router.get("/calculate-priority")
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
    if existing_count < 8:
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
    
    # Eliminar entradas históricas asociadas
    histories = session.exec(select(KBArticleHistory).where(KBArticleHistory.article_id == article_id)).all()
    for h in histories:
        session.delete(h)
        
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

