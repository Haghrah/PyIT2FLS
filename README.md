PyIT2FLS
========
NumPy based toolkit for Interval Type 2 Fuzzy Logic Systems (IT2FLS).

## Examples
In the code below, the chaotic Mackey-Glass time series is predicted using PyIT2FLS toolkit. The designed IT2FLS has three inputs and an output. Inputs are three consecutive samples of the time series. For each input and for the ouput three Interval Type 2 Fuzzy Sets (IT2FS) are defined. The parameters of these sets are achieved using the Particle Swarm Optimization (PSO) algorithm to have minimum Mean Square Error (MSE). The full code of the example and the PSO solver are presented in examples folder.

```python
import numpy as np
import matplotlib.pyplot as plt
from pyit2fls import IT2FS_Gaussian_UncertStd, IT2FLS, min_t_norm, max_s_norm
import PyPSO

def mackey_glass(tav, n, beta, gamma, step):
    x = [np.random.random() for i in range(tav)]
    for i in range(step):
        x.append(x[-1] + beta * x[-tav] / (1 + x[-tav] ** n) - gamma * x[-1])
    return x[tav:]

mg = mackey_glass(2, 9.65, 2., 1., 1000)

domain = np.linspace(0., 1.5, 15)
L = 100  # Learning set length
LearningSet = []
for i in range(200, 200 + L):
    LearningSet.append([[mg[i], mg[i - 1], mg[i - 2]], mg[i + 1]])

def calculate(x, i):
    A1 = IT2FS_Gaussian_UncertStd(domain, x[:3])
    A2 = IT2FS_Gaussian_UncertStd(domain, x[3:6])
    A3 = IT2FS_Gaussian_UncertStd(domain, x[6:9])
    
    B1 = IT2FS_Gaussian_UncertStd(domain, x[9:12])
    B2 = IT2FS_Gaussian_UncertStd(domain, x[12:15])
    B3 = IT2FS_Gaussian_UncertStd(domain, x[15:18])
    
    C1 = IT2FS_Gaussian_UncertStd(domain, x[18:21])
    C2 = IT2FS_Gaussian_UncertStd(domain, x[21:24])
    C3 = IT2FS_Gaussian_UncertStd(domain, x[24:27])
    
    O1 = IT2FS_Gaussian_UncertStd(domain, x[27:30])
    O2 = IT2FS_Gaussian_UncertStd(domain, x[30:33])
    O3 = IT2FS_Gaussian_UncertStd(domain, x[33:36])
    
    it2fls = IT2FLS()
    it2fls.add_input_variable("A")
    it2fls.add_input_variable("B")
    it2fls.add_input_variable("C")
    it2fls.add_output_variable("O")
    
    it2fls.add_rule([("A", A1), ("B", B1), ("C", C1)], [("O", O1)])
    it2fls.add_rule([("A", A2), ("B", B2), ("C", C2)], [("O", O2)])
    it2fls.add_rule([("A", A3), ("B", B3), ("C", C3)], [("O", O3)])
    
    tr = it2fls.evaluate({"A":i[0], "B":i[1], "C":i[2]}, 
                        min_t_norm, max_s_norm, domain, method="Height", 
                        algorithm="EIASC")
    o = tr["O"]
    return (o[0] + o[1]) / 2

def cost_func(x):
    A1 = IT2FS_Gaussian_UncertStd(domain, x[:3])
    A2 = IT2FS_Gaussian_UncertStd(domain, x[3:6])
    A3 = IT2FS_Gaussian_UncertStd(domain, x[6:9])
    
    B1 = IT2FS_Gaussian_UncertStd(domain, x[9:12])
    B2 = IT2FS_Gaussian_UncertStd(domain, x[12:15])
    B3 = IT2FS_Gaussian_UncertStd(domain, x[15:18])
    
    C1 = IT2FS_Gaussian_UncertStd(domain, x[18:21])
    C2 = IT2FS_Gaussian_UncertStd(domain, x[21:24])
    C3 = IT2FS_Gaussian_UncertStd(domain, x[24:27])
    
    O1 = IT2FS_Gaussian_UncertStd(domain, x[27:30])
    O2 = IT2FS_Gaussian_UncertStd(domain, x[30:33])
    O3 = IT2FS_Gaussian_UncertStd(domain, x[33:36])
    
    it2fls = IT2FLS()
    it2fls.add_input_variable("A")
    it2fls.add_input_variable("B")
    it2fls.add_input_variable("C")
    it2fls.add_output_variable("O")
    
    it2fls.add_rule([("A", A1), ("B", B1), ("C", C1)], [("O", O1)])
    it2fls.add_rule([("A", A2), ("B", B2), ("C", C2)], [("O", O2)])
    it2fls.add_rule([("A", A3), ("B", B3), ("C", C3)], [("O", O3)])
    
    err = 0
    for L in LearningSet:
        tr = it2fls.evaluate({"A":L[0][0], "B":L[0][1], "C":L[0][2]}, 
                            min_t_norm, max_s_norm, domain, method="Height", 
                            algorithm="EIASC")
        o = tr["O"]
        err += ((o[0] + o[1]) / 2 - L[1]) ** 2
    return err / len(LearningSet)

x = np.random.random(size=(36,))
e = cost_func(x)
print(e)

def solution_generator():
    return 1.5 * np.random.rand(12 * 3)

def velocity_generator():
    return 0.25 * np.random.rand(12 * 3)

mySolver = PyPSO.PyPSO(cost_func, 50, 200, solution_generator, velocity_generator)
conv = mySolver.solve()

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
```

## Licence
PyIT2FLS is published under GNU General Public License v3.0. If you are using the developed toolkit, please cite the paper <PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems>.

## Installation
PyIT2FLS can be installed by unzipping the source code in one directory and using this command:

    (sudo) python setup.py install

