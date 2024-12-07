#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 00:11:49 2020

@author: arslan
"""

from pyit2fls import (IT2Mamdani, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     product_t_norm, max_s_norm, crisp, )
from numpy import (linspace, meshgrid, zeros, )
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import (LinearLocator, FormatStrFormatter, )

# Defining the domain of the input variable x1.
domain1 = linspace(1., 2., 100)

# Defining the domain of the input variable x2.
domain2 = linspace(2., 3., 100)

# Defining the domain of the output variable y1.
domain3 = linspace(3., 4., 100)

# Defining the domain of the output variable y2.
domain4 = linspace(4., 5., 100)

# Defining the Small set for the input variable x1.
Small1 = IT2FS_Gaussian_UncertStd(domain1, [1., 0.2, 0.025, 1.])

# Defining the Medium set for the input variable x1.
Medium1 = IT2FS_Gaussian_UncertStd(domain1, [1.5, 0.3, 0.025, 1.])

# Defining the Large set for the input variable x1.
Large1 = IT2FS_Gaussian_UncertStd(domain1, [2., 0.4, 0.025, 1.])

# Plotting the sets defined for the input variable x1.
IT2FS_plot(Small1, Medium1, Large1, 
            legends=["Small", "Medium", "large"])


# Defining the Small set for the input variable x2.
Small2 = IT2FS_Gaussian_UncertStd(domain2, [2., 0.4, 0.025, 1.])

# Defining the Medium set for the input variable x2.
Medium2 = IT2FS_Gaussian_UncertStd(domain2, [2.5, 0.3, 0.025, 1.])

# Defining the Large set for the input variable x1.
Large2 = IT2FS_Gaussian_UncertStd(domain2, [3., 0.2, 0.025, 1.])

# Plotting the sets defined for the input variable x1.
IT2FS_plot(Small2, Medium2, Large2,
            legends=["Small", "Medium", "large"])

# Defining the Low set for the output variable y1
Low1 = IT2FS_Gaussian_UncertStd(domain3, [3., 0.5, 0.025, 1.])

# Defining the High set for the output variable y1
High1 = IT2FS_Gaussian_UncertStd(domain3, [4., 0.5, 0.025, 1.])

# Plotting the sets defined for the output variable y1.
IT2FS_plot(Low1, High1, 
            legends=["Low", "High"])


# Defining the Low set for the output variable y2
Low2 = IT2FS_Gaussian_UncertStd(domain4, [4., 0.5, 0.025, 1.])

# Defining the High set for the output variable y2
High2 = IT2FS_Gaussian_UncertStd(domain4, [5., 0.5, 0.025, 1.])

# Plotting the sets defined for the output variable y2.
IT2FS_plot(Low2, High2, 
            legends=["Low", "High"])

# Defining the mamdani interval type 2 fuzzy logic system
myIT2FLS = IT2Mamdani(product_t_norm, max_s_norm)

# Adding the input variables to the myIT2FLS
myIT2FLS.add_input_variable("x1")
myIT2FLS.add_input_variable("x2")

# Adding the output variables to the myIT2FLS
myIT2FLS.add_output_variable("y1")
myIT2FLS.add_output_variable("y2")

# Defining the rule base of the MyIT2FLS
myIT2FLS.add_rule([("x1", Small1), ("x2", Small2)], [("y1", Low1), ("y2", Low2)])
myIT2FLS.add_rule([("x1", Small1), ("x2", Medium2)], [("y1", Low1), ("y2", Low2)])
myIT2FLS.add_rule([("x1", Small1), ("x2", Large2)], [("y1", Low1), ("y2", High2)])
myIT2FLS.add_rule([("x1", Medium1), ("x2", Small2)], [("y1", Low1), ("y2", Low2)])
myIT2FLS.add_rule([("x1", Medium1), ("x2", Medium2)], [("y1", Low1), ("y2", Low2)])
myIT2FLS.add_rule([("x1", Medium1), ("x2", Large2)], [("y1", High1), ("y2", High2)])
myIT2FLS.add_rule([("x1", Large1), ("x2", Small2)], [("y1", High1), ("y2", Low2)])
myIT2FLS.add_rule([("x1", Large1), ("x2", Medium2)], [("y1", High1), ("y2", High2)])
myIT2FLS.add_rule([("x1", Large1), ("x2", Large2)], [("y1", High1), ("y2", High2)])

# Evaluating the outputs of the myIT2FLS for the points in the input domain, 
# and plotting the output surfaces.
X1, X2 = meshgrid(domain1, domain2)
Z1 = zeros(shape=(len(domain1), len(domain2)))
Z2 = zeros(shape=(len(domain1), len(domain2)))
for i, x1 in zip(range(len(domain1)), domain1):
    for j, x2 in zip(range(len(domain2)), domain2):
        it2out, tr = myIT2FLS.evaluate({"x1":x1, "x2":x2})
        Z1[i, j], Z2[i, j] = crisp(tr["y1"]), crisp(tr["y2"])

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






