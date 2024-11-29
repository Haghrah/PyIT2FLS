from pyit2fls import (IT2Mamdani_ML, IT2FS_Gaussian_UncertStd, )
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

N = 2
M = 3
myIT2Mamdani = IT2Mamdani_ML(N, M, IT2FS_Gaussian_UncertStd, (-4., 4.), 
                             algorithm="PSO", algorithm_params=[200, 200, 0.3, 0.3, 2.4])
print(myIT2Mamdani.fit(X, y))

x1, x2 = meshgrid(X1, X2)
y1 = sin(x1) + cos(x2)
y2 = zeros_like(y1)
for i in range(10):
    for j in range(10):
        y2[i, j] = myIT2Mamdani.score(array([X1[j], X2[i], ]))

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
original = ax.plot_surface(x1, x2, y1, cmap="viridis", vmin=y1.min(), vmax=y1.max())
fig.colorbar(original, ax=ax, shrink=0.5, aspect=10, 
             label="Original Plane")
ax.set_title("3D Surface Plot")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
fitted = ax.plot_surface(x1, x2, y2, cmap="viridis", vmin=y1.min(), vmax=y1.max())
fig.colorbar(fitted, ax=ax, shrink=0.5, aspect=10, 
             label="Fitted Plane")
ax.set_title("3D Surface Plot")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
error_surface = ax.plot_surface(x1, x2, abs(y2 - y1), cmap="Greens", alpha=0.8)
fig.colorbar(error_surface, ax=ax, shrink=0.5, aspect=10, 
             label="Error")
ax.plot_surface(x1, x2, y1, cmap="Blues", alpha=0.7)
ax.set_title("3D Surface Plot")
plt.show()







