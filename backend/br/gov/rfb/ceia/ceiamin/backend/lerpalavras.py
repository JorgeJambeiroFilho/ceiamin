from br.gov.rfb.ceia.ceiamin.backend.minceiamongo import getBotMongoDB
from br.gov.rfb.ceia.ceiamin.backend.palavras import Palavras

async def lerPalavrasMDB():
    mdb = getBotMongoDB()
    collection = mdb.palavras
    palavras = []
    async for document in collection.find():
        palavra = [
            document["vocabulo"],
            document.get("votoIngles",0),
            document.get("votoPortugues",0)
        ] 
        palavras.append(palavra)
    return Palavras(palavras)


async def inserirPalavraMDB(Palavra, votoI, votoP):
    mdb = getBotMongoDB()
    collection = mdb.palavras
    await collection.insert_one({
        "vocabulo": Palavra,
        "votoIngles": votoI,
        "votoPortugues": votoP
    })   
    # await collection.create_index([("vocabulo")])
    retorno = ({ 
        "Inserir palavra MDB": "ok" , 
        "Palavra": Palavra, 
        "Voto Inglês": votoI, 
        "Voto Português": votoP
    })
    print (retorno)
    return retorno

async def votarPalavraMDB(Palavra, votoI, votoP):
    mdb = getBotMongoDB()
    collection = mdb.palavras
    votarpalavra = await collection.find_one({"vocabulo": Palavra})
    oldIngles = votarpalavra["votoIngles"]
    oldPortugues = votarpalavra["votoPortugues"]
    await collection.update_one(
        {"vocabulo": Palavra},
        {'$set': {
            {"votoIngles": oldIngles + votoI},
            {"votoPortugues": oldPortugues + votoP}
        }
    })   
    retorno = ({ 
        "Votar palavra MDB": "ok" , 
        "Palavra": Palavra, 
        "Old Voto Inglês": oldIngles, 
        "Old Voto Português": oldPortugues,
        "Voto Inglês": votoI, 
        "Voto Português": votoP
    })
    print (retorno)
    return retorno

async def apagarPalavraMDB(vocabulo):
    mdb = getBotMongoDB()
    collection = mdb.palavras
    await collection.delete_one({ "vocabulo": vocabulo })   
    retorno = ({ 
        "Apagar palavra MDB": "ok" , 
        "Palavra": vocabulo
    })
    print (retorno)
    return retorno