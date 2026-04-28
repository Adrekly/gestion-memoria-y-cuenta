"""
Router de Sedes — Gestión de sedes de la UNEG.
"""
from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_database
from app.schemas.sede import SedeCreate, SedeUpdate, SedeResponse

router = APIRouter()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("", response_model=list[SedeResponse])
async def listar_sedes():
    """Listar todas las sedes de la UNEG."""
    db = get_database()
    cursor = db.sedes.find().sort("codigo", 1)
    return [_serialize(doc) async for doc in cursor]


@router.post("", response_model=SedeResponse, status_code=201)
async def crear_sede(sede: SedeCreate):
    """Registrar una nueva sede."""
    db = get_database()

    existente = await db.sedes.find_one({"codigo": sede.codigo})
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe una sede con código '{sede.codigo}'")

    doc = sede.model_dump()
    result = await db.sedes.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize(doc)


@router.put("/{sede_id}", response_model=SedeResponse)
async def actualizar_sede(sede_id: str, datos: SedeUpdate):
    """Actualizar una sede existente."""
    db = get_database()
    update_data = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    try:
        result = await db.sedes.find_one_and_update(
            {"_id": ObjectId(sede_id)},
            {"$set": update_data},
            return_document=True,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not result:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return _serialize(result)
