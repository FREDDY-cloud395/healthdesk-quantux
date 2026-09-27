import re

def apply_fixes():
    file_path = 'scripts/build_full_scrumban_board.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update ISSUE-31 to rework with so_feedback and new screenshot
    old_issue_31 = '''            "id": "ISSUE-31",
            "title": "[P1 - ALTA PRIORIDAD] Ejecución del Demonio y Paso Automático de la Tarjeta al Fondo de la Pila de Revisión",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "qa",
            "discipline": "Frontend / Automatización Scrumban",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-31",
            "doc_title": "DOC-QA-004 (ISSUE-31)",
            "doc_desc": "Al hacer clic sobre el demonio de retrabajo, la tarea se ejecuta y al finalizar se posiciona estrictamente al fondo de la pila de revisión.",
            "attachment_image": "assets/capturas/ISSUE-31_demonio_fondo_de_pila.png",'''

    new_issue_31 = '''            "id": "ISSUE-31",
            "title": "[P1 - ALTA PRIORIDAD] Ejecución del Demonio y Paso Automático de Toda Tarjeta que Pase de Retrabajo a Revisión al Fondo de la Pila",
            "epic": "EP-07: Gobernanza PMI+IA, Blindaje OJO & Calidad",
            "sp": 3,
            "sprint": "Sprint 6",
            "status": "rework",
            "so_feedback": {
                "status": "RECHAZADO - ENVIADO A RETRABAJO",
                "observation": "Criterios de Aceptación Verificables (Gherkin). Escenario 1: DADO el clic sobre el botón del demonio, CUANDO finaliza la animación y corrección, ENTONCES la tarjeta pasa a 'En Revisión' al fondo de la lista. Este punto no está resuelto, toda tarjeta que pase de retrabajo a revisión debe ir al fondo de la pila de revisión, pasa a retrabajo.",
                "reviewer": "Freddy Cortés (Solution Owner)",
                "date": "2026-09-27"
            },
            "discipline": "Frontend / Automatización Scrumban",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-31",
            "doc_title": "DOC-QA-004 (ISSUE-31)",
            "doc_desc": "Al hacer clic sobre el demonio o mover de retrabajo a revisión, la tarjeta se posiciona incondicionalmente al fondo de la pila de revisión (FIFO estricto).",
            "attachment_image": "assets/capturas/ISSUE-31_boton_guardar_informacion_modal_retrabajo.png",'''

    if old_issue_31 in content:
        content = content.replace(old_issue_31, new_issue_31)
        print("ISSUE-31 updated to rework.")
    else:
        print("WARNING: old_issue_31 pattern not matched exactly, checking regex...")
        content = re.sub(
            r'("id":\s*"ISSUE-31",\s*"title":\s*"[^"]*",\s*"epic":\s*"[^"]*",\s*"sp":\s*\d+,\s*"sprint":\s*"Sprint 6",\s*"status":\s*)"qa"',
            r'\1"rework",\n            "so_feedback": {\n                "status": "RECHAZADO - ENVIADO A RETRABAJO",\n                "observation": "Criterios de Aceptación Verificables (Gherkin). Escenario 1: DADO el clic sobre el botón del demonio, CUANDO finaliza la animación y corrección, ENTONCES la tarjeta pasa a \'En Revisión\' al fondo de la lista. Este punto no está resuelto, toda tarjeta que pase de retrabajo a revisión debe ir al fondo de la pila de revisión, pasa a retrabajo.",\n                "reviewer": "Freddy Cortés (Solution Owner)",\n                "date": "2026-09-27"\n            }',
            content
        )

    # 2. Add ISSUE-31 to REWORK sets
    content = content.replace(
        '["ISSUE-06", "ISSUE-34", "MEJ-11", "ISSUE-41", "MEJ-12"]',
        '["ISSUE-06", "ISSUE-31", "ISSUE-34", "MEJ-11", "ISSUE-41", "MEJ-12"]'
    )

    # 3. Add the missing observation handler functions
    # Locate updateCardObservation
    obs_funcs = '''    function saveObservationFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const obsInput = document.getElementById('modal-so-obs-' + taskId);
      const val = obsInput ? obsInput.value.trim() : '';

      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      if (!task.so_feedback) {{
        task.so_feedback = {{
          status: 'OBSERVADO / EN RETRABAJO',
          observation: val,
          reviewer: 'Freddy Cortés (Solution Owner)',
          date: nowStr
        }};
      }} else {{
        task.so_feedback.observation = val;
        task.so_feedback.date = nowStr;
      }}

      if (currentTaskImageData) {{
        task.attachment_image = currentTaskImageData;
      }}

      saveState(false);
      renderCurrentView();

      // Feedback visual interactivo en el botón
      const btn = event && event.currentTarget ? event.currentTarget : null;
      if (btn) {{
        const origText = btn.innerHTML;
        btn.innerHTML = '<span>✅</span> ¡Guardado!';
        btn.style.background = '#16A34A';
        setTimeout(() => {{
          btn.innerHTML = origText;
          btn.style.background = '#2563EB';
        }}, 1600);
      }} else {{
        alert('✓ Observación técnica guardada exitosamente.');
      }}
    }}

    function appendObservationFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const extra = prompt('Escribí la nueva observación o detalle a sumar a la tarjeta ' + taskId + ':');
      if (!extra || !extra.trim()) return;

      const obsInput = document.getElementById('modal-so-obs-' + taskId);
      const prevVal = obsInput ? obsInput.value.trim() : (task.so_feedback ? task.so_feedback.observation : '');
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      const updatedVal = prevVal ? (prevVal + '\\n\\n[' + nowStr + ' - Solution Owner]: ' + extra.trim()) : ('[' + nowStr + ' - Solution Owner]: ' + extra.trim());

      if (obsInput) obsInput.value = updatedVal;
      updateCardObservation(taskId, updatedVal);
      saveState(false);
      renderCurrentView();
      alert('✓ Nueva observación sumada y guardada exitosamente.');
    }}

    function saveCardObservation(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const cardInput = document.getElementById('card-obs-' + taskId);
      const val = cardInput ? cardInput.value.trim() : '';
      updateCardObservation(taskId, val);
      saveState(false);
      renderCurrentView();

      const btn = event && event.currentTarget ? event.currentTarget : null;
      if (btn) {{
        const origText = btn.innerHTML;
        btn.innerHTML = '<span>✓</span>';
        btn.style.background = '#16A34A';
        setTimeout(() => {{
          btn.innerHTML = origText;
          btn.style.background = '#2563EB';
        }}, 1400);
      }}
    }}

    function appendCardObservation(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const extra = prompt('Escribí la nueva observación a sumar:');
      if (!extra || !extra.trim()) return;
      const cardInput = document.getElementById('card-obs-' + taskId);
      const prevVal = cardInput ? cardInput.value.trim() : (task.so_feedback ? task.so_feedback.observation : '');
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      const updatedVal = prevVal ? (prevVal + '\\n\\n[' + nowStr + ']: ' + extra.trim()) : ('[' + nowStr + ']: ' + extra.trim());
      if (cardInput) cardInput.value = updatedVal;
      updateCardObservation(taskId, updatedVal);
      saveState(false);
      renderCurrentView();
    }}
'''

    if 'function saveObservationFromModal' not in content:
        # insert after updateCardObservation
        target_needle = 'saveState(false);\n    }'
        if target_needle in content:
            pos = content.find(target_needle) + len(target_needle)
            content = content[:pos] + '\n\n' + obs_funcs + content[pos:]
            print("Observation functions inserted successfully.")
        else:
            print("Target needle not found, checking double braces...")
            target_needle2 = 'saveState(false);\n    }}'
            pos = content.find(target_needle2) + len(target_needle2)
            content = content[:pos] + '\n\n' + obs_funcs + content[pos:]
            print("Observation functions inserted successfully after double braces.")

    # 4. Update drop handler to enforce that cards moving to QA go strictly to the BOTTOM (push)
    old_drop_slice = '''      task.status = colName;
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        tasks.unshift(movedTask);
      }}'''

    new_drop_slice = '''      const previousStatus = task.status;
      task.status = colName;
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        // Regla de Oro del Solution Owner: toda tarjeta que pase de retrabajo a revisión (o entre a QA) va al FONDO de la lista (FIFO estricto)
        if (colName === 'qa' || previousStatus === 'rework') {{
          tasks.push(movedTask);
        }} else {{
          tasks.unshift(movedTask);
        }}
      }}'''

    if old_drop_slice in content:
        content = content.replace(old_drop_slice, new_drop_slice)
        print("Drop handler updated to push to bottom when entering QA.")
    else:
        print("Drop slice pattern not matched directly, checking...")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Fixes applied to scripts/build_full_scrumban_board.py.")

if __name__ == '__main__':
    apply_fixes()
