"""
Router de Bienes — CRUD completo con validación SUDEBIP.
"""
from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from datetime import datetime

from app.database import get_database
from app.schemas.bien import (
    BienCreate, BienUpdate, BienCambioEstado,
    BienResponse, BienListResponse, EstadisticasBienesResponse,
    EstadoBien,
)
from app.services.audit_service import registrar_auditoria

router = APIRouter()


def _serialize_bien(doc: dict) -> dict:
    """Convierte un documento MongoDB a formato serializable."""
    doc["_id"] = str(doc["_id"])
    return doc


async def _generar_codigo_inventario(db, sede_codigo: str, grupo: str) -> str:
    """Genera un código de inventario único: UNEG-{SEDE}-{GRUPO}-{SEQ}."""
    # Contar bienes existentes en esa sede+grupo para generar secuencia
    prefix = f"UNEG-{sede_codigo}-{grupo}"
    count = await db.bienes.count_documents({
        "codigo_inventario": {"$regex": f"^{prefix}"}
    })
    seq = str(count + 1).zfill(5)
    return f"{prefix}-{seq}"


@router.post("", status_code=201)
async def crear_bien(bien: BienCreate):
    """
    Registrar un nuevo bien con validación SUDEBIP automática.
    El código de inventario se genera automáticamente.
    """
    db = get_database()

    # Verificar que el código SUDEBIP existe en el clasificador
    clasificador = await db.clasificador_sudebip.find_one({"codigo": bien.codigo_sudebip})
    if not clasificador:
        raise HTTPException(
            status_code=400,
            detail=f"Código SUDEBIP '{bien.codigo_sudebip}' no encontrado en el clasificador. "
                   "Use GET /api/clasificador/buscar para encontrar el código correcto."
        )

    # Verificar que la sede existe
    sede = await db.sedes.find_one({"codigo": bien.sede_codigo, "activa": True})
    if not sede:
        raise HTTPException(
            status_code=400,
            detail=f"Sede '{bien.sede_codigo}' no encontrada o no está activa."
        )

    # Verificar serial duplicado (si se proporcionó)
    if bien.serial:
        existente = await db.bienes.find_one({"serial": bien.serial})
        if existente:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un bien con serial '{bien.serial}' "
                       f"(código: {existente.get('codigo_inventario', 'N/A')})"
            )

    # Generar código de inventario
    grupo_codigo = bien.codigo_sudebip.split(".")[1]  # Extraer subgrupo
    codigo_inventario = await _generar_codigo_inventario(db, bien.sede_codigo, grupo_codigo)

    # Construir documento
    doc = {
        "codigo_inventario": codigo_inventario,
        "codigo_sudebip": bien.codigo_sudebip,
        "grupo_sudebip": bien.grupo_sudebip,
        "descripcion": bien.descripcion,
        "marca": bien.marca,
        "modelo": bien.modelo,
        "serial": bien.serial,
        "valor_adquisicion": bien.valor_adquisicion,
        "fecha_adquisicion": bien.fecha_adquisicion,
        "estado": EstadoBien.EN_USO.value,
        "condicion": bien.condicion.value,
        "sede": {"codigo": sede["codigo"], "nombre": sede["nombre"]},
        "ubicacion_especifica": bien.ubicacion_especifica,
        "responsable": bien.responsable,
        "cedula_responsable": bien.cedula_responsable,
        "departamento": bien.departamento,
        "observaciones": bien.observaciones,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await db.bienes.insert_one(doc)
    doc["_id"] = result.inserted_id

    await registrar_auditoria(
        accion="CREAR",
        coleccion="bienes",
        documento_id=doc["codigo_inventario"],
        usuario=bien.responsable,
        detalles={"descripcion": bien.descripcion, "sede": sede["nombre"], "valor": bien.valor_adquisicion},
    )

    return _serialize_bien(doc)


@router.get("")
async def listar_bienes(
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    sede: str | None = Query(None, description="Filtrar por código de sede"),
    estado: EstadoBien | None = Query(None, description="Filtrar por estado"),
    grupo_sudebip: str | None = Query(None, description="Filtrar por grupo SUDEBIP"),
    busqueda: str | None = Query(None, description="Búsqueda por descripción"),
):
    """Listar bienes con filtros y paginación."""
    db = get_database()
    filtro = {}

    if sede:
        filtro["sede.codigo"] = sede
    if estado:
        filtro["estado"] = estado.value
    if grupo_sudebip:
        filtro["codigo_sudebip"] = {"$regex": f"^{grupo_sudebip}"}
    if busqueda:
        filtro["descripcion"] = {"$regex": busqueda, "$options": "i"}

    total = await db.bienes.count_documents(filtro)
    skip = (pagina - 1) * por_pagina

    cursor = db.bienes.find(filtro).sort("created_at", -1).skip(skip).limit(por_pagina)
    bienes = [_serialize_bien(doc) async for doc in cursor]

    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "bienes": bienes,
    }


