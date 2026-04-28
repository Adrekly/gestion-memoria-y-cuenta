"""
Router del Clasificador SUDEBIP — Consulta del catálogo de codificación.
"""
from fastapi import APIRouter, HTTPException, Query

from app.database import get_database
from app.schemas.clasificador import ClasificadorResponse, ClasificadorBusquedaResponse

router = APIRouter()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/buscar", response_model=ClasificadorBusquedaResponse)
async def buscar_clasificador(
    q: str = Query(..., min_length=2, description="Término de búsqueda (ej: 'escritorio', 'computadora')"),
):
    """
    Buscar en el Clasificador Único de Bienes de la SUDEBIP.
    Busca por descripción y palabras clave.
    """
    db = get_database()

    # Intentar búsqueda full-text primero
    resultados = []
    try:
        cursor = db.clasificador_sudebip.find(
            {"$text": {"$search": q}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(10)
        resultados = [_serialize(doc) async for doc in cursor]
        # Remover el campo score de los resultados
        for r in resultados:
            r.pop("score", None)
    except Exception:
        pass

    # Si no hay resultados con text search, usar regex
    if not resultados:
        cursor = db.clasificador_sudebip.find({
            "$or": [
                {"descripcion": {"$regex": q, "$options": "i"}},
                {"palabras_clave": {"$regex": q, "$options": "i"}},
                {"descripcion_subgrupo": {"$regex": q, "$options": "i"}},
            ]
        }).limit(10)
        resultados = [_serialize(doc) async for doc in cursor]

    return {"total": len(resultados), "resultados": resultados}


@router.get("/{codigo}", response_model=ClasificadorResponse)
async def obtener_codigo(codigo: str):
    """Obtener detalle de un código SUDEBIP específico."""
    db = get_database()
    doc = await db.clasificador_sudebip.find_one({"codigo": codigo})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Código '{codigo}' no encontrado en el clasificador")
    return _serialize(doc)
