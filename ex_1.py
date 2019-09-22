#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:12:04 2019

@author: arslan
"""

from pyit2fls import IT2FS, trapezoid_mf, tri_mf
from numpy import linspace

mySet = IT2FS(linspace(0., 1., 100), 
              trapezoid_mf, [0, 0.4, 0.6, 1., 1.], 
              tri_mf, [0.25, 0.5, 0.75, 0.6])
mySet.plot(filename="mySet")


