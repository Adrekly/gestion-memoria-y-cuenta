"""
API UNEG - Sistema de Gestión de Memoria y Cuenta
Punto de entrada principal de la aplicación FastAPI.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import connect_db, disconnect_db, get_database
from app.seeds.clasificador_seed import seed_clasificador
from app.seeds.sedes_seed import seed_sedes

# Importar routers
from app.routers import bienes, movimientos, desincorporaciones, sedes, clasificador, chat, reportes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación (startup/shutdown)."""
    # --- Startup ---
    await connect_db()
    # Ejecutar seeds (solo inserta si las colecciones están vacías)
    db = get_database()
    await seed_clasificador(db)
    await seed_sedes(db)
    print("[OK] API UNEG lista")
    yield
    # --- Shutdown ---
    await disconnect_db()


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "API para la gestión integral de activos de la UNEG, "
        "alineada con la Ley Orgánica de Bienes Públicos y la SUDEBIP."
    ),
    lifespan=lifespan,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registrar routers ---
app.include_router(bienes.router, prefix="/api/bienes", tags=["Bienes"])
app.include_router(movimientos.router, prefix="/api/movimientos", tags=["Movimientos"])
app.include_router(desincorporaciones.router, prefix="/api/desincorporaciones", tags=["Desincorporaciones"])
app.include_router(sedes.router, prefix="/api/sedes", tags=["Sedes"])
app.include_router(clasificador.router, prefix="/api/clasificador", tags=["Clasificador SUDEBIP"])
app.include_router(chat.router, prefix="/api/chat", tags=["Asistente IA"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes BM"])


@app.get("/", tags=["Health"])
async def root():
    """Endpoint de verificación de salud."""
    return {
        "sistema": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "estado": "operativo",
    }
