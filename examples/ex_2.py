#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:56:00 2019

@author: arslan
"""

from pyit2fls import IT2FS_Gaussian_UncertMean, IT2FS_plot, meet, \
                     join, min_t_norm, max_s_norm
from numpy import linspace


# Defining three interval type 2 fuzzy sets for testing the meet and join 
# functions.

# Domain is defined as discrete space in the interval [0, 1] divided to 100 parts.
domain = linspace(0., 1., 100)

# The first IT2FLS is defined as a Gaussian set with uncertain mean value.
# The mean center = 0.25, 
# the mean spread = 0.1, 
# the standard deviation = 0.1, and 
# the height = 1.
A = IT2FS_Gaussian_UncertMean(domain, [0.25, 0.1, 0.1, 1.])

# The second IT2FLS is defined as a Gaussian set with uncertain mean value.
# The mean center = 0.5, 
# the mean spread = 0.1, 
# the standard deviation = 0.1, and 
# the height = 1.
B = IT2FS_Gaussian_UncertMean(domain, [0.5, 0.1, 0.1, 1.])

# The third IT2FLS is defined as a Gaussian set with uncertain mean value.
# The mean center = 0.75, 
# the mean spread = 0.1, 
# the standard deviation = 0.1, and 
# the height = 1.
C = IT2FS_Gaussian_UncertMean(domain, [0.75, 0.1, 0.1, 1.])

# All the three sets are plotted in same figure with legends and the ouput is saved 
# to a file.
IT2FS_plot(A, B, C, title="", legends=["Small","Medium","Large"], filename="multiSet")

# The meet of two sets A and B is calculated as the set AB, and plotted. 
# The T-norm used in meet operation is minimum T-norm.
AB = meet(domain, A, B, min_t_norm)
AB.plot(filename="meet")

# The join of two sets B and C is calculated as the set BC, and plotted. 
# The S-norm used in join operation is maximum S-norm.
BC = join(domain, B, C, max_s_norm)
BC.plot(filename="join")
