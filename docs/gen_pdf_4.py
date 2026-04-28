"""Genera PDF 4: Flujos de Procesos."""
from fpdf import FPDF

class FlowPDF(FPDF):
    P=(0,51,102); S=(196,163,90); D=(33,37,41); W=(255,255,255)

    def header(self):
        self.set_font("Helvetica","B",9); self.set_text_color(*self.P)
        self.cell(0,6,"UNEG - Flujos de Procesos",align="L")
        self.cell(0,6,"Documento Tecnico",align="R",new_x="LMARGIN",new_y="NEXT")
        self.set_draw_color(*self.S); self.set_line_width(0.8)
        self.line(10,self.get_y(),200,self.get_y()); self.ln(4)

    def footer(self):
        self.set_y(-15); self.set_font("Helvetica","I",8); self.set_text_color(150,150,150)
        self.cell(0,10,f"Pagina {self.page_no()}/{{nb}}",align="C")

    def titulo(self,t):
        self.set_font("Helvetica","B",16); self.set_text_color(*self.P)
        self.cell(0,12,t,new_x="LMARGIN",new_y="NEXT")
        self.set_draw_color(*self.S); self.set_line_width(0.5)
        self.line(10,self.get_y(),80,self.get_y()); self.ln(6)

    def txt(self,t):
        self.set_font("Helvetica","",10); self.set_text_color(*self.D)
        self.multi_cell(0,5.5,t); self.ln(3)

    def nodo(self, x, y, w, h, label, color, shape="rect"):
        self.set_fill_color(*color)
        self.set_draw_color(max(0,color[0]-40),max(0,color[1]-40),max(0,color[2]-40))
        if shape == "diamond":
            cx, cy = x + w/2, y + h/2
            pts = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
            # Draw diamond as lines
            for i in range(4):
                x1, y1 = pts[i]; x2, y2 = pts[(i+1)%4]
                self.line(x1, y1, x2, y2)
            self.set_font("Helvetica","B",6); self.set_text_color(*self.D)
            self.set_xy(x+2, cy-3); self.cell(w-4, 6, label, align="C")
        elif shape == "round":
            self.rect(x, y, w, h, style="DF", round_corners=True)
            self.set_font("Helvetica","B",7); self.set_text_color(*self.W)
            self.set_xy(x, y+1); self.cell(w, h-2, label, align="C")
        else:
            self.rect(x, y, w, h, style="DF")
            self.set_font("Helvetica","B",7); self.set_text_color(*self.W)
            self.set_xy(x, y+1); self.cell(w, h-2, label, align="C")

    def flecha(self, x1, y1, x2, y2, label=""):
        self.set_draw_color(100,100,100); self.set_line_width(0.4)
        self.line(x1, y1, x2, y2)
        # Arrowhead
        if y2 > y1:  # down
            self.line(x2, y2, x2-2, y2-3); self.line(x2, y2, x2+2, y2-3)
        elif y2 < y1:  # up
            self.line(x2, y2, x2-2, y2+3); self.line(x2, y2, x2+2, y2+3)
        elif x2 > x1:  # right
            self.line(x2, y2, x2-3, y2-2); self.line(x2, y2, x2-3, y2+2)
        else:  # left
            self.line(x2, y2, x2+3, y2-2); self.line(x2, y2, x2+3, y2+2)
        if label:
            self.set_font("Helvetica","",5.5); self.set_text_color(100,100,100)
            mx=(x1+x2)/2; my=(y1+y2)/2
            self.set_xy(mx-10, my-5); self.cell(20,4,label,align="C")


