import random
from builtins import print, filter


def excluirIndividuosIguais(populacao):
    bkp = list()
    fDeX = -99999;
    for p in populacao:
        if p[2] != fDeX:
            bkp.append(p)
            fDeX = p[2]
    bkp.sort(key=sortAptidao)
    populacao = bkp
    return populacao

def probabilidade(aptidao, soma):
    resultado = round((aptidao / soma) * 100)
    if (resultado == 0):
        resultado = 1
    return resultado

def fitness(x):
    return (x ** 2) - (3 * x) + 4

def converteFenotipo2Genotipo(fenotipo):
    binario = bin(fenotipo)
    sinal = '1'
    if (binario[0:1] == '-'):
        sinal = '0'
        binario = binario[1:]
    return sinal + str(binario[2:].zfill(4))

def converteGenotipo2Fenotipo(genotipo):
    sinal = '0b'
    if (genotipo[0:1] == '0'):
        sinal = '-0b'
    return int(sinal + genotipo[1:], 2)

def crossover(genotipo1, genotipo2, idxCross):
    return genotipo1[:idxCross] + genotipo2[idxCross:] + ';' + genotipo2[:idxCross] + genotipo1[idxCross:]

def mutacao(genotipo, idxMut):
    gene = '0'
    if (genotipo[idxMut] == '0'):
        gene = '1'
    return str(genotipo[:idxMut]) + str(gene) + str(genotipo[idxMut + 1:])

def sortProbabilidadeSelecao(val):
    return val[3]

def sortAptidao(val):
    return val[2]

def geraIndividuo(fenotipo,populacao):
    genotipo = converteFenotipo2Genotipo(fenotipo)
    aptidao = fitness(fenotipo)
    x = [fenotipo, genotipo, aptidao]
    populacao.append(x)
    return populacao

def recuperaSomaInversao(populacao):
    soma = 0
    for p in populacao:
        soma = soma + p[3]
    return soma

def recuperaSomaAptidao(populacao):
    soma = 0
    for p in populacao:
        soma = soma + p[2]
    return soma

def avaliaPopulacao(populacao):
    soma = recuperaSomaAptidao(populacao)
    tamanhoPopulacao = len(populacao)
    for i in range(tamanhoPopulacao):
        aptidao = populacao[i][2]
        inversao = soma - aptidao
        x = [populacao[i][0], populacao[i][1], populacao[i][2], inversao]
        populacao[i] = x

    somaInversao = recuperaSomaInversao(populacao)
    for i in range(tamanhoPopulacao):
        aptidaoInversa = populacao[i][3]
        probabilidadeSelecao = probabilidade(aptidaoInversa, somaInversao)
        x = [populacao[i][0], populacao[i][1], populacao[i][2], probabilidadeSelecao]
        populacao[i] = x

    populacao.sort(key=sortProbabilidadeSelecao, reverse=True)
    return populacao

def geraNovaPopulacao(populacao,taxaCrossover,taxaMutacao):
    pais = list()
    filhos = list()
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

    qtdCasal = int(len(pais) / 2)
    indx = 0
    for p in range(qtdCasal):
        filho1 = pais[indx]
        filho2 = pais[indx + 1]
        probabilidadeCross = random.randint(1, 100)
        if probabilidadeCross <= taxaCrossover:
            genCrossover = random.randint(0, 4)
            filhosCross = str(crossover(filho1, filho2, genCrossover)).split(';') # Crossover
            filho1 = filhosCross[0]
            filho2 = filhosCross[1]
        isFilho = 0;
        for filho in [filho1, filho2]:
            for gen in range(len(filho)):
                probabilidadeMutacao = random.randint(1, 100)
                if probabilidadeMutacao <= taxaMutacao:
                    filho = mutacao(filho, gen) # Mutacao
            if isFilho == 0:
                filho1 = filho
                isFilho = 1
            else:
                filho2 = filho
        filhos.append(filho1)
        filhos.append(filho2)
        indx = indx + 2
    return filhos

def atualizaPopulacao(populacao, filhos):
    for f in filhos:
        fenotipo = converteGenotipo2Fenotipo(f)
        populacao = geraIndividuo(fenotipo, populacao)
    populacao.sort(key=sortAptidao)
    return populacao
'''
x -> [-10, +10]
Populacao Inicial = 4
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
populacao = list()
pais = list()
filhos = list()

populacaoInicial = 4
taxaCrossover = 60
taxaMutacao = 1
numeroDeGeracoes = 5

for p in range(populacaoInicial):
    fenotipo = random.randint(-10, 10)
    populacao = geraIndividuo(fenotipo,populacao)

for geracao in range(numeroDeGeracoes):
    populacao = avaliaPopulacao(populacao)
    # pais = selecao(populacao)
    # filhos = reproducao(populacao,taxaCrossover)
    # filhos = mutacao(populacao,taxaMutacao)
    filhos = geraNovaPopulacao(populacao,taxaCrossover,taxaMutacao)
    populacao = atualizaPopulacao(populacao,filhos)

print(populacao)

# populacao = excluirIndividuosIguais(populacao)
# print(populacao)

# for g in range(numeroDeGeracoes):

'''
1) Encontrar valor de x para o qual a função f(x) = x2 - 3x + 4 assume o valor mínimo
- Assumir que x ∈ [-10, +10]
- Codificar X como vetor binário
- Criar uma população inicial com 4 indivíduos
- Aplicar Mutação com taxa de 1%
- Aplicar Crossover com taxa de 60%
- Usar seleção por roleta.
- Usar no máximo 5 gerações.

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
