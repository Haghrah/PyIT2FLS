#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 01:39:58 2024

@author: arslan
"""

from numpy import (reshape, )
from .pyit2fls import (gaussian_mf, )


class T1TSK_ML_Model:

    def __init__(self, P, TSKN, TSKM, mf, c=1.0):
        self.p = reshape(P[:-TSKM], (TSKM, TSKN, 2, ))
        self.q = P[-TSKM:]
        self.N = TSKN
        self.M = TSKM
        self.mf = mf
        self.c = c


class T1TSK_ML:

    def __init__(self, ):
        pass





