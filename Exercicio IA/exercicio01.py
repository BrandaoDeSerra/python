import random
from builtins import print, filter

# ##################################################
def probabilidade(aptidao, soma):
    resultado = round((aptidao / soma) * 100)
    if (resultado == 0):
        resultado = 1
    return resultado
# ##################################################
def fitness(x):
    return x**2 - 3*x + 4
# ##################################################
def converterFenotipo2Genotipo(fenotipo):
    binario = bin(fenotipo)
    sinal = '1'
    if (binario[0:1] == '-'):
        sinal = '0'
        binario = binario[1:]
    return sinal + str(binario[2:].zfill(4))
# ##################################################
def converterGenotipo2Fenotipo(genotipo):
    sinal = '0b'
    if (genotipo[0:1] == '0'):
        sinal = '-0b'
    return int(sinal + genotipo[1:], 2)
# ##################################################
def crossover(genotipo1, genotipo2, idxCross):
    return genotipo1[:idxCross] + genotipo2[idxCross:] + ';' + genotipo2[:idxCross] + genotipo1[idxCross:]
# ##################################################
def mutation(genotipo, idxMut):
    gene = '0'
    if (genotipo[idxMut] == '0'):
        gene = '1'
    return str(genotipo[:idxMut]) + str(gene) + str(genotipo[idxMut + 1:])
# ##################################################
def ordenaProbabilidadeSelecao(val):
    return val[3]
# ##################################################
def ordenaAptidao(val):
    return val[2]
# ##################################################
def gerarIndividuo(fenotipo,populacao):
    genotipo = converterFenotipo2Genotipo(fenotipo)
    aptidao = fitness(fenotipo)
    x = [fenotipo, genotipo, aptidao]
    populacao.append(x)
    return populacao
# ##################################################
def recuperarSomaInversao(populacao):
    soma = 0
    for p in populacao:
        soma = soma + p[3]
    return soma
# ##################################################
def recuperarSomaAptidao(populacao):
    soma = 0
    for p in populacao:
        soma = soma + p[2]
    return soma
# ##################################################
def avaliarPopulacao(populacao):
    soma = recuperarSomaAptidao(populacao)
    tamanhoPopulacao = len(populacao)
    for i in range(tamanhoPopulacao):
        aptidao = populacao[i][2]
        inversao = soma - aptidao
        x = [populacao[i][0], populacao[i][1], populacao[i][2], inversao]
        populacao[i] = x
    somaInversao = recuperarSomaInversao(populacao)
    for i in range(tamanhoPopulacao):
        aptidaoInversa = populacao[i][3]
        probabilidadeSelecao = probabilidade(aptidaoInversa, somaInversao)
        x = [populacao[i][0], populacao[i][1], populacao[i][2], probabilidadeSelecao]
        populacao[i] = x
    populacao.sort(key=ordenaProbabilidadeSelecao, reverse=True)
    return populacao
# ##################################################
def selecao(pais,populacao):
    tamanhoPopulacao = len(populacao)
    qtdPais = (round(tamanhoPopulacao / 2) - (tamanhoPopulacao % 2)) * 2  # total de Casais que vao se formar com a população atual
    for c in range(qtdPais):  # seleção do pais
        roleta = random.randint(1, 100)
        referenciaInicial = 0
        achouPaiApto = 0
        for p in range(tamanhoPopulacao):
            probabilidadeSelecaoIndividuo = populacao[p][3]
            referenciaFinal = referenciaInicial + probabilidadeSelecaoIndividuo
            if (referenciaInicial + 1) <= roleta <= referenciaFinal:
                pais.append(populacao[p][1])  # recupera o gene
                achouPaiApto = 1
                break
            referenciaInicial = referenciaFinal
        if achouPaiApto == 0:  # caso exceção da distribuição dos 100%, vai para o que tem mais chances de seleção, o primeiro
            pais.append(populacao[0][1])
    return pais
# ##################################################
def reproducao(pais,taxaCrossover):
    qtdCasal = int(len(pais) / 2)
    indx = 0
    for p in range(qtdCasal):
        filho1 = pais[indx]
        filho2 = pais[indx + 1]
        probabilidadeCross = random.randint(1, 100)
        if probabilidadeCross <= taxaCrossover:
            genCrossover = random.randint(0, 4)
            filhosCross = str(crossover(filho1, filho2, genCrossover)).split(';')  # Crossover
            filho1 = filhosCross[0]
            filho2 = filhosCross[1]
        filhos.append(filho1)
        filhos.append(filho2)
        indx = indx + 2
    pais.clear()
    return filhos
# ##################################################
def mutacao(filhos,taxaMutacao):
    indx = 0
    for filho in filhos:
        for gen in range(len(filho)):
            probabilidadeMutacao = random.randint(1, 100)
            if probabilidadeMutacao <= taxaMutacao:
                filho = mutation(filho, gen)  # Mutacao
        filhos[indx] = filho
        indx = indx + 1
    return filhos
# ##################################################
def atualizarPopulacao(populacao, filhos):
    for f in filhos:
        fenotipo = converterGenotipo2Fenotipo(f)
        # limita populacao entre -10 a 10
        if fenotipo < -10:
            fenotipo = -10
        elif fenotipo > 10:
            fenotipo = 10
        populacao = gerarIndividuo(fenotipo, populacao)
    filhos.clear()
    populacao.sort(key=ordenaAptidao)
    return populacao
# ##################################################
def eliminaIndividuosDuplicados(populacao):
    bkp = list()
    f2x = -99999;
    for p in populacao:
        if p[2] != f2x:
            bkp.append(p)
            f2x = p[2]
    bkp.sort(key=ordenaAptidao)
    populacao = bkp
    return populacao

'''
1) Encontrar valor de x para o qual a função f(x) = x2 - 3x + 4 assume o valor mínimo
- Assumir que x ∈ [-10, +10]
- Codificar X como vetor binário
- Criar uma população inicial com 4 indivíduos
- Aplicar Mutação com taxa de 1%
- Aplicar Crossover com taxa de 60%
- Usar seleção por roleta.
- Usar no máximo 5 gerações.

x -> [-10, +10]
Populacao Inicial = 4
Taxa de Crossover = 60% 
Taxa de Mutação = 1%  
Probabilidade de Escolha P(i) = SOMATORIO f(i) - f(i) / SOMATORIO (SOMATORIO f(i) - f(i) ))

1 bit(sinal) + 4 bits(valor 15 a -15 ) = 5 bits

individuo
  - Fenotipo
  - Genotipo
  - Aptidão
  - probabilidadeSelecao
'''
populacao = list()
pais = list();
filhos = list();

populacaoInicial = 4
taxaCrossover = 60
taxaMutacao = 1
numeroDeGeracoes = 5

# Gera populacao Inicial
for p in range(populacaoInicial):
    fenotipo = random.randint(-10, 10)
    populacao = gerarIndividuo(fenotipo,populacao)

for geracao in range(numeroDeGeracoes):
    pais.clear()
    filhos.clear()
    filhos = list();
    populacao = avaliarPopulacao(populacao)
    pais = selecao(pais,populacao)
    filhos = reproducao(pais,taxaCrossover)
    filhos = mutacao(filhos,taxaMutacao)
    populacao = atualizarPopulacao(populacao,filhos)
    #populacao = eliminaIndividuosDuplicados(populacao)

# listar populacao
for individuo in populacao:
    print('x = '+str(individuo[0])+' >> f(x) = '+str(individuo[2]))

