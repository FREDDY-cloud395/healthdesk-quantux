import re
import os
import json

def update_board():
    board_py = 'scripts/build_full_scrumban_board.py'
    with open(board_py, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add MEJ-16 if not present
    if '"id": "MEJ-16"' not in content:
        mej16_block = '''        {
            "id": "MEJ-16",
            "title": "[Sprint 7] Directiva de Diseño Quantux: Erradicación de Colores Rojos y Tonos Rojizos en Barras de Progreso e Interfaz, Alineación a Paleta Oficial (Cyan/Slate/Azul)",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 3,
            "sprint": "Sprint 7",
            "status": "todo",
            "discipline": "Frontend / Design System & UX Governance",
            "type": "MEJ",
            "priority": "P1",
            "doc_link": "02_ESPECIFICACION_FUNCIONAL_Y_BACKLOG.md#mej-16",
            "doc_title": "DOC-REQ-014 (MEJ-16)",
            "doc_desc": "Sustitución de colores rojos y tonos rojizos en barras de progreso e interfaces por la paleta oficial Quantux (#00C4B4, #0284C7, #0F172A).",
            "attachment_image": "assets/capturas/MEJ-16_evitar_colores_rojos_paleta_quantux.png",
            "business_impact": {
                "level": "ALTO",
                "dimension": "Identidad Visual de Marca & Ergonomía Cognitiva Quantux",
                "description": "Erradica el uso de tonos rojos/rojizos en elementos informativos o de avance que generan alarma innecesaria en el usuario, consolidando una interfaz médica serena y profesional alineada a los cánones Quantux.",
                "metric_target": "100% de apego a la paleta oficial (#00C4B4, #0284C7, #0F172A); 0 elementos de progreso con gradientes o fondos rojizos.",
                "risk_of_inaction": "Percepción errónea de fallo o estrés visual por parte de los operadores médicos ante barras de progreso de aspecto crítico."
            },
            "issue_details": {
                "severity": "P1 — Alta Prioridad / Directiva Expresa de Diseño del Solution Owner",
                "component": "docs/00_Tablero_Scrumban_Quantux.html, frontend/css, scripts/build_full_scrumban_board.py",
                "description": "El Solution Owner dictaminó: 'evita usar los colores Rojo y tonos rojisos, aplica esta mejora en el sprint 7, estás guardando todo lo que te digo que va en el sprint siete ?'.",
                "root_cause": "Uso previo de acentos rojos (#DC2626, #450A0A) en barras de avance y componentes que deben migrarse a la paleta identitaria de Quantux.",
                "solution": "1. Reemplazar estilos y gradientes rojizos por la paleta Quantux: Cyan (#00C4B4), Azul Profesional (#0284C7), Dark Slate (#0F172A) y fondos neutros suaves (#F8FAFC);\\n2. Aplicar la directiva en barras de progreso y componentes en Sprint 7 conforme a la orden del Solution Owner;\\n3. Catalogar con impacto en negocio y preservar trazabilidad en el Backlog.",
                "acceptance_criteria": [
                    "Escenario 1 (Erradicación de Rojos): Las barras de progreso y elementos de estado eliminan fondos y acentos rojizos (#450A0A, #DC2626) adoptando el Cyan/Azul Quantux.",
                    "Escenario 2 (Planificación en Sprint 7): La tarea queda formalmente registrada en Sprint 7 como mejora P1 catalogada por impacto.",
                    "Escenario 3 (Trazabilidad): El Solution Owner visualiza la tarjeta en el Sprint Backlog del Sprint 7 con su impacto de negocio registrado."
                ]
            }
        },'''
        # insert after MEJ-15 closing brace
        m = re.search(r'("id":\s*"MEJ-15".*?\}\s*\},)', content, re.DOTALL)
        if m:
            content = content[:m.end()] + '\n' + mej16_block + content[m.end():]
            print("MEJ-16 inserted successfully.")

    # 2. Add ISSUE-59, ISSUE-60, ISSUE-61, ISSUE-62 in extra_tasks if not present
    if '"id": "ISSUE-59"' not in content:
        # Load from update_scrumban_sprint6.py or append
        import scripts.update_scrumban_sprint6 as upd
        # We already have new_tasks_code in update_scrumban_sprint6.py
        pass

    # 3. Update client-side init() in build_full_scrumban_board.py to guarantee proper columns
    client_init_patch = '''      // Asegurar que todas las tareas del INITIAL_BACKLOG existan en tasks con metadatos actualizados
      const REWORK_SO_SET = new Set(["ISSUE-06", "ISSUE-34", "MEJ-11", "ISSUE-41", "MEJ-12"]);
      const SPRINT6_NEW_SET = new Set(["ISSUE-59", "ISSUE-60", "ISSUE-61", "ISSUE-62"]);

      INITIAL_BACKLOG.forEach(initTask => {
        const existing = tasks.find(t => t.id === initTask.id);
        if (!existing) {
          tasks.push(JSON.parse(JSON.stringify(initTask)));
        } else {
          existing.title = initTask.title;
          existing.sprint = initTask.sprint;
          existing.sp = initTask.sp;
          existing.priority = initTask.priority;
          existing.type = initTask.type;
          existing.discipline = initTask.discipline;
          if (initTask.business_impact) existing.business_impact = initTask.business_impact;
          if (initTask.doc_link) existing.doc_link = initTask.doc_link;
          if (initTask.doc_title) existing.doc_title = initTask.doc_title;
          if (initTask.doc_desc) existing.doc_desc = initTask.doc_desc;
          if (initTask.attachment_image) existing.attachment_image = initTask.attachment_image;
          if (initTask.issue_details) existing.issue_details = initTask.issue_details;
          if (initTask.acceptance_criteria) existing.acceptance_criteria = initTask.acceptance_criteria;

          // Forzar estado de retrabajo dictado por el Solution Owner
          if (REWORK_SO_SET.has(initTask.id)) {
            existing.status = 'rework';
            existing.priority = 'P1';
            existing.so_feedback = initTask.so_feedback;
          }
          // Forzar presencia en Sprint Backlog de tareas solicitadas para este sprint si no están en done
          if (SPRINT6_NEW_SET.has(initTask.id) && existing.status !== 'done') {
            existing.status = 'sprint';
            existing.sprint = 'Sprint 6';
            existing.priority = 'P1';
          }
        }
      });'''

    # Replace the existing loop in init()
    old_loop_pattern = r'// Asegurar que todas las tareas del INITIAL_BACKLOG existan en tasks con metadatos actualizados.*?INITIAL_BACKLOG\.forEach\(initTask => \{.*?\}\);\s*\}'
    # Use re.sub with caution or exact match
    target_needle = "// Asegurar que todas las tareas del INITIAL_BACKLOG existan en tasks con metadatos actualizados"
    if target_needle in content:
        start_pos = content.find(target_needle)
        end_needle = "// Blindaje de Gobernanza Permanente"
        end_pos = content.find(end_needle, start_pos)
        if start_pos != -1 and end_pos != -1:
            content = content[:start_pos] + client_init_patch + '\n\n      ' + content[end_pos:]
            print("client_init_patch applied successfully.")

    with open(board_py, 'w', encoding='utf-8') as f:
        f.write(content)
    print("build_full_scrumban_board.py updated.")

if __name__ == '__main__':
    update_board()
