import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

from collections import Counter

import os
import ast
import spacy

sp=spacy.load('pt_core_news_sm')
#carregando lingua portuguesa
# CASO ISTO NAO FUNCIONE É NECESSARIO ANTES IR NO TERMINAL/CMD E INSERIR O COMANDO
#python -m spacy download pt
# para que o SpaCy baixe corpora da lingua portuguesa


lematizador=WordNetLemmatizer()
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('rlsp')

tokenizador_sentencas=nltk.data.load('tokenizers/punkt/portuguese.pickle')

#debugger
def deu_ruim(*a):
    for i in a:
        print(i)

#pega arquivo .LVOC com dicionario de lemas e ocorrencias e importa
def arq_2_lemas(caminho):
    if not os.path.exists(caminho):
        deu_ruim('caminho')
        return Counter()
    fp=None
    try:
        u=os.path.split(caminho)
        FORMATO=u[len(u)-1].split('.')[1].lower()
        #print(FORMATO)
        if FORMATO != 'lvoc':
            return Counter()
    except Exception as e:
        deu_ruim(e)
        return Counter()
    try :
        fp=open(caminho, encoding='utf-8', errors='ignore')
        t=fp.read()
        tx=t.replace("})","}").replace("Counter(",'')
        resp=ast.literal_eval(tx)
        return Counter(resp)
    except Exception as e:
        deu_ruim(e)
        return Counter()

#idem pra tokens
def arq_2_tokens(caminho):
    if not os.path.exists(caminho):
        deu_ruim('caminho')
        return Counter()
    fp=None
    try:
        u=os.path.split(caminho)
        FORMATO=u[len(u)-1].split('.')[1].lower()
        #print(FORMATO)
        if FORMATO != 'voc':
            return Counter()
    except Exception as e:
        deu_ruim(e)
        return Counter()
    try :
        fp=open(caminho, encoding='utf-8', errors='ignore')
        t=fp.read()
        tx=t.replace("})","}").replace("Counter(",'')
        resp=ast.literal_eval(tx)
        return Counter(resp)
    except Exception as e:
        deu_ruim(e)
        return Counter()

#abre arquivo JSON e o salva num dicionario
def JSONopen(narq):
    jfp=open(narq,encoding='utf-8',errors='ignore')
    data=json.load(jfp)
    return data

#guarda tokens em arquivo
def tokens_2_arq(voc,nome):
    fp=open(nome+'.VOC','w', encoding='utf-8', errors='ignore')
    V=Counter(voc)
    print(V)
    fp.write(str(V))
    fp.close()
    return  os.path.join(os.getcwd(),nome+'.VOC')
''

#guarda lemas em arquivo
def lemas_2_arq(voc,nome):
    fp=open(nome+'.LVOC','w', encoding='utf-8', errors='ignore')
    V=Counter(voc)
    print(V)
    fp.write(str(V))
    fp.close()
    return  os.path.join(os.getcwd(),nome+'.LVOC')


#classe tem odio : indice de for i in a['has_anger']

#probabilidade
def P(A,Ω):
    if not Ω :
        return None
    return len(A)/len(Ω)


def priori(base):
    k=[]
    for i in base['has_anger']:
        if base['has_anger'][i]!=None:
            k.append(i)
    return P(k,base['txt'])


#Limpa dataset e lematiza
def limpa_base_e_lemmatiza(dataset,idioma,tokenizador_stcs):
    lemas=[]
    tokens=[]
    new_dataset={}
    for ip in dataset:
        #print('---------')
#        print(str(dataset[ip]))
        k = re.sub(r'>>[0-9]+', '', str(dataset[ip]))
        k = re.sub(r'[\#][0-9a-zA-Z\_]+', '', k)
        k = re.sub(r'[\@][0-9a-zA-Z\_]+', '', k)
        stopword='>'
        frases=k.replace('>',' ')
        frases=k.replace('.',' ')
        frases=k.replace('?',' ')

        sentencas=tokenizador_stcs.tokenize(frases)
        for sentenca in sentencas:
            #print('<<S>',sentenca,">")
            for token in idioma(sentenca):
                tokens.append(token)
                lemas.append(token.lemma_)
                #print('<[Token] ',token,' > , <[Lema]',token.lemma_,'>')
#        new_dataset[ip]=k
#    return new_dataset
    return tokens_2_arq(tokens,'vocab_tweets'),lemas_2_arq(lemas,'vocab_tweets')



a=JSONopen('df_dataset.json')
#for i in a:
#    print(i)

#print(a['has_anger'],'811 tem odio',a['txt']['811'])
#print('textos com ódio')
#for i in a['has_anger']:
#    if a['has_anger'][i]!= None:# and i==63552:
#        t=a['txt'][i]
#        print(t.find('#'),t)

#print(a['origin'])

limpa_base_e_lemmatiza(a['txt'],sp,tokenizador_sentencas)
print(priori(a))
#print(arq_2_lemas('vocab_tweets.LVOC'))