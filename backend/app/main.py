from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.seed import run_seed
from app.api.endpoints import auth, tickets, masters, users

app = FastAPI(
    title="HealthDesk Quantux API",
    description="Backend oficial del Sistema Centralizado de Gestión de Tickets de Soporte de Quantux Salud",
    version="2.5.0"
)

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

# RUTA AL DIRECTORIO FRONTEND Y DOCS
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))

if os.path.exists(frontend_dir):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

if os.path.exists(docs_dir):
    app.mount("/docs-files", StaticFiles(directory=docs_dir), name="docs_files")

@app.get("/")
@app.get("/cockpit")
def serve_cockpit():
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Frontend no encontrado"}

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
def serve_especificacion():
    f = os.path.join(docs_dir, "02_Especificacion_Funcional_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Especificación no encontrada"}

@app.get("/presentacion")
def serve_presentacion():
    f = os.path.join(docs_dir, "06_Presentacion_Ejecutiva_Quantux.html")
    if os.path.exists(f):
        return FileResponse(f, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Presentación no encontrada"}

@app.get("/api")
def api_status():
    return {
        "system": "HealthDesk Quantux",
        "organization": "Quantux Salud",
        "status": "ONLINE",
        "version": "2.5.0",
        "release": "ITIL Tiered Support & Multi-Helpdesk Edition (N1/N2/N3)",
        "cockpit_url": "/cockpit",
        "scrumban_url": "/scrumban",
        "presentacion_url": "/presentacion",
        "docs_url": "/docs"
    }


