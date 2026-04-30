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


from typing import List, Dict, Optional

class MensajeHistorial(BaseModel):
    rol: str
    texto: str

class ChatRequest(BaseModel):
    """Solicitud de chat."""
    pregunta: str = Field(..., min_length=1, max_length=1000)
    historial: List[MensajeHistorial] = []


class ChatResponse(BaseModel):
    """Respuesta del chat."""
    pregunta: str
    respuesta: str


async def _obtener_contexto_inventario(pregunta: str) -> str:
    """Genera un contexto dinámico con datos globales y resultados específicos (RAG)."""
    db = get_database()
    lineas = ["Datos actuales del inventario:\n"]

    # Búsqueda dinámica (RAG)
    # Extraer palabras largas de la pregunta para buscar
    palabras = [p for p in pregunta.split() if len(p) > 3]
    if palabras:
        query_text = " ".join(palabras)
        cursor_busqueda = db.bienes.find(
            {"$text": {"$search": query_text}}
        ).sort([("score", {"$meta": "textScore"})]).limit(5)
        
        resultados = []
        async for doc in cursor_busqueda:
            resultados.append(f"- Bien {doc.get('codigo_inventario')}: {doc.get('descripcion')} | Sede: {doc.get('sede', {}).get('nombre', 'N/A')} | Estado: {doc.get('estado')}")
        
        if resultados:
            lineas.append("BIENES ESPECIFICOS ENCONTRADOS RELACIONADOS A LA PREGUNTA:")
            lineas.extend(resultados)
            lineas.append("\n")

    # Contar bienes por sede
    pipeline_sede = [
        {"$match": {"estado": {"$ne": "DESINCORPORADO"}}},
        {"$group": {
            "_id": "$sede.nombre",
            "total": {"$sum": 1},
        }},
        {"$sort": {"total": -1}},
    ]
    async for doc in db.bienes.aggregate(pipeline_sede):
        lineas.append(f"- Sede {doc['_id']}: {doc['total']} bienes activos")

    # Total general
    total = await db.bienes.count_documents({"estado": {"$ne": "DESINCORPORADO"}})
    lineas.append(f"\nTotal general de bienes activos: {total}")

    return "\n".join(lineas)


TEMPLATE = """
Eres el Asistente Virtual de Gestion de Activos de la UNEG. Tu proposito es ayudar al personal a consultar el inventario.

NORMAS DE COMPORTAMIENTO:
1. Responde de forma clara y directa utilizando formato Markdown (listas, negritas).
2. Usa el CONTEXTO proporcionado para responder.
3. El HISTORIAL contiene la conversacion previa, usalo para entender referencias a respuestas anteriores.
4. Si la respuesta no esta ni en el contexto ni en el historial, di amablemente que no tienes esa informacion exacta.

CONTEXTO ACTUAL DEL INVENTARIO:
{contexto}

HISTORIAL DE LA CONVERSACION:
{historial}

PREGUNTA DEL USUARIO: {pregunta}

RESPUESTA DEL ASISTENTE:
"""


@router.post("", response_model=ChatResponse)
async def consultar_asistente(request: ChatRequest):
    """Consultar el asistente virtual de inventario."""
    try:
        contexto = await _obtener_contexto_inventario(request.pregunta)

        # Formatear historial
        historial_str = ""
        for msg in request.historial[-5:]:  # Solo los ultimos 5 para no saturar contexto
            historial_str += f"{msg.rol.upper()}: {msg.texto}\n"
        if not historial_str:
            historial_str = "No hay conversacion previa."

        try:
            from langchain_community.llms import Ollama
            from langchain_core.prompts import PromptTemplate

            settings = get_settings()
            llm = Ollama(model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_BASE_URL)
            prompt = PromptTemplate(input_variables=["contexto", "historial", "pregunta"], template=TEMPLATE)
            chain = prompt | llm

            respuesta = chain.invoke({
                "contexto": contexto,
                "historial": historial_str,
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
