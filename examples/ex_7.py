#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 13:04:29 2020

@author: arslan
"""

from pyit2fls import IT2FLS, Mamdani, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     min_t_norm, max_s_norm, TR_plot, crisp
from numpy import linspace
from time import time

t = time()
for i in range(1000):
    domain = linspace(0., 1., 100)
    
    Small = IT2FS_Gaussian_UncertStd(domain, [0, 0.15, 0.1, 1.])
    Medium = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.15, 0.1, 1.])
    Large = IT2FS_Gaussian_UncertStd(domain, [1., 0.15, 0.1, 1.])
    
    myIT2FLS = Mamdani(min_t_norm, max_s_norm)
    myIT2FLS.add_input_variable("x1")
    myIT2FLS.add_input_variable("x2")
    myIT2FLS.add_output_variable("y1")
    myIT2FLS.add_output_variable("y2")
    
    myIT2FLS.add_rule([("x1", Small), ("x2", Small)], [("y1", Small), ("y2", Large)])
    myIT2FLS.add_rule([("x1", Medium), ("x2", Medium)], [("y1", Medium), ("y2", Small)])
    myIT2FLS.add_rule([("x1", Large), ("x2", Large)], [("y1", Large), ("y2", Small)])
    
    it2out, tr = myIT2FLS.evaluate({"x1":0.923, "x2":0.745})
    
print(it2out, tr)
    

print("Mamdani average execution time:", (time() -t) / 1000)


t = time()
for i in range(1000):
    domain = linspace(0., 1., 100)
    
    Small = IT2FS_Gaussian_UncertStd(domain, [0, 0.15, 0.1, 1.])
    Medium = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.15, 0.1, 1.])
    Large = IT2FS_Gaussian_UncertStd(domain, [1., 0.15, 0.1, 1.])
    
    myIT2FLS = IT2FLS()
    myIT2FLS.add_input_variable("x1")
    myIT2FLS.add_input_variable("x2")
    myIT2FLS.add_output_variable("y1")
    myIT2FLS.add_output_variable("y2")
    
    myIT2FLS.add_rule([("x1", Small), ("x2", Small)], [("y1", Small), ("y2", Large)])
    myIT2FLS.add_rule([("x1", Medium), ("x2", Medium)], [("y1", Medium), ("y2", Small)])
    myIT2FLS.add_rule([("x1", Large), ("x2", Large)], [("y1", Large), ("y2", Small)])
    
    it2out, tr = myIT2FLS.evaluate({"x1":0.923, "x2":0.745}, min_t_norm, max_s_norm, domain, 
                                   method= "Centroid", algorithm= "KM")
    
print(it2out, tr)

print("IT2FLS average execution time:", (time() -t) / 1000)




