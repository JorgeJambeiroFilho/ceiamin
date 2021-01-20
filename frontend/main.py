#Este arquivo tem que se chamar "main.py" para ser encontrado pelo servidor web (uvicorn)
import json
import traceback
from datetime import datetime
from aiohttp import ClientResponse, ClientSession
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uuid
from dynaconf import settings
from multidict import CIMultiDict
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response, PlainTextResponse
import jwt
import aiohttp

USE_REVPROXY = False

#para rodar sem intermediação do nginx, comente esta linha
if USE_REVPROXY:
    dir = "/app/"
    backprefix = ""
else:
    dir = ""
    backprefix = "http://127.0.0.1:8001"



app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory=dir+"static"), name="static")

secret = str(uuid.uuid1())


@app.get("/frontend", response_class=HTMLResponse)
async def read_items(request:Request):
    #uso este código para redirecionar o navegador
    if not await checkSession(request):
        return get_oauth2_login_url_intern(request)

    # usaria este código em um método do backend, para só recusar um pedido e deixar que o javascript se virasse com a redirecionamento
    #if not await checkSession(request):
    #    return PlainTextResponse("Sessão indefinida ou expirada", status_code=403)

    fp = open(dir + "static/ceiamin.html")
    text = fp.read()
    #ftext = text.format(backprefix=backprefix) # o format do python atrapalha o uso de mustache no vue.js
    ftext = text.replace("{backprefix}", backprefix)
    return ftext



def get_oauth2_login_url_intern(request: Request):
    host = request.headers["host"]
    if "X-Forwarded-Ssl" in request.headers and request.headers["X-Forwarded-Ssl"]=='on':
        protocol = "https"
    else:
        protocol = request.url.scheme

    print(request.headers)

    state = str(uuid.uuid1())
    nonce = 456
    cid = "ceiamin"

    callback = protocol + "://" + host + "/frontend/oauth2Callback/"

    url = "{burl}?client_id={cid}&response_type=code&state={state}&nonce={nonce}&redirect_uri={callback}"\
          .format(burl=settings.OAUTH2_AUTHORIZATION_URL, nonce=nonce, state=state, cid=cid, callback=callback)

    response = RedirectResponse(url=url)
    response.set_cookie(key="ceiamin_oauth_state", value=state, path="/")
    print("state "+state)
    return response


async def checkSession(request:Request):

    if "ceiaminsession" not in request.cookies:
        return False

    session_str = request.cookies["ceiaminsession"]
    session_bytes = session_str.encode("utf-8")

    try:
        session_data = jwt.decode(session_bytes, secret, algorithms='HS256')
        if "timeini" not in session_data:
            return False
        timen = datetime.now().timestamp()
        timeini = float(session_data["timeini"])
        if timen - timeini > 12 * 60 * 60:
            return False
        return True
    except jwt.exceptions.InvalidTokenError as ex:
        return False


@app.get("/frontend/oauth2Callback")
async def oauth2_callback(request:Request):

    host = request.headers["host"]
    if "X-Forwarded-Ssl" in request.headers and request.headers["X-Forwarded-Ssl"] == 'on':
        protocol = "https"
    else:
        protocol = request.url.scheme

    cid = "ceiamin"

    callback = protocol+"://" + host + "/frontend/oauth2Callback/"

    state = request.query_params['state']
    #session_state = request.rel_url.query['session_state']
    saved_state = request.cookies["ceiamin_oauth_state"]
    code = request.query_params['code']

    form = aiohttp.FormData({"grant_type":"authorization_code", "code":code, "client_id":cid, "redirect_uri": callback})

    resp: ClientResponse = None
    try:
        if state != saved_state:
            raise Exception("State "+state+" != "+saved_state)
        openClientSession: ClientSession = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=(settings.TEST==0)))
        resp: ClientResponse = await openClientSession.post(settings.OAUTH2_TOKEN_URL, data=form())
        body = await resp.read()
        print("Corpo da resposta HTTP para obter token")
        print(body)
        jsonToken = json.loads(body)
        key = "Bearer " + jsonToken["access_token"]
        aheaders = CIMultiDict()
        aheaders.add("Authorization", key)
        userInfo: ClientResponse = await openClientSession.get(settings.OAUTH2_USERINFO_URL, headers=aheaders)
        body = await userInfo.read()
        jsonUser = json.loads(body)

    except:
        traceback.print_exc()
        res = PlainTextResponse("Autorização falhou.", status_code=403)
        return res
    finally:
        if resp:
            resp.close()

    sessionId = str(uuid.uuid1())
    encoded_jwt = jwt.encode({'session': sessionId, 'user': jsonUser["preferred_username"], "timeini":str(datetime.now().timestamp()) }, secret, algorithm='HS256')
    if isinstance(encoded_jwt, str):
        encoded_jwt_str = encoded_jwt
    else:
        encoded_jwt_str = encoded_jwt.decode("utf-8")

    response = RedirectResponse("/frontend")
    response.set_cookie("ceiaminsession", encoded_jwt_str, path="/")

    return response