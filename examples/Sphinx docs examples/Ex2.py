#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:43:11 2024

@author: arslan
"""

from pyit2fls import (T1TSK, T1FS, trapezoid_mf, T1FS_plot, )
from numpy import linspace

domain = linspace(-1.5, 1.5, 100)
set1 = T1FS(domain, trapezoid_mf, [-1.25, -0.75, -0.25, 0.25, 1.])
set2 = T1FS(domain, trapezoid_mf, [-0.25, 0.25, 0.75, 1.25, 1.])
T1FS_plot(set1, set2, legends=["Trapezoidal Set 1", "Trapezoidal Set 2", ])

myT1TSK = T1TSK()
myT1TSK.add_input_variable("X1")
myT1TSK.add_input_variable("X2")

myT1TSK.add_output_variable("Y1")
myT1TSK.add_output_variable("Y2")











