#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:56:00 2019

@author: arslan
"""

from pyit2fls import IT2FS_Gaussian_UncertMean, IT2FS_plot, meet, \
                     join, min_t_norm, max_s_norm
from numpy import linspace

domain = linspace(0., 1., 100)

A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.1])
B = IT2FS_Gaussian_UncertMean(domain, [0.33, 0.1, 0.1])
C = IT2FS_Gaussian_UncertMean(domain, [0.66, 0.1, 0.1])

IT2FS_plot(A, B, C, title="", legends=["Small","Medium","Large"], filename="multiSet")

AB = meet(domain, A, B, min_t_norm)
AB.plot(filename="meet")

BC = join(domain, B, C, max_s_norm)
BC.plot(filename="join")
