#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 10:24:56 2020

@author: arslan
"""

from pyit2fls import Mamdani, IT2FS_Gaussian_UncertStd, IT2FS_plot, \
                     product_t_norm, max_s_norm, crisp
from numpy import linspace, random, sin, cos, array

domainX1 = linspace(-1., 1., 101)
domainX2 = linspace(-1., 1., 101)
domainY1 = linspace(-0.5, 1.5, 101)
domainY2 = linspace(-0.5, 1.5, 101)

X1Small = IT2FS_Gaussian_UncertStd(domainX1, [-1., 0.2, 0.1, 1.])
X1Medium = IT2FS_Gaussian_UncertStd(domainX1, [0., 0.2, 0.1, 1.])
X1Large = IT2FS_Gaussian_UncertStd(domainX1, [1., 0.2, 0.1, 1.])
# IT2FS_plot(X1Small, X1Medium, X1Large)

X2Small = IT2FS_Gaussian_UncertStd(domainX2, [-1., 0.2, 0.1, 1.])
X2Medium = IT2FS_Gaussian_UncertStd(domainX2, [0., 0.2, 0.1, 1.])
X2Large = IT2FS_Gaussian_UncertStd(domainX2, [1., 0.2, 0.1, 1.])
# IT2FS_plot(X2Small, X2Medium, X2Large)

Y1Small = IT2FS_Gaussian_UncertStd(domainY1, [-0.5, 0.2, 0.1, 1.])
Y1Medium = IT2FS_Gaussian_UncertStd(domainY1, [0.5, 0.2, 0.1, 1.])
Y1Large = IT2FS_Gaussian_UncertStd(domainY1, [1.5, 0.2, 0.1, 1.])
# IT2FS_plot(Y1Small, Y1Medium, Y1Large)

Y2Small = IT2FS_Gaussian_UncertStd(domainY2, [-0.5, 0.2, 0.1, 1.])
Y2Medium = IT2FS_Gaussian_UncertStd(domainY2, [0.5, 0.2, 0.1, 1.])
Y2Large = IT2FS_Gaussian_UncertStd(domainY2, [1., 0.2, 0.1, 1.])
# IT2FS_plot(Y2Small, Y2Medium, Y2Large)

myIT2FLS = Mamdani(product_t_norm, max_s_norm, method="CoSet")
myIT2FLS.add_input_variable("x1")
myIT2FLS.add_input_variable("x2")
myIT2FLS.add_output_variable("y1")
myIT2FLS.add_output_variable("y2")

nX1 = 3
X1Sets = [X1Small, X1Medium, X1Large]
nX2 = 3
X2Sets = [X2Small, X2Medium, X2Large]
nY1 = 3
Y1Sets = [Y1Small, Y1Medium, Y1Large]
nY2 = 3
Y2Sets = [Y2Small, Y2Medium, Y2Large]

def generateRuleBase():
    Rules = []
    for i in range(9):
        rule = [i // nX1, i % nX2, 
                random.randint(nY1), random.randint(nY2)]
        Rules.append(rule)
    return Rules


tt = 2 * (random.rand(20) - 0.5)
Data = array([sin(tt), 
              cos(tt), 
              sin(tt) + cos(tt), 
              cos(tt) - sin(tt)])

def error(R, D):
    # R: Rules
    # D: Data
    err = 0.
    myIT2FLS.rules = []
    for rule in R:
        myIT2FLS.add_rule([("x1", X1Sets[rule[0]]), ("x2", X2Sets[rule[1]])], 
                          [("y1", Y1Sets[rule[2]]), ("y2", Y2Sets[rule[3]])])
    for i in range(D.shape[1]):
        tr = myIT2FLS.evaluate({"x1":D[0, i], "x2":D[1, i]})
        err += (crisp(tr["y1"]) - D[2, i]) ** 2 + (crisp(tr["y2"]) - D[3, i]) ** 2
    return err
    
if __name__ == "__main__":
    myRules = [[0, 0, 0, 1], 
              [0, 1, 0, 2], 
              [0, 2, 1, 2], 
              [1, 0, 0, 0], 
              [1, 1, 1, 1], 
              [1, 2, 2, 2], 
              [2, 0, 1, 0], 
              [2, 1, 2, 0], 
              [2, 2, 2, 1]]
    minErr = float("inf")
    minRules = []
    for i in range(100):
        rule = generateRuleBase()
        err = error(rule, Data)
        if err < minErr:
            minErr = err
            minRules = rule
        print(str(i) + ".", err)
    
    print("Best generated rule base:")
    print(minRules)
    print("Minimum error:", minErr)
    
    print("Rule base defined by expert:")
    print(myRules)
    print("Error:", error(myRules, Data))




























