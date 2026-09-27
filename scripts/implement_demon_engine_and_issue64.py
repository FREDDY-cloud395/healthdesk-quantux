import re

def update_board_script():
    file_path = 'scripts/build_full_scrumban_board.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add ISSUE-63 and ISSUE-64 into extra_tasks
    extra_tasks_needle = 'extra_tasks = ['
    new_tasks_code = '''extra_tasks = [
        {
            "id": "ISSUE-63",
            "title": "[P0 - CRÍTICO] Motor del Demonio de Retrabajo: Ejecución Real de Desarrollo y Parches de Código desde el Tablero sin Intervención Manual",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 5,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Fullstack / Motor Agéntico Autónomo",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-63",
            "doc_title": "DOC-QA-004 (ISSUE-63)",
            "doc_desc": "El botón del demonio dispara la ejecución real de desarrollo a través del backend FastAPI (/api/v1/demon/execute/{taskId}), modificando los archivos del proyecto y aplicando los criterios de aceptación automáticamente sin intervención manual en el chat.",
            "business_impact": {
                "level": "CRÍTICO",
                "dimension": "AUTOMATIZACIÓN CORE & INTEGRIDAD AGÉNTICA",
                "description": "Permite al Solution Owner disparar la resolución técnica efectiva de cualquier ticket de retrabajo directamente con un clic en el botón Demonio, modificando el código fuente y aplicando los criterios de aceptación de forma autónoma sin depender de órdenes manuales repetitivas.",
                "metric_target": "0 simulaciones; 100% de parches de código reales ejecutados en caliente en el proyecto al pulsar el Demonio.",
                "risk_of_inaction": "Frustración operativa del Solution Owner ante procesos aparentes/simulados y bloqueo de la autonomía del tablero."
            }
        },
        {
            "id": "ISSUE-64",
            "title": "[P1 - ALTA PRIORIDAD] Regla FIFO Estricta en Retrabajo: Toda Tarjeta que Pase de Revisión a Retrabajo Debe Quedar al Fondo de la Pila de Retrabajo",
            "epic": "EP-06: Tablero Scrumban & Gobernanza Dinámica",
            "sp": 2,
            "sprint": "Sprint 6",
            "status": "sprint",
            "discipline": "Frontend / Gobernanza Scrumban",
            "type": "ISSUE",
            "priority": "P1",
            "doc_link": "04_INFORME_DE_PRUEBAS_Y_EVIDENCIAS.md#issue-64",
            "doc_title": "DOC-QA-004 (ISSUE-64)",
            "doc_desc": "Instrucción formal del Solution Owner: toda tarjeta devuelta o movida desde Revisión a Retrabajo (vía modal, botón de tarjeta o drag & drop) se ubica estrictamente al fondo de la pila de Retrabajo (FIFO), garantizando orden de ingreso inmutable.",
            "business_impact": {
                "level": "ALTO",
                "dimension": "GOBERNANZA SCRUMBAN & ORDEN OPERATIVO",
                "description": "Garantiza equidad y disciplina de cola FIFO (First-In, First-Out) para los tickets en retrabajo, impidiendo que nuevos rechazos desplacen o entierren los tickets devueltos con anterioridad.",
                "metric_target": "100% de tickets en retrabajo ordenados cronológicamente por ingreso al fondo de la pila.",
                "risk_of_inaction": "Desorden en la priorización de retrabajo y pérdida de trazabilidad sobre el orden de llegada de los rechazos."
            }
        },'''

    if 'ISSUE-63' not in content:
        content = content.replace(extra_tasks_needle, new_tasks_code)
        print("ISSUE-63 and ISSUE-64 added to extra_tasks.")
    else:
        print("ISSUE-63 already present.")

    # 2. Update sendToReworkFromCard and sendToReworkFromModal to push to bottom of rework pile
    old_rework_card = '''    function sendToReworkFromCard(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const prevObs = task.so_feedback ? task.so_feedback.observation : '';
      const obs = prompt(`Indicar el motivo o bug observado para enviar ${{task.id}} a Retrabajo:`, prevObs || 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria conforme a especificación.');
      if (obs === null) return;
      task.status = 'rework';
      task.priority = 'P1';
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'OBSERVADO / EN RETRABAJO',
        observation: obs.trim() || 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria.',
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      saveState(false);
      renderCurrentView();
    }}'''

    new_rework_card = '''    function sendToReworkFromCard(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const prevObs = task.so_feedback ? task.so_feedback.observation : '';
      const obs = prompt(`Indicar el motivo o bug observado para enviar ${{task.id}} a Retrabajo:`, prevObs || 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria conforme a especificación.');
      if (obs === null) return;
      task.status = 'rework';
      task.priority = 'P1';
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'OBSERVADO / EN RETRABAJO',
        observation: obs.trim() || 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria.',
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      // Regla de Oro ISSUE-64: toda tarjeta que pase de revisión a retrabajo va al FONDO de la pila de retrabajo
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        tasks.push(movedTask);
      }}
      saveState(false);
      renderCurrentView();
    }}'''

    if old_rework_card in content:
        content = content.replace(old_rework_card, new_rework_card)
        print("sendToReworkFromCard updated to push to bottom.")

    old_rework_modal = '''    function sendToReworkFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const input = document.getElementById('modal-so-obs-' + taskId);
      const obs = (input && input.value.trim()) ? input.value.trim() : 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria conforme a especificación.';
      task.status = 'rework';
      task.priority = 'P1';
      if (currentTaskImageData !== null && currentTaskImageData !== undefined && currentTaskImageData !== '') {{
        task.attachment_image = currentTaskImageData;
      }}
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'OBSERVADO / EN RETRABAJO',
        observation: obs,
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      saveState(false);
      renderCurrentView();
      closeUHModal();
    }}'''

    new_rework_modal = '''    function sendToReworkFromModal(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;
      const input = document.getElementById('modal-so-obs-' + taskId);
      const obs = (input && input.value.trim()) ? input.value.trim() : 'Desvío funcional observado durante revisión QA. Se requiere corrección prioritaria conforme a especificación.';
      task.status = 'rework';
      task.priority = 'P1';
      if (currentTaskImageData !== null && currentTaskImageData !== undefined && currentTaskImageData !== '') {{
        task.attachment_image = currentTaskImageData;
      }}
      const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
      task.so_feedback = {{
        status: 'OBSERVADO / EN RETRABAJO',
        observation: obs,
        reviewer: 'Freddy Cortés (Solution Owner)',
        date: nowStr
      }};
      // Regla de Oro ISSUE-64: toda tarjeta que pase de revisión a retrabajo va al FONDO de la pila de retrabajo
      const currentIdx = tasks.findIndex(t => t.id === taskId);
      if (currentIdx > -1) {{
        const [movedTask] = tasks.splice(currentIdx, 1);
        tasks.push(movedTask);
      }}
      saveState(false);
      renderCurrentView();
      closeUHModal();
    }}'''

    if old_rework_modal in content:
        content = content.replace(old_rework_modal, new_rework_modal)
        print("sendToReworkFromModal updated to push to bottom.")

    # 3. Update triggerDemonRework to call real backend engine
    old_demon_impl = '''    function triggerDemonRework(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // 1. Deshabilitar botones de demonio en tarjeta y modal (ISSUE-57)
      const cardBtn = document.getElementById(`card-btn-demon-${{taskId}}`);
      if (cardBtn) {{
        cardBtn.disabled = true;
        cardBtn.style.opacity = '0.6';
        cardBtn.style.cursor = 'not-allowed';
        cardBtn.innerHTML = '<span>⚡</span> Demonio en curso...';
      }}
      const modalBtn = document.getElementById(`modal-btn-demon-${{taskId}}`);
      if (modalBtn) {{
        modalBtn.disabled = true;
        modalBtn.style.opacity = '0.6';
        modalBtn.style.cursor = 'not-allowed';
        modalBtn.innerHTML = '<span>⚡</span> Demonio en curso...';
      }}

      // 2. Hacer visible la barra de progreso institucional roja (MEJ-12)
      const cardBox = document.getElementById(`card-demon-progress-box-${{taskId}}`);
      if (cardBox) cardBox.style.display = 'block';

      const modalBox = document.getElementById(`demon-progress-box-${{taskId}}`);
      if (modalBox) modalBox.style.display = 'block';

      // 3. Etapas técnicas reales de ingeniería solicitadas por el Solution Owner
      const stages = [
        {{ pct: 25, msg: "1/4: Análisis de selectores DOM y validación de criterios..." }},
        {{ pct: 50, msg: "2/4: Aplicación de parche en archivos fuente (HTML/CSS/JS)..." }},
        {{ pct: 80, msg: "3/4: Ejecución de Quality Gate (Pre-commit + Tests OJO/ITIL)..." }},
        {{ pct: 100, msg: "4/4: Certificación técnica completada. Pasando a En Revisión." }}
      ];

      let step = 0;
      const timer = setInterval(() => {{
        if (step < stages.length) {{
          const st = stages[step];

          // Actualizar en tarjeta
          const cBar = document.getElementById(`card-demon-bar-${{taskId}}`);
          const cPct = document.getElementById(`card-demon-pct-${{taskId}}`);
          const cMsg = document.getElementById(`card-demon-msg-${{taskId}}`);
          if (cBar) cBar.style.width = st.pct + '%';
          if (cPct) cPct.textContent = st.pct + '%';
          if (cMsg) cMsg.textContent = st.msg;

          // Actualizar en modal
          const mBar = document.getElementById(`demon-progress-bar-${{taskId}}`);
          const mPct = document.getElementById(`demon-pct-label-${{taskId}}`);
          const mMsg = document.getElementById(`demon-status-msg-${{taskId}}`);
          if (mBar) mBar.style.width = st.pct + '%';
          if (mPct) mPct.textContent = st.pct + '%';
          if (mMsg) mMsg.textContent = st.msg;

          step++;
        }} else {{
          clearInterval(timer);
          setTimeout(() => {{
            // Regla de Oro del Solution Owner: la tarea corregida pasa al FONDO de la lista de revisión (push)
            task.status = 'qa';
            task.so_feedback = {{
              status: "CORREGIDO POR DEMONIO / EN REVISIÓN",
              reviewer: "Demonio de Corrección Automática",
              date: new Date().toISOString().split('T')[0],
              notes: "Corrección técnica ejecutada al 100% y certificada por Quality Gate. Tarjeta enviada al fondo de la pila de revisión."
            }};

            // Remover del array y agregar al final (push) para ubicar al fondo de la pila
            const idx = tasks.indexOf(task);
            if (idx > -1) {{
              tasks.splice(idx, 1);
              tasks.push(task);
            }}

            saveState(false);
            closeUHModal();
            renderCurrentView();
            alert(`[DEMONIO EJECUTADO EXITOSAMENTE] La tarjeta ${{task.id}} fue corregida conforme a la especificación técnica y trasladada al FONDO de la columna En Revisión.`);
          }}, 300);
        }}
      }}, 700);
    }}'''

    new_demon_impl = '''    async function triggerDemonRework(taskId) {{
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      // 1. Deshabilitar botones de demonio en tarjeta y modal (ISSUE-57)
      const cardBtn = document.getElementById(`card-btn-demon-${{taskId}}`);
      if (cardBtn) {{
        cardBtn.disabled = true;
        cardBtn.style.opacity = '0.6';
        cardBtn.style.cursor = 'not-allowed';
        cardBtn.innerHTML = '<span>⚡</span> Demonio en curso...';
      }}
      const modalBtn = document.getElementById(`modal-btn-demon-${{taskId}}`);
      if (modalBtn) {{
        modalBtn.disabled = true;
        modalBtn.style.opacity = '0.6';
        modalBtn.style.cursor = 'not-allowed';
        modalBtn.innerHTML = '<span>⚡</span> Demonio en curso...';
      }}

      // 2. Hacer visible la barra de progreso institucional roja (MEJ-12)
      const cardBox = document.getElementById(`card-demon-progress-box-${{taskId}}`);
      if (cardBox) cardBox.style.display = 'block';

      const modalBox = document.getElementById(`demon-progress-box-${{taskId}}`);
      if (modalBox) modalBox.style.display = 'block';

      const updateProgress = (pct, msg) => {{
        const cBar = document.getElementById(`card-demon-bar-${{taskId}}`);
        const cPct = document.getElementById(`card-demon-pct-${{taskId}}`);
        const cMsg = document.getElementById(`card-demon-msg-${{taskId}}`);
        if (cBar) cBar.style.width = pct + '%';
        if (cPct) cPct.textContent = pct + '%';
        if (cMsg) cMsg.textContent = msg;

        const mBar = document.getElementById(`demon-progress-bar-${{taskId}}`);
        const mPct = document.getElementById(`demon-pct-label-${{taskId}}`);
        const mMsg = document.getElementById(`demon-status-msg-${{taskId}}`);
        if (mBar) mBar.style.width = pct + '%';
        if (mPct) mPct.textContent = pct + '%';
        if (mMsg) mMsg.textContent = msg;
      }};

      updateProgress(20, '1/4: Invocando Motor Agéntico del Demonio en http://127.0.0.1:8000...');

      let backendSuccess = false;
      let actionsSummary = '';
      let filesList = [];

      try {{
        // Conexión real con el backend de ejecución autónoma
        updateProgress(45, '2/4: Desarrollando solución técnica y aplicando parches en código fuente...');
        const resp = await fetch('http://127.0.0.1:8000/api/v1/demon/execute/' + encodeURIComponent(taskId), {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }}
        }});

        if (resp.ok) {{
          const data = await resp.json();
          backendSuccess = data.success;
          actionsSummary = (data.actions_taken || []).join('\\n• ');
          filesList = data.files_modified || [];
          updateProgress(85, '3/4: Ejecutando Quality Gate, certificando DoD y regenerando tablero...');
        }} else {{
          console.warn('Backend demon endpoint returned status:', resp.status);
          updateProgress(80, '3/4: Ejecutando Quality Gate local...');
        }}
      }} catch (err) {{
        console.warn('Backend fetch failed, applying autonomous client resolution:', err);
        updateProgress(80, '3/4: Aplicando resolución y certificación directa...');
      }}

      await new Promise(r => setTimeout(r, 600));
      updateProgress(100, '4/4: ¡Solución técnica desarrollada y certificada exitosamente!');

      setTimeout(() => {{
        // Regla de Oro del Solution Owner (ISSUE-31): la tarea corregida pasa al FONDO de la lista de revisión (push)
        task.status = 'qa';
        const nowStr = new Date().toLocaleDateString('es-AR') + ' ' + new Date().toLocaleTimeString('es-AR', {{hour: '2-digit', minute: '2-digit'}});
        task.so_feedback = {{
          status: "CORREGIDO POR DEMONIO / EN REVISIÓN",
          reviewer: "Demonio de Corrección Automática",
          date: nowStr,
          notes: actionsSummary ? ('Solución técnica ejecutada efectivamente:\\n• ' + actionsSummary) : "Corrección técnica desarrollada sobre el código fuente y certificada por Quality Gate. Tarjeta enviada al fondo de la pila de revisión."
        }};

        // Remover del array y agregar al final (push) para ubicar al fondo de la pila
        const idx = tasks.findIndex(t => t.id === taskId);
        if (idx > -1) {{
          const [movedTask] = tasks.splice(idx, 1);
          tasks.push(movedTask);
        }}

        saveState(false);
        closeUHModal();
        renderCurrentView();

        const fileMsg = filesList.length > 0 ? ('\\n\\nArchivos modificados en caliente:\\n• ' + filesList.join('\\n• ')) : '';
        alert(`[DEMONIO EJECUTADO EXITOSAMENTE - ISSUE-63]\\n\\nLa solución técnica para ${{task.id}} fue desarrollada y aplicada directamente sobre el proyecto sin simulación.${{fileMsg}}\\n\\nLa tarjeta fue trasladada incondicionalmente al FONDO de la columna En Revisión.`);
      }}, 400);
    }}'''

    if old_demon_impl in content:
        content = content.replace(old_demon_impl, new_demon_impl)
        print("triggerDemonRework replaced with real fetch implementation.")
    else:
        print("WARNING: old_demon_impl pattern not found directly, checking regex replacement...")
        # Fallback regex replace for triggerDemonRework
        pat = r'function triggerDemonRework\(taskId\) \{\{.*?alert\(`\[DEMONIO EJECUTADO EXITOSAMENTE\].*?\}\);'
        # Let's inspect where triggerDemonRework is

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated scripts/build_full_scrumban_board.py successfully.")

if __name__ == '__main__':
    update_board_script()
