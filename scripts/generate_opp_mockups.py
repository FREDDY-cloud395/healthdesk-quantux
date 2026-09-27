"""
Generador de mockups visuales para las oportunidades de mejora del mercado (OPP-04 a OPP-12).
Genera diagramas e interfaces mockeadas de alta fidelidad para el Tablero Scrumban.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "assets", "capturas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

OPP_MOCKUPS = [
    {
        "filename": "OPP-04_copiloto_ia_resumen_resolucion.png",
        "tag": "OPP-04 • BENCHMARK ZENDESK COPILOT / SERVICENOW GENAI",
        "title": "Copiloto IA: Resumen Ejecutivo y Sugerencia de Resolución en 1 Clic",
        "badge_color": "#0284C7",
        "boxes": [
            ("Hilo Clínico Analizado", "3 intercambios con Dr. Martín Gómez (MN 39.412) sobre rechazo de token en validador CD2."),
            ("Síntesis Generativa (Resumen)", "Falla transitoria en el bus provincial SISA. Videoconsulta completada exitosamente."),
            ("Borrador Sugerido en 1 Clic", "'Estimado Dr.: Registramos la validación diferida. Puede emitir prescripción de respaldo...'")
        ],
        "status": "Benchmark Homologado • Aceleración FCR +42%"
    },
    {
        "filename": "OPP-05_macro_automatizaciones_predictivas.png",
        "tag": "OPP-05 • BENCHMARK FRESHSERVICE FREDDY / INTERCOM WORKFLOWS",
        "title": "Motor de Macro-Automatizaciones Predictivas por Intención Semántica",
        "badge_color": "#7C3AED",
        "boxes": [
            ("Detección de Intención", "Intent: 'MATRICULA_DISCREPANCIA_SISA' (Confianza: 98.4%)"),
            ("Acción Orquestada Automática", "1. Consultar endpoint /api/sisa/v2 | 2. Enviar comprobante diferido | 3. Etiquetar ticket"),
            ("Resultado Operativo", "Ticket categorizado y pre-resuelto sin intervención manual N1.")
        ],
        "status": "Benchmark Homologado • Deflexión Autónoma N1 85%"
    },
    {
        "filename": "OPP-06_asistente_flotante_pip.png",
        "tag": "OPP-06 • BENCHMARK EPIC SYSTEMS / TELADOC HEALTH",
        "title": "Asistente Flotante PiP (Picture-in-Picture) para Modo 'Atención Ininterrumpida'",
        "badge_color": "#059669",
        "boxes": [
            ("Estado Videoconsulta", "Videollamada Activa con Paciente (WebRTC Canal Cifrado)"),
            ("Widget Flotante Desacoplado", "Mini-panel superpuesto con selector de vademécum Alfabeta y contingencia papel."),
            ("Beneficio Clínico", "El médico nunca pierde contacto visual con el paciente ni minimiza la historia clínica.")
        ],
        "status": "Benchmark Homologado • Cero Fricción en Telemedicina"
    },
    {
        "filename": "OPP-07_sla_early_warning_ml.png",
        "tag": "OPP-07 • BENCHMARK SERVICENOW INCIDENT INTELLIGENCE",
        "title": "Sistema Predictivo de Alerta Temprana de SLA Breach con Riesgo ML",
        "badge_color": "#EA580C",
        "boxes": [
            ("Ticket Bajo Análisis", "#INC-2026-0947 (Falla Token en Prescripción - OSDE)"),
            ("Score de Riesgo de Quiebre", "Probabilidad de Breach: 84.2% (Tiempo restante: 18 min)"),
            ("Acción Preventiva Disparada", "Elevación de prioridad a P1 y reasignación prioritaria al Lead de Soporte.")
        ],
        "status": "Benchmark Homologado • Reducción Breach SLA 94%"
    },
    {
        "filename": "OPP-08_visor_hl7_fhir_interoperabilidad.png",
        "tag": "OPP-08 • BENCHMARK CERNER MILLENNIUM / HEALTH GORILLA",
        "title": "Visor de Interoperabilidad Clínica HL7 FHIR R4 para Contexto de Soporte",
        "badge_color": "#0D9488",
        "boxes": [
            ("Recurso FHIR Mapeado", "Bundle / Encounter / Condition / MedicationRequest (JSON R4)"),
            ("Anonimización Estricta", "DNI, Nombre y Datos Sensibles enmascarados conforme Ley 25.326."),
            ("Diagnóstico Interoperable", "Error: Discrepancia en código SNOMED-CT de prescripción farmacéutica.")
        ],
        "status": "Benchmark Homologado • Interoperabilidad HL7 FHIR"
    },
    {
        "filename": "OPP-09_telemetria_webrtc_conmutacion_preventiva.png",
        "tag": "OPP-09 • BENCHMARK ZOOM PHONE / TEAMS TELEHEALTH",
        "title": "Telemetría WebRTC Proactiva y Conmutación Preventiva a Audio/Contingencia",
        "badge_color": "#2563EB",
        "boxes": [
            ("Métricas en Tiempo Real", "Jitter: 42ms | Packet Loss: 6.8% | RTT: 180ms | Video Bitrate: Degradado"),
            ("Alerta Proactiva N1", "Conexión inestable detectada antes de interrupción de videoconsulta."),
            ("Conmutación Automática", "Sugerencia en 1 clic: 'Conmutar a Audio HD de bajo consumo o contingencia telefónica'.")
        ],
        "status": "Benchmark Homologado • Continuidad Asistencial 99.9%"
    },
    {
        "filename": "OPP-10_busqueda_semantica_vectorial_kb.png",
        "tag": "OPP-10 • BENCHMARK PINECONE / ALGOLIA AI / SERVICENOW AI SEARCH",
        "title": "Motor de Búsqueda Semántica Vectorial sobre KB y Vademécum",
        "badge_color": "#9333EA",
        "boxes": [
            ("Query No Estructurada", "'el doctor no encuentra el remedio para la presion del socio'"),
            ("Recuperación Vectorial", "Match 96.2%: CD2-REC-003 'Vademécum Alfabeta: Búsqueda por Monodroga'"),
            ("Impacto Operativo", "Resolución instantánea sin requerir códigos técnicos ni palabras exactas.")
        ],
        "status": "Benchmark Homologado • Búsqueda Híbrida Vectorial + BM25"
    },
    {
        "filename": "OPP-11_orquestador_ola_multiequipo_skills.png",
        "tag": "OPP-11 • BENCHMARK JIRA SERVICE MANAGEMENT / PAGERDUTY",
        "title": "Orquestador de Acuerdos OLA Multiequipo con Asignación por Skills y Carga",
        "badge_color": "#4F46E5",
        "boxes": [
            ("Matriz OLA Integrada", "N1 -> N2: 15 min | N2 -> Especialistas N3: 45 min | N3 -> DevOps: 2 horas"),
            ("Asignación por Habilidad", "Especialidad requerida: 'SISA / Microservicios Redis' -> Asignado a Analista N2 Senior"),
            ("Balanceo de Carga", "Ponderación de tickets activos para evitar sobrecarga operativa.")
        ],
        "status": "Benchmark Homologado • Cumplimiento ITIL 4 OLA 99%"
    },
    {
        "filename": "OPP-12_generador_rca_postmortem_1clic.png",
        "tag": "OPP-12 • BENCHMARK PAGERDUTY POSTMORTEMS / DATADOG RCA",
        "title": "Generador Automatizado de Informes Periciales Post-Mortem y RCA con 1 Clic",
        "badge_color": "#DC2626",
        "boxes": [
            ("Incidente Cerrado", "#INC-2026-0812 (Interrupción Masiva Validador OSDE)"),
            ("Compilación Forense", "Timeline de alertas, logs de auditor, tickets vinculados y MTTR compilados."),
            ("Informe Homologado", "Exportación PDF/Word con dictamen formal para auditoría médica y dirección.")
        ],
        "status": "Benchmark Homologado • Reporte Pericial Certificado"
    }
]

def generate_mockup(data):
    width, height = 760, 420
    im = Image.new("RGB", (width, height), color="#0F172A")
    draw = ImageDraw.Draw(im)

    # Background card container
    draw.rounded_rectangle([15, 15, width - 15, height - 15], radius=12, fill="#1E293B", outline="#334155", width=2)

    # Header bar
    draw.rounded_rectangle([25, 25, width - 25, 80], radius=8, fill="#0F172A", outline="#475569", width=1)
    
    # Tag badge
    draw.rounded_rectangle([35, 33, 500, 52], radius=4, fill=data["badge_color"])
    draw.text((42, 36), data["tag"], fill="#FFFFFF")

    # Title
    draw.text((35, 58), data["title"], fill="#F8FAFC")

    # 3 Content Boxes
    y_start = 95
    box_height = 80
    gap = 12

    for idx, (label, content) in enumerate(data["boxes"]):
        y_pos = y_start + idx * (box_height + gap)
        draw.rounded_rectangle([25, y_pos, width - 25, y_pos + box_height], radius=6, fill="#0F172A", outline="#334155", width=1)
        
        # Section pill
        draw.rounded_rectangle([35, y_pos + 10, 240, y_pos + 28], radius=3, fill="#334155")
        draw.text((42, y_pos + 12), label, fill="#38BDF8")
        
        # Content text
        draw.text((35, y_pos + 38), content, fill="#CBD5E1")

    # Footer
    footer_y = height - 42
    draw.text((35, footer_y), data["status"], fill="#10B981")
    draw.text((width - 240, footer_y), "QuantUX ServiceDesk v4.0", fill="#64748B")

    filepath = os.path.join(OUTPUT_DIR, data["filename"])
    im.save(filepath, "PNG")
    print(f"Generado: {filepath}")

if __name__ == "__main__":
    for item in OPP_MOCKUPS:
        generate_mockup(item)
    print("Todos los mockups de oportunidades generados exitosamente.")
