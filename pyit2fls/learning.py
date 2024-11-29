#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 01:39:58 2024

@author: arslan
"""

from numpy import (reshape, exp, array, zeros, zeros_like, asarray, linspace, )
from numpy.linalg import (norm, )
from numpy.random import (rand, randint, )
from scipy.optimize import (differential_evolution, minimize, )
from pyit2fls import (T1FS, gaussian_mf, T1Mamdani, T1TSK, 
                      IT2FS_Gaussian_UncertMean, IT2FS_Gaussian_UncertStd, 
                      IT2Mamdani, IT2TSK, product_t_norm, max_s_norm, crisp, )


class PSO:
    
    def __init__(self, N, M, func, bounds, args=()):
        self.func = func
        self.args = args
        self.N  = N
        self.M  = M
        self.bounds = bounds
        self.X  = self.bounds[0] + (self.bounds[1] - self.bounds[0]) * rand(self.N, self.M)
        self.V  = 4.0 * (self.bounds[1] - self.bounds[0]) * (rand(self.N, self.M) - 0.5)
        self.Xb = self.X.copy()
        self.Fb = zeros(shape=(self.N, ))
        
        self.Fb[0] = self.func(self.X[0, :], *self.args)
        
        self.xb = self.X[0, :].copy()
        self.fb = self.Fb[0]
        
        self.iterNum = 0
        
        for i in range(1, self.N):
            self.Fb[i] = self.func(self.X[i, :], *self.args)
                
            if self.Fb[i] < self.fb:
                self.fb = self.Fb[i]
                self.xb = self.X[i, :].copy()
    
    
    def iterate(self, omega=0.3, phi_p=0.3, phi_g=2.1):
        self.iterNum += 1
        r_p = rand(self.N, self.M)
        r_g = rand(self.N, self.M)
        self.V = omega * self.V + \
                 phi_p * r_p * (self.Xb - self.X) + \
                 phi_g * r_g * (self.xb - self.X)
        self.X = self.X + self.V
        
        for i in range(self.N):
            tmp = self.func(self.X[i, :], *self.args)
                
            if tmp < self.Fb[i]:
                self.Xb[i, :] = self.X[i, :].copy()
                self.Fb[i] = tmp
                if tmp < self.fb:
                    self.xb = self.X[i, :].copy()
                    self.fb = tmp


class solution:
    
    def __init__(self, M, func, bounds, args=()):
        self.solution = bounds[0] + (bounds[1] - bounds[0]) * rand(M, )
        self.fitness = func(self.solution, *args)


class GA:
    
    def __init__(self, N, M, func, bounds, args=()):
        self.func = func
        self.args = args
        self.N  = N
        self.M  = M
        self.bounds = bounds
        self.population = []
        for i in range(self.N):
            self.population.append(solution(self.M, self.func, self.bounds, args))

        self.population = sorted(self.population, key=lambda solution:solution.fitness)
        self.iterNum = 0
    
    
    def tournament_selection(self, num, tp):
        high = int(self.N * tp)
        return [i1 if self.population[i1].fitness < self.population[i2].fitness else i2 
                for i1, i2 in zip(randint(high, size=num), randint(high, size=num))]
    
    
    def mutate(self, individual):
        transfer_vector = (rand(self.M) -0.5) / (self.iterNum + 1.)
        return individual.solution.copy() + transfer_vector
    
    def crossover(self, parent1, parent2):
        a = rand(self.M)
        b = rand(self.M)
        return (a * parent1.solution + b * parent2.solution) / (a + b)
    
    def iterate(self, mutation_num, crossover_num, tp):
        parent_list = self.tournament_selection(2 * crossover_num, 1.0)
        
        for i, j in zip(parent_list[::2], parent_list[1::2]):
            child_solution = self.crossover(self.population[i], self.population[j])
            if self.func(child_solution, *self.args) < self.population[i].fitness:
                self.population[i].solution = child_solution.copy()
                self.population[i].fitness = self.func(child_solution, *self.args)
            elif self.func(child_solution, *self.args) < self.population[j].fitness:
                self.population[j].solution = child_solution.copy()
                self.population[j].fitness = self.func(child_solution, *self.args)

        parent_list = self.tournament_selection(mutation_num, tp)
        for i in parent_list:
            mutated_solution = self.mutate(self.population[i])
            if self.func(mutated_solution, *self.args) < self.population[i].fitness:
                self.population[i].solution = mutated_solution.copy()
                self.population[i].fitness = self.func(mutated_solution, *self.args)
        
        self.population = sorted(self.population, key=lambda solution:solution.fitness)
        self.iterNum += 1


class gaussian_mf_learning:

    def d0(self, x, c, v):
        return exp(- ((x - c) / v) ** 2)

    def d1(self, x, c, v):
        return - 2 * ((x - c) / v ** 2) * exp(- ((x - c) / v) ** 2)


class T1Fuzzy_ML_Model:
    """
    N: Number of inputs
    M: Number of rules
    P: Model parameters (a vector of size M * (2 * N + 1))
    mf: List of membership functions for each input in each rule
    c: Output scaling factor
    """
    def __init__(self, P, N, M, mf, c=1.0):
        self.p = reshape(P[:-M], (M, N, 2, ))
        for i in range(M):
            for j in range(N):
                self.p[i][j][1] = abs(self.p[i][j][1])

        self.q = P[-M:]
        self.N = N
        self.M = M
        self.mf = mf
        self.c = c
    
    def d0(self, d0x):
        s = 1.
        d = 0.
        n = 0.
        for l in range(self.M):
            s = 1.
            for i in range(self.N):
                s *= self.mf[l][i].d0(d0x[i], self.p[l][i][0], self.p[l][i][1])
            n += self.q[l] * s
            d += s
        return self.c * n / d
    
    def d1(self, d0x, d1x):
        s1 = 0.
        s2 = 0.
        s3 = 0.
        s4 = 0.
        
        for l in range(self.M):
            s5 = 1.
            for i in range(self.N):
                s5 *= self.mf[l][i].d0(d0x[i], self.p[l][i][0], self.p[l][i][1])
            s1 += self.q[l] * s5
            s2 += s5
        
        for j in range(self.N):
            s7 = 0.
            s8 = 0.
            for l in range(self.M):
                s6 = 1.
                for i in range(self.N):
                    if i != j:
                        s6 *= self.mf[l][i].d0(d0x[i], self.p[l][i][0], self.p[l][i][1])
                
                s7 += self.q[l] * self.mf[l][j].d1(d0x[j], self.p[l][j][0], self.p[l][j][1]) * s6
                s8 += self.mf[l][j].d1(d0x[j], self.p[l][j][0], self.p[l][j][1]) * s6
            
            s3 += d1x[j] * s7
            s4 += d1x[j] * s8
        
        return (s3 * s2 - s1 * s4) / s2 ** 2


class T1Fuzzy_ML:

    def __init__(self, N, M, Bounds=None, algorithm="DE", algorithm_params=[]):
        self.N = N
        self.M = M
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params
        self.paramNum = M * (2 * N + 1)
        self.params = rand(self.paramNum, )
        self.Bounds = [Bounds, ] * self.paramNum
        self.mf = gaussian_mf_learning()
        self.model = T1Fuzzy_ML_Model(self.params, self.N, self.M, 
                                      [[self.mf, ] * self.N, ] * self.M)

    def error(self, P, X, y):
        model = T1Fuzzy_ML_Model(P, self.N, self.M, 
                                 [[self.mf, ] * self.N, ] * self.M)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model.d0(x)
        return norm(y - o)

    def fit(self, X, y):
        if self.algorithm == "DE":
            self.params = differential_evolution(self.error, bounds=self.Bounds, 
                                            args=(X, y), disp=True).x
        elif self.algorithm == "Nelder-Mead":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "Powell":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "CG":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, 
                              options={"disp":True, }).x
        elif self.algorithm == "PSO":
            myPSO = PSO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4])
                print("Iteration ", i+1, ".", myPSO.fb)
            self.params = myPSO.xb
        elif self.algorithm == "GA":
            myGA = GA(self.algorithm_params[0], self.paramNum, self.error, 
                      self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myGA.iterate(self.algorithm_params[2], 
                             self.algorithm_params[3], 
                             self.algorithm_params[4], )
                print("Iteration ", i+1, ".", myGA.population[0].fitness)
            self.params = myGA.population[0].solution
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
        self.model = T1Fuzzy_ML_Model(self.params, self.N, self.M, 
                                      [[self.mf, ] * self.N, ] * self.M)
        return self.error(self.params, X, y)

    def score(self, X):
        X = asarray(X)
        if X.ndim == 1:
            return self.model.d0(X)
        elif X.ndim == 2:
            o = []
            for x in X:
                o.append(self.model.d0(x))
            return array(o)
        else:
            raise ValueError("Input must be a 1D or 2D NumPy array!")


class T1Mamdani_ML(T1Fuzzy_ML):
    
    def __init__(self, N, M, Bounds=None, algorithm="DE", algorithm_params=[]):
        super().__init__(N, M, Bounds, algorithm, algorithm_params)
    
    def get_T1Mamdani(self, std=1., ):
        generated_T1Mamdani = T1Mamdani()

        for i in range(self.N):
            generated_T1Mamdani.add_input_variable("X" + str(i + 1))
        generated_T1Mamdani.add_output_variable("Y")

        for i in range(self.M):
            antecedent = []
            for j in range(self.N):
                domain = linspace(self.model.p[i][j][0] - 5. * self.model.p[i][j][1], # 5 x std before mean
                                  self.model.p[i][j][0] + 5. * self.model.p[i][j][1], # 5 x std after mean
                                  int(10. * self.model.p[i][j][1] * 100)) # 100 points for each unit
                antecedent.append(("X" + str(i + 1), 
                                   T1FS(domain, gaussian_mf, 
                                        params=[self.model.p[i][j][0], self.model.p[i][j][1], 1., ])))

            domain = linspace(self.model.q[i] - 5. * std, # 5 x std before mean
                              self.model.q[i] + 5. * std, # 5 x std after mean
                              int(10. * std * 100.)) # 100 points for each unit
            consequent = [("Y", 
                           T1FS(domain, gaussian_mf, 
                                params=[self.model.q[i], std, 1., ]), ), 
                         ]
            generated_T1Mamdani.add_rule(antecedent, consequent)

        return generated_T1Mamdani


class T1TSK_ML(T1Fuzzy_ML):
    
    def __init__(self, N, M, Bounds=None, algorithm="DE", algorithm_params=[]):
        super().__init__(N, M, Bounds, algorithm, algorithm_params)

    def get_T1TSK(self, std=1., ):
        generated_T1TSK = T1TSK()

        for i in range(self.N):
            generated_T1TSK.add_input_variable("X" + str(i + 1))
        generated_T1TSK.add_output_variable("Y")

        for i in range(self.M):
            antecedent = []
            for j in range(self.N):
                domain = linspace(self.model.p[i][j][0] - 5. * self.model.p[i][j][1], # 5 x std before mean
                                  self.model.p[i][j][0] + 5. * self.model.p[i][j][1], # 5 x std after mean
                                  int(10. * self.model.p[i][j][1] * 100)) # 100 points for each unit
                antecedent.append(("X" + str(i + 1), 
                                   T1FS(domain, gaussian_mf, 
                                        params=[self.model.p[i][j][0], self.model.p[i][j][1], 1., ])))

            consequent = [("Y", lambda *X: self.model.q[i]), 
                         ]
            generated_T1TSK.add_rule(antecedent, consequent)

        return generated_T1TSK


class T1TSK_SI_Model:

    def __init__(self, ):
        pass


class T1TSK_SI:

    def __init__(self, ):
        pass

    def __call__(self, ):
        pass


class IT2TSK_ML_Model:

    def __init__(self, P, N, M, it2fs, c=1.0):
        self.N = N
        self.M = M
        self.p = reshape(P[:-M], (M, N, 3, ))
        for i in range(M):
            for j in range(N):
                self.p[i][j][1] = abs(self.p[i][j][1])
                self.p[i][j][2] = abs(self.p[i][j][2])
        self.q = P[-M:]

        self.model = IT2TSK(product_t_norm, max_s_norm)
        for i in range(N):
            self.model.add_input_variable(f"X{i + 1}")
        self.model.add_output_variable("Y")

        self.it2fs = it2fs
        self.c = c
        
        for i in range(M):
            antecedent = []
            consequentDict = {"const":self.q[i], }
            for j in range(N):
                if it2fs == IT2FS_Gaussian_UncertMean:
                    std = self.p[i][j][2]
                elif it2fs == IT2FS_Gaussian_UncertStd:
                    std = self.p[i][j][1]
                else:
                    raise ValueError("You can use only IT2FS_Gaussian_UncertMean or IT2FS_Gaussian_UncertStd!")
                
                domain = linspace(self.p[i][j][0] - 5. * std, # 5 x std before mean
                                  self.p[i][j][0] + 5. * std, # 5 x std after mean
                                  int(10. * std * 10)) # 10 points for each unit
                antecedent.append((f"X{j + 1}", 
                                   it2fs(domain, params=[self.p[i][j][0], 
                                                         self.p[i][j][1], 
                                                         self.p[i][j][2], 
                                                         1.0]), ), )
                consequentDict[f"X{j + 1}"] = 0.
            
            consequent = [("Y", consequentDict)]
            self.model.add_rule(antecedent, consequent)

    def __call__(self, X):
        _X = {f"X{i + 1}":X[i] for i in range(self.N)}
        return self.model.evaluate(_X)["Y"]


class IT2TSK_ML:

    def __init__(self, N, M, it2fs, Bounds=None, algorithm="DE", algorithm_params=[], c=1.0):
        self.N = N
        self.M = M
        self.it2fs = it2fs
        self.Bounds = Bounds
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params
        self.c = c
        self.paramNum = M * (3 * N + 1)
        self.params = rand(self.paramNum, )
        self.Bounds = [Bounds, ] * self.paramNum
        self.model = IT2TSK_ML_Model(self.params, self.N, self.M, self.it2fs, self.c)

    def error(self, P, X, y):
        model = IT2TSK_ML_Model(P, self.N, self.M, self.it2fs, self.c)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model(x)
        return norm(y - o)

    def fit(self, X, y):
        if self.algorithm == "DE":
            self.params = differential_evolution(self.error, bounds=self.Bounds, 
                                            args=(X, y), disp=True).x
        elif self.algorithm == "Nelder-Mead":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "Powell":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "CG":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, 
                              options={"disp":True, }).x
        elif self.algorithm == "PSO":
            myPSO = PSO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4])
                print("Iteration ", i+1, ".", myPSO.fb)
            self.params = myPSO.xb
        elif self.algorithm == "GA":
            myGA = GA(self.algorithm_params[0], self.paramNum, self.error, 
                      self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myGA.iterate(self.algorithm_params[2], 
                             self.algorithm_params[3], 
                             self.algorithm_params[4], )
                print("Iteration ", i+1, ".", myGA.population[0].fitness)
            self.params = myGA.population[0].solution
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
        self.model = IT2TSK_ML_Model(self.params, self.N, self.M, self.it2fs, self.c)
        return self.error(self.params, X, y)

    def score(self, X):
        X = asarray(X)
        if X.ndim == 1:
            return self.model(X)
        elif X.ndim == 2:
            o = []
            for x in X:
                o.append(self.model(x))
            return array(o)
        else:
            raise ValueError("Input must be a 1D or 2D NumPy array!")


class IT2Mamdani_ML_Model:

    def __init__(self, P, N, M, it2fs, c=1.0):
        self.N = N
        self.M = M
        self.p = reshape(P[:-3 * M], (M, N, 3, ))
        for i in range(M):
            for j in range(N):
                self.p[i][j][1] = abs(self.p[i][j][1])
                self.p[i][j][2] = abs(self.p[i][j][2])
        self.q = reshape(P[-3 * M:], (M, 3))
        for i in range(M):
            self.q[i][1] = abs(self.q[i][1])
            self.q[i][2] = abs(self.q[i][2])

        self.model = IT2Mamdani(product_t_norm, max_s_norm)
        
        for i in range(N):
            self.model.add_input_variable(f"X{i + 1}")
        self.model.add_output_variable("Y")

        self.it2fs = it2fs
        self.c = c

        for i in range(M):
            antecedent = []
            for j in range(N):
                if it2fs == IT2FS_Gaussian_UncertMean:
                    std = self.p[i][j][2]
                elif it2fs == IT2FS_Gaussian_UncertStd:
                    std = self.p[i][j][1]
                else:
                    raise ValueError("You can use only IT2FS_Gaussian_UncertMean or IT2FS_Gaussian_UncertStd!")
                
                domain = linspace(self.p[i][j][0] - 5. * std, # 5 x std before mean
                                  self.p[i][j][0] + 5. * std, # 5 x std after mean
                                  int(10. * std * 10)) # 10 points for each unit
                antecedent.append((f"X{j + 1}", 
                                   it2fs(domain, params=[self.p[i][j][0], 
                                                         self.p[i][j][1], 
                                                         self.p[i][j][2], 
                                                         1.0]), ), )
            if it2fs == IT2FS_Gaussian_UncertMean:
                std = self.q[i][2]
            elif it2fs == IT2FS_Gaussian_UncertStd:
                std = self.q[i][1]
            else:
                raise ValueError("You can use only IT2FS_Gaussian_UncertMean or IT2FS_Gaussian_UncertStd!")
            
            domain = linspace(self.q[i][0] - 5. * std, # 5 x std before mean
                              self.q[i][0] + 5. * std, # 5 x std after mean
                              int(10. * std * 10)) # 10 points for each unit

            consequent = [("Y", it2fs(domain, params=[self.p[i][j][0], 
                                                      self.p[i][j][1], 
                                                      self.p[i][j][2], 
                                                      1.0]), ), ]
            self.model.add_rule(antecedent, consequent)


    def __call__(self, X):
        _X = {f"X{i + 1}":X[i] for i in range(self.N)}
        it2out, tr = self.model.evaluate(_X)
        return crisp(tr["Y"])



class IT2Mamdani_ML:

    def __init__(self, N, M, it2fs, Bounds=None, algorithm="DE", algorithm_params=[], c=1.0):
        self.N = N
        self.M = M
        self.it2fs = it2fs
        self.Bounds = Bounds
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params
        self.c = c
        self.paramNum = M * (3 * N + 3)
        self.params = rand(self.paramNum, )
        self.Bounds = [Bounds, ] * self.paramNum
        self.model = IT2Mamdani_ML_Model(self.params, self.N, self.M, self.it2fs, self.c)
    

    def error(self, P, X, y):
        model = IT2Mamdani_ML_Model(P, self.N, self.M, self.it2fs, self.c)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model(x)
        return norm(y - o)
    

    def fit(self, X, y):
        if self.algorithm == "DE":
            self.params = differential_evolution(self.error, bounds=self.Bounds, 
                                            args=(X, y), disp=True).x
        elif self.algorithm == "Nelder-Mead":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "Powell":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, bounds=self.Bounds, 
                              options={"disp":True, }).x
        elif self.algorithm == "CG":
            self.params = minimize(self.error, self.params, args=(X, y), 
                              method=self.algorithm, 
                              options={"disp":True, }).x
        elif self.algorithm == "PSO":
            myPSO = PSO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4])
                print("Iteration ", i+1, ".", myPSO.fb)
            self.params = myPSO.xb
        elif self.algorithm == "GA":
            myGA = GA(self.algorithm_params[0], self.paramNum, self.error, 
                      self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                myGA.iterate(self.algorithm_params[2], 
                             self.algorithm_params[3], 
                             self.algorithm_params[4], )
                print("Iteration ", i+1, ".", myGA.population[0].fitness)
            self.params = myGA.population[0].solution
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
        self.model = IT2Mamdani_ML_Model(self.params, self.N, self.M, self.it2fs, self.c)
        return self.error(self.params, X, y)
    

    def score(self, X):
        X = asarray(X)
        if X.ndim == 1:
            return self.model(X)
        elif X.ndim == 2:
            o = []
            for x in X:
                o.append(self.model(x))
            return array(o)
        else:
            raise ValueError("Input must be a 1D or 2D NumPy array!")


class IT2TSK_SI_Model:

    def __init__(self, ):
        pass


class IT2TSK_SI:

    def __init__(self, ):
        pass

    def __call__(self, ):
        pass




