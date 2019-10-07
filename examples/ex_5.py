#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 20:19:08 2019

@author: arslan
"""

from matplotlib.pyplot import figure, plot, legend, grid, show, xlabel, \
                              ylabel, savefig
from pyit2fls import IT2FS_Gaussian_UncertStd, IT2FLS, \
                     min_t_norm, product_t_norm, max_s_norm, IT2FS_plot
from numpy import linspace, array, trapz, where
from numpy import abs as npabs
from numpy import max as npmax
from ddeint import ddeint

# %%
def ITAE(a, b, t):
    return trapz(t * npabs(a - b), t)

def os(y):
    return npabs(npmax(y) - y[-1])

def ts(y, t):
    ss = y[-1]
    tol = 0.02 * ss
    yy = npabs(y - ss)[::-1]
    return t[t.size - where(yy>tol)[0][0]]

# %%

def u(t):
    return 1. if t > 1. else 0.

def u_dot(t):
#    return 0
    a = 100
    return (a if 1. < t < (1. + 1./a) else 0)

# %% Interval Type 2 Fuzzy PID Codes ...
domain = linspace(-1., 1., 201)

N = IT2FS_Gaussian_UncertStd(domain, [-1., 0.5, 0.1])
Z = IT2FS_Gaussian_UncertStd(domain, [0., 0.2, 0.025])
P = IT2FS_Gaussian_UncertStd(domain, [1., 0.5, 0.1])
IT2FS_plot(N, Z, P, legends=["Negative", "Zero", "Positive"], filename="delay_pid_input_sets")

NB = IT2FS_Gaussian_UncertStd(domain, [-1., 0.1, 0.05])
NM = IT2FS_Gaussian_UncertStd(domain, [-0.5, 0.1, 0.05])
Z = IT2FS_Gaussian_UncertStd(domain, [0., 0.1, 0.05])
PM = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.1, 0.05])
PB = IT2FS_Gaussian_UncertStd(domain, [1., 0.1, 0.05])
IT2FS_plot(NB, NM, Z, PM, PB, legends=["Negative Big", "Negative Medium", 
                                       "Zero", "Positive Medium", 
                                       "Positive Big"], filename="delay_pid_output_sets")

it2fls = IT2FLS()
it2fls.add_input_variable("I1")  # E
it2fls.add_input_variable("I2")  # dot E
it2fls.add_output_variable("O")

it2fls.add_rule([("I1", N), ("I2", N)], [("O", NB)])
it2fls.add_rule([("I1", N), ("I2", Z)], [("O", NM)])
it2fls.add_rule([("I1", N), ("I2", P)], [("O", Z)])
it2fls.add_rule([("I1", Z), ("I2", N)], [("O", NM)])
it2fls.add_rule([("I1", Z), ("I2", Z)], [("O", Z)])
it2fls.add_rule([("I1", Z), ("I2", P)], [("O", NM)])
it2fls.add_rule([("I1", P), ("I2", N)], [("O", Z)])
it2fls.add_rule([("I1", P), ("I2", Z)], [("O", PM)])
it2fls.add_rule([("I1", P), ("I2", P)], [("O", PB)])

def eval_IT2FPID_KM(i1, i2):
    c, TR = it2fls.evaluate({"I1":i1, "I2":i2},
                        min_t_norm, max_s_norm, domain, method="Centroid", 
                        algorithm="EKM")
    o = TR["O"]
    return (o[0] + o[1]) / 2

def eval_IT2FPID_EIASC(i1, i2):
    c, TR = it2fls.evaluate({"I1":i1, "I2":i2},
                        min_t_norm, max_s_norm, domain, method="Centroid", 
                        algorithm="EIASC")
    o = TR["O"]
    return (o[0] + o[1]) / 2

def eval_IT2FPID_WM(i1, i2):
    c, TR = it2fls.evaluate({"I1":i1, "I2":i2},
                        min_t_norm, max_s_norm, domain, method="Centroid", 
                        algorithm="WM")
    o = TR["O"]
    return (o[0] + o[1]) / 2

def eval_IT2FPID_BMM(i1, i2):
    c, y = it2fls.evaluate({"I1":i1, "I2":i2},
                        min_t_norm, max_s_norm, domain, method="Centroid", 
                        algorithm="BMM", algorithm_params=(0.5, 0.5))
    return y["O"]

def eval_IT2FPID_NT(i1, i2):
    c, y = it2fls.evaluate({"I1":i1, "I2":i2},
                        min_t_norm, max_s_norm, domain, method="Centroid", 
                        algorithm="NT")
    return y["O"]

# %% Overall system
def raw_sys(Y, t, K, T, L):
    return array([(-1. / T) * Y[0](t) + (K / T) * u(t - L)])

def cl_sys(Y, t, K, T, L):
    return array([(-1. / T) * Y[0](t) + (K / T) * (u(t - L) - Y[0](t - L))])

def model_KM(Y, t, K, T, L, Ka, Kb, Ke, Kd):
    y2 = Y[1](t)
    y1d = Y[0](t - L)
    y2d = Y[1](t - L)
    e1 = u(t - L) - y1d
    de1 = u_dot(t - L) - y2d
    xd1 = eval_IT2FPID_KM(min(max(Ke * e1, -1), 1), min(max(Kd * de1, -1), 1))
    e2 = u(t - L - 0.01) - Y[0](t - L - 0.01)
    de2 = u_dot(t - L - 0.01) - Y[1](t - L - 0.01)
    xd2 = eval_IT2FPID_KM(min(max(Ke * e2, -1), 1), min(max(Kd * de2, -1), 1))
    dxd = (xd1 - xd2) / 0.01
    return array([y2, (-1./T) * y2 + (K * Ka / T) * dxd + (K * Kb / T) * xd1])

def model_EIASC(Y, t, K, T, L, Ka, Kb, Ke, Kd):
    y2 = Y[1](t)
    y1d = Y[0](t - L)
    y2d = Y[1](t - L)
    e1 = u(t - L) - y1d
    de1 = u_dot(t - L) - y2d
    xd1 = eval_IT2FPID_EIASC(min(max(Ke * e1, -1), 1), min(max(Kd * de1, -1), 1))
    e2 = u(t - L - 0.01) - Y[0](t - L - 0.01)
    de2 = u_dot(t - L - 0.01) - Y[1](t - L - 0.01)
    xd2 = eval_IT2FPID_EIASC(min(max(Ke * e2, -1), 1), min(max(Kd * de2, -1), 1))
    dxd = (xd1 - xd2) / 0.01
    return array([y2, (-1./T) * y2 + (K * Ka / T) * dxd + (K * Kb / T) * xd1])

def model_WM(Y, t, K, T, L, Ka, Kb, Ke, Kd):
    y2 = Y[1](t)
    y1d = Y[0](t - L)
    y2d = Y[1](t - L)
    e1 = u(t - L) - y1d
    de1 = u_dot(t - L) - y2d
    xd1 = eval_IT2FPID_WM(min(max(Ke * e1, -1), 1), min(max(Kd * de1, -1), 1))
    e2 = u(t - L - 0.01) - Y[0](t - L - 0.01)
    de2 = u_dot(t - L - 0.01) - Y[1](t - L - 0.01)
    xd2 = eval_IT2FPID_WM(min(max(Ke * e2, -1), 1), min(max(Kd * de2, -1), 1))
    dxd = (xd1 - xd2) / 0.01
    return array([y2, (-1./T) * y2 + (K * Ka / T) * dxd + (K * Kb / T) * xd1])

def model_BMM(Y, t, K, T, L, Ka, Kb, Ke, Kd):
    y2 = Y[1](t)
    y1d = Y[0](t - L)
    y2d = Y[1](t - L)
    e1 = u(t - L) - y1d
    de1 = u_dot(t - L) - y2d
    xd1 = eval_IT2FPID_BMM(min(max(Ke * e1, -1), 1), min(max(Kd * de1, -1), 1))
    e2 = u(t - L - 0.01) - Y[0](t - L - 0.01)
    de2 = u_dot(t - L - 0.01) - Y[1](t - L - 0.01)
    xd2 = eval_IT2FPID_BMM(min(max(Ke * e2, -1), 1), min(max(Kd * de2, -1), 1))
    dxd = (xd1 - xd2) / 0.01
    return array([y2, (-1./T) * y2 + (K * Ka / T) * dxd + (K * Kb / T) * xd1])

def model_NT(Y, t, K, T, L, Ka, Kb, Ke, Kd):
    y2 = Y[1](t)
    y1d = Y[0](t - L)
    y2d = Y[1](t - L)
    e1 = u(t - L) - y1d
    de1 = u_dot(t - L) - y2d
    xd1 = eval_IT2FPID_NT(min(max(Ke * e1, -1), 1), min(max(Kd * de1, -1), 1))
    e2 = u(t - L - 0.01) - Y[0](t - L - 0.01)
    de2 = u_dot(t - L - 0.01) - Y[1](t - L - 0.01)
    xd2 = eval_IT2FPID_NT(min(max(Ke * e2, -1), 1), min(max(Kd * de2, -1), 1))
    dxd = (xd1 - xd2) / 0.01
    return array([y2, (-1./T) * y2 + (K * Ka / T) * dxd + (K * Kb / T) * xd1])

g1 = lambda t : 0
g2 = lambda t : 0

# %%
# Nominal
K = 1.
T = 1.
L = 0.2

# Perturbed 1.
#K = 1.3
#T = 1.9
#L = 0.4

#Perturbed 2.
#K = 1.1
#T = 1.3
#L = 0.45

tt = linspace(0., 20. ,2000)
#y_raw = ddeint(raw_sys, [g1], tt, fargs=(K, T, L, ))
#y_cl = ddeint(cl_sys, [g1], tt, fargs=(K, T, L, ))
print("KM evaluation start!")
y_it2fpid_KM = ddeint(model_KM, [g1, g2], tt, fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, ))

print("EIASC evaluation start!")
y_it2fpid_EIASC = ddeint(model_EIASC, [g1, g2], tt, fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, ))

print("WM evaluation start!")
y_it2fpid_WM = ddeint(model_WM, [g1, g2], tt, fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, ))

print("BMM evaluation start!")
y_it2fpid_BMM = ddeint(model_BMM, [g1, g2], tt, fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, ))

print("NT evaluation start!")
y_it2fpid_NT = ddeint(model_NT, [g1, g2], tt, fargs=(K, T, L, 0.25, 4.25, 0.8, 0.5, ))

figure()

ref = array([u(t) for t in tt])
plot(tt, ref, label="Reference")
plot(tt, y_it2fpid_KM[:,0], label="KM", linewidth=1.)
plot(tt, y_it2fpid_EIASC[:,0], label="EIASC", linewidth=1.)
plot(tt, y_it2fpid_WM[:,0], label="WM", linewidth=1.)
plot(tt, y_it2fpid_BMM[:,0], label="BMM", linewidth=1.)
plot(tt, y_it2fpid_NT[:,0], label="NT", linewidth=1.)


legend()
xlabel("Time (s)")
ylabel("System response")
grid(True)

savefig("delay_pid_case1_comp.pdf", format="pdf", dpi=300, bbox_inches="tight")
show()



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





