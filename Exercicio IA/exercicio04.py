'''
w = inicio 0.9 vai descendo ate 0,1
C1 É UM PESO PARA O MELHOR LOCAL
C2 É UM PESO PARA O MAIOR GLOBAL

R1

v1 = w * v1 + c1 * r1 (p1 - s1) +
v1 = 0.9 * 3

Usando alguma biblioteca ou implementando diretamente em alguma linguagem de programação,
desenvolva uma solução para minimizar a função de Rosenbrock (em anexo). Faça testes pra
identificar um conjunto de parâmetros adequado. Plote o gráfico de evolução da solução.

'''
import random
import numpy as np

W = 0.5
c1 = 0.8
c2 = 0.9

n_iterations = int(input("Inform the number of iterations: "))
target_error = float(input("Inform the target error: "))
n_particles = int(input("Inform the number of particles: "))


def fncRosenbrock(particle):
    x = particle[0]
    y = particle[1]
    a = 1. - x
    b = y - x * x
    return (b * b * 100.) + (a * a)

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
        return fncRosenbrock(particle)

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
