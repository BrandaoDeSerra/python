#

'''
COMPUTACAO EVOLUCIONARIA

Problemas de otimização ( x > f(x) > Y ) Conheço o modelo e os resultados, mas não conheço as entradas
   1-Computação evolucionária =: Crossover(Cruzamento) / Seleção(filtrar o melhor)  / Mutação (novos individuos)
     * AG
     * PG
   2-Inteligencia de enxames
     * PSO
     * ACO
'''
import random
from builtins import print, filter

'''
Populacao = 4
Taxa de Crossover = 70% > 7 possibilidades
Taxa de Mutação = 10% > entre 0 e 100 - de 0 a 10 troca - demais não troca
Probabilidade de Escolha P(i) = f(i) / SOMATORIO f(i)

4 + 4 bits = 8 bits
'''

rangePopulacao = 4
taxaCrossover = 70
taxaMutacao = 10
numeroDeGeracoes = 10

def probabilidade(valor,soma):
    x = round(valor / soma)
    x = round(x * 100)
    return x

def fitness(x1,x2):
    return ( (x1**2) - ((x2**2)/2) + (2*x2) + (x1*x2) )

individuo = list()
soma = 0

for p in range(rangePopulacao):
    x1 = random.randint(1, 10)
    x2 = random.randint(1, 10)
    genotipo = str(bin(x1)[2:].zfill(4)) + str(bin(x2)[2:].zfill(4))
    aptidao = round(fitness(x1, x2))
    if(aptidao <= 0):
        aptidao = 1
    x = [x1,x2,genotipo,aptidao]
    individuo.append(x)
    soma = soma + aptidao

length = len(individuo)
for p in range(length):
    aptidao = individuo[p][3]
    probabilidadeSelecao = probabilidade(aptidao,soma)
    pSelecao = random.randint(1, 100)
    pCrossover = random.randint(1, 100)
    pMutacao = random.randint(1, 100)
    cromossomoIndex = random.randint(1, 7)
    x = [individuo[p][0],individuo[p][1],individuo[p][2],individuo[p][3],probabilidadeSelecao,taxaCrossover,pCrossover,cromossomoIndex,taxaMutacao,pMutacao]
    individuo[p] = x

print(individuo)

'''
for 
    
    

    print('x1 -> '+str(bin(x1)[2:].zfill(4)))
    print('x2 -> ' + str(bin(x2)[2:].zfill(4)))
    print('x1 = '+str(x1)+' / x2 = '+str(x2)+' >>> fitness = '+str(val))
    print('--------')

    individuo[ind][0] = x1

    ind++


'''