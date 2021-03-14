import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

dataset = pd.read_csv('./arquivos/Tweets_Mg.csv', encoding='utf-8')
print(dataset.count())
print(dataset[dataset.Classificacao == 'Neutro'].count())
print(dataset[dataset.Classificacao == 'Positivo'].count())
print(dataset[dataset.Classificacao == 'Negativo'].count())


def PreprocessamentoSemStopWords(instancia):
    # remove links dos tweets
    # remove stopwords
    instancia = re.sub(r"http\S+", "", instancia).lower().replace(',', '').replace('.', '').replace(';', '').replace(
        '-', '')
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))
    palavras = [i for i in instancia.split() if not i in stopwords]
    return " ".join(palavras)


def Stemming(instancia):
    stemmer = nltk.stem.RSLPStemmer()
    palavras = []
    for w in instancia.split():
        palavras.append(stemmer.stem(w))
    return " ".join(palavras)


def Preprocessamento(instancia):
    # remove links, pontos, virgulas,ponto e virgulas dos tweets
    # coloca tudo em minusculo
    instancia = re.sub(r"http\S+", "", instancia).lower().replace(',', '').replace('.', '').replace(';', '').replace(
        '-', '').replace(':', '')
    return instancia


#print(PreprocessamentoSemStopWords('Eu não gosto do partido, e também não votaria novamente nesse governante!'))

tweets = dataset['Text'].values
classes = dataset['Classificacao'].values

vectorizer = CountVectorizer(analyzer="word")
freq_tweets = vectorizer.fit_transform(tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets, classes)

# defina instâncias de teste dentro de uma lista
testes = ['Esse governo está no início, vamos ver o que vai dar', 'Estou muito feliz com o governo de Minas esse ano',
          'O estado de Minas Gerais decretou calamidade financeira!!!',
          'A segurança desse país está deixando a desejar', 'O governador de Minas é do PT']
freq_testes = vectorizer.transform(testes)

# Fazendo a classificação com o modelo treinado.
modelo.predict(freq_testes)

# Fazendo o cross validation do modelo
resultados = cross_val_predict(modelo, freq_tweets, classes, cv=10)

# Medindo a acurácia média do modelo
metrics.accuracy_score(classes, resultados)

# Medidas de validação do modelo
sentimento = ['Positivo', 'Negativo', 'Neutro']
print(metrics.classification_report(classes, resultados, sentimento))

# Matriz de confusão
print(pd.crosstab(classes, resultados, rownames=['Real'], colnames=['Predito'], margins=True))

vectorizer = CountVectorizer(ngram_range=(1, 2))
freq_tweets = vectorizer.fit_transform(tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets, classes)

resultados = cross_val_predict(modelo, freq_tweets, classes, cv=10)
metrics.accuracy_score(classes, resultados)

sentimento = ['Positivo', 'Negativo', 'Neutro']
print(metrics.classification_report(classes, resultados, sentimento))

print(pd.crosstab(classes, resultados, rownames=['Real'], colnames=['Predito'], margins=True))
