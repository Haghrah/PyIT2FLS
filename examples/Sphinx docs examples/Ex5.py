#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:47:28 2024

@author: arslan
"""

from pyit2fls import (IT2FS, R_IT2FS_Gaussian_UncertStd, 
                      L_IT2FS_Gaussian_UncertStd, IT2FS_plot, 
                      hamacher_product_t_norm, probabilistic_sum_s_norm, 
                      meet, join)
from numpy import linspace

domain = linspace(1, 2, 1001)

RGaussian_UncertStd = R_IT2FS_Gaussian_UncertStd(domain, [1.25, 0.2, 0.05, 0.6])
LGaussian_UncertStd = L_IT2FS_Gaussian_UncertStd(domain, [1.75, 0.2, 0.05, 0.6])

MEET = meet(domain, RGaussian_UncertStd, LGaussian_UncertStd, hamacher_product_t_norm)
JOIN = meet(domain, RGaussian_UncertStd, LGaussian_UncertStd, probabilistic_sum_s_norm)

IT2FS_plot(RGaussian_UncertStd, LGaussian_UncertStd, 
           legends=["IT2FS1", 
                    "IT2FS2", ])

IT2FS_plot(MEET, JOIN, 
           legends=["MEET", 
                    "JOIN", ])
