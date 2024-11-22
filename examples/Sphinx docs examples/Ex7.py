#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:41:48 2024

@author: arslan
"""


from pyit2fls import IT2Mamdani, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     min_t_norm, max_s_norm, crisp
from numpy import linspace, meshgrid, zeros
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

domain1 = linspace(1., 2., 100)
domain2 = linspace(2., 3., 100)
domain3 = linspace(3., 4., 100)

Small1  = IT2FS_Gaussian_UncertStd(domain1, [1.0, 0.2, 0.025, 1.])
Small2  = IT2FS_Gaussian_UncertStd(domain2, [2.0, 0.3, 0.025, 1.])
Medium1 = IT2FS_Gaussian_UncertStd(domain1, [1.5, 0.2, 0.025, 1.])
Medium2 = IT2FS_Gaussian_UncertStd(domain2, [2.5, 0.3, 0.025, 1.])
Large1  = IT2FS_Gaussian_UncertStd(domain1, [2.0, 0.2, 0.025, 1.])
Large2  = IT2FS_Gaussian_UncertStd(domain2, [3.0, 0.3, 0.025, 1.])

IT2FS_plot(Small1, Medium1, Large1, 
           legends=["Small 1", "Medium 1", "large 1"])
IT2FS_plot(Small2, Medium2, Large2,
           legends=["Smal 2l", "Medium 2", "large 2"])

Low1  = IT2FS_Gaussian_UncertStd(domain3, [3., 0.3, 0.025, 1.])
High1 = IT2FS_Gaussian_UncertStd(domain3, [4., 0.3, 0.025, 1.])

IT2FS_plot(Low1, High1, 
            legends=["Low", "High"])

myIT2FLS = IT2Mamdani(min_t_norm, max_s_norm)

myIT2FLS.add_input_variable("X1")
myIT2FLS.add_input_variable("X2")

myIT2FLS.add_output_variable("Y")

myIT2FLS.add_rule([("X1", Small1),  ("X2", Small2)],  [("Y", Low1),  ])
myIT2FLS.add_rule([("X1", Small1),  ("X2", Medium2)], [("Y", Low1),  ])
myIT2FLS.add_rule([("X1", Small1),  ("X2", Large2)],  [("Y", Low1),  ])
myIT2FLS.add_rule([("X1", Medium1), ("X2", Small2)],  [("Y", Low1),  ])
myIT2FLS.add_rule([("X1", Medium1), ("X2", Medium2)], [("Y", Low1),  ])
myIT2FLS.add_rule([("X1", Medium1), ("X2", Large2)],  [("Y", High1), ])
myIT2FLS.add_rule([("X1", Large1),  ("X2", Small2)],  [("Y", High1), ])
myIT2FLS.add_rule([("X1", Large1),  ("X2", Medium2)], [("Y", High1), ])
myIT2FLS.add_rule([("X1", Large1),  ("X2", Large2)],  [("Y", High1), ])

X1, X2 = meshgrid(domain1, domain2)
Z1 = zeros(shape=(len(domain1), len(domain2)))
for i, x1 in zip(range(len(domain1)), domain1):
    for j, x2 in zip(range(len(domain2)), domain2):
        it2out, tr = myIT2FLS.evaluate({"X1":x1, "X2":x2})
        Z1[i, j] = crisp(tr["Y"])

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X1, X2, Z1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()