def generar():
    pdf = FlowPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # PORTADA
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica","B",26); pdf.set_text_color(*FlowPDF.P)
    pdf.cell(0,14,"Flujos de Procesos",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(*FlowPDF.S); pdf.set_line_width(1.2)
    pdf.line(60,pdf.get_y(),150,pdf.get_y()); pdf.ln(8)
    pdf.set_font("Helvetica","",13); pdf.set_text_color(*FlowPDF.D)
    pdf.cell(0,8,"Diagramas de flujo de los procesos principales",align="C",new_x="LMARGIN",new_y="NEXT")

    # FLUJO 1: REGISTRO DE BIEN
    pdf.add_page()
    pdf.titulo("1. Flujo: Registro de un Bien")
    pdf.txt("Proceso completo desde que el usuario ingresa los datos hasta que el bien queda registrado en MongoDB.")
    y = pdf.get_y() + 4
    cx = 105  # center x

    steps = [
        (cx-30, y, 60, 10, "Inicio: Usuario abre formulario", (46,204,113), "round"),
        (cx-35, y+16, 70, 10, "Ingresa datos del bien", (74,144,226), "rect"),
        (cx-35, y+32, 70, 10, "IA busca en Clasificador SUDEBIP", (155,89,182), "rect"),
        (cx-20, y+50, 40, 20, "Codigo encontrado?", (243,156,18), "diamond"),
        (cx-35, y+78, 70, 10, "Asignar codigo automaticamente", (46,204,113), "rect"),
        (cx-35, y+94, 70, 10, "Validacion Pydantic completa", (231,76,60), "rect"),
        (cx-20, y+112, 40, 20, "Datos validos?", (243,156,18), "diamond"),
        (cx-35, y+140, 70, 10, "Guardar en MongoDB", (76,175,80), "rect"),
        (cx-35, y+156, 70, 10, "Generar codigo inventario unico", (74,144,226), "rect"),
        (cx-30, y+172, 60, 10, "Bien registrado exitosamente", (46,204,113), "round"),
    ]

    for s in steps:
        pdf.nodo(*s)

    # Flechas verticales
    for i in range(len(steps)-1):
        s1, s2 = steps[i], steps[i+1]
        y1_end = s1[1] + s1[3]
        y2_start = s2[1]
        if s1[6] == "diamond":
            y1_end = s1[1] + s1[3]
        pdf.flecha(cx, y1_end, cx, y2_start)

    # Side labels for diamonds
    pdf.set_font("Helvetica","B",6); pdf.set_text_color(46,204,113)
    pdf.set_xy(cx+22, y+58); pdf.cell(10,4,"Si")
    pdf.set_xy(cx+22, y+120); pdf.cell(10,4,"Si")

    # Side paths for "No"
    pdf.set_text_color(231,76,60)
    # Diamond 1 No -> manual classification
    pdf.set_draw_color(231,76,60); pdf.set_line_width(0.3)
    pdf.line(cx-20, y+60, cx-45, y+60)
    pdf.set_font("Helvetica","B",6)
    pdf.set_xy(cx-70, y+57); pdf.cell(22,4,"No: Manual")

    # Diamond 2 No -> show errors
    pdf.line(cx+20, y+122, cx+45, y+122)
    pdf.set_xy(cx+46, y+119); pdf.cell(22,4,"No: Errores")

    pdf.ln(y+190 - pdf.get_y())

    # FLUJO 2: DESINCORPORACION
    pdf.add_page()
    pdf.titulo("2. Flujo: Desincorporacion de un Bien")
    pdf.txt("Proceso de baja de un bien con validacion por IA y aprobacion de autoridad.")
    y = pdf.get_y() + 4

    steps2 = [
        (cx-30, y, 60, 10, "Inicio: Solicitud de baja", (46,204,113), "round"),
        (cx-35, y+16, 70, 10, "Seleccionar bien y motivo", (74,144,226), "rect"),
        (cx-35, y+32, 70, 10, "Ingresar justificacion tecnica", (74,144,226), "rect"),
        (cx-35, y+48, 70, 10, "IA analiza justificacion", (155,89,182), "rect"),
        (cx-22, y+66, 44, 20, "Cumple criterios?", (243,156,18), "diamond"),
        (cx-35, y+94, 70, 10, "Estado: EN_REVISION", (74,144,226), "rect"),
        (cx-35, y+110, 70, 10, "Revision por autoridad", (52,73,94), "rect"),
        (cx-22, y+128, 44, 20, "Aprobada?", (243,156,18), "diamond"),
        (cx-35, y+156, 70, 10, "Estado bien: DESINCORPORADO", (231,76,60), "rect"),
        (cx-30, y+172, 60, 10, "Registrar en historial", (46,204,113), "round"),
    ]

    for s in steps2:
        pdf.nodo(*s)

    for i in range(len(steps2)-1):
        s1, s2 = steps2[i], steps2[i+1]
        pdf.flecha(cx, s1[1]+s1[3], cx, s2[1])

    # Labels
    pdf.set_font("Helvetica","B",6)
    pdf.set_text_color(46,204,113)
    pdf.set_xy(cx+24, y+74); pdf.cell(10,4,"Si")
    pdf.set_xy(cx+24, y+136); pdf.cell(10,4,"Si")

    pdf.set_text_color(231,76,60)
    pdf.set_draw_color(231,76,60)
    pdf.line(cx-22, y+76, cx-50, y+76)
    pdf.line(cx-50, y+76, cx-50, y+37)
    pdf.set_font("Helvetica","B",6)
    pdf.set_xy(cx-75, y+73); pdf.cell(22,4,"No: Corregir")

    pdf.line(cx+22, y+138, cx+50, y+138)
    pdf.set_xy(cx+52, y+135); pdf.cell(22,4,"No: Rechazada")

    pdf.ln(y+190 - pdf.get_y())

    # FLUJO 3: GENERACION DE REPORTES
    pdf.add_page()
    pdf.titulo("3. Flujo: Generacion de Reportes BM")
    pdf.txt("Proceso de generacion automatica de los formularios BM-1 a BM-4 para la Memoria y Cuenta.")
    y = pdf.get_y() + 4

    steps3 = [
        (cx-30, y, 60, 10, "Usuario solicita reporte", (46,204,113), "round"),
        (cx-35, y+16, 70, 10, "Seleccionar tipo (BM-1 a BM-4)", (74,144,226), "rect"),
        (cx-35, y+32, 70, 10, "Seleccionar filtros (sede, fecha)", (74,144,226), "rect"),
        (cx-35, y+48, 70, 10, "Sistema consulta MongoDB", (76,175,80), "rect"),
        (cx-35, y+64, 70, 10, "Procesar y agregar datos", (155,89,182), "rect"),
        (cx-22, y+82, 44, 20, "Es BM-4?", (243,156,18), "diamond"),
        (cx-35, y+110, 70, 10, "Generar documento PDF", (231,76,60), "rect"),
        (cx-30, y+126, 60, 10, "Descargar reporte", (46,204,113), "round"),
    ]

    for s in steps3:
        pdf.nodo(*s)
    for i in range(len(steps3)-1):
        s1, s2 = steps3[i], steps3[i+1]
        pdf.flecha(cx, s1[1]+s1[3], cx, s2[1])

    # BM-4 special path
    pdf.set_font("Helvetica","B",6)
    pdf.set_text_color(155,89,182)
    pdf.set_draw_color(155,89,182); pdf.set_line_width(0.3)
    pdf.line(cx+22, y+92, cx+55, y+92)
    pdf.nodo(cx+55, y+85, 50, 14, "IA genera narrativa\npara Memoria y Cuenta", (155,89,182), "rect")
    pdf.line(cx+80, y+99, cx+80, y+115)
    pdf.line(cx+80, y+115, cx+35, y+115)
    pdf.set_text_color(46,204,113)
    pdf.set_xy(cx+24, y+100); pdf.cell(10,4,"No")
    pdf.set_text_color(155,89,182)
    pdf.set_xy(cx+24, y+88); pdf.cell(10,4,"Si")

    pdf.ln(y+145 - pdf.get_y())

    # FLUJO 4: MOVIMIENTO
    pdf.add_page()
    pdf.titulo("4. Flujo: Movimiento/Traslado de Bien")
    pdf.txt("Proceso de traslado de un bien entre sedes de la UNEG.")
    y = pdf.get_y() + 4

    steps4 = [
        (cx-30, y, 60, 10, "Solicitud de traslado", (46,204,113), "round"),
        (cx-35, y+16, 70, 10, "Seleccionar bien a trasladar", (74,144,226), "rect"),
        (cx-35, y+32, 70, 10, "Seleccionar sede destino", (74,144,226), "rect"),
        (cx-35, y+48, 70, 10, "Ingresar motivo y autorizacion", (74,144,226), "rect"),
        (cx-35, y+64, 70, 10, "Registrar movimiento en BD", (76,175,80), "rect"),
        (cx-35, y+80, 70, 10, "Actualizar sede del bien", (76,175,80), "rect"),
        (cx-30, y+96, 60, 10, "Traslado completado", (46,204,113), "round"),
    ]

    for s in steps4:
        pdf.nodo(*s)
    for i in range(len(steps4)-1):
        s1, s2 = steps4[i], steps4[i+1]
        pdf.flecha(cx, s1[1]+s1[3], cx, s2[1])

    out = "docs/04_Flujos_Procesos.pdf"
    pdf.output(out)
    print(f"Generado: {out}")

if __name__ == "__main__":
    generar()
