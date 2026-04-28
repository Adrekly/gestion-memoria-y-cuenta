"""
Seed de datos de prueba: bienes, movimientos y desincorporaciones.
Inserta directamente en MongoDB via docker exec.
"""
import json
import subprocess
from datetime import datetime, timedelta
import random

BIENES = [
    # Computadoras
    {"codigo_sudebip": "1.03.01.01", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Computadora de escritorio Dell OptiPlex 7090", "marca": "Dell", "modelo": "OptiPlex 7090", "serial": "DL-2024-001", "valor_adquisicion": 850.00, "fecha_adquisicion": "2023-03-15", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Administrativo, Piso 2, Oficina 201", "responsable": "Maria Garcia", "cedula_responsable": "V-15234567", "departamento": "Administracion"},
    {"codigo_sudebip": "1.03.01.01", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Computadora de escritorio HP ProDesk 400", "marca": "HP", "modelo": "ProDesk 400 G7", "serial": "HP-2024-002", "valor_adquisicion": 720.00, "fecha_adquisicion": "2023-05-20", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Academico, Laboratorio 3", "responsable": "Carlos Rodriguez", "cedula_responsable": "V-18456789", "departamento": "Coordinacion de Informatica"},
    {"codigo_sudebip": "1.03.01.01", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Computadora de escritorio Lenovo ThinkCentre", "marca": "Lenovo", "modelo": "ThinkCentre M70q", "serial": "LN-2023-015", "valor_adquisicion": 680.00, "fecha_adquisicion": "2022-11-10", "condicion": "REGULAR", "sede_codigo": "VAS", "ubicacion_especifica": "Oficina de Registro, Planta Baja", "responsable": "Ana Martinez", "cedula_responsable": "V-20123456", "departamento": "Registro Academico"},
    {"codigo_sudebip": "1.03.01.02", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Laptop HP EliteBook 840 G8", "marca": "HP", "modelo": "EliteBook 840 G8", "serial": "HP-LAP-2024-001", "valor_adquisicion": 1200.00, "fecha_adquisicion": "2024-01-10", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Decanato, Oficina del Decano", "responsable": "Prof. Juan Hernandez", "cedula_responsable": "V-12345678", "departamento": "Decanato de Ingenieria"},
    {"codigo_sudebip": "1.03.01.02", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Laptop Dell Latitude 5520", "marca": "Dell", "modelo": "Latitude 5520", "serial": "DL-LAP-2023-008", "valor_adquisicion": 950.00, "fecha_adquisicion": "2023-08-22", "condicion": "BUENO", "sede_codigo": "JBO", "ubicacion_especifica": "Biblioteca Central, Sala de Profesores", "responsable": "Luisa Perez", "cedula_responsable": "V-14567890", "departamento": "Biblioteca"},
    # Monitores
    {"codigo_sudebip": "1.03.02.01", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Monitor Samsung 24 pulgadas LED", "marca": "Samsung", "modelo": "S24R350", "serial": "SM-MON-2024-003", "valor_adquisicion": 180.00, "fecha_adquisicion": "2023-03-15", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Administrativo, Piso 2, Oficina 201", "responsable": "Maria Garcia", "cedula_responsable": "V-15234567", "departamento": "Administracion"},
    {"codigo_sudebip": "1.03.02.01", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Monitor LG 27 pulgadas IPS", "marca": "LG", "modelo": "27MK430H", "serial": "LG-MON-2023-007", "valor_adquisicion": 220.00, "fecha_adquisicion": "2023-06-01", "condicion": "BUENO", "sede_codigo": "VAS", "ubicacion_especifica": "Laboratorio de Diseno, Piso 1", "responsable": "Pedro Sanchez", "cedula_responsable": "V-19876543", "departamento": "Coordinacion de Diseno"},
    # Impresoras
    {"codigo_sudebip": "1.03.02.02", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Impresora HP LaserJet Pro M404dn", "marca": "HP", "modelo": "LaserJet Pro M404dn", "serial": "HP-IMP-2023-004", "valor_adquisicion": 350.00, "fecha_adquisicion": "2023-02-28", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Administrativo, Piso 1, Sala de Copiado", "responsable": "Rosa Diaz", "cedula_responsable": "V-16789012", "departamento": "Administracion"},
    {"codigo_sudebip": "1.03.02.02", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Impresora Epson EcoTank L3250", "marca": "Epson", "modelo": "EcoTank L3250", "serial": "EP-IMP-2022-011", "valor_adquisicion": 250.00, "fecha_adquisicion": "2022-09-15", "condicion": "MALO", "sede_codigo": "CHI", "ubicacion_especifica": "Oficina de Coordinacion, Planta Baja", "responsable": "Miguel Torres", "cedula_responsable": "V-17654321", "departamento": "Coordinacion de Extension"},
    # Escritorios
    {"codigo_sudebip": "1.02.01.01", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Escritorio ejecutivo de madera con gavetas", "marca": "Muebles Venezuela", "modelo": "EJ-200", "serial": "MV-ESC-2020-001", "valor_adquisicion": 280.00, "fecha_adquisicion": "2020-06-10", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Decanato, Oficina del Decano", "responsable": "Prof. Juan Hernandez", "cedula_responsable": "V-12345678", "departamento": "Decanato de Ingenieria"},
    {"codigo_sudebip": "1.02.01.01", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Escritorio secretarial metalico", "marca": "Ofimuebles", "modelo": "SEC-100", "serial": "OF-ESC-2019-015", "valor_adquisicion": 150.00, "fecha_adquisicion": "2019-03-22", "condicion": "REGULAR", "sede_codigo": "VAS", "ubicacion_especifica": "Oficina de Registro, Planta Baja", "responsable": "Ana Martinez", "cedula_responsable": "V-20123456", "departamento": "Registro Academico"},
    {"codigo_sudebip": "1.02.01.01", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Escritorio de trabajo en L", "marca": "Ofimuebles", "modelo": "TL-300", "serial": "OF-ESC-2021-022", "valor_adquisicion": 320.00, "fecha_adquisicion": "2021-01-15", "condicion": "BUENO", "sede_codigo": "JBO", "ubicacion_especifica": "Coordinacion de Postgrado, Piso 2", "responsable": "Dra. Carmen Lopez", "cedula_responsable": "V-11234567", "departamento": "Postgrado"},
    # Sillas
    {"codigo_sudebip": "1.02.01.02", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Silla ejecutiva ergonomica con apoyabrazos", "marca": "ErgoSit", "modelo": "PRO-500", "serial": "ES-SIL-2023-001", "valor_adquisicion": 180.00, "fecha_adquisicion": "2023-04-05", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Decanato, Oficina del Decano", "responsable": "Prof. Juan Hernandez", "cedula_responsable": "V-12345678", "departamento": "Decanato de Ingenieria"},
    {"codigo_sudebip": "1.02.01.02", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Silla de oficina giratoria negra", "marca": "GeneriMueble", "modelo": "OFC-200", "serial": "GM-SIL-2020-033", "valor_adquisicion": 85.00, "fecha_adquisicion": "2020-08-12", "condicion": "MALO", "sede_codigo": "CHI", "ubicacion_especifica": "Sala de Reuniones, Piso 1", "responsable": "Roberto Blanco", "cedula_responsable": "V-13456789", "departamento": "Coordinacion de Extension"},
    # Proyectores
    {"codigo_sudebip": "1.04.01.01", "grupo_sudebip": "Equipos de Comunicacion", "descripcion": "Videoproyector Epson PowerLite E20", "marca": "Epson", "modelo": "PowerLite E20", "serial": "EP-PRO-2023-002", "valor_adquisicion": 450.00, "fecha_adquisicion": "2023-07-18", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Auditorio Principal", "responsable": "Jose Ramirez", "cedula_responsable": "V-16234567", "departamento": "Servicios Generales"},
    {"codigo_sudebip": "1.04.01.01", "grupo_sudebip": "Equipos de Comunicacion", "descripcion": "Videoproyector ViewSonic PA503S", "marca": "ViewSonic", "modelo": "PA503S", "serial": "VS-PRO-2021-006", "valor_adquisicion": 380.00, "fecha_adquisicion": "2021-11-25", "condicion": "REGULAR", "sede_codigo": "VAS", "ubicacion_especifica": "Sala de Conferencias B", "responsable": "Pedro Sanchez", "cedula_responsable": "V-19876543", "departamento": "Coordinacion de Diseno"},
    # Aires acondicionados
    {"codigo_sudebip": "1.05.01.01", "grupo_sudebip": "Equipos de Climatizacion", "descripcion": "Aire acondicionado split 12000 BTU", "marca": "Samsung", "modelo": "AR12BSHQAWKNAZ", "serial": "SM-AC-2022-004", "valor_adquisicion": 550.00, "fecha_adquisicion": "2022-04-10", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Administrativo, Piso 2", "responsable": "Jose Ramirez", "cedula_responsable": "V-16234567", "departamento": "Servicios Generales"},
    {"codigo_sudebip": "1.05.01.01", "grupo_sudebip": "Equipos de Climatizacion", "descripcion": "Aire acondicionado split 18000 BTU", "marca": "LG", "modelo": "S4-Q18KL3QA", "serial": "LG-AC-2020-009", "valor_adquisicion": 750.00, "fecha_adquisicion": "2020-01-20", "condicion": "REGULAR", "sede_codigo": "JBO", "ubicacion_especifica": "Biblioteca Central, Sala Principal", "responsable": "Luisa Perez", "cedula_responsable": "V-14567890", "departamento": "Biblioteca"},
    # Archivadores
    {"codigo_sudebip": "1.02.01.03", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Archivador metalico 4 gavetas", "marca": "ArchiVen", "modelo": "AM-400", "serial": "AV-ARC-2018-007", "valor_adquisicion": 120.00, "fecha_adquisicion": "2018-05-30", "condicion": "REGULAR", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Administrativo, Piso 1, Archivo", "responsable": "Rosa Diaz", "cedula_responsable": "V-16789012", "departamento": "Administracion"},
    # Camaras de seguridad
    {"codigo_sudebip": "1.07.01.01", "grupo_sudebip": "Equipos de Seguridad", "descripcion": "Camara de seguridad IP Hikvision 2MP", "marca": "Hikvision", "modelo": "DS-2CD1023G0E", "serial": "HK-CAM-2023-012", "valor_adquisicion": 95.00, "fecha_adquisicion": "2023-09-01", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Entrada Principal, Caseta de Vigilancia", "responsable": "Jose Ramirez", "cedula_responsable": "V-16234567", "departamento": "Seguridad"},
    # Pupitres
    {"codigo_sudebip": "1.02.03.01", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Pupitre universitario con paleta derecha", "marca": "MobEscolar", "modelo": "PU-100", "serial": None, "valor_adquisicion": 45.00, "fecha_adquisicion": "2019-02-15", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Academico, Aula 101", "responsable": "Carlos Rodriguez", "cedula_responsable": "V-18456789", "departamento": "Coordinacion de Informatica"},
    {"codigo_sudebip": "1.02.03.01", "grupo_sudebip": "Mobiliario y Equipos de Oficina", "descripcion": "Pupitre universitario con paleta derecha", "marca": "MobEscolar", "modelo": "PU-100", "serial": None, "valor_adquisicion": 45.00, "fecha_adquisicion": "2019-02-15", "condicion": "REGULAR", "sede_codigo": "VAS", "ubicacion_especifica": "Aula Magna, Planta Baja", "responsable": "Pedro Sanchez", "cedula_responsable": "V-19876543", "departamento": "Coordinacion de Diseno"},
    # Electrodomesticos
    {"codigo_sudebip": "1.08.01.01", "grupo_sudebip": "Otros Bienes Muebles", "descripcion": "Dispensador de agua fria/caliente", "marca": "Avanti", "modelo": "WD363P", "serial": "AV-DIS-2023-003", "valor_adquisicion": 120.00, "fecha_adquisicion": "2023-06-15", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Edificio Administrativo, Piso 1, Recepcion", "responsable": "Rosa Diaz", "cedula_responsable": "V-16789012", "departamento": "Administracion"},
    {"codigo_sudebip": "1.08.01.01", "grupo_sudebip": "Otros Bienes Muebles", "descripcion": "Microondas Samsung 1.1 pies cubicos", "marca": "Samsung", "modelo": "MS32J5133AT", "serial": "SM-MIC-2022-005", "valor_adquisicion": 85.00, "fecha_adquisicion": "2022-12-01", "condicion": "BUENO", "sede_codigo": "JBO", "ubicacion_especifica": "Comedor Universitario", "responsable": "Luisa Perez", "cedula_responsable": "V-14567890", "departamento": "Bienestar Estudiantil"},
    # Equipos de red
    {"codigo_sudebip": "1.03.03.02", "grupo_sudebip": "Equipos de Computacion", "descripcion": "Switch Cisco Catalyst 24 puertos", "marca": "Cisco", "modelo": "C9200L-24T-4G", "serial": "CS-SW-2023-001", "valor_adquisicion": 1800.00, "fecha_adquisicion": "2023-10-05", "condicion": "BUENO", "sede_codigo": "ATL", "ubicacion_especifica": "Data Center, Rack Principal", "responsable": "Carlos Rodriguez", "cedula_responsable": "V-18456789", "departamento": "Coordinacion de Informatica"},
]

def run_mongo(js_code):
    """Ejecuta JS en MongoDB via docker exec."""
    result = subprocess.run(
        ["docker", "exec", "uneg_mongodb", "mongosh", "uneg_bienes", "--quiet", "--eval", js_code],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
    return result.stdout.strip()

def main():
    # Verificar conexion
    count = run_mongo("db.bienes.countDocuments()")
    print(f"Bienes actuales: {count}")
    if int(count) > 0:
        print("Ya hay bienes. Limpiando...")
        run_mongo("db.bienes.deleteMany({})")
        run_mongo("db.movimientos.deleteMany({})")
        run_mongo("db.desincorporaciones.deleteMany({})")

    # Obtener IDs de sedes
    sedes_json = run_mongo("JSON.stringify(db.sedes.find({}, {codigo:1, nombre:1}).toArray())")
    sedes = {s["codigo"]: s["nombre"] for s in json.loads(sedes_json)}

    # Insertar bienes
    bien_ids = []
    for i, b in enumerate(BIENES):
        sede_nombre = sedes.get(b["sede_codigo"], b["sede_codigo"])
        grupo_num = b["codigo_sudebip"].split(".")[1]
        seq = str(i + 1).zfill(5)
        codigo_inv = f"UNEG-{b['sede_codigo']}-{grupo_num}-{seq}"

        # Algunos bienes con estados especiales
        estado = "EN_USO"
        if i == 8:  # Impresora Epson mala
            estado = "INSERVIBLE"
        elif i == 13:  # Silla mala
            estado = "EN_DESUSO"
        elif i == 18:  # Aire LG
            estado = "EN_REPARACION"

        doc = {
            "codigo_inventario": codigo_inv,
            "codigo_sudebip": b["codigo_sudebip"],
            "grupo_sudebip": b["grupo_sudebip"],
            "descripcion": b["descripcion"],
            "marca": b.get("marca"),
            "modelo": b.get("modelo"),
            "serial": b.get("serial"),
            "valor_adquisicion": b["valor_adquisicion"],
            "fecha_adquisicion": {"$date": f"{b['fecha_adquisicion']}T00:00:00Z"},
            "estado": estado,
            "condicion": b["condicion"],
            "sede": {"codigo": b["sede_codigo"], "nombre": sede_nombre},
            "ubicacion_especifica": b.get("ubicacion_especifica"),
            "responsable": b["responsable"],
            "cedula_responsable": b["cedula_responsable"],
            "departamento": b["departamento"],
            "observaciones": None,
            "created_at": {"$date": f"{b['fecha_adquisicion']}T10:00:00Z"},
            "updated_at": {"$date": f"{b['fecha_adquisicion']}T10:00:00Z"},
        }

        doc_json = json.dumps(doc).replace('"', '\\"')
        result = run_mongo(f'JSON.stringify(db.bienes.insertOne(JSON.parse("{doc_json}")))')
        try:
            inserted = json.loads(result)
            bien_ids.append(inserted.get("insertedId", {}).get("$oid", str(i)))
        except:
            bien_ids.append(str(i))

    print(f"[OK] {len(BIENES)} bienes insertados")

    # Obtener IDs reales
    ids_json = run_mongo("JSON.stringify(db.bienes.find({}, {_id:1}).toArray())")
    ids = json.loads(ids_json)
    real_ids = [doc["_id"]["$oid"] for doc in ids]

    # Insertar movimientos
    movimientos = [
        {"bien_idx": 3, "tipo": "ENTRADA", "fecha": "2024-01-10", "sede_origen": None, "sede_destino": "ATL", "motivo": "Incorporacion de laptop nueva por compra directa", "autorizado_por": "Dir. Administracion", "documento_soporte": "OC-2024-001"},
        {"bien_idx": 4, "tipo": "ENTRADA", "fecha": "2023-08-22", "sede_origen": None, "sede_destino": "JBO", "motivo": "Incorporacion de laptop para Biblioteca Central", "autorizado_por": "Dir. Administracion", "documento_soporte": "OC-2023-045"},
        {"bien_idx": 0, "tipo": "TRASLADO", "fecha": "2024-06-15", "sede_origen": "VAS", "sede_destino": "ATL", "motivo": "Reasignacion a nueva oficina administrativa", "autorizado_por": "Jefe de Bienes", "documento_soporte": "MEM-2024-012"},
        {"bien_idx": 2, "tipo": "REASIGNACION", "fecha": "2024-03-10", "sede_origen": "VAS", "sede_destino": "VAS", "motivo": "Cambio de custodio por rotacion de personal", "autorizado_por": "Coord. Registro", "documento_soporte": "MEM-2024-008"},
        {"bien_idx": 25, "tipo": "ENTRADA", "fecha": "2023-10-05", "sede_origen": None, "sede_destino": "ATL", "motivo": "Adquisicion de equipamiento de red para data center", "autorizado_por": "Dir. Administracion", "documento_soporte": "OC-2023-089"},
        {"bien_idx": 15, "tipo": "TRASLADO", "fecha": "2024-02-20", "sede_origen": "ATL", "sede_destino": "VAS", "motivo": "Traslado de proyector para evento academico en Villa Asia", "autorizado_por": "Coord. Academica", "documento_soporte": "MEM-2024-005"},
        {"bien_idx": 8, "tipo": "SALIDA", "fecha": "2024-09-01", "sede_origen": "CHI", "sede_destino": None, "motivo": "Retiro para diagnostico tecnico en taller externo", "autorizado_por": "Jefe de Bienes", "documento_soporte": "MEM-2024-031"},
    ]

    for m in movimientos:
        doc = {
            "bien_id": {"$oid": real_ids[m["bien_idx"]]},
            "tipo": m["tipo"],
            "fecha": {"$date": f"{m['fecha']}T10:00:00Z"},
            "sede_origen": m["sede_origen"],
            "sede_destino": m["sede_destino"],
            "motivo": m["motivo"],
            "autorizado_por": m["autorizado_por"],
            "documento_soporte": m["documento_soporte"],
        }
        doc_json = json.dumps(doc).replace('"', '\\"')
        run_mongo(f'db.movimientos.insertOne(JSON.parse("{doc_json}"))')

    print(f"[OK] {len(movimientos)} movimientos insertados")

    # Insertar desincorporaciones
    desincorporaciones = [
        {"bien_idx": 8, "motivo": "INSERVIBILIDAD", "justificacion": "La impresora Epson EcoTank L3250 presenta fallo total del cabezal de impresion. Se realizaron dos intentos de reparacion sin exito. El costo de reemplazo del cabezal supera el 70% del valor del equipo. Se recomienda desincorporacion por inservibilidad tecnica.", "estado_proceso": "EN_REVISION", "solicitado_por": "Miguel Torres", "aprobado_por": None},
        {"bien_idx": 13, "motivo": "OBSOLESCENCIA", "justificacion": "La silla de oficina giratoria presenta desgaste severo en el mecanismo de elevacion hidraulica y la base de ruedas. El tapizado esta deteriorado con roturas multiples. Tiene mas de 4 anos de uso continuo y no justifica inversion en reparacion.", "estado_proceso": "APROBADA", "solicitado_por": "Roberto Blanco", "aprobado_por": "Jefe de Bienes Nacionales"},
    ]

    for d in desincorporaciones:
        validacion = {
            "cumple_criterios": True,
            "observaciones": "Justificacion tecnica cumple con los criterios minimos de la SUDEBIP.",
            "fecha_validacion": {"$date": "2024-10-01T10:00:00Z"},
        }
        doc = {
            "bien_id": {"$oid": real_ids[d["bien_idx"]]},
            "motivo": d["motivo"],
            "justificacion_tecnica": d["justificacion"],
            "estado_proceso": d["estado_proceso"],
            "solicitado_por": d["solicitado_por"],
            "fecha_solicitud": {"$date": "2024-09-15T10:00:00Z"},
            "validacion_ia": validacion,
            "aprobado_por": d["aprobado_por"],
            "fecha_aprobacion": {"$date": "2024-10-05T10:00:00Z"} if d["aprobado_por"] else None,
            "observaciones": None,
        }
        doc_json = json.dumps(doc).replace('"', '\\"')
        run_mongo(f'db.desincorporaciones.insertOne(JSON.parse("{doc_json}"))')

    # Marcar el bien aprobado como DESINCORPORADO
    run_mongo(f'db.bienes.updateOne({{_id: ObjectId("{real_ids[13]}")}}, {{$set: {{estado: "DESINCORPORADO"}}}})')

    print(f"[OK] {len(desincorporaciones)} desincorporaciones insertadas")

    # Resumen final
    print("\n=== RESUMEN ===")
    print(f"Bienes:              {run_mongo('db.bienes.countDocuments()')}")
    print(f"Movimientos:         {run_mongo('db.movimientos.countDocuments()')}")
    print(f"Desincorporaciones:  {run_mongo('db.desincorporaciones.countDocuments()')}")
    print(f"Sedes:               {run_mongo('db.sedes.countDocuments()')}")
    print(f"Clasificador:        {run_mongo('db.clasificador_sudebip.countDocuments()')}")

if __name__ == "__main__":
    main()
