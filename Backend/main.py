# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import Base, engine
from routes.usuarios_controller import router as auth_router, router_compat as usuarios_compat_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la app FastAPI
app = FastAPI(title="SN-52 Backend")

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto si tu frontend usa otro dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta para archivos estáticos (por ejemplo, imágenes o adjuntos)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configurar carpeta de plantillas HTML
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(auth_router)           # Rutas /auth/...
app.include_router(usuarios_compat_router)  # Rutas /usuarios/... (compatibilidad con correos antiguos)

# Ruta raíz de prueba
@app.get("/")
def read_root():
    return {"mensaje": "Backend SN-52 corriendo correctamente 🚀"}
