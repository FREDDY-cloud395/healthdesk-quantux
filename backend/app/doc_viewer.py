import os
import html
from fastapi.responses import FileResponse, HTMLResponse

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ — Suite Documental Oficial Quantux</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <script src="/assets/marked.min.js"></script>
  <style>
    :root {
      --q-navy: #1E3A5F;
      --q-navy-dark: #142842;
      --q-navy-soft: #2D4B73;
      --q-teal: #00C4B4;
      --q-teal-light: #E0F7F5;
      --q-bg: #F8FAFC;
      --q-border: #E2E8F0;
      --q-text-main: #1E293B;
      --q-text-muted: #64748B;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--q-bg);
      color: var(--q-text-main);
      line-height: 1.6;
      font-size: 13.5px;
    }

    /* TOPBAR */
    .doc-topbar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--q-navy);
      color: #FFFFFF;
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--q-teal);
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }

    .doc-topbar-left {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .doc-logo {
      font-family: 'Montserrat', sans-serif;
      font-weight: 800;
      font-size: 15px;
      letter-spacing: -0.5px;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .doc-logo span { color: var(--q-teal); }

    .doc-badge {
      background: rgba(0, 196, 180, 0.18);
      color: #5EEAD4;
      border: 1px solid rgba(0, 196, 180, 0.4);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }

    .doc-topbar-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-doc {
      background: rgba(255, 255, 255, 0.1);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      cursor: pointer;
    }

    .btn-doc:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: var(--q-teal);
    }

    .btn-doc-primary {
      background: var(--q-teal);
      color: var(--q-navy-dark);
      border-color: var(--q-teal);
      font-weight: 700;
    }

    .btn-doc-primary:hover {
      background: #00A89A;
      color: #FFFFFF;
    }

    /* LAYOUT */
    .doc-layout {
      display: flex;
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
      gap: 28px;
    }

    /* SIDEBAR TOC */
    .doc-sidebar {
      width: 290px;
      flex-shrink: 0;
      position: sticky;
      top: 75px;
      max-height: calc(100vh - 95px);
      overflow-y: auto;
      background: #FFFFFF;
      border: 1px solid var(--q-border);
      border-radius: 8px;
      padding: 16px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .doc-sidebar h4 {
      font-family: 'Montserrat', sans-serif;
      font-size: 12px;
      font-weight: 800;
      color: var(--q-navy);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--q-border);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .doc-toc-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .doc-toc-item a {
      color: var(--q-text-muted);
      text-decoration: none;
      font-size: 11.5px;
      display: block;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.15s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .doc-toc-item a:hover {
      color: var(--q-navy);
      background: #F1F5F9;
    }

    .doc-toc-item.level-1 a { font-weight: 700; color: var(--q-navy); }
    .doc-toc-item.level-2 a { padding-left: 14px; }
    .doc-toc-item.level-3 a { padding-left: 22px; font-size: 10.5px; color: #64748B; }

    /* CONTENT ARTICLE */
    .doc-main {
      flex: 1;
      min-width: 0;
      background: #FFFFFF;
      border: 1px solid var(--q-border);
      border-radius: 8px;
      padding: 36px 48px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    /* MARKDOWN STYLES */
    .markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4 {
      font-family: 'Montserrat', sans-serif;
      color: var(--q-navy);
      margin-top: 26px;
      margin-bottom: 12px;
      font-weight: 800;
      line-height: 1.3;
    }

    .markdown-body h1 {
      font-size: 22px;
      border-bottom: 2px solid var(--q-teal);
      padding-bottom: 8px;
      margin-top: 0;
    }

    .markdown-body h2 {
      font-size: 17px;
      border-bottom: 1px solid var(--q-border);
      padding-bottom: 6px;
    }

    .markdown-body h3 { font-size: 14.5px; }
    .markdown-body h4 { font-size: 13px; color: var(--q-navy-soft); }

    .markdown-body p { margin-bottom: 12px; color: #334155; }
    .markdown-body ul, .markdown-body ol { margin-bottom: 14px; padding-left: 24px; }
    .markdown-body li { margin-bottom: 5px; }

    .markdown-body code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      background: #F1F5F9;
      color: #BE123C;
      padding: 2px 5px;
      border-radius: 4px;
      border: 1px solid #E2E8F0;
    }

    .markdown-body pre {
      background: #0F172A;
      color: #E2E8F0;
      padding: 14px 18px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 14px 0;
    }

    .markdown-body pre code {
      background: transparent;
      color: inherit;
      border: none;
      padding: 0;
      font-size: 12px;
    }

    .markdown-body table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 12px;
    }

    .markdown-body th, .markdown-body td {
      border: 1px solid var(--q-border);
      padding: 8px 12px;
      text-align: left;
    }

    .markdown-body th {
      background: #F8FAFC;
      font-family: 'Montserrat', sans-serif;
      font-weight: 700;
      color: var(--q-navy);
    }

    .markdown-body tr:nth-child(even) td { background: #FAFAFA; }

    .markdown-body blockquote {
      border-left: 4px solid var(--q-teal);
      padding: 8px 14px;
      margin: 14px 0;
      background: #F0FDFA;
      color: #0F766E;
      border-radius: 0 6px 6px 0;
    }

    .markdown-body img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid var(--q-border);
      margin: 12px 0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* ANCHOR HIGHLIGHT */
    .highlight-target {
      outline: 3px solid var(--q-teal) !important;
      background: #E0F7F5 !important;
      transition: all 0.4s ease;
      border-radius: 4px;
      padding: 4px 8px !important;
      box-shadow: 0 0 15px rgba(0, 196, 180, 0.4);
    }

    @media (max-width: 900px) {
      .doc-layout { flex-direction: column; padding: 14px; }
      .doc-sidebar { width: 100%; position: static; max-height: none; }
      .doc-main { padding: 20px; }
    }
  </style>
</head>
<body>
  <header class="doc-topbar">
    <div class="doc-topbar-left">
      <div class="doc-logo">
        QUANTUX <span>HEALTHDESK</span>
      </div>
      <span class="doc-badge">DOCUMENTO RECTOR OFICIAL</span>
      <span style="font-size: 12px; font-weight: 600; color: #94A3B8;">__FILENAME__</span>
    </div>
    <div class="doc-topbar-actions">
      <a href="/scrumban" class="btn-doc btn-doc-primary">
        <span>📋</span> Volver al Tablero Scrumban
      </a>
      <a href="?raw=true" class="btn-doc" title="Descargar o ver archivo en texto plano">
        <span>📄</span> Raw / Descargar
      </a>
      <button onclick="window.print()" class="btn-doc">
        <span>🖨️</span> Imprimir / PDF
      </button>
    </div>
  </header>

  <div class="doc-layout">
    <aside class="doc-sidebar">
      <h4><span>📑</span> Contenido del Documento</h4>
      <ul class="doc-toc-list" id="doc-toc"></ul>
    </aside>

    <main class="doc-main">
      <div id="markdown-container" class="markdown-body">
        <div style="text-align: center; padding: 40px; color: #64748B;">
          Cargando documento oficial...
        </div>
      </div>
    </main>
  </div>

  <textarea id="raw-markdown-data" style="display: none;">__MARKDOWN_CONTENT__</textarea>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const raw = document.getElementById('raw-markdown-data').value;
      const container = document.getElementById('markdown-container');
      const toc = document.getElementById('doc-toc');

      if (window.marked) {
        container.innerHTML = marked.parse(raw);
      } else {
        container.innerHTML = '<pre>' + raw.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
      }

      // Generar TOC dinámico desde H1, H2, H3
      const headings = container.querySelectorAll('h1, h2, h3');
      headings.forEach((h, idx) => {
        const text = h.textContent.trim();
        const tag = h.tagName.toLowerCase();
        let id = h.id || text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        if (!id) id = 'section-' + idx;
        h.id = id;

        const li = document.createElement('li');
        li.className = 'doc-toc-item level-' + (tag === 'h1' ? '1' : tag === 'h2' ? '2' : '3');
        li.innerHTML = `<a href="#${id}" title="${text}">${text}</a>`;
        toc.appendChild(li);
      });

      // Función de salto inteligente a Anchor
      function handleAnchor() {
        const hash = window.location.hash ? decodeURIComponent(window.location.hash.substring(1)).toLowerCase() : '';
        if (!hash) return;

        let el = document.getElementById(hash) || document.getElementById(hash.toUpperCase());
        if (!el) {
          // Búsqueda inteligente por contenido de texto (ej. UH-68, ISSUE-07, etc.)
          const allEls = container.querySelectorAll('h1, h2, h3, h4, h5, li, strong, p, tr');
          for (const cand of allEls) {
            if (cand.textContent.toLowerCase().includes(hash)) {
              el = cand;
              break;
            }
          }
        }

        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          el.classList.add('highlight-target');
          setTimeout(() => el.classList.remove('highlight-target'), 3500);
        }
      }

      // Ejecutar salto al cargar y al cambiar de hash
      setTimeout(handleAnchor, 250);
      window.addEventListener('hashchange', handleAnchor);
    });
  </script>
</body>
</html>
"""

def serve_document(file_path: str, file_name: str, raw: bool = False):
    """
    Entrega el documento en formato HTML visualizador o FileResponse.
    """
    if not os.path.exists(file_path):
        return HTMLResponse(
            f"<h2>404 - Documento Oficial no encontrado</h2><p>El archivo <code>{file_name}</code> no existe en el repositorio.</p><a href='/scrumban'>Volver al Tablero Scrumban</a>",
            status_code=404
        )

    # Si es HTML directo
    if file_path.endswith(".html"):
        return FileResponse(file_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

    # Si el usuario pide el archivo crudo/raw
    if raw:
        media_type = "text/markdown; charset=utf-8" if file_path.endswith(".md") else "text/plain; charset=utf-8"
        return FileResponse(file_path, media_type=media_type)

    # Si es Markdown, renderizar en el visor oficial
    if file_path.endswith(".md"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()

        # Reemplazar caracteres especiales para textarea seguro
        escaped_content = html.escape(content)
        title = os.path.splitext(file_name)[0].replace("_", " ")

        rendered = HTML_TEMPLATE.replace("__TITLE__", title)
        rendered = rendered.replace("__FILENAME__", file_name)
        rendered = rendered.replace("__MARKDOWN_CONTENT__", escaped_content)

        return HTMLResponse(rendered, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

    # Si es Python o código fuente
    if file_path.endswith((".py", ".js", ".css", ".json")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception:
            with open(file_path, "r", encoding="latin-1") as f:
                code_content = f.read()

        md_wrapped = f"# Código Fuente: {file_name}\n\n```python\n{code_content}\n```"
        escaped_content = html.escape(md_wrapped)
        title = f"Código: {file_name}"

        rendered = HTML_TEMPLATE.replace("__TITLE__", title)
        rendered = rendered.replace("__FILENAME__", file_name)
        rendered = rendered.replace("__MARKDOWN_CONTENT__", escaped_content)

        return HTMLResponse(rendered, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

    # Otros archivos (PDF, PNG, etc.)
    return FileResponse(file_path)
