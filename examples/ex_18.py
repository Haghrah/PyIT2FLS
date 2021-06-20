#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 11:51:49 2021

@author: arslan
"""


from pyit2fls import (IT2FS_Gaussian_UncertStd, IT2FS_LGaussian_UncertStd, 
                      IT2FS_RGaussian_UncertStd, IT2Mamdani, product_t_norm, 
                      probabilistic_sum_s_norm, IT2FS_plot, crisp, )

from numpy import (random, linspace, array, zeros, shape, sort, 
                   maximum, minimum, )
from scipy.optimize import (differential_evolution, minimize, basinhopping, )
from PyPSO import PyPSO

class Classifier:
    
    def normalizeParameters(self, parameters, n=3):
        p = zeros(shape=(3 * n + 2 + 3 ** n, ))
        
        for i in range(n):
            p[3 * i:3 * (i + 1)] = sort(parameters[3 * i:3 * (i + 1)])
        
        p[3 * n:3 * n + 2] = maximum(0., minimum(1., sort(parameters[3 * n:3 * n + 2])))
        
        p[3 * n + 2:] = parameters[3 * n + 2:] > 0
        
        return p
    
    def __init__(self, attributes, decisions, parameters, n=3):
        self.attributes = attributes
        self.decisions = decisions
        self.p = self.normalizeParameters(parameters)
        
        self.idomain = linspace(-1.0, 1.0, 1001)
        self.odomain = linspace( 0.0, 1.0, 1001)
        
        self.att1_s1 = IT2FS_RGaussian_UncertStd(self.idomain, params=[self.p[0], 
                                                                        0.25, 0.05, 1.0])
        self.att1_s2 = IT2FS_Gaussian_UncertStd(self.idomain,  params=[self.p[1], 
                                                                        0.25, 0.05, 1.0])
        self.att1_s3 = IT2FS_LGaussian_UncertStd(self.idomain, params=[self.p[2], 
                                                                        0.25, 0.05, 1.0])
        self.ATT1_SETS = [self.att1_s1, self.att1_s2, self.att1_s3]
        
        
        self.att2_s1 = IT2FS_RGaussian_UncertStd(self.idomain, params=[self.p[3], 
                                                                        0.25, 0.05, 1.0])
        self.att2_s2 = IT2FS_Gaussian_UncertStd(self.idomain,  params=[self.p[4], 
                                                                        0.25, 0.05, 1.0])
        self.att2_s3 = IT2FS_LGaussian_UncertStd(self.idomain, params=[self.p[5], 
                                                                        0.25, 0.05, 1.0])
        self.ATT2_SETS = [self.att2_s1, self.att2_s2, self.att2_s3]
        
        
        self.att3_s1 = IT2FS_RGaussian_UncertStd(self.idomain, params=[self.p[6], 
                                                                        0.25, 0.05, 1.0])
        self.att3_s2 = IT2FS_Gaussian_UncertStd(self.idomain,  params=[self.p[7], 
                                                                        0.25, 0.05, 1.0])
        self.att3_s3 = IT2FS_LGaussian_UncertStd(self.idomain, params=[self.p[8], 
                                                                        0.25, 0.05, 1.0])
        self.ATT3_SETS = [self.att3_s1, self.att3_s2, self.att3_s3]
        
        
        self.deci_s1 = IT2FS_RGaussian_UncertStd(self.odomain, params=[self.p[9], 
                                                                        0.25, 0.05, 1.0])
        self.deci_s2 = IT2FS_LGaussian_UncertStd(self.odomain, params=[self.p[10], 
                                                                        0.25, 0.05, 1.0])
        self.DECI_SETS = [self.deci_s1, self.deci_s2]
        
        
        self.DM = IT2Mamdani(product_t_norm, probabilistic_sum_s_norm)
        
        self.DM.add_input_variable("ATT1")
        self.DM.add_input_variable("ATT2")
        self.DM.add_input_variable("ATT3")
        
        self.DM.add_output_variable("DECI")
        
        
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.DM.add_rule([("ATT1", self.ATT1_SETS[i]), 
                                      ("ATT2", self.ATT2_SETS[j]), 
                                      ("ATT3", self.ATT3_SETS[k])], 
                                     [("DECI", self.DECI_SETS[int(self.p[11 + i * 9 + j * 3 + k])])])
    
    def __call__(self, att1, att2, att3):
        o, tr = self.DM.evaluate({"ATT1": att1, "ATT2": att2, "ATT3": att3})
        return crisp(tr["DECI"])
    
    def error(self):
        err = 0.
        for attribute, decision in zip(self.attributes, self.decisions):
            o = self.__call__(*attribute)
            if o > 0.51 and decision != 1:
                err += o - 0.51
            elif o < 0.49 and decision != 0:
                err += 0.49 - o
        return err / len(self.decisions)

if __name__ == "__main__":
    
    def parametersGenerator(n=3):
        return 2 * (random.rand(3 * n + 2 + 3 ** n) - 0.5)
    
    def velocityGenerator(n=3):
        return 4. * (random.rand(3 * n + 2 + 3 ** n) - 0.5)
    
    
    attributes = array([[-0.4, -0.3, -0.5], 
                        [-0.4,  0.2, -0.1], 
                        [-0.3, -0.4, -0.3], 
                        [ 0.3, -0.3,  0.0], 
                        [ 0.2, -0.3,  0.0], 
                        [ 0.2,  0.0,  0.0]])
    decisions = array([1, 0, 1, 0, 0, 1])
    
    def error(p):
        myClassifier = Classifier(attributes, decisions, p)
        return myClassifier.error()
    
    mySolver= PyPSO(error, 5, 100, parametersGenerator, velocityGenerator)
    mySolver.solve()
    
    p = mySolver.best_known_position
    
    myClassifier = Classifier(attributes, decisions, p)
    IT2FS_plot(myClassifier.att1_s1, myClassifier.att1_s2, myClassifier.att1_s3)
    IT2FS_plot(myClassifier.att2_s1, myClassifier.att2_s2, myClassifier.att2_s3)
    IT2FS_plot(myClassifier.att3_s1, myClassifier.att3_s2, myClassifier.att3_s3)
    IT2FS_plot(myClassifier.deci_s1, myClassifier.deci_s2)
    
    print(myClassifier.error())




























