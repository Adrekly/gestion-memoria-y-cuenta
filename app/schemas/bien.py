"""
Schemas Pydantic para la colección de Bienes.
Validación estricta alineada con la codificación SUDEBIP.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId


# --- Enums ---

class EstadoBien(str, Enum):
    """Estados válidos de un bien según la normativa SUDEBIP."""
    EN_USO = "EN_USO"
    EN_DESUSO = "EN_DESUSO"
    INSERVIBLE = "INSERVIBLE"
    EN_REPARACION = "EN_REPARACION"
    DESINCORPORADO = "DESINCORPORADO"
    FALTANTE = "FALTANTE"


class CondicionBien(str, Enum):
    """Condición física del bien."""
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    MALO = "MALO"


# --- Sub-schemas ---

class SedeRef(BaseModel):
    """Referencia embebida a una sede."""
    codigo: str = Field(..., min_length=2, max_length=5, description="Código de la sede (ej: ATL)")
    nombre: str = Field(..., min_length=3, description="Nombre de la sede")


# --- Schemas de entrada ---

class BienCreate(BaseModel):
    """Schema para registrar un nuevo bien."""
    codigo_sudebip: str = Field(
        ..., 
        pattern=r"^\d+\.\d{2}\.\d{2}\.\d{2}$",
        description="Código del Clasificador SUDEBIP (ej: 1.02.01.01)"
    )
    grupo_sudebip: str = Field(..., min_length=3, description="Descripción del grupo SUDEBIP")
    descripcion: str = Field(..., min_length=5, max_length=500, description="Descripción del bien")
    marca: Optional[str] = Field(None, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    serial: Optional[str] = Field(None, max_length=100)
    valor_adquisicion: float = Field(..., ge=0, description="Valor en USD o Bs")
    fecha_adquisicion: datetime = Field(..., description="Fecha de compra/incorporación")
    condicion: CondicionBien = Field(default=CondicionBien.BUENO)
    sede_codigo: str = Field(..., min_length=2, max_length=5, description="Código de la sede")
    ubicacion_especifica: Optional[str] = Field(None, max_length=200, description="Edificio, piso, oficina")
    responsable: str = Field(..., min_length=3, max_length=150, description="Nombre del custodio")
    cedula_responsable: str = Field(
        ..., 
        pattern=r"^[VEJPvejp]-?\d{6,10}$",
        description="Cédula del custodio (ej: V-12345678)"
    )
    departamento: str = Field(..., min_length=3, max_length=150)
    observaciones: Optional[str] = Field(None, max_length=1000)

    @field_validator("cedula_responsable")
    @classmethod
    def normalizar_cedula(cls, v: str) -> str:
        """Normaliza el formato de cédula: V-12345678"""
        v = v.upper().replace(" ", "")
        if "-" not in v:
            v = v[0] + "-" + v[1:]
        return v


class BienUpdate(BaseModel):
    """Schema para actualizar un bien existente (campos opcionales)."""
    descripcion: Optional[str] = Field(None, min_length=5, max_length=500)
    marca: Optional[str] = Field(None, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    serial: Optional[str] = Field(None, max_length=100)
    valor_adquisicion: Optional[float] = Field(None, ge=0)
    condicion: Optional[CondicionBien] = None
    ubicacion_especifica: Optional[str] = Field(None, max_length=200)
    responsable: Optional[str] = Field(None, min_length=3, max_length=150)
    cedula_responsable: Optional[str] = Field(None, pattern=r"^[VEJPvejp]-?\d{6,10}$")
    departamento: Optional[str] = Field(None, min_length=3, max_length=150)
    observaciones: Optional[str] = Field(None, max_length=1000)


class BienCambioEstado(BaseModel):
    """Schema para cambiar el estado de un bien."""
    estado: EstadoBien
    motivo: str = Field(..., min_length=10, max_length=500, description="Motivo del cambio de estado")


# --- Schemas de salida ---

class BienResponse(BaseModel):
    """Schema de respuesta para un bien."""
    id: str = Field(..., alias="_id")
    codigo_inventario: str
    codigo_sudebip: str
    grupo_sudebip: str
    descripcion: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serial: Optional[str] = None
    valor_adquisicion: float
    fecha_adquisicion: datetime
    estado: EstadoBien
    condicion: CondicionBien
    sede: SedeRef
    ubicacion_especifica: Optional[str] = None
    responsable: str
    cedula_responsable: str
    departamento: str
    observaciones: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class BienListResponse(BaseModel):
    """Schema de respuesta para listado paginado de bienes."""
    total: int
    pagina: int
    por_pagina: int
    bienes: list[BienResponse]


class EstadisticasBienesResponse(BaseModel):
    """Estadísticas resumidas del inventario."""
    total_bienes: int
    por_estado: dict[str, int]
    por_sede: dict[str, int]
    por_grupo_sudebip: dict[str, int]
    valor_total: float
