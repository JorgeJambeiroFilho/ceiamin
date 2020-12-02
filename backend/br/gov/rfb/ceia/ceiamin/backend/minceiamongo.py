import traceback

import motor.motor_asyncio
from bson import Binary, ObjectId
from dynaconf import settings

ceiaMinMongoClient: motor.motor_asyncio.AsyncIOMotorClient = None

if settings.TEST:
    print("Executando com as configuração do docker")
else:
    print("Executando com as configuração de depuração")

def getBotMongoDB():
    global ceiaMinMongoClient

    if ceiaMinMongoClient is None:
        try:
            ceiaMinMongoClient = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT, username=settings.MONGO_DB_USER, password=settings.MONGO_DB_PASSWORD)
        except:
            traceback.print_exc()
    return ceiaMinMongoClient.ceiamindb

def closeBotMongoDb():
    if ceiaMinMongoClient is not None:
        ceiaMinMongoClient.close()
