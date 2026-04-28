"""
Router de Chat — Asistente virtual IA con contexto dinámico desde MongoDB.
Refactorizado del main.py original para usar datos reales de la BD.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import os

from app.database import get_database
from app.config import get_settings

router = APIRouter()


class ChatRequest(BaseModel):
    """Solicitud de chat."""
    pregunta: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    """Respuesta del chat."""
    pregunta: str
    respuesta: str


async def _obtener_contexto_inventario() -> str:
    """Genera un contexto dinámico con datos reales del inventario."""
    db = get_database()

    # Contar bienes por sede
    pipeline_sede = [
        {"$match": {"estado": {"$ne": "DESINCORPORADO"}}},
        {"$group": {
            "_id": "$sede.nombre",
            "total": {"$sum": 1},
            "valor": {"$sum": "$valor_adquisicion"},
        }},
        {"$sort": {"total": -1}},
    ]

    lineas = ["Datos actualizados del inventario de la UNEG:\n"]

    async for doc in db.bienes.aggregate(pipeline_sede):
        lineas.append(f"- {doc['_id']}: {doc['total']} bienes (valor: ${doc['valor']:,.2f})")

    # Resumen por grupo SUDEBIP
    pipeline_grupo = [
        {"$match": {"estado": {"$ne": "DESINCORPORADO"}}},
        {"$group": {"_id": "$grupo_sudebip", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 5},
    ]
    lineas.append("\nPrincipales categorias de bienes:")
    async for doc in db.bienes.aggregate(pipeline_grupo):
        lineas.append(f"- {doc['_id']}: {doc['total']} unidades")

    # Total general
    total = await db.bienes.count_documents({"estado": {"$ne": "DESINCORPORADO"}})
    faltantes = await db.bienes.count_documents({"estado": "FALTANTE"})
    lineas.append(f"\nTotal de bienes activos: {total}")
    if faltantes:
        lineas.append(f"Bienes faltantes: {faltantes}")

    # Sedes
    sedes = []
    async for s in db.sedes.find({"activa": True}):
        sedes.append(f"{s['nombre']} ({s['codigo']})")
    lineas.append(f"\nSedes activas: {', '.join(sedes)}")

    return "\n".join(lineas)


TEMPLATE = """
Eres el Asistente Virtual de Gestion de Activos de la UNEG. Tu proposito es ayudar al personal administrativo a consultar el inventario de la universidad.

NORMAS DE COMPORTAMIENTO:
1. Si el usuario te saluda, responde cordialmente, identificate y explica brevemente que tipo de informacion puedes dar.
2. Si preguntan algo especifico sobre activos, busca UNICAMENTE en el CONTEXTO proporcionado abajo.
3. Si la respuesta no esta en el CONTEXTO, responde amablemente que no tienes esa informacion.
4. Manten un tono profesional, servicial y breve.

CONTEXTO INSTITUCIONAL:
{contexto}

PREGUNTA DEL USUARIO: {pregunta}

RESPUESTA DEL ASISTENTE:
"""


@router.post("", response_model=ChatResponse)
async def consultar_asistente(request: ChatRequest):
    """Consultar el asistente virtual de inventario."""
    try:
        # Obtener contexto dinámico desde MongoDB
        contexto = await _obtener_contexto_inventario()

        # Intentar usar Ollama/LangChain
        try:
            from langchain_community.llms import Ollama
            from langchain_core.prompts import PromptTemplate

            settings = get_settings()
            llm = Ollama(model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_BASE_URL)
            prompt = PromptTemplate(input_variables=["contexto", "pregunta"], template=TEMPLATE)
            chain = prompt | llm

            respuesta = chain.invoke({
                "contexto": contexto,
                "pregunta": request.pregunta,
            })

            return {"pregunta": request.pregunta, "respuesta": respuesta.strip()}

        except Exception as e:
            # Si Ollama no está disponible, dar respuesta basada en contexto
            return {
                "pregunta": request.pregunta,
                "respuesta": (
                    f"El modelo de IA no esta disponible en este momento ({str(e)[:100]}). "
                    f"Sin embargo, aqui esta el resumen del inventario:\n\n{contexto}"
                ),
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
