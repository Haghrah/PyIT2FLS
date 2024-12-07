#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 02:51:58 2021

@author: arslan
"""
from numpy import (array, random, linspace, )
from pyit2fls import (T1FS, gaussian_mf, min_t_norm, max_s_norm, 
                      product_t_norm, T1FMatrix, T1FMatrix_Intersection, 
                      T1FMatrix_Union, Minmax, Maxmin, T1FSoftMatrix, 
                      T1FMatrix_Complement, T1FSoftMatrix_Product)

matrix = random.rand(3, 3)
domain = linspace(0., 1., 101)
A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
B = T1FS(domain, mf=gaussian_mf, params=[0.4, 0.2, 1.])
t1fmatrix1 = T1FMatrix(matrix, A)
t1fmatrix2 = T1FMatrix(matrix, B)
print("Matrix 1:\n", t1fmatrix1)
print("Matrix 2:\n", t1fmatrix2)
print("-------------------")
print("Intersection of matrices:\n", T1FMatrix_Intersection(t1fmatrix1, t1fmatrix2, min_t_norm))
print("Union of matrices:\n", T1FMatrix_Union(t1fmatrix1, t1fmatrix2, max_s_norm))
print("-------------------")
print("Minimum-Maximum of matrices:\n", Minmax(t1fmatrix1, t1fmatrix2))
print("Maximum-Minimum of matrices:\n", Maxmin(t1fmatrix1, t1fmatrix2))
print("-------------------")

t1fsoftmatrix = T1FSoftMatrix([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 
                              [A, B])
print(t1fsoftmatrix)
print(T1FMatrix_Complement(t1fsoftmatrix))
print("-------------------")

A1 = array([[0.3, 0.2, 0.1], 
            [0.5, 0.4, 0.2], 
            [0.6, 0.5, 0.7], 
            [0.4, 0.6, 0.8], 
            [0.8, 0.6, 0.3]])
A2 = array([[0.7, 0.2, 0.5], 
            [0.6, 0.4, 0.9], 
            [0.7, 0.8, 0.6], 
            [0.5, 0.6, 1.0], 
            [0.4, 0.5, 0.7]])
A3 = array([[0.5, 0.4, 0.6], 
            [0.4, 0.7, 0.6], 
            [0.6, 0.5, 0.5], 
            [0.8, 0.6, 0.4], 
            [0.5, 0.6, 0.5]])
print(T1FSoftMatrix_Product(5, 3, product_t_norm, A1, A2, A3))
print("-------------------")












