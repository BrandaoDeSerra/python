from gensim.summarization.summarizer import summarize

# Leitura de dados
redacao = None
with open("./arquivos/redacao.txt", 'r') as redacao_file:
    redacao = redacao_file.read().strip()
print(redacao)
print("--------------------------------------------------------------")
# Sumarização com metade das sentenças
print(summarize(redacao, ratio=0.3))
print("--------------------------------------------------------------")