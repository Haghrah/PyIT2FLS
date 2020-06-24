#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:12:04 2019

@author: arslan
"""


from pyit2fls import IT2FS, trapezoid_mf, tri_mf
from numpy import linspace

# Defining an interval type 2 fuzzy set with trapezoidal UMF and triangular LMF
domain = linspace(0., 1., 100)  # Domain is defined as discrete space in the
                                # interval [0, 1] divided to 100 parts.
mySet = IT2FS(domain, 
              trapezoid_mf, [0, 0.4, 0.6, 1., 1.],  # Trapezoidal UMF with 
                                                    # left = 0.,
                                                    # center left = 0.4,
                                                    # center right = 0.6, 
                                                    # right = 1., 
                                                    # and height = 1.
              tri_mf, [0.25, 0.5, 0.75, 0.6])       # Triangular LMF with 
                                                    # left = 0.25,
                                                    # center = 0.5,
                                                    # right = 0.75,
                                                    # and height = 0.6.
mySet.plot(filename="mySet")  # Plotting the set and saving to the file, 
                              # named mySet.

