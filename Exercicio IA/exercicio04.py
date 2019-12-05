'''
Usando alguma biblioteca ou implementando diretamente em alguma linguagem de programação,
desenvolva uma solução para minimizar a função de Rosenbrock (em anexo). Faça testes pra
identificar um conjunto de parâmetros adequado. Plote o gráfico de evolução da solução.

Xmin / Ymin = -2
Xmax / Ymax = +2

minGlobal = +1 (x e y)

w = inicio 0.9 vai descendo ate 0.2
C1 É UM PESO PARA O MELHOR LOCAL
C2 É UM PESO PARA O MAIOR GLOBAL

R1 -> radomico de 0.0 a 1.0
R2 -> radomico de 0.0 a 1.0
'''
import random
import time
import matplotlib.pyplot as plt

# ##################################################
def fitness(particula):  # Rosenbrock
    x = particula[0]
    y = particula[1]
    a = 1.0 - x
    b = y - x * x
    return (b * b * 100.0) + (a * a)

# ##################################################
def calculaNovaVelocidade(particula, v):  # Calculo da velocidade por particula
    r1 = random.random() # faixa de 0.0 a 1.0
    r2 = random.random() # faixa de 0.0 a 1.0
    part_1 = (w * particula.velocidade[v])
    part_2 = (c1 * r1 * (particula.melhor_local_posicao[v] - particula.posicao[v]))
    part_3 = (c2 * r2 * (melhor_global_posicao[v] - particula.posicao[v]))
    return part_1 + part_2 + part_3

# ##################################################
class Particula:
    def __init__(self, qtdVariaveis, min_value, max_value):
        self.posicao = [0.0 for c in range(qtdVariaveis)]  # Iniciando array das posicoes
        self.velocidade = [0.0 for c in range(qtdVariaveis)]  # Iniciando array das velocidades
        for c in range(qtdVariaveis):
            self.posicao[c] = ((valorMaximo - valorMinimo) * random.random() + valorMinimo)  # Atualizando as posições iniciais
            self.velocidade[c] = ((valorMaximo - valorMinimo) * random.random() + valorMinimo)  # Atualizando as velocidades iniciais
        self.fitness = fitness(self.posicao)  # Calculando do fitness de cada posição das partículas
        self.melhor_local_posicao = list(self.posicao)  # posição da particula
        self.melhor_local = self.fitness  # melhor fitness da particula

# ##################################################
def init_plot():
    ax.scatter(2, 2, alpha=0.8, c='red', edgecolors='none', s=1)
    ax.scatter(-2, -2, alpha=0.8, c='red', edgecolors='none', s=1)
    ax.scatter(1, 1, alpha=0.8, c='red', edgecolors='none', s=30)

# ----------------------
# >>>>>>> INICIO <<<<<<<

qtdParticulasIniciais = 50  # Número de Partículas Iniciais

numeroDeDimensoes = 2  # Número de dimensões x e y
valorMinimo = -2  # Minimo valor para x e y
valorMaximo = +2  # Máximo valor para x e y

qtdIteracoes = 800  # Número de Iterações

w = 0.9  # Inércia  w (inicial) = 0,9 e diminui para w (final) = 0,2

c1 = 1.4  # peso para o melhor Local
c2 = 1.7  # peso para o melhor global

# Criando Enxame inicial
enxame = [Particula(numeroDeDimensoes, valorMinimo, valorMaximo) for c in range(qtdParticulasIniciais)]

melhor_global_posicao = [0.0 for c in range(numeroDeDimensoes)]
melhor_global = 99999999999999

# Analisando cada particula para atualizar o melor fitness Global, que é a minimização da função de Rosenbrick(fitness)
for particula in enxame:
    if particula.fitness < melhor_global:
        melhor_global = particula.fitness
        melhor_global_posicao = list(particula.posicao)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.title('Evolução PSO')
init_plot()

for ciclo in range(qtdIteracoes):

    for particula in enxame:
        x = particula.posicao[0]
        y = particula.posicao[1]
        ax.scatter(x, y, alpha=0.8, c='black', edgecolors='none', s=30)
    #time.sleep(2)

    # Inércia -> fator de desagregação / dispersão
    if w > 0.2 and ciclo % 50 == 0 and ciclo != 0:
        w = w - 0.1

    for particula in enxame:
        # Calculando a nova velocidade de cada partícula
        for v in range(numeroDeDimensoes):
            particula.velocidade[v] = calculaNovaVelocidade(particula, v)
            if particula.velocidade[v] < valorMinimo:
                particula.velocidade[v] = valorMinimo
            elif particula.velocidade[v] > valorMaximo:
                particula.velocidade[v] = valorMaximo

        # Verificando a nova posição usando a nova Velocidade, limitado pelos valores maximos e minimos definidos
        for i in range(numeroDeDimensoes):
            particula.posicao[i] = particula.posicao[i] + particula.velocidade[i]
            if particula.posicao[i] < valorMinimo:
                particula.posicao[i] = valorMinimo
            elif particula.posicao[i] > valorMaximo:
                particula.posicao[i] = valorMaximo

        # Avaliando o fitness da nova posição
        particula.fitness = fitness(particula.posicao)

        # Avaliando o melhor Local
        if particula.fitness < particula.melhor_local:
            particula.melhor_local = particula.fitness
            particula.melhor_local_posicao = list(particula.posicao)

        # Avaliando o melhor Global
        if particula.fitness < melhor_global:
            melhor_global = particula.fitness
            melhor_global_posicao = list(particula.posicao)

        ax.clear()
        init_plot()

print(melhor_global_posicao)
print(melhor_global)

#https://pyswarms.readthedocs.io/en/latest/examples/tutorials/visualization.html#Plotting-in-2-D-space