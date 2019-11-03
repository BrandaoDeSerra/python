import matplotlib.pyplot as plt
import itertools
import random

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

# ##################################################
def geraPopulacaoInicial(populacao):
    fenotipo_1_inicial = '1234'
    fenotipo_2_inicial = '4321'
    fenotipo_3_inicial = '3214'
    fenotipo_4_inicial = '4231'
    gerarIndividuo(fenotipo_1_inicial, populacao)
    gerarIndividuo(fenotipo_2_inicial, populacao)
    gerarIndividuo(fenotipo_3_inicial, populacao)
    gerarIndividuo(fenotipo_4_inicial, populacao)

# ##################################################
def gerarIndividuo(fenotipo,populacao):
    genotipo = fenotipo
    aptidao = fitness(fenotipo)
    x = [len(populacao)+1, fenotipo, genotipo, aptidao]
    populacao.append(x)

# ##################################################
def recuperarSomaInversao(populacao):
    soma = 0
    for p in populacao:
        soma = soma + p[4]
    return soma

# ##################################################
def recuperarSomaAptidao(populacao):
    soma = 0
    for p in populacao:
        soma = soma + p[3]
    return soma

# ##################################################
def probabilidade(aptidao, soma):
    resultado = round((aptidao / soma) * 100)
    if (resultado == 0):
        resultado = 1
    return resultado

# ##################################################
def avaliarPopulacao(populacao):
    soma = recuperarSomaAptidao(populacao)
    tamanhoPopulacao = len(populacao)
    for i in range(tamanhoPopulacao):
        aptidao = populacao[i][3]
        inversao = soma - aptidao
        x = [populacao[i][0],populacao[i][1], populacao[i][2], populacao[i][3], inversao]
        populacao[i] = x
    somaInversao = recuperarSomaInversao(populacao)
    for i in range(tamanhoPopulacao):
        aptidaoInversa = populacao[i][4]
        probabilidadeSelecao = probabilidade(aptidaoInversa, somaInversao)
        x = [populacao[i][0], populacao[i][1], populacao[i][2], populacao[i][3], probabilidadeSelecao]
        populacao[i] = x
    populacao.sort(key=ordenaProbabilidadeSelecao, reverse=True)

# ##################################################
def ordenaProbabilidadeSelecao(val):
    return val[4]

# ##################################################
def ordenaAptidao(val):
    return val[3]

# ##################################################
def ordenaPopulacao(val):
    return val[0]

# ##################################################
def ordenaFenotipo(val):
    return val[1]


# ##################################################
def selecao(pais,populacao):
    tamanhoPopulacao = len(populacao)
    qtdPais = (round(tamanhoPopulacao / 2) - (tamanhoPopulacao % 2)) * 2  # total de Casais que vao se formar com a população atual
    for c in range(qtdPais):  # seleção do pais
        roleta = random.randint(1, 100)
        referenciaInicial = 0
        achouPaiApto = 0
        for p in range(tamanhoPopulacao):
            probabilidadeSelecaoIndividuo = populacao[p][4]
            referenciaFinal = referenciaInicial + probabilidadeSelecaoIndividuo
            if (referenciaInicial + 1) <= roleta <= referenciaFinal:
                pais.append(populacao[p][2])  # recupera o gene
                achouPaiApto = 1
                break
            referenciaInicial = referenciaFinal
        if achouPaiApto == 0:  # caso exceção da distribuição dos 100%, vai para o que tem mais chances de seleção, o primeiro
            pais.append(populacao[0][2])

# ##################################################
def reproducao(pais,taxaCrossover):
    qtdCasal = int(len(pais) / 2)
    indx = 0
    for p in range(qtdCasal):
        filho1 = pais[indx]
        filho2 = pais[indx + 1]
        probabilidadeCross = random.randint(1, 100)
        if probabilidadeCross <= taxaCrossover:
            genCrossover = random.randint(2, 3)
            filho1,filho2 = crossover(filho1, filho2, genCrossover)  # Crossover
        filhos.append(filho1)
        filhos.append(filho2)
        indx = indx + 2
    pais.clear()

# ##################################################
def mutacao(filhos,taxaMutacao):
    indx = 0
    for filho in filhos:
        for gen in range(len(filho)):
            probabilidadeMutacao = random.randint(1, 100)
            if probabilidadeMutacao <= taxaMutacao:
                gen1 = gen
                if gen < 3:
                    gen2 = random.randint(gen+1, 3)
                else:
                    gen2 = gen
                    gen1 = random.randint(0, 2)
                filho = mutation(filho, gen1,gen2)  # Mutacao
                break
        filhos[indx] = filho
        indx = indx + 1

# ##################################################
def atualizarPopulacao(populacao, filhos):
    for fenotipo in filhos:
        gerarIndividuo(fenotipo, populacao)
    filhos.clear()
    populacao.sort(key=ordenaAptidao)

# ##################################################
def eliminaIndividuos(populacao,repetidos,populacaoMinimaParaExcluir):
    populacao.sort(key=ordenaFenotipo)
    bkp = list()
    f2x = '0000'
    for p in populacao:
        if p[2] != f2x:
            bkp.append(p)
            f2x = p[2]
    if len(bkp) >= repetidos:
        populacao = bkp
    populacao.sort(key=ordenaAptidao)
    if len(populacao) >= populacaoMinimaParaExcluir:
        ind = 1 # exclui 2 elementos menos aptos
        for i in reversed(populacao):
            populacao.remove(i)
            if ind==0:
                break
            ind = ind - 1
    return populacao

'''

2) Resolver o problema do caixeiro viajante (representado pela imagem em anexo), sendo que a solução consiste em encontrar um caminho sem repetições com custo mínimo.
Execute o algoritmo com 3 variações de parâmetros e plote o gráfico de evolução da aptidão. Interprete os resultados.
Obs: Nesse problema, é preciso primeiro definir como representar um cromossomo e como definir uma função de aptidão.

Individuo
  -0 Ordem
  -1 Fenotipo
  -2 Genotipo
  -3 Aptidão
  -4 probabilidadeSelecao
  
'''

cidades = [1,2,3,4]
populacao = list()
pais = list()
filhos = list()

taxaCrossover = 60
taxaMutacao = 1
numeroDeGeracoes = 15

# Gera populacao Inicial
geraPopulacaoInicial(populacao)

for geracao in range(numeroDeGeracoes):
    avaliarPopulacao(populacao)
    selecao(pais,populacao)
    reproducao(pais,taxaCrossover)
    mutacao(filhos,taxaMutacao)
    atualizarPopulacao(populacao,filhos)
    populacao = eliminaIndividuos(populacao,16,32) # individuo Repetido / populacao minima para excluir menos aptos

y = list()
x = list()
for i in range(len(populacao)):
   y.append(populacao[i][3])
   x.append(populacao[i][1])

plt.plot(x,y)
plt.show()

populacao = eliminaIndividuos(populacao,16,32)
# listar populacao
for individuo in populacao:
    print('ordem:'+str(individuo[0])+' | x='+str(individuo[1])+' >> f(x)='+str(individuo[3]))
