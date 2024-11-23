#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:11:43 2024

@author: arslan
"""

from pyit2fls import (IT2FS, tri_mf, const_mf, rtri_mf, ltri_mf, 
                      trapezoid_mf, gaussian_mf, IT2FS_Gaussian_UncertMean, 
                      IT2FS_Gaussian_UncertStd, R_IT2FS_Gaussian_UncertStd, 
                      L_IT2FS_Gaussian_UncertStd, IT2FS_plot, )
from numpy import linspace

domain = linspace(0, 4, 1001)

Const = IT2FS(domain, const_mf, [1.0], const_mf, [0.9], check_set=True)
Tri = IT2FS(domain, tri_mf, [0.7, 1.0, 1.3, 0.3], tri_mf, [0.8, 1.0, 1.2, 0.2], check_set=True)
RTri = IT2FS(domain, rtri_mf, [1.85, 1.25, 0.8], rtri_mf, [1.75, 1.15, 0.8], check_set=True)
LTri = IT2FS(domain, ltri_mf, [0.15, 0.75, 0.7], ltri_mf, [0.25, 0.85, 0.7], check_set=True)
Trapezoid = IT2FS(domain, 
                  trapezoid_mf, [0.45, 0.85, 1.15, 1.55, 0.5], 
                  trapezoid_mf, [0.55, 0.95, 1.05, 1.45, 0.45], 
                  check_set=True)
Gaussian = IT2FS(domain, 
                  gaussian_mf, [2.25, 0.1, 0.5], 
                  gaussian_mf, [2.25, 0.05, 0.4], 
                  check_set=True)
Gaussian_UncertMean = IT2FS_Gaussian_UncertMean(domain, [2.5, 0.1, 0.1, 0.5])
Gaussian_UncertStd = IT2FS_Gaussian_UncertStd(domain, [2.75, 0.1, 0.05, 0.5])
RGaussian_UncertStd = R_IT2FS_Gaussian_UncertStd(domain, [3.25, 0.2, 0.05, 0.6])
LGaussian_UncertStd = L_IT2FS_Gaussian_UncertStd(domain, [3.75, 0.2, 0.05, 0.6])

IT2FS_plot(Const, Tri, RTri, LTri, Trapezoid, Gaussian,
           Gaussian_UncertMean, Gaussian_UncertStd, 
           RGaussian_UncertStd, LGaussian_UncertStd, 
           legends = ["Const Set", 
                      "Triangular Set", 
                      "Right Triangular Set", 
                      "Left Triangular Set", 
                      "Trapezoid", 
                      "Gaussian", 
                      "G. with Uncertain Mean", 
                      "G. with Uncertain Std", 
                      "Right G. with Uncertain Std", 
                      "Left G. with Uncertain Std", ])




