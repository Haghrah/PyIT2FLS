#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 02:40:21 2019

@author: arslan
"""

from pyit2fls import IT2Mamdani, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     min_t_norm, max_s_norm, TR_plot, crisp
from numpy import linspace

domain = linspace(0., 1., 100)  # Domain is defined as discrete space in the
                                # interval [0, 1] divided to 100 parts.

# The Small set is defined as a Guassian IT2FS with uncertain standard deviation 
# value. The mean, the standard deviation center, the standard deviation spread, 
# and the height of the set are set to 0., 0.15, 0.1, and 1., respectively.
Small = IT2FS_Gaussian_UncertStd(domain, [0, 0.15, 0.05, 1.])

# The Medium set is defined as a Guassian IT2FS with uncertain standard deviation 
# value. The mean, the standard deviation center, the standard deviation spread, 
# and the height of the set are set to 0.5, 0.15, 0.1, and 1., respectively.
Medium = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.15, 0.05, 1.])

# The Large set is defined as a Guassian IT2FS with uncertain standard deviation 
# value. The mean, the standard deviation center, the standard deviation spread, 
# and the height of the set are set to 1., 0.15, 0.1, and 1., respectively.
Large = IT2FS_Gaussian_UncertStd(domain, [1., 0.15, 0.05, 1.])

# Three sets, Small, Medium, and Large are plotted using the function IT2FS_plot.
IT2FS_plot(Small, Medium, Large, legends=["Small", "Medium", "large"], filename="simp_ex_sets")

# An Interval Type 2 Fuzzy Logic System is created. To evaluate the defined 
# IT2 Mamdani FLS the minimum t-norm and maximum s-norm are used. The centroid 
# method is selected for evaluating the IF-THEN rules and the KM algorithm is 
# selected as type reduction algorithm. 
# The variables and output variables are defined. As it can be seen, the 
# system has two inputs and two outputs.
myIT2FLS = IT2Mamdani(min_t_norm, max_s_norm, 
                      method="Centroid", algorithm="KM")
myIT2FLS.add_input_variable("x1")
myIT2FLS.add_input_variable("x2")
myIT2FLS.add_output_variable("y1")
myIT2FLS.add_output_variable("y2")

# Now we are going to add the fuzzy IF-THEN rules.
# There are three rules to add:
# 1. IF x1 is Small AND x2 is Small THEN y1 is Small AND y2 is Large
myIT2FLS.add_rule([("x1", Small), ("x2", Small)], [("y1", Small), ("y2", Large)])
# 2. IF x1 is Medium AND x2 is Medium THEN y1 is Medium AND y2 is Small
myIT2FLS.add_rule([("x1", Medium), ("x2", Medium)], [("y1", Medium), ("y2", Small)])
# 3. IF x1 is Large AND x2 is Large THEN y1 is Large AND y2 is Small
myIT2FLS.add_rule([("x1", Large), ("x2", Large)], [("y1", Large), ("y2", Small)])

# The first input is 0.923 and the second one is 0.745.
it2out, tr = myIT2FLS.evaluate({"x1":0.923, "x2":0.745})

# Here the output IT2FSs and their type reduced versions are plotted.
# The crisp output is also calculated and printed.
it2out["y1"].plot(filename="y1_out")
TR_plot(domain, tr["y1"], filename="y1_tr")
print(crisp(tr["y1"]))

it2out["y2"].plot(filename="y2_out")
TR_plot(domain, tr["y2"], filename="y2_tr")
print(crisp(tr["y2"]))





