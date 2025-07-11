#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 01:39:58 2024

@author: arslan
"""

from numpy import (reshape, exp, array, zeros, zeros_like, asarray, linspace, 
                   concatenate, abs, clip, argsort, argmin, sqrt, sin, 
                   pi, copy, argmax, vstack, ones, mean, delete, where, append, sort, )
from numpy.linalg import (norm, )
from numpy.random import (rand, randint, uniform, normal, choice, )
from scipy.optimize import (differential_evolution, minimize, )
from pyit2fls import (T1FS, gaussian_mf, T1Mamdani, T1TSK, 
                      IT2FS_Gaussian_UncertMean, IT2FS_Gaussian_UncertStd, 
                      IT2Mamdani, IT2TSK, product_t_norm, max_s_norm, crisp, )
from abc import ABC, abstractmethod


class Optimizer(ABC):
    """
    Abstract base class for optimizers.
    """

    def __init__(self, population_size, solution_size, objective_function, bounds, args=None):
        self.population_size = population_size
        self.solution_size = solution_size
        self.objective_function = objective_function
        self.bounds = bounds
        self.args = args if args is not None else {}
        super().__init__()
        self.best_solution = zeros((self.solution_size, ), )
        self.best_fitness = self.objective_function(self.best_solution, *args)

    @abstractmethod
    def iterate(self, algorithm_parameters):
        pass


class ICA:
    """Imperialist Competitive Algorithm (ICA) for determining optimal parameters of fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        population_size : int

            Number of countries (solutions) in the population.
        
        solution_size : int

            Number of parameters constructing each country.
        
        objective_function : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *objective_function*.
    
        .. rubric:: Functions
            
        Functions defined in ICA class:

        iterate:

            Advances the ICA by one iteration.

        get_best_solution:

            Finds the best solution (country) in the current population.
    """
    def __init__(self, population_size, solution_size, objective_function, bounds, args=None):
        """
        Initializes the ICA class with the given parameters.

        .. rubric:: Parameters

        population_size : int

            Number of countries (solutions) in the population.
        
        solution_size : int

            Number of parameters constructing each country.
        
        objective_function : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *objective_function*.
        """
        self.population_size = population_size
        self.solution_size = solution_size
        self.objective_function = objective_function
        self.bounds = bounds
        self.args = args if args is not None else {}

        # Initialize countries (solutions) randomly within bounds
        self.countries = zeros((self.population_size, self.solution_size, ), )
        self.fitness = zeros((self.population_size, ), )
        
        for i in range(self.population_size):
            self.countries[i] = uniform(low=self.bounds[0], high=self.bounds[1], size=(self.solution_size, ), )
            try:
                self.fitness[i] = self.objective_function(self.countries[i], *self.args)
            except IndexError:
                self.fitness[i] = float("inf")

        # Select imperialists and colonies
        self.imperialist_indices = argsort(self.fitness)[:self.population_size // 3]  # Example: 1/3 are imperialists
        self.colony_indices = argsort(self.fitness)[self.population_size // 3:]

        self.get_best_solution()

    def iterate(self, assimilation_coefficient=2, revolution_rate=0.1):
        """Advances the ICA by one iteration.

            .. rubric:: Parameters

            assimilation_coefficient : float

                Coefficient controlling the movement of colonies towards their imperialist.
            
            revolution_rate : float

                Probability of a colony randomly changing its position.
        """
        # Assimilation: Colonies move towards their imperialist
        for colony_index in self.colony_indices:
            imperialist_index = self.imperialist_indices[colony_index % len(self.imperialist_indices)]  # Assign to an imperialist
            difference = self.countries[imperialist_index] - self.countries[colony_index]
            self.countries[colony_index] += uniform(0, assimilation_coefficient) * difference
            try:
                self.fitness[colony_index] = self.objective_function(self.countries[colony_index], *self.args)
            except IndexError:
                self.fitness[colony_index] = float("inf")

        # Revolution: Some colonies randomly change their position
        for colony_index in self.colony_indices:
            if rand() < revolution_rate:
                self.countries[colony_index] = uniform(low=self.bounds[0], high=self.bounds[1], size=self.solution_size)
                try:
                    self.fitness[colony_index] = self.objective_function(self.countries[colony_index], *self.args)
                except IndexError:
                    self.fitness[colony_index] = float("inf")

        # Imperialistic Competition: Select the weakest empire
        weakest_empire_index = argmax([mean(self.fitness[self.colony_indices[self.colony_indices % len(self.imperialist_indices) == i]]) for i in range(len(self.imperialist_indices))])
        weakest_imperialist_index = self.imperialist_indices[weakest_empire_index]

        # Move the weakest colony to the best empire
        best_empire_index = argmin([mean(self.fitness[self.colony_indices[self.colony_indices % len(self.imperialist_indices) == i]]) for i in range(len(self.imperialist_indices))])
        if best_empire_index != weakest_empire_index:
            weakest_colony_index = self.colony_indices[argmax(self.fitness[self.colony_indices[self.colony_indices % len(self.imperialist_indices) == weakest_empire_index]])]
            self.imperialist_indices[weakest_empire_index] = weakest_colony_index
            self.colony_indices = delete(self.colony_indices, where(self.colony_indices == weakest_colony_index)[0])
            self.colony_indices = append(self.colony_indices, weakest_imperialist_index)
            self.imperialist_indices = sort(self.imperialist_indices)
            self.colony_indices = sort(self.colony_indices)

        # Update fitness and re-sort
        for i in range(self.population_size):
            try:
                self.fitness[i] = self.objective_function(self.countries[i], *self.args)
            except IndexError:
                self.fitness[i] = float("inf")
        self.imperialist_indices = argsort(self.fitness)[:len(self.imperialist_indices)]
        self.colony_indices = argsort(self.fitness)[len(self.imperialist_indices):]

        self.get_best_solution()
        return self.best_fitness

    def get_best_solution(self):
        """Finds the best solution (country) in the current population."""
        best_index = argmin(self.fitness)
        self.best_country = self.countries[best_index]
        self.best_fitness = self.fitness[best_index]


class CuckooSearch:
    """Cuckoo Search (CS) for determining optimal parameters of fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        population_size : int

            Number of nests (solutions) in the population.
        
        solution_size : int

            Number of parameters constructing each solution.
        
        objective_function : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *objective_function*.
    
        .. rubric:: Functions
            
        Functions defined in CuckooSearch class:

        iterate:

            Advances the Cuckoo Search by one iteration.
    """
    def __init__(self, population_size, solution_size, objective_function, bounds, args=None):
        """
        Initializes the CuckooSearch class with the given parameters.

        .. rubric:: Parameters

        population_size : int

            Number of nests (solutions) in the population.
        
        solution_size : int

            Number of parameters constructing each solution.
        
        objective_function : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *objective_function*.
        """
        self.population_size = population_size
        self.solution_size = solution_size
        self.objective_function = objective_function
        self.bounds = bounds
        self.args = args if args is not None else {}  # Handle cases with no extra arguments

        # Initialize nests (solutions) randomly within bounds
        self.nests = zeros((self.population_size, self.solution_size, ), )
        self.fitness = zeros((self.population_size, ), )
        for i in range(self.population_size):
            self.nests[i] = uniform(low=self.bounds[0], high=self.bounds[1], size=(self.solution_size, ))
            try:
                self.fitness[i] = self.objective_function(self.nests[i], *args)
            except IndexError:
                self.fitness[i] = float("inf")
        
        self.get_best_solution()


    def iterate(self, pa=0.25, step_size_factor=0.01): # Example parameters
        """Advances the Cuckoo Search by one iteration.

            .. rubric:: Parameters

            pa : float

                Probability of abandoning a nest.
            
            step_size_factor : float

                Step size factor for Levy flight.
        """
        # Cuckoo search process
        for i in range(self.population_size):
            new_nest = self.get_cuckoo(self.nests[i], step_size_factor)
            try:
                new_fitness = self.objective_function(new_nest, *self.args)
            except IndexError:
                new_fitness = float("inf")
            j = randint(0, self.population_size)
            if new_fitness < self.fitness[j]:
                self.nests[j] = new_nest
                self.fitness[j] = new_fitness
                
        for i in range(self.population_size):
            if rand() < pa:
                self.nests[i] = uniform(low=self.bounds[0], high=self.bounds[1], size=self.solution_size)
                try:
                    self.fitness[i] = self.objective_function(self.nests[i], *self.args)  # Recalculate fitness
                except IndexError:
                    self.fitness[i] = float("inf")
        
        self.get_best_solution()
        return self.best_fitness


    def get_cuckoo(self, nest, step_size_factor):
        """Generates a new solution using Levy flight.

            .. rubric:: Parameters

            nest : numpy array

                Current solution (nest).
            
            step_size_factor : float

                Step size factor for Levy flight.
        """
         # Levy flight (simplified)
        u = normal(0, 1, self.solution_size)
        v = normal(0, 1, self.solution_size)
        step_size = step_size_factor * u / abs(v)**(1/3) # Example Levy step
        new_nest = nest + step_size
        return new_nest

    def get_best_solution(self):
        """Finds the best solution (nest) in the current population."""
        best_index = argmin(self.fitness)
        self.best_nest = self.nests[best_index]
        self.best_fitness = self.fitness[best_index]
        

class FFA:
    """Firefly Algorithm (FFA) for determining optimal parameters of fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        population : int

            Number of fireflies in the population.
        
        param_num : int

            Number of parameters constructing each firefly.
        
        obj_func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *obj_func*.
    
        .. rubric:: Functions
            
        Functions defined in FFA class:

        iterate:

            Advances the FFA by one iteration.
    """
    def __init__(self, population, param_num, obj_func, bounds, args=()):
        """
        Initializes the FFA class with the given parameters.

        .. rubric:: Parameters

        population : int

            Number of fireflies in the population.
        
        param_num : int

            Number of parameters constructing each firefly.
        
        obj_func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *obj_func*.
        """
        self.population = population
        self.param_num = param_num
        self.bounds = bounds
        self.obj_func = obj_func
        self.args = args
        self.fireflies = uniform(bounds[0], bounds[1], (population, param_num))
        
        self.fitness = []
        for firefly in self.fireflies:
            try:
                self.fitness.append(self.obj_func(firefly, *args))
            except IndexError:
                self.fitness.append(float("inf"))
        
        best_index = argmin(self.fitness)
        self.best_firefly = self.fireflies[best_index]
        self.best_fitness = self.fitness[best_index]

    def iterate(self, alpha, beta0, gamma):
        """Advances the FFA by one iteration.

            .. rubric:: Parameters

            alpha : float

                Randomization parameter controlling the randomness of the movement.
            
            beta0 : float

                Attractiveness at distance zero.
            
            gamma : float

                Light absorption coefficient controlling the decrease in attractiveness with distance.
        """
        for i in range(self.population):
            for j in range(self.population):
                if self.fitness[j] < self.fitness[i]:
                    r = norm(self.fireflies[i] - self.fireflies[j])
                    beta = beta0 * exp(-gamma * r ** 2)
                    new_position = self.fireflies[i] + beta * (self.fireflies[j] - self.fireflies[i]) + \
                                   alpha * (rand(self.param_num) - 0.5)
                    
                    try:
                        fitness = self.obj_func(new_position, *self.args)
                    except IndexError:
                        fitness = float("inf")
                    
                    if fitness < self.fitness[i]:
                        self.fireflies[i] = new_position
                        self.fitness[i] = fitness
        best_index = argmin(self.fitness)
        self.best_firefly = self.fireflies[best_index]
        self.best_fitness = self.fitness[best_index]
        return self.best_fitness


class WOA:
    """Whale Optimization Algorithm (WOA) for determining optimal parameters of fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        population : int

            Number of whales in the population.
        
        param_num : int

            Number of parameters constructing each whale.
        
        obj_func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *obj_func*.
    
        .. rubric:: Functions
            
        Functions defined in WOA class:

        iterate:

            Advances the WOA by one iteration.
    """
    def __init__(self, population, param_num, obj_func, bounds, args=()):
        """
        Initializes the WOA class with the given parameters.

        .. rubric:: Parameters

        population : int

            Number of whales in the population.
        
        param_num : int

            Number of parameters constructing each whale.
        
        obj_func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *obj_func*.
        """
        self.population = population
        self.param_num = param_num
        self.bounds = bounds
        self.obj_func = obj_func
        self.args = args
        self.whales = zeros((population, param_num, ), )
        self.fitness = zeros((population, ))
        for i in range(self.population):
            self.whales[i] = uniform(self.bounds[0], self.bounds[1], self.param_num)
            try:
                self.fitness[i] = self.obj_func(self.whales[i], *args)
            except IndexError:
                self.fitness[i] = float("inf")

        best_index = argmin(self.fitness)
        self.best_whale = self.whales[best_index]
        self.best_fitness = self.fitness[best_index]

    def iterate(self, t, max_iter):
        """Advances the WOA by one iteration.

            .. rubric:: Parameters

            t : int

                Current iteration number.
            
            max_iter : int

                Maximum number of iterations.
        """
        a = 2 - 2 * t / max_iter  # Linearly decreasing from 2 to 0
        for i in range(self.population):
            r1, r2 = rand(), rand()
            A = 2 * a * r1 - a
            C = 2 * r2
            p = rand()

            if p < 0.5:
                if abs(A) < 1:
                    D = abs(C * self.best_whale - self.whales[i])
                    new_position = self.best_whale - A * D
                else:
                    rand_whale = self.whales[randint(0, self.population)]
                    D = abs(C * rand_whale - self.whales[i])
                    new_position = rand_whale - A * D
            else:
                l = uniform(-1, 1)
                new_position = self.best_whale + l * abs(self.best_whale - self.whales[i])

            try:
                fitness = self.obj_func(new_position, *self.args)
            except IndexError:
                fitness = float("inf")
            
            if fitness < self.fitness[i]:
                self.whales[i] = new_position
                self.fitness[i] = fitness

        best_index = argmin(self.fitness)
        self.best_whale = self.whales[best_index]
        self.best_fitness = self.fitness[best_index]
        return self.best_fitness


class GWO:
    """Grey Wolf Optimizer (GWO) for determining optimal parameters of fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        population : int

            Number of wolves in the population.
        
        param_num : int

            Number of parameters constructing each wolf.
        
        obj_func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *obj_func*.
    
        .. rubric:: Functions
            
        Functions defined in GWO class:

        iterate:

            Advances the GWO by one iteration.
    """
    def __init__(self, population, param_num, obj_func, bounds, args=()):
        """
        Initializes the GWO class with the given parameters.

        .. rubric:: Parameters

        population : int

            Number of wolves in the population.
        
        param_num : int

            Number of parameters constructing each wolf.
        
        obj_func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *obj_func*.
        """
        self.population = population
        self.param_num = param_num
        self.bounds = bounds
        self.obj_func = obj_func
        self.args = args
        self.alpha, self.beta, self.delta = None, None, None
        self.alpha_fitness, self.beta_fitness, self.delta_fitness = float("inf"), float("inf"), float("inf")
        self.wolves = zeros((self.population, self.param_num, ), )
        self.fitness = zeros((self.population, ))
        for i in range(self.population):
            self.wolves[i] = uniform(self.bounds[0], self.bounds[1], self.param_num)
            try:
                self.fitness[i] = self.obj_func(self.wolves[i], *args)
            except IndexError:
                self.fitness[i] = float("inf")
        self._update_leaders()

    def _update_leaders(self):
        """
        Updates the alpha, beta, and delta wolves based on their fitness values.
        """
        sorted_indices = argsort(self.fitness)
        self.alpha = self.wolves[sorted_indices[0]]
        self.alpha_fitness = self.fitness[sorted_indices[0]]
        self.beta = self.wolves[sorted_indices[1]]
        self.beta_fitness = self.fitness[sorted_indices[1]]
        self.delta = self.wolves[sorted_indices[2]]
        self.delta_fitness = self.fitness[sorted_indices[2]]

    def iterate(self, t, max_iter):
        """Advances the GWO by one iteration.

            .. rubric:: Parameters

            t : int

                Current iteration number.
            
            max_iter : int

                Maximum number of iterations.
        """
        a = 2 - 2 * (t + 1) / max_iter  # Linearly decreasing from 2 to 0
        for i in range(self.population):
            A1, A2, A3 = a * (2 * rand(self.param_num) - 1), \
                         a * (2 * rand(self.param_num) - 1), \
                         a * (2 * rand(self.param_num) - 1)
            C1, C2, C3 = 2 * rand(self.param_num), 2 * rand(self.param_num), 2 * rand(self.param_num)

            X1 = self.alpha - A1 * abs(C1 * self.alpha - self.wolves[i])
            X2 = self.beta - A2 * abs(C2 * self.beta - self.wolves[i])
            X3 = self.delta - A3 * abs(C3 * self.delta - self.wolves[i])

            newPosition = (X1 + X2 + X3) / 3
            
            try:
                fitness = self.obj_func(newPosition, *self.args)
            except IndexError:
                fitness = float("inf")

            if fitness < self.fitness[i]:
                self.wolves[i] = newPosition
                self.fitness[i] = fitness

        self._update_leaders()
        return self.alpha_fitness



class PSO:
    """Particle Swarm Optimization (PSO) for determining optimal parameters of fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        N : int

            Number of particles in the swarm.
        
        M : int

            Number of parameters constructing each particle.
        
        func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *func*.
    
        .. rubric:: Functions
            
        Functions defined in PSO class:

        iterate:

            Advances the PSO by one iteration.
    """
    def __init__(self, N, M, func, bounds, args=()):
        """
        Initializes the PSO class with the given parameters.

        .. rubric:: Parameters

        N : int

            Number of particles in the swarm.
        
        M : int

            Number of parameters constructing each particle.
        
        func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *func*.
        """
        self.func = func
        self.args = args
        self.N  = N
        self.M  = M
        self.bounds = bounds
        self.X  = self.bounds[0] + (self.bounds[1] - self.bounds[0]) * rand(self.N, self.M)
        self.V  = 4.0 * (self.bounds[1] - self.bounds[0]) * (rand(self.N, self.M) - 0.5)
        self.Xb = self.X.copy()
        self.Fb = zeros(shape=(self.N, ))
        
        try:
            self.Fb[0] = self.func(self.X[0], *self.args)
        except IndexError:
            self.Fb[0] = float("inf")
        
        self.xb = self.X[0].copy()
        self.fb = self.Fb[0]
        
        self.iterNum = 0
        
        for i in range(1, self.N):
            try:
                self.Fb[i] = self.func(self.X[i], *self.args)
            except IndexError:
                self.Fb[i] = float("inf")
                
            if self.Fb[i] < self.fb:
                self.fb = self.Fb[i]
                self.xb = self.X[i].copy()
    
    
    def iterate(self, omega=0.3, phi_p=0.3, phi_g=2.1):
        """Advances the PSO by one iteration.

            .. rubric:: Parameters

            omega : float

                Inertia weight controlling the influence of the previous velocity.
            
            phi_p : float

                Cognitive coefficient controlling the influence of the particle's best-known position.
            
            phi_g : float

                Social coefficient controlling the influence of the global best-known position.
        """
        self.iterNum += 1
        r_p = rand(self.N, self.M)
        r_g = rand(self.N, self.M)
        self.V = omega * self.V + \
                 phi_p * r_p * (self.Xb - self.X) + \
                 phi_g * r_g * (self.xb - self.X)
        self.X = self.X + self.V
        
        for i in range(self.N):
            try:
                tmp = self.func(self.X[i], *self.args)
            except IndexError:
                continue
            if tmp < self.Fb[i]:
                self.Xb[i] = self.X[i].copy()
                self.Fb[i] = tmp
                if tmp < self.fb:
                    self.xb = self.X[i].copy()
                    self.fb = tmp
        return self.fb
            

class solution:
    
    def __init__(self, M, func, bounds, args=()):
        self.solution = bounds[0] + (bounds[1] - bounds[0]) * rand(M, )
        try:
            self.fitness = func(self.solution, *args)
        except IndexError:
            self.fitness = float("inf")

class GA:
    """Genetic Algorithm (GA) for determining optimal parameters of the fuzzy models.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        N : int

            Number of individuals in the population.
        
        M : int

            Number of parameters constructing each individual.
        
        func : function

            Objective function of the minimizing optimization problem.
        
        bounds : iterable

            Lower and upper bounds of the parameters of the optimization problem solutions.
        
        args : tuple

            The extra arguments that can be passed while calling the objective function, *func*.
    
        .. rubric:: Functions
            
        Functions defined in GA class:

        tournament_selection:

            Returns a list of *num* indices of individuals selected using the tournament selection method 
            among *tp* top percent of the individuals in the population.

        mutate:

            Applies the mutation operator on a specific individual.

        crossover:

            Produces an offspring using two individuals selected from the population.

        iterate:

            Advances the GA by one iteration.
    """
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
        """Returns a list of *num* indices of individuals selected using the tournament selection method 
            among *tp* top percent of the individuals in the population.

            .. rubric:: Parameters

            num : int

                The needed number of indices.
            
            tp : float

                A specific percent of population that selection would be among them.
        """
        high = int(self.N * tp)
        return [i1 if self.population[i1].fitness < self.population[i2].fitness else i2 
                for i1, i2 in zip(randint(high, size=num), randint(high, size=num))]
    
    
    def mutate(self, individual):
        """Applies the mutation operator on a specific individual.

            .. rubric:: Parameters

            individual : object of type *solution*

                The individual that the mutation would be applied on it.
        """
        transfer_vector = (self.bounds[1] - self.bounds[0]) * (rand(self.M) - 0.5) / (self.iterNum + 1.)
        return individual.solution.copy() + transfer_vector
    
    def crossover(self, parent1, parent2):
        """Produces an offspring using two individuals selected from the population.

            .. rubric:: Parameters

            parent1 : object of type *solution*

                The first parent for producing the offspring.

            parent2 : object of type *solution*

                The second parent for producing the offspring.
        """
        a = rand(self.M)
        b = rand(self.M)
        return (a * parent1.solution.copy() + b * parent2.solution.copy()) / (a + b)
    
    def iterate(self, mutation_num, crossover_num, tp):
        """Advances the GA by one iteration.

            .. rubric:: Parameters

            mutation_num : int

                The number of mutation operations that would be applied in each iteration.

            crossover_num : int

                The number of crossover operations that would be applied in each iteration.

            tp : float

                The implemented genetic algorithm (GA) applies the mutation and crossover operators 
                exclusively to the elite subset of the population, which represents the fitter 
                solutions. The parameter *tp* defines the elite group as the fraction 0 < *tp* < 1 
                of the population comprising individuals with superior fitness.
        """
        parent_list = self.tournament_selection(2 * crossover_num, 1.0)
        for i, j in zip(parent_list[::2], parent_list[1::2]):
            child_solution = self.crossover(self.population[i], self.population[j])
            try:
                tmp = self.func(child_solution, *self.args)
            except IndexError:
                continue
            if tmp < self.population[i].fitness:
                self.population[i].solution = child_solution.copy()
                self.population[i].fitness = tmp
            elif tmp < self.population[j].fitness:
                self.population[j].solution = child_solution.copy()
                self.population[j].fitness = tmp
        parent_list = self.tournament_selection(mutation_num, tp)
        for i in parent_list:
            mutated_solution = self.mutate(self.population[i])
            try:
                tmp = self.func(mutated_solution, *self.args)
            except IndexError:
                continue
            if tmp < self.population[i].fitness:
                self.population[i].solution = mutated_solution.copy()
                self.population[i].fitness = tmp
        
        self.population = sorted(self.population, key=lambda solution:solution.fitness)
        self.iterNum += 1
        return self.population[0].fitness


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
    """
    A general type fuzzy model for learning from data. *T1Mamdani_ML* and *T1TSK_ML* classes are build up based 
    on this class and they only help to provide a linguistic interpretation of the results by the *T1Fuzzy_ML* 
    class.

    .. rubric:: Parameters
    
    Parameters of the constructor function:

    N : int

        The inputs number of the model.
    
    M : int

        The rules number of the model.
    
    Bounds : tuple of float

        The upper and lower bounds of the parameters of the model.
    
    algorithm : str

        Indicates the algorithm to be used for determining the model parameters. It should be one 
        of the strings "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", "ICA". 
        The first four algorithms, which are based on scipy, are not computationally efficient. 
        So, we have provided embedded GA and PSO algorithms for calculating model parameters by 
        optimizing an error function. The users can write their own heuristic optimization solvers as 
        a subclass of Optimizer class.

    algorithm_params : list of numbers

        The parameters of the selected algorithm. For more details refer to each algorithm's documentations.
    
    .. rubric:: Functions

    Functions defined in T1Fuzzy_ML class:

        error : The error function utilized for parameter optimization of the model.

        fit : Fits the model based on the given input output data.

        score : Evaluates the model for desired input data.

    """
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
        """
        The error function for optimizing the model parameters.

        .. rubric:: Parameters

        P : list of float or numpy (n,) shaped array

            P provides the list of parameters which the model error would be evaluated 
            based on it.

        X : list of 1D numpy array or 2D numpy array

            X is the set of data which the model error would be evaluated for them.
        
        y : list of float or numpy (n,) shaped array

            y is the set of desired outputs which the model error would be evaluated based on them.
        """
        model = T1Fuzzy_ML_Model(P, self.N, self.M, 
                                 [[self.mf, ] * self.N, ] * self.M)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model.d0(x)
        return norm(y - o)

    def fit(self, X, y):
        """
        Function for finding the best set of parameters fitting the pair of input and output data.

        .. rubric:: Parameters

        X : 

            X is the set of data which the model error would be evaluated for them.

        y : 

            y is the set of desired outputs which the model error would be evaluated based on them.

        """
        convergence = []
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
                convergence.append(
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4]))
                print(f"Iteration {i+1}", myPSO.fb)
            self.params = myPSO.xb
        elif self.algorithm == "GA":
            myGA = GA(self.algorithm_params[0], self.paramNum, self.error, 
                      self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myGA.iterate(self.algorithm_params[2], 
                             self.algorithm_params[3], 
                             self.algorithm_params[4], ))
                print(f"Iteration {i+1}.", myGA.population[0].fitness)
            self.params = myGA.population[0].solution
        elif self.algorithm == "GWO":
            myGWO = GWO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myGWO.iterate(i, self.algorithm_params[1], ))
                print("Iteration ", i+1, ".", myGWO.alpha_fitness)
            self.params = myGWO.alpha
        elif self.algorithm == "WOA":
            myWOA = WOA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myWOA.iterate(i, self.algorithm_params[1], ))
                print("Iteration ", i+1, ".", myWOA.best_fitness)
            self.params = myWOA.best_whale
        elif self.algorithm == "FFA":
            myFFA = FFA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myFFA.iterate(self.algorithm_params[2], self.algorithm_params[3], self.algorithm_params[4]))
                print("Iteration ", i+1, ".", myFFA.best_fitness)
            self.params = myFFA.best_firefly
        elif self.algorithm == "CSO":
            myCSO = CuckooSearch(self.algorithm_params[0], self.paramNum, self.error, 
                                 self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myCSO.iterate(self.algorithm_params[2], self.algorithm_params[3], ))
                print("Iteration ", i+1, ".", myCSO.best_fitness)
            self.params = myCSO.best_nest
        elif self.algorithm == "ICA":
            myICA = ICA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myICA.iterate(self.algorithm_params[2], self.algorithm_params[3]))
                print("Iteration ", i+1, ".", myICA.best_fitness)
            self.params = myICA.best_country
        elif issubclass(self.algorithm, Optimizer):
            myOpt = self.algorithm(self.algorithm_params[0], self.paramNum, self.error, 
                                   self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myOpt.iterate(self.algorithm_params))
                print("Iteration ", i+1, ".", myOpt.best_fitness)
            self.params = myOpt.best_solution
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
        self.model = T1Fuzzy_ML_Model(self.params, self.N, self.M, 
                                      [[self.mf, ] * self.N, ] * self.M)
        if len(convergence) > 0:
            return self.error(self.params, X, y), convergence
        else:
            return self.error(self.params, X, y)

    def score(self, X):
        """
        Function for evaluating the model output for desired set of inputs.

        .. rubric:: Parameters

        X : 
        
            X is the set of data which the model would be evaluated for them.

        """
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
    """Type-1 Mamdani Machine Learning (T1Mamdani_ML) for learning from data using Type-1 Mamdani fuzzy systems.

        This class extends the *T1Fuzzy_ML* class to provide a linguistic interpretation of the results by generating a Type-1 Mamdani fuzzy system based on the learned parameters.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        N : int

            The number of inputs to the fuzzy system.
        
        M : int

            The number of rules in the fuzzy system.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include "DE", "Nelder-Mead", "Powell", "CG", "PSO", and "GA", "GWO", "WOA", "FFA", "CSO", "ICA". 
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the chosen algorithm. Please refer to the documentations of the algorithms for more details.
    
        .. rubric:: Functions
            
        Functions defined in *T1Mamdani_ML* class:

        get_T1Mamdani:

            Generates a Type-1 Mamdani fuzzy system based on the learned parameters.
    """
    def __init__(self, N, M, Bounds=None, algorithm="DE", algorithm_params=[]):
        """
        Initializes the *T1Mamdani_ML* class with the given parameters.

        .. rubric:: Parameters

        N : int

            The number of inputs to the fuzzy system.
        
        M : int

            The number of rules in the fuzzy system.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include "DE", "Nelder-Mead", "Powell", "CG", "PSO", and "GA", "GWO", "WOA", "FFA", "CSO", "ICA". 
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the chosen algorithm. Please refer to the documentations of the algorithms for more details.
        """
        super().__init__(N, M, Bounds, algorithm, algorithm_params)
    
    def get_T1Mamdani(self, std=1., ):
        """
        Generates a Type-1 Mamdani fuzzy system based on the learned parameters.

        .. rubric:: Parameters

        std : float

            The standard deviation for the Gaussian membership functions used in the fuzzy system.

        .. rubric:: Returns

        T1Mamdani:

            A Type-1 Mamdani fuzzy system generated based on the learned parameters.
        """
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
    """Type-1 TSK Machine Learning (T1TSK_ML) for learning from data using Type-1 Takagi-Sugeno fuzzy systems.

        This class extends the *T1Fuzzy_ML* class to provide a linguistic interpretation of the results by generating a Type-1 TSK fuzzy system based on the learned parameters.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        N : int

            The number of inputs to the fuzzy system.
        
        M : int

            The number of rules in the fuzzy system.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include 
            "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", and "ICA".
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the chosen algorithm. Please refer to the documentations of the algorithms for more details.
    
        .. rubric:: Functions
            
        Functions defined in T1TSK_ML class:

        get_T1TSK:

            Generates a Type-1 TSK fuzzy system based on the learned parameters.
    """
    def __init__(self, N, M, Bounds=None, algorithm="DE", algorithm_params=[]):
        """
        Initializes the T1TSK_ML class with the given parameters.

        .. rubric:: Parameters

        N : int

            The number of inputs to the fuzzy system.
        
        M : int

            The number of rules in the fuzzy system.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", and "ICA".
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the chosen algorithm. Please refer to the documentations of the algorithms for more details.
        """
        super().__init__(N, M, Bounds, algorithm, algorithm_params)

    def get_T1TSK(self, std=1., ):
        """
        Generates a Type-1 TSK fuzzy system based on the learned parameters.

        .. rubric:: Parameters

        std : float

            The standard deviation for the Gaussian membership functions used in the fuzzy system.

        .. rubric:: Returns

        T1TSK:

            A Type-1 TSK fuzzy system generated based on the learned parameters.
        """
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


class Linear_System:
    """
    A class for representing linear systems.
    """
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
    
    def __call__(self, t, X, U):
        """
        Call self as a function.

        .. rubric:: Parameters
    
        Parameters of the function:

        t : float

            The time variable.

        X : numpy (n,) shaped array

            The system states at time t.

        U : function of t and X

            A function for calculating the system input(s) at time t and state X.
        """
        X = X.reshape((-1, 1))
        U_ = U(t, X)
        return (self.A @ X + self.B @ U_).flatten()
    
    def Y(self, t, X, U):
        """
        A function for calculating the system output based on the current time, systemstates, and system input(s).

        .. rubric:: Parameters
    
        Parameters of the function:

        t : float

            The time variable.

        X : numpy (n,) shaped array

            The system states at time t.

        U : function of t and X

            A function for calculating the system input(s) at time t and state X.
        """
        X = X.reshape((-1, 1))
        U_ = U(t, X)
        return (self.C @ X + self.D @ U_).flatten()

    def __repr__(self, ):
        return f"Linear system with\nA: {str(self.A)}\nB: {str(self.B)}\nC: {str(self.C)}\nD: {str(self.D)}"
    
    def __str__(self, ):
        return f"Linear system with\nA: {str(self.A)}\nB: {str(self.B)}\nC: {str(self.C)}\nD: {str(self.D)}"

    def __add__(self, other):
        """
        Simple element-wise addition for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : Linear_System

            The other linear system to be added.
        """
        try:
            return Linear_System(self.A + other.A, self.B + other.B, self.C + other.C, self.D + other.D)
        except:
            raise TypeError("Size inconsistency!")

    def __sub__(self, other):
        """
        Simple element-wise subtraction for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : Linear_System

            The other linear system to be subtracted.
        """
        try:
            return Linear_System(self.A - other.A, self.B - other.B, self.C - other.C, self.D - other.D)
        except:
            raise TypeError("Size inconsistency!")
    
    def __neg__(self, ):
        """
        Simple element-wise negation for all system matrices to form a new linear system. 
        """
        return Linear_System(-self.A, -self.B, -self.C, -self.D)

    def __mul__(self, other):
        """
        Simple element-wise multiplication for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : int or float

            The number to be multiplicated.
        """
        if isinstance(other, (int, float, )):
            return Linear_System(other * self.A, other * self.B, other * self.C, other * self.D)
        else:
            raise TypeError("Unsupported operand type for *!")
    
    def __rmul__(self, other):
        """
        Simple element-wise right-side multiplication for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : int or float

            The number to be multiplicated.
        """
        if isinstance(other, (int, float, )):
            return Linear_System(other * self.A, other * self.B, other * self.C, other * self.D)
        else:
            raise TypeError("Unsupported operand type for *!")
    
    def __truediv__(self, other):
        """
        Simple element-wise true division for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : int or float

            The number to be used in division.
        """
        if isinstance(other, (int, float, )):
            return Linear_System(self.A / other, self.B / other, self.C / other, self.D / other)
        else:
            raise TypeError("Unsupported operand type for /!")
    
    def __isub__(self, other):
        """
        Simple element-wise subtraction for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : Linear_System

            The other linear system to be subtracted.
        """
        try:
            return Linear_System(self.A - other.A, self.B - other.B, self.C - other.C, self.D - other.D)
        except:
            raise TypeError("Size inconsistency!")

    def __iadd__(self, other):
        """
        Simple element-wise addition for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : Linear_System

            The other linear system to be added.
        """
        try:
            return Linear_System(self.A + other.A, self.B + other.B, self.C + other.C, self.D + other.D)
        except:
            raise TypeError("Size inconsistency!")

    def __imul__(self, other):
        """
        Simple element-wise multiplication for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : int or float

            The number to be multiplicated.
        """
        if isinstance(other, (int, float, )):
            return Linear_System(other * self.A, other * self.B, other * self.C, other * self.D)
        else:
            raise TypeError("Unsupported operand type for *!")

    def __idiv__(self, other):
        """
        Simple element-wise division for all system matrices to form a new linear system. 

        .. rubric:: Parameters

        other : int or float

            The number to be used in division.
        """
        if isinstance(other, (int, float, )):
            return Linear_System(self.A / other, self.B / other, self.C / other, self.D / other)
        else:
            raise TypeError("Unsupported operand type for /!")


class T1_TS_Model:
    """
    Type-1 Takagi-Sugeno (T1_TS) fuzzy model.

    This class provides a faster but less general implementation of a Type-1 Takagi-Sugeno fuzzy model. 
    It requires low-level configurations for membership functions, parameters, and system rules.

    .. rubric:: Parameters

    Parameters of the constructor function:

    mfList : list of list of membership functions

        Membership functions describing each input of the TS system in each rule of 
        the rule base.

    mfParamsList : list of list of list of floats

        List of parameters corresponded with mmbership functions describing each input 
        of the TS system in each rule of the rule base.

    systemList : list of *Linear_System*

        List of antecedent of each rule as a linear system.

    R : int

        Number of the rules in the rule base of the system.

    N : int

        Number of the state variables of the systtem.

    M : int

        Number of the inputs of the system.

    P : int

        Number of the outputs of the system.
    
    .. rubric:: Functions

    d0 : 
        
        Computes the aggregated linear system based on the states.
    
    __call__ : 
        
        Evaluates the TS fuzzy system for a given time, state, and input.
    
    Y : 
        
        Computes the output of the fuzzy system for a given time, state, and input.


    """
    def __init__(self, mfList, mfParamsList, systemList, R, N, M, P):
        """
        Initializes the T1_TS_Model class with the given parameters.

        .. rubric:: Parameters

        mfList : list of list of membership functions

            Membership functions describing each input of the TS system in each rule of 
            the rule base.

        mfParamsList : list of list of list of floats

            List of parameters corresponded with mmbership functions describing each input 
            of the TS system in each rule of the rule base.

        systemList : list of Linear_System objects

            A list of linear systems representing the consequent of each rule in the fuzzy 
            system.

        R : int

            The number of rules in the fuzzy system.

        N : int

            The number of state variables of the system.

        M : int

            The number of inputs of the system.

        P : int

            The number of outputs of the system.
        """
        self.mfList = mfList
        self.mfParamsList = mfParamsList
        self.systemList = systemList
        self.R = R
        self.N = N
        self.M = M
        self.P = P
    
    def d0(self, d0x):
        """
        Computes the aggregated linear system based on the states.

        .. rubric:: Parameters

        d0x : numpy array

            The state variables for which the aggregated linear system will be computed.

        .. rubric:: Returns

        Linear_System:

            The aggregated linear system based on the states.
        """
        d = 0.
        n = Linear_System(zeros((self.N, self.N)), 
                          zeros((self.N, self.M)), 
                          zeros((self.P, self.N)), 
                          zeros((self.P, self.P)), )
        for l in range(self.R):
            s = 1.
            for i in range(self.N):
                s *= self.mfList[l][i](d0x[i], self.mfParamsList[l][i])
            n += self.systemList[l] * s
            d += s
        return n / d
    
    def __call__(self, t, X, U):
        """
        Evaluates the fuzzy system for a given time, state, and input.

        .. rubric:: Parameters

        t : float

            The time variable.

        X : numpy array

            The state variables of the system.

        U : function

            A function representing the system inputs as a function of time and state.

        .. rubric:: Returns

        numpy array:

            The evaluated state derivatives of the fuzzy system.
        """
        ts = self.d0(X)
        return ts(t, X, U)

    def Y(self, t, X, U):
        """
        Computes the output of the TS system for a given time, state, and input.

        .. rubric:: Parameters

        t : float

            The time variable.

        X : numpy array

            The state variables of the system.

        U : function

            A function representing the system inputs as a function of time and state.

        .. rubric:: Returns

        numpy array:

            The output of the TS system.
        """
        ts = self.d0(X)
        return ts.Y(t, X, U)


class IT2TSK_ML_Model:
    """Interval Type-2 TSK Model for representing and evaluating interval type-2 fuzzy TSK systems in machine learning applications.

        This class implements an interval type-2 fuzzy TSK model using Gaussian membership functions with uncertainty in either the mean or the standard deviation.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        P : list of floats or numpy array

            The parameters of the model, including antecedent and consequent parameters.

        N : int

            The number of inputs to the fuzzy system.

        M : int

            The number of rules in the fuzzy system.

        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.

        c : float

            Output scaling factor for the model.
    
        .. rubric:: Functions
            
        Functions defined in IT2TSK_ML_Model class:

        __call__:

            Evaluates the fuzzy system for a given input.
    """
    def __init__(self, P, N, M, it2fs, c=1.0):
        """
        Initializes the IT2TSK_ML_Model class with the given parameters.

        .. rubric:: Parameters

        P : list of floats or numpy array

            The parameters of the model, including antecedent and consequent parameters.

        N : int

            The number of inputs to the fuzzy system.

        M : int

            The number of rules in the fuzzy system.

        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.

        c : float

            Output scaling factor for the model.
        """
        self.N = N
        self.M = M
        self.p = reshape(P[:-M], (M, N, 3, ))
        for i in range(M):
            for j in range(N):
                self.p[i][j][1] = abs(self.p[i][j][1])
                self.p[i][j][2] = abs(self.p[i][j][2])
        self.q = P[-M:]

        self.it2tsk = IT2TSK(product_t_norm, max_s_norm)
        for i in range(N):
            self.it2tsk.add_input_variable(f"X{i + 1}")
        self.it2tsk.add_output_variable("Y")

        self.it2fs = it2fs
        self.c = c
        
        for i in range(M):
            antecedent = []
            consequentDict = {"const":self.q[i], }
            for j in range(N):
                if it2fs == IT2FS_Gaussian_UncertMean:
                    std = max(self.p[i][j][1], self.p[i][j][2])
                elif it2fs == IT2FS_Gaussian_UncertStd:
                    std = self.p[i][j][1]
                else:
                    raise ValueError("You can use only IT2FS_Gaussian_UncertMean or IT2FS_Gaussian_UncertStd!")
                
                domain = linspace(self.p[i][j][0] - 5. * std, # 5 x std before mean
                                  self.p[i][j][0] + 5. * std, # 5 x std after mean
                                  max(100, int(10. * std * 10))) # 10 points for each unit
                antecedent.append((f"X{j + 1}", 
                                   it2fs(domain, params=[self.p[i][j][0], 
                                                         self.p[i][j][1], 
                                                         self.p[i][j][2], 
                                                         1.0]), ), )
                consequentDict[f"X{j + 1}"] = 0.
            
            consequent = [("Y", consequentDict)]
            self.it2tsk.add_rule(antecedent, consequent)

    def __call__(self, X):
        """
        Evaluates the fuzzy system for a given input.

        .. rubric:: Parameters

        X : numpy array

            The input data for which the fuzzy system will be evaluated.

        .. rubric:: Returns

        float:

            The output of the fuzzy system for the given input.
        """
        _X = {f"X{i + 1}":X[i] for i in range(self.N)}
        return self.it2tsk.evaluate(_X)["Y"]


class IT2TSK_ML:
    """Interval Type-2 TSK Machine Learning (IT2TSK_ML) for learning from data using interval type-2 fuzzy TSK systems.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        N : int

            Number of inputs to the model.
        
        M : int

            Number of rules in the fuzzy system.
        
        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. 
            It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include 
            "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", and "ICA". 
            Custom algorithms inheriting from the *Optimizer* class can also be used.
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the 
            chosen algorithm.
        
        c : float

            Output scaling factor for the model.
    
        .. rubric:: Functions
            
        Functions defined in IT2TSK_ML class:

        error:

            The error function used for optimizing the model parameters.

        fit:

            Fits the model to the given input-output data.

        score:

            Evaluates the model for a given set of inputs.
    """

    def __init__(self, N, M, it2fs, Bounds=None, algorithm="DE", algorithm_params=[], c=1.0):
        """
        Initializes the IT2TSK_ML class with the given parameters.

        .. rubric:: Parameters

        N : int

            Number of inputs to the model.
        
        M : int

            Number of rules in the fuzzy system.
        
        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. 
            It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include 
            "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", and "ICA". 
            Custom algorithms inheriting from the *Optimizer* class can also be used.
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the 
            chosen algorithm.
        
        c : float

            Output scaling factor for the model.
        """
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
        """
        The error function for optimizing the model parameters.

        .. rubric:: Parameters

        P : list of float or numpy (n,) shaped array

            The list of parameters for which the model error will be evaluated.

        X : list of 1D numpy arrays or 2D numpy array

            The input data for which the model error will be evaluated.
        
        y : list of float or numpy (n,) shaped array

            The desired outputs for which the model error will be evaluated.
        """
        model = IT2TSK_ML_Model(P, self.N, self.M, self.it2fs, self.c)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model(x)
        return norm(y - o)

    def fit(self, X, y):
        """
        Fits the model to the given input-output data.

        .. rubric:: Parameters

        X : list of 1D numpy arrays or 2D numpy array

            The input data for training the model.

        y : list of float or numpy (n,) shaped array

            The desired outputs for training the model.
        """
        convergence = []
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
                convergence.append(
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4]))
                print(f"Iteration {i+1}", myPSO.fb)
            self.params = myPSO.xb
        elif self.algorithm == "GA":
            myGA = GA(self.algorithm_params[0], self.paramNum, self.error, 
                      self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myGA.iterate(self.algorithm_params[2], 
                             self.algorithm_params[3], 
                             self.algorithm_params[4], ))
                print(f"Iteration {i+1}.", myGA.population[0].fitness)
            self.params = myGA.population[0].solution
        elif self.algorithm == "GWO":
            myGWO = GWO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myGWO.iterate(i, self.algorithm_params[1], ))
                print("Iteration ", i+1, ".", myGWO.alpha_fitness)
            self.params = myGWO.alpha
        elif self.algorithm == "WOA":
            myWOA = WOA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myWOA.iterate(i, self.algorithm_params[1], ))
                print("Iteration ", i+1, ".", myWOA.best_fitness)
            self.params = myWOA.best_whale
        elif self.algorithm == "FFA":
            myFFA = FFA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myFFA.iterate(self.algorithm_params[2], self.algorithm_params[3], self.algorithm_params[4]))
                print("Iteration ", i+1, ".", myFFA.best_fitness)
            self.params = myFFA.best_firefly
        elif self.algorithm == "CSO":
            myCSO = CuckooSearch(self.algorithm_params[0], self.paramNum, self.error, 
                                 self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myCSO.iterate(self.algorithm_params[2], self.algorithm_params[3], ))
                print("Iteration ", i+1, ".", myCSO.best_fitness)
            self.params = myCSO.best_nest
        elif self.algorithm == "ICA":
            myICA = ICA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myICA.iterate(self.algorithm_params[2], self.algorithm_params[3]))
                print("Iteration ", i+1, ".", myICA.best_fitness)
            self.params = myICA.best_country
        elif issubclass(self.algorithm, Optimizer):
            myOpt = self.algorithm(self.algorithm_params[0], self.paramNum, self.error, 
                                   self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myOpt.iterate(self.algorithm_params))
                print("Iteration ", i+1, ".", myOpt.best_fitness)
            self.params = myOpt.best_solution
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
        self.model = IT2TSK_ML_Model(self.params, self.N, self.M, self.it2fs, self.c)
        if len(convergence) > 0:
            return self.error(self.params, X, y), convergence
        else:
            return self.error(self.params, X, y)

    def score(self, X):
        """
        Evaluates the model for a given set of inputs.

        .. rubric:: Parameters

        X : list of 1D numpy arrays or 2D numpy array

            The input data for which the model will be evaluated.
        """
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
    """Interval Type-2 Mamdani Model for representing and evaluating interval type-2 Mamdani fuzzy systems in machine learning applications.

        This class implements an interval type-2 Mamdani fuzzy model using Gaussian membership functions with uncertainty in either the mean or the standard deviation for both antecedents and consequents.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        P : list of floats or numpy array

            The parameters of the model, including antecedent and consequent parameters.

        N : int

            The number of inputs to the fuzzy system.

        M : int

            The number of rules in the fuzzy system.

        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.

        c : float

            Output scaling factor for the model.
    
        .. rubric:: Functions
            
        Functions defined in IT2Mamdani_ML_Model class:

        __call__:

            Evaluates the fuzzy system for a given input and returns the defuzzified output.
    """
    def __init__(self, P, N, M, it2fs, c=1.0):
        """
        Initializes the IT2Mamdani_ML_Model class with the given parameters.

        .. rubric:: Parameters

        P : list of floats or numpy array

            The parameters of the model, including antecedent and consequent parameters.

        N : int

            The number of inputs to the fuzzy system.

        M : int

            The number of rules in the fuzzy system.

        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.

        c : float

            Output scaling factor for the model.
        """
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

        self.it2mamdani = IT2Mamdani(product_t_norm, max_s_norm)
        
        for i in range(N):
            self.it2mamdani.add_input_variable(f"X{i + 1}")
        self.it2mamdani.add_output_variable("Y")

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

            consequent = [("Y", it2fs(domain, params=[self.q[i][0], 
                                                      self.q[i][1], 
                                                      self.q[i][2], 
                                                      1.0]), ), ]
            self.it2mamdani.add_rule(antecedent, consequent)


    def __call__(self, X):
        """
        Evaluates the fuzzy system for a given input and returns the defuzzified output.

        .. rubric:: Parameters

        X : numpy array

            The input data for which the fuzzy system will be evaluated.

        .. rubric:: Returns

        float:

            The defuzzified output of the fuzzy system for the given input.
        """
        _X = {f"X{i + 1}":X[i] for i in range(self.N)}
        it2out, tr = self.it2mamdani.evaluate(_X)
        return crisp(tr["Y"])


class IT2Mamdani_ML:
    """Interval Type-2 Mamdani Machine Learning (IT2Mamdani_ML) for learning from data using interval type-2 Mamdani fuzzy systems.

        This class provides a framework for training interval type-2 Mamdani fuzzy systems using various optimization algorithms. It supports Gaussian membership functions with uncertainty in either the mean or the standard deviation for both antecedents and consequents.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        N : int

            The number of inputs to the fuzzy system.
        
        M : int

            The number of rules in the fuzzy system.
        
        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", and "ICA". Custom algorithms inheriting from the *Optimizer* class can also be used.
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the chosen algorithm.
        
        c : float

            Output scaling factor for the model.
    
        .. rubric:: Functions
            
        Functions defined in IT2Mamdani_ML class:

        error:

            The error function used for optimizing the model parameters.

        fit:

            Fits the model to the given input-output data.

        score:

            Evaluates the model for a given set of inputs.
    """

    def __init__(self, N, M, it2fs, Bounds=None, algorithm="DE", algorithm_params=[], c=1.0):
        """
        Initializes the IT2Mamdani_ML class with the given parameters.

        .. rubric:: Parameters

        N : int

            The number of inputs to the fuzzy system.
        
        M : int

            The number of rules in the fuzzy system.
        
        it2fs : class

            The interval type-2 fuzzy set class to be used for the antecedents and consequents. It should be either *IT2FS_Gaussian_UncertMean* or *IT2FS_Gaussian_UncertStd*.
        
        Bounds : tuple of float

            The lower and upper bounds for the parameters of the model.
        
        algorithm : str

            The optimization algorithm to be used for parameter learning. Supported algorithms include "DE", "Nelder-Mead", "Powell", "CG", "PSO", "GA", "GWO", "WOA", "FFA", "CSO", and "ICA". Custom algorithms inheriting from the *Optimizer* class can also be used.
        
        algorithm_params : list of numbers

            Parameters for the selected optimization algorithm. The required parameters depend on the chosen algorithm.
        
        c : float

            Output scaling factor for the model.
        """
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
        """
        The error function used for optimizing the model parameters.

        .. rubric:: Parameters

        P : list of float or numpy (n,) shaped array

            The list of parameters for which the model error will be evaluated.

        X : list of 1D or 2D numpy array

            The input data for which the model error will be evaluated.
        
        y : list of float or numpy (n,) shaped array

            The desired outputs for which the model error will be evaluated.

        .. rubric:: Returns

        float:

            The computed error value for the given parameters and data.
        """
        model = IT2Mamdani_ML_Model(P, self.N, self.M, self.it2fs, self.c)
        o = zeros_like(y)
        for i, x in zip(range(len(y)), X):
            o[i] = model(x)
        return norm(y - o)
    

    def fit(self, X, y):
        """
        Fits the model to the given input-output data using the selected optimization algorithm.

        .. rubric:: Parameters

        X : list of 1D or 2D numpy array

            The input data for training the model.

        y : list of float or numpy (n,) shaped array

            The desired outputs for training the model.

        .. rubric:: Returns

        float or tuple:

            The final error value after optimization, and optionally the convergence history.
        """
        convergence = []
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
                convergence.append(
                myPSO.iterate(self.algorithm_params[2], 
                              self.algorithm_params[3], 
                              self.algorithm_params[4]))
                print(f"Iteration {i+1}", myPSO.fb)
            self.params = myPSO.xb
        elif self.algorithm == "GA":
            myGA = GA(self.algorithm_params[0], self.paramNum, self.error, 
                      self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myGA.iterate(self.algorithm_params[2], 
                             self.algorithm_params[3], 
                             self.algorithm_params[4], ))
                print(f"Iteration {i+1}.", myGA.population[0].fitness)
            self.params = myGA.population[0].solution
        elif self.algorithm == "GWO":
            myGWO = GWO(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myGWO.iterate(i, self.algorithm_params[1], ))
                print("Iteration ", i+1, ".", myGWO.alpha_fitness)
            self.params = myGWO.alpha
        elif self.algorithm == "WOA":
            myWOA = WOA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myWOA.iterate(i, self.algorithm_params[1], ))
                print("Iteration ", i+1, ".", myWOA.best_fitness)
            self.params = myWOA.best_whale
        elif self.algorithm == "FFA":
            myFFA = FFA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myFFA.iterate(self.algorithm_params[2], self.algorithm_params[3], self.algorithm_params[4]))
                print("Iteration ", i+1, ".", myFFA.best_fitness)
            self.params = myFFA.best_firefly
        elif self.algorithm == "CSO":
            myCSO = CuckooSearch(self.algorithm_params[0], self.paramNum, self.error, 
                                 self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myCSO.iterate(self.algorithm_params[2], self.algorithm_params[3], ))
                print("Iteration ", i+1, ".", myCSO.best_fitness)
            self.params = myCSO.best_nest
        elif self.algorithm == "ICA":
            myICA = ICA(self.algorithm_params[0], self.paramNum, self.error, 
                        self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myICA.iterate(self.algorithm_params[2], self.algorithm_params[3]))
                print("Iteration ", i+1, ".", myICA.best_fitness)
            self.params = myICA.best_country
        elif issubclass(self.algorithm, Optimizer):
            myOpt = self.algorithm(self.algorithm_params[0], self.paramNum, self.error, 
                                   self.Bounds[0], args=(X, y, ))
            for i in range(self.algorithm_params[1]):
                convergence.append(
                myOpt.iterate(self.algorithm_params))
                print("Iteration ", i+1, ".", myOpt.best_fitness)
            self.params = myOpt.best_solution
        else:
            raise ValueError(self.algorithm + " algorithm is not supported!")
        
        self.model = IT2Mamdani_ML_Model(self.params, self.N, self.M, self.it2fs, self.c)
        if len(convergence) > 0:
            return self.error(self.params, X, y), convergence
        else:
            return self.error(self.params, X, y)
    

    def score(self, X):
        """
        Evaluates the model for a given set of inputs.

        .. rubric:: Parameters

        X : list of 1D or 2D numpy array

            The input data for which the model will be evaluated.

        .. rubric:: Returns

        float or numpy array:

            The model output(s) for the given input(s).
        """
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


class IT2_TS_Model:
    """Interval Type-2 Takagi-Sugeno (IT2_TS) fuzzy model.

        This class implements an interval type-2 Takagi-Sugeno fuzzy model, which uses lower and upper membership functions (LMFs and UMFs) to handle uncertainty in the system.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        lmfList : list of list of functions

            A list of membership functions (MFs) for the lower membership functions (LMFs) of each input in each rule of the fuzzy system.

        lmfParamsList : list of list of lists of floats

            A list of parameters corresponding to the lower membership functions (LMFs) for each input in each rule of the fuzzy system.

        umfList : list of list of functions

            A list of membership functions (MFs) for the upper membership functions (UMFs) of each input in each rule of the fuzzy system.

        umfParamsList : list of list of lists of floats

            A list of parameters corresponding to the upper membership functions (UMFs) for each input in each rule of the fuzzy system.

        systemList : list of *Linear_System* objects

            A list of linear systems representing the consequent of each rule in the fuzzy system.

        R : int

            The number of rules in the fuzzy system.

        N : int

            The number of state variables in the system.

        M : int

            The number of inputs to the systems.

        P : int

            The number of outputs of the systems.
    
        .. rubric:: Functions
            
        Functions defined in IT2_TS_Model class:

        d0:

            Computes the aggregated linear system based on the input membership function values.

        __call__:

            Evaluates the fuzzy system for a given time, state, and input.

        Y:

            Computes the output of the fuzzy system for a given time, state, and input.
    """
    def __init__(self, lmfList, lmfParamsList, umfList, umfParamsList, systemList, R, N, M, P):
        """
        Initializes the IT2_TS_Model class with the given parameters.

        .. rubric:: Parameters
            
        Parameters of the constructor function:

        lmfList : list of list of functions

            A list of membership functions (MFs) for the lower membership functions (LMFs) of each input in each rule of the fuzzy system.

        lmfParamsList : list of list of lists of floats

            A list of parameters corresponding to the lower membership functions (LMFs) for each input in each rule of the fuzzy system.

        umfList : list of list of functions

            A list of membership functions (MFs) for the upper membership functions (UMFs) of each input in each rule of the fuzzy system.

        umfParamsList : list of list of lists of floats

            A list of parameters corresponding to the upper membership functions (UMFs) for each input in each rule of the fuzzy system.

        systemList : list of *Linear_System* objects

            A list of linear systems representing the consequent of each rule in the fuzzy system.

        R : int

            The number of rules in the fuzzy system.

        N : int

            The number of state variables in the system.

        M : int

            The number of inputs to the systems.

        P : int

            The number of outputs of the systems.
        """
        self.lmfList = lmfList
        self.lmfParamsList = lmfParamsList
        self.umfList = umfList
        self.umfParamsList = umfParamsList
        self.systemList = systemList
        self.R = R
        self.N = N
        self.M = M
        self.P = P
    
    def d0(self, d0x):
        """
        Computes the aggregated linear system based on the states.

        .. rubric:: Parameters

        d0x : numpy array

            The state variables for which the aggregated linear system will be computed.

        .. rubric:: Returns

        Linear_System:

            The aggregated linear system based on the states.
        """
        d = 0.
        n = Linear_System(zeros((self.N, self.N)), 
                          zeros((self.N, self.M)), 
                          zeros((self.P, self.N)), 
                          zeros((self.P, self.P)), )
        for l in range(self.R):
            s1 = 1. # LMF
            s2 = 1. # UMF
            for i in range(self.N):
                s1 *= self.lmfList[l][i](d0x[i], self.lmfParamsList[l][i])
                s2 *= self.umfList[l][i](d0x[i], self.umfParamsList[l][i])
            n += self.systemList[l] * (s1 + s2)
            d += s1 + s2
        return n / d

    def __call__(self, t, X, U):
        """
        Evaluates the fuzzy system for a given time, state, and input.

        .. rubric:: Parameters

        t : float

            The time variable.

        X : numpy array

            The state variables of the system.

        U : function

            A function representing the system inputs as a function of time and state.

        .. rubric:: Returns

        numpy array:

            The evaluated state derivatives of the fuzzy system.
        """
        ts = self.d0(X)
        return ts(t, X, U)

    def Y(self, t, X, U):
        """
        Computes the output of the fuzzy system for a given time, state, and input.

        .. rubric:: Parameters

        t : float

            The time variable.

        X : numpy array

            The state variables of the system.

        U : function

            A function representing the system inputs as a function of time and state.

        .. rubric:: Returns

        numpy array:

            The output of the fuzzy system.
        """
        ts = self.d0(X)
        return ts.Y(t, X, U)






