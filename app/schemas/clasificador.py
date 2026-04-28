"""
Schemas Pydantic para el Clasificador Único de Bienes (SUDEBIP).
"""
from pydantic import BaseModel, Field
from typing import Optional


class ClasificadorResponse(BaseModel):
    """Schema de respuesta para un ítem del clasificador."""
    id: str = Field(..., alias="_id")
    codigo: str
    grupo: str
    subgrupo: str
    seccion: str
    categoria: str
    descripcion_grupo: str
    descripcion_subgrupo: str
    descripcion_seccion: Optional[str] = None
    descripcion: str
    palabras_clave: list[str] = []

    class Config:
        populate_by_name = True


class ClasificadorBusquedaResponse(BaseModel):
    """Resultado de búsqueda en el clasificador."""
    total: int
    resultados: list[ClasificadorResponse]
