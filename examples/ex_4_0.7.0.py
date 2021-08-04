#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 13:13:55 2019

@author: arslan
"""
import numpy as np
import matplotlib.pyplot as plt
from pyit2fls import IT2FS_Gaussian_UncertStd, IT2Mamdani, min_t_norm, max_s_norm
import PyPSO
from time import time

def mackey_glass(tav, n, beta, gamma, step):
    x = [np.random.random() for i in range(tav)]
    for i in range(step):
        x.append(x[-1] + beta * x[-tav] / (1 + x[-tav] ** n) - gamma * x[-1])
    return x[tav:]

mg = mackey_glass(2, 9.65, 2., 1., 1000)

# plt.figure()
# plt.plot(mg[200:600])
# plt.xticks([40 * i for i in range(11)], [str(40 * i + 200) for i in range(11)])
# plt.ylim(bottom=0, top=1.8)
# plt.legend(["Mackey-Glass dynamics\n" + r"$\gamma$=1, $\beta$=2, $\tau$=2, and $n$=9.65"])
# plt.grid(True)
# plt.savefig("mackey_glass_1.eps", format="eps", dpi=500, bbox_inches="tight")
# plt.show()

domain = np.linspace(0., 1.5, 15)
L = 100  # Learning set length
LearningSet = []
for i in range(200, 200 + L):
    LearningSet.append([[mg[i], mg[i - 1], mg[i - 2]], mg[i + 1]])

it2fls = IT2Mamdani(t_norm=min_t_norm, s_norm=max_s_norm,
                    method="Height", algorithm="EIASC")
it2fls.add_input_variable("A")
it2fls.add_input_variable("B")
it2fls.add_input_variable("C")
it2fls.add_output_variable("O")

it2fls.add_rule([("A", ), ("B", ), ("C", )], [("O", )])
it2fls.add_rule([("A", ), ("B", ), ("C", )], [("O", )])
it2fls.add_rule([("A", ), ("B", ), ("C", )], [("O", )])

def calculate(x, i):
    A1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[:3], 1))
    A2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[3:6], 1))
    A3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[6:9], 1))
    
    B1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[9:12], 1))
    B2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[12:15], 1))
    B3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[15:18], 1))
    
    C1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[18:21], 1))
    C2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[21:24], 1))
    C3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[24:27], 1))
    
    O1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[27:30], 1))
    O2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[30:33], 1))
    O3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[33:36], 1))
    
    it2fls.rules[0] = ([("A", A1), ("B", B1), ("C", C1)], [("O", O1)])
    it2fls.rules[1] = ([("A", A2), ("B", B2), ("C", C2)], [("O", O2)])
    it2fls.rules[2] = ([("A", A3), ("B", B3), ("C", C3)], [("O", O3)])
    
    tr = it2fls.evaluate({"A":i[0], "B":i[1], "C":i[2]})
    o = tr["O"]
    return (o[0] + o[1]) / 2

def cost_func(x):
    A1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[:3], 1))
    A2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[3:6], 1))
    A3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[6:9], 1))
    
    B1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[9:12], 1))
    B2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[12:15], 1))
    B3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[15:18], 1))
    
    C1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[18:21], 1))
    C2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[21:24], 1))
    C3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[24:27], 1))
    
    O1 = IT2FS_Gaussian_UncertStd(domain, np.append(x[27:30], 1))
    O2 = IT2FS_Gaussian_UncertStd(domain, np.append(x[30:33], 1))
    O3 = IT2FS_Gaussian_UncertStd(domain, np.append(x[33:36], 1))
    
    it2fls.rules[0] = ([("A", A1), ("B", B1), ("C", C1)], [("O", O1)])
    it2fls.rules[1] = ([("A", A2), ("B", B2), ("C", C2)], [("O", O2)])
    it2fls.rules[2] = ([("A", A3), ("B", B3), ("C", C3)], [("O", O3)])
    
    err = 0
    for L in LearningSet:
        tr = it2fls.evaluate({"A":L[0][0], "B":L[0][1], "C":L[0][2]})
        o = tr["O"]
        err += ((o[0] + o[1]) / 2 - L[1]) ** 2
    return err / len(LearningSet)


def solution_generator():
    return 1.5 * np.random.rand(12 * 3)

def velocity_generator():
    return 2.5 * np.random.rand(12 * 3)

mySolver = PyPSO.PyPSO(cost_func, 50, 75, solution_generator, velocity_generator)
t = time()
conv = mySolver.solve()
print(time() - t)

plt.figure()
plt.plot(conv)
plt.grid(True)
plt.xlabel("Iteration")
plt.ylabel("MSE")
plt.savefig("convergence.pdf", format="pdf", dpi=300, bbox_inches="tight")
plt.show()

out = []
correct = []
for i in range(200, 200 + L):
    out.append(calculate(mySolver.best_known_position, [mg[i], mg[i - 1], mg[i - 2]]))
    correct.append(mg[i + 1])

out = np.array(out)
correct = np.array(correct)
error = np.abs(out - correct)

plt.figure()
plt.plot(out, linewidth=1.)
plt.plot(correct, linewidth=1.)
plt.plot(error, linewidth=1.)
plt.grid(True)
plt.legend(["Predicted", "Real", "Error"], loc=1)
plt.xlabel("t")
plt.ylabel("y(t)")
plt.savefig("MackeyGlassSO1.pdf", format="pdf", dpi=300, bbox_inches="tight")
plt.show()


out = []
correct = []
for i in range(200 + L, 200 + 2 * L):
    out.append(calculate(mySolver.best_known_position, [mg[i], mg[i - 1], mg[i - 2]]))
    correct.append(mg[i + 1])
out = np.array(out)
correct = np.array(correct)
error = np.abs(out - correct)

plt.figure()
plt.plot(out, linewidth=1.)
plt.plot(correct, linewidth=1.)
plt.plot(error, linewidth=1.)
plt.grid(True)
plt.legend(["Predicted", "Real", "Error"], loc=1)
plt.xlabel("t")
plt.ylabel("y(t)")
plt.savefig("MackeyGlassSO2.pdf", format="pdf", dpi=300, bbox_inches="tight")
plt.show()

















