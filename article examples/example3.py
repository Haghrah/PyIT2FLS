#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:11:43 2024

@author: arslan
"""

from numpy import (linspace, array, vstack, )
from numpy.random import (random, )
import matplotlib.pyplot as plt
from pyit2fls import (IT2TSK_ML, T1TSK_ML, IT2FS_Gaussian_UncertMean, )

def mackey_glass(tav, n, beta, gamma, step):
    x = [random() for i in range(tav)]
    for i in range(step):
        x.append(x[-1] + beta * x[-tav] / (1 + x[-tav] ** n) - gamma * x[-1])
    return array(x[tav:])

mg = mackey_glass(2, 9.65, 2., 1., 1000)

domain = linspace(0., 1.5, 15)
H = 3
L = 100  # Training and test data length
S = 200  # Starting index of training and test data in Mackey-Glass time series
X_train = vstack([mg[S - h - 1:S + L - h - 1] for h in range(H)]).T
X_test  = vstack([mg[S + L - h - 1:S + 2 * L - h - 1] for h in range(H)]).T
y_train_actual = mg[S:S + L]
y_test_actual = mg[S + L:S + 2 * L]
for i in range(S, S + L):
    X_train[i - S, :]      = array(mg[i - H    :i])
    X_test[i - S, :] = array(mg[i + L - H:i + L])

N = 3
M = 9
myIT2TSK = IT2TSK_ML(N, M, IT2FS_Gaussian_UncertMean, (-2., 2.), 
                     algorithm="GA", 
                     algorithm_params=[50, 100, 400, 20, 0.04])
myIT2TSK.fit(X_train, y_train_actual)
y_train_prediction = myIT2TSK.score(X_train)
y_test_prediction = myIT2TSK.score(X_test)

learning_indices = linspace(S, S + L - 1, L)
test_indices = linspace(S + L, S + 2 * L - 1, L)

plt.figure(figsize=(12, 5), )
plt.plot(learning_indices, y_train_actual, label="Actual Training Values", linestyle="-", )
plt.plot(learning_indices, y_train_prediction, label="Model Fit (Training)", linestyle="--", )
plt.plot(test_indices, y_test_actual, label="Actual Test Values", linestyle=":", )
plt.plot(test_indices, y_test_prediction, label="Model Forecast (Test)", linestyle="-.", )
plt.xticks([S + 10 * i for i in range(21)])
plt.title("Mackey-Glass Chaotic Time Series\n" + r"$\gamma$=1, $\beta$=2, $\tau$=2, and $n$=9.65")
plt.legend(loc="upper left", bbox_to_anchor=(1., 1.02))
plt.grid(which="major", linestyle="-", linewidth=0.75, color="gray", alpha=0.7)
plt.minorticks_on() 
plt.grid(which="minor", linestyle=":", linewidth=0.5, color="lightgray", alpha=0.7)
plt.savefig("../images/mackey_glass_1.pdf", format="pdf", dpi=600, bbox_inches="tight")
plt.show()


myTSK = T1TSK_ML(N, M, (-4., 4.), algorithm="PSO", 
                 algorithm_params=[200, 200, 0.3, 0.3, 1.8])
myTSK.fit(X_train, y_train_actual)
y_train_prediction = myTSK.score(X_train)
y_test_prediction = myTSK.score(X_test)

plt.figure(figsize=(12, 5), )
plt.plot(learning_indices, y_train_actual, label="Actual Training Values", linestyle="-", )
plt.plot(learning_indices, y_train_prediction, label="Model Fit (Training)", linestyle="--", )
plt.plot(test_indices, y_test_actual, label="Actual Test Values", linestyle=":", )
plt.plot(test_indices, y_test_prediction, label="Model Forecast (Test)", linestyle="-.", )
plt.xticks([S + 10 * i for i in range(21)])
plt.title("Mackey-Glass Chaotic Time Series\n" + r"$\gamma$=1, $\beta$=2, $\tau$=2, and $n$=9.65")
plt.legend(loc="upper left", bbox_to_anchor=(1., 1.02))
plt.grid(which="major", linestyle="-", linewidth=0.75, color="gray", alpha=0.7)
plt.minorticks_on() 
plt.grid(which="minor", linestyle=":", linewidth=0.5, color="lightgray", alpha=0.7)
plt.savefig("../images/mackey_glass_2.pdf", format="pdf", dpi=600, bbox_inches="tight")
plt.show()













