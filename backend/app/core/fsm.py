from app.models.entities import TicketStatus, ImpactLevel, UrgencyLevel, PriorityLevel

def calculate_priority(impact: ImpactLevel, urgency: UrgencyLevel) -> PriorityLevel:
    # Normalizar strings
    imp_str = str(impact.value if hasattr(impact, "value") else impact).upper()
    urg_str = str(urgency.value if hasattr(urgency, "value") else urgency).upper()
    
    # Mapeo a escala 1..3
    imp_score = 3 if imp_str in ["CRITICO", "ALTO"] else (2 if imp_str == "MEDIO" else 1)
    urg_score = 3 if urg_str in ["CRITICA", "CRITICO", "ALTA", "ALTO"] else (2 if urg_str in ["MEDIA", "MEDIO"] else 1)
    
    matrix = {
        (3, 3): PriorityLevel.P1, # Crítica
        (3, 2): PriorityLevel.P2, # Alta
        (3, 1): PriorityLevel.P3, # Media
        (2, 3): PriorityLevel.P2, # Alta
        (2, 2): PriorityLevel.P3, # Media
        (2, 1): PriorityLevel.P4, # Baja
        (1, 3): PriorityLevel.P3, # Media
        (1, 2): PriorityLevel.P4, # Baja
        (1, 1): PriorityLevel.P5, # Planificada
    }
    return matrix.get((imp_score, urg_score), PriorityLevel.P3)

# TRANSICIONES PERMITIDAS DE LA FSM
ALLOWED_TRANSITIONS = {
    TicketStatus.NUEVO: [TicketStatus.ASIGNADO, TicketStatus.EN_CURSO],
    TicketStatus.ASIGNADO: [TicketStatus.EN_CURSO, TicketStatus.ASIGNADO],
    TicketStatus.EN_CURSO: [TicketStatus.RESUELTO, TicketStatus.EN_CURSO],
    TicketStatus.RESUELTO: [TicketStatus.CERRADO, TicketStatus.EN_CURSO],
    TicketStatus.CERRADO: []  # Estado final inmutable
}

def validate_status_transition(current_status: TicketStatus, target_status: TicketStatus) -> bool:
    allowed = ALLOWED_TRANSITIONS.get(current_status, [])
    return target_status in allowed
