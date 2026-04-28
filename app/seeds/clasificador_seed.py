"""
Seed del Clasificador Único de Bienes de la SUDEBIP.
Catálogo aproximado basado en la normativa venezolana.
Se actualizará cuando se obtenga el catálogo oficial completo.
"""

CLASIFICADOR_SUDEBIP = [
    # === GRUPO 1: BIENES MUEBLES ===
    # --- 1.01: Maquinaria y Equipos ---
    {
        "codigo": "1.01.01.01", "grupo": "1", "subgrupo": "01", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Maquinaria y Equipos",
        "descripcion_seccion": "Maquinaria Industrial", "descripcion": "Maquinaria de Produccion",
        "palabras_clave": ["maquinaria", "equipo industrial", "produccion", "manufactura"]
    },
    {
        "codigo": "1.01.02.01", "grupo": "1", "subgrupo": "01", "seccion": "02", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Maquinaria y Equipos",
        "descripcion_seccion": "Equipos de Laboratorio", "descripcion": "Equipos de Laboratorio General",
        "palabras_clave": ["laboratorio", "microscopio", "centrifuga", "equipo cientifico"]
    },
    {
        "codigo": "1.01.02.02", "grupo": "1", "subgrupo": "01", "seccion": "02", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Maquinaria y Equipos",
        "descripcion_seccion": "Equipos de Laboratorio", "descripcion": "Instrumentos de Medicion",
        "palabras_clave": ["medicion", "balanza", "termometro", "instrumento", "calibracion"]
    },
    # --- 1.02: Mobiliario y Equipos de Oficina ---
    {
        "codigo": "1.02.01.01", "grupo": "1", "subgrupo": "02", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Mobiliario de Oficina", "descripcion": "Escritorios",
        "palabras_clave": ["escritorio", "mesa de trabajo", "puesto de trabajo", "escritorio ejecutivo"]
    },
    {
        "codigo": "1.02.01.02", "grupo": "1", "subgrupo": "02", "seccion": "01", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Mobiliario de Oficina", "descripcion": "Sillas y Sillones",
        "palabras_clave": ["silla", "sillon", "silla ejecutiva", "silla ergonomica", "silla de oficina"]
    },
    {
        "codigo": "1.02.01.03", "grupo": "1", "subgrupo": "02", "seccion": "01", "categoria": "03",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Mobiliario de Oficina", "descripcion": "Archivadores y Estantes",
        "palabras_clave": ["archivador", "estante", "estanteria", "archivo", "gabinete", "anaquel"]
    },
    {
        "codigo": "1.02.01.04", "grupo": "1", "subgrupo": "02", "seccion": "01", "categoria": "04",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Mobiliario de Oficina", "descripcion": "Mesas de Reuniones",
        "palabras_clave": ["mesa de reuniones", "mesa conferencia", "mesa de juntas"]
    },
    {
        "codigo": "1.02.02.01", "grupo": "1", "subgrupo": "02", "seccion": "02", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Equipos de Oficina", "descripcion": "Telefonos y Fax",
        "palabras_clave": ["telefono", "fax", "central telefonica", "conmutador"]
    },
    {
        "codigo": "1.02.02.02", "grupo": "1", "subgrupo": "02", "seccion": "02", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Equipos de Oficina", "descripcion": "Calculadoras y Sumadoras",
        "palabras_clave": ["calculadora", "sumadora"]
    },
    # --- Mobiliario Educativo ---
    {
        "codigo": "1.02.03.01", "grupo": "1", "subgrupo": "02", "seccion": "03", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Mobiliario Educativo", "descripcion": "Pupitres",
        "palabras_clave": ["pupitre", "mesa de estudiante", "puesto de estudio"]
    },
    {
        "codigo": "1.02.03.02", "grupo": "1", "subgrupo": "02", "seccion": "03", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Mobiliario y Equipos de Oficina",
        "descripcion_seccion": "Mobiliario Educativo", "descripcion": "Pizarras y Pizarrones",
        "palabras_clave": ["pizarra", "pizarron", "tablero", "pizarra acrilica", "pizarra digital"]
    },
    # --- 1.03: Equipos de Computación ---
    {
        "codigo": "1.03.01.01", "grupo": "1", "subgrupo": "03", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Computadoras", "descripcion": "Computadoras de Escritorio",
        "palabras_clave": ["computadora", "computador", "desktop", "pc", "equipo de computo", "cpu"]
    },
    {
        "codigo": "1.03.01.02", "grupo": "1", "subgrupo": "03", "seccion": "01", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Computadoras", "descripcion": "Computadoras Portatiles",
        "palabras_clave": ["laptop", "portatil", "notebook", "computadora portatil"]
    },
    {
        "codigo": "1.03.01.03", "grupo": "1", "subgrupo": "03", "seccion": "01", "categoria": "03",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Computadoras", "descripcion": "Tablets",
        "palabras_clave": ["tablet", "tableta", "ipad"]
    },
    {
        "codigo": "1.03.02.01", "grupo": "1", "subgrupo": "03", "seccion": "02", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Perifericos", "descripcion": "Monitores",
        "palabras_clave": ["monitor", "pantalla", "display", "monitor led"]
    },
    {
        "codigo": "1.03.02.02", "grupo": "1", "subgrupo": "03", "seccion": "02", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Perifericos", "descripcion": "Impresoras",
        "palabras_clave": ["impresora", "printer", "impresora laser", "impresora inkjet", "multifuncional"]
    },
    {
        "codigo": "1.03.02.03", "grupo": "1", "subgrupo": "03", "seccion": "02", "categoria": "03",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Perifericos", "descripcion": "Escaneres",
        "palabras_clave": ["escaner", "scanner", "digitalizador"]
    },
    {
        "codigo": "1.03.02.04", "grupo": "1", "subgrupo": "03", "seccion": "02", "categoria": "04",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Perifericos", "descripcion": "Teclados y Mouse",
        "palabras_clave": ["teclado", "mouse", "raton", "keyboard"]
    },
    {
        "codigo": "1.03.03.01", "grupo": "1", "subgrupo": "03", "seccion": "03", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Servidores y Redes", "descripcion": "Servidores",
        "palabras_clave": ["servidor", "server", "rack", "blade"]
    },
    {
        "codigo": "1.03.03.02", "grupo": "1", "subgrupo": "03", "seccion": "03", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Computacion",
        "descripcion_seccion": "Servidores y Redes", "descripcion": "Equipos de Red",
        "palabras_clave": ["switch", "router", "access point", "hub", "red", "networking"]
    },
    # --- 1.04: Equipos de Comunicación y Audiovisual ---
    {
        "codigo": "1.04.01.01", "grupo": "1", "subgrupo": "04", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Comunicacion",
        "descripcion_seccion": "Equipos Audiovisuales", "descripcion": "Videoproyectores",
        "palabras_clave": ["proyector", "videoproyector", "video beam", "videobeam", "beamer"]
    },
    {
        "codigo": "1.04.01.02", "grupo": "1", "subgrupo": "04", "seccion": "01", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Comunicacion",
        "descripcion_seccion": "Equipos Audiovisuales", "descripcion": "Televisores y Pantallas",
        "palabras_clave": ["televisor", "tv", "pantalla", "smart tv", "television"]
    },
    {
        "codigo": "1.04.01.03", "grupo": "1", "subgrupo": "04", "seccion": "01", "categoria": "03",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Comunicacion",
        "descripcion_seccion": "Equipos Audiovisuales", "descripcion": "Equipos de Sonido",
        "palabras_clave": ["sonido", "parlante", "altavoz", "microfono", "amplificador", "corneta"]
    },
    # --- 1.05: Equipos de Climatización ---
    {
        "codigo": "1.05.01.01", "grupo": "1", "subgrupo": "05", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Climatizacion",
        "descripcion_seccion": "Aires Acondicionados", "descripcion": "Aires Acondicionados",
        "palabras_clave": ["aire acondicionado", "aire", "climatizador", "split", "ventilador"]
    },
    # --- 1.06: Equipos de Transporte ---
    {
        "codigo": "1.06.01.01", "grupo": "1", "subgrupo": "06", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Transporte",
        "descripcion_seccion": "Vehiculos", "descripcion": "Vehiculos Automotores",
        "palabras_clave": ["vehiculo", "carro", "camioneta", "autobus", "transporte"]
    },
    # --- 1.07: Equipos de Seguridad ---
    {
        "codigo": "1.07.01.01", "grupo": "1", "subgrupo": "07", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Seguridad",
        "descripcion_seccion": "Seguridad Electronica", "descripcion": "Camaras de Seguridad",
        "palabras_clave": ["camara", "seguridad", "cctv", "vigilancia", "dvr"]
    },
    {
        "codigo": "1.07.01.02", "grupo": "1", "subgrupo": "07", "seccion": "01", "categoria": "02",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Equipos de Seguridad",
        "descripcion_seccion": "Seguridad Electronica", "descripcion": "Extintores",
        "palabras_clave": ["extintor", "extincion", "incendio", "contra incendio"]
    },
    # --- 1.08: Otros Bienes Muebles ---
    {
        "codigo": "1.08.01.01", "grupo": "1", "subgrupo": "08", "seccion": "01", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Otros Bienes Muebles",
        "descripcion_seccion": "Electrodomesticos", "descripcion": "Electrodomesticos",
        "palabras_clave": ["nevera", "microondas", "cafetera", "dispensador", "refrigerador", "horno"]
    },
    {
        "codigo": "1.08.02.01", "grupo": "1", "subgrupo": "08", "seccion": "02", "categoria": "01",
        "descripcion_grupo": "Bienes Muebles", "descripcion_subgrupo": "Otros Bienes Muebles",
        "descripcion_seccion": "Equipos Deportivos", "descripcion": "Equipos Deportivos",
        "palabras_clave": ["deportivo", "gimnasio", "equipo deportivo", "cancha"]
    },
]


async def seed_clasificador(db) -> int:
    """Inserta el clasificador SUDEBIP en la base de datos si no existe."""
    collection = db.clasificador_sudebip
    count = await collection.count_documents({})
    if count > 0:
        print(f"[INFO] Clasificador SUDEBIP ya tiene {count} registros. Omitiendo seed.")
        return count

    result = await collection.insert_many(CLASIFICADOR_SUDEBIP)
    inserted = len(result.inserted_ids)
    print(f"[OK] Clasificador SUDEBIP: {inserted} registros insertados")
    return inserted
