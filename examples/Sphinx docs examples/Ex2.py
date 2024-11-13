#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:43:11 2024

@author: arslan
"""

from pyit2fls import (T1TSK, T1FS, gaussian_mf, T1FS_plot, )
from numpy import (linspace, meshgrid, zeros, )
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import (LinearLocator, FormatStrFormatter, )

domain = linspace(-1.5, 1.5, 100)
t1fs1 = T1FS(domain, gaussian_mf, [-0.5, 0.5, 1.])
t1fs2 = T1FS(domain, gaussian_mf, [ 0.5, 0.5, 1.])
T1FS_plot(t1fs1, t1fs2, legends=["Gaussian Set 1", "Gaussian Set 2", ])

myT1TSK = T1TSK()
myT1TSK.add_input_variable("X1")
myT1TSK.add_input_variable("X2")

myT1TSK.add_output_variable("Y")

def Y1(X1, X2):
    return 2. * X1 + 3. * X2

def Y2(X1, X2):
    return -1.5 * X1 + 2. * X2

def Y3(X1, X2):
    return -2. * X1 - 1.2 * X2

def Y4(X1, X2):
    return 5. * X1 - 2.5 * X2

myT1TSK.add_rule([("X1", t1fs1), ("X2", t1fs1)], 
             [("Y", Y1), ])
myT1TSK.add_rule([("X1", t1fs1), ("X2", t1fs2)], 
             [("Y", Y2), ])
myT1TSK.add_rule([("X1", t1fs2), ("X2", t1fs1)], 
             [("Y", Y3), ])
myT1TSK.add_rule([("X1", t1fs2), ("X2", t1fs2)], 
             [("Y", Y4), ])

X1, X2 = meshgrid(domain, domain)
O = zeros(shape=X1.shape)

for i, x1 in zip(range(len(domain)), domain):
    for j, x2 in zip(range(len(domain)), domain):
        o = myT1TSK.evaluate({"X1":x1, "X2":x2}, params=(x1, x2))
        O[i, j] = o["Y"]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X1, X2, O, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()













