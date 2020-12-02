#Este arquivo tem que se chamar "main.py" para ser encontrado pelo servidor web (uvicorn)

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

USE_REVPROXY = False

#para rodar sem intermediação do ngix, comente esta linha
if USE_REVPROXY:
    dir = "/app/"
    backprefix = ""
else:
    dir = ""
    backprefix = "http://127.0.0.1:8001"



app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory=dir+"static"), name="static")


@app.get("/frontend", response_class=HTMLResponse)
async def read_items():
    fp = open(dir + "static/ceiamin.html")
    text = fp.read()
    #ftext = text.format(backprefix=backprefix) # o format do python atrapalha o uso de mustache no vue.js
    ftext = text.replace("{backprefix}", backprefix)
    return ftext
