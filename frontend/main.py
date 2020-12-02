#Este arquivo tem que se chamar "main.py" para ser encontrado pelo servidor web (uvicorn)

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

#para rodar sem intermediação do ngix, comente esta linha
dir = "/app/"

app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory=dir+"static"), name="static")

