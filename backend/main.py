from fastapi import FastAPI
from enum import Enum

from br.gov.rfb.ceia.ceiamin.backend.palavras import Palavras
from fastapi.middleware.cors import CORSMiddleware



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
