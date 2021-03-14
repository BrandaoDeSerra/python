# Neurório perceptron
"""

Entrada_1 > sensor 1
Entrada_2 > Sensor 2

Bias      * Peso --|

Entrada_1 * Peso --|  >-- função soma -> Função ativação = 0 ou 1

Entrada_2 * Peso --|

tabela - Classe
   0 0 - 0 Ligar alarme
   0 1 - 0 Ligar alarme
   1 0 - 0 Liba alarme
   1 1 - 1 Desligar alarme

"""

# Função de soma
import numpy


def funcaoSoma(entradas, w0, numeroDeEntradas, peso):
    soma = w0 * peso[0]
    for wi in range(numeroDeEntradas):
        soma = soma + (entradas[wi] * peso[wi+1])
    return soma


# Função de ativação > Step Function (função degrau)
def stepFunction(pSoma):
    if pSoma >= 0.0:
        return 1
    return 0


# função de Aprendizado, ajsute de Pesos
def ajusteDePesos(pesos, w0, entrada, fator):
    pesos[0] = pesos[0] + fator * w0
    i = 0
    for x in entrada:
        pesos[i + 1] = pesos[i + 1] + fator * x
        i = i + 1
        if i >= qtdEntradas:
            break
    return pesos


# Tabela                      u1/u2/desejavel
tabela_classe = numpy.array([[0, 0, 0],
                             [0, 1, 0],
                             [1, 0, 0],
                             [1, 1, 1]])

pesosSinapticos = numpy.array([0,  # peso bias inicial
                               3,  # peso entrada 1 aleatorio inicial
                               3])  # peso entrada 2 aleatorio inicial

resultado = []  # resultado de cada ciclo
erroEntrada = []  # Erro entrada
qtdEntradas = 2
taxaAprendizado_delta = 1  # Inicialmente aleátório
bias = 1  # limiar

erro = 1

ciclos = 1
exemplo = 1

# treino
while erro == 1:
    erro = 0
    exemplo = 1
    print("Ciclo : " + str(ciclos))
    for row in tabela_classe:
        somaEntradas = funcaoSoma(row, bias, qtdEntradas, pesosSinapticos)
        y = stepFunction(somaEntradas)  # saida y = 0 ou 1
        desejavel = row[2] # Classe desejada
        if desejavel != y:
            fator = taxaAprendizado_delta * (desejavel - y)
            pesosSinapticos = ajusteDePesos(pesosSinapticos, bias, row, fator)
            erro = 1
        print("  Exemplo : " + str(exemplo))
        print("  desejavel : " + str(desejavel))
        print("  Saída : " + str(y))
        print("  - - - - - - - - - - - - - - - -  ")
        exemplo = exemplo + 1

    ciclos = ciclos + 1
    print("......................................")
print("Peso sináptico Bias w0 :"+str(pesosSinapticos[0]))
print("Peso sináptico w1 :"+str(pesosSinapticos[1]))
print("Peso sináptico w2 :"+str(pesosSinapticos[2]))

