"""Genera PDF 3: Modelo de Datos (ER)."""
from fpdf import FPDF

class ERPDF(FPDF):
    P = (0, 51, 102); S = (196, 163, 90); D = (33, 37, 41); W = (255, 255, 255); LB = (245, 247, 250)

    def header(self):
        self.set_font("Helvetica", "B", 9); self.set_text_color(*self.P)
        self.cell(0, 6, "UNEG - Modelo de Datos", align="L")
        self.cell(0, 6, "Documento Tecnico", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.S); self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y()); self.ln(4)

    def footer(self):
        self.set_y(-15); self.set_font("Helvetica", "I", 8); self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def titulo(self, t):
        self.set_font("Helvetica", "B", 16); self.set_text_color(*self.P)
        self.cell(0, 12, t, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.S); self.set_line_width(0.5)
        self.line(10, self.get_y(), 80, self.get_y()); self.ln(6)

    def sub(self, t):
        self.set_font("Helvetica", "B", 13); self.set_text_color(*self.P)
        self.cell(0, 10, t, new_x="LMARGIN", new_y="NEXT"); self.ln(2)

    def txt(self, t):
        self.set_font("Helvetica", "", 10); self.set_text_color(*self.D)
        self.multi_cell(0, 5.5, t); self.ln(3)

    def entidad(self, x, y, nombre, campos, color, w=55):
        # Header
        self.set_fill_color(*color)
        self.set_draw_color(max(0,color[0]-40), max(0,color[1]-40), max(0,color[2]-40))
        self.rect(x, y, w, 8, style="DF")
        self.set_font("Helvetica", "B", 8); self.set_text_color(*self.W)
        self.set_xy(x, y); self.cell(w, 8, nombre, align="C")
        # Body
        self.set_fill_color(250, 250, 255)
        h = len(campos) * 5.5 + 2
        self.rect(x, y + 8, w, h, style="DF")
        self.set_font("Helvetica", "", 6.5); self.set_text_color(*self.D)
        for i, c in enumerate(campos):
            self.set_xy(x + 2, y + 9 + i * 5.5)
            self.cell(w - 4, 5, c)
        return y + 8 + h

    def relacion(self, x1, y1, x2, y2, label="", card1="", card2=""):
        self.set_draw_color(100, 100, 100); self.set_line_width(0.4)
        self.line(x1, y1, x2, y2)
        self.set_font("Helvetica", "I", 6); self.set_text_color(100, 100, 100)
        mx = (x1 + x2) / 2; my = (y1 + y2) / 2
        if label:
            self.set_xy(mx - 12, my - 6); self.cell(24, 4, label, align="C")
        if card1:
            self.set_xy(x1 - 5 if x1 < x2 else x1 + 1, y1 - 4); self.cell(10, 4, card1)
        if card2:
            self.set_xy(x2 - 5 if x2 < x1 else x2 + 1, y2 - 4); self.cell(10, 4, card2)


