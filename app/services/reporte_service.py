"""
Servicio de generación de reportes BM-1 a BM-4 en PDF.
Usa fpdf2 para generar los formularios oficiales de la SUDEBIP.
"""
from fpdf import FPDF
from io import BytesIO
from datetime import datetime
from typing import Optional


class ReporteBM(FPDF):
    """Clase base para reportes BM con formato institucional."""
    P = (0, 51, 102)
    S = (196, 163, 90)
    D = (33, 37, 41)
    W = (255, 255, 255)

    def __init__(self, titulo_reporte: str, codigo_bm: str):
        super().__init__()
        self._titulo_reporte = titulo_reporte
        self._codigo_bm = codigo_bm

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.P)
        self.cell(0, 5, "UNIVERSIDAD NACIONAL EXPERIMENTAL DE GUAYANA", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.cell(0, 5, "Departamento de Bienes Publicos", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 5, f"Formulario {self._codigo_bm}: {self._titulo_reporte}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.S)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(95, 10, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        self.cell(95, 10, f"Pagina {self.page_no()}/{{nb}}", align="R")

    def tabla_header(self, cols, anchos):
        self.set_font("Helvetica", "B", 7)
        self.set_fill_color(*self.P)
        self.set_text_color(*self.W)
        for i, col in enumerate(cols):
            self.cell(anchos[i], 6, col, border=1, fill=True, align="C")
        self.ln()

    def tabla_row(self, datos, anchos, fill=False):
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*self.D)
        if fill:
            self.set_fill_color(245, 247, 250)
        else:
            self.set_fill_color(*self.W)
        for i, d in enumerate(datos):
            self.cell(anchos[i], 5.5, str(d)[:30], border=1, fill=True)
        self.ln()


def _to_buffer(pdf: FPDF) -> BytesIO:
    """Convierte el PDF a un buffer de bytes."""
    buf = BytesIO()
    buf.write(pdf.output())
    buf.seek(0)
    return buf


async def generar_bm1(db, sede: Optional[str] = None) -> BytesIO:
    """BM-1: Inventario de Bienes - foto actual del inventario."""
    pdf = ReporteBM("Inventario de Bienes Muebles", "BM-1")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page("L")  # Landscape para más columnas

    # Info del reporte
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*ReporteBM.D)
    filtro_texto = f"Sede: {sede}" if sede else "Todas las sedes"
    pdf.cell(0, 5, f"Filtro: {filtro_texto}  |  Fecha de corte: {datetime.now().strftime('%d/%m/%Y')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Tabla
    cols = ["Cod. Inventario", "Cod. SUDEBIP", "Descripcion", "Marca", "Estado", "Condicion", "Sede", "Responsable", "Valor"]
    anchos = [30, 22, 50, 25, 22, 20, 35, 40, 23]
    pdf.tabla_header(cols, anchos)

    filtro = {}
    if sede:
        filtro["sede.codigo"] = sede

    fill = False
    total_valor = 0.0
    count = 0
    async for bien in db.bienes.find(filtro).sort("codigo_inventario", 1):
        if pdf.get_y() > 180:
            pdf.add_page("L")
            pdf.tabla_header(cols, anchos)
        datos = [
            bien.get("codigo_inventario", ""),
            bien.get("codigo_sudebip", ""),
            bien.get("descripcion", ""),
            bien.get("marca", ""),
            bien.get("estado", ""),
            bien.get("condicion", ""),
            bien.get("sede", {}).get("nombre", ""),
            bien.get("responsable", ""),
            f"${bien.get('valor_adquisicion', 0):,.2f}",
        ]
        pdf.tabla_row(datos, anchos, fill)
        fill = not fill
        total_valor += bien.get("valor_adquisicion", 0)
        count += 1

    # Totales
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ReporteBM.P)
    pdf.cell(0, 6, f"Total de bienes: {count}  |  Valor total: ${total_valor:,.2f}", new_x="LMARGIN", new_y="NEXT")

    return _to_buffer(pdf)


