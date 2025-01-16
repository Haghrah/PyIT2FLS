#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:10:33 2021

@author: arslan
"""

from pyit2fls import (IT2FS_Gaussian_UncertMean, IT2FS_Emphasize, IT2FS_plot, 
                      T1FS, gaussian_mf, T1FS_Emphasize, T1FS_plot)
from numpy import linspace

domain = linspace(0., 1., 101)


IT2mySet = IT2FS_Gaussian_UncertMean(domain, [0.5, 0.1, 0.2, 1.], check_set=True)
IT2Emphasized_mySet = IT2FS_Emphasize(IT2mySet, m=3.)
IT2FS_plot(IT2mySet, IT2Emphasized_mySet, legends=["Simple", "Emphasized"])


T1mySet = T1FS(domain, mf=gaussian_mf, params=[0.5, 0.1, 1.])
T1Emphasized_mySet = T1FS_Emphasize(T1mySet, m=3.)
T1FS_plot(T1mySet, T1Emphasized_mySet, legends=["Simple", "Emphasized"])




