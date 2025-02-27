#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:11:43 2024

@author: arslan
"""

from numpy import (array, linspace, trapz, sin, cos,  
                   reshape, dot, sqrt, )
from numpy.random import (rand, )
from numpy.linalg import (inv, )
from scipy.integrate import (solve_ivp, )
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import (Rectangle, )
import multiprocessing
from pyit2fls import (T1TSK, T1FS, gaussian_mf, GA, PSO, )


def ITAE(X, t, dt):
    if len(X) != len(t):
        return float("inf")
    else:
        return trapz(sqrt(1.0 * X[:, 0] ** 2 + 1.0 * X[:, 1] ** 2 + 
                          4.0 * X[:, 2] ** 2 + 1.0 * X[:, 3] ** 2), dx=dt)

class CartPole:
    
    g = 9.8
    
    def __init__(self, M, m, l, I, b):
        self.M = M
        self.m = m
        self.l = l
        self.I = I
        self.b = b
    
    def __call__(self, t, X, u, p, N, M, ):
        dx1 = X[1]
        dx3 = X[3]
        A = array([[self.M + self.m            , self.m * self.l * cos(X[2])    , ], 
                   [self.m * self.l * cos(X[2]), (self.I + self.m * self.l ** 2), ], ])
        b = array([[u(t, X, p, N, M, ) + self.m * self.l * X[3] ** 2 * sin(X[2]) - self.b * X[1], ], 
                   [self.g * self.m * self.l * sin(X[2])                  , ], ])
        y = inv(A) @ b
        dx2 = y[0, 0]
        dx4 = y[1, 0]
        return array([dx1, dx2, dx3, dx4, ])

class IPAnimator:
    
    def animate(self, t, X, S, l):
        fig, ax = plt.subplots(figsize=(16, 4))
        ax.set_xlim([-5.0, 5.0])
        ax.set_ylim([-1.5, 1.5])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Animated output of the simulation")
        cart = Rectangle([X[0, 0] - 0.2, 0 - 0.05], 0.4, 0.1, facecolor='red')
        beam = ax.plot([X[0, 0], X[0, 0] + l * sin(X[0, 2])], 
                        [0.     , l * cos(X[0, 2])], linewidth=2)[0]
        ax.add_patch(cart)
        ax.grid(True)
        
        def update(frame):
            cart.set_xy([X[frame, 0] - 0.2, 0 - 0.05])
            beam.set_xdata([X[frame, 0], X[frame, 0] + l * sin(X[frame, 2])])
            beam.set_ydata([0., l * cos(X[frame, 2])])
            return cart
        
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=24, metadata=dict(artist='Amir Arslan Haghrah'),
                        extra_args=['-pix_fmt', 'yuv420p'])
        self.ani = animation.FuncAnimation(fig=fig, func=update, frames=len(t), interval=1000 * S)
        self.ani.save('cartPole.mp4', writer=writer)
        plt.show()

T1TSKCtrl = T1TSK()
T1TSKCtrl.add_input_variable("X1")
T1TSKCtrl.add_input_variable("X2")
T1TSKCtrl.add_input_variable("X3")
T1TSKCtrl.add_input_variable("X4")
T1TSKCtrl.add_output_variable("Y")
domain = linspace(-1.5, 1.5, 100)

def u(t, X, p, N, M):
    T1TSKCtrl.rules = []
    setsList = []
    for i in range(N * M):
        setsList.append(T1FS(domain, gaussian_mf, 
                             [p[2 * i], abs(p[2 * i + 1]), 1.]))
    rulesOutput = reshape(p[2 * N * M:], (M, N ), )
    for i, c in enumerate(rulesOutput):
        antecedent = []
        for j in range(N):
            antecedent.append((f"X{j+1}", setsList[i * N + j]))
        consequent = [("Y", lambda *Z : Z[0] * c[0] + Z[1] * c[1]
                                      + Z[2] * c[2] + Z[3] * c[3], ), ]
        T1TSKCtrl.add_rule(antecedent, consequent, )
    return T1TSKCtrl.evaluate({"X1":X[0], "X2":X[1], 
                               "X3":X[2], "X4":X[3], }, 
                              params=(X[0], X[1], 
                                      X[2], X[3]))["Y"]

def run_with_timeout(func, args, timeout):
    with multiprocessing.Pool(processes=1) as pool:
        result = pool.apply_async(func, args)
        try:
            return result.get(timeout)
        except multiprocessing.TimeoutError:
            pool.terminate()
            return float("inf")

if __name__ == "__main__":
    l = 1.0
    cartPole = CartPole(0.3, 0.2, l, 0.1, 0.006)
    T = 10.0
    S = 0.01
    t = linspace(0.0, T, int(T / S))
    L0 = 8 # Number of random initial conditions used in learning process
    X0 = 2.0 * (rand(L0, 4) - 0.5) * array([1.0, 1.0, 0.1, 1.0, ])
    timeOut = 0.5
    N = 4
    M = 16
    paramNum = M * (3 * N)
    
    def objectiveFunctionSingleITAE(p, N, M, k, ):
        return ITAE(solve_ivp(cartPole, [0., T], X0[k], args=(u, p, N, M, ), 
                              t_eval=t, dense_output=True, 
                              method="RK45").y.T, t, S)
    
    def objFuncSingleITAE(p, N, M, timeout, ):
        o = 0.
        for i in range(L0):
            o += run_with_timeout(objectiveFunctionSingleITAE, (p, N, M, i, ) , timeout)
        return o
    
    
    # mySolver = PSO(20, paramNum, objFuncSingleITAE, (0., 100.), args=(N, M, timeOut, ), )
    # for i in range(25):
    #     mySolver.iterate(omega=0.3, phi_g=0.3, phi_p=2.1)
    #     print(f"Ite {i + 1}. Best ITAE: {mySolver.fb}")
    #     print(mySolver.xb)
    # optimalParams = mySolver.xb
    
    mySolver = GA(20, paramNum, objFuncSingleITAE, (0., 100.), args=(N, M, timeOut, ), )
    for i in range(25):
        mySolver.iterate(10, 10, 0.2)
        print(f"Ite {i + 1}. Best ITAE: {mySolver.population[0].fitness}")
    #     print(mySolver.population[0].solution)
    optimalParams = mySolver.population[0].solution
    
    print(f"Objective function: {objFuncSingleITAE(optimalParams, N, M, timeOut)}")

    T = 5.
    S = 0.01
    t = linspace(0.0, T, int(T / S))
    Result = solve_ivp(cartPole, [0., T], 
                        2. * (rand(4) - 0.5) * array([1., 1., 0.4, 1., ]), 
                        args=(u, optimalParams, N, M, ), 
                        t_eval=t, dense_output=True, 
                        method="RK45")
    t = Result.t
    X = Result.y.T
    
    plt.figure()
    plt.plot(t, X[:, 0], label=r"$x(t)$", linestyle="-")
    plt.plot(t, X[:, 1], label=r"$\dot{x}(t)$", linestyle="--")
    plt.plot(t, X[:, 2], label=r"$\theta (t)$", linestyle=":")
    plt.plot(t, X[:, 3], label=r"$\dot{\theta}(t)$", linestyle="-.")
    plt.grid(which="major", linestyle="-", linewidth=0.75, color="gray", alpha=0.7)
    plt.minorticks_on() 
    plt.grid(which="minor", linestyle=":", linewidth=0.5, color="lightgray", alpha=0.7)
    plt.legend()
    plt.grid(True)
    plt.xlabel("Time (s)")
    plt.ylabel("State Variable")
    plt.savefig("../images/example2_statespace.pdf", format="pdf", dpi=600, bbox_inches="tight")
    plt.show()
    
    invertedPendulumAnimator = IPAnimator()
    invertedPendulumAnimator.animate(t, X, S, l)


    
























































