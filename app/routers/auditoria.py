"""
Router de Auditoría — Consulta del historial de acciones del sistema.
"""
from fastapi import APIRouter, Query
from datetime import datetime

from app.database import get_database

router = APIRouter()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("")
async def listar_auditoria(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    coleccion: str | None = Query(None, description="Filtrar por colección (bienes, movimientos, desincorporaciones)"),
    accion: str | None = Query(None, description="Filtrar por tipo de acción"),
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
):
    """Listar entradas del log de auditoría."""
    db = get_database()
    filtro = {}

    if coleccion:
        filtro["coleccion"] = coleccion
    if accion:
        filtro["accion"] = accion
    if fecha_desde or fecha_hasta:
        filtro["fecha"] = {}
        if fecha_desde:
            filtro["fecha"]["$gte"] = fecha_desde
        if fecha_hasta:
            filtro["fecha"]["$lte"] = fecha_hasta

    total = await db.audit_log.count_documents(filtro)
    skip = (pagina - 1) * por_pagina

    cursor = db.audit_log.find(filtro).sort("fecha", -1).skip(skip).limit(por_pagina)
    items = [_serialize(doc) async for doc in cursor]

    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "registros": items,
    }
