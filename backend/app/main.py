from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.db.seed import run_seed
from app.api.endpoints import auth, tickets, masters, users

app = FastAPI(
    title="Quantux ServiceDesk Enterprise API",
    description="Backend centralizado de Quantux ServiceDesk Enterprise (Ambiente de Desarrollo en la Nube v4.0.0-DEV)",
    version="4.0.0-DEV"
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

# SEED AUTOMATICO AL INICIAR
@app.on_event("startup")
def on_startup():
    run_seed()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ENRUTADORES
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación y Roles"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["Tickets"])
app.include_router(masters.router, prefix="/api/v1", tags=["Tablas Maestras"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios"])

# Configuración de Rutas de Archivos Estáticos
docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

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
    app.mount("/docs-files", StaticFiles(directory=docs_dir), name="docs_files")

# Endpoints de Documentación y Cockpit Central
@app.get("/")
@app.get("/cockpit")
def serve_cockpit():
    f = os.path.join(frontend_dir, "index.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Quantux ServiceDesk UI no encontrado"}

@app.get("/scrumban")
def serve_scrumban():
    f = os.path.join(docs_dir, "00_Tablero_Scrumban_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Tablero Scrumban no encontrado"}

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

@app.get("/api")
@app.get("/health")
def api_status():
    return {
        "system": "Quantux ServiceDesk Enterprise",
        "organization": "Quantux Global Enterprise",
        "status": "ONLINE",
        "environment": "Cloud Development (v4.0.0-DEV)",
        "version": "4.0.0-DEV",
        "release": "Ambiente de Desarrollo en la Nube (v4.0.0-DEV)",
        "cockpit_url": "/cockpit",
        "scrumban_url": "/scrumban",
        "manual_url": "/manual",
        "docs_url": "/docs"
    }
