#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 16:14:58 2021

@author: arslan
"""

from numpy import (array, random, linspace, zeros, min, max, 
                   minimum, maximum, )
from pyit2fls import (T1FS, gaussian_mf, min_t_norm, max_s_norm, )

class T1FMatrix:
    
    def __init__(self, matrix, t1fs):
        self.matrix = matrix
        self.t1fmatrix = t1fs(matrix)
    
    def __array__(self):
        return self.t1fmatrix
    
    def __getitem__(self, item):
        return self.t1fmatrix.__getitem__(item)
    
    @property
    def shape(self):
        return self.t1fmatrix.shape
    
    def __repr__(self):
        return repr(self.t1fmatrix)
    
    def __str__(self):
        return str(self.t1fmatrix)
    

def T1FMatrix_Intersection(m1, m2, t_norm):
    return t_norm(m1, m2)

def T1FMatrix_Union(m1, m2, s_norm):
    return s_norm(m1, m2)

def T1FMatrix_Minmax(m1, m2):
    m, n = m1.shape
    r, q = m2.shape
    if r != n:
        raise TypeError("Matrices are inconsistent.")
    o = zeros(shape=(m, q))
    for i in range(m):
        for j in range(q):
            o[i, j] = min(maximum(m1[i, :], m2[:, j]))
    return o

def T1FMatrix_Maxmin(m1, m2):
    m, n = m1.shape
    r, q = m2.shape
    if r != n:
        raise TypeError("Matrices are inconsistent.")
    o = zeros(shape=(m, q))
    for i in range(m):
        for j in range(q):
            o[i, j] = max(minimum(m1[i, :], m2[:, j]))
    return o


class T1FSoftMatrix:
    
    def __init__(self):
        pass
    
    def __array__(self):
        return
    
    def __repr__(self):
        return
    
    def __str__(self):
        return


if __name__ == "__main__":
    matrix = random.rand(3, 3)
    domain = linspace(0., 1., 101)
    A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    B = T1FS(domain, mf=gaussian_mf, params=[0.4, 0.2, 1.])
    t1fmatrix1 = T1FMatrix(matrix, A)
    t1fmatrix2 = T1FMatrix(matrix, B)
    print("Matrix 1:\n", t1fmatrix1)
    print("Matrix 2:\n", t1fmatrix2)
    print("Intersection of matrices:\n", T1FMatrix_Intersection(t1fmatrix1, t1fmatrix2, min_t_norm))
    print("Union of matrices:\n", T1FMatrix_Union(t1fmatrix1, t1fmatrix2, max_s_norm))
    print("Minimum-Maximum of matrices:\n", T1FMatrix_Minmax(t1fmatrix1, t1fmatrix2))
    print("Maximum-Minimum of matrices:\n", T1FMatrix_Maxmin(t1fmatrix1, t1fmatrix2))




