from pyit2fls import (T1TSK_ML, )
from numpy import (linspace, array, abs, pi, sin, cos, meshgrid, zeros_like, )
from scipy.optimize import (Bounds, )
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

X1 = linspace(-pi, pi, 10)
X2 = linspace(-pi, pi, 10)

X = []
y = []
for x1 in X1:
    for x2 in X2:
        X.append([x1, x2])
        y.append(sin(x1) + cos(x2))
X = array(X)

myTSK = T1TSK_ML(2, 16, (-4., 4.), algorithm="PSO", 
                 algorithm_params=[100, 100, 0.3, 0.3, 2.4])
print(myTSK.fit(X, y))

x1, x2 = meshgrid(X1, X2)
y1 = sin(x1) + cos(x2)
y2 = zeros_like(y1)
for i in range(10):
    for j in range(10):
        y2[i, j] = myTSK.score(array([X1[j], X2[i], ]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x1, x2, y1, cmap='viridis')
ax.set_title('3D Surface Plot')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x1, x2, y2, cmap='viridis')
ax.set_title('3D Surface Plot')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x1, x2, abs(y2 - y1), cmap='viridis')
ax.set_title('3D Surface Plot')
plt.show()










