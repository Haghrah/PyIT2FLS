#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:11:43 2024

@author: arslan
"""

from pyit2fls import (T1FS, trapezoid_mf, T1FS_plot, 
                      min_t_norm, product_t_norm, T1FS_AND, 
                      max_s_norm, probabilistic_sum_s_norm, T1FS_OR, 
                      IT2FS_RGaussian_UncertStd, 
                      IT2FS_LGaussian_UncertStd, IT2FS_plot, 
                      MEET, JOIN)
from numpy import (linspace, )
import matplotlib.pyplot as plt

domain = linspace(-1.0, 1.0, 2001)
set1 = T1FS(domain, trapezoid_mf, [-0.75, -0.25, 0.25, 0.75, 1.])
set2 = -set1

T1FS_plot(set1, set2, legends=["[T1FS1]", "[NOT T1FS1]", ], filename="../images/figure1_1")

set3 = T1FS_AND(domain, set1, set2, min_t_norm)
set4 = T1FS_AND(domain, set1, set2, product_t_norm)
T1FS_plot(set3, set4, legends=["[T1FS1] AND [NOT T1FS1] (minimum t-norm)", 
                               "[T1FS1] AND [NOT T1FS1] (product t-norm)", ], 
          filename="../images/figure1_2")

set5 = T1FS_OR(domain, set1, set2, max_s_norm)
set6 = T1FS_OR(domain, set1, set2, probabilistic_sum_s_norm)
T1FS_plot(set5, set6, legends=["[T1FS1] OR [NOT T1FS1] (maximum s-norm)", 
                               "[T1FS1] OR [NOT T1FS1] (probabilistic sum s-norm)", ], 
          filename="../images/figure1_3")


domain = linspace(1, 2, 1001)

it2fs1 = IT2FS_RGaussian_UncertStd(domain, [1.25, 0.2, 0.05, 0.6])
it2fs2 = IT2FS_LGaussian_UncertStd(domain, [1.75, 0.2, 0.05, 0.6])
it2fs3 = -it2fs1
it2fs4 = -it2fs2

it2fs5 = MEET(domain, min_t_norm, it2fs1, it2fs2, it2fs3, it2fs4)
it2fs6 = JOIN(domain, max_s_norm, it2fs1, it2fs2, it2fs3, it2fs4)

IT2FS_plot(it2fs1, it2fs2, it2fs3, it2fs4,  
           legends=["[IT2FS1]", 
                    "[IT2FS2]", 
                    "[NOT IT2FS1]", 
                    "[NOT IT2FS2]", ], 
           legendloc="upper right", 
           filename="../images/figure3_1", ext="pdf")
plt.tight_layout()


IT2FS_plot(it2fs5, it2fs6, 
           legends=["MEET of the all four sets", 
                    "JOIN of the all four sets", ], 
           filename="../images/figure3_2", ext="pdf")


















