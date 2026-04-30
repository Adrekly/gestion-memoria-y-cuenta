"""
Conexión asíncrona a MongoDB usando Motor.
Gestiona la conexión, inicialización de índices y acceso a colecciones.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import get_settings

# Instancias globales (se inicializan en startup)
_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def get_database() -> AsyncIOMotorDatabase:
    """Retorna la instancia de la base de datos."""
    if _db is None:
        raise RuntimeError("La base de datos no ha sido inicializada. Llama a connect_db() primero.")
    return _db


async def connect_db() -> None:
    """Establece la conexión con MongoDB y crea los índices necesarios."""
    global _client, _db
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.MONGO_URL)
    _db = _client[settings.MONGO_DB_NAME]

    # Verificar conexión
    await _client.admin.command("ping")
    print(f"[OK] Conectado a MongoDB: {settings.MONGO_DB_NAME}")

    # Crear índices
    await _create_indexes()


async def _create_indexes() -> None:
    """Crea los índices recomendados para rendimiento y unicidad."""
    db = get_database()

    # Colección: bienes
    await db.bienes.create_index("codigo_inventario", unique=True)
    await db.bienes.create_index("codigo_sudebip")
    await db.bienes.create_index("estado")
    await db.bienes.create_index("sede.codigo")
    await db.bienes.create_index("departamento")
    await db.bienes.create_index(
        "serial",
        unique=True,
        partialFilterExpression={"serial": {"$type": "string", "$gt": ""}}
    )  # Permite seriales nulos o vacíos sin chocar
    await db.bienes.create_index([("sede.codigo", 1), ("estado", 1)])  # Compuesto para filtros
    await db.bienes.create_index(
        [("descripcion", "text"), ("codigo_inventario", "text")],
        default_language="spanish",
        name="idx_bienes_text"
    )

    # Colección: movimientos
    await db.movimientos.create_index("bien_id")
    await db.movimientos.create_index("fecha")
    await db.movimientos.create_index("tipo")

    # Colección: desincorporaciones
    await db.desincorporaciones.create_index("bien_id")
    await db.desincorporaciones.create_index("estado_proceso")

    # Colección: clasificador_sudebip
    await db.clasificador_sudebip.create_index("codigo", unique=True)
    await db.clasificador_sudebip.create_index(
        [("descripcion", "text"), ("palabras_clave", "text")],
        default_language="spanish",
        name="idx_clasificador_text"
    )

    # Colección: sedes
    await db.sedes.create_index("codigo", unique=True)

    # Colección: audit_log
    await db.audit_log.create_index("coleccion")
    await db.audit_log.create_index("documento_id")
    await db.audit_log.create_index("accion")
    await db.audit_log.create_index("fecha")  # Podría configurarse un TTL si se desea

    print("[OK] Indices de MongoDB creados/verificados")


async def disconnect_db() -> None:
    """Cierra la conexión con MongoDB."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("[OK] Desconectado de MongoDB")
