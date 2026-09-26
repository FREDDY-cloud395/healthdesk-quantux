from app.models.entities import TicketStatus, ImpactLevel, UrgencyLevel, PriorityLevel

def calculate_priority(impact: ImpactLevel, urgency: UrgencyLevel) -> PriorityLevel:
    # Normalizar strings
    imp_str = str(impact.value if hasattr(impact, "value") else impact).upper()
    urg_str = str(urgency.value if hasattr(urgency, "value") else urgency).upper()
    
    # Mapeo a escala 1..3 (Cruce matricial ITIL de Impacto x Urgencia)
    imp_score = 3 if imp_str in ["CRITICO", "ALTO", "INSTITUCIONAL"] else (2 if imp_str in ["MEDIO", "MULTIPLES_PRESTADORES"] else 1)
    urg_score = 3 if urg_str in ["CRITICA", "CRITICO", "ALTA", "ALTO", "ATENCION_ACTIVA"] else (2 if urg_str in ["MEDIA", "MEDIO", "DIFERIDO"] else 1)
    
    matrix = {
        (3, 3): PriorityLevel.P1, # P1 Crítica (< 15 min)
        (3, 2): PriorityLevel.P2, # P2 Alta (< 30 min)
        (3, 1): PriorityLevel.P3, # P3 Media (< 2 hs)
        (2, 3): PriorityLevel.P2, # P2 Alta (< 30 min)
        (2, 2): PriorityLevel.P3, # P3 Media (< 2 hs)
        (2, 1): PriorityLevel.P4, # P4 Baja (< 24 hs)
        (1, 3): PriorityLevel.P3, # P3 Media (< 2 hs)
        (1, 2): PriorityLevel.P4, # P4 Baja (< 24 hs)
        (1, 1): PriorityLevel.P4, # P4 Baja (< 24 hs)
    }
    return matrix.get((imp_score, urg_score), PriorityLevel.P3)

# TRANSICIONES PERMITIDAS DE LA FSM (7 ESTADOS ITIL 4 OFICIALES)
ALLOWED_TRANSITIONS = {
    TicketStatus.NUEVO: [TicketStatus.ASIGNADO, TicketStatus.EN_CURSO],
    TicketStatus.ASIGNADO: [TicketStatus.EN_CURSO, TicketStatus.ASIGNADO],
    TicketStatus.EN_CURSO: [
        TicketStatus.RESUELTO,
        TicketStatus.EN_CURSO,
        TicketStatus.ESPERANDO_AL_PRESTADOR,
        TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA,
        TicketStatus.EN_ESPERA
    ],
    TicketStatus.ESPERANDO_AL_PRESTADOR: [
        TicketStatus.EN_CURSO,
        TicketStatus.RESUELTO,
        TicketStatus.ESPERANDO_AL_PRESTADOR
    ],
    TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA: [
        TicketStatus.EN_CURSO,
        TicketStatus.RESUELTO,
        TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA
    ],
    TicketStatus.EN_ESPERA: [
        TicketStatus.EN_CURSO,
        TicketStatus.RESUELTO,
        TicketStatus.EN_ESPERA
    ],
    TicketStatus.RESUELTO: [TicketStatus.CERRADO, TicketStatus.EN_CURSO],
    TicketStatus.CERRADO: [TicketStatus.EN_CURSO]  # Reapertura asistida
}

def validate_status_transition(current_status: TicketStatus, target_status: TicketStatus) -> bool:
    allowed = ALLOWED_TRANSITIONS.get(current_status, [])
    return target_status in allowed

def is_sla_paused_status(status: TicketStatus) -> bool:
    """Retorna True si el estado del ticket implica la detención transitoria (pausa) del reloj de SLA."""
    return status in [
        TicketStatus.ESPERANDO_AL_PRESTADOR,
        TicketStatus.EN_ESPERA_PASARELA_OSDE_SISA,
        TicketStatus.EN_ESPERA
    ]