def generar():
    pdf = ERPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # PORTADA
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 26); pdf.set_text_color(*ERPDF.P)
    pdf.cell(0, 14, "Modelo de Datos", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(*ERPDF.S); pdf.set_line_width(1.2)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y()); pdf.ln(8)
    pdf.set_font("Helvetica", "", 13); pdf.set_text_color(*ERPDF.D)
    pdf.cell(0, 8, "Diagrama Entidad-Relacion y Esquemas", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Base de Datos MongoDB", align="C", new_x="LMARGIN", new_y="NEXT")

    # ER DIAGRAM
    pdf.add_page()
    pdf.titulo("1. Diagrama Entidad-Relacion")
    pdf.txt("Representacion visual de las colecciones MongoDB y sus relaciones logicas:")
    y0 = pdf.get_y() + 4

    # Entidades
    pdf.entidad(10, y0, "BIENES", [
        "_id: ObjectId (PK)", "codigo_inventario: String (UK)",
        "codigo_sudebip: String (FK)", "descripcion: String",
        "marca: String", "modelo: String", "serial: String",
        "valor_adquisicion: Float", "fecha_adquisicion: Date",
        "estado: Enum", "condicion: Enum",
        "sede_codigo: String (FK)", "ubicacion: String",
        "responsable: String", "cedula_responsable: String",
    ], (0, 51, 102), w=60)

    pdf.entidad(80, y0, "MOVIMIENTOS", [
        "_id: ObjectId (PK)", "bien_id: ObjectId (FK)",
        "tipo: Enum", "fecha: Date",
        "sede_origen: String (FK)", "sede_destino: String (FK)",
        "motivo: String", "autorizado_por: String",
        "documento_soporte: String",
    ], (231, 76, 60), w=55)

    pdf.entidad(145, y0, "DESINCORPORACIONES", [
        "_id: ObjectId (PK)", "bien_id: ObjectId (FK)",
        "motivo: Enum", "justificacion: String",
        "estado_proceso: Enum",
        "solicitado_por: String", "fecha_solicitud: Date",
        "validacion_ia: Object",
        "aprobado_por: String", "fecha_aprobacion: Date",
    ], (155, 89, 182), w=55)

    y1 = y0 + 100
    pdf.entidad(20, y1, "SEDES", [
        "_id: ObjectId (PK)", "codigo: String (UK)",
        "nombre: String", "ciudad: String",
        "direccion: String", "activa: Boolean",
    ], (46, 204, 113), w=55)

    pdf.entidad(120, y1, "CLASIFICADOR_SUDEBIP", [
        "_id: ObjectId (PK)", "codigo: String (UK)",
        "grupo: String", "subgrupo: String",
        "seccion: String", "categoria: String",
        "descripcion: String", "palabras_clave: Array",
    ], (243, 156, 18), w=60)

    # Relaciones
    pdf.relacion(70, y0 + 30, 80, y0 + 30, "tiene", "1", "N")
    pdf.relacion(70, y0 + 40, 145, y0 + 40, "puede tener", "1", "0..1")
    pdf.relacion(30, y0 + 93, 30, y1, "ubicado en", "N", "1")
    pdf.relacion(60, y0 + 93, 120, y1 + 10, "clasificado", "N", "1")

    pdf.ln(y1 + 60 - pdf.get_y())

    # COLECCION BIENES
    pdf.add_page()
    pdf.titulo("2. Coleccion: bienes")
    pdf.txt("Coleccion principal que almacena cada activo registrado en la UNEG.")

    pdf.sub("Campos")
    campos = [
        ["_id", "ObjectId", "Identificador unico MongoDB"],
        ["codigo_inventario", "String", "Formato: UNEG-{SEDE}-{GRUPO}-{SEQ}"],
        ["codigo_sudebip", "String", "Codigo del clasificador (ej: 1.02.01.01)"],
        ["grupo_sudebip", "String", "Descripcion del grupo"],
        ["descripcion", "String", "Descripcion del bien"],
        ["marca", "String", "Marca del equipo/mobiliario"],
        ["modelo", "String", "Modelo especifico"],
        ["serial", "String", "Numero de serie"],
        ["valor_adquisicion", "Float", "Valor en USD o Bs"],
        ["fecha_adquisicion", "Date", "Fecha de compra/incorporacion"],
        ["estado", "Enum", "EN_USO, EN_DESUSO, INSERVIBLE, etc."],
        ["condicion", "Enum", "BUENO, REGULAR, MALO"],
        ["sede", "Object", "{ codigo, nombre }"],
        ["ubicacion_especifica", "String", "Edificio, piso, oficina"],
        ["responsable", "String", "Nombre del custodio"],
        ["cedula_responsable", "String", "Cedula del custodio"],
        ["departamento", "String", "Departamento o coordinacion"],
        ["observaciones", "String", "Notas adicionales"],
        ["created_at", "DateTime", "Fecha de registro"],
        ["updated_at", "DateTime", "Ultima modificacion"],
    ]

    anchos = [45, 30, 115]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Campo", "Tipo", "Descripcion"]):
        pdf.cell(anchos[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    fill = False
    for row in campos:
        if pdf.get_y() > 260: pdf.add_page()
        pdf.set_font("Helvetica", "B" if row[0] == "_id" else "", 7)
        pdf.set_text_color(*ERPDF.D)
        if fill: pdf.set_fill_color(235, 240, 248)
        else: pdf.set_fill_color(*ERPDF.W)
        for i, c in enumerate(row):
            pdf.cell(anchos[i], 5.5, c, border=1, fill=True)
        pdf.ln(); fill = not fill

    pdf.ln(4)
    pdf.sub("Estados validos del bien")
    estados = [
        ["EN_USO", "El bien esta en uso activo"],
        ["EN_DESUSO", "El bien no se utiliza pero esta funcional"],
        ["INSERVIBLE", "El bien no funciona, candidato a desincorporacion"],
        ["EN_REPARACION", "El bien esta en proceso de reparacion"],
        ["DESINCORPORADO", "El bien fue dado de baja oficialmente"],
        ["FALTANTE", "El bien no se localiza (BM-3)"],
    ]
    anchos2 = [50, 140]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Estado", "Descripcion"]):
        pdf.cell(anchos2[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for row in estados:
        pdf.set_font("Helvetica", "B", 7); pdf.set_text_color(*ERPDF.D)
        pdf.set_fill_color(*ERPDF.W)
        pdf.cell(anchos2[0], 5.5, row[0], border=1, fill=True, align="C")
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(anchos2[1], 5.5, row[1], border=1, fill=True)
        pdf.ln()

    # COLECCION MOVIMIENTOS
    pdf.add_page()
    pdf.titulo("3. Coleccion: movimientos")
    pdf.txt("Registra cada movimiento de bienes (entradas, salidas, traslados, reasignaciones).")
    campos_mov = [
        ["_id", "ObjectId", "Identificador unico"],
        ["bien_id", "ObjectId", "Referencia al bien (FK)"],
        ["tipo", "Enum", "ENTRADA, SALIDA, TRASLADO, REASIGNACION"],
        ["fecha", "Date", "Fecha del movimiento"],
        ["sede_origen", "String", "Codigo de sede origen"],
        ["sede_destino", "String", "Codigo de sede destino"],
        ["motivo", "String", "Razon del movimiento"],
        ["autorizado_por", "String", "Persona que autoriza"],
        ["documento_soporte", "String", "Numero de oficio/acta"],
    ]
    anchos = [45, 30, 115]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Campo", "Tipo", "Descripcion"]):
        pdf.cell(anchos[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for row in campos_mov:
        pdf.set_font("Helvetica", "", 7); pdf.set_text_color(*ERPDF.D)
        pdf.set_fill_color(*ERPDF.W)
        for i, c in enumerate(row):
            pdf.cell(anchos[i], 5.5, c, border=1, fill=True)
        pdf.ln()

    # COLECCION DESINCORPORACIONES
    pdf.ln(6)
    pdf.titulo("4. Coleccion: desincorporaciones")
    pdf.txt("Gestiona el proceso de baja de bienes con validacion legal y aprobacion.")
    campos_des = [
        ["_id", "ObjectId", "Identificador unico"],
        ["bien_id", "ObjectId", "Referencia al bien (FK)"],
        ["motivo", "Enum", "OBSOLESCENCIA, INSERVIBILIDAD, HURTO, etc."],
        ["justificacion_tecnica", "String", "Descripcion tecnica detallada"],
        ["estado_proceso", "Enum", "SOLICITADA, EN_REVISION, APROBADA, etc."],
        ["solicitado_por", "String", "Persona que solicita"],
        ["fecha_solicitud", "Date", "Fecha de la solicitud"],
        ["validacion_ia", "Object", "Resultado del analisis de IA"],
        ["aprobado_por", "String", "Persona que aprueba"],
        ["fecha_aprobacion", "Date", "Fecha de aprobacion"],
    ]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Campo", "Tipo", "Descripcion"]):
        pdf.cell(anchos[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for row in campos_des:
        pdf.set_font("Helvetica", "", 7); pdf.set_text_color(*ERPDF.D)
        pdf.set_fill_color(*ERPDF.W)
        for i, c in enumerate(row):
            pdf.cell(anchos[i], 5.5, c, border=1, fill=True)
        pdf.ln()

    # COLECCION CLASIFICADOR + SEDES
    pdf.add_page()
    pdf.titulo("5. Coleccion: clasificador_sudebip")
    pdf.txt("Catalogo oficial de codificacion de bienes segun la SUDEBIP.")
    campos_cla = [
        ["_id", "ObjectId", "Identificador unico"],
        ["codigo", "String", "Codigo jerarquico (ej: 1.02.01.01)"],
        ["grupo", "String", "Primer nivel (ej: 1)"],
        ["subgrupo", "String", "Segundo nivel (ej: 02)"],
        ["seccion", "String", "Tercer nivel (ej: 01)"],
        ["categoria", "String", "Cuarto nivel (ej: 01)"],
        ["descripcion_grupo", "String", "Nombre del grupo"],
        ["descripcion_subgrupo", "String", "Nombre del subgrupo"],
        ["descripcion", "String", "Nombre de la categoria"],
        ["palabras_clave", "Array", "Sinonimos para busqueda"],
    ]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Campo", "Tipo", "Descripcion"]):
        pdf.cell(anchos[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for row in campos_cla:
        pdf.set_font("Helvetica", "", 7); pdf.set_text_color(*ERPDF.D)
        pdf.set_fill_color(*ERPDF.W)
        for i, c in enumerate(row):
            pdf.cell(anchos[i], 5.5, c, border=1, fill=True)
        pdf.ln()

    pdf.ln(6)
    pdf.titulo("6. Coleccion: sedes")
    pdf.txt("Sedes y nucleos de la UNEG donde se ubican los bienes.")
    campos_sed = [
        ["_id", "ObjectId", "Identificador unico"],
        ["codigo", "String", "Codigo corto (ej: ATL, VAS)"],
        ["nombre", "String", "Nombre completo de la sede"],
        ["ciudad", "String", "Ciudad donde se ubica"],
        ["direccion", "String", "Direccion fisica"],
        ["activa", "Boolean", "Si la sede esta activa"],
    ]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Campo", "Tipo", "Descripcion"]):
        pdf.cell(anchos[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for row in campos_sed:
        pdf.set_font("Helvetica", "", 7); pdf.set_text_color(*ERPDF.D)
        pdf.set_fill_color(*ERPDF.W)
        for i, c in enumerate(row):
            pdf.cell(anchos[i], 5.5, c, border=1, fill=True)
        pdf.ln()

    # INDICES
    pdf.ln(8)
    pdf.titulo("7. Indices Recomendados")
    indices = [
        ["bienes", "codigo_inventario", "Unico", "Busqueda rapida por codigo"],
        ["bienes", "codigo_sudebip", "Normal", "Filtro por clasificacion"],
        ["bienes", "estado", "Normal", "Filtro por estado"],
        ["bienes", "sede.codigo", "Normal", "Filtro por sede"],
        ["movimientos", "bien_id", "Normal", "Historial del bien"],
        ["movimientos", "fecha", "Normal", "Filtro por periodo"],
        ["desincorporaciones", "bien_id", "Unico", "Una por bien"],
        ["clasificador_sudebip", "codigo", "Unico", "Busqueda por codigo"],
        ["clasificador_sudebip", "palabras_clave", "Text", "Busqueda full-text"],
        ["sedes", "codigo", "Unico", "Busqueda por codigo"],
    ]
    anchos3 = [40, 45, 25, 80]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*ERPDF.P); pdf.set_text_color(*ERPDF.W)
    for i, h in enumerate(["Coleccion", "Campo", "Tipo", "Proposito"]):
        pdf.cell(anchos3[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()
    for row in indices:
        if pdf.get_y() > 260: pdf.add_page()
        pdf.set_font("Helvetica", "", 7); pdf.set_text_color(*ERPDF.D)
        pdf.set_fill_color(*ERPDF.W)
        for i, c in enumerate(row):
            pdf.cell(anchos3[i], 5.5, c, border=1, fill=True)
        pdf.ln()

    out = "docs/03_Modelo_Datos_ER.pdf"
    pdf.output(out)
    print(f"Generado: {out}")

if __name__ == "__main__":
    generar()
