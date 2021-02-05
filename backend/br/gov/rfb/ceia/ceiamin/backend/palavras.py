from br.gov.rfb.ceia.ceiamin.backend.minceiamongo import getBotMongoDB
import os


class Palavras:
    def __init__(self, palavra):
        self.palavras = palavra
        # self.palavras = []
        # self.palavras.append(palavra)


# class Palavras:
#     def __init__(self):
#         mdb = getBotMongoDB()
#         collection = mdb.palavras
#         self.palavras = []
#         for document in collection.find():
#             palavra = [
#                 document["vocabulo"],
#                 document.get("votoIngles",0),
#                 document.get("votoPortugues",0)
#             ] 
#         self.palavras.append(palavra)
        

class initialPalavras:
    def __init__(self):
        self.palavras = []
        #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fp = open("palavras.txt", mode="r", encoding="utf-8")
        lin = fp.readline()
        while (lin):
            #print(lin)
            if (lin[0]!='#'):
                lis = lin.split()
                palavra = [lis[1], lis[3]]
                self.palavras.append(palavra)
            lin = fp.readline()