from numpy import (array, linspace, )
from scipy.integrate import (solve_ivp, )
import matplotlib.pyplot as plt
from pyit2fls import (Linear_System, T1_TS_Model, gaussian_mf_learning, )
import matplotlib.pyplot as plt


A1 = array([[-1.,  0.,  0., ], 
            [ 0., -1.,  0., ], 
            [ 0.,  0., -1., ], ])
A2 = array([[-1.,  1.,  0., ], 
            [ 0.,  1.,  0., ], 
            [ 0.,  0., -1., ], ])
A3 = array([[-1.,  1.,  0., ], 
            [ 0.,  1.,  1., ], 
            [ 0.,  0., -1., ], ])
A4 = array([[-1.,  1.,  0., ], 
            [ 0.,  2.,  1., ], 
            [ 0.,  0., -1., ], ])

B1 = array([[1., ], 
            [0., ], 
            [0., ], ])
B2 = array([[2., ], 
            [0., ], 
            [0., ], ])
B3 = array([[2., ], 
            [0., ], 
            [0., ], ])
B4 = array([[1., ], 
            [0., ], 
            [0., ], ])

C1 = array([1., 0., 0., ])
C2 = array([2., 0., 0., ])
C3 = array([2., 0., 0., ])
C4 = array([1., 0., 0., ])

D1 = array([[0., ], ])
D2 = array([[0., ], ])
D3 = array([[0., ], ])
D4 = array([[0., ], ])



linearSystem1 = Linear_System(A1, B1, C1, D1)
linearSystem2 = Linear_System(A2, B2, C2, D2)
linearSystem3 = Linear_System(A3, B3, C3, D3)
linearSystem4 = Linear_System(A4, B4, C4, D4)


params = [[[ 1., 1., ],   # Rule 1: Parameters of a gaussian fuzzy set corresponded with x1
           [ 0., 1., ],   # Rule 1: Parameters of a gaussian fuzzy set corresponded with x2
           [ 1., 1., ]],  # Rule 1: Parameters of a gaussian fuzzy set corresponded with x3
          [[ 1., 1., ],   # Rule 2: Parameters of a gaussian fuzzy set corresponded with x1
           [ 0., 1., ],   # Rule 2: Parameters of a gaussian fuzzy set corresponded with x2
           [-1., 1., ]],  # Rule 2: Parameters of a gaussian fuzzy set corresponded with x3
          [[-1., 1., ],   # Rule 3: Parameters of a gaussian fuzzy set corresponded with x1
           [0., 1., ],   # Rule 3: Parameters of a gaussian fuzzy set corresponded with x2
           [ 1., 1., ]],  # Rule 3: Parameters of a gaussian fuzzy set corresponded with x3
          [[-1., 1., ],   # Rule 4: Parameters of a gaussian fuzzy set corresponded with x1
           [ 0., 1., ],   # Rule 4: Parameters of a gaussian fuzzy set corresponded with x2
           [-1., 1., ]], ]# Rule 4: Parameters of a gaussian fuzzy set corresponded with x3
myTakagiSugeno = T1_TS_Model(params, [linearSystem1, 
                                      linearSystem2, 
                                      linearSystem3, 
                                      linearSystem4], 4, 3, 1, 1)

def U(t, X):
    return array([[- X[0] - X[1] - X[2] ], ])

X0 = array([1., -2., 3., ])
dt = 0.001
T  = 100.
t  = linspace(0., T, int(T / dt))
X  = solve_ivp(myTakagiSugeno, [0., T], X0, args=(U, ), 
               method="RK45", t_eval=t, dense_output=True).y

plt.figure()
plt.plot(t, X[0, :], label=r"$x_{1}$")
plt.plot(t, X[1, :], label=r"$x_{2}$")
plt.plot(t, X[2, :], label=r"$x_{3}$")
plt.legend()
plt.grid(True)
plt.show()













