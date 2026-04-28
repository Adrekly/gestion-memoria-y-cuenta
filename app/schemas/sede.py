"""
Schemas Pydantic para Sedes de la UNEG.
"""
from pydantic import BaseModel, Field
from typing import Optional


class SedeCreate(BaseModel):
    """Schema para registrar una nueva sede."""
    codigo: str = Field(..., min_length=2, max_length=5, description="Código corto (ej: ATL)")
    nombre: str = Field(..., min_length=3, max_length=150, description="Nombre completo")
    ciudad: str = Field(..., min_length=3, max_length=100)
    direccion: Optional[str] = Field(None, max_length=300)
    activa: bool = Field(default=True)


class SedeUpdate(BaseModel):
    """Schema para actualizar una sede."""
    nombre: Optional[str] = Field(None, min_length=3, max_length=150)
    ciudad: Optional[str] = Field(None, min_length=3, max_length=100)
    direccion: Optional[str] = Field(None, max_length=300)
    activa: Optional[bool] = None


class SedeResponse(BaseModel):
    """Schema de respuesta para una sede."""
    id: str = Field(..., alias="_id")
    codigo: str
    nombre: str
    ciudad: str
    direccion: Optional[str] = None
    activa: bool

    class Config:
        populate_by_name = True
