"""
Router de Reportes — Generación de formularios BM-1 a BM-4.
Genera PDFs descargables con datos del inventario.
"""
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from datetime import datetime
from io import BytesIO

from app.database import get_database
from app.services.reporte_service import generar_bm1, generar_bm2, generar_bm3, generar_bm4

router = APIRouter()


@router.get("/bm1")
async def reporte_bm1(
    sede: str | None = Query(None, description="Filtrar por código de sede"),
):
    """
    BM-1: Inventario de Bienes.
    Genera un PDF con el inventario actual de la UNEG.
    """
    db = get_database()
    pdf_buffer = await generar_bm1(db, sede=sede)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=BM-1_Inventario_Bienes.pdf"},
    )


@router.get("/bm2")
async def reporte_bm2(
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
    sede: str | None = Query(None),
):
    """
    BM-2: Movimiento de Bienes.
    Genera un PDF con los movimientos del período.
    """
    db = get_database()
    pdf_buffer = await generar_bm2(db, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta, sede=sede)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=BM-2_Movimiento_Bienes.pdf"},
    )


@router.get("/bm3")
async def reporte_bm3(sede: str | None = Query(None)):
    """
    BM-3: Relación de Bienes Faltantes.
    Genera un PDF con los bienes en estado FALTANTE.
    """
    db = get_database()
    pdf_buffer = await generar_bm3(db, sede=sede)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=BM-3_Bienes_Faltantes.pdf"},
    )


@router.get("/bm4")
async def reporte_bm4(
    fecha_desde: datetime | None = Query(None),
    fecha_hasta: datetime | None = Query(None),
):
    """
    BM-4: Resumen del Movimiento.
    Genera el resumen para la Memoria y Cuenta.
    """
    db = get_database()
    pdf_buffer = await generar_bm4(db, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=BM-4_Resumen_Memoria_Cuenta.pdf"},
    )
