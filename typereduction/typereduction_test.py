#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 00:29:35 2021

@author: arslan
"""

from numpy import array
import typereduction
from pyit2fls import EIASC_algorithm

intervals = array([[1., 2., 0., 0.], 
                   [1., 2., 0., 0.], 
                   [1., 2., 0., 0.], 
                   [1., 2., 0., 0.], 
                   [1., 2., 3., 4.], 
                   [2., 3., 4., 5.], 
                   [3., 4., 5., 6.], 
                   [4., 5., 6., 7.], 
                   [1., 2., 0., 0.], 
                   [1., 2., 0., 0.], 
                   [1., 2., 0., 0.], 
                   [0., 2., 10., 10.], ])

print(typereduction.EIASC_algorithm(intervals))
print(EIASC_algorithm(intervals))
