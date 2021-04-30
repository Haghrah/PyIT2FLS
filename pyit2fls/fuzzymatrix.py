#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 16:14:58 2021

@author: arslan
"""

from numpy import (array, zeros, min, max, sum, 
                   minimum, maximum, vstack, 
                   array_equal, )

def T1FMatrix(matrix, t1fs):
    return t1fs(matrix)

def T1FMatrix_Complement(matrix):
    return 1 - matrix

def T1FMatrix_Intersection(m1, m2, t_norm):
    return t_norm(m1, m2)

def T1FMatrix_Union(m1, m2, s_norm):
    return s_norm(m1, m2)

def Minmax(m1, m2):
    m, n = m1.shape
    r, q = m2.shape
    if r != n:
        raise TypeError("Matrices are inconsistent.")
    o = zeros(shape=(m, q))
    for i in range(m):
        for j in range(q):
            o[i, j] = min(maximum(m1[i, :], m2[:, j]))
    return o

def Maxmin(m1, m2):
    m, n = m1.shape
    r, q = m2.shape
    if r != n:
        raise TypeError("Matrices are inconsistent.")
    o = zeros(shape=(m, q))
    for i in range(m):
        for j in range(q):
            o[i, j] = max(minimum(m1[i, :], m2[:, j]))
    return o


def T1FMatrix_isNull(matrix):
    return array_equal(matrix, 0.)

def T1FMatrix_isUniversal(matrix):
    return array_equal(matrix, 1.)

def T1FSoftMatrix_Product(r, c, norm, *matrices):
    if len(matrices) == 0:
        raise ValueError("At least one matrix is required.")
    o = matrices[0]
    for i in range(1,  len(matrices)):
        o = norm(o, matrices[i])
    return sum(o, axis=1) / len(matrices)


def T1FSoftMatrix(U, F):
    U = array(U)
    t1fsoftmatrix = []
    for f in F:
        t1fsoftmatrix.append(f(U))
    return vstack(t1fsoftmatrix)
    



