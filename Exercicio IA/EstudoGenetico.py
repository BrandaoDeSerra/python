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


import random
import numpy as np

W = 0.5
c1 = 0.8
c2 = 0.9

n_iterations = int(input("Inform the number of iterations: "))
target_error = float(input("Inform the target error: "))
n_particles = int(input("Inform the number of particles: "))

class Particle():
    def __init__(self):
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0,0])

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)

    def move(self):
        self.position = self.position + self.velocity


class Space():

    def __init__(self, target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*50, random.random()*50])

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()

    def fitness(self, particle):
        return particle.position[0] ** 2 + particle.position[1] ** 2 + 1

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if(particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position


    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            if(self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        for particle in self.particles:
            global W
            new_velocity = (W*particle.velocity) + (c1*random.random()) * (particle.pbest_position - particle.position) + \
                           (random.random()*c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()


search_space = Space(1, target_error, n_particles)
particles_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particles_vector
search_space.print_particles()

iteration = 0
while(iteration < n_iterations):
    search_space.set_pbest()
    search_space.set_gbest()

    if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
        break

    search_space.move_particles()
    iteration += 1

print("The best solution is: ", search_space.gbest_position, " in n_iterations: ", iteration)
