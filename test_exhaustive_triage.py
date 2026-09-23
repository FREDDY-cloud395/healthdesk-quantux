# -*- coding: utf-8 -*-
from backend.app.services.ai_triage import N3CognitiveTriageEngine

test_cases = [
    # Módulo Prestador: Identidad y Matrículas
    ("matricula", "PREST-002"),
    ("matriculas", "PREST-002"),
    ("cambio de nombre", "PREST-002"),
    ("cambiar nombre", "PREST-002"),
    ("nombre del medico", "PREST-002"),
    ("nombre en web", "PREST-002"),
    ("padding matricula", "PREST-002"),
    ("roxana fuentes", "PREST-002"),
    ("matricula caba", "PREST-002"),
    ("prefijo dr", "PREST-002"),
    ("prefijo lic", "PREST-002"),
    ("duplicidad de prestador", "PREST-002"),
    
    # Mail de Login / IAM vs Usuario vs Socio vs Sede
    ("cambio de mail de login", "IAM-001"),
    ("correo de login", "IAM-001"),
    ("correo principal", "IAM-001"),
    ("cambio de mail", "USR-001"),
    ("cambiar mail", "USR-001"),
    ("cambio de correo", "USR-001"),
    ("mail del usuario", "USR-001"),
    ("mail de socio", "SOC-001"),
    ("correo del paciente", "SOC-001"),
    ("mail de consultorio", "SEDE-001"),
    ("mail de sede", "SEDE-001"),
    
    # Módulo Socio
    ("contacto de socio", "SOC-001"),
    ("telefono de socio", "SOC-001"),
    ("notificaciones no recibidas", "SOC-001"),
    ("cache de socios", "SOC-001"),
    ("datos del socio", "SOC-001"),
    
    # Módulo Sede / Consultorio
    ("inhabilitar sede", "SEDE-001"),
    ("inhabilitacion por ic", "SEDE-001"),
    ("prefijo 1000", "SEDE-001"),
    ("telefono consultorio", "SEDE-001"),
    
    # CUIT
    ("cuit", "PREST-001"),
    ("cambio de cuit", "PREST-001"),
    
    # Diferido
    ("diferido", "PAU-001"),
    ("registro por diferido", "PAU-001"),
    ("atencion rechazada", "PAU-001"),
    ("consulta rechazada", "PAU-001"),
    
    # Recetas
    ("receta", "PDF-005"),
    ("descargar receta", "PDF-005"),
    ("receta 404", "PDF-005"),
    
    # Videoconsulta
    ("videoconsulta", "TEL-001"),
    ("jitsi", "VID-002"),
    ("pantalla blanca", "VID-002"),
    
    # Nutrición
    ("nutricion", "NUT-008"),
    ("190173", "NUT-008"),
    
    # Matrículas SISA y Bloqueos
    ("sisa", "CD2-MAT-001"),
    ("selector bloqueado", "MAT-001"),
    
    # Derivación y DW
    ("circuito de derivacion", "ESC-001"),
    ("derivacion inteligente", "ESC-001"),
    ("atencion modular", "ESC-001"),
    
    # Alta prestador
    ("alta prestador", "INST-001"),
    ("alta de prestador", "INST-001"),
    
    # Consultas que DEBEN fallar (fuera de catálogo)
    ("reparar aire acondicionado", "FALLBACK"),
    ("prestamo bancario hipotecario", "FALLBACK")
]

print(f"=== EJECUTANDO TEST DE REGRESION PERICIAL ({len(test_cases)} CASOS) ===")
failures = []
for query, expected_code in test_cases:
    res = N3CognitiveTriageEngine.analyze_incident(query)
    is_fallback = res.get("is_fallback")
    rb = res.get("matched_runbook")
    rb_title = rb["title"] if rb else "FALLBACK"
    
    passed = False
    if expected_code == "FALLBACK":
        passed = is_fallback
    else:
        passed = (not is_fallback) and (expected_code in rb_title)
        
    status = "OK" if passed else "FAIL"
    if not passed:
        failures.append((query, expected_code, rb_title, is_fallback))
    print(f"[{status:4s}] '{query:30s}' -> Esperado: {expected_code:12s} | Obtenido: {rb_title[:45]}")

print("\n" + "="*50)
print(f"TOTAL: {len(test_cases)} | EXITOSOS: {len(test_cases)-len(failures)} | FALLAS: {len(failures)}")
if failures:
    print("DETALLE DE FALLAS:")
    for q, exp, got, fb in failures:
        print(f"  * Query: '{q}' | Esperaba: '{exp}' | Obtuvo: '{got}' (is_fallback={fb})")
