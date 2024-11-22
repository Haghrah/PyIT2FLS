#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:41:38 2024

@author: arslan
"""

from pyit2fls import (IT2TSK, IT2FS_Gaussian_UncertStd, IT2FS_plot, 
                     product_t_norm, max_s_norm, )
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy import linspace, meshgrid, zeros

domain = linspace(0., 1., 100)

X1, X2 = meshgrid(domain, domain)

IT2FS1 = IT2FS_Gaussian_UncertStd(domain, [0, 0.2, 0.05, 1.])
IT2FS2 = IT2FS_Gaussian_UncertStd(domain, [1., 0.2, 0.05, 1.])
IT2FS_plot(IT2FS1, IT2FS2, title="Sets", 
            legends=["IT2FS1", "IT2FS2"])

myIT2FLS = IT2TSK(product_t_norm, max_s_norm)

myIT2FLS.add_input_variable("X1")
myIT2FLS.add_input_variable("X2")
myIT2FLS.add_output_variable("Y")

myIT2FLS.add_rule([("X1", IT2FS1), ("X2", IT2FS1)], 
                  [("Y", {"const":1., "X1":1., "X2":1.}), ])
myIT2FLS.add_rule([("X1", IT2FS1), ("X2", IT2FS2)], 
                  [("Y", {"const":0.5, "X1":1.5, "X2":0.5}), ])
myIT2FLS.add_rule([("X1", IT2FS2), ("X2", IT2FS1)], 
                  [("Y", {"const":-0.2, "X1":2., "X2":0.1}), ])
myIT2FLS.add_rule([("X1", IT2FS2), ("X2", IT2FS2)], 
                  [("Y", {"const":-1., "X1":4., "X2":-0.5}), ])


O = zeros(shape=X1.shape)

for i, x1 in zip(range(len(domain)), domain):
    for j, x2 in zip(range(len(domain)), domain):
        o = myIT2FLS.evaluate({"X1":x1, "X2":x2})
        O[i, j] = o["Y"]


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X1, X2, O, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()