@router.get("/buscar-codigo")
async def buscar_bienes_por_codigo(
    q: str = Query(..., min_length=2, description="Búsqueda por código de inventario o descripción"),
):
    """
    Busca bienes por código de inventario o descripción.
    Retorna hasta 10 resultados ligeros para autocompletado.
    """
    db = get_database()
    filtro = {
        "$or": [
            {"codigo_inventario": {"$regex": q, "$options": "i"}},
            {"descripcion": {"$regex": q, "$options": "i"}},
        ],
        "estado": {"$ne": "DESINCORPORADO"},
    }

    cursor = db.bienes.find(filtro, {
        "codigo_inventario": 1, "descripcion": 1, "sede": 1, "estado": 1,
    }).limit(10)

    resultados = []
    async for doc in cursor:
        resultados.append({
            "codigo_inventario": doc["codigo_inventario"],
            "descripcion": doc["descripcion"],
            "sede": doc.get("sede", {}).get("nombre", ""),
            "estado": doc.get("estado", ""),
        })

    return resultados


@router.get("/estadisticas")
async def obtener_estadisticas():
    """Obtener estadísticas resumidas del inventario."""
    db = get_database()

    total = await db.bienes.count_documents({})

    # Por estado
    pipeline_estado = [
        {"$group": {"_id": "$estado", "count": {"$sum": 1}}}
    ]
    por_estado = {}
    async for doc in db.bienes.aggregate(pipeline_estado):
        por_estado[doc["_id"]] = doc["count"]

    # Por sede
    pipeline_sede = [
        {"$group": {"_id": "$sede.codigo", "count": {"$sum": 1}}}
    ]
    por_sede = {}
    async for doc in db.bienes.aggregate(pipeline_sede):
        por_sede[doc["_id"]] = doc["count"]

    # Por grupo SUDEBIP (primer nivel)
    pipeline_grupo = [
        {"$group": {"_id": "$grupo_sudebip", "count": {"$sum": 1}}}
    ]
    por_grupo = {}
    async for doc in db.bienes.aggregate(pipeline_grupo):
        por_grupo[doc["_id"]] = doc["count"]

    # Valor total
    pipeline_valor = [
        {"$group": {"_id": None, "total": {"$sum": "$valor_adquisicion"}}}
    ]
    valor_total = 0.0
    async for doc in db.bienes.aggregate(pipeline_valor):
        valor_total = doc["total"]

    # Por condición
    pipeline_condicion = [
        {"$group": {"_id": "$condicion", "count": {"$sum": 1}}}
    ]
    por_condicion = {}
    async for doc in db.bienes.aggregate(pipeline_condicion):
        por_condicion[doc["_id"]] = doc["count"]

    # Desincorporaciones pendientes
    desinc_pendientes = await db.desincorporaciones.count_documents({
        "estado_proceso": {"$in": ["SOLICITADA", "EN_REVISION"]}
    })

    # Últimos 5 movimientos
    ultimos_movimientos = []
    cursor_mov = db.movimientos.find().sort("fecha", -1).limit(5)
    async for doc in cursor_mov:
        bien = await db.bienes.find_one({"_id": doc.get("bien_id")})
        ultimos_movimientos.append({
            "tipo": doc.get("tipo"),
            "bien": bien.get("codigo_inventario", "N/A") if bien else "N/A",
            "descripcion": bien.get("descripcion", "") if bien else "",
            "fecha": doc.get("fecha").isoformat() if doc.get("fecha") else None,
            "autorizado_por": doc.get("autorizado_por"),
        })

    return {
        "total_bienes": total,
        "por_estado": por_estado,
        "por_sede": por_sede,
        "por_grupo_sudebip": por_grupo,
        "valor_total": valor_total,
        "por_condicion": por_condicion,
        "desincorporaciones_pendientes": desinc_pendientes,
        "ultimos_movimientos": ultimos_movimientos,
    }


