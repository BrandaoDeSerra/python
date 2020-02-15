import nltk.corpus

nltk.download('mac_morpho')
sentencas = nltk.corpus.mac_morpho.tagged_sents()

# print(len(sentencas)) #51397 total
# print(sentencas[10])

sentencas_lowercase = [[(p.lower(),t) for (p,t) in sentenca] for sentenca in sentencas if sentenca]

sentencas_treinamento = sentencas_lowercase[5000:] # 46397
sentencas_teste = sentencas_lowercase[:5000]       #  5000

# >>>>> Rotuladores

#rotulador base
rotulador0 = nltk.DefaultTagger('N')
print(rotulador0.evaluate(sentencas_teste)) # verificar a curácia

#unigrama
rotulador1 = nltk.UnigramTagger(sentencas_treinamento,backoff=rotulador0)
print(rotulador1.evaluate(sentencas_teste))# verificar a curácia

#Bigrama
rotulador2 = nltk.BigramTagger(sentencas_treinamento,backoff=rotulador1)
print(rotulador2.evaluate(sentencas_teste))# verificar a curácia

#Trigrama
rotulador3 = nltk.TrigramTagger(sentencas_treinamento,backoff=rotulador2)
print(rotulador3.evaluate(sentencas_teste))# verificar a curácia

#N-grama
rotulador4 = nltk.NgramTagger(sentencas_treinamento,backoff=rotulador3)
print(rotulador4.evaluate(sentencas_teste))# verificar a curácia

# HMM modelo oculto de MARKOV
rotulador5 = nltk.HiddenMarkovModelTagger(sentencas_treinamento,)
print(rotulador5.evaluate(sentencas_teste))# verificar a curácia
