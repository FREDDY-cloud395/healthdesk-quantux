with open('scripts/build_full_scrumban_board.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace unescaped braces in the client init patch
bad_block = '''      INITIAL_BACKLOG.forEach(initTask => {
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

good_block = '''      INITIAL_BACKLOG.forEach(initTask => {{
        const existing = tasks.find(t => t.id === initTask.id);
        if (!existing) {{
          tasks.push(JSON.parse(JSON.stringify(initTask)));
        }} else {{
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
          if (REWORK_SO_SET.has(initTask.id)) {{
            existing.status = 'rework';
            existing.priority = 'P1';
            existing.so_feedback = initTask.so_feedback;
          }}
          // Forzar presencia en Sprint Backlog de tareas solicitadas para este sprint si no están en done
          if (SPRINT6_NEW_SET.has(initTask.id) && existing.status !== 'done') {{
            existing.status = 'sprint';
            existing.sprint = 'Sprint 6';
            existing.priority = 'P1';
          }}
        }}
      }});'''

text = text.replace(bad_block, good_block)

with open('scripts/build_full_scrumban_board.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Braces escaped properly.")