@router.get("/{bien_id}")
async def obtener_bien(bien_id: str):
    """Obtener detalle de un bien por su ID."""
    db = get_database()
    try:
        if ObjectId.is_valid(bien_id):
            doc = await db.bienes.find_one({"_id": ObjectId(bien_id)})
        else:
            doc = await db.bienes.find_one({"codigo_inventario": bien_id})
    except Exception:
        raise HTTPException(status_code=400, detail="ID o código inválido")

    if not doc:
        raise HTTPException(status_code=404, detail="Bien no encontrado")
    return _serialize_bien(doc)


@router.get("/{bien_id}/historial")
async def obtener_historial_bien(bien_id: str):
    """Obtener el historial completo de un bien (auditoría, movimientos, desincorporaciones)."""
    db = get_database()
    try:
        if ObjectId.is_valid(bien_id):
            bien = await db.bienes.find_one({"_id": ObjectId(bien_id)})
        else:
            bien = await db.bienes.find_one({"codigo_inventario": bien_id})
    except Exception:
        raise HTTPException(status_code=400, detail="ID o código inválido")

    if not bien:
        raise HTTPException(status_code=404, detail="Bien no encontrado")

    codigo = bien.get("codigo_inventario")

    # 1. Obtener logs de auditoría
    logs_cursor = db.audit_log.find({"documento_id": {"$in": [codigo, bien_id]}}).sort("fecha", -1)
    logs = []
    async for log in logs_cursor:
        log["_id"] = str(log["_id"])
        logs.append(log)

    return {
        "bien": _serialize_bien(bien),
        "historial": logs
    }


@router.put("/{bien_id}")
async def actualizar_bien(bien_id: str, datos: BienUpdate):
    """Actualizar campos de un bien existente."""
    db = get_database()

    # Obtener estado anterior para el audit log
    try:
        bien_anterior = await db.bienes.find_one({"_id": ObjectId(bien_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    if not bien_anterior:
        raise HTTPException(status_code=404, detail="Bien no encontrado")

    update_data = {k: v for k, v in datos.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    update_data["updated_at"] = datetime.utcnow()

    # Registrar cambios campo a campo
    cambios = {}
    for campo, nuevo_valor in update_data.items():
        if campo == "updated_at":
            continue
        anterior = bien_anterior.get(campo)
        if anterior != nuevo_valor:
            cambios[campo] = {"anterior": str(anterior), "nuevo": str(nuevo_valor)}

    result = await db.bienes.find_one_and_update(
        {"_id": ObjectId(bien_id)},
        {"$set": update_data},
        return_document=True,
    )

    if cambios:
        await registrar_auditoria(
            accion="ACTUALIZAR",
            coleccion="bienes",
            documento_id=bien_anterior.get("codigo_inventario", bien_id),
            detalles={"campos_modificados": list(cambios.keys())},
            cambios=cambios,
        )

    return _serialize_bien(result)


@router.patch("/{bien_id}/estado")
async def cambiar_estado_bien(bien_id: str, cambio: BienCambioEstado):
    """
    Cambiar el estado de un bien.
    Requiere un motivo obligatorio para trazabilidad.
    """
    db = get_database()

    try:
        bien = await db.bienes.find_one({"_id": ObjectId(bien_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not bien:
        raise HTTPException(status_code=404, detail="Bien no encontrado")

    # Validar transiciones de estado
    estado_actual = bien["estado"]
    if estado_actual == EstadoBien.DESINCORPORADO.value:
        raise HTTPException(
            status_code=400,
            detail="Un bien desincorporado no puede cambiar de estado. Use el módulo de desincorporaciones."
        )

    result = await db.bienes.find_one_and_update(
        {"_id": ObjectId(bien_id)},
        {"$set": {
            "estado": cambio.estado.value,
            "updated_at": datetime.utcnow(),
        }},
        return_document=True,
    )

    await registrar_auditoria(
        accion="CAMBIO_ESTADO",
        coleccion="bienes",
        documento_id=bien.get("codigo_inventario", bien_id),
        detalles={"motivo": cambio.motivo},
        cambios={"estado": {"anterior": estado_actual, "nuevo": cambio.estado.value}},
    )

    return _serialize_bien(result)
