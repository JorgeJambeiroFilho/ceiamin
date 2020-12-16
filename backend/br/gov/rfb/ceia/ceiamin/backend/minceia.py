from br.gov.rfb.ceia.ceiamin.backend.minceiamongo import getBotMongoDB
from br.gov.rfb.ceia.ceiamin.backend.palavras import Palavras


async def wordInitialLoad():
    mdb = getBotMongoDB()
    palavras = Palavras()
    for palavra in palavras.palavras:
        pp = {"word":palavra[1]}
        pi = {"word":palavra[3]}
        await mdb.words.insert_one(pp)
        await mdb.words.insert_one(pi)
