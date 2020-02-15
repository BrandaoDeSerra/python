# Bibliotecas
from nltk.util import ngrams
import collections
import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

# Carregar dados
proposicoes = pd.read_csv("./arquivos/proposicoes_normalizadas.csv")
proposicoes = list(proposicoes['texto'])

# Modelo de linguagem
nlp = spacy.load("pt_core_news_sm")

# N-Gramas
# Tokens coleção
tokens = []
for t in proposicoes:
    doc = nlp(t)
    tokens.extend([p.text for p in doc])

# N-gramas
N = 2
ngramas = ngrams(tokens, N)
frequencia_ngramas = collections.Counter(ngramas)
for x in frequencia_ngramas.most_common(10):
    print(x)

# Modelos Vetoriais
textos_exemplo = ['Este é o primeiro documento',
                  'Este documento é o segundo documento',
                  'E este é o terceiro, o derradeiro']
## Booleano
# Vetorizador booleano
vetorizador = CountVectorizer(binary=True)
matriz_booleana = vetorizador.fit_transform(textos_exemplo)
print(cosine_similarity(matriz_booleana))

matriz_booleana_df = pd.DataFrame(matriz_booleana.todense(), index=['Doc1', 'Doc2', 'Doc3'],columns=vetorizador.get_feature_names())
print(matriz_booleana_df)

# Vetorizador TF-IDF
vetorizador = TfidfVectorizer(norm='l1')
matriz_tfidf = vetorizador.fit_transform(textos_exemplo)

matriz_tfidf_df = pd.DataFrame(matriz_tfidf.todense(), index=['Doc1', 'Doc2', 'Doc3'],columns=vetorizador.get_feature_names())
print(matriz_tfidf_df)

# Vetores de Palavras
proposicoes_tokenizadas = []
for t in proposicoes:
    proposicoes_tokenizadas.append(t.split())

model = Word2Vec(proposicoes_tokenizadas, size=100, window=5, min_count=1, workers=4)
print(model.wv.most_similar(positive=['criança'], topn=10))
print(model.wv.most_similar(positive=['saúde'], topn=10))
print(model.wv.most_similar(positive=['valores'], topn=10))

# Similaridade textual
similaridades = cosine_similarity(matriz_tfidf)
similaridades_df = pd.DataFrame(similaridades, columns=['Doc1', 'Doc2', 'Doc3'], index=['Doc1', 'Doc2', 'Doc3'])
print(similaridades_df)



