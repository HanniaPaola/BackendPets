from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import engine, Base
import models  # importa todos los modelos para que SQLAlchemy los registre

from routers import auth, pets, tasks

# Crea todas las tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc UI
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,     # oculta schemas por defecto
        "docExpansion": "list",             # colapsa endpoints por defecto
        "persistAuthorization": True,       # mantiene el token al recargar
    }
)

# CORS — ajusta origins en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(pets.router)
app.include_router(tasks.router)


@app.get("/", tags=["🏠 Home"], summary="Bienvenida")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running 🚀"
    }


@app.get("/health", tags=["🏠 Home"], summary="Health check")
def health():
    return {"status": "ok"}
