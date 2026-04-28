"""Genera PDF 2: Arquitectura del Sistema."""
from fpdf import FPDF
import math

class ArqPDF(FPDF):
    P = (0, 51, 102)
    S = (196, 163, 90)
    D = (33, 37, 41)
    W = (255, 255, 255)
    LB = (245, 247, 250)

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.P)
        self.cell(0, 6, "UNEG - Arquitectura del Sistema", align="L")
        self.cell(0, 6, "Documento Tecnico", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.S)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def titulo(self, txt):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*self.P)
        self.cell(0, 12, txt, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.S)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(6)

    def sub(self, txt):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*self.P)
        self.cell(0, 10, txt, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def txt(self, t):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.D)
        self.multi_cell(0, 5.5, t)
        self.ln(3)

    def caja(self, x, y, w, h, label, color, sub_label=None):
        self.set_fill_color(*color)
        self.set_draw_color(max(0, color[0]-30), max(0, color[1]-30), max(0, color[2]-30))
        self.rect(x, y, w, h, style="DF")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.W)
        self.set_xy(x, y + 2)
        self.cell(w, 5, label, align="C")
        if sub_label:
            self.set_font("Helvetica", "", 6)
            self.set_xy(x, y + 7)
            self.cell(w, 4, sub_label, align="C")

    def flecha_v(self, x, y1, y2):
        self.set_draw_color(*self.D)
        self.set_line_width(0.4)
        self.line(x, y1, x, y2)
        self.line(x, y2, x - 2, y2 - 3)
        self.line(x, y2, x + 2, y2 - 3)

    def flecha_h(self, x1, y, x2):
        self.set_draw_color(*self.D)
        self.set_line_width(0.4)
        self.line(x1, y, x2, y)
        self.line(x2, y, x2 - 3, y - 2)
        self.line(x2, y, x2 - 3, y + 2)


