#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:35:28 2020

@author: arslan
"""


from pyit2fls import IT2TSK, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     product_t_norm, max_s_norm
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy import linspace, meshgrid, zeros
from time import time

domain = linspace(0., 1., 100)

X1, X2 = meshgrid(domain, domain)
Y11 = X1 + X2 + 1.
Y12 = 2. * X1 - X2 + 1.
Y21 = 1.5 * X1 + 0.5 * X2 + 0.5
Y22 = 1.5 * X1 - 0.5 * X2 + 0.5
Y31 = 2. * X1 + 0.1 * X2 - 0.2
Y32 = 0.5 * X1 + 0.1 * X2 + 0.
Y41 = 4. * X1 - 0.5 * X2 - 1.
Y42 = -0.5 * X1 + X2 - 0.5

fig = plt.figure(figsize=plt.figaspect(0.25))
ax = fig.add_subplot(1, 4, 1, projection="3d")
surf = ax.plot_surface(X1, X2, Y11, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax = fig.add_subplot(1, 4, 2, projection="3d")
surf = ax.plot_surface(X1, X2, Y21, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax = fig.add_subplot(1, 4, 3, projection="3d")
surf = ax.plot_surface(X1, X2, Y31, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax = fig.add_subplot(1, 4, 4, projection="3d")
surf = ax.plot_surface(X1, X2, Y41, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.show()

fig = plt.figure(figsize=plt.figaspect(0.25))
ax = fig.add_subplot(1, 4, 1, projection="3d")
surf = ax.plot_surface(X1, X2, Y12, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax = fig.add_subplot(1, 4, 2, projection="3d")
surf = ax.plot_surface(X1, X2, Y22, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax = fig.add_subplot(1, 4, 3, projection="3d")
surf = ax.plot_surface(X1, X2, Y32, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax = fig.add_subplot(1, 4, 4, projection="3d")
surf = ax.plot_surface(X1, X2, Y42, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.show()


Small = IT2FS_Gaussian_UncertStd(domain, [0, 0.15, 0.1, 1.])
Big = IT2FS_Gaussian_UncertStd(domain, [1., 0.15, 0.1, 1.])
# IT2FS_plot(Small, Big, title="Sets", 
#            legends=["Small", "Big"])

myIT2FLS = IT2TSK(product_t_norm, max_s_norm)

myIT2FLS.add_input_variable("x1")
myIT2FLS.add_input_variable("x2")
myIT2FLS.add_output_variable("y1")
myIT2FLS.add_output_variable("y2")

myIT2FLS.add_rule([("x1", Small), ("x2", Small)], 
                  [("y1", {"const":1., "x1":1., "x2":1.}), 
                   ("y2", {"const":1., "x1":2., "x2":-1.})])
myIT2FLS.add_rule([("x1", Small), ("x2", Big)], 
                  [("y1", {"const":0.5, "x1":1.5, "x2":0.5}), 
                   ("y2", {"const":0.5, "x1":1.5, "x2":-0.5})])
myIT2FLS.add_rule([("x1", Big), ("x2", Small)], 
                  [("y1", {"const":-0.2, "x1":2., "x2":0.1}), 
                   ("y2", {"const":0., "x1":0.5, "x2":0.1})])
myIT2FLS.add_rule([("x1", Big), ("x2", Big)], 
                  [("y1", {"const":-1., "x1":4., "x2":-0.5}), 
                   ("y2", {"const":-0.5, "x1":-0.5, "x2":1.})])


Z1 = zeros(shape=X1.shape)
Z2 = zeros(shape=X1.shape)

for i, x1 in zip(range(len(domain)), domain):
    for j, x2 in zip(range(len(domain)), domain):
        z = myIT2FLS.evaluate({"x1":x1, "x2":x2})
        Z1[i, j], Z2[i, j] = z["y1"], z["y2"]


fig = plt.figure()
ax = fig.gca(projection="3d")
surf = ax.plot_surface(X1, X2, Z1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

fig = plt.figure()
ax = fig.gca(projection="3d")
surf = ax.plot_surface(X1, X2, Z2, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()











