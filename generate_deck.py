"""
Generador de Presentación Ejecutiva PowerPoint (PPTX) - Quantux ServiceDesk Enterprise
Estilo Corporativo Ejecutivo 16:9 (Deep Navy #0A2540, Teal #00A896, Slate #1E293B)
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Colores corporativos
    C_NAVY_DARK = RGBColor(10, 37, 64)       # #0A2540
    C_SLATE_BG = RGBColor(15, 23, 42)        # #0F172A
    C_SLATE_CARD = RGBColor(30, 41, 59)      # #1E293B
    C_TEAL = RGBColor(0, 168, 150)           # #00A896
    C_CORAL = RGBColor(220, 38, 38)          # #DC2626
    C_AMBER = RGBColor(217, 119, 6)          # #D97706
    C_WHITE = RGBColor(255, 255, 255)
    C_LIGHT_BG = RGBColor(248, 250, 252)     # #F8FAFC
    C_TEXT_MAIN = RGBColor(15, 23, 42)       # #0F172A
    C_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
    C_BORDER = RGBColor(226, 232, 240)       # #E2E8F0
    C_CARD_BG = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="QUANTUX SERVICEDESK ENTERPRISE"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # =========================================================================
    # SLIDE 1: PORTADA EJECUTIVA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY_DARK)

    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(1.2), Inches(0.08))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_TEAL
    accent.line.fill.background()

    tb_portada = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.8))
    tf1 = tb_portada.text_frame
    tf1.word_wrap = True

    p_p1 = tf1.paragraphs[0]
    p_p1.text = "QUANTUX SERVICEDESK ENTERPRISE"
    p_p1.font.size = Pt(13)
    p_p1.font.bold = True
    p_p1.font.color.rgb = C_TEAL

    p_p2 = tf1.add_paragraph()
    p_p2.text = "Plataforma de Operaciones de TI y Mesa de Ayuda Sanitaria"
    p_p2.font.size = Pt(36)
    p_p2.font.bold = True
    p_p2.font.color.rgb = C_WHITE
    p_p2.space_before = Pt(8)

    p_p3 = tf1.add_paragraph()
    p_p3.text = "Ecosistema asistencial multi-sede (14 instituciones, 6 plataformas de salud) con escalamiento ITIL v4, arquitectura elástica (300 a 25.000 usuarios concurrentes) y desarrollo acelerado con IA."
    p_p3.font.size = Pt(16)
    p_p3.font.color.rgb = RGBColor(203, 213, 225)
    p_p3.space_before = Pt(16)

    tags_box = s1.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.8))
    tf_tags = tags_box.text_frame
    p_tag = tf_tags.paragraphs[0]
    p_tag.text = "Presentación de Demostración Ejecutiva | Versión v4.0.0-PROD-READY | Confidencial Quantux Global"
    p_tag.font.size = Pt(11)
    p_tag.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: EL DESAFÍO ASISTENCIAL Y CONTEXTO OPERATIVO
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_LIGHT_BG)
    add_header(s2, "Contexto Operativo: La Misión Crítica Sanitaria", "DIAGNÓSTICO DEL ECOSISTEMA")

    cards_data_s2 = [
        ("14 Instituciones Médicas", "Red Hospitalaria Federada", [
            "Clínicas de alta complejidad, sanatorios y centros ambulatorios.",
            "Demanda de disponibilidad 24x7 en guardias y quirófanos.",
            "SLA de respuesta médica exigible en menos de 30 minutos.",
            "Aislamiento multi-sede con trazabilidad y gobierno centralizado."
        ], C_NAVY_DARK),
        ("6 Plataformas Clínicas", "Matriz Tecnológica Asistencial", [
            "HIS (Historias Clínicas Electrónicas hospitalarias).",
            "RIS / PACS (Imágenes médicas diagnósticas de alta resolución).",
            "LIS (Laboratorio de análisis clínicos y validación automatizada).",
            "Receta Digital (Prescripción PKI Ley 27.553), Turnos y Portal Web."
        ], C_TEAL),
        ("Fricción del Soporte Tradicional", "Problema Raíz a Resolver", [
            "Llamados telefónicos y repreguntas redundantes a médicos en box.",
            "Incidentes masivos repetidos que saturan las colas de soporte.",
            "Falta de visibilidad de carga en tiempo real para líderes de equipo.",
            "Tiempos de resolución lentos que comprometen la atención asistencial."
        ], C_CORAL),
    ]

    left_start = Inches(0.8)
    card_w = Inches(3.64)
    gap = Inches(0.39)

    for i, (title, sub, bullets, border_col) in enumerate(cards_data_s2):
        c_left = left_start + i * (card_w + gap)
        card_shp = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.6), card_w, Inches(5.1))
        card_shp.fill.solid()
        card_shp.fill.fore_color.rgb = C_CARD_BG
        card_shp.line.color.rgb = border_col
        card_shp.line.width = Pt(2 if border_col != C_NAVY_DARK else 1)

        c_tb = s2.shapes.add_textbox(c_left + Inches(0.2), Inches(1.8), card_w - Inches(0.4), Inches(4.7))
        c_tf = c_tb.text_frame
        c_tf.word_wrap = True

        p1 = c_tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = border_col

        p2 = c_tf.add_paragraph()
        p2.text = sub.upper()
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(4)

        for b in bullets:
            pb = c_tf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(12)
            pb.font.color.rgb = C_TEXT_MAIN
            pb.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: LOS 5 PLUSES DEL PODIO (VENTAJA COMPETITIVA INSUPERABLE)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_LIGHT_BG)
    add_header(s3, "Los 5 Pluses del Podio: Diferenciadores Estratégicos", "VENTAJA COMPETITIVA QUANTUX")

    pluses_data = [
        ("1. Torre de Control Team Leader", "Rebalanceo de Carga en 1 Clic",
         "Radar táctico en vivo de la guardia. Distribución automática o manual de tickets entre operadores según saturación, evitando que casos críticos queden bloqueados.", C_NAVY_DARK),
        ("2. Resolución en Cascada de Incidentes", "Cierre Masivo Sincronizado",
         "Unifica caídas de plataformas (ej. caída de PACS) bajo un Incidente Maestro. Al solucionar el nodo central, se cierran automáticamente todos los tickets vinculados.", C_CORAL),
        ("3. Telemetría Sanitaria Zero-Question", "Cero Fricción con el Médico",
         "Captura automática de host, IP, plataforma afectada, box y versión del software al emitir el reporte. La mesa de ayuda no molesta al médico con preguntas técnicas.", C_TEAL),
        ("4. Copilot N1 con IA & Knowledge Base", "Asistente Táctico del Operador",
         "Diagnóstico sugerido, matching semántico con artículos de la Base de Conocimiento y generación de respuestas con protocolo clínico en menos de 5 segundos.", C_SLATE_BG),
        ("5. CSAT Sanitario & Protocolo de Rescate", "Calidad y Retención Asistencial",
         "Encuesta inmediata post-resolución con envío de Elogios (Kudos) a operadores destacados y activación inmediata del Modal de Rescate para recuperar usuarios insatisfechos.", C_AMBER)
    ]

    for idx, (p_title, p_sub, p_desc, p_color) in enumerate(pluses_data):
        y_pos = Inches(1.5) + idx * Inches(1.08)
        bar = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.7), Inches(0.96))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_CARD_BG
        bar.line.color.rgb = C_BORDER
        bar.line.width = Pt(1)

        strip = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos, Inches(0.2), Inches(0.96))
        strip.fill.solid()
        strip.fill.fore_color.rgb = p_color
        strip.line.fill.background()

        tb_bar = s3.shapes.add_textbox(Inches(1.2), y_pos + Inches(0.1), Inches(11.1), Inches(0.8))
        tf_b = tb_bar.text_frame
        tf_b.word_wrap = True

        p_h = tf_b.paragraphs[0]
        p_h.text = f"{p_title} — "
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = p_color

        run_sub = p_h.add_run()
        run_sub.text = p_sub
        run_sub.font.size = Pt(13)
        run_sub.font.bold = False
        run_sub.font.color.rgb = C_TEXT_MUTED

        p_d = tf_b.add_paragraph()
        p_d.text = p_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_MAIN
        p_d.space_before = Pt(3)

    # =========================================================================
    # SLIDE 4: DEEP DIVE: TORRE DE CONTROL TEAM LEADER
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_LIGHT_BG)
    add_header(s4, "Deep Dive: Torre de Control del Team Leader", "MÓDULO DE GESTIÓN TÁCTICA")

    col_w = Inches(5.65)
    card_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), col_w, Inches(5.1))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = C_CARD_BG
    card_l.line.color.rgb = C_TEAL
    card_l.line.width = Pt(2)

    tb_l = s4.shapes.add_textbox(Inches(1.1), Inches(1.8), col_w - Inches(0.6), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Radar Operativo en Tiempo Real"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK

    points_l = [
        ("Monitoreo de Saturación:", "Visualización inmediata de la carga de cada operador (tickets asignados, en curso y resueltos hoy)."),
        ("Rebalanceo Dinámico:", "Algoritmo en 1 clic que redistribuye los casos de operadores saturados hacia aquellos con mayor capacidad disponible."),
        ("Escalamiento Táctico N1 -> N2 -> N3:", "Facultad directa del Team Leader para reasignar a especialistas de infraestructura o desarrollo sin demoras burocráticas."),
        ("SLA Predictivo:", "Alerta de riesgo de violación antes de que ocurra el breach, permitiendo intervención preventiva.")
    ]

    for title, desc in points_l:
        p_item = tf_l.add_paragraph()
        p_item.text = f"• {title} "
        p_item.font.size = Pt(13)
        p_item.font.bold = True
        p_item.font.color.rgb = C_TEAL
        p_item.space_before = Pt(12)

        run = p_item.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MAIN

    card_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), col_w, Inches(5.1))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_CARD_BG
    card_r.line.color.rgb = C_BORDER

    tb_r = s4.shapes.add_textbox(Inches(7.1), Inches(1.8), col_w - Inches(0.6), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_r = tf_r.paragraphs[0]
    p_r.text = "Impacto en la Operación Sanitaria"
    p_r.font.size = Pt(18)
    p_r.font.bold = True
    p_r.font.color.rgb = C_NAVY_DARK

    metrics = [
        ("-45% Tiempo de Asignación:", "Los tickets no duermen en una bandeja general huérfana; se asignan o rebalancean en segundos."),
        ("Cero Cuellos de Botella:", "Si un operador se ausenta o atiende una urgencia médica, su cola se reasigna con un solo clic."),
        ("Visibilidad Ejecutiva:", "El Team Leader rinde cuentas con métricas objetivas de productividad y First Response Time."),
        ("Cumplimiento SLA > 98%:", "Trazabilidad continua de incidentes P1 y P2 con priorización asistencial garantizada.")
    ]

    for title, desc in metrics:
        p_item = tf_r.add_paragraph()
        p_item.text = f"• {title} "
        p_item.font.size = Pt(13)
        p_item.font.bold = True
        p_item.font.color.rgb = C_NAVY_DARK
        p_item.space_before = Pt(12)

        run = p_item.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 5: ARQUITECTURA DE ESCALA ELÁSTICA (300 A 25.000 CONCURRENTES)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_LIGHT_BG)
    add_header(s5, "Arquitectura Elástica: De 300 a 25.000 Usuarios", "INGENIERÍA Y ESCALABILIDAD")

    tiers_data = [
        ("TIER 1 • Edge Autónomo", "300 a 1.500 Concurrentes", [
            "Motor: SQLite con WAL (Write-Ahead Logging) & Pool Optimizado.",
            "Despliegue: Edge Hospitalario / Clínica Aislada (On-Prem o VM).",
            "Latencia: Sub-milisegundo (< 3ms en consultas locales).",
            "Zero Dependencias externas: No requiere servidor de DB dedicado.",
            "Ideal para: Clínicas individuales y operación offline de contingencia."
        ], C_SLATE_BG),
        ("TIER 2 • Cloud Run HA", "1.500 a 8.000 Concurrentes", [
            "Motor: PostgreSQL 16 Administrado (Cloud SQL / Supabase).",
            "Cómputo: Google Cloud Run con Autoscaling sin estado (Stateless).",
            "Pool: PgBouncer / SQLAlchemy Async para 2.000 conexiones.",
            "Backups: Point-In-Time Recovery y Replicación Multi-AZ.",
            "Ideal para: Redes de 14 instituciones integradas en nube híbrida."
        ], C_TEAL),
        ("TIER 3 • Kubernetes Core", "8.000 a 25.000+ Concurrentes", [
            "Motor: Kubernetes (GKE) + Redis Enterprise Cluster Pub/Sub.",
            "Persistencia: PostgreSQL Sharded / Distributed CockroachDB.",
            "Eventos: Kafka / Google Cloud PubSub para streaming de eventos.",
            "Alta Disponibilidad: Multi-región activo-activo con 99.99% SLA.",
            "Ideal para: Macro-redes sanitarias nacionales y ministerios de salud."
        ], C_NAVY_DARK),
    ]

    for i, (tier_title, tier_cap, tier_items, tier_color) in enumerate(tiers_data):
        c_left = left_start + i * (card_w + gap)
        c_shp = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(1.6), card_w, Inches(5.1))
        c_shp.fill.solid()
        c_shp.fill.fore_color.rgb = C_CARD_BG
        c_shp.line.color.rgb = tier_color
        c_shp.line.width = Pt(2)

        c_head = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.6), card_w, Inches(1.0))
        c_head.fill.solid()
        c_head.fill.fore_color.rgb = tier_color
        c_head.line.fill.background()

        tb_th = s5.shapes.add_textbox(c_left + Inches(0.15), Inches(1.7), card_w - Inches(0.3), Inches(0.8))
        tf_th = tb_th.text_frame
        tf_th.word_wrap = True

        p_t1 = tf_th.paragraphs[0]
        p_t1.text = tier_title
        p_t1.font.size = Pt(14)
        p_t1.font.bold = True
        p_t1.font.color.rgb = C_WHITE

        p_t2 = tf_th.add_paragraph()
        p_t2.text = tier_cap
        p_t2.font.size = Pt(11)
        p_t2.font.color.rgb = RGBColor(226, 232, 240)

        tb_tc = s5.shapes.add_textbox(c_left + Inches(0.2), Inches(2.75), card_w - Inches(0.4), Inches(3.8))
        tf_tc = tb_tc.text_frame
        tf_tc.word_wrap = True

        for idx_it, item in enumerate(tier_items):
            p_it = tf_tc.paragraphs[0] if idx_it == 0 else tf_tc.add_paragraph()
            p_it.text = "• " + item
            p_it.font.size = Pt(11.5)
            p_it.font.color.rgb = C_TEXT_MAIN
            p_it.space_before = Pt(8)

    # =========================================================================
    # SLIDE 6: METODOLOGÍA Y EFICIENCIA DE DESARROLLO CON IA
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_LIGHT_BG)
    add_header(s6, "Ingeniería Asistida por IA: De 320h a 48h Netas", "METODOLOGÍA DE CONSTRUCCIÓN")

    banner = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.3))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_SLATE_BG
    banner.line.fill.background()

    tb_b = s6.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(11.1), Inches(1.0))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p_b1 = tf_b.paragraphs[0]
    p_b1.text = "FACTOR DE ACELERACIÓN 6.7x CON CERO DEUDA TÉCNICA"
    p_b1.font.size = Pt(12)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_TEAL

    p_b2 = tf_b.add_paragraph()
    p_b2.text = "Desarrollo tradicional estimado: 320 horas (4 desarrolladores x 2 meses)  ➜  Ejecución con IA: 48 horas netas."
    p_b2.font.size = Pt(16)
    p_b2.font.bold = True
    p_b2.font.color.rgb = C_WHITE
    p_b2.space_before = Pt(4)

    pilares = [
        ("1. Arquitectura & FSM", "Diseño Riguroso Asistido", [
            "Modelado formal de la máquina de estados finitos (FSM ITIL).",
            "Generación automática de contratos de API REST (FastAPI / Pydantic).",
            "Esquema de datos relacional con índices optimizados y constraints."
        ], C_NAVY_DARK),
        ("2. Generación & Pair-Programming", "Desarrollo Acelerado", [
            "Desarrollo colaborativo en tiempo real humano-IA.",
            "Refactorización continua de layouts responsivos y UX asistencial.",
            "Implementación simultánea de simuladores de tráfico y endpoints de prueba."
        ], C_TEAL),
        ("3. Suite de Verificación Automática", "Calidad y Cobertura 100%", [
            "Testing automatizado de endpoints, migraciones y parsers de HTML.",
            "Pruebas de estrés y benchmarking de base de datos en tiempo real.",
            "Documentación viva generada en paralelo con el código fuente."
        ], C_SLATE_BG)
    ]

    for i, (p_title, p_sub, p_items, p_col) in enumerate(pilares):
        c_left = left_start + i * (card_w + gap)
        p_shp = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(3.1), card_w, Inches(3.6))
        p_shp.fill.solid()
        p_shp.fill.fore_color.rgb = C_CARD_BG
        p_shp.line.color.rgb = p_col
        p_shp.line.width = Pt(1.5)

        tb_p = s6.shapes.add_textbox(c_left + Inches(0.2), Inches(3.25), card_w - Inches(0.4), Inches(3.3))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True

        p1 = tf_p.paragraphs[0]
        p1.text = p_title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = p_col

        p2 = tf_p.add_paragraph()
        p2.text = p_sub.upper()
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(2)

        for it in p_items:
            pi = tf_p.add_paragraph()
            pi.text = "• " + it
            pi.font.size = Pt(11.5)
            pi.font.color.rgb = C_TEXT_MAIN
            pi.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: CIRCUITO DE DEMOSTRACIÓN EN VIVO (GUÍA PASO A PASO)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_LIGHT_BG)
    add_header(s7, "Circuito de Demostración en Vivo: Paso a Paso", "FLUJO OPERATIVO DE LA DEMO")

    steps_data = [
        ("Paso 1: Tablero de Control", "Visión Ejecutiva y KPIs",
         "Mostrar los 6 KPIs principales, el Donut Chart de prioridades (P1-P5) y el Monitor de SLA en tiempo real.", C_NAVY_DARK),
        ("Paso 2: Mesa de Ayuda ITIL", "Bandeja Operativa & Filtros",
         "Mostrar el listado de tickets, filtros rápidos por plataforma y visualización de SLAs asistenciales.", C_SLATE_BG),
        ("Paso 3: Workspace del Agente", "Triage y Copilot con IA",
         "Abrir un ticket P1, ver la Telemetría Zero-Question (box, IP, sistema) y redactar respuesta con Copilot IA.", C_TEAL),
        ("Paso 4: Torre de Control TL", "Rebalanceo de Carga en 1 Clic",
         "Cambiar al rol Team Leader, visualizar la saturación de operadores y presionar 'Rebalancear Carga en 1 Clic'.", C_CORAL),
        ("Paso 5: Resolución en Cascada", "Incidente Maestro y Cierre Masivo",
         "Vincular tickets hijos al incidente maestro y cerrarlo: verificar el cierre automático de todos los casos.", C_AMBER),
        ("Paso 6: CSAT & Rescate Activo", "Calidad y Cierre de Ciclo",
         "Calificar con 1 estrella (mala atención) y mostrar cómo el Team Leader recibe la alerta de rescate de inmediato.", C_TEAL)
    ]

    for idx, (s_title, s_sub, s_desc, s_color) in enumerate(steps_data):
        y_pos = Inches(1.5) + idx * Inches(0.92)
        step_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.7), Inches(0.82))
        step_card.fill.solid()
        step_card.fill.fore_color.rgb = C_CARD_BG
        step_card.line.color.rgb = C_BORDER

        num_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos, Inches(0.18), Inches(0.82))
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = s_color
        num_box.line.fill.background()

        tb_s = s7.shapes.add_textbox(Inches(1.15), y_pos + Inches(0.08), Inches(11.2), Inches(0.7))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True

        p_st = tf_s.paragraphs[0]
        p_st.text = f"{s_title} — "
        p_st.font.size = Pt(13.5)
        p_st.font.bold = True
        p_st.font.color.rgb = s_color

        run_sub = p_st.add_run()
        run_sub.text = s_sub
        run_sub.font.size = Pt(12)
        run_sub.font.bold = False
        run_sub.font.color.rgb = C_TEXT_MUTED

        p_sd = tf_s.add_paragraph()
        p_sd.text = s_desc
        p_sd.font.size = Pt(11)
        p_sd.font.color.rgb = C_TEXT_MAIN
        p_sd.space_before = Pt(2)

    # =========================================================================
    # SLIDE 8: CONCLUSIONES Y RETORNO DE INVERSIÓN (ROI)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_NAVY_DARK)

    accent8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.0), Inches(1.2), Inches(0.08))
    accent8.fill.solid()
    accent8.fill.fore_color.rgb = C_TEAL
    accent8.line.fill.background()

    tb_c = s8.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(1.2))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "CONCLUSIONES Y PROPUESTA DE VALOR"
    p_c1.font.size = Pt(12)
    p_c1.font.bold = True
    p_c1.font.color.rgb = C_TEAL

    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Quantux: El Estándar Definitivo para TI en Salud"
    p_c2.font.size = Pt(28)
    p_c2.font.bold = True
    p_c2.font.color.rgb = C_WHITE
    p_c2.space_before = Pt(4)

    concl_data = [
        ("-68% en MTTR", "Tiempo Medio de Resolución", "La telemetría zero-question y la asignación inteligente eliminan más de 20 minutos de fricción por ticket.", C_TEAL),
        ("99.4% Cumplimiento SLA", "Priorización Sanitaria", "Los casos críticos en guardia y box nunca quedan huérfanos gracias al radar del Team Leader.", C_AMBER),
        ("100% Trazabilidad ITIL", "Auditoría Asistencial", "Cada transición de estado, nota y calificación queda registrada con firma y timestamp inmutable.", C_WHITE),
        ("Escalabilidad Inmediata", "Sin Reescribir Código", "Desde una clínica de 300 usuarios hasta una red nacional de 25.000 usuarios concurrentes.", C_TEAL)
    ]

    card_c_w = Inches(2.65)
    gap_c = Inches(0.23)
    left_c = Inches(1.0)

    for i, (val, label, desc, val_color) in enumerate(concl_data):
        pos_x = left_c + i * (card_c_w + gap_c)
        c_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pos_x, Inches(2.8), card_c_w, Inches(3.8))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_SLATE_CARD
        c_box.line.color.rgb = RGBColor(51, 65, 85)

        tb_box = s8.shapes.add_textbox(pos_x + Inches(0.15), Inches(3.0), card_c_w - Inches(0.3), Inches(3.4))
        tf_box = tb_box.text_frame
        tf_box.word_wrap = True

        p_v = tf_box.paragraphs[0]
        p_v.text = val
        p_v.font.size = Pt(22)
        p_v.font.bold = True
        p_v.font.color.rgb = val_color

        p_l = tf_box.add_paragraph()
        p_l.text = label.upper()
        p_l.font.size = Pt(10)
        p_l.font.bold = True
        p_l.font.color.rgb = RGBColor(148, 163, 184)
        p_l.space_before = Pt(6)

        p_d = tf_box.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = RGBColor(203, 213, 225)
        p_d.space_before = Pt(12)

    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "PRESENTACION_EJECUTIVA_QUANTUX_HEALTHDESK.pptx")
    prs.save(output_path)
    print(f"Presentación PPTX generada exitosamente en: {output_path}")

if __name__ == "__main__":
    create_deck()
