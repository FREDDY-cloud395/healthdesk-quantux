from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.db.seed import run_seed

app = FastAPI(
    title="Quantux ServiceDesk Enterprise API - v8.1.0",
    description="Backend centralizado de Quantux ServiceDesk Enterprise (v8.1.0 - Lote 1 de Documentación Funcional CD2 Incorporado)",
    version="8.1.0-DEV"
)

# GZIP para aceleración de transferencia en redes móviles y tablets (90% reducción de payload)
app.add_middleware(GZipMiddleware, minimum_size=500)

# CORS para permitir conexion desde la UI Cockpit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

from app.api.endpoints import auth, tickets, masters, users, releases, team_leader, files, ai_assistant, demon

# SEED AUTOMATICO Y MOTOR DE DEMOSTRACION CONTINUA AL INICIAR
from app.services.live_simulator import start_live_simulator
from app.services.file_bot import start_file_bot

@app.on_event("startup")
def on_startup():
    run_seed()
    start_live_simulator(25)
    start_file_bot()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ENRUTADORES
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación y Roles"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["Tickets"])
app.include_router(ai_assistant.router, prefix="/api/v1/ai", tags=["Asistente IA Cognitivo N3 & Triage"])
app.include_router(files.router, prefix="/api/v1/files", tags=["Archivos y Bot Gestor"])
app.include_router(masters.router, prefix="/api/v1", tags=["Tablas Maestras"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(releases.router, prefix="/api/v1/releases", tags=["Software Releases"])
app.include_router(team_leader.router, prefix="/api/v1/team-leader", tags=["Torre de Control Team Leader"])
app.include_router(demon.router, prefix="/api/v1/demon", tags=["Demonio de Retrabajo Agéntico"])

# Configuración de Rutas de Archivos Estáticos
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
docs_dir = os.path.abspath(os.path.join(base_dir, "docs"))
frontend_dir = os.path.abspath(os.path.join(base_dir, "frontend"))

# Montar frontend en /static, /css, /js, /assets
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    css_dir = os.path.join(frontend_dir, "css")
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    js_dir = os.path.join(frontend_dir, "js")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")
    assets_dir = os.path.join(frontend_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

if os.path.exists(docs_dir):
    app.mount("/docs-files-static", StaticFiles(directory=docs_dir), name="docs_files_static")

from app.doc_viewer import serve_document

@app.get("/docs-files/{file_name:path}")
@app.get("/docs/{file_name:path}")
def route_docs_path(file_name: str, raw: bool = False):
    candidates = [
        os.path.join(docs_dir, file_name),
        os.path.join(docs_dir, f"{file_name}.md"),
        os.path.join(base_dir, file_name),
        os.path.join(base_dir, f"{file_name}.md"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return serve_document(c, os.path.basename(c), raw=raw)
    return serve_document("", file_name, raw=raw)

@app.get("/{file_name}.md")
def route_markdown_root(file_name: str, raw: bool = False):
    full_name = f"{file_name}.md"
    candidates = [
        os.path.join(docs_dir, full_name),
        os.path.join(base_dir, full_name),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return serve_document(c, os.path.basename(c), raw=raw)
    return serve_document("", full_name, raw=raw)

@app.get("/{file_name}.py")
def route_py_root(file_name: str, raw: bool = False):
    full_name = f"{file_name}.py"
    candidates = [
        os.path.join(base_dir, full_name),
        os.path.join(base_dir, "scripts", full_name),
        os.path.join(docs_dir, full_name),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return serve_document(c, os.path.basename(c), raw=raw)
    return serve_document("", full_name, raw=raw)

# Endpoints de Documentación y Cockpit Central
@app.get("/")
@app.get("/cockpit")
@app.get("/cockpit/")
@app.get("/cockpi")
def serve_cockpit():
    f = os.path.join(frontend_dir, "index.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Quantux ServiceDesk UI no encontrado"}

# PWA & Mobile App Endpoints
@app.get("/manifest.json")
def serve_manifest():
    f = os.path.join(frontend_dir, "manifest.json")
    if os.path.exists(f):
        return FileResponse(f, media_type="application/manifest+json", headers={"Cache-Control": "public, max-age=3600"})
    return {"message": "Manifest no encontrado"}

@app.get("/sw.js")
def serve_sw():
    f = os.path.join(frontend_dir, "sw.js")
    if os.path.exists(f):
        return FileResponse(f, media_type="application/javascript", headers={"Service-Worker-Allowed": "/", "Cache-Control": "no-cache"})
    return {"message": "Service Worker no encontrado"}

@app.get("/mockup-mesa-ayuda")
def serve_mockup_mesa_ayuda():
    f = os.path.join(frontend_dir, "mockup-mesa-ayuda.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Mockup Mesa de Ayuda no encontrado"}

@app.get("/scrumban")
def serve_scrumban():
    f = os.path.join(docs_dir, "00_Tablero_Scrumban_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Tablero Scrumban no encontrado"}

@app.get("/assets/{file_path:path}")
def serve_assets(file_path: str):
    p1 = os.path.join(docs_dir, "assets", file_path)
    if os.path.exists(p1):
        return FileResponse(p1, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    p2 = os.path.join(frontend_dir, "assets", file_path)
    if os.path.exists(p2):
        return FileResponse(p2, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Recurso no encontrado", "file": file_path}

@app.get("/plan")
def serve_plan():
    f = os.path.join(docs_dir, "01_Plan_de_Gestion_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Plan de Gestión no encontrado"}

@app.get("/especificacion")
@app.get("/especificacion-v4")
def serve_especificacion():
    f_v4 = os.path.join(docs_dir, "03_Especificacion_Funcional_v4.html")
    if os.path.exists(f_v4):
        return FileResponse(f_v4, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    f = os.path.join(docs_dir, "02_Especificacion_Funcional_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Especificación no encontrada"}

@app.get("/arquitectura")
def serve_arquitectura():
    f = os.path.join(docs_dir, "03_Arquitectura_Tecnica_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Arquitectura no encontrada"}

@app.get("/pruebas")
def serve_pruebas():
    f = os.path.join(docs_dir, "04_Informe_de_Pruebas_y_Evidencias_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Informe de Pruebas no encontrado"}

@app.get("/manual")
def serve_manual():
    f = os.path.join(docs_dir, "05_Manual_Operativo_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Manual de Usuario no encontrado"}

@app.get("/presentacion")
def serve_presentacion():
    f = os.path.join(docs_dir, "06_Presentacion_Ejecutiva_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Presentación no encontrada"}

@app.get("/presentacion.pptx")
@app.get("/presentacion/descargar")
def download_presentacion_pptx():
    f = os.path.join(docs_dir, "PRESENTACION_EJECUTIVA_QUANTUX_HEALTHDESK.pptx")
    if os.path.exists(f):
        return FileResponse(
            f,
            filename="PRESENTACION_EJECUTIVA_QUANTUX_HEALTHDESK.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    return {"message": "Presentación PowerPoint no encontrada"}

@app.get("/reemplazo-n1")
@app.get("/portal-n1")
@app.get("/n1")
def serve_reemplazo_n1():
    f = os.path.join(frontend_dir, "reemplazo-n1.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Interfaz Oficial de Reemplazo N1 no encontrada"}

@app.get("/propuesta-n1")
def serve_propuesta_n1_html():
    f = os.path.join(docs_dir, "Documento_Propuesta_Solucion_Reemplazo_N1_Final.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Documento Propuesta N1 no encontrado"}

@app.get("/propuesta-n1.pdf")
def download_propuesta_n1_pdf():
    f = os.path.join(docs_dir, "Propuesta_Funcional_Reemplazo_N1_OSDE_Quantux.pdf")
    if os.path.exists(f):
        return FileResponse(
            f,
            filename="Propuesta_Funcional_Reemplazo_N1_OSDE_Quantux.pdf",
            media_type="application/pdf"
        )
    return {"message": "PDF Propuesta N1 no encontrado"}

@app.get("/api")
@app.get("/health")
def api_status():
    return {
        "system": "Quantux ServiceDesk Enterprise",
        "organization": "Quantux Global Enterprise",
        "status": "ONLINE",
        "environment": "Enterprise Edition (v4.3.0)",
        "version": "4.3.0",
        "release": "Reemplazo Integral N1 OSDE (v4.3.0 • ITIL 4, KCS v6 & Densidad Silenciosa)",
        "cockpit_url": "/cockpit",
        "reemplazo_n1_url": "/reemplazo-n1",
        "propuesta_url": "/propuesta-n1",
        "propuesta_pdf_url": "/propuesta-n1.pdf",
        "scrumban_url": "/scrumban",
        "manual_url": "/manual",
        "docs_url": "/docs"
    }
