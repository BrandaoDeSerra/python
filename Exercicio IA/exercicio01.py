
import random
from builtins import print, filter

def probabilidade(aptidao, soma):
    resultado = round((aptidao / soma) * 100)
    if(resultado == 0):
        resultado = 1
    return resultado

def fitness(x):
    return (x**2) - (3*x) + 4

def converteFenotipo2Genotipo(fenotipo):
    binario = bin(fenotipo)
    sinal = '1'
    if (binario[0:1] == '-'):
        sinal = '0'
        binario = binario[1:]
    return sinal + str(binario[2:].zfill(4))

def converteGenotipo2Fenotipo(genotipo):
    sinal = '0b'
    if(x[0:1] == '0'):
        sinal = '-0b'
    return int(sinal+genotipo[1:],2)

def crossover(genotipo1,genotipo2, idxCross):
    return genotipo1[:idxCross] + genotipo2[idxCross:]+';'+genotipo2[:idxCross] + genotipo1[idxCross:]

def mutacao(genotipo,idxMut):
    gene = '0'
    if(genotipo[idxMut] == '0'):
        gene = '1'
    return str(genotipo[:idxMut]) + str(gene) + str(genotipo[idxMut+1:])

def sortProbabilidadeSelecao(val):
    return val[3]

'''
x -> [-10, +10]
Populacao = 4
Taxa de Crossover = 60% 
Taxa de Mutação = 1%  
Probabilidade de Escolha P(i) = SOMATORIO f(i) - f(i) / SOMATORIO (SOMATORIO f(i) - f(i) ))

4 + 4 bits = 8 bits

individuo
  - Fenotipo
  - Genotipo
  - Aptidão
  - probabilidadeSelecao
'''

rangePopulacao = 4
taxaCrossover = 60
taxaMutacao = 1
numeroDeGeracoes = 5

populacao = list()
soma = 0

for p in range(rangePopulacao):
    fenotipo = random.randint(-10, 10)
    genotipo = converteFenotipo2Genotipo(fenotipo)
    aptidao = fitness(fenotipo)
    x = [fenotipo, genotipo, aptidao]
    populacao.append(x)
    soma = soma + aptidao

somaInversao = 0
tamanhoPopulacao = len(populacao)
for i in range(tamanhoPopulacao):
    aptidao = populacao[i][2]
    inversao = soma - aptidao
    x = [populacao[i][0],populacao[i][1],populacao[i][2],inversao]
    somaInversao = somaInversao + inversao
    populacao[i] = x

print(populacao)
for i in range(tamanhoPopulacao):
    aptidaoInversa = populacao[i][3]
    probabilidadeSelecao = probabilidade(aptidaoInversa,somaInversao)
    x = [populacao[i][0],populacao[i][1],populacao[i][2],probabilidadeSelecao]
    populacao[i] = x

casais = list()
totalCasais = round(tamanhoPopulacao / 2) - (tamanhoPopulacao % 2) #total de Casais que vao se formar com a população atual

#ordenando pelo mais tem probabilidade de sair
populacao.sort(key = sortProbabilidadeSelecao,reverse = True)
print(populacao)

for c in range(tamanhoPopulacao):
    roleta = random.randint(1, 100)
    for p in range(tamanhoPopulacao):
        probabilidadeSelecaoIndividuo = populacao[p][3]
      #  if( )
       # if(probabilidadeSelecaoIndividuo)





#for g in range(1,numeroDeGeracoes):

'''

    print(fenotipo)
    print(converteFenotipoParaGenotipo(fenotipo))
    print(converteGenotipoParaFenotipo(genotipo))
    
    filhos = str(crossover('10101','00110',4)).split(';')
    print(filhos[0])
    print(filhos[1])

    m = mutacao('10101',4)
    print(m)
for 



    print('x1 -> '+str(bin(x1)[2:].zfill(4)))
    print('x2 -> ' + str(bin(x2)[2:].zfill(4)))
    print('x1 = '+str(x1)+' / x2 = '+str(x2)+' >>> fitness = '+str(val))
    print('--------')

    individuo[ind][0] = x1

    ind++


'''