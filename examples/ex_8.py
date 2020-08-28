#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 13:22:01 2020

@author: arslan
"""

from pyit2fls import TSK, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     product_t_norm, max_s_norm

from numpy import linspace
from time import time

domain = linspace(0., 1., 100)

Small = IT2FS_Gaussian_UncertStd(domain, [0, 0.15, 0.1, 1.])
Medium = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.15, 0.1, 1.])
Large = IT2FS_Gaussian_UncertStd(domain, [1., 0.15, 0.1, 1.])
IT2FS_plot(Small, Medium, Large, title="Sets", 
           legends=["Small", "Medium", "Large"])

myIT2FLS = TSK(product_t_norm, max_s_norm)

myIT2FLS.add_input_variable("x1")
myIT2FLS.add_input_variable("x2")
myIT2FLS.add_output_variable("y1")
myIT2FLS.add_output_variable("y2")

# IF x1 is Small AND x2 is Small
# THEN y1 = x1 + 2.3 x2 + 0.5 AND y2 = 1.2 x1 + 1.5 x2 + 1.
myIT2FLS.add_rule([("x1", Small), ("x2", Small)], 
                  [("y1", {"const":0.5, "x1":1., "x2":2.3}), 
                   ("y2", {"const":1., "x1":1.2, "x2":1.5})])

# IF x1 is Medium AND x2 is Medium
# THEN y1 = 2.7 x1 + 1.9 x2 + 1. AND y2 = 2.5 x1 + 2. x2 + 1.
myIT2FLS.add_rule([("x1", Medium), ("x2", Medium)], 
                  [("y1", {"const":1., "x1":2.7, "x2":1.9}), 
                   ("y2", {"const":1., "x1":2.5, "x2":2.})])

# IF x1 is Large AND x2 is Large
# THEN y1 = 2. x1 + 3. x2 + 1. AND y2 = x1 + x2 + 2.
myIT2FLS.add_rule([("x1", Large), ("x2", Large)], 
                  [("y1", {"const":1., "x1":2., "x2":3.}), 
                   ("y2", {"const":2., "x1":1., "x2":1.})])

print(myIT2FLS.evaluate({"x1":0.9, "x2":0.9}))





















