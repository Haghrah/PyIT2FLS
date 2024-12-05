#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:56:00 2019

@author: arslan
"""

from pyit2fls import (IT2FS_Gaussian_UncertMean, IT2FS_plot, MEET, \
                     JOIN, min_t_norm, max_s_norm, )
from numpy import linspace


# Defining three interval type 2 fuzzy sets for testing the meet and join 
# functions.

# Domain is defined as discrete space in the interval [0, 1] divided to 100 parts.
domain = linspace(0., 1., 100)

# The first IT2FLS is defined as a Gaussian set with uncertain mean value.
# Center of the mean = 0.25, 
# Spread of the mean = 0.1, 
# Standard deviation = 0.1, and 
# Height = 1.
A = IT2FS_Gaussian_UncertMean(domain, [0.25, 0.1, 0.1, 1.])

# The second IT2FLS is defined as a Gaussian set with uncertain mean value.
# Center of the mean = 0.5, 
# Spread of the mean = 0.1, 
# Standard deviation = 0.1, and 
# Height = 1.
B = IT2FS_Gaussian_UncertMean(domain, [0.5, 0.1, 0.1, 1.])

# The third IT2FLS is defined as a Gaussian set with uncertain mean value.
# Center of the mean = 0.75, 
# Spread of the mean = 0.1, 
# Standard deviation = 0.1, and 
# Height = 1.
C = IT2FS_Gaussian_UncertMean(domain, [0.75, 0.1, 0.1, 1.])

# All the three sets are plotted in the same figure with legends and the ouput is saved 
# to a file named multiSet.pdf.
IT2FS_plot(A, B, C, title="", legends=["Small","Medium","Large"], filename="multiSet")

# The meet of two sets A and B is calculated as the set AB, and plotted. 
# T-norm used in the meet operation is minimum T-norm.
AB = MEET(domain, min_t_norm, A, B, C)
AB.plot(filename="meet")

# The join of two sets B and C is calculated as the set BC, and plotted. 
# S-norm used in the join operation is maximum S-norm.
BC = JOIN(domain, max_s_norm, A, B, C)
BC.plot(filename="join")
