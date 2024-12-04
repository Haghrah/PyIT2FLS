#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:25:30 2020

@author: arslan
"""

from numpy import linspace, meshgrid, zeros
from pyit2fls import T1FS, T1Mamdani, T1FS_plot, gaussian_mf
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# Defining the domain of the input variable x1.
domain1 = linspace(1., 2., 101)

# Defining the domain of the input variable x2.
domain2 = linspace(2., 3., 101)

# Defining the domain of the output variable y1.
domain3 = linspace(3., 4., 101)

# Defining the domain of the output variable y2.
domain4 = linspace(4., 5., 101)

SMALL1  = T1FS(domain1, gaussian_mf, [1.0, 0.15, 1.])
MEDIUM1 = T1FS(domain1, gaussian_mf, [1.5, 0.15, 1.])
LARGE1  = T1FS(domain1, gaussian_mf, [2.0, 0.15, 1.])

# T1FS_plot(SMALL1, MEDIUM1, LARGE1, legends=["Small", "Medium", "Large"])

SMALL2  = T1FS(domain2, gaussian_mf, [2.0, 0.15, 1.])
MEDIUM2 = T1FS(domain2, gaussian_mf, [2.5, 0.15, 1.])
LARGE2  = T1FS(domain2, gaussian_mf, [3.0, 0.15, 1.])

# T1FS_plot(SMALL2, MEDIUM2, LARGE2, legends=["Small", "Medium", "Large"])

LOW1 = T1FS(domain3, gaussian_mf, [3.0, 0.1, 1.])
HIGH1 = T1FS(domain3, gaussian_mf, [4.0, 0.1, 1.])

# T1FS_plot(LOW1, HIGH1, legends=["Low", "High"])

LOW2 = T1FS(domain4, gaussian_mf, [4.0, 0.1, 1.])
HIGH2 = T1FS(domain4, gaussian_mf, [5.0, 0.1, 1.])

# T1FS_plot(LOW2, HIGH2, legends=["Low", "High"])

SYS = T1Mamdani(engine="Minimum", defuzzification="CoG")
SYS.add_input_variable("x1")
SYS.add_input_variable("x2")
SYS.add_output_variable("y1")
SYS.add_output_variable("y2")

SYS.add_rule([("x1", SMALL1), ("x2", SMALL2)], [("y1", LOW1), ("y2", LOW2)])
SYS.add_rule([("x1", SMALL1), ("x2", MEDIUM2)], [("y1", LOW1), ("y2", HIGH2)])
SYS.add_rule([("x1", SMALL1), ("x2", LARGE2)], [("y1", LOW1), ("y2", HIGH2)])
SYS.add_rule([("x1", MEDIUM1), ("x2", SMALL2)], [("y1", LOW1), ("y2", LOW2)])
SYS.add_rule([("x1", MEDIUM1), ("x2", MEDIUM2)], [("y1", LOW1), ("y2", HIGH2)])
SYS.add_rule([("x1", MEDIUM1), ("x2", LARGE2)], [("y1", HIGH1), ("y2", HIGH2)])
SYS.add_rule([("x1", LARGE1), ("x2", SMALL2)], [("y1", HIGH1), ("y2", LOW2)])
SYS.add_rule([("x1", LARGE1), ("x2", MEDIUM2)], [("y1", HIGH1), ("y2", HIGH2)])
SYS.add_rule([("x1", LARGE1), ("x2", LARGE2)], [("y1", HIGH1), ("y2", HIGH2)])

X1, X2 = meshgrid(domain1, domain2)
Z1 = zeros(shape=(len(domain1), len(domain2)))
Z2 = zeros(shape=(len(domain1), len(domain2)))
for i, x1 in zip(range(len(domain1)), domain1):
    for j, x2 in zip(range(len(domain2)), domain2):
        s, c = SYS.evaluate({"x1":x1, "x2":x2})
        Z1[i, j], Z2[i, j] = c["y1"], c["y2"]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X1, X2, Z1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X1, X2, Z2, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()


