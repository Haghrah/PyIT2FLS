#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 20:19:08 2019

@author: arslan
"""

import matplotlib.pyplot as plt
from pyit2fls import (IT2FS_Gaussian_UncertStd, IT2Mamdani, 
                     min_t_norm, product_t_norm, max_s_norm, IT2FS_plot, )
from numpy import (linspace, array, where, abs, max, )
from scipy.integrate import (trapezoid, )
from ddeintlib import ddeint

# %%
def ITAE(a, b, t):
    return trapezoid(t * abs(a - b), t)

def os(y):
    return abs(max(y) - y[-1])

def ts(y, t):
    ss = y[-1]
    tol = 0.02 * ss
    yy = abs(y - ss)[::-1]
    return t[t.size - where(yy>tol)[0][0]]

# %%
def u(t):
    return 1. if t > 1. else 0.

def u_dot(t):
#    return 0
    a = 10
    return (a if 1. < t < (1. + 1./a) else 0)

# %% Interval Type 2 Fuzzy PID Codes ...
domain = linspace(-1., 1., 201)

N = IT2FS_Gaussian_UncertStd(domain, [-1., 0.5, 0.1, 1.])
Z = IT2FS_Gaussian_UncertStd(domain, [0., 0.2, 0.025, 1.])
P = IT2FS_Gaussian_UncertStd(domain, [1., 0.5, 0.1, 1.])
IT2FS_plot(N, Z, P, legends=["Negative", "Zero", "Positive"], filename="delay_pid_input_sets")

NB = IT2FS_Gaussian_UncertStd(domain, [-1., 0.1, 0.05, 1.])
NM = IT2FS_Gaussian_UncertStd(domain, [-0.5, 0.1, 0.05, 1.])
ZZ = IT2FS_Gaussian_UncertStd(domain, [0., 0.1, 0.05, 1.])
PM = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.1, 0.05, 1.])
PB = IT2FS_Gaussian_UncertStd(domain, [1., 0.1, 0.05, 1.])
IT2FS_plot(NB, NM, ZZ, PM, PB, legends=["Negative Big", "Negative Medium", 
                                       "Zero", "Positive Medium", 
                                       "Positive Big"], filename="delay_pid_output_sets")

def fuzzySystem(algorithm, algorithm_params=[]):
    it2fls = IT2Mamdani(min_t_norm, max_s_norm, method="Centroid", 
                        algorithm=algorithm, algorithm_params=algorithm_params)
    it2fls.add_input_variable("I1")  # E
    it2fls.add_input_variable("I2")  # dot E
    it2fls.add_output_variable("O")
    
    it2fls.add_rule([("I1", N), ("I2", N)], [("O", NB)])
    it2fls.add_rule([("I1", N), ("I2", Z)], [("O", NM)])
    it2fls.add_rule([("I1", N), ("I2", P)], [("O", ZZ)])
    it2fls.add_rule([("I1", Z), ("I2", N)], [("O", NM)])
    it2fls.add_rule([("I1", Z), ("I2", Z)], [("O", ZZ)])
    it2fls.add_rule([("I1", Z), ("I2", P)], [("O", NM)])
    it2fls.add_rule([("I1", P), ("I2", N)], [("O", ZZ)])
    it2fls.add_rule([("I1", P), ("I2", Z)], [("O", PM)])
    it2fls.add_rule([("I1", P), ("I2", P)], [("O", PB)])
    return it2fls

it2fpid_KM = fuzzySystem("KM")
it2fpid_EIASC = fuzzySystem("EIASC")
it2fpid_WM = fuzzySystem("WM")
it2fpid_BMM = fuzzySystem("BMM", algorithm_params=(0.5, 0.5))
it2fpid_NT = fuzzySystem("NT")

def eval_IT2FPID_KM(i1, i2):
    c, TR = it2fpid_KM.evaluate({"I1":i1, "I2":i2})
    o = TR["O"]
    return (o[0] + o[1]) / 2

def eval_IT2FPID_EIASC(i1, i2):
    c, TR = it2fpid_EIASC.evaluate({"I1":i1, "I2":i2})
    o = TR["O"]
    return (o[0] + o[1]) / 2

def eval_IT2FPID_WM(i1, i2):
    c, TR = it2fpid_WM.evaluate({"I1":i1, "I2":i2})
    o = TR["O"]
    return (o[0] + o[1]) / 2

def eval_IT2FPID_BMM(i1, i2):
    c, y = it2fpid_BMM.evaluate({"I1":i1, "I2":i2})
    return y["O"]

def eval_IT2FPID_NT(i1, i2):
    c, y = it2fpid_NT.evaluate({"I1":i1, "I2":i2})
    return y["O"]

# %% Overall system
def raw_sys(Y, t, K, T, L):
    return array([(-1. / T) * Y[0](t) + (K / T) * u(t - L)])

def cl_sys(Y, t, K, T, L):
    return array([(-1. / T) * Y[0](t) + (K / T) * (u(t - L) - Y[0](t - L))])

def model_fuzzy(Y, t, K, T, L, Ka, Kb, Ke, Kd, eval_func):
    epsilon = 0.001
    
    y2 = Y[1](t)
    
    e1 = u(t - L) - Y[0](t - L)
    de1 = u_dot(t - L) - Y[1](t - L)
    xd1 = eval_func(min(max(Ke * e1, -1), 1), min(max(Kd * de1, -1), 1))
    
    
    e2 = u(t - L - epsilon) - Y[0](t - L - epsilon)
    de2 = u_dot(t - L - epsilon) - Y[1](t - L - epsilon)
    xd2 = eval_func(min(max(Ke * e2, -1), 1), min(max(Kd * de2, -1), 1))
    
    
    
    dxd = (xd1 - xd2) / epsilon
    
    
    
    return array([y2, (-1./T) * y2 + (K * Ka / T) * dxd + (K * Kb / T) * xd1])

g1 = lambda t : 0
g2 = lambda t : 0

# %%
# Nominal
# K = 1.
# T = 1.
# L = 0.2

# Perturbed 1.
K = 1.3
T = 1.9
L = 0.4

#Perturbed 2.
#K = 1.1
#T = 1.3
#L = 0.45

tt = linspace(0., 20. ,2000)

y_raw = ddeint(raw_sys, [g1], tt, fargs=(K, T, L, ))
y_cl = ddeint(cl_sys, [g1], tt, fargs=(K, T, L, ))

print("KM evaluation start!")
y_it2fpid_KM = ddeint(model_fuzzy, [g1, g2], tt, 
                      fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, eval_IT2FPID_KM, ))

print("EIASC evaluation start!")
y_it2fpid_EIASC = ddeint(model_fuzzy, [g1, g2], tt, 
                         fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, eval_IT2FPID_EIASC, ))

print("WM evaluation start!")
y_it2fpid_WM = ddeint(model_fuzzy, [g1, g2], tt, 
                      fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, eval_IT2FPID_WM, ))

print("BMM evaluation start!")
y_it2fpid_BMM = ddeint(model_fuzzy, [g1, g2], tt, 
                       fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, eval_IT2FPID_BMM, ))

print("NT evaluation start!")
y_it2fpid_NT = ddeint(model_fuzzy, [g1, g2], tt, 
                      fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, eval_IT2FPID_NT, ))

ref = array([u(t) for t in tt])

plt.figure()
plt.plot(tt, ref, label="Reference")
plt.plot(tt, y_it2fpid_KM[:,0], label="KM", linewidth=1.)
plt.plot(tt, y_it2fpid_EIASC[:,0], label="EIASC", linewidth=1.)
plt.plot(tt, y_it2fpid_WM[:,0], label="WM", linewidth=1.)
plt.plot(tt, y_it2fpid_BMM[:,0], label="BMM", linewidth=1.)
plt.plot(tt, y_it2fpid_NT[:,0], label="NT", linewidth=1.)
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("System response")
plt.grid(True)
plt.savefig("delay_pid_case1_comp.pdf", format="pdf", dpi=300, bbox_inches="tight")
plt.show()



print("KM:")
print("ITAE:", ITAE(ref, y_it2fpid_KM[:,0], tt))
print("Overshoot:", 100 * os(y_it2fpid_KM[:,0]))
print("Settling time:", ts(y_it2fpid_KM[:,0], tt))

print("EIASC:")
print("ITAE:", ITAE(ref, y_it2fpid_EIASC[:,0], tt))
print("Overshoot:", 100 * os(y_it2fpid_EIASC[:,0]))
print("Settling time:", ts(y_it2fpid_EIASC[:,0], tt))

print("WM:")
print("ITAE:", ITAE(ref, y_it2fpid_WM[:,0], tt))
print("Overshoot:", 100 * os(y_it2fpid_WM[:,0]))
print("Settling time:", ts(y_it2fpid_WM[:,0], tt))

print("BMM:")
print("ITAE:", ITAE(ref, y_it2fpid_BMM[:,0], tt))
print("Overshoot:", 100 * os(y_it2fpid_BMM[:,0]))
print("Settling time:", ts(y_it2fpid_BMM[:,0], tt))

print("NT:")
print("ITAE:", ITAE(ref, y_it2fpid_NT[:,0], tt))
print("Overshoot:", 100 * os(y_it2fpid_NT[:,0]))
print("Settling time:", ts(y_it2fpid_NT[:,0], tt))
