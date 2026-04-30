"""
Servicio de Auditoría — Registra cada acción importante del sistema.
Proporciona trazabilidad completa para la Contraloría.
"""
from datetime import datetime
from app.database import get_database


async def registrar_auditoria(
    accion: str,
    coleccion: str,
    documento_id: str,
    usuario: str = "Sistema",
    detalles: dict | None = None,
    cambios: dict | None = None,
) -> None:
    """
    Registra una entrada en el log de auditoría.

    Args:
        accion: Tipo de acción (CREAR, ACTUALIZAR, CAMBIO_ESTADO, DESINCORPORAR, MOVIMIENTO)
        coleccion: Nombre de la colección afectada (bienes, movimientos, desincorporaciones)
        documento_id: ID o código del documento afectado
        usuario: Nombre del usuario que realizó la acción
        detalles: Información adicional sobre la acción
        cambios: Diccionario con {campo: {anterior: X, nuevo: Y}}
    """
    db = get_database()

    entry = {
        "accion": accion,
        "coleccion": coleccion,
        "documento_id": str(documento_id),
        "usuario": usuario,
        "fecha": datetime.utcnow(),
        "detalles": detalles or {},
        "cambios": cambios or {},
    }

    await db.audit_log.insert_one(entry)
