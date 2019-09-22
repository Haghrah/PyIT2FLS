#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module implements ddeint, a simple Differential Delay Equation
solver built on top of Scipy's odeint
Created by @Zulko, https://github.com/Zulko/ddeint
Improved by @Haghrah, https://github.com/Haghrah/ddeint
"""
# REQUIRES Numpy and Scipy.
import numpy as np
import scipy.integrate
import scipy.interpolate

class ddeVar:
    """
    The instances of this class are special function-like
    variables which store their past values in an interpolator and
    can be called for any past time: Y(t), Y(t-d).
    Very convenient for the integration of DDEs.
    """

    def __init__(self,g,tc=0):
        """ g(t) = expression of Y(t) for t<tc """

        self.g = g
        self.tc= tc
        # We must fill the interpolator with 2 points minimum
        self.itpr = scipy.interpolate.interp1d(
            np.array([tc-1,tc]), # X
            np.array([self.g(tc),self.g(tc)]).T, # Y
            kind='linear', bounds_error=False,
            fill_value = self.g(tc))

    def update(self, t, Y):
        """ Add one new (ti,yi) to the interpolator """
        self.itpr.x = np.hstack([self.itpr.x, [t]])
        self.itpr.y = np.hstack([self.itpr.y, Y])
        self.itpr.fill_value = Y

    def __call__(self,t=0):
        """ Y(t) will return the instance's value at time t """
        return (self.g(t) if (t<self.tc) else self.itpr(t))


class ddeVars:
    
    def __init__(self, gs, tc=0):
        self.tc= tc
        self.n = len(gs)
        self.Vars = [ddeVar(g, tc) for g in gs]
    
    def update(self, t, Y):
        for i in range(self.n):
            self.Vars[i].update(t, Y[i])
    
    def __getitem__(self, key):
        return self.Vars[key]
        
    def __call__(self, t=0):
        return np.array([var(t) for var in self.Vars])


class dde(scipy.integrate.ode):
    """
    This class overwrites a few functions of ``scipy.integrate.ode``
    to allow for updates of the pseudo-variable Y between each
    integration step.
    """

    def __init__(self, f, jac=None):

        def f2(t,y,args):
            return f(self.Y, t, *args)
        scipy.integrate.ode.__init__(self, f2, jac)
        self.set_f_params(None)

    def integrate(self, t, step=0, relax=0):
        scipy.integrate.ode.integrate(self, t, step, relax)
        self.Y.update(self.t, self.y)
        return self.y

    def set_initial_value(self, Y):
        self.Y = Y #!!! Y will be modified during integration
        scipy.integrate.ode.set_initial_value(self, Y(Y.tc), Y.tc)


def ddeint(func, gs, tt, fargs=None):
    """ Solves Delay Differential Equations
    Similar to scipy.integrate.odeint. Solves a Delay differential
    Equation system (DDE) defined by
        Y(t) = g(t) for t<0
        Y'(t) = func(Y,t) for t>= 0
    Where func can involve past values of Y, like Y(t-d).
    
    Parameters
    -----------
    
    func
      a function Y,t,args -> Y'(t), where args is optional.
      The variable Y is an instance of class ddeVars (A class containing 
      a list of ddeVar objects). It's elements are called like a 
      function: Y[0](t), Y[0](t-d), etc. Each element of Y represents a 
      state variable which can have a different delay value. It must be 
      noticed that, Y[i](t) returns a number.
      
    gs
      The 'list of history functions'. A list of functions g(t) = Y[i](t) 
      for t<0, g(t) returns a number.
    
    tt
      The vector of times [t0, t1, ...] at which the system must
      be solved.
    fargs
      Additional arguments to be passed to parameter ``func``, if any.
    Examples
    ---------
    
    The delay ``d`` is a tunable parameter of the model.
    >>> import numpy as np
    >>> from ddeint import ddeint
    >>> 
    >>> def model(X, t, d):
    >>>     x = X[0](t)
    >>>     xd = X[0](t - d)
    >>>     y = X[1](t)
    >>>     yd = X[1](t - d)
    >>>     return array([0.5 * x * (1 - yd), -0.5 * y * (1 - xd)])
    >>> 
    >>> g1 = lambda t: 1 # 'history' at t<0 for x
    >>> g2 = lambda t: 2 # 'history' at t<0 for y
    >>> tt = np.linspace(0, 30, 20000) # times for integration
    >>> d = 0.5 # set parameter d 
    >>> yy = ddeint(model, [g1, g2], tt, fargs=(d,)) # solve the DDE !
     
    """

    dde_ = dde(func)
    dde_.set_initial_value(ddeVars(gs,tt[0]))
    dde_.set_f_params(fargs if fargs else [])
    results = [np.array([g(tt[0]) for g in gs])]
    results.extend(dde_.integrate(dde_.t + dt) for dt in np.diff(tt))
    return np.array(results)