async def generar_bm2(db, fecha_desde=None, fecha_hasta=None, sede=None) -> BytesIO:
    """BM-2: Movimiento de Bienes - entradas y salidas del período."""
    pdf = ReporteBM("Movimiento de Bienes", "BM-2")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page("L")

    filtro = {}
    if fecha_desde or fecha_hasta:
        filtro["fecha"] = {}
        if fecha_desde:
            filtro["fecha"]["$gte"] = fecha_desde
        if fecha_hasta:
            filtro["fecha"]["$lte"] = fecha_hasta
    if sede:
        filtro["$or"] = [{"sede_origen": sede}, {"sede_destino": sede}]

    # Info
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*ReporteBM.D)
    desde_txt = fecha_desde.strftime('%d/%m/%Y') if fecha_desde else "Inicio"
    hasta_txt = fecha_hasta.strftime('%d/%m/%Y') if fecha_hasta else "Actual"
    pdf.cell(0, 5, f"Periodo: {desde_txt} - {hasta_txt}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    cols = ["Fecha", "Tipo", "Bien", "Descripcion", "Origen", "Destino", "Motivo", "Autorizado por"]
    anchos = [22, 25, 30, 45, 25, 25, 45, 50]
    pdf.tabla_header(cols, anchos)

    fill = False
    count = 0
    async for mov in db.movimientos.find(filtro).sort("fecha", -1):
        if pdf.get_y() > 180:
            pdf.add_page("L")
            pdf.tabla_header(cols, anchos)

        # Obtener info del bien
        bien_desc = ""
        bien_cod = ""
        try:
            bien = await db.bienes.find_one({"_id": mov["bien_id"]})
            if bien:
                bien_desc = bien.get("descripcion", "")
                bien_cod = bien.get("codigo_inventario", "")
        except Exception:
            pass

        fecha = mov.get("fecha", datetime.now())
        if isinstance(fecha, datetime):
            fecha = fecha.strftime("%d/%m/%Y")

        datos = [
            str(fecha),
            mov.get("tipo", ""),
            bien_cod,
            bien_desc,
            mov.get("sede_origen", ""),
            mov.get("sede_destino", ""),
            mov.get("motivo", ""),
            mov.get("autorizado_por", ""),
        ]
        pdf.tabla_row(datos, anchos, fill)
        fill = not fill
        count += 1

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ReporteBM.P)
    pdf.cell(0, 6, f"Total de movimientos en el periodo: {count}", new_x="LMARGIN", new_y="NEXT")

    return _to_buffer(pdf)


async def generar_bm3(db, sede=None) -> BytesIO:
    """BM-3: Relación de Bienes Faltantes."""
    pdf = ReporteBM("Relacion de Bienes Faltantes", "BM-3")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    filtro = {"estado": "FALTANTE"}
    if sede:
        filtro["sede.codigo"] = sede

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*ReporteBM.D)
    pdf.cell(0, 5, f"Fecha del reporte: {datetime.now().strftime('%d/%m/%Y')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    cols = ["Cod. Inventario", "Descripcion", "Sede", "Ubicacion", "Responsable", "Valor"]
    anchos = [35, 50, 35, 30, 25, 20]
    pdf.tabla_header(cols, anchos)

    fill = False
    count = 0
    async for bien in db.bienes.find(filtro).sort("codigo_inventario", 1):
        if pdf.get_y() > 260:
            pdf.add_page()
            pdf.tabla_header(cols, anchos)
        datos = [
            bien.get("codigo_inventario", ""),
            bien.get("descripcion", ""),
            bien.get("sede", {}).get("nombre", ""),
            bien.get("ubicacion_especifica", ""),
            bien.get("responsable", ""),
            f"${bien.get('valor_adquisicion', 0):,.2f}",
        ]
        pdf.tabla_row(datos, anchos, fill)
        fill = not fill
        count += 1

    if count == 0:
        pdf.ln(5)
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, "No se registran bienes faltantes.", align="C", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*ReporteBM.P)
        pdf.cell(0, 6, f"Total de bienes faltantes: {count}", new_x="LMARGIN", new_y="NEXT")

    return _to_buffer(pdf)


