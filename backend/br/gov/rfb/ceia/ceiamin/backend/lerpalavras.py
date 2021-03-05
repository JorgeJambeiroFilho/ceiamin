from br.gov.rfb.ceia.ceiamin.backend.minceiamongo import getBotMongoDB
from br.gov.rfb.ceia.ceiamin.backend.palavras import Palavras


async def lerPalavrasMDB():
    mdb = getBotMongoDB()
    collection = mdb.palavras
    palavras = []
    async for document in collection.find():
        palavra = [
            document["_id"],
            document.get("votoIngles",0),
            document.get("votoPortugues",0),
            document.get("probabilidadeIngles",0),
            document.get("probabilidadePortugues",0)
        ] 
        palavras.append(palavra)
    return Palavras(palavras)


async def inserirPalavraMDB(Palavra, votoI, votoP):
    mdb = getBotMongoDB()
    collection = mdb.palavras
    try:
        collection.insert_one({
            "_id": Palavra,
            "votoIngles": votoI,
            "votoPortugues": votoP
        })   
        retorno = ({ 
            "Inserir palavra MDB": "ok" , 
            "Palavra": Palavra, 
            "Voto Inglês": votoI, 
            "Voto Português": votoP
        })
        print (retorno)
    except Exception as e:
        print (e)


async def apagarPalavraMDB(vocabulo):
    mdb = getBotMongoDB()
    collection = mdb.palavras
    await collection.delete_many({ "_id": vocabulo })   
    retorno = ({ 
        "Apagar palavra MDB": "ok" , 
        "Palavra": vocabulo
    })
    print (retorno)
    return retorno


async def votarPalavraMDB(Palavra, votoI, votoP):
    mdb = getBotMongoDB()
    collection = mdb.palavras
    await collection.update_one(
        {"_id": Palavra},
        {'$inc': {
            "votoIngles": votoI,
            "votoPortugues": votoP
        }
    })   
    retorno = ({ 
        "Votar palavra MDB": "ok" , 
        "Palavra": Palavra, 
        "Voto Inglês": votoI, 
        "Voto Português": votoP
    })
    print (retorno)
    return retorno