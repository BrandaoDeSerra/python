'''
w = inicio 0.9 vai descendo ate 0,2
C1 É UM PESO PARA O MELHOR LOCAL
C2 É UM PESO PARA O MAIOR GLOBAL

R1 - radomico
R2 - radomico

v1 = w * v1 + c1 * r1 (p1 - s1) +
v1 = 0.9 * 3

Usando alguma biblioteca ou implementando diretamente em alguma linguagem de programação,
desenvolva uma solução para minimizar a função de Rosenbrock (em anexo). Faça testes pra
identificar um conjunto de parâmetros adequado. Plote o gráfico de evolução da solução.

Xmin / Ymin = -2
Xmax / Ymax = +2

minGlobal = +1
'''
import random
import sys

# ##################################################
def fitness(particle):  # Rosenbrock
    x = particle[0]
    y = particle[1]
    a = 1. - x
    b = y - x * x
    return (b * b * 100.) + (a * a)

# ##################################################
def calculaNovaVelocidade(particula, v):  # Calculo da velocidade por particula
    r1 = random.random()
    r2 = random.random()
    part_1 = (w * particula.velocities[v])
    part_2 = (c1 * r1 * (particula.melhor_particula_positions[v] - particula.positions[v]))
    part_3 = (c2 * r2 * (melhor_enxame_posicao[v] - particula.posicao[v]))
    novaVelocidade = part_1 + part_2 + part_3
    return novaVelocidade

# ##################################################
class Particle:
    def __init__(self, qtdVariaveis, min_value, max_value):
        self.posicao = [0.0 for v in range(qtdVariaveis)]  # Iniciando array das posicoes
        self.velocities = [0.0 for v in range(qtdVariaveis)]  # Iniciando array das velocidades
        for v in range(qtdVariaveis):
            self.posicao[v] = ((valorMaximo - valorMinimo) * random.random() + valorMinimo)  # Atualizando as posições iniciais
            self.velocities[v] = ((valorMaximo - valorMinimo) * random.random() + valorMinimo)  # Atualizando as velocidades iniciais
        self.fitness = fitness(self.posicao)  # Calculando do fitness de cada posição das partículas
        self.melhor_particula_posicao = list(self.posicao)  # posição da particula
        self.melhor_particula_local = self.fitness # melhor fitness da particula

# ----------------------
# >>>>>>> INICIO <<<<<<<

qtdParticulasIniciais = 5  # Número de Partículas Iniciais

numeroDeDimensoes = 2  # Número de dimensões
valorMinimo = -2  # Minimo valor para x e y
valorMaximo = +2  # Máximo valor para x e y

qtdIteracoes = 10  # Número de Iterações

w = 0.9  # Inércia  w (inicial) = 0,9 e diminui para w (final) = 0,2

c1 = 1.49  # peso para o melhor Local
c2 = 1.50  # peso para o melhor global

# Criando Enxame inicial
enxame = [Particle(numeroDeDimensoes, valorMinimo, valorMaximo) for p in range(qtdParticulasIniciais)]

melhor_enxame_posicao = [0.0 for v in range(numeroDeDimensoes)]
melhor_enxame_global = sys.float_info.max

# Analisando cada particula para atualizar o melor fitness Global, que é a minimização da função de Rosenbrick(fitness)
for particula in enxame:
    if particula.fitness < melhor_enxame_global:
        melhor_enxame_global = particula.fitness
        melhor_enxame_posicao = list(particula.posicao)

for i in range(qtdIteracoes):
    for particula in enxame:
        # Calculando a nova velocidade de cada partícula
        for v in range(numeroDeDimensoes):
            particula.velocities[v] = calculaNovaVelocidade(particula, v)
            if particula.velocities[v] < valorMinimo:
                particula.velocities[v] = valorMinimo
            elif particula.velocities[v] > valorMaximo:
                particula.velocities[v] = valorMaximo

        # verificando a nova posição usando a nova Velocidade, limitado pelos valores maximos e minimos definidos
        for v in range(numeroDeDimensoes):
            particula.posicao[v] += particula.velocities[v]
            if particula.posicao[v] < valorMinimo:
                particula.posicao[v] = valorMinimo
            elif particula.posicao[v] > valorMaximo:
                particula.posicao[v] = valorMaximo

        # Avaliando o fitness da nova posição
        particula.fitness = fitness(particula.posicao)

        # Avaliando o melhor Local
        if particula.fitness < particula.melhor_particula_local:
            particula.melhor_particula_local = particula.fitness
            particula.melhor_particula_posicao = list(particula.posicao)

        # avaliando o melhor Global
        if particula.fitness < melhor_enxame_global:
            melhor_enxame_global = particula.fitness
            melhor_enxame_posicao = list(particula.posicao)

        # fator de desagregação / dispersão
        if w > 0.2:
            w = w - 0.1

print(melhor_enxame_posicao)
