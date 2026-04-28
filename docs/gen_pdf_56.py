"""Genera PDF 5: Casos de Uso y PDF 6: Marco Legal."""
from fpdf import FPDF

class DocPDF(FPDF):
    P=(0,51,102); S=(196,163,90); D=(33,37,41); W=(255,255,255); LB=(245,247,250)

    def header(self):
        self.set_font("Helvetica","B",9); self.set_text_color(*self.P)
        self.cell(0,6,"UNEG - Documentacion del Sistema",align="L")
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

    def sub(self,t):
        self.set_font("Helvetica","B",13); self.set_text_color(*self.P)
        self.cell(0,10,t,new_x="LMARGIN",new_y="NEXT"); self.ln(2)

    def txt(self,t):
        self.set_font("Helvetica","",10); self.set_text_color(*self.D)
        self.multi_cell(0,5.5,t); self.ln(3)

    def caja(self,titulo,contenido):
        self.set_fill_color(*self.P); self.set_font("Helvetica","B",10); self.set_text_color(*self.W)
        self.cell(190,6,f"  {titulo}",fill=True,new_x="LMARGIN",new_y="NEXT")
        self.set_fill_color(*self.LB); self.set_font("Helvetica","",9); self.set_text_color(*self.D)
        self.multi_cell(190,5,contenido,fill=True); self.ln(4)

    def bullet(self,t):
        self.set_font("Helvetica","",10); self.set_text_color(*self.D)
        x0=self.get_x(); self.cell(6,5.5,"-"); self.multi_cell(174,5.5,t); self.set_x(x0)

    def tabla(self,h,rows,w=None):
        if not w: w=[190//len(h)]*len(h)
        self.set_font("Helvetica","B",8); self.set_fill_color(*self.P); self.set_text_color(*self.W)
        for i,hh in enumerate(h): self.cell(w[i],7,hh,border=1,fill=True,align="C")
        self.ln(); f=False
        for r in rows:
            if self.get_y()>260: self.add_page()
            self.set_font("Helvetica","",7); self.set_text_color(*self.D)
            self.set_fill_color(235,240,248) if f else self.set_fill_color(*self.W)
            for i,c in enumerate(r): self.cell(w[i],5.5,str(c),border=1,fill=True)
            self.ln(); f=not f
        self.ln(4)


def gen_casos_uso():
    pdf = DocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # PORTADA
    pdf.add_page(); pdf.ln(50)
    pdf.set_font("Helvetica","B",26); pdf.set_text_color(*DocPDF.P)
    pdf.cell(0,14,"Casos de Uso",align="C",new_x="LMARGIN",new_y="NEXT"); pdf.ln(4)
    pdf.set_draw_color(*DocPDF.S); pdf.set_line_width(1.2)
    pdf.line(60,pdf.get_y(),150,pdf.get_y()); pdf.ln(8)
    pdf.set_font("Helvetica","",13); pdf.set_text_color(*DocPDF.D)
    pdf.cell(0,8,"Especificacion de Casos de Uso del Sistema",align="C",new_x="LMARGIN",new_y="NEXT")

    # ACTORES
    pdf.add_page()
    pdf.titulo("1. Actores del Sistema")
    pdf.tabla(["Actor","Descripcion","Permisos"],[
        ["Operador","Personal de Bienes Nacionales","Registrar, consultar, mover bienes"],
        ["Supervisor","Jefe del Departamento","Aprobar desincorporaciones, reportes"],
        ["Asistente IA","Modelo Gemma:7b","Clasificar, validar, generar narrativa"],
    ],[40,75,75])

    # DIAGRAMA DE CASOS DE USO (visual)
    pdf.ln(2)
    pdf.sub("Diagrama de Casos de Uso")
    y0 = pdf.get_y() + 2

    # Actores (stickman simplified as boxes)
    actors = [
        ("Operador", 15, y0+20, (74,144,226)),
        ("Supervisor", 15, y0+65, (231,76,60)),
        ("IA", 170, y0+40, (155,89,182)),
    ]
    for name, x, y, color in actors:
        pdf.set_fill_color(*color)
        pdf.set_draw_color(max(0,color[0]-40),max(0,color[1]-40),max(0,color[2]-40))
        pdf.rect(x, y, 25, 12, style="DF")
        pdf.set_font("Helvetica","B",7); pdf.set_text_color(*DocPDF.W)
        pdf.set_xy(x, y+2); pdf.cell(25, 8, name, align="C")

    # Use cases (ellipses as rounded rects)
    cases = [
        ("CU-01: Registrar Bien", 60, y0+2),
        ("CU-02: Consultar Inventario", 60, y0+14),
        ("CU-03: Registrar Movimiento", 60, y0+26),
        ("CU-04: Solicitar Desincorporacion", 60, y0+38),
        ("CU-05: Aprobar Desincorporacion", 60, y0+50),
        ("CU-06: Generar Reporte BM", 60, y0+62),
        ("CU-07: Consultar via Chat IA", 60, y0+74),
        ("CU-08: Clasificar Bien SUDEBIP", 115, y0+26),
        ("CU-09: Validar Desincorporacion", 115, y0+50),
    ]
    for name, x, y in cases:
        pdf.set_fill_color(230,240,255)
        pdf.set_draw_color(*DocPDF.P)
        pdf.rect(x, y, 50, 10, style="DF")
        pdf.set_font("Helvetica","",5.5); pdf.set_text_color(*DocPDF.D)
        pdf.set_xy(x, y+1); pdf.cell(50, 8, name, align="C")

    # Lines from actors to cases
    pdf.set_draw_color(180,180,180); pdf.set_line_width(0.2)
    # Operador -> CU1-4,6,7
    for i in [0,1,2,3,5,6]:
        pdf.line(40, actors[0][2]+6, cases[i][1], cases[i][2]+5)
    # Supervisor -> CU2,5,6
    for i in [1,4,5]:
        pdf.line(40, actors[1][2]+6, cases[i][1], cases[i][2]+5)
    # IA -> CU8,9
    for i in [7,8]:
        pdf.line(170, actors[2][2]+6, cases[i][1]+50, cases[i][2]+5)

    pdf.ln(y0+92 - pdf.get_y())

    # DETAILED USE CASES
    pdf.add_page()
    pdf.titulo("2. Especificacion Detallada de Casos de Uso")

    use_cases = [
        ("CU-01: Registrar Bien",
         "Operador", "El operador necesita incorporar un nuevo bien al inventario",
         "1. El operador abre el formulario de registro\n"
         "2. Ingresa descripcion, marca, modelo, serial, valor, fecha\n"
         "3. Selecciona la sede y ubicacion especifica\n"
         "4. El sistema busca el codigo SUDEBIP automaticamente (CU-08)\n"
         "5. El operador confirma o ajusta el codigo\n"
         "6. El sistema valida todos los campos con Pydantic\n"
         "7. Se genera el codigo de inventario unico\n"
         "8. El bien queda registrado con estado EN_USO",
         "El bien es visible en el inventario y en futuros reportes BM-1"),
        ("CU-02: Consultar Inventario",
         "Operador / Supervisor", "Necesita buscar o filtrar bienes existentes",
         "1. El usuario accede al modulo de inventario\n"
         "2. Aplica filtros (sede, estado, grupo SUDEBIP, busqueda)\n"
         "3. El sistema muestra resultados paginados\n"
         "4. El usuario puede ver el detalle de cada bien",
         "El usuario obtiene la informacion solicitada"),
        ("CU-03: Registrar Movimiento",
         "Operador", "Un bien debe ser trasladado entre sedes",
         "1. El operador selecciona el bien a mover\n"
         "2. Selecciona tipo: traslado, reasignacion, entrada, salida\n"
         "3. Indica sede destino y motivo\n"
         "4. Adjunta documento soporte (numero de oficio)\n"
         "5. El sistema registra el movimiento\n"
         "6. Actualiza la ubicacion del bien automaticamente",
         "Movimiento registrado, visible en reportes BM-2"),
        ("CU-04: Solicitar Desincorporacion",
         "Operador", "Un bien debe ser dado de baja del inventario",
         "1. El operador selecciona el bien\n"
         "2. Selecciona motivo: obsolescencia, inservibilidad, hurto, etc.\n"
         "3. Escribe justificacion tecnica detallada\n"
         "4. La IA analiza la justificacion (CU-09)\n"
         "5. Si cumple criterios, pasa a estado EN_REVISION\n"
         "6. Si no cumple, muestra observaciones para corregir",
         "Solicitud creada en estado EN_REVISION o corregida"),
        ("CU-05: Aprobar Desincorporacion",
         "Supervisor", "Autorizar la baja definitiva de un bien",
         "1. El supervisor ve las solicitudes EN_REVISION\n"
         "2. Revisa justificacion y validacion de IA\n"
         "3. Aprueba o rechaza la solicitud\n"
         "4. Si aprueba, el bien pasa a DESINCORPORADO\n"
         "5. Se registra en el historial",
         "Bien desincorporado o solicitud rechazada"),
        ("CU-06: Generar Reporte BM",
         "Operador / Supervisor", "Generar formularios legales para SUDEBIP",
         "1. El usuario selecciona el tipo de reporte (BM-1 a BM-4)\n"
         "2. Aplica filtros de sede y periodo\n"
         "3. El sistema consulta MongoDB y agrega datos\n"
         "4. Para BM-4, la IA genera narrativa adicional\n"
         "5. Se genera el PDF con formato oficial\n"
         "6. El usuario descarga el reporte",
         "Reporte PDF generado y listo para la Memoria y Cuenta"),
    ]

    for cu_name, actor, pre, steps, post in use_cases:
        if pdf.get_y() > 200: pdf.add_page()
        pdf.sub(cu_name)
        pdf.caja("Actor(es)", actor)
        pdf.caja("Precondicion", pre)
        pdf.caja("Flujo Principal", steps)
        pdf.caja("Postcondicion", post)
        pdf.ln(4)

    out = "docs/05_Casos_de_Uso.pdf"
    pdf.output(out)
    print(f"Generado: {out}")


def gen_marco_legal():
    pdf = DocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # PORTADA
    pdf.add_page(); pdf.ln(50)
    pdf.set_font("Helvetica","B",26); pdf.set_text_color(*DocPDF.P)
    pdf.cell(0,14,"Marco Legal y Normativo",align="C",new_x="LMARGIN",new_y="NEXT"); pdf.ln(4)
    pdf.set_draw_color(*DocPDF.S); pdf.set_line_width(1.2)
    pdf.line(60,pdf.get_y(),150,pdf.get_y()); pdf.ln(8)
    pdf.set_font("Helvetica","",13); pdf.set_text_color(*DocPDF.D)
    pdf.cell(0,8,"Fundamentacion legal del sistema",align="C",new_x="LMARGIN",new_y="NEXT")
    pdf.cell(0,8,"segun la legislacion venezolana vigente",align="C",new_x="LMARGIN",new_y="NEXT")

    # LEY ORGANICA
    pdf.add_page()
    pdf.titulo("1. Ley Organica de Bienes Publicos")
    pdf.txt("Publicada en Gaceta Oficial N. 6.155 Extraordinario del 19 de noviembre de 2014. "
            "Esta ley establece los principios, normas y procedimientos que regulan la "
            "administracion, registro, control y disposicion de los bienes publicos.")

    pdf.sub("Principios Fundamentales")
    for p in [
        "Registro y Control: Todo bien publico debe estar debidamente registrado en inventarios actualizados.",
        "Transparencia: La informacion sobre bienes publicos debe ser accesible y verificable.",
        "Responsabilidad: Cada bien debe tener un custodio responsable identificado.",
        "Conservacion: Los bienes deben mantenerse en condiciones optimas de funcionamiento.",
        "Eficiencia: Los bienes deben utilizarse de manera eficiente y racional.",
    ]:
        pdf.bullet(p)

    pdf.ln(4)
    pdf.sub("Clasificacion de Bienes Publicos")
    pdf.tabla(["Categoria","Descripcion","Ejemplo en UNEG"],[
        ["Bienes Muebles","Objetos movibles","Computadoras, escritorios, proyectores"],
        ["Bienes Inmuebles","Edificaciones y terrenos","Sedes, laboratorios, auditorios"],
        ["Bienes Intangibles","Propiedad intelectual","Software, licencias, patentes"],
    ],[45,70,75])

    pdf.sub("Articulos Relevantes para el Sistema")
    arts = [
        ("Art. 20-25: Del Registro de Bienes",
         "Establece la obligatoriedad de mantener un registro actualizado de todos "
         "los bienes. El sistema automatiza este registro con validacion SUDEBIP."),
        ("Art. 30-35: Del Control y Custodia",
         "Cada bien debe tener un responsable asignado. El sistema registra "
         "cedula y nombre del custodio para cada activo."),
        ("Art. 40-50: De la Desincorporacion",
         "Define los procedimientos y causales para dar de baja un bien. "
         "El sistema implementa estos flujos con validacion de IA."),
        ("Art. 55-60: De los Inventarios",
         "Exige inventarios periodicos con formatos especificos. "
         "El sistema genera automaticamente los formularios BM requeridos."),
    ]
    for titulo, desc in arts:
        pdf.caja(titulo, desc)

    # SUDEBIP
    pdf.add_page()
    pdf.titulo("2. SUDEBIP")
    pdf.txt("La Superintendencia de Bienes Publicos (SUDEBIP) es el organo rector en materia "
            "de bienes publicos en Venezuela. Adscrita al Ministerio del Poder Popular de "
            "Economia, Finanzas y Comercio Exterior.")

    pdf.sub("Funciones principales")
    for f in [
        "Regular, supervisar y administrar los bienes publicos del Estado.",
        "Establecer y mantener el Clasificador Unico de Bienes.",
        "Definir los formatos oficiales para reportes de inventario (BM-1 a BM-4).",
        "Fiscalizar el cumplimiento de la Ley de Bienes Publicos.",
        "Autorizar procedimientos de desincorporacion.",
    ]:
        pdf.bullet(f)

    pdf.ln(4)
    pdf.sub("Clasificador Unico de Bienes")
    pdf.txt("Es el catalogo oficial donde cada tipo de bien tiene un codigo jerarquico "
            "unico. Su uso es obligatorio para todas las instituciones publicas.")
    pdf.txt("Formato del codigo: G.SG.SC.CA (Grupo.Subgrupo.Seccion.Categoria)")
    pdf.tabla(["Nivel","Ejemplo","Descripcion"],[
        ["Grupo","1","Bienes Muebles"],
        ["Subgrupo","1.02","Mobiliario y Equipos de Oficina"],
        ["Seccion","1.02.01","Mobiliario de Oficina"],
        ["Categoria","1.02.01.01","Escritorios"],
    ],[35,35,120])

    pdf.txt("Implementacion en el sistema:\n"
            "- La coleccion 'clasificador_sudebip' almacena todo el catalogo\n"
            "- Al registrar un bien, la IA sugiere el codigo basandose en la descripcion\n"
            "- Pydantic valida que el codigo sea valido antes de guardar\n"
            "- Se impide el registro de bienes sin codificacion SUDEBIP")

    # FORMULARIOS BM
    pdf.add_page()
    pdf.titulo("3. Formularios BM")
    pdf.txt("La SUDEBIP exige cuatro formularios especificos para la gestion de bienes. "
            "El sistema genera estos reportes automaticamente desde la base de datos.")

    bm_forms = [
        ("BM-1: Inventario de Bienes Muebles",
         "Proposito: Presentar una fotografia actualizada de todos los bienes muebles "
         "de la institucion en un momento dado.\n\n"
         "Contenido requerido:\n"
         "- Codigo de inventario del bien\n"
         "- Codigo SUDEBIP\n"
         "- Descripcion detallada\n"
         "- Estado y condicion\n"
         "- Valor de adquisicion\n"
         "- Ubicacion (sede, edificio, piso)\n"
         "- Responsable asignado\n\n"
         "Fuente en el sistema: Coleccion 'bienes' (todos los registros activos)\n"
         "Filtros disponibles: Por sede, por grupo SUDEBIP, por estado"),
        ("BM-2: Movimiento de Bienes",
         "Proposito: Registrar todas las entradas y salidas de bienes en un periodo "
         "determinado (generalmente mensual).\n\n"
         "Contenido requerido:\n"
         "- Tipo de movimiento (entrada, salida, traslado)\n"
         "- Bien afectado con su codigo\n"
         "- Fecha del movimiento\n"
         "- Sede origen y destino\n"
         "- Motivo del movimiento\n"
         "- Persona que autorizo\n\n"
         "Fuente en el sistema: Coleccion 'movimientos' con filtro por periodo\n"
         "Periodicidad: Mensual"),
        ("BM-3: Relacion de Bienes Faltantes",
         "Proposito: Documentar los bienes que no se localizan fisicamente, ya sea "
         "por extravio, hurto o robo. Es un reporte critico.\n\n"
         "Contenido requerido:\n"
         "- Bienes con estado FALTANTE\n"
         "- Ultima ubicacion conocida\n"
         "- Ultimo responsable\n"
         "- Fecha en que se detecto la falta\n"
         "- Acciones tomadas\n\n"
         "Fuente en el sistema: Coleccion 'bienes' filtrada por estado=FALTANTE"),
        ("BM-4: Resumen del Movimiento",
         "Proposito: Consolidar la informacion de los formularios anteriores en un "
         "resumen ejecutivo. Es el insumo principal para la Memoria y Cuenta.\n\n"
         "Contenido requerido:\n"
         "- Total de bienes por estado\n"
         "- Total de movimientos del periodo\n"
         "- Bienes incorporados vs desincorporados\n"
         "- Valor total del inventario\n"
         "- Narrativa descriptiva del periodo\n\n"
         "Fuente: Agregacion de todas las colecciones\n"
         "Valor agregado del sistema: La IA genera la narrativa automaticamente"),
    ]
    for titulo, desc in bm_forms:
        if pdf.get_y() > 140: pdf.add_page()
        pdf.caja(titulo, desc)

    # DESINCORPORACION
    pdf.add_page()
    pdf.titulo("4. Normativa de Desincorporacion")
    pdf.txt("La desincorporacion es el proceso mas sensible para la SUDEBIP. "
            "No se puede eliminar un bien del inventario sin justificacion legal. "
            "El sistema implementa controles estrictos alineados con la ley.")

    pdf.sub("Causales de Desincorporacion")
    pdf.tabla(["Causal","Descripcion","Validacion del Sistema"],[
        ["OBSOLESCENCIA","Tecnologia superada","IA verifica antiguedad y criterios"],
        ["INSERVIBILIDAD","No funcional, irreparable","Requiere informe tecnico"],
        ["HURTO/ROBO","Sustraccion del bien","Requiere denuncia policial"],
        ["SINIESTRO","Dano por evento fortuito","Requiere informe de siniestro"],
        ["DONACION","Cesion a otra entidad","Requiere acta de donacion"],
    ],[35,55,100])

    pdf.ln(2)
    pdf.sub("Controles implementados en el sistema")
    for c in [
        "Un bien no puede eliminarse de la base de datos. Solo cambia de estado a DESINCORPORADO.",
        "Toda solicitud requiere justificacion tecnica escrita.",
        "La IA analiza si la justificacion cumple con los criterios legales.",
        "Se requiere aprobacion de un supervisor para ejecutar la baja.",
        "El historial completo del bien se mantiene para auditoria.",
        "Los bienes desincorporados aparecen en los reportes BM-4.",
    ]:
        pdf.bullet(c)

    # MEMORIA Y CUENTA
    pdf.add_page()
    pdf.titulo("5. La Memoria y Cuenta")
    pdf.txt("La Memoria y Cuenta es el informe anual que toda institucion publica venezolana "
            "debe presentar. Detalla la gestion realizada durante el ejercicio fiscal, "
            "incluyendo el manejo de los bienes publicos.")

    pdf.sub("Rol del sistema en la Memoria y Cuenta")
    pdf.txt("El sistema genera automaticamente la seccion de Bienes Publicos de la "
            "Memoria y Cuenta a traves del formulario BM-4, que incluye:")
    for r in [
        "Estadisticas consolidadas del inventario por sede y grupo.",
        "Resumen de movimientos del periodo (incorporaciones, traslados, bajas).",
        "Relacion de bienes faltantes o desincorporados.",
        "Narrativa descriptiva generada por IA basada en los datos reales.",
        "Valor total del patrimonio mueble de la universidad.",
    ]:
        pdf.bullet(r)

    pdf.ln(4)
    pdf.caja("Propuesta de Valor del Sistema",
        "El sistema no es solo un software de gestion de inventario. Actua como un "
        "filtro de cumplimiento legal que:\n\n"
        "1. Utiliza Pydantic para FORZAR que cada entrada de datos respete la "
        "codificacion del Clasificador Unico de la SUDEBIP.\n\n"
        "2. Emplea inteligencia artificial para ASEGURAR que la narrativa de la "
        "Memoria y Cuenta coincida con los formatos BM exigidos.\n\n"
        "3. Automatiza la generacion de los 4 formularios BM reduciendo el "
        "error humano y los tiempos de elaboracion.\n\n"
        "4. Garantiza la SOBERANIA DE DATOS ejecutando todo el procesamiento "
        "de IA de forma local mediante Ollama.\n\n"
        "Esto le da un peso institucional enorme al servicio comunitario, porque "
        "esta resolviendo un problema burocratico real de la universidad.")

    out = "docs/06_Marco_Legal.pdf"
    pdf.output(out)
    print(f"Generado: {out}")


if __name__ == "__main__":
    gen_casos_uso()
    gen_marco_legal()
