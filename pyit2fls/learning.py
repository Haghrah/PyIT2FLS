#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 01:39:58 2024

@author: arslan
"""

from numpy import (reshape, exp, array, zeros_like, asarray, )
from numpy.linalg import (norm, )
from numpy.random import (rand, )
from scipy.optimize import (differential_evolution, minimize, )

class gaussian_mf_learning:

    def d0(self, x, c, v):
        return exp(- ((x - c) / v) ** 2)

    def d1(self, x, c, v):
        return - 2 * ((x - c) / v ** 2) * exp(- ((x - c) / v) ** 2)


class T1TSK_ML_Model:
    """
    TSKN: Number of inputs
    TSKM: Number of rules
    P: Model parameters (a vector of size TSKM * (2 * TSKN + 1))
    mf: List of membership functions for each input in each rule
    c: Output scaling factor
    """
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

    def __init__(self, TSKN, TSKM, Bounds=None, algorithm="DE"):
        self.TSKN = TSKN
        self.TSKM = TSKM
        self.algorithm = algorithm
        self.paramNum = TSKM * (2 * TSKN + 1)
        self.params = rand(self.paramNum, )
        self.Bounds = [Bounds, ] * self.paramNum
        self.mf = gaussian_mf_learning()
        self.model = T1TSK_ML_Model(self.params, self.TSKN, self.TSKM, 
                                    [[self.mf, ] * self.TSKN, ] * self.TSKM)

    def error(self, P, X, y):
        model = T1TSK_ML_Model(P, self.TSKN, self.TSKM, 
                               [[self.mf, ] * self.TSKN, ] * self.TSKM)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model.d0(x)
        return norm(y - o)

    def fit(self, X, y):
        if self.algorithm == "DE":
            result = differential_evolution(self.error, bounds=self.Bounds, 
                                            args=(X, y), disp=True)
        elif self.algorithm == "Nelder-Mead":
            result = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, })
        elif self.algorithm == "Powell":
            result = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, })
        elif self.algorithm == "CG":
            result = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, 
                              options={"disp":True, })
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        self.params = result.x
        self.model = T1TSK_ML_Model(self.params, self.TSKN, self.TSKM, 
                                    [[self.mf, ] * self.TSKN, ] * self.TSKM)
        return self.error(self.params, X, y)

    def score(self, X):
        X = asarray(X)
        if X.ndim == 1:
            return self.model.d0(X)
        elif X.ndim == 2:
            o = []
            for x in X:
                o.append(self.model.d0(x))
            return array(o)
        else:
            raise ValueError("Input must be a 1D or 2D NumPy array!")













