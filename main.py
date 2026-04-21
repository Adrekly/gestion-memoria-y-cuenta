from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import os

app = FastAPI(title="API UNEG Memoria y Cuenta")

# Habilitar CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción aquí pones la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
llm = Ollama(model="gemma:7b", base_url=ollama_url)

class QueryRequest(BaseModel):
    pregunta: str

# Refinamiento estricto del Agente
# ... (mantén tus imports y configuración de CORS igual)

template = """
Eres el Asistente Virtual de Gestión de Activos de la UNEG. Tu propósito es ayudar al personal administrativo a consultar el inventario de la universidad.

NORMAS DE COMPORTAMIENTO:
1. Si el usuario te saluda (ej. "Hola", "Buenos días"), responde cordialmente, identifícate y explícale brevemente qué tipo de información puedes darle (consultas de activos, sedes, equipos).
2. Si te preguntan algo específico sobre activos (cantidades, ubicaciones, presupuestos), busca ÚNICAMENTE en el CONTEXTO proporcionado abajo.
3. Si la respuesta específica no está en el CONTEXTO, responde amablemente: "Lo siento, no tengo registros específicos de ese activo en mi base de datos actual. ¿Deseas consultar algo más sobre las sedes de Puerto Ordaz o Ciudad Bolívar?"
4. Mantén siempre un tono profesional, servicial y breve.

CONTEXTO INSTITUCIONAL:
{contexto}

PREGUNTA DEL USUARIO: {pregunta}

RESPUESTA DEL ASISTENTE:
"""

prompt = PromptTemplate(input_variables=["contexto", "pregunta"], template=template)
chain = prompt | llm

@app.post("/api/chat")
async def consultar_activos(request: QueryRequest):
    try:
        # CONTEXTO TEMPORAL (Esto es lo que el chatbot "sabe")
        # Tip: Agrega aquí un par de líneas más para que tenga qué decir.
        datos_reales_uneg = """
        - Sede Puerto Ordaz (Atlántico): 50 computadoras de escritorio, 20 videoproyectores, 150 pupitres.
        - Sede Ciudad Bolívar: 30 computadoras de escritorio, 5 servidores, 100 pupitres.
        - Presupuesto ejecutado en tecnología 2025: 15.000 USD.
        - Responsable de inventario: Departamento de Bienes Nacionales UNEG.
        - Sede Atlantico: 10 impresoras, 5 escáneres, 200 sillas.
        - Sede Villa Asia: 20 computadoras portátiles, 10 proyectores, 100 pupitres, 4 aires.
        """
        
        # Invocamos al modelo
        respuesta = chain.invoke({
            "contexto": datos_reales_uneg, 
            "pregunta": request.pregunta
        })
        
        return {"pregunta": request.pregunta, "respuesta": respuesta.strip()}
        
    except Exception as e:
        # Log del error para que sepas qué pasó exactamente
        print(f"Error interno: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))