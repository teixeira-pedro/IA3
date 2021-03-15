import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

from collections import Counter

import os

import spacy

sp=spacy.load('pt_core_news_sm')
#carregando lingua portuguesa
# CASO ISTO NAO FUNCIONE É NECESSARIO ANTES IR NO TERMINAL/CMD E INSERIR O COMANDO
#python -m spacy download pt
# para que o SpaCy baixe corpora da lingua portuguesa


lematizador=WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('rlsp')

tokenizador_sentencas=nltk.data.load('tokenizers/punkt/portuguese.pickle')

def JSONopen(narq):
    jfp=open(narq,encoding='utf-8',errors='ignore')
    data=json.load(jfp)
    return data

def tokens_2_arq(voc,nome):
    fp=open(nome+'.VOC','w', encoding='utf-8', errors='ignore')
    V=Counter(voc)
    print(V)
    fp.write(str(V))
    fp.close()
    return  os.path.join(os.getcwd(),nome+'.LVOC')

def lemas_2_arq(voc,nome):
    fp=open(nome+'.LVOC','w', encoding='utf-8', errors='ignore')
    V=Counter(voc)
    print(V)
    fp.write(str(V))
    fp.close()
    return  os.path.join(os.getcwd(),nome+'.LVOC')



def limpa_base(dataset,idioma,tokenizador_stcs):
    lemas=[]
    tokens=[]
    new_dataset={}
    for ip in dataset:
        print('---------')
#        print(str(dataset[ip]))
        k = re.sub(r'>>[0-9]+', '', str(dataset[ip]))
        k = re.sub(r'[\#][0-9a-zA-Z\_]+', '', k)
        k = re.sub(r'[\@][0-9a-zA-Z\_]+', '', k)
        stopword='>'
        frases=k.replace('>','.')

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
for i in a:
    print(i)

#print(a['has_anger'],'811 tem odio',a['txt']['811'])
#print('textos com ódio')
#for i in a['has_anger']:
#    if a['has_anger'][i]!= None:# and i==63552:
#        t=a['txt'][i]
#        print(t.find('#'),t)

print(a['origin'])

limpa_base(a['txt'],sp,tokenizador_sentencas)
