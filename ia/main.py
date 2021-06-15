from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import numpy as np

from br.gov.rfb.ceia.ceiamin.backend.lerpalavras import probPalavraMDB



from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import make_scorer
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

import pickle

app = FastAPI()

class Prob(BaseModel):
    vocabulo: str
    prob_ingles: Optional[int] = 0
    prob_portugues: Optional[int] = 0

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/treina")
async def treina():
    
    with open('palavras_inglesas.txt', encoding='ISO-8859-1') as f:
        palavras_inglesas = f.read()
        #print(palavras_inglesas)

    vocabulario_ingles = []
    inicio=0
    fim=len(palavras_inglesas)

    while inicio <= fim:
        palavra = ''
        while inicio < fim and palavras_inglesas[inicio] != ' ':
            palavra += palavras_inglesas[inicio]
            inicio += 1
        inicio += 1
        if palavra != '':
            vocabulario_ingles.append(palavra)

    #print(len(vocabulario_ingles))
    vocabulario_ingles = list(dict.fromkeys(vocabulario_ingles))
    #print(len(vocabulario_ingles))

    with open('palavras_portuguesas.txt', encoding='ISO-8859-1') as f:
        palavras_portuguesas = f.read()
        #print(palavras_portuguesas)

    vocabulario_portugues = []
    inicio=0
    fim=len(palavras_portuguesas)

    while inicio <= fim:
        palavra = ''
        while inicio < fim and palavras_portuguesas[inicio] != ' ':
            palavra += palavras_portuguesas[inicio]
            inicio += 1
        inicio += 1
        if palavra != '':
            vocabulario_portugues.append(palavra)

    #print(len(vocabulario_portugues))
    vocabulario_portugues = list(dict.fromkeys(vocabulario_portugues))
    #print(len(vocabulario_portugues))

    ingles = np.zeros(698).astype(np.int8)
    for i in range(340):
        ingles[i]=1

    portugues = np.zeros(698).astype(np.int8)
    for i in range(358):
        portugues[340+i]=1

    ingles = list(ingles)
    portugues = list(portugues)

    vocabulario = vocabulario_ingles + vocabulario_portugues

    d = {'Vocabulario': vocabulario, 'Ingles': ingles, 'Portugues': portugues}
    palavras_rotulos = pd.DataFrame(data=d)

    categories = ['Ingles', 'Portugues']
    train, test = train_test_split(palavras_rotulos)
    X_train = train.Vocabulario
    X_test = test.Vocabulario
    #print(X_train.shape)
    #print(X_test.shape)

    LOGREG_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer()),
                    ('log', OneVsRestClassifier(LogisticRegression(dual=False), n_jobs=1))])

    LOGREG_params = {'tfidf__analyzer': ['char'], 'tfidf__ngram_range': [(1, 3),(1, 4)], 'log__estimator__C': [10.0], 'log__estimator__penalty': ["l2"]}

    my_scorer = make_scorer(recall_score)
    LOGREG_gs = GridSearchCV(LOGREG_pipeline, param_grid=LOGREG_params, scoring=my_scorer, cv = 3, verbose = 1, n_jobs = -1)

    for category in categories:
        print('... Processing {}'.format(category))

        LOGREG_gs.fit(X_train, train[category])

        prediction = LOGREG_gs.predict(X_test)
        
        print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))
        print('Test sensitivity is {}'.format(recall_score(test[category], prediction)))
        print('Best Parameters are {}'.format(LOGREG_gs.best_params_))

        #probabilities = LOGREG_gs.predict_proba(X_test)

    filename = 'ceiamin_IA_model.sav'

    pickle.dump(LOGREG_gs, open(filename, 'wb'))
    return {"message": "Modelo Treinado"}

@app.post("/backend/calculaprobpalavra")
async def calcula_prob_palavra(palavra: str):
    filename = 'ceiamin_IA_model.sav'
    LOGREG_gs = pickle.load(open(filename, 'rb'))
    serie_palavra = pd.Series([palavra])
    probabilidade = LOGREG_gs.predict_proba(serie_palavra)
    prob = Prob
    prob.vocabulo = palavra
    prob.prob_ingles = probabilidade[0,0]
    prob.prob_portugues = probabilidade[0,1]
    #return {"palavra": prob.vocabulo, 'prob ingles': prob.prob_ingles, 'prob portuges': prob.prob_portugues}
    try:
        retorno = await probPalavraMDB(
            prob.vocabulo, 
            prob.prob_ingles, 
            prob.prob_portugues
            )
        print (retorno)
        return retorno
    except Exception as e:
        traceback.print_exc()
        return {"Gravar probabilidade palavra": "Falhou"}
        