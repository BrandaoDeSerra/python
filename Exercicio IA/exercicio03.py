'''Selecione um algoritmo evolucionário que não estudamos em sala e explique seu funcionamento, elencando os seus elementos
(representação de indivíduos, operadores, geração etc.) e acentuando as diferenças e semelhanças em relação aos algoritmos genéticos.
'''

Os algorítimos evolucionário, seguem uma linha inspirada em mecanismos da evolução orgânica, observando a natureza, para resolver problemas de otimização e busca.
Em aula estudamos um algorito genético e como todo os algoritimos dessa natureza tem como inspiração caracteristicas da biologia evolutiva, são elas a hereditariedade,
recombinação, mutação e seleção natural.
  Principais componentes de algoritimo genetico
   1- função fitness (função objetivo)
   2- indivíduo
     2.1- população
   4- seleção
   5- reprodução
     5.1- Cruzamento
     5.2- Mutação
   6- gerações

O algoritimo cultura segue tambem a linha da computação Evolutiva. Esse tipo de Algoritimo tem 2 fatores de herança uma GENÉTICA e outra CULTURAL
Componentes de um Algoritmo Cultural

1-População
 -1.1 Função de avaliação
 -1.2 Função de Evolução
2-Espaço de crença
 -2.1 Operadores Culturais
     .Generalização
     .Especialização
     .Fusão
     .Fissão
3-Protocolo de comunicação
 -3.1 Votação - função de Aceitação -> Influencia o Espaço de crença
 -3.2 Promoção - função de Influência -> Influencia um componente da população

>>> Comparaçãoes dos algoritimos <<<

#Algoritmos Genéticos:

Início
  t=0                        # primeira geração
  inicializar população P(t) # população inicial aleatória
  avaliar população P(t)     # calcula f(i) para cada indivíduo
  enquanto (não condição_fim) faça
    t=t+1                    # próxima geração
    selecionar P(t) de P(t-1)# seleção de pais
    altera P(t)              # crossover e mutação
  fim enquanto
fim

#Algoritmo Cultural
Início
  t= 0                               # primeira geração
  inicializar população P(t)         # população inicial aleatória
  Inicializar Espaço de Crença EP(t) # Iniciando Espaço de crença
  avaliar população P(t)             # calcula f(i) para cada indivíduo
  enquanto (não condição_fim) faça
    Comunicação (P(t), EP(t));       # votação
    Atualização EP(t);               # uso de operadores culturais
    Comunicação (EP(t), P(t));       # promoção
    t = t+1                          # próxima geração
    selecionar P(t) de P(t-1)
    altera P(t)                      # crossover e mutação
    avaliar P(t)                     # calcula f(i) para cada indivíduo
  fim enquanto
fim