#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 00:29:35 2021

@author: arslan
"""

import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_int, c_double

# input type for the cos_doubles function
# must be a double array, with single dimension that is contiguous
array_2d_double = npct.ndpointer(dtype=np.double, ndim=2, flags='CONTIGUOUS')
array_1d_double = npct.ndpointer(dtype=np.double, ndim=1, flags='CONTIGUOUS')

# load the library, using numpy mechanisms
libcd = npct.load_library("libtypereduction", ".")

# setup the return types and argument types
libcd.EIASC_Algorithm.restype = c_double
libcd.EIASC_Algorithm.argtypes = [array_2d_double, array_1d_double, c_int, array_1d_double]


def EIASC_Algorithm(intervals, params=np.array([])):
    o = np.zeros(shape=(3, ))
    libcd.EIASC_Algorithm(intervals, params, len(intervals), o)
    return o




