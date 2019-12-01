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

Xmin / Ymin = -2
Xmax / Ymax = +2

minGlobal = +1
'''
#!/usr/bin/env python

################################################################################
# File name: pso.py                                                            #
# Description: A module that solves a minimization problem using PSO           #
#------------------------------------------------------------------------------#
# Author: Hussein S. Al-Olimat                                                 #
# Email: hussein@knoesis.org                                                   #
#------------------------------------------------------------------------------#
# Date-last-modified: Nov 7, 2016                                              #
# Python-version: 2.7                                                          #
################################################################################
# This file is part of hussein.space: Hussein S. Al-Olimat's weblog -          #
# Blogging about computer science things I've done or intesetred in            #
#------------------------------------------------------------------------------#
# This code is licensed under a Creative Commons Attribution 4.0 International #
# License. The full license terms and conditions can be found over:            #
# https://creativecommons.org/licenses/by/4.0/                                 #
################################################################################


import random
import sys

################################################################################

# the x and y in our function (x - y + 7) (aka. dimensions)
number_of_variables = 2
# the minimum possible value x or y can take
min_value = -2
# the maximum possible value x or y can take
max_value = 2
# the number of particles in the swarm
number_of_particles = 10
# number of times the algorithm moves each particle in the problem space
number_of_iterations = 2000

w = 0.729    # inertia
c1 = 1.49 # cognitive (particle)
c2 = 1.49 # social (swarm)

################################################################################

class Particle:

    # this is only done one time when we create each particle
    # value of positions, velocities, fitness, best fitness, and best positions
    # is going to be updated later in the code during each iteration
    def __init__(self, number_of_variables, min_value, max_value):

        # init x and y values
        self.positions = [0.0 for v in range(number_of_variables)]
        # init velocities of x and y
        self.velocities = [0.0 for v in range(number_of_variables)]

        for v in range(number_of_variables):
            # update x and y positions
            self.positions[v] = ((max_value - min_value) * random.random()
                                + min_value)
            # update x and y velocities
            self.velocities[v] = ((max_value - min_value) * random.random()
                                + min_value)

        # current fitness after updating the x and y values
        self.fitness = Fitness(self.positions)
        # the current particle positions as the best fitness found yet
        self.best_particle_positions = list(self.positions)
        # the current particle fitness as the best fitness found yet
        self.best_particle_fitness = self.fitness

#Rosenbrock
def Fitness(positions):
    x = particle[0]
    y = particle[1]
    a = 1. - x
    b = y - x * x
    return (b * b * 100.) + (a * a)

# calculate a new velocity for one variable
def calculate_new_velocity_value(particle, v):

    # generate random numbers
    r1 = random.random()
    r2 = random.random()

    # the learning rate part
    part_1 = (w * particle.velocities[v])
    # the cognitive part - learning from itself
    part_2 = (c1 * r1 * (particle.best_particle_positions[v] - particle.positions[v]))
    # the social part - learning from others
    part_3 = (c2 * r2 * (best_swarm_positions[v] - particle.positions[v]))

    new_velocity = part_1 + part_2 + part_3

    return new_velocity

################################################################################

# create the swarm
swarm = [Particle(number_of_variables, min_value, max_value)
                    for __x in range(number_of_particles)]

######################################### best particle error and positions ####

best_swarm_positions = [0.0 for v in range(number_of_variables)]
best_swarm_fitness = sys.float_info.max

for particle in swarm: # check each particle
    if particle.fitness < best_swarm_fitness:
        best_swarm_fitness = particle.fitness
        best_swarm_positions = list(particle.positions)

################################################################################

for __x in range(number_of_iterations):
    for particle in swarm:
        # start moving/updating particles to calculate new fitness

        # compute new velocities for each particle
        for v in range(number_of_variables):

            particle.velocities[v] = calculate_new_velocity_value(particle, v)

            if particle.velocities[v] < min_value:
                particle.velocities[v] = min_value
            elif particle.velocities[v] > max_value:
                particle.velocities[v] = max_value

        # compute new positions using the new velocities
        for v in range(number_of_variables):
            particle.positions[v] += particle.velocities[v]

            if particle.positions[v] < min_value:
                particle.positions[v] = min_value
            elif particle.positions[v] > max_value:
                particle.positions[v] = max_value

        # compute the fitness of the new positions
        particle.fitness = Fitness(particle.positions)

        # are the new positions a new best for the particle?
        if particle.fitness < particle.best_particle_fitness:
            particle.best_particle_fitness = particle.fitness
            particle.best_particle_positions = list(particle.positions)

        # are the new positions a new best overall?
        if particle.fitness < best_swarm_fitness:
            best_swarm_fitness = particle.fitness
            best_swarm_positions = list(particle.positions)


################################################################################

print(best_swarm_positions)