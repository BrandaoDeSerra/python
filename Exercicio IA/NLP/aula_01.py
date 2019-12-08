'''Normalização de Texto '''

import pandas as pd
import nltk
import spacy
import unicodedata
import string
from collections import Counter
from itertools import chain


# Transformar para minusculas
exemplo_texto = "Meu nome é Marcelo Pita"
print(exemplo_texto.lower())

# Transformar coluna texto para minusculas
proposicoes = pd.read_csv("./arquivos/proposicoes.csv") # Carregar dados
proposicoes['texto'] = proposicoes['texto'].map(lambda x: x.lower())
print(proposicoes)

# Remover palavras com menos de 3 e mais de 25 caracteres
exemplo_texto = "este é um exemplo de texto com sahhsdhidisdiasdjisajdijdisajd palavras pequenas e grandes"
palavras_adequadas = []
for p in exemplo_texto.split():
    tamanho_p = len(p)
    if tamanho_p >= 3 and tamanho_p <= 25:
        palavras_adequadas.append(p)
exemplo_texto_ok = " ".join(palavras_adequadas)
print(exemplo_texto_ok)

proposicoes_tamanho_ok = []

for index, row in proposicoes.iterrows():
    texto = row[0]
    palavras_adequadas = []
    for p in texto.split():
        tamanho_p = len(p)
        if 3 <= tamanho_p <= 25:
            palavras_adequadas.append(p)
    proposicoes_tamanho_ok.append(" ".join(palavras_adequadas))

proposicoes['texto'] = proposicoes_tamanho_ok
print(proposicoes)

nltk.download('stopwords')
nltk.download('rslp')
#!python3 -m spacy download pt_core_news_sm

# >>>>> Remoção de stopwords
# Carregar stopwords
stopwords = nltk.corpus.stopwords.words('portuguese')
print(stopwords)

# Exemplo
exemplo_texto = "este é um texto com stopwords"
palavras_adequadas = [p for p in exemplo_texto.split() if p not in stopwords]
exemplo_texto_ok = " ".join(palavras_adequadas)
print(exemplo_texto_ok)

proposicoes_stopwords_ok = []

for index, row in proposicoes.iterrows():
    texto = row[0]
    palavras_adequadas = [p for p in texto.split() if p not in stopwords]
    proposicoes_stopwords_ok.append(" ".join(palavras_adequadas))

proposicoes['texto'] = proposicoes_stopwords_ok
print(proposicoes)

# >>>>> Remover pontuação / Caracter Especial
nlp = spacy.load("pt_core_news_sm")
pontuacao = string.punctuation.strip()
pontuacao_lista = []
for pont in pontuacao.strip():
    pontuacao_lista.append(pont)
pontuacao_lista.append('º')
pontuacao_lista.append('ª')
pontuacao_lista.append('...')
pontuacao_lista.append('“')
pontuacao_lista.append('”')
pontuacao_lista.append('')
print(pontuacao_lista)

exemplo_texto = "ei! você aí... não acha isso um absurdo?!"
exemplo_texto_tokens = nlp(exemplo_texto)
exemplo_texto_tokens = [str(t) for t in exemplo_texto_tokens if str(t) not in pontuacao_lista]
exemplo_texto_ok = " ".join(exemplo_texto_tokens)
print(exemplo_texto_ok)

proposicoes_ok = []
for index, row in proposicoes.iterrows():
    texto = row[0]
    texto_tokens = nlp(texto)
    texto_tokens = [str(t) for t in texto_tokens if str(t) not in pontuacao_lista]
    proposicoes_ok.append(" ".join(texto_tokens))
proposicoes['texto'] = proposicoes_ok
print(proposicoes)

# >>>>> Estemização
estemizador_port = nltk.stem.RSLPStemmer()
exemplo_texto = "água mole pedra dura tanto bate até que fura"
palavras_estemizadas = []
for p in exemplo_texto.split():
    palavras_estemizadas.append(estemizador_port.stem(p))
print(palavras_estemizadas)

proposicoes_estemizadas = []
for index, row in proposicoes.iterrows():
    texto = row[0]
    texto_tokens_estemizados = [estemizador_port.stem(t) for t in texto.split()]
    proposicoes_estemizadas.append(" ".join(texto_tokens_estemizados))
proposicoes['texto_estemizado'] = proposicoes_estemizadas
print(proposicoes)

# >>>>> Lematização
exemplo_texto = "água mole pedra dura tanto bate até que fura"
lemas = []
exemplo_texto_tokens = nlp(exemplo_texto)
for t in exemplo_texto_tokens:
    lemas.append(t.lemma_)
print(lemas)

proposicoes_lemas = []
for index, row in proposicoes.iterrows():
    texto = row[0]
    texto_tokens = nlp(texto)
    lemas = []
    for t in texto_tokens:
        lemas.append(t.lemma_)
    proposicoes_lemas.append(" ".join(lemas))
proposicoes['texto_lemas'] = proposicoes_lemas
print(proposicoes)

# >>>>> Remoção de acentuação
exemplo_texto = "água mole pedra dura tanto bate até que fura"
print(unicodedata.normalize('NFKD', exemplo_texto).encode('ASCII', 'ignore'))

proposicoes['texto'] = proposicoes['texto'].map(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))
proposicoes['texto_estemizado'] = proposicoes['texto_estemizado'].map(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))
proposicoes['texto_lemas'] = proposicoes['texto_lemas'].map(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore'))

proposicoes['texto'] = proposicoes['texto'].str.decode('utf-8')
proposicoes['texto_estemizado'] = proposicoes['texto_estemizado'].str.decode('utf-8')
proposicoes['texto_lemas'] = proposicoes['texto_lemas'].str.decode('utf-8')

print(proposicoes)


# >>>>> Remoção de palavras de baixa frequência
frequencia_minima = 5
proposicoes_tokens = proposicoes['texto'].str.split().tolist()
c = Counter(chain.from_iterable(proposicoes_tokens))
proposicoes['texto'] = [' '.join([j for j in i if c[j] > frequencia_minima]) for i in proposicoes_tokens]
proposicoes_tokens = proposicoes['texto_estemizado'].str.split().tolist()
c = Counter(chain.from_iterable(proposicoes_tokens))
proposicoes['texto_estemizado'] = [' '.join([j for j in i if c[j] > frequencia_minima]) for i in proposicoes_tokens]
proposicoes_tokens = proposicoes['texto_lemas'].str.split().tolist()
c = Counter(chain.from_iterable(proposicoes_tokens))
proposicoes['texto_lemas'] = [' '.join([j for j in i if c[j] > frequencia_minima]) for i in proposicoes_tokens]
print(proposicoes)