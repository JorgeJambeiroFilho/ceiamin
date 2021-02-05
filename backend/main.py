from typing import Optional, List 
from fastapi import FastAPI
from pydantic import BaseModel

from br.gov.rfb.ceia.ceiamin.backend.minceia import wordInitialLoad
from br.gov.rfb.ceia.ceiamin.backend.palavras import Palavras
from br.gov.rfb.ceia.ceiamin.backend.lerpalavras import lerPalavrasMDB, inserirPalavraMDB, apagarPalavraMDB
from fastapi.middleware.cors import CORSMiddleware
import traceback


app = FastAPI()


class Vocabulo(BaseModel):
    palavras_unicas: List[str]
    voto_ingles: int 
    voto_portugues: int


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return { "Initialload": "Ok" }
    except Exception as e:
        traceback.print_exc()
        return { "Initialload": "Falhou" }

@app.get("/backend/lerpalavras")
async def get_model():
    try:
        palavras = await lerPalavrasMDB()
        # palavras = Palavras()
        return { "palavras": palavras.palavras }
    except Exception as e:
        traceback.print_exc()
        return {"Ler palavras": "Falhou"}

@app.post("/backend/inserirpalavra")
async def inserir_palavra(vocabulo: Vocabulo):
    try:
        for cadapalavra in range(len(vocabulo.palavras_unicas)): 
            retorno = await inserirPalavraMDB(
                vocabulo.palavras_unicas[cadapalavra], 
                vocabulo.voto_ingles, 
                vocabulo.voto_portugues
                )
        print (retorno)
        # alert("Palavras inseridas")
        return retorno
    except Exception as e:
        traceback.print_exc()
        return {"Inserir palavra": "Falhou"}

@app.post("/backend/apagarpalavra")
async def apagar_palavra(vocabulo: str):
    try:
        apagarPalavraMDB(vocabulo)       
    except Exception as e:
        traceback.print_exc()
        return {"Apagar palavra": "Falhou"}