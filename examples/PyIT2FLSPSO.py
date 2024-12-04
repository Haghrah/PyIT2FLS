#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:48:37 2018

@author: arslan
"""

from numpy import random, shape
import numpy as np
import matplotlib.pyplot as plt

class Particle:

    def __init__(self, solution_generator_function, velocity_generator_function):
        self.cost = float("inf")
        self.best_known_cost = float("inf")
        self.position = solution_generator_function()
        self.velocity = velocity_generator_function()
        self.best_known_position = self.position.copy()
        return

    def __repr__(self):
        o = "Position:\n"
        for d in self.position:
            o += str(d) + "\n"
        o += "Current cost: " + str(self.cost) + "\nBest known position:\n"
        for d in self.best_known_position:
            o += str(d) + "\n"
        o += "Best known cost: " + str(self.best_known_cost)
        return o

class PyPSO:
    
    def __init__(self, cost_function, particle_num, iteration_num, solution_generator_function, velocity_generator_function, omega=0.3, phi_p=0.3, phi_g=2.1):
        self.cost_function = cost_function
        self.particle_num = particle_num
        self.iteration_num = iteration_num
        self.omega = omega
        self.phi_p = phi_p
        self.phi_g = phi_g
        self.particles = []
        self.best_known_cost = float("inf")
        self.best_known_position = []
        for i in range(self.particle_num):
            self.particles.append(Particle(solution_generator_function, velocity_generator_function))
            self.particles[i].cost = self.cost_function(self.particles[i].position)
            self.particles[i].best_known_cost = self.particles[i].cost
            if self.particles[i].cost < self.best_known_cost:
                self.best_known_position = self.particles[i].position.copy()
                self.best_known_cost = self.particles[i].cost
            print("Particle", i+1, "created!")
        return
    
    def __repr__(self):
        o = "Best known position:\n"
        for d in self.best_known_position:
            o += str(d) + "\n"
        o += "Best known cost: " + str(self.best_known_cost)
        return o
    
    def solve(self):
        print("Solver has started!")
        convergence = []
        for i in range(self.iteration_num):
            for particle in self.particles:
                r_p = random.random(size=shape(particle.position))
                r_g = random.random(size=shape(particle.position))
                particle.velocity = self.omega * particle.velocity + \
                    self.phi_p * r_p * (particle.best_known_position - particle.position) + \
                    self.phi_g * r_g * (self.best_known_position- particle.position)
                particle.position = np.abs(particle.position + particle.velocity)
                particle.cost = self.cost_function(particle.position)
                if particle.cost < particle.best_known_cost:
                    particle.best_known_position = particle.position.copy()
                    particle.best_known_cost = particle.cost
                    if particle.best_known_cost < self.best_known_cost:
                        self.best_known_position = particle.best_known_position.copy()
                        self.best_known_cost = particle.best_known_cost
            print("Iteration. " + str(i+1))
            print(self.best_known_cost)
            convergence.append(self.best_known_cost)
        plt.figure()
        plt.plot(convergence)
        plt.title("Convergence diagram")
        plt.xlabel("Iteration")
        plt.ylabel("Total cost")
        plt.grid(True)
        plt.show()
        return convergence

if __name__ == "__main__":
    print("PSO algorithm library")






