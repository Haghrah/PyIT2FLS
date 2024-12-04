from numpy import (array, linspace, )
from numpy.random import (rand, )
from scipy.integrate import (solve_ivp, )
import matplotlib.pyplot as plt
from pyit2fls import (Linear_System, T1_TS_Model, rtri_mf, ltri_mf, )
import matplotlib.pyplot as plt


A1 = array([[-1.,  1., ], 
            [ 0., -1., ],  ])
A2 = array([[ 1.,  1., ], 
            [ 0.,  1., ], ])
A3 = array([[ 1.,  1., ], 
            [ 0.,  1., ], ])
A4 = array([[-1.,  1., ], 
            [ 0., -2., ], ])

B1 = array([[ 1., ], 
            [-1., ], ])
B2 = array([[ 2., ], 
            [ 0., ], ])
B3 = array([[ 2., ], 
            [-1., ], ])
B4 = array([[ 1., ], 
            [ 0., ], ])

C1 = array([1., 0.5, ])
C2 = array([2., 0.1, ])
C3 = array([2., 0.1, ])
C4 = array([1., 0.5, ])

D1 = array([[0.1, ], ])
D2 = array([[0.2, ], ])
D3 = array([[0.2, ], ])
D4 = array([[0.1, ], ])


linearSystem1 = Linear_System(A1, B1, C1, D1)
linearSystem2 = Linear_System(A2, B2, C2, D2)
linearSystem3 = Linear_System(A3, B3, C3, D3)
linearSystem4 = Linear_System(A4, B4, C4, D4)

mfList = [[rtri_mf,       # Rule 1: The fuzzy set corresponded with x1
           rtri_mf, ],    # Rule 1: The fuzzy set corresponded with x2
          [rtri_mf,       # Rule 2: The fuzzy set corresponded with x1
           ltri_mf, ],    # Rule 2: The fuzzy set corresponded with x2
          [ltri_mf,       # Rule 3: The fuzzy set corresponded with x1
           rtri_mf, ],    # Rule 3: The fuzzy set corresponded with x2
          [ltri_mf,       # Rule 4: The fuzzy set corresponded with x1
           ltri_mf, ], ]  # Rule 4: The fuzzy set corresponded with x2
mfParamsList = [[[-1., 0., 1., ],      # Rule 1: Parameters of the fuzzy set corresponded with x1
                 [-1., 0., 1., ], ],   # Rule 1: Parameters of the fuzzy set corresponded with x2
                [[-1., 0., 1., ],      # Rule 2: Parameters of the fuzzy set corresponded with x1
                 [ 1., 0., 1., ], ],   # Rule 2: Parameters of the fuzzy set corresponded with x2
                [[ 1., 0., 1., ],      # Rule 3: Parameters of the fuzzy set corresponded with x1
                 [-1., 0., 1., ], ],   # Rule 3: Parameters of the fuzzy set corresponded with x2
                [[ 1., 0., 1., ],      # Rule 4: Parameters of the fuzzy set corresponded with x1
                 [ 1., 0., 1., ], ], ] # Rule 4: Parameters of the fuzzy set corresponded with x2
myTakagiSugeno = T1_TS_Model(mfList, mfParamsList, 
                             [linearSystem1, 
                              linearSystem2, 
                              linearSystem3, 
                              linearSystem4], 
                              4, 2, 1, 1)

def U(t, X):
    return array([[0.1 * X[0] + 0.1 * X[1] ], ])

X0 = 4. * (rand(2) - 0.5)
dt = 0.001
T  = 100.
t  = linspace(0., T, int(T / dt))
X  = solve_ivp(myTakagiSugeno, [0., T], X0, args=(U, ), 
               method="RK45", t_eval=t, dense_output=True).y

plt.figure()
plt.plot(t, X[0, :], label=r"$x_{1}$")
plt.plot(t, X[1, :], label=r"$x_{2}$")
plt.legend()
plt.grid(True)
plt.show()













