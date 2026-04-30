"""
Router de Movimientos — Registro y consulta de movimientos de bienes.
"""
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.schemas.movimiento import (
    MovimientoCreate, MovimientoResponse, MovimientoListResponse, TipoMovimiento,
)
from app.services.audit_service import registrar_auditoria

router = APIRouter()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "bien_id" in doc and isinstance(doc["bien_id"], ObjectId):
        doc["bien_id"] = str(doc["bien_id"])
    return doc


@router.post("", response_model=MovimientoResponse, status_code=201)
async def registrar_movimiento(mov: MovimientoCreate):
    """Registrar un nuevo movimiento de bien."""
    db = get_database()

    # Verificar que el bien existe
    bien = await db.bienes.find_one({"codigo_inventario": mov.codigo_inventario})

    if not bien:
        raise HTTPException(status_code=404, detail=f"Bien con código {mov.codigo_inventario} no encontrado")

    # Verificar sedes si es traslado
    if mov.tipo == TipoMovimiento.TRASLADO:
        if not mov.sede_destino:
            raise HTTPException(status_code=400, detail="Se requiere sede_destino para traslados")
        sede_dest = await db.sedes.find_one({"codigo": mov.sede_destino, "activa": True})
        if not sede_dest:
            raise HTTPException(status_code=400, detail=f"Sede destino '{mov.sede_destino}' no encontrada")

    doc = {
        "bien_id": bien["_id"],
        "tipo": mov.tipo.value,
        "fecha": mov.fecha,
        "sede_origen": mov.sede_origen or bien["sede"]["codigo"],
        "sede_destino": mov.sede_destino,
        "motivo": mov.motivo,
        "autorizado_por": mov.autorizado_por,
        "documento_soporte": mov.documento_soporte,
    }

    result = await db.movimientos.insert_one(doc)
    doc["_id"] = result.inserted_id

    # Si es traslado, actualizar la sede del bien
    if mov.tipo == TipoMovimiento.TRASLADO and mov.sede_destino:
        sede_dest = await db.sedes.find_one({"codigo": mov.sede_destino})
        await db.bienes.update_one(
            {"_id": bien["_id"]},
            {"$set": {
                "sede": {"codigo": sede_dest["codigo"], "nombre": sede_dest["nombre"]},
                "updated_at": datetime.utcnow(),
            }}
        )

    # Agregar datos del bien para la respuesta
    doc["bien_descripcion"] = bien.get("descripcion")
    doc["bien_codigo_inventario"] = bien.get("codigo_inventario")

    await registrar_auditoria(
        accion="MOVIMIENTO",
        coleccion="movimientos",
        documento_id=bien.get("codigo_inventario", str(doc["_id"])),
        usuario=mov.autorizado_por,
        detalles={
            "tipo": mov.tipo.value,
            "bien": bien.get("descripcion"),
            "sede_origen": doc["sede_origen"],
            "sede_destino": mov.sede_destino,
            "motivo": mov.motivo,
        },
    )

    return _serialize(doc)


@router.get("", response_model=MovimientoListResponse)
async def listar_movimientos(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    tipo: TipoMovimiento | None = Query(None),
    bien_id: str | None = Query(None),
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
):
    """Listar movimientos con filtros y paginación."""
    db = get_database()
    filtro = {}

    if tipo:
        filtro["tipo"] = tipo.value
    if bien_id:
        try:
            filtro["bien_id"] = ObjectId(bien_id)
        except Exception:
            raise HTTPException(status_code=400, detail="bien_id inválido")
    if fecha_desde or fecha_hasta:
        filtro["fecha"] = {}
        if fecha_desde:
            filtro["fecha"]["$gte"] = fecha_desde
        if fecha_hasta:
            filtro["fecha"]["$lte"] = fecha_hasta

    total = await db.movimientos.count_documents(filtro)
    skip = (pagina - 1) * por_pagina

    cursor = db.movimientos.find(filtro).sort("fecha", -1).skip(skip).limit(por_pagina)
    movimientos = []
    async for doc in cursor:
        doc = _serialize(doc)
        # Enriquecer con datos del bien
        try:
            bien = await db.bienes.find_one({"_id": ObjectId(doc["bien_id"])})
            if bien:
                doc["bien_descripcion"] = bien.get("descripcion")
                doc["bien_codigo_inventario"] = bien.get("codigo_inventario")
        except Exception:
            pass
        movimientos.append(doc)

    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "movimientos": movimientos,
    }
