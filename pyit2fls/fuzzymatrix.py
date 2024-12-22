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
    """
    Creating a type 1 fuzzy matrix.
    
    .. rubric:: Parameters
    
    matrix : numpy (n, m, ) shaped array
        
        The input matrix.
    
    t1fs : T1FS 
        
        Type 1 fuzzy set describing the matrix elements.
    
    .. rubric:: Returns
    
    output : numpy (n, m, ) shaped array
        
        Returns membership degrees associated with the elements of the input matrix.
    
    .. rubric:: Examples
    
    >>> matrix = random.rand(3, 3)
    >>> domain = linspace(0., 1., 101)
    >>> A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    >>> t1fmatrix1 = T1FMatrix(matrix, A)
    """
    return t1fs(matrix)

def T1FMatrix_Complement(matrix):
    """
    Calculating complement of a type 1 fuzzy matrix.
    
    .. rubric:: Parameters
    
    matrix : numpy (n, m, ) shaped array
        
        The input matrix.
    
    .. rubric:: Returns
    
    output : numpy (n, m, ) shaped array
        
        Returns complement of the input matrix.
    
    .. rubric:: Examples
    
    >>> matrix = random.rand(3, 3)
    >>> domain = linspace(0., 1., 101)
    >>> A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    >>> t1fmatrix1 = T1FMatrix(matrix, A)
    >>> t1fmatrix2 = T1FMatrix_Complement(t1fmatrix1)
    """
    return 1 - matrix

def T1FMatrix_Intersection(m1, m2, t_norm):
    """
    Calculating intersection of two type 1 fuzzy matrices.
    
    .. rubric:: Parameters
    
    m1 : numpy (n, m, ) shaped array
        
        The first fuzzy matrix.
    
    m2 : numpy (n, m, ) shaped array
        
        The second fuzzy matrix.
    
    t_norm : function

        T-norm function for calculating the intersection.

    .. rubric:: Returns
    
    output : numpy (n, m, ) shaped array
        
        Returns intersection of the input matrices.
    
    .. rubric:: Examples
    
    >>> matrix = random.rand(3, 3)
    >>> domain = linspace(0., 1., 101)
    >>> A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    >>> B = T1FS(domain, mf=gaussian_mf, params=[0.4, 0.2, 1.])
    >>> t1fmatrix1 = T1FMatrix(matrix, A)
    >>> t1fmatrix2 = T1FMatrix(matrix, B)
    >>> t1fmatrix3 = T1FMatrix_Intersection(t1fmatrix1, t1fmatrix2, min_t_norm)
    """
    return t_norm(m1, m2)

def T1FMatrix_Union(m1, m2, s_norm):
    """
    Calculating union of two type 1 fuzzy matrices.
    
    .. rubric:: Parameters
    
    m1 : numpy (n, m, ) shaped array
        
        The first fuzzy matrix.
    
    m2 : numpy (n, m, ) shaped array
        
        The second fuzzy matrix.
    
    s_norm : function

        S-norm function for calculating the union.

    .. rubric:: Returns
    
    output : numpy (n, m, ) shaped array
        
        Returns union of the input matrices.
    
    .. rubric:: Examples
    
    >>> matrix = random.rand(3, 3)
    >>> domain = linspace(0., 1., 101)
    >>> A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    >>> B = T1FS(domain, mf=gaussian_mf, params=[0.4, 0.2, 1.])
    >>> t1fmatrix1 = T1FMatrix(matrix, A)
    >>> t1fmatrix2 = T1FMatrix(matrix, B)
    >>> t1fmatrix3 = T1FMatrix_Union(t1fmatrix1, t1fmatrix2, max_s_norm)
    """
    return s_norm(m1, m2)

def Minmax(m1, m2):
    """
    Calculating min-max of two type 1 fuzzy matrices.
    
    .. rubric:: Parameters
    
    m1 : numpy (n, m, ) shaped array
        
        The first fuzzy matrix.
    
    m2 : numpy (n, m, ) shaped array
        
        The second fuzzy matrix.
    
    .. rubric:: Returns
    
    output : numpy (n, m, ) shaped array
        
        Returns min-max of the input matrices.
    
    .. rubric:: Examples
    
    >>> matrix = random.rand(3, 3)
    >>> domain = linspace(0., 1., 101)
    >>> A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    >>> B = T1FS(domain, mf=gaussian_mf, params=[0.4, 0.2, 1.])
    >>> t1fmatrix1 = T1FMatrix(matrix, A)
    >>> t1fmatrix2 = T1FMatrix(matrix, B)
    >>> t1fmatrix3 = Minmax(t1fmatrix1, t1fmatrix2)
    """
    m, n = m1.shape
    r, q = m2.shape
    if r != n:
        raise ValueError("Matrices are inconsistent.")
    o = zeros(shape=(m, q))
    for i in range(m):
        for j in range(q):
            o[i, j] = min(maximum(m1[i, :], m2[:, j]))
    return o

def Maxmin(m1, m2):
    """
    Calculating max-min of two type 1 fuzzy matrices.
    
    .. rubric:: Parameters
    
    m1 : numpy (n, m, ) shaped array
        
        The first fuzzy matrix.
    
    m2 : numpy (n, m, ) shaped array
        
        The second fuzzy matrix.
    
    .. rubric:: Returns
    
    output : numpy (n, m, ) shaped array
        
        Returns max-min of the input matrices.
    
    .. rubric:: Examples
    
    >>> matrix = random.rand(3, 3)
    >>> domain = linspace(0., 1., 101)
    >>> A = T1FS(domain, mf=gaussian_mf, params=[0.6, 0.2, 1.])
    >>> B = T1FS(domain, mf=gaussian_mf, params=[0.4, 0.2, 1.])
    >>> t1fmatrix1 = T1FMatrix(matrix, A)
    >>> t1fmatrix2 = T1FMatrix(matrix, B)
    >>> t1fmatrix3 = Maxmin(t1fmatrix1, t1fmatrix2)
    """
    m, n = m1.shape
    r, q = m2.shape
    if r != n:
        raise ValueError("Matrices are inconsistent.")
    o = zeros(shape=(m, q))
    for i in range(m):
        for j in range(q):
            o[i, j] = max(minimum(m1[i, :], m2[:, j]))
    return o


def T1FMatrix_isNull(matrix):
    """
    Checks if all elements of the input matrix is zero.
    
    .. rubric:: Parameters
    
    matrix : numpy (n, m, ) shaped array
        
        The input fuzzy matrix.
    
    .. rubric:: Returns
    
    output : boolean
        
        Returns True if all elements are zero, else False.

    """
    return array_equal(matrix, 0.)

def T1FMatrix_isUniversal(matrix):
    """
    Checks if all elements of the input matrix is one.
    
    .. rubric:: Parameters
    
    matrix : numpy (n, m, ) shaped array
        
        The input fuzzy matrix.
    
    .. rubric:: Returns
    
    output : boolean
        
        Returns True if all elements are one, else False.

    """
    return array_equal(matrix, 1.)

def T1FSoftMatrix_Product(r, c, norm, *matrices):
    """
    Calculates soft matrix product.
    """
    if len(matrices) == 0:
        raise ValueError("At least one matrix is required.")
    o = matrices[0]
    for i in range(1,  len(matrices)):
        o = norm(o, matrices[i])
    return sum(o, axis=1) / len(matrices)


def T1FSoftMatrix(U, F):
    """
    Creates a soft matrix.
    """
    U = array(U)
    t1fsoftmatrix = []
    for f in F:
        t1fsoftmatrix.append(f(U))
    return vstack(t1fsoftmatrix)
    



