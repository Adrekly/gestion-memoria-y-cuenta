"""Genera PDF 1: Documento Principal del Proyecto."""
from fpdf import FPDF

class DocPDF(FPDF):
    PRIMARY = (0, 51, 102)
    SECONDARY = (196, 163, 90)
    DARK = (33, 37, 41)
    LIGHT_BG = (245, 247, 250)
    WHITE = (255, 255, 255)

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.PRIMARY)
        self.cell(0, 6, "UNEG - Sistema de Gestion de Memoria y Cuenta", align="L")
        self.cell(0, 6, "Documento Tecnico", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.SECONDARY)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def titulo_seccion(self, txt):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*self.PRIMARY)
        self.cell(0, 12, txt, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.SECONDARY)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(6)

    def subtitulo(self, txt):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*self.PRIMARY)
        self.cell(0, 10, txt, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def parrafo(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.5, txt)
        self.ln(3)

    def bullet(self, txt):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.DARK)
        x0 = self.get_x()
        self.cell(6, 5.5, "-")
        self.multi_cell(174, 5.5, txt)
        self.set_x(x0)

    def caja_info(self, titulo, contenido):
        self.set_fill_color(*self.LIGHT_BG)
        self.set_draw_color(*self.PRIMARY)
        y0 = self.get_y()
        self.rect(10, y0, 190, 6, style="")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.WHITE)
        self.set_fill_color(*self.PRIMARY)
        self.cell(190, 6, f"  {titulo}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_fill_color(*self.LIGHT_BG)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        self.multi_cell(190, 5, contenido, fill=True)
        self.ln(4)

    def tabla(self, encabezados, filas, anchos=None):
        if not anchos:
            anchos = [190 // len(encabezados)] * len(encabezados)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*self.PRIMARY)
        self.set_text_color(*self.WHITE)
        for i, h in enumerate(encabezados):
            self.cell(anchos[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.DARK)
        fill = False
        for fila in filas:
            if self.get_y() > 260:
                self.add_page()
            if fill:
                self.set_fill_color(235, 240, 248)
            else:
                self.set_fill_color(*self.WHITE)
            for i, c in enumerate(fila):
                self.cell(anchos[i], 6, str(c), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(4)


def generar():
    pdf = DocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # === PORTADA ===
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*DocPDF.PRIMARY)
    pdf.cell(0, 14, "Sistema de Gestion de", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "Memoria y Cuenta", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_draw_color(*DocPDF.SECONDARY)
    pdf.set_line_width(1.2)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(*DocPDF.DARK)
    pdf.cell(0, 8, "Universidad Nacional Experimental de Guayana", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Departamento de Bienes Publicos", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "Alineado con la Ley Organica de Bienes Publicos", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "y normativas de la SUDEBIP", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Fecha: Abril 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Version: 1.0", align="C", new_x="LMARGIN", new_y="NEXT")

    # === INDICE ===
    pdf.add_page()
    pdf.titulo_seccion("Indice de Contenido")
    items = [
        "1. Introduccion y Justificacion",
        "2. Objetivo General y Especificos",
        "3. Alcance del Sistema",
        "4. Marco Legal y Normativo",
        "5. Descripcion Funcional",
        "6. Stack Tecnologico",
        "7. Sedes de la UNEG",
        "8. Formularios BM (SUDEBIP)",
        "9. Modulos del Sistema",
        "10. Clasificador Unico de Bienes",
        "11. Integracion con Inteligencia Artificial",
        "12. Resumen Ejecutivo",
    ]
    for item in items:
        pdf.bullet(item)

    # === 1. INTRODUCCION ===
    pdf.add_page()
    pdf.titulo_seccion("1. Introduccion y Justificacion")
    pdf.parrafo(
        "La Universidad Nacional Experimental de Guayana (UNEG) cuenta con multiples "
        "sedes distribuidas en el estado Bolivar, cada una con un inventario significativo "
        "de bienes muebles e inmuebles que requieren gestion, control y reporte conforme "
        "a la legislacion venezolana vigente."
    )
    pdf.parrafo(
        "Actualmente, el Departamento de Bienes Publicos de la UNEG enfrenta desafios "
        "en la administracion de activos: registros manuales propensos a errores, "
        "dificultad para generar los reportes exigidos por la SUDEBIP (Superintendencia "
        "de Bienes Publicos), y falta de trazabilidad en los movimientos de bienes "
        "entre sedes."
    )
    pdf.parrafo(
        "El presente sistema propone una solucion tecnologica integral que automatiza "
        "la gestion de activos, garantiza el cumplimiento normativo mediante validacion "
        "inteligente de datos, y genera automaticamente los formularios BM-1 a BM-4 "
        "requeridos para la Memoria y Cuenta institucional."
    )
    pdf.caja_info("Problema Identificado",
        "Los procesos manuales de gestion de bienes generan:\n"
        "- Inconsistencias en la codificacion SUDEBIP\n"
        "- Retrasos en la generacion de reportes BM\n"
        "- Falta de trazabilidad en movimientos entre sedes\n"
        "- Riesgo de incumplimiento legal en desincorporaciones")

    # === 2. OBJETIVOS ===
    pdf.add_page()
    pdf.titulo_seccion("2. Objetivo General y Especificos")
    pdf.subtitulo("Objetivo General")
    pdf.parrafo(
        "Desarrollar un sistema informatico para la gestion integral de activos de la "
        "UNEG, alineado con la Ley Organica de Bienes Publicos y las normativas de la "
        "SUDEBIP, que automatice el registro, control, movimiento y desincorporacion "
        "de bienes, asi como la generacion de los formularios legales para la Memoria y Cuenta."
    )
    pdf.subtitulo("Objetivos Especificos")
    objs = [
        "Implementar un modulo de registro de bienes con validacion automatica del Clasificador Unico de Bienes de la SUDEBIP.",
        "Desarrollar el seguimiento de movimientos de bienes entre sedes (entradas, salidas, traslados, reasignaciones).",
        "Crear un flujo de desincorporacion que exija justificacion tecnica validada por inteligencia artificial.",
        "Automatizar la generacion de los formularios BM-1 (Inventario), BM-2 (Movimientos), BM-3 (Faltantes) y BM-4 (Resumen).",
        "Integrar un asistente virtual basado en IA (Gemma) para consultas de inventario en lenguaje natural.",
        "Garantizar la soberania de datos mediante ejecucion local del modelo de IA con Ollama.",
    ]
    for o in objs:
        pdf.bullet(o)

    # === 3. ALCANCE ===
    pdf.add_page()
    pdf.titulo_seccion("3. Alcance del Sistema")
    pdf.subtitulo("Incluido en el alcance")
    inc = [
        "Gestion CRUD de bienes muebles en todas las sedes de la UNEG.",
        "Clasificacion automatica segun catalogo SUDEBIP.",
        "Registro y auditoria de movimientos de bienes.",
        "Flujo de desincorporacion con validacion normativa.",
        "Generacion de reportes BM-1 a BM-4 en formato PDF.",
        "Asistente virtual IA para consultas de inventario.",
        "Dashboard con indicadores clave por sede y estado.",
    ]
    for i in inc:
        pdf.bullet(i)
    pdf.ln(4)
    pdf.subtitulo("Excluido del alcance (Version 1.0)")
    exc = [
        "Autenticacion y gestion de roles de usuario.",
        "Computer Vision / OCR para lectura de etiquetas de bienes.",
        "Gestion de bienes inmuebles.",
        "Integracion con sistemas financieros externos.",
    ]
    for e in exc:
        pdf.bullet(e)

    # === 4. MARCO LEGAL ===
    pdf.add_page()
    pdf.titulo_seccion("4. Marco Legal y Normativo")
    pdf.parrafo(
        "El sistema se fundamenta en el siguiente marco juridico venezolano:"
    )
    pdf.caja_info("Ley Organica de Bienes Publicos (Gaceta Oficial N. 6.155, 2014)",
        "Establece los principios, normas y procedimientos para la administracion, "
        "registro, control y disposicion de los bienes publicos. Define las categorias "
        "de bienes (muebles, inmuebles, intangibles) y los procedimientos para su "
        "incorporacion y desincorporacion.")
    pdf.caja_info("SUDEBIP - Superintendencia de Bienes Publicos",
        "Organo rector en materia de bienes publicos en Venezuela. Establece:\n"
        "- El Clasificador Unico de Bienes (codificacion obligatoria)\n"
        "- Los formularios BM-1 a BM-4 para reportes de inventario\n"
        "- Los procedimientos de desincorporacion y baja de bienes\n"
        "- Las normas de marcaje e identificacion de activos")
    pdf.caja_info("Cumplimiento del Sistema",
        "El sistema actua como filtro de cumplimiento legal:\n"
        "- Usa Pydantic para forzar que cada entrada respete la codificacion SUDEBIP\n"
        "- Emplea IA para validar justificaciones de desincorporacion\n"
        "- Genera automaticamente los reportes en los formatos BM exigidos\n"
        "- Mantiene trazabilidad completa de cada bien desde su registro hasta su baja")

    # === 5. DESCRIPCION FUNCIONAL ===
    pdf.add_page()
    pdf.titulo_seccion("5. Descripcion Funcional")
    pdf.parrafo(
        "El sistema se organiza en modulos funcionales que cubren el ciclo de vida "
        "completo de un bien publico dentro de la UNEG:"
    )
    pdf.subtitulo("Ciclo de vida de un bien")
    pdf.parrafo("Registro -> Clasificacion SUDEBIP -> Uso -> Movimiento/Traslado -> Desuso -> Desincorporacion")
    pdf.ln(2)
    pdf.subtitulo("Flujo operativo")
    pdf.parrafo(
        "1. ENTRADA: El operador registra un bien nuevo. El sistema valida la descripcion "
        "contra el Clasificador SUDEBIP y asigna automaticamente el codigo correspondiente.\n\n"
        "2. PROCESAMIENTO: El sistema mantiene auditoria de estados (En Uso, En Desuso, "
        "Inservible, En Reparacion) segun la normativa vigente.\n\n"
        "3. MOVIMIENTO: Cada traslado entre sedes queda registrado con fecha, motivo, "
        "origen, destino y autorizacion.\n\n"
        "4. DESINCORPORACION: Requiere justificacion tecnica que es analizada por la IA "
        "antes de proceder. El bien no se elimina, solo cambia de estado.\n\n"
        "5. SALIDA: Generacion automatica de reportes BM-1 a BM-4 para la Memoria y Cuenta."
    )

    # === 6. STACK TECNOLOGICO ===
    pdf.add_page()
    pdf.titulo_seccion("6. Stack Tecnologico")
    pdf.tabla(
        ["Componente", "Tecnologia", "Justificacion"],
        [
            ["Backend", "Python + FastAPI", "Alto rendimiento, async, auto-docs"],
            ["Validacion", "Pydantic v2", "Validacion estricta de datos"],
            ["Base de Datos", "MongoDB", "Flexibilidad documental"],
            ["Driver BD", "Motor (async)", "Operaciones no bloqueantes"],
            ["Frontend", "React 19 + Vite", "UI reactiva y moderna"],
            ["Estilos", "Tailwind CSS v4", "Desarrollo rapido de UI"],
            ["IA Local", "Ollama + Gemma:7b", "Soberania de datos"],
            ["Orquestacion IA", "LangChain", "Gestion de prompts"],
            ["Reportes", "fpdf2 / openpyxl", "Generacion PDF/Excel"],
            ["Contenedores", "Docker Compose", "Portabilidad total"],
        ],
        [40, 45, 105],
    )
    pdf.caja_info("Soberania de Datos",
        "El modelo de IA Gemma:7b se ejecuta localmente mediante Ollama. "
        "Ningun dato institucional sale de la infraestructura de la UNEG. "
        "Esto cumple con las politicas de privacidad de datos publicos.")

    # === 7. SEDES ===
    pdf.add_page()
    pdf.titulo_seccion("7. Sedes de la UNEG")
    pdf.parrafo("El sistema gestiona bienes en las siguientes sedes universitarias:")
    pdf.tabla(
        ["Codigo", "Sede", "Ciudad", "Estado"],
        [
            ["ATL", "Ciudad Universitaria (Atlantico)", "Ciudad Guayana", "Activa"],
            ["VAS", "Villa Asia", "Ciudad Guayana", "Activa"],
            ["CHI", "Chilemex", "Ciudad Guayana", "Activa"],
            ["JBO", "Jardin Botanico", "Ciudad Bolivar", "Activa"],
            ["CDV", "Casa de las Doce Ventanas", "Ciudad Bolivar", "Activa"],
            ["UPA", "Sede Upata", "Upata", "Activa"],
            ["CAL", "Sede El Callao", "El Callao", "Activa"],
            ["SEU", "Santa Elena de Uairen", "Sta. Elena", "Activa"],
        ],
        [25, 75, 50, 40],
    )

    # === 8. FORMULARIOS BM ===
    pdf.add_page()
    pdf.titulo_seccion("8. Formularios BM (SUDEBIP)")
    pdf.parrafo(
        "La SUDEBIP exige formatos especificos para la gestion de bienes. "
        "El sistema genera estos reportes automaticamente:"
    )
    pdf.tabla(
        ["Formulario", "Nombre", "Funcion"],
        [
            ["BM-1", "Inventario de Bienes", "Foto actual de todos los bienes de la UNEG"],
            ["BM-2", "Movimiento de Bienes", "Registro mensual de entradas y salidas"],
            ["BM-3", "Relacion de Bienes Faltantes", "Reporte de bienes extraviados o robados"],
            ["BM-4", "Resumen del Movimiento", "Insumo principal para la Memoria y Cuenta"],
        ],
        [30, 60, 100],
    )
    pdf.ln(2)
    for fm, desc in [
        ("BM-1: Inventario de Bienes",
         "Fuente: Coleccion 'bienes' (estado actual)\n"
         "Contenido: Codigo inventario, codigo SUDEBIP, descripcion, sede, estado, "
         "condicion, valor, responsable.\n"
         "Formato: PDF/Excel con filtros por sede, grupo SUDEBIP, estado."),
        ("BM-2: Movimiento de Bienes",
         "Fuente: Coleccion 'movimientos' (filtro por periodo)\n"
         "Contenido: Bien, tipo de movimiento, fecha, sede origen/destino, motivo.\n"
         "Formato: PDF/Excel con resumen mensual."),
        ("BM-3: Relacion de Bienes Faltantes",
         "Fuente: Coleccion 'bienes' (estado = FALTANTE)\n"
         "Contenido: Bienes reportados como extraviados, robados o no localizados.\n"
         "Formato: PDF con fecha de reporte, ultimo responsable conocido."),
        ("BM-4: Resumen del Movimiento",
         "Fuente: Agregacion de movimientos + desincorporaciones\n"
         "Contenido: Resumen estadistico + narrativa generada por IA.\n"
         "Formato: PDF listo para incluir en la Memoria y Cuenta."),
    ]:
        pdf.caja_info(fm, desc)

    # === 9. MODULOS ===
    pdf.add_page()
    pdf.titulo_seccion("9. Modulos del Sistema")
    for mod, desc in [
        ("Modulo de Registro de Bienes",
         "CRUD completo con validacion SUDEBIP automatica. Genera codigo de inventario "
         "unico por sede. Campos: descripcion, marca, modelo, serial, valor, fecha, "
         "sede, ubicacion, responsable, estado, condicion."),
        ("Modulo de Movimientos",
         "Registro de entradas, salidas, traslados entre sedes y reasignaciones. "
         "Cada movimiento requiere motivo, autorizacion y documento soporte."),
        ("Modulo de Desincorporacion",
         "Flujo de solicitud -> revision IA -> aprobacion. Motivos: obsolescencia, "
         "inservibilidad, hurto/robo, siniestro, donacion. El bien no se elimina."),
        ("Modulo de Reportes BM",
         "Generacion automatica de formularios BM-1 a BM-4 en PDF. "
         "Filtros por sede, periodo, grupo SUDEBIP."),
        ("Modulo de Clasificador SUDEBIP",
         "Busqueda y asignacion de codigos del Clasificador Unico de Bienes. "
         "Busqueda por palabras clave con sugerencias de IA."),
        ("Modulo de Asistente IA",
         "Chat con Gemma:7b para consultas en lenguaje natural. "
         "Contexto dinamico desde MongoDB. Ejecucion 100% local."),
        ("Dashboard",
         "Panel con KPIs: total de bienes, distribucion por sede, por estado, "
         "por grupo SUDEBIP. Graficos interactivos con Recharts."),
    ]:
        pdf.caja_info(mod, desc)

    # === 10. CLASIFICADOR ===
    pdf.add_page()
    pdf.titulo_seccion("10. Clasificador Unico de Bienes")
    pdf.parrafo(
        "El Clasificador Unico de Bienes de la SUDEBIP es un catalogo oficial donde "
        "cada tipo de bien tiene un codigo jerarquico. El sistema valida que cada bien "
        "registrado tenga un codigo valido del clasificador."
    )
    pdf.subtitulo("Estructura del Codigo")
    pdf.parrafo("Formato: G.SG.SC.CA  (Grupo.Subgrupo.Seccion.Categoria)")
    pdf.tabla(
        ["Nivel", "Ejemplo", "Descripcion"],
        [
            ["Grupo (G)", "1", "Bienes Muebles"],
            ["Subgrupo (SG)", "1.02", "Mobiliario y Equipos de Oficina"],
            ["Seccion (SC)", "1.02.01", "Mobiliario de Oficina"],
            ["Categoria (CA)", "1.02.01.01", "Escritorios"],
        ],
        [40, 40, 110],
    )
    pdf.subtitulo("Grupos Principales")
    pdf.tabla(
        ["Codigo", "Grupo"],
        [
            ["1", "Bienes Muebles"],
            ["1.01", "Maquinaria y Equipos"],
            ["1.02", "Mobiliario y Equipos de Oficina"],
            ["1.03", "Equipos de Computacion"],
            ["1.04", "Equipos de Comunicacion"],
            ["1.05", "Equipos Medicos"],
            ["1.06", "Equipos de Transporte"],
            ["1.07", "Herramientas y Repuestos"],
            ["1.08", "Otros Bienes Muebles"],
        ],
        [30, 160],
    )

    # === 11. IA ===
    pdf.add_page()
    pdf.titulo_seccion("11. Integracion con Inteligencia Artificial")
    pdf.parrafo(
        "El sistema integra el modelo de IA Gemma:7b ejecutado localmente "
        "mediante Ollama para las siguientes funcionalidades:"
    )
    for func, desc in [
        ("Clasificacion Automatica SUDEBIP",
         "Al registrar un bien, la IA analiza la descripcion y sugiere el codigo "
         "del Clasificador Unico de Bienes correspondiente. Esto reduce errores "
         "humanos en la codificacion."),
        ("Validacion de Desincorporaciones",
         "La IA analiza la justificacion tecnica de una solicitud de baja y evalua "
         "si cumple con los criterios legales establecidos en la Ley Organica de "
         "Bienes Publicos."),
        ("Generacion de Narrativa (Memoria y Cuenta)",
         "Para el formulario BM-4, la IA genera texto descriptivo que resume los "
         "movimientos del periodo, listo para incluir en la Memoria y Cuenta."),
        ("Asistente de Consulta",
         "Chat en lenguaje natural para que el personal administrativo consulte "
         "el inventario sin necesidad de conocer la interfaz tecnica."),
    ]:
        pdf.caja_info(func, desc)

    # === 12. RESUMEN ===
    pdf.add_page()
    pdf.titulo_seccion("12. Resumen Ejecutivo")
    pdf.caja_info("Propuesta de Valor",
        "El sistema no es solo un software de gestion. Actua como un filtro de "
        "cumplimiento legal que:\n"
        "- Utiliza Pydantic para forzar la codificacion SUDEBIP\n"
        "- Emplea IA para asegurar que los reportes BM sean correctos\n"
        "- Automatiza la generacion de la Memoria y Cuenta\n"
        "- Garantiza soberania de datos con ejecucion 100% local")
    pdf.parrafo(
        "Este proyecto resuelve un problema burocratico real de la universidad, "
        "aportando valor institucional al Departamento de Bienes Publicos de la UNEG."
    )

    out = "docs/01_Documento_Principal_Proyecto.pdf"
    pdf.output(out)
    print(f"Generado: {out}")

if __name__ == "__main__":
    generar()
