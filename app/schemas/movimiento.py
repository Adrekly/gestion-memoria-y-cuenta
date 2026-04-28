"""
Schemas Pydantic para la colección de Movimientos.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoMovimiento(str, Enum):
    """Tipos de movimiento de bienes."""
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    TRASLADO = "TRASLADO"
    REASIGNACION = "REASIGNACION"


class MovimientoCreate(BaseModel):
    """Schema para registrar un nuevo movimiento."""
    codigo_inventario: str = Field(..., description="Código de inventario del bien (ej: UNEG-ATL-...)")
    tipo: TipoMovimiento
    fecha: datetime = Field(default_factory=datetime.utcnow)
    sede_origen: Optional[str] = Field(None, min_length=2, max_length=5)
    sede_destino: Optional[str] = Field(None, min_length=2, max_length=5)
    motivo: str = Field(..., min_length=5, max_length=500)
    autorizado_por: str = Field(..., min_length=3, max_length=150)
    documento_soporte: Optional[str] = Field(None, max_length=100, description="Número de oficio/acta")


class MovimientoResponse(BaseModel):
    """Schema de respuesta para un movimiento."""
    id: str = Field(..., alias="_id")
    bien_id: str
    tipo: TipoMovimiento
    fecha: datetime
    sede_origen: Optional[str] = None
    sede_destino: Optional[str] = None
    motivo: str
    autorizado_por: str
    documento_soporte: Optional[str] = None
    # Datos del bien (join virtual)
    bien_descripcion: Optional[str] = None
    bien_codigo_inventario: Optional[str] = None

    class Config:
        populate_by_name = True


class MovimientoListResponse(BaseModel):
    """Listado paginado de movimientos."""
    total: int
    pagina: int
    por_pagina: int
    movimientos: list[MovimientoResponse]
