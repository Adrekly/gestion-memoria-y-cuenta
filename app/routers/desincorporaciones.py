"""
Router de Desincorporaciones — Flujo de baja de bienes con validación IA.
"""
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.schemas.desincorporacion import (
    DesincorporacionCreate, DesincorporacionCambioEstado,
    DesincorporacionResponse, DesincorporacionListResponse,
    EstadoProceso,
)
from app.schemas.bien import EstadoBien
from app.services.audit_service import registrar_auditoria

router = APIRouter()


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "bien_id" in doc and isinstance(doc["bien_id"], ObjectId):
        doc["bien_id"] = str(doc["bien_id"])
    return doc


@router.post("", response_model=DesincorporacionResponse, status_code=201)
async def solicitar_desincorporacion(data: DesincorporacionCreate):
    """
    Solicitar la desincorporación de un bien.
    La justificación será validada por IA si está disponible.
    """
    db = get_database()

    # Verificar que el bien existe y no está ya desincorporado
    bien = await db.bienes.find_one({"codigo_inventario": data.codigo_inventario})

    if not bien:
        raise HTTPException(status_code=404, detail=f"Bien con código {data.codigo_inventario} no encontrado")

    if bien["estado"] == EstadoBien.DESINCORPORADO.value:
        raise HTTPException(status_code=400, detail="Este bien ya fue desincorporado")

    # Verificar que no existe ya una solicitud activa
    existente = await db.desincorporaciones.find_one({
        "bien_id": bien["_id"],
        "estado_proceso": {"$in": [
            EstadoProceso.SOLICITADA.value,
            EstadoProceso.EN_REVISION.value,
        ]}
    })
    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una solicitud de desincorporación activa para este bien"
        )

    # Validación IA básica (se mejorará con el servicio de IA)
    validacion_ia = {
        "cumple_criterios": len(data.justificacion_tecnica) >= 20,
        "observaciones": "Justificación recibida. Pendiente revisión por supervisor.",
        "fecha_validacion": datetime.utcnow(),
    }

    doc = {
        "bien_id": bien["_id"],
        "motivo": data.motivo.value,
        "justificacion_tecnica": data.justificacion_tecnica,
        "estado_proceso": EstadoProceso.EN_REVISION.value,
        "solicitado_por": data.solicitado_por,
        "fecha_solicitud": datetime.utcnow(),
        "validacion_ia": validacion_ia,
        "aprobado_por": None,
        "fecha_aprobacion": None,
        "observaciones": None,
    }

    result = await db.desincorporaciones.insert_one(doc)
    doc["_id"] = result.inserted_id
    doc["bien_descripcion"] = bien.get("descripcion")
    doc["bien_codigo_inventario"] = bien.get("codigo_inventario")

    await registrar_auditoria(
        accion="DESINCORPORAR",
        coleccion="desincorporaciones",
        documento_id=bien.get("codigo_inventario", str(doc["_id"])),
        usuario=data.solicitado_por,
        detalles={"motivo": data.motivo.value, "bien": bien.get("descripcion")},
    )

    return _serialize(doc)


@router.patch("/{desincorporacion_id}/estado", response_model=DesincorporacionResponse)
async def cambiar_estado_desincorporacion(desincorporacion_id: str, cambio: DesincorporacionCambioEstado):
    """Aprobar o rechazar una solicitud de desincorporación."""
    db = get_database()

    if cambio.estado not in [EstadoProceso.APROBADA, EstadoProceso.RECHAZADA]:
        raise HTTPException(
            status_code=400,
            detail="Solo se permite cambiar a estado APROBADA o RECHAZADA"
        )

    try:
        desinc = await db.desincorporaciones.find_one({"_id": ObjectId(desincorporacion_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not desinc:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if desinc["estado_proceso"] != EstadoProceso.EN_REVISION.value:
        raise HTTPException(
            status_code=400,
            detail=f"Solo se pueden aprobar/rechazar solicitudes EN_REVISION. Estado actual: {desinc['estado_proceso']}"
        )

    update = {
        "estado_proceso": cambio.estado.value,
        "aprobado_por": cambio.aprobado_por,
        "fecha_aprobacion": datetime.utcnow(),
        "observaciones": cambio.observaciones,
    }

    result = await db.desincorporaciones.find_one_and_update(
        {"_id": ObjectId(desincorporacion_id)},
        {"$set": update},
        return_document=True,
    )

    # Si se aprueba, cambiar estado del bien a DESINCORPORADO
    if cambio.estado == EstadoProceso.APROBADA:
        await db.bienes.update_one(
            {"_id": desinc["bien_id"]},
            {"$set": {
                "estado": EstadoBien.DESINCORPORADO.value,
                "updated_at": datetime.utcnow(),
            }}
        )

    # Enriquecer con datos del bien
    bien = await db.bienes.find_one({"_id": desinc["bien_id"]})
    if bien:
        result["bien_descripcion"] = bien.get("descripcion")
        result["bien_codigo_inventario"] = bien.get("codigo_inventario")

    await registrar_auditoria(
        accion=f"DESINCORPORACION_{cambio.estado.value}",
        coleccion="desincorporaciones",
        documento_id=bien.get("codigo_inventario", desincorporacion_id) if bien else desincorporacion_id,
        usuario=cambio.aprobado_por,
        detalles={"observaciones": cambio.observaciones},
        cambios={"estado_proceso": {"anterior": desinc["estado_proceso"], "nuevo": cambio.estado.value}},
    )

    return _serialize(result)


@router.get("", response_model=DesincorporacionListResponse)
async def listar_desincorporaciones(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    estado: EstadoProceso | None = Query(None),
):
    """Listar solicitudes de desincorporación."""
    db = get_database()
    filtro = {}
    if estado:
        filtro["estado_proceso"] = estado.value

    total = await db.desincorporaciones.count_documents(filtro)
    skip = (pagina - 1) * por_pagina

    cursor = db.desincorporaciones.find(filtro).sort("fecha_solicitud", -1).skip(skip).limit(por_pagina)
    items = []
    async for doc in cursor:
        doc = _serialize(doc)
        try:
            bien = await db.bienes.find_one({"_id": ObjectId(doc["bien_id"])})
            if bien:
                doc["bien_descripcion"] = bien.get("descripcion")
                doc["bien_codigo_inventario"] = bien.get("codigo_inventario")
        except Exception:
            pass
        items.append(doc)

    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "desincorporaciones": items,
    }
