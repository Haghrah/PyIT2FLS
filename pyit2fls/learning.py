#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 01:39:58 2024

@author: arslan
"""

from numpy import (reshape, exp, array, zeros, zeros_like, asarray, )
from numpy.linalg import (norm, )
from numpy.random import (rand, )
from scipy.optimize import (differential_evolution, minimize, )


class PSO:
    
    def __init__(self, N, M, func, bounds, args=()):
        self.func = func
        self.args = args
        self.N  = N
        self.M  = M
        self.bounds = bounds
        self.X  = self.bounds[0] + (self.bounds[1] - self.bounds[0]) * rand(self.N, self.M)
        self.V  = 4.0 * (self.bounds[1] - self.bounds[0]) * (rand(self.N, self.M) - 0.5)
        self.Xb = self.X.copy()
        self.Fb = zeros(shape=(self.N, ))
        
        self.Fb[0] = self.func(self.X[0, :], *self.args)
        
        self.xb = self.X[0, :].copy()
        self.fb = self.Fb[0]
        
        self.iterNum = 0
        
        for i in range(1, self.N):
            self.Fb[i] = self.func(self.X[i, :], *self.args)
                
            if self.Fb[i] < self.fb:
                self.fb = self.Fb[i]
                self.xb = self.X[i, :].copy()
        
        # self.saveData()
                
    
    def saveData(self):
        dataFile = open(str(self.iterNum) + ".txt", "w")
        for i in range(self.N):
            for j in range(self.M):
                dataFile.write(str(self.X[i, j]) + "\n")
            
            for j in range(self.M):
                dataFile.write(str(self.V[i, j]) + "\n")
            
            for j in range(self.M):
                dataFile.write(str(self.Xb[i, j]) + "\n")
            
            dataFile.write(str(self.Fb[i]) + "\n")
        
        for j in range(self.M):
            dataFile.write(str(self.xb[j]) + "\n")
        
        dataFile.write(str(self.fb) + "\n")
        
        dataFile.close()
    
    
    def iterate(self, omega=0.3, phi_p=0.3, phi_g=2.1):
        self.iterNum += 1
        r_p = rand(self.N, self.M)
        r_g = rand(self.N, self.M)
        self.V = omega * self.V + \
                 phi_p * r_p * (self.Xb - self.X) + \
                 phi_g * r_g * (self.xb - self.X)
        self.X = self.X + self.V
        
        for i in range(self.N):
            tmp = self.func(self.X[i, :], *self.args)
                
            if tmp < self.Fb[i]:
                self.Xb[i, :] = self.X[i, :].copy()
                self.Fb[i] = tmp
                if tmp < self.fb:
                    self.xb = self.X[i, :].copy()
                    self.fb = tmp
        
        # self.saveData()


class gaussian_mf_learning:

    def d0(self, x, c, v):
        return exp(- ((x - c) / v) ** 2)

    def d1(self, x, c, v):
        return - 2 * ((x - c) / v ** 2) * exp(- ((x - c) / v) ** 2)


class T1Mamdani_ML_Model:
    """
    P: Number of inputs
    U: Universe of discourse of inputs as a list of 
       tuples demonstrating lowest and highest possible 
       values of each variable.
    N: Number of sets describing each input
    L: Number of rules
    M: Number of sets describing the output
    V: Universe of discourse of output as a tuple
       demonstrating the lowest and highest possible 
       values of the output variable.
    """
    def __init__(self, Params, P, U, N, L, M, V, mf):
        self.Params = Params
        self.P = P
        self.U = U
        self.N = N
        self.L = L
        self.M = M
        self.V = V
        self.mf = mf

    def d0(self, ):
        pass

    def d1(self, ):
        pass


class T1Mamdani_ML:
    """
    """
    def __init__(self, ):
        pass

    def error(self, ):
        return 0.
    
    def fit(self, ):
        pass

    def score(self, ):
        pass



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

    def __init__(self, TSKN, TSKM, Bounds=None, algorithm="DE", algorithm_params=[]):
        self.TSKN = TSKN
        self.TSKM = TSKM
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params
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
            self.params = differential_evolution(self.error, bounds=self.Bounds, 
                                            args=(X, y), disp=True).x
        elif self.algorithm == "Nelder-Mead":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "Powell":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "CG":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, 
                              options={"disp":True, }).x
        elif self.algorithm == "PSO":
            myPSO = PSO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4])
                print("Iteration ", i+1, ".", myPSO.fb)
            self.params = myPSO.xb
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
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













