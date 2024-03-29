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
    
    def d0(self, d0x):
        s = 1.
        d = 0.
        n = 0.
        for l in range(self.M):
            s = 1.
            for i in range(self.N):
                s *= self.mf[l][i].d0(d0x[i], self.p[l][i][0], self.p[l][i][1])
            n += self.q[l] * s
            d += s
        return self.c * n / d
    
    def d1(self, d0x, d1x):
        s1 = 0.
        s2 = 0.
        s3 = 0.
        s4 = 0.
        
        for l in range(self.M):
            s5 = 1.
            for i in range(self.N):
                s5 *= self.mf[l][i].d0(d0x[i], self.p[l][i][0], self.p[l][i][1])
            s1 += self.q[l] * s5
            s2 += s5
        
        for j in range(self.N):
            s7 = 0.
            s8 = 0.
            for l in range(self.M):
                s6 = 1.
                for i in range(self.N):
                    if i != j:
                        s6 *= self.mf[l][i].d0(d0x[i], self.p[l][i][0], self.p[l][i][1])
                
                s7 += self.q[l] * self.mf[l][j].d1(d0x[j], self.p[l][j][0], self.p[l][j][1]) * s6
                s8 += self.mf[l][j].d1(d0x[j], self.p[l][j][0], self.p[l][j][1]) * s6
            
            s3 += d1x[j] * s7
            s4 += d1x[j] * s8
        
        return (s3 * s2 - s1 * s4) / s2 ** 2


class T1TSK_ML:

    def __init__(self, ):
        pass





