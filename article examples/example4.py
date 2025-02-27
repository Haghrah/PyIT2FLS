#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:11:44 2024

@author: arslan
"""

from pyit2fls import (IT2Mamdani_ML, IT2FS_Gaussian_UncertMean, 
                      Optimizer, )
from numpy import (linspace, array, pi, sin, argmin, argmax, 
                   cos, meshgrid, zeros_like, sum, zeros, )
from numpy.random import (rand, uniform, randint, )
import matplotlib.pyplot as plt


class HSO(Optimizer):
    def __init__(self, population_size, solution_size, objective_function, bounds, args=None):
        super().__init__(population_size, solution_size, objective_function, bounds, args)

        # Initialize Harmony Memory (HM) randomly
        self.hm = uniform(low=self.bounds[0], high=self.bounds[1], size=(self.population_size, self.solution_size))
        self.hm_fitness = []
        for harmony in self.hm:
            try:
                self.hm_fitness.append(self.objective_function(harmony, *self.args))
            except:
                self.hm_fitness.append(float("inf"))
        self.hm_fitness = array(self.hm_fitness)
        
        best_index = argmin(self.hm_fitness)
        self.best_solution = self.hm[best_index]
        self.best_fitness = self.hm_fitness[best_index]

    def iterate(self, algorithm_params): # hmcr=0.9, par=0.3, bw=0.01
        new_harmony = zeros(self.solution_size)
        
        for i in range(self.solution_size):
            if rand() < algorithm_params[2]:
                # Memory consideration
                new_harmony[i] = self.hm[randint(0, self.population_size), i]
                if rand() < algorithm_params[3]:
                    # Pitch adjustment
                    new_harmony[i] += uniform(-algorithm_params[4], algorithm_params[4])
            else:
                # Random selection
                new_harmony[i] = uniform(self.bounds[0], self.bounds[1])
        try:
            new_fitness = self.objective_function(new_harmony, *self.args)
        except:
            new_fitness = float("inf")

        # Update Harmony Memory
        worst_index = argmax(self.hm_fitness)
        if new_fitness < self.hm_fitness[worst_index]:
            self.hm[worst_index] = new_harmony
            self.hm_fitness[worst_index] = new_fitness
        
        best_index = argmin(self.hm_fitness)
        self.best_solution = self.hm[best_index]
        self.best_fitness = self.hm_fitness[best_index]
        
        return self.best_fitness


X1 = linspace(-pi, pi, 10)
X2 = linspace(-pi, pi, 10)

X = []
y = []
noise = 1.0 * (rand(len(X1), len(X2)) - 0.5)
for i, x1 in zip(range(len(X1)), X1):
    for j, x2 in zip(range(len(X2)), X2):
        X.append([x1, x2])
        y.append(sin(x1) + cos(x2) + noise[i, j])
X = array(X)

N = 2
M = 4
myIT2Mamdani = IT2Mamdani_ML(N, M, IT2FS_Gaussian_UncertMean, (-pi, pi), 
                             algorithm=HSO, 
                             algorithm_params=[10, 5000, 0.95, 0.9, 0.05])
err, conv = myIT2Mamdani.fit(X, y)

x1, x2 = meshgrid(X1, X2)
y1 = sin(x1) + cos(x2) + noise
y2 = zeros_like(y1)
for i in range(10):
    for j in range(10):
        y2[i, j] = myIT2Mamdani.score(array([X1[j], X2[i], ]))

y3 = sin(x1) + cos(x2)

print(f"Fitting error with respect to original surface: {sum((y2-y3) ** 2) ** 0.5}")
print(f"Fitting error with respect to noisy surface: {sum((y2-y1) ** 2) ** 0.5}")


plt.figure(figsize=(8, 5))
plt.plot(conv, label="HSO Algorithm")
plt.legend()
plt.title("Convergence Diagram")
plt.grid(which="major", linestyle="-", linewidth=0.75, color="gray", alpha=0.7)
plt.minorticks_on() 
plt.grid(which="minor", linestyle=":", linewidth=0.5, color="lightgray", alpha=0.7)
plt.xlabel("Iteration")
plt.ylabel("Objective function")
plt.savefig("../images/example4_conv.pdf", format="pdf", dpi=600, bbox_inches="tight")
plt.show()

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')
original = ax.plot_surface(x1, x2, y3, cmap="Blues", 
                            vmin=y1.min(), vmax=y1.max())
fig.colorbar(original, ax=ax, shrink=0.5, aspect=10, 
              label="Original Surface")
ax.view_init(elev=10, azim=-60)
ax.set_xlabel(r"$x_{1}$")
ax.set_ylabel(r"$x_{2}$")

plt.tight_layout()
plt.savefig("example4_1.pdf", format="pdf", 
            dpi=600, bbox_inches="tight")
plt.show()


fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')
fitted = ax.plot_surface(x1, x2, y1, cmap="Blues", 
                          vmin=y1.min(), vmax=y1.max())
fig.colorbar(fitted, ax=ax, shrink=0.5, aspect=10, 
              label="Noisy Surface")
ax.view_init(elev=10, azim=-60)
ax.set_xlabel(r"$x_{1}$")
ax.set_ylabel(r"$x_{2}$")

plt.tight_layout()
plt.savefig("example4_2.pdf", format="pdf", 
            dpi=600, bbox_inches="tight")
plt.show()


fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')
error_surface = ax.plot_surface(x1, x2, abs(y2 - y3), 
                                cmap="Greens", alpha=0.8)
fig.colorbar(error_surface, ax=ax, shrink=0.5, aspect=10, 
              label="Error Surface")
ax.plot_surface(x1, x2, y2, cmap="Blues", alpha=0.7)
ax.view_init(elev=10, azim=-60)
ax.set_xlabel(r"$x_{1}$")
ax.set_ylabel(r"$x_{2}$")

plt.tight_layout()
plt.savefig("example4_3.pdf", format="pdf", 
            dpi=600, bbox_inches="tight")
plt.show()





