def generar():
    pdf = ArqPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # === PORTADA ===
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(*ArqPDF.P)
    pdf.cell(0, 14, "Arquitectura del Sistema", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(*ArqPDF.S)
    pdf.set_line_width(1.2)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*ArqPDF.D)
    pdf.cell(0, 8, "Sistema de Gestion de Memoria y Cuenta", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "UNEG", align="C", new_x="LMARGIN", new_y="NEXT")

    # === DIAGRAMA DE ARQUITECTURA GENERAL ===
    pdf.add_page()
    pdf.titulo("1. Arquitectura General del Sistema")
    pdf.txt("El sistema sigue una arquitectura de tres capas (Frontend, Backend, Datos) "
            "con contenedorizacion Docker para portabilidad.")
    pdf.ln(2)

    # Dibujar diagrama
    y0 = pdf.get_y() + 2
    # Capa Frontend
    pdf.set_fill_color(230, 240, 255)
    pdf.set_draw_color(*ArqPDF.P)
    pdf.set_line_width(0.3)
    pdf.rect(15, y0, 180, 22, style="DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ArqPDF.P)
    pdf.set_xy(17, y0 + 1)
    pdf.cell(50, 5, "CAPA FRONTEND")
    pdf.caja(20, y0 + 7, 50, 12, "React 19 + Vite", (74, 144, 226), "Dashboard + Forms")
    pdf.caja(80, y0 + 7, 50, 12, "Tailwind CSS v4", (56, 178, 172), "Estilos")
    pdf.caja(140, y0 + 7, 50, 12, "Recharts", (142, 68, 173), "Graficos")

    # Flechas
    pdf.flecha_v(105, y0 + 22, y0 + 30)

    # Capa Backend
    y1 = y0 + 30
    pdf.set_fill_color(255, 243, 224)
    pdf.set_draw_color(196, 163, 90)
    pdf.rect(15, y1, 180, 45, style="DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ArqPDF.P)
    pdf.set_xy(17, y1 + 1)
    pdf.cell(50, 5, "CAPA BACKEND (FastAPI)")

    pdf.caja(20, y1 + 8, 38, 12, "API REST", (52, 73, 94), "Routers")
    pdf.caja(62, y1 + 8, 38, 12, "Pydantic v2", (231, 76, 60), "Validacion")
    pdf.caja(104, y1 + 8, 38, 12, "LangChain", (46, 204, 113), "IA Service")
    pdf.caja(146, y1 + 8, 44, 12, "Reportes PDF", (243, 156, 18), "BM-1 a BM-4")

    pdf.caja(20, y1 + 25, 55, 14, "Clasificador SUDEBIP", (155, 89, 182), "Codificacion bienes")
    pdf.caja(80, y1 + 25, 55, 14, "Validacion Legal", (231, 76, 60), "Desincorporaciones")
    pdf.caja(140, y1 + 25, 50, 14, "Narrativa IA", (46, 204, 113), "Memoria y Cuenta")

    # Flechas
    pdf.flecha_v(60, y1 + 45, y1 + 53)
    pdf.flecha_v(150, y1 + 45, y1 + 53)

    # Capa Datos
    y2 = y1 + 53
    pdf.set_fill_color(232, 245, 233)
    pdf.set_draw_color(76, 175, 80)
    pdf.rect(15, y2, 180, 22, style="DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ArqPDF.P)
    pdf.set_xy(17, y2 + 1)
    pdf.cell(50, 5, "CAPA DE DATOS")

    pdf.caja(25, y2 + 7, 55, 12, "MongoDB 7", (76, 175, 80), "Motor async driver")
    pdf.caja(130, y2 + 7, 55, 12, "Ollama", (255, 152, 0), "Gemma:7b local")

    pdf.ln(y2 + 30 - pdf.get_y())

    # === DIAGRAMA DE COMPONENTES ===
    pdf.add_page()
    pdf.titulo("2. Diagrama de Componentes del Backend")
    pdf.txt("Estructura modular del backend organizada por responsabilidad.")
    pdf.ln(2)

    y0 = pdf.get_y() + 2
    components = [
        ("app/main.py", "Punto de entrada FastAPI", (0, 51, 102)),
        ("app/config.py", "Configuracion centralizada", (52, 73, 94)),
        ("app/database.py", "Conexion MongoDB", (76, 175, 80)),
    ]
    routers = [
        ("bienes.py", "CRUD activos"),
        ("movimientos.py", "Historial"),
        ("desincorporaciones.py", "Flujo baja"),
        ("reportes.py", "BM-1 a BM-4"),
        ("clasificador.py", "Catalogo"),
        ("chat.py", "Asistente IA"),
        ("sedes.py", "Gestion sedes"),
    ]
    services = [
        ("ia_service.py", "LangChain + Gemma"),
        ("reporte_service.py", "Gen. PDFs"),
        ("clasificador_service.py", "Busqueda SUDEBIP"),
        ("validacion_service.py", "Valid. legal"),
    ]

    # Main components
    for i, (name, desc, color) in enumerate(components):
        pdf.caja(15 + i * 63, y0, 58, 14, name, color, desc)

    # Routers section
    y1 = y0 + 20
    pdf.set_fill_color(230, 240, 255)
    pdf.set_draw_color(*ArqPDF.P)
    pdf.rect(15, y1, 180, 45, style="DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ArqPDF.P)
    pdf.set_xy(17, y1 + 1)
    pdf.cell(50, 5, "ROUTERS (app/routers/)")

    for i, (name, desc) in enumerate(routers):
        col = i % 4
        row = i // 4
        pdf.caja(20 + col * 44, y1 + 8 + row * 18, 40, 14, name, (74, 144, 226), desc)

    # Services section
    y2 = y1 + 50
    pdf.set_fill_color(232, 245, 233)
    pdf.set_draw_color(76, 175, 80)
    pdf.rect(15, y2, 180, 25, style="DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*ArqPDF.P)
    pdf.set_xy(17, y2 + 1)
    pdf.cell(50, 5, "SERVICES (app/services/)")

    for i, (name, desc) in enumerate(services):
        pdf.caja(20 + i * 44, y2 + 8, 40, 14, name, (46, 204, 113), desc)

    pdf.ln(y2 + 30 - pdf.get_y())

    # === DOCKER ===
    pdf.add_page()
    pdf.titulo("3. Infraestructura Docker")
    pdf.txt("El sistema se despliega mediante Docker Compose con 4 servicios contenedorizados:")

    y0 = pdf.get_y() + 4
    containers = [
        ("uneg_frontend", "React + Vite", ":5173", (74, 144, 226)),
        ("uneg_api", "FastAPI + Python", ":8000", (231, 76, 60)),
        ("uneg_mongodb", "MongoDB 7", ":27017", (76, 175, 80)),
        ("uneg_ollama", "Ollama + Gemma", ":11434", (255, 152, 0)),
    ]

    pdf.set_fill_color(*ArqPDF.LB)
    pdf.set_draw_color(*ArqPDF.P)
    pdf.rect(15, y0, 180, 70, style="DF")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ArqPDF.P)
    pdf.set_xy(17, y0 + 2)
    pdf.cell(60, 6, "Docker Compose Network")

    for i, (name, tech, port, color) in enumerate(containers):
        x = 25 + (i % 2) * 85
        y = y0 + 12 + (i // 2) * 28
        pdf.set_fill_color(*color)
        pdf.set_draw_color(max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40))
        pdf.rect(x, y, 75, 22, style="DF")
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*ArqPDF.W)
        pdf.set_xy(x, y + 3)
        pdf.cell(75, 5, name, align="C")
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(x, y + 9)
        pdf.cell(75, 4, tech, align="C")
        pdf.set_xy(x, y + 14)
        pdf.cell(75, 4, f"Puerto {port}", align="C")

    # Flechas entre containers
    pdf.flecha_h(100, y0 + 23, 110)  # frontend -> api
    pdf.flecha_v(62, y0 + 34, y0 + 40)  # api -> mongo (conceptual)
    pdf.flecha_v(147, y0 + 34, y0 + 40)  # api -> ollama (conceptual)

    pdf.ln(y0 + 78 - pdf.get_y())

    # === COMUNICACION ===
    pdf.add_page()
    pdf.titulo("4. Flujo de Comunicacion")
    pdf.txt("Diagrama de secuencia simplificado para el registro de un bien:")
    y0 = pdf.get_y() + 4

    actors = [
        ("Usuario", 35, (74, 144, 226)),
        ("Frontend", 75, (142, 68, 173)),
        ("API", 115, (231, 76, 60)),
        ("MongoDB", 155, (76, 175, 80)),
    ]

    # Lineas de vida
    for name, x, color in actors:
        pdf.caja(x - 15, y0, 30, 10, name, color)
        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.2)
        pdf.set_dash_pattern(dash=2, gap=2)
        pdf.line(x, y0 + 10, x, y0 + 90)
    pdf.set_dash_pattern(dash=0, gap=0)

    # Mensajes
    msgs = [
        (35, 75, "Llena formulario", y0 + 18),
        (75, 115, "POST /api/bienes", y0 + 30),
        (115, 115, "Validar Pydantic", y0 + 40),
        (115, 155, "Guardar documento", y0 + 50),
        (155, 115, "OK + _id", y0 + 60),
        (115, 75, "201 Created", y0 + 70),
        (75, 35, "Notificacion exito", y0 + 80),
    ]

    for x1, x2, msg, y in msgs:
        pdf.set_draw_color(*ArqPDF.D)
        pdf.set_line_width(0.3)
        if x1 == x2:
            pdf.rect(x1, y - 1, 15, 6, style="D")
            pdf.set_font("Helvetica", "", 6)
            pdf.set_text_color(*ArqPDF.D)
            pdf.set_xy(x1 + 16, y)
            pdf.cell(30, 4, msg)
        else:
            if x2 > x1:
                pdf.flecha_h(x1, y, x2)
            else:
                pdf.set_draw_color(*ArqPDF.D)
                pdf.set_line_width(0.3)
                pdf.line(x1, y, x2, y)
                pdf.line(x2, y, x2 + 3, y - 2)
                pdf.line(x2, y, x2 + 3, y + 2)
            pdf.set_font("Helvetica", "", 6)
            pdf.set_text_color(*ArqPDF.D)
            mid = min(x1, x2) + abs(x2 - x1) / 2
            pdf.set_xy(mid - 12, y - 5)
            pdf.cell(24, 4, msg, align="C")

    pdf.ln(y0 + 98 - pdf.get_y())

    # === API ENDPOINTS ===
    pdf.add_page()
    pdf.titulo("5. Endpoints de la API REST")
    pdf.txt("Listado completo de endpoints organizados por modulo:")

    # Tabla de endpoints
    endpoints = [
        ["POST", "/api/bienes", "Registrar bien nuevo"],
        ["GET", "/api/bienes", "Listar bienes (filtros)"],
        ["GET", "/api/bienes/{id}", "Detalle de un bien"],
        ["PUT", "/api/bienes/{id}", "Actualizar bien"],
        ["PATCH", "/api/bienes/{id}/estado", "Cambiar estado"],
        ["GET", "/api/bienes/estadisticas", "KPIs por sede/grupo"],
        ["POST", "/api/movimientos", "Registrar movimiento"],
        ["GET", "/api/movimientos", "Historial movimientos"],
        ["POST", "/api/desincorporaciones", "Solicitar baja"],
        ["PATCH", "/api/desincorporaciones/{id}", "Aprobar/rechazar"],
        ["GET", "/api/desincorporaciones", "Listar solicitudes"],
        ["GET", "/api/reportes/bm1", "Inventario (PDF)"],
        ["GET", "/api/reportes/bm2", "Movimientos (PDF)"],
        ["GET", "/api/reportes/bm3", "Faltantes (PDF)"],
        ["GET", "/api/reportes/bm4", "Resumen M&C (PDF)"],
        ["GET", "/api/clasificador/buscar", "Buscar codigo SUDEBIP"],
        ["POST", "/api/chat", "Consulta asistente IA"],
        ["GET", "/api/sedes", "Listar sedes"],
        ["POST", "/api/sedes", "Registrar sede"],
    ]

    anchos = [20, 65, 105]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*ArqPDF.P)
    pdf.set_text_color(*ArqPDF.W)
    for i, h in enumerate(["Metodo", "Endpoint", "Descripcion"]):
        pdf.cell(anchos[i], 7, h, border=1, fill=True, align="C")
    pdf.ln()

    colors_method = {
        "GET": (46, 204, 113),
        "POST": (74, 144, 226),
        "PUT": (243, 156, 18),
        "PATCH": (155, 89, 182),
        "DELETE": (231, 76, 60),
    }

    for row in endpoints:
        if pdf.get_y() > 260:
            pdf.add_page()
        method, endpoint, desc = row
        mc = colors_method.get(method, ArqPDF.D)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(*mc)
        pdf.set_text_color(*ArqPDF.W)
        pdf.cell(anchos[0], 6, method, border=1, fill=True, align="C")
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*ArqPDF.D)
        pdf.set_fill_color(*ArqPDF.W)
        pdf.cell(anchos[1], 6, endpoint, border=1, fill=True)
        pdf.cell(anchos[2], 6, desc, border=1, fill=True)
        pdf.ln()

    out = "docs/02_Arquitectura_Sistema.pdf"
    pdf.output(out)
    print(f"Generado: {out}")

if __name__ == "__main__":
    generar()
