#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:16:26 2020

@author: arslan
"""

from pyit2fls import IT2FS_Gaussian_UncertMean, join, IT2FS_plot, \
    max_s_norm, probabilistic_sum_s_norm, bounded_sum_s_norm, \
    drastic_s_norm, nilpotent_maximum_s_norm, einstein_sum_s_norm
from numpy import linspace


domain = linspace(-1., 7., 8001)
A1 = IT2FS_Gaussian_UncertMean(domain, [0., 0.2, 0.25, 1.])
A2 = IT2FS_Gaussian_UncertMean(domain, [1., 0.2, 0.25, 1.])
A3 = IT2FS_Gaussian_UncertMean(domain, [2., 0.2, 0.25, 1.])
A4 = IT2FS_Gaussian_UncertMean(domain, [3., 0.2, 0.25, 1.])
A5 = IT2FS_Gaussian_UncertMean(domain, [4., 0.2, 0.25, 1.])
A6 = IT2FS_Gaussian_UncertMean(domain, [5., 0.2, 0.25, 1.])
A7 = IT2FS_Gaussian_UncertMean(domain, [6., 0.2, 0.25, 1.])
IT2FS_plot(A1, A2, A3, A4, A5, A6, A7, title="Sets", 
           legends=["Set 1", "Set 2", "Set 3", "Set 4", 
                    "Set 5", "Set 6", "Set 7"])

M1 = join(domain, A1, A2, max_s_norm)
M2 = join(domain, A2, A3, probabilistic_sum_s_norm)
M3 = join(domain, A3, A4, bounded_sum_s_norm)
M4 = join(domain, A4, A5, drastic_s_norm)
M5 = join(domain, A5, A6, nilpotent_maximum_s_norm)
M6 = join(domain, A6, A7, einstein_sum_s_norm)

IT2FS_plot(M1, M3, M5, 
           legends=["Maximum (1, 2)", 
                    "Bounded Sum (3, 4)",
                    "Nilpotent Maximum (5, 6)", ], )

IT2FS_plot(M2, M4, M6, 
           legends=["Probabilistic Sum (2, 3)", 
                    "Drastic (4, 5)", 
                    "Einstein Sum (6, 7)"], )











