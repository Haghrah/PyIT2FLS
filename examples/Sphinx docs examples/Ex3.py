#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 09:03:02 2024

@author: arslan
"""

from pyit2fls import (T1Mamdani, T1FS, gaussian_mf, T1FS_plot, )
from numpy import (linspace, meshgrid, zeros, )
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import (LinearLocator, FormatStrFormatter, )

inputDomain = linspace(-1.5, 1.5, 100)
t1fs1 = T1FS(inputDomain, gaussian_mf, [-0.5, 0.5, 1.])
t1fs2 = T1FS(inputDomain, gaussian_mf, [ 0.5, 0.5, 1.])
T1FS_plot(t1fs1, t1fs2, legends=["Gaussian Set 1", "Gaussian Set 2", ])

outputDomain = linspace(-10., 10., 1000)
t1fs3 = T1FS(outputDomain, gaussian_mf, [-7.5, 2.0, 1.])
t1fs4 = T1FS(outputDomain, gaussian_mf, [-2.5, 2.0, 1.])
t1fs5 = T1FS(outputDomain, gaussian_mf, [ 2.5, 2.0, 1.])
t1fs6 = T1FS(outputDomain, gaussian_mf, [ 7.5, 2.0, 1.])
T1FS_plot(t1fs3, t1fs4, t1fs5, t1fs6, 
          legends=["Gaussian Set 3", "Gaussian Set 4", 
                   "Gaussian Set 5", "Gaussian Set 6", ])

myT1Mamdani = T1Mamdani(engine="Product", defuzzification="CoG")
myT1Mamdani.add_input_variable("X1")
myT1Mamdani.add_input_variable("X2")

myT1Mamdani.add_output_variable("Y")

myT1Mamdani.add_rule([("X1", t1fs1), ("X2", t1fs1)], [("Y", t1fs3), ])
myT1Mamdani.add_rule([("X1", t1fs1), ("X2", t1fs2)], [("Y", t1fs4), ])
myT1Mamdani.add_rule([("X1", t1fs2), ("X2", t1fs1)], [("Y", t1fs5), ])
myT1Mamdani.add_rule([("X1", t1fs2), ("X2", t1fs2)], [("Y", t1fs6), ])

X1, X2 = meshgrid(inputDomain, inputDomain)
O = zeros(shape=X1.shape)

for i, x1 in zip(range(len(inputDomain)), inputDomain):
    for j, x2 in zip(range(len(inputDomain)), inputDomain):
        s, c = myT1Mamdani.evaluate({"X1":x1, "X2":x2})
        O[i, j] = c["Y"]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X1, X2, O, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()



















