#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:09:12 2020

@author: arslan
"""

from pyit2fls import IT2FS, tri_mf, const_mf, rtri_mf, ltri_mf, \
    trapezoid_mf, gaussian_mf, IT2FS_Gaussian_UncertMean, \
    IT2FS_Gaussian_UncertStd, R_IT2FS_Gaussian_UncertStd, \
    L_IT2FS_Gaussian_UncertStd, IT2FS_plot
from numpy import linspace

domain = linspace(0, 1, 1001)

Const = IT2FS(domain, const_mf, [0.6], const_mf, [0.4], check_set=True)

Tri = IT2FS(domain, tri_mf, [0.1, 0.5, 0.9, 1], tri_mf, [0.3, 0.5, 0.7, 0.7], check_set=True)

RTri = IT2FS(domain, rtri_mf, [0.85, 0.2, 1], rtri_mf, [0.75, 0.1, 1.], check_set=True)

LTri = IT2FS(domain, ltri_mf, [0.15, 0.8, 1], ltri_mf, [0.25, 0.9, 1.], check_set=True)

IT2FS_plot(Const, Tri, 
           legends = ["Const Set", 
                      "Triangular Set"])
IT2FS_plot(RTri, LTri, 
           legends = ["Right Triangular Set", 
                      "Left Triangular Set"])

Trapezoid = IT2FS(domain, 
                  trapezoid_mf, [0.1, 0.35, 0.65, 0.9, 1.0], 
                  trapezoid_mf, [0.2, 0.4, 0.6, 0.8, 0.8], 
                  check_set=True)

Trapezoid.plot(legends="Trapezoid IT2FS")

Gaussian = IT2FS(domain, 
                 gaussian_mf, [0.5, 0.1, 1.0], 
                 gaussian_mf, [0.5, 0.05, 0.8], 
                 check_set=True)

Gaussian.plot(legends="Gaussian IT2FS")

Gaussian_UncertMean = IT2FS_Gaussian_UncertMean(domain, [0.5, 0.1, 0.1, 1.])
Gaussian_UncertMean.plot(legends="Gaussian IT2FS with Uncertain Mean")

Gaussian_UncertStd = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.1, 0.05, 0.75])
Gaussian_UncertStd.plot(legends="Gaussian IT2FS with Uncertain Std")

RGaussian_UncertStd = R_IT2FS_Gaussian_UncertStd(domain, [0.5, 0.1, 0.05, 0.8])
RGaussian_UncertStd.plot(legends="Right Gaussian IT2FS with Uncertain Std")

LGaussian_UncertStd = L_IT2FS_Gaussian_UncertStd(domain, [0.5, 0.1, 0.05, 0.8])
LGaussian_UncertStd.plot(legends="Left Gaussian IT2FS with Uncertain Std")









