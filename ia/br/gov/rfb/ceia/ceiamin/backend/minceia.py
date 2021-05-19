from br.gov.rfb.ceia.ceiamin.backend.minceiamongo import getBotMongoDB
from br.gov.rfb.ceia.ceiamin.backend.palavras import initialPalavras


async def wordInitialLoad():
    mdb = getBotMongoDB()
    palavras = initialPalavras()
    for palavra in palavras.palavras:
        palavraIngles = { palavra[0], 1, 0 }
        palavraPortugues = { palavra[1], 0, 1 }
        await mdb.palavras.insert_one(palavraIngles)
        await mdb.palavras.insert_one(palavraPortugues)
        
