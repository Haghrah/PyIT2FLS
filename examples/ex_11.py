#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:16:26 2020

@author: arslan
"""

from pyit2fls import IT2FS_Gaussian_UncertMean, meet, IT2FS_plot, \
    min_t_norm, product_t_norm, lukasiewicz_t_norm, \
    drastic_t_norm, nilpotent_minimum_t_norm, hamacher_product_t_norm
from numpy import linspace


domain = linspace(-1., 7., 8001)
A1 = IT2FS_Gaussian_UncertMean(domain, [0., 0.2, 0.5, 1.])
A2 = IT2FS_Gaussian_UncertMean(domain, [1., 0.2, 0.5, 1.])
A3 = IT2FS_Gaussian_UncertMean(domain, [2., 0.2, 0.5, 1.])
A4 = IT2FS_Gaussian_UncertMean(domain, [3., 0.2, 0.5, 1.])
A5 = IT2FS_Gaussian_UncertMean(domain, [4., 0.2, 0.5, 1.])
A6 = IT2FS_Gaussian_UncertMean(domain, [5., 0.2, 0.5, 1.])
A7 = IT2FS_Gaussian_UncertMean(domain, [6., 0.2, 0.5, 1.])
IT2FS_plot(A1, A2, A3, A4, A5, A6, A7, title="Sets", 
           legends=["Set 1", "Set 2", "Set 3", "Set 4", 
                    "Set 5", "Set 6", "Set 7"])

M1 = meet(domain, A1, A2, min_t_norm)
M2 = meet(domain, A2, A3, product_t_norm)
M3 = meet(domain, A3, A4, lukasiewicz_t_norm)
M4 = meet(domain, A4, A5, drastic_t_norm)
M5 = meet(domain, A5, A6, nilpotent_minimum_t_norm)
M6 = meet(domain, A6, A7, hamacher_product_t_norm)

IT2FS_plot(M1, M2, M3, M4, M5, M6, 
           legends=["Minimum (1, 2)", "Product (2, 3)", 
                    "Lukasiewicz (3, 4)", "Drastic (4, 5)", 
                    "Nilpotent Minimum (5, 6)", "Hamacher Product (6, 7)"])











