import matplotlib.pyplot as plt
import itertools
import random

# ##################################################
def recuperarCromossomo(combinacao):
    return str(combinacao[0])+str(combinacao[1])+str(combinacao[2])+str(combinacao[3])

# ##################################################
def crossover(genotipo1, genotipo2, idxCross):
    filho1 = genotipo2[idxCross:]
    part = ''
    for i in genotipo1:
        if filho1.find(i) >= 0:
            continue
        else:
            part = part+i
    filho1 = part+filho1;
    part = ''
    filho2 = genotipo1[idxCross:]
    for i in genotipo2:
        if filho2.find(i) >= 0:
            continue
        else:
            part = part+i
    filho2 = part + filho2;
    return filho1,filho2

# ##################################################
def mutation(genotipo, idxMut1,idxMut2):
    gen1 = genotipo[idxMut1]
    gen2 = genotipo[idxMut2]
    part1 = genotipo[:idxMut1]
    part2 = genotipo[idxMut1+1:idxMut2]
    part3 = genotipo[idxMut2+1:]
    return part1+gen2+part2+gen1+part3

# ##################################################
def fitness(roteiro):
    distancias = ['1221=2', '1331=6', '1441=3', '2332=4', '2442=7', '3443=2']
    part1 = roteiro[0:2]
    part2 = roteiro[1:3]
    part3 = roteiro[2:4]
    soma = 0
    for part in [part1,part2,part3]:
        for ref in distancias:
            if ref.find(part) >= 0:
                valor = ref.split('=')
                soma = soma + int(valor[1])
                break
    return soma

'''

2) Resolver o problema do caixeiro viajante (representado pela imagem em anexo), sendo que a solução consiste em encontrar um caminho sem repetições com custo mínimo.
Execute o algoritmo com 3 variações de parâmetros e plote o gráfico de evolução da aptidão. Interprete os resultados.
Obs: Nesse problema, é preciso primeiro definir como representar um cromossomo e como definir uma função de aptidão.

'''
#y = [0,1,2,3,4,5,6,7,8,9]
#x = [0.1,1,2.1,3,3.1,4.1,5,6,7.1,8]
#plt.plot(x,y)
#plt.show()


cidades = [1,2,3,4]

x = list(itertools.permutations(cidades))

ind1 = mutation('13425',0,3)
print(ind1)

ind1,ind2 = crossover('13425','34512',1) #index 2 ou 3
print(ind1,ind2)

for i in x:
    cromossomo = recuperarCromossomo(i)
    print('x='+cromossomo+' > f(x)='+str(fitness(cromossomo)))

