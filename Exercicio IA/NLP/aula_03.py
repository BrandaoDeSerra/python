import spacy
import pandas as pd

nlp = spacy.load('pt_core_news_sm')

preposicoes = pd.read_csv("./arquivos/proposicoes.csv") # Carregar dados
preposicoes = list(preposicoes['texto'])

texto_tokenizados = []
for texto in preposicoes:
    texto_tokenizado = nlp(texto)
    texto_tokenizados.append(texto_tokenizado)

'''
texto_exemplo = "Você fez o trabalho que eu pedi, João?"
doc = nlp(texto_exemplo)
print([(token.text,token.pos_) for token in doc])

# Identificação de partes da fala",
textos_partes_fala = []
for tt in texto_tokenizados:
    textos_partes_fala.append([(p.text, p.pos_) for p in tt])

print(textos_partes_fala)

# Filtragem de partes da fala de interesse: NOUN, PROPN, ADJ, VERB"
proposicoes_filtradas = []
for t in textos_partes_fala:
    texto_filtrado = []
    for palavra, parte_fala in t:
        if parte_fala in ['NOUN', 'PROPN', 'ADJ', 'VERB']:
            texto_filtrado.append(palavra)
    proposicoes_filtradas.append(" ".join(texto_filtrado))
print(proposicoes_filtradas)
'''
# Exemplo Reconhecimento de Entidades nomeadas
texto_exemplo = "Diario de Pernambuco é um jornal publicado na cidade do Recife, no estado de Pernambuco, Brasil. É o mais antigo periódico em circulação da América Latina, fundado em 7 de novembro de 1825 pelo tipógrafo Antonino José de Miranda Falcão. Quando o Diario de Pernambuco foi fundado, o Recife ainda não era a capital do estado, fato que só ocorreu um ano e três meses depois."
doc = nlp(texto_exemplo)
print([(entity, entity.label_) for entity in doc.ents])

print(texto_tokenizados[200])
print([(entity, entity.label_) for entity in texto_tokenizados[200].ents])

print(texto_tokenizados[15])
print([(entity, entity.label_) for entity in texto_tokenizados[15].ents])