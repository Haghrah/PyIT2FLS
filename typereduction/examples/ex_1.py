#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 00:29:35 2021

@author: arslan
"""

from numpy import random, column_stack
import typereduction
from pyit2fls import EIASC_algorithm, KM_algorithm, EKM_algorithm, WM_algorithm
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

N = 1001
M = 100
x = random.rand(N)
fl = random.rand(N)
fh = fl + random.rand(N)
intervals = column_stack((x, x, fl, fh))



t_ = 0
for _ in range(M):
    t = time()
    EIASC_algorithm(intervals)
    t_ += time() - t

print("EIASC python implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    eiasc = typereduction.EIASC_algorithm(intervals)
    t_ += time() - t

print("EIASC C implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    KM_algorithm(intervals)
    t_ += time() - t

print("KM python implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    km = typereduction.KM_algorithm(intervals)
    t_ += time() - t

print("KM C implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    EKM_algorithm(intervals)
    t_ += time() - t

print("EKM python implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    ekm = typereduction.EKM_algorithm(intervals)
    t_ += time() - t

print("EKM C implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    WM_algorithm(intervals)
    t_ += time() - t

print("WM python implementation:", t_)

t_ = 0
for _ in range(M):
    t = time()
    wm = typereduction.WM_algorithm(intervals)
    t_ += time() - t

print("WM C implementation:", t_)


print("KM:", km)
print("EKM:", ekm)
print("EIASC:", eiasc)
print("WM:", wm)


