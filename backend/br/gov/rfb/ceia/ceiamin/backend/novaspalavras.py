from br.gov.rfb.ceia.ceiamin.backend.minceiamongo import getBotMongoDB


async def palavrasCarregamentoInicial():
    mdb = getBotMongoDB()
    collection = mdb.palavras
    carregadas = []

    async for document in collection.find({}):
        carregadas.append(document["vocabulo"])
    return carregadas