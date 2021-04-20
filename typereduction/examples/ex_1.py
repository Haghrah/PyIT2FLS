#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 00:29:35 2021

@author: arslan
"""

from numpy import array, random, column_stack, row_stack
from numpy import sum as npsum
import typereduction
from pyit2fls import EIASC_algorithm, KM_algorithm
from time import time

# intervals = array([[0.1, 0.3, 0., 0.], 
#                    [0.2, 0.4, 0., 0.], 
#                    [0.3, 0.5, 0., 0.], 
#                    [0.4, 0.6, 0., 0.], 
#                    [0.5, 0.7, 3., 4.], 
#                    [0.6, 0.8, 4., 5.], 
#                    [0.7, 0.9, 5., 6.], 
#                    [0.8, 1.0, 6., 7.], 
#                    [0.9, 1.1, 0., 0.], 
#                    [1.0, 1.2, 0., 0.], 
#                    [1.1, 1.3, 0., 0.], 
#                    [0.0, 1.4, 10., 10.], ])

x = random.rand(101)
fl = random.rand(101)
fh = fl + random.rand(101)
intervals = column_stack((x, x, fl, fh))

t1 = 0
for _ in range(10000):
    t = time()
    EIASC_algorithm(intervals)
    t1 += time() - t

print(t1)

t2 = 0
for _ in range(10000):
    t = time()
    KM_algorithm(intervals)
    t2 += time() - t

print(t2)

t3 = 0
for _ in range(10000):
    t = time()
    typereduction.EIASC_algorithm(intervals)
    t3 += time() - t

print(t3)