async def generar_bm4(db, fecha_desde=None, fecha_hasta=None) -> BytesIO:
    """BM-4: Resumen del Movimiento - insumo para Memoria y Cuenta."""
    pdf = ReporteBM("Resumen del Movimiento", "BM-4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*ReporteBM.D)
    desde = fecha_desde.strftime('%d/%m/%Y') if fecha_desde else "Inicio"
    hasta = fecha_hasta.strftime('%d/%m/%Y') if fecha_hasta else datetime.now().strftime('%d/%m/%Y')
    pdf.cell(0, 5, f"Periodo: {desde} - {hasta}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # === Resumen del inventario ===
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*ReporteBM.P)
    pdf.cell(0, 8, "1. Resumen del Inventario", new_x="LMARGIN", new_y="NEXT")

    total = await db.bienes.count_documents({})
    activos = await db.bienes.count_documents({"estado": {"$ne": "DESINCORPORADO"}})
    desincorporados = await db.bienes.count_documents({"estado": "DESINCORPORADO"})
    faltantes = await db.bienes.count_documents({"estado": "FALTANTE"})

    pipeline_valor = [
        {"$match": {"estado": {"$ne": "DESINCORPORADO"}}},
        {"$group": {"_id": None, "total": {"$sum": "$valor_adquisicion"}}}
    ]
    valor_total = 0.0
    async for doc in db.bienes.aggregate(pipeline_valor):
        valor_total = doc["total"]

    resumen = [
        ["Total de bienes registrados", str(total)],
        ["Bienes activos", str(activos)],
        ["Bienes desincorporados", str(desincorporados)],
        ["Bienes faltantes", str(faltantes)],
        ["Valor total del inventario activo", f"${valor_total:,.2f}"],
    ]

    anchos = [120, 70]
    for row in resumen:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*ReporteBM.D)
        pdf.cell(anchos[0], 6, row[0], border=1)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(anchos[1], 6, row[1], border=1, align="C")
        pdf.ln()

    # === Distribución por sede ===
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*ReporteBM.P)
    pdf.cell(0, 8, "2. Distribucion por Sede", new_x="LMARGIN", new_y="NEXT")

    pipeline_sede = [
        {"$match": {"estado": {"$ne": "DESINCORPORADO"}}},
        {"$group": {"_id": "$sede.nombre", "total": {"$sum": 1}, "valor": {"$sum": "$valor_adquisicion"}}},
        {"$sort": {"total": -1}},
    ]
    cols_sede = ["Sede", "Cantidad", "Valor"]
    anchos_sede = [100, 40, 50]
    pdf.tabla_header(cols_sede, anchos_sede)
    async for doc in db.bienes.aggregate(pipeline_sede):
        pdf.tabla_row([doc["_id"], str(doc["total"]), f"${doc['valor']:,.2f}"], anchos_sede)

    # === Movimientos del periodo ===
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*ReporteBM.P)
    pdf.cell(0, 8, "3. Movimientos del Periodo", new_x="LMARGIN", new_y="NEXT")

    filtro_mov = {}
    if fecha_desde or fecha_hasta:
        filtro_mov["fecha"] = {}
        if fecha_desde:
            filtro_mov["fecha"]["$gte"] = fecha_desde
        if fecha_hasta:
            filtro_mov["fecha"]["$lte"] = fecha_hasta

    pipeline_tipo = [
        {"$match": filtro_mov} if filtro_mov else {"$match": {}},
        {"$group": {"_id": "$tipo", "total": {"$sum": 1}}},
    ]
    cols_tipo = ["Tipo de Movimiento", "Cantidad"]
    anchos_tipo = [120, 70]
    pdf.tabla_header(cols_tipo, anchos_tipo)
    async for doc in db.movimientos.aggregate(pipeline_tipo):
        pdf.tabla_row([doc["_id"], str(doc["total"])], anchos_tipo)

    # === Narrativa ===
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*ReporteBM.P)
    pdf.cell(0, 8, "4. Narrativa para la Memoria y Cuenta", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*ReporteBM.D)
    narrativa = (
        f"Durante el periodo reportado, la Universidad Nacional Experimental de Guayana "
        f"registro un total de {total} bienes muebles en su inventario, de los cuales "
        f"{activos} se encuentran activos con un valor patrimonial de ${valor_total:,.2f}. "
        f"Se registraron {desincorporados} bienes desincorporados y {faltantes} bienes "
        f"faltantes. La gestion de bienes se realizo en cumplimiento de la Ley Organica "
        f"de Bienes Publicos y las normativas establecidas por la SUDEBIP."
    )
    pdf.multi_cell(0, 5.5, narrativa)

    # === Firmas ===
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(95, 5, "________________________", align="C")
    pdf.cell(95, 5, "________________________", align="C")
    pdf.ln()
    pdf.cell(95, 5, "Jefe de Bienes Nacionales", align="C")
    pdf.cell(95, 5, "Director de Administracion", align="C")

    return _to_buffer(pdf)
