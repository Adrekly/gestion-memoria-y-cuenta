"""
Schemas Pydantic para la colección de Desincorporaciones.
Incluye validación para el flujo legal de baja de bienes.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MotivoDesincorporacion(str, Enum):
    """Causales legales de desincorporación según la Ley de Bienes Públicos."""
    OBSOLESCENCIA = "OBSOLESCENCIA"
    INSERVIBILIDAD = "INSERVIBILIDAD"
    HURTO = "HURTO"
    ROBO = "ROBO"
    SINIESTRO = "SINIESTRO"
    DONACION = "DONACION"
    OTRO = "OTRO"


class EstadoProceso(str, Enum):
    """Estados del proceso de desincorporación."""
    SOLICITADA = "SOLICITADA"
    EN_REVISION = "EN_REVISION"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"
    EJECUTADA = "EJECUTADA"


class ValidacionIA(BaseModel):
    """Resultado de la validación de IA sobre la justificación."""
    cumple_criterios: bool
    observaciones: str
    fecha_validacion: datetime = Field(default_factory=datetime.utcnow)


class DesincorporacionCreate(BaseModel):
    """Schema para solicitar una desincorporación."""
    codigo_inventario: str = Field(..., description="Código de inventario del bien (ej: UNEG-ATL-...)")
    motivo: MotivoDesincorporacion
    justificacion_tecnica: str = Field(
        ..., 
        min_length=20, 
        max_length=2000,
        description="Justificación técnica detallada (mínimo 20 caracteres)"
    )
    solicitado_por: str = Field(..., min_length=3, max_length=150)


class DesincorporacionCambioEstado(BaseModel):
    """Schema para aprobar o rechazar una desincorporación."""
    estado: EstadoProceso = Field(
        ..., 
        description="Solo se permite APROBADA o RECHAZADA"
    )
    aprobado_por: str = Field(..., min_length=3, max_length=150)
    observaciones: Optional[str] = Field(None, max_length=1000)


class DesincorporacionResponse(BaseModel):
    """Schema de respuesta para una desincorporación."""
    id: str = Field(..., alias="_id")
    bien_id: str
    motivo: MotivoDesincorporacion
    justificacion_tecnica: str
    estado_proceso: EstadoProceso
    solicitado_por: str
    fecha_solicitud: datetime
    validacion_ia: Optional[ValidacionIA] = None
    aprobado_por: Optional[str] = None
    fecha_aprobacion: Optional[datetime] = None
    observaciones: Optional[str] = None
    # Datos del bien (join virtual)
    bien_descripcion: Optional[str] = None
    bien_codigo_inventario: Optional[str] = None

    class Config:
        populate_by_name = True


class DesincorporacionListResponse(BaseModel):
    """Listado paginado de desincorporaciones."""
    total: int
    pagina: int
    por_pagina: int
    desincorporaciones: list[DesincorporacionResponse]
