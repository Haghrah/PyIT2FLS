#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:11:44 2024

@author: arslan
"""

from pyit2fls import (IT2Mamdani_ML, IT2FS_Gaussian_UncertMean, 
                      IT2FS_plot, )
from numpy import (linspace, array, abs, pi, sin, 
                   cos, meshgrid, zeros_like, sum, 
                   column_stack, )
from numpy.random import (rand, )
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x1 = linspace(-pi, pi, 10)
x2 = linspace(-pi, pi, 10)

X1, X2 = meshgrid(x1, x2)

X = column_stack((X1.ravel(), X2.ravel()))
y1 = sin(X1) + cos(X2)
noise = 1.0 * (rand(len(X1), len(X2)) - 0.5)
y2 = y1 + noise

N = 2
M = 4


myIT2Mamdani = IT2Mamdani_ML(N, M, IT2FS_Gaussian_UncertMean, (-pi, pi), 
                             algorithm="GWO", 
                             algorithm_params=[200, 100, ])

err, conv = myIT2Mamdani.fit(X, y2.ravel())

y3 = myIT2Mamdani.score(X).reshape(X1.shape)

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')
original = ax.plot_surface(X1, X2, y1, cmap="Blues", 
                           vmin=y1.min(), vmax=y1.max())
fig.colorbar(original, ax=ax, shrink=0.5, aspect=10, 
              label="Original Surface")
ax.view_init(elev=10, azim=-60)
ax.set_xlabel(r"$x_{1}$")
ax.set_ylabel(r"$x_{2}$")

plt.tight_layout()
plt.savefig("example9_1.png", format="png", 
            dpi=600, bbox_inches="tight")
plt.show()


fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')
fitted = ax.plot_surface(X1, X2, y2, cmap="Blues", 
                         vmin=y2.min(), vmax=y2.max())
fig.colorbar(fitted, ax=ax, shrink=0.5, aspect=10, 
             label="Noisy Surface")
ax.view_init(elev=10, azim=-60)
ax.set_xlabel(r"$x_{1}$")
ax.set_ylabel(r"$x_{2}$")

plt.tight_layout()
plt.savefig("example9_2.png", format="png", 
            dpi=600, bbox_inches="tight")
plt.show()


fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111, projection='3d')
error_surface = ax.plot_surface(X1, X2, abs(y1 - y3), 
                                cmap="Greens", alpha=0.8)
fig.colorbar(error_surface, ax=ax, shrink=0.5, aspect=10, 
              label="Error Surface")
ax.plot_surface(X1, X2, y3, cmap="Blues", alpha=0.7)
ax.view_init(elev=10, azim=-60)
ax.set_xlabel(r"$x_{1}$")
ax.set_ylabel(r"$x_{2}$")

plt.tight_layout()
plt.savefig("example9_3.png", format="png", 
            dpi=600, bbox_inches="tight")
plt.show()



systemData = open("data_Ex9.txt", "w")

for i, rule in zip(range(len(myIT2Mamdani.model.it2mamdani.rules)), 
                   myIT2Mamdani.model.it2mamdani.rules):
    IT2FS_plot(rule[0][0][1], rule[0][1][1], rule[1][0][1], title=f"Rule {i+1}", 
                legends=[r"$X_{1}$", r"$X_{2}$", r"$Y$", ], 
                filename=f"example8_{i+4}", ext="png")
    ruleText = f"Rule {i+1}: IF X1 IS [{rule[0][0][1]}] AND X2 IS [{rule[0][1][1]}] THEN Y IS [{rule[1][0][1]}]"
    print(ruleText)
    systemData.write(ruleText + "\n")

systemData.close()


print(f"Fitting error with respect to original surface: {sum((y1 - y3) ** 2) ** 0.5}")
print(f"Fitting error with respect to noisy surface: {sum((y2 - y3) ** 2) ** 0.5}")

