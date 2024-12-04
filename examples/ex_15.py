#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 10:32:55 2020

@author: arslan
"""


from pyit2fls import T1FS, gaussian_mf, T1FS_plot, T1TSK
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy import linspace, meshgrid, zeros
from time import time

#%%
# The universe of discourse for all input variables are same -> [0, 1)
domain = linspace(0., 1., 100)


#%%
# The fuzzy system will be evaluated in the [0, 1) x [0, 1) space. 
X1, X2 = meshgrid(domain, domain)


# %%
# Eight functions are defined, that are used in consequence
# part of the rules in the fuzzy rule-base.
def y11(x1, x2):
    return x1 + x2 + 1.

def y12(x1, x2):
    return 2. * x1 - x2 + 1.

def y21(x1, x2):
    return 1.5 * x1 + 0.5 * x2 + 0.5

def y22(x1, x2):
    return 1.5 * x1 - 0.5 * x2 + 0.5

def y31(x1, x2):
    return 2. * x1 + 0.1 * x2 - 0.2

def y32(x1, x2):
    return 0.5 * x1 + 0.1 * x2 + 0.

def y41(x1, x2):
    return 4. * x1 - 0.5 * x2 - 1.

def y42(x1, x2):
    return -0.5 * x1 + x2 - 0.5


# %%
# Defined surfaces for being used in consequence part of rules are 
# evaluated and plotted here:
Y11 = y11(X1, X2)
Y12 = y12(X1, X2)
Y21 = y21(X1, X2)
Y22 = y22(X1, X2)
Y31 = y31(X1, X2)
Y32 = y32(X1, X2)
Y41 = y41(X1, X2)
Y42 = y42(X1, X2)

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


# %%
# The fuzzy sets representing the universe of discourse of the 
# fuzzy system are defined and plotted here:
Small = T1FS(domain, gaussian_mf, [0, 0.15, 1.])
Big = T1FS(domain, gaussian_mf, [1., 0.15, 1.])

T1FS_plot(Small, Big, title="Sets", 
          legends=["Small", "Big"])

# The fuzzy system is created using the T1TSK class:
SYS = T1TSK()

# Input and output variables are defined and added to the fuzzy system.
SYS.add_input_variable("x1")
SYS.add_input_variable("x2")
SYS.add_output_variable("y1")
SYS.add_output_variable("y2")

# Rule-base of the fuzzy system is defined here:
# The previously defined functions (yij) are used here.
SYS.add_rule([("x1", Small), ("x2", Small)], 
             [("y1", y11), 
              ("y2", y12)])
SYS.add_rule([("x1", Small), ("x2", Big)], 
             [("y1", y21), 
              ("y2", y22)])
SYS.add_rule([("x1", Big), ("x2", Small)], 
             [("y1", y31), 
              ("y2", y32)])
SYS.add_rule([("x1", Big), ("x2", Big)], 
             [("y1", y41), 
              ("y2", y42)])


# %%
# The output planes of the fuzzy system are evaluated and plotted here:
Z1 = zeros(shape=X1.shape)
Z2 = zeros(shape=X1.shape)

for i, x1 in zip(range(len(domain)), domain):
    for j, x2 in zip(range(len(domain)), domain):
        # The params input of the evaluate function indicates the inputs of
        # the functions given in the consequence part of the rules.
        z = SYS.evaluate({"x1":x1, "x2":x2}, params=(x1, x2))
        Z1[i, j], Z2[i, j] = z["y1"], z["y2"]


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










