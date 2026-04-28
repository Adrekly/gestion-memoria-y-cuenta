"""
Seed de Sedes de la UNEG.
Datos basados en la información oficial de la universidad.
"""

SEDES_UNEG = [
    {
        "codigo": "ATL",
        "nombre": "Ciudad Universitaria (Atlantico)",
        "ciudad": "Ciudad Guayana",
        "direccion": "Av. Atlantico, Puerto Ordaz, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "VAS",
        "nombre": "Villa Asia",
        "ciudad": "Ciudad Guayana",
        "direccion": "Urbanizacion Villa Asia, Puerto Ordaz, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "CHI",
        "nombre": "Chilemex",
        "ciudad": "Ciudad Guayana",
        "direccion": "Zona Industrial Chilemex, Puerto Ordaz, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "JBO",
        "nombre": "Jardin Botanico",
        "ciudad": "Ciudad Bolivar",
        "direccion": "Av. Germania, Ciudad Bolivar, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "CDV",
        "nombre": "Casa de las Doce Ventanas",
        "ciudad": "Ciudad Bolivar",
        "direccion": "Casco Historico, Ciudad Bolivar, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "UPA",
        "nombre": "Sede Upata",
        "ciudad": "Upata",
        "direccion": "Upata, Municipio Piar, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "CAL",
        "nombre": "Sede El Callao",
        "ciudad": "El Callao",
        "direccion": "El Callao, Municipio El Callao, Edo. Bolivar",
        "activa": True,
    },
    {
        "codigo": "SEU",
        "nombre": "Santa Elena de Uairen",
        "ciudad": "Santa Elena de Uairen",
        "direccion": "Santa Elena de Uairen, Municipio Gran Sabana, Edo. Bolivar",
        "activa": True,
    },
]


async def seed_sedes(db) -> int:
    """Inserta las sedes de la UNEG si no existen."""
    collection = db.sedes
    count = await collection.count_documents({})
    if count > 0:
        print(f"[INFO] Sedes ya tiene {count} registros. Omitiendo seed.")
        return count

    result = await collection.insert_many(SEDES_UNEG)
    inserted = len(result.inserted_ids)
    print(f"[OK] Sedes UNEG: {inserted} registros insertados")
    return inserted
