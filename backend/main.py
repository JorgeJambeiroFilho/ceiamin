from fastapi import FastAPI
from enum import Enum

from br.gov.rfb.ceia.ceiamin.backend.minceia import wordInitialLoad
from br.gov.rfb.ceia.ceiamin.backend.palavras import Palavras
from br.gov.rfb.ceia.ceiamin.backend.novaspalavras import palavrasCarregamentoInicial
from fastapi.middleware.cors import CORSMiddleware
import traceback


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lingua(str, Enum):
    objeto = "ingles"
    animal = "portugues"

@app.get("/backend")
async def root():
    return {"message": "Hello World"}

@app.get("/backend/palavras")
async def get_model():
    palavras = Palavras()
    return { "palavras": palavras.palavras }

@app.get("/backend/initialload")
async def get_model():
    try:
        await wordInitialLoad()
        return { "initialload": "ok"}
    except Exception as e:
        traceback.print_exc()
        return {"initialload": "fail"}

@app.get("/backend/novaspalavras")
async def get_model():
    try:
        vocabulos = await palavrasCarregamentoInicial()
        return { "Novas palavras": vocabulos }
    except Exception as e:
        traceback.print_exc()
        return {"Novas palavras": "Falhou"}