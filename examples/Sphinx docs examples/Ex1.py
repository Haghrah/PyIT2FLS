#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:40:26 2024

@author: arslan
"""


from pyit2fls import (T1FS, trapezoid_mf, T1FS_plot, )
from numpy import linspace

domain = linspace(-1.5, 1.5, 100)
set1 = T1FS(domain, trapezoid_mf, [-1.25, -0.75, -0.25, 0.25, 1.])
set2 = T1FS(domain, trapezoid_mf, [-0.25, 0.25, 0.75, 1.25, 1.])
T1FS_plot(set1, set2, legends=["Trapezoidal Set 1", "Trapezoidal Set 2", ])

from pyit2fls import (min_t_norm, product_t_norm, T1FS_AND, )

set3 = T1FS_AND(domain, set1, set2, min_t_norm)
set4 = T1FS_AND(domain, set1, set2, product_t_norm)
T1FS_plot(set3, set4, legends=["Fuzzy Set 3", "Fuzzy Set 4", ])

from pyit2fls import (max_s_norm, probabilistic_sum_s_norm, T1FS_OR, )

set5 = T1FS_OR(domain, set1, set2, max_s_norm)
set6 = T1FS_OR(domain, set1, set2, probabilistic_sum_s_norm)
T1FS_plot(set5, set6, legends=["Fuzzy Set 5", "Fuzzy Set 6", ])

































