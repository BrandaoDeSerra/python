import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

def imprimir_top_palavras(lda, palavras, topn):
    probabilidades = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]
    for topico_idx, topico in enumerate(probabilidades):
        top_palavras_idx = topico.argsort()[:-topn - 1:-1]
        print("Tópico %d:" % topico_idx)
        for i in top_palavras_idx:
            print("        " + palavras[i] + "   " + str(round(topico[i], 6)))
    print()

# Textos das proposicoes
proposicoes = list(pd.read_csv("./arquivos/proposicoes.csv")['texto'])

nlp = spacy.load("pt_core_news_sm")

# Tokenização dos textos
textos_tokenizados = []
for texto in proposicoes:
    texto_tokenizado = nlp(texto)
    textos_tokenizados.append(texto_tokenizado)

# Identificação de partes da fala
textos_partes_fala = []
for tt in textos_tokenizados:
    textos_partes_fala.append([(p.text, p.pos_) for p in tt])

# Filtragem de partes da fala de interesse:
# NOUN, PROPN, ADJ, VERB
proposicoes_filtradas = []
for t in textos_partes_fala:
    texto_filtrado = []
    for palavra, parte_fala in t:
        if parte_fala in ['NOUN', 'PROPN', 'ADJ', 'VERB']:
            texto_filtrado.append(palavra)
    proposicoes_filtradas.append(" ".join(texto_filtrado).lower())

# Vetorizador TF (frequencia de termos nos documentos)
vetorizador_tf = CountVectorizer(max_df=0.5, min_df=3)
tf_textos = vetorizador_tf.fit_transform(proposicoes_filtradas)
print(tf_textos.todense())

# Número de tópicos
K = 20
alfa = 0.01
beta = 0.001
lda = LatentDirichletAllocation(n_components=20, max_iter=100, doc_topic_prior=alfa, topic_word_prior=beta, n_jobs=7, verbose=1)
lda.fit(tf_textos)

imprimir_top_palavras(lda, vetorizador_tf.get_feature_names(), 10)

