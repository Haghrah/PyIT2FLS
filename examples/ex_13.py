#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:16:26 2020

@author: arslan
"""

from pyit2fls import IT2FS_Gaussian_UncertMean, meet, \
    hamacher_product_t_norm, IT2FS_plot
from numpy import linspace


domain = linspace(0., 1., 1000)
A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.25, 1.])
B = IT2FS_Gaussian_UncertMean(domain, [1., 0.1, 0.25, 1.])
IT2FS_plot(A, B, legends=["Small","Large"])

AB1 = meet(domain, A, B, hamacher_product_t_norm)
AB1.plot()


