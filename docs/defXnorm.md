<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining new t-norms and s-norms
Defining new t-norms and s-norms will be explained using examples. The first example is about defining a new s-norm and using it in join operator. We are going to define the probabilistic sum s-norm, which is defined as below:

<img src="https://render.githubusercontent.com/render/math?math=\perp_{sum}(a,b)=a %2B b - a.b"> 

```python
from pyit2fls import IT2FS_Gaussian_UncertMean, join, IT2FS_plot
from numpy import linspace

def probabilistic_sum_s_norm(a, b):
	return a + b - a * b

domain = linspace(0., 1., 1000)
A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.25, 1.])
B = IT2FS_Gaussian_UncertMean(domain, [1., 0.1, 0.25, 1.])
IT2FS_plot(A, B, legends=["Small","Large"])

AB = join(domain, A, B, probabilistic_sum_s_norm)
AB.plot()
```

The output plots of this example are represented as below.

|  The **_SMALL_** and **_LARGE_** sets  | Join of the two sets |
|:---------------------:|:-----------:|
| <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/3.1.png" width="256"> | <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/3.2.png" width="256"> |

In the next example we are going to define a new t-norm an use it in meet operator. Let's define Łukasiewicz t-norm defined by the formula below:

<img src="https://render.githubusercontent.com/render/math?math=\top_{Luk}(a,b)=max\{0, a %2B b - 1\}"> 


```python
from pyit2fls import IT2FS_Gaussian_UncertMean, meet, IT2FS_plot
from numpy import linspace, maximum

def Lukasiewicz_t_norm(a, b):
    return maximum(0, a + b - 1)

domain = linspace(0., 1., 1000)
A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.4, 1.])
B = IT2FS_Gaussian_UncertMean(domain, [1., 0.1, 0.4, 1.])
IT2FS_plot(A, B, legends=["Small","Large"])

AB = meet(domain, A, B, Lukasiewicz_t_norm)
AB.plot()
```

The output plots of this example are represented as below.

|  The **_SMALL_** and **_LARGE_** sets  | Meet of the two sets |
|:---------------------:|:-----------:|
| <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/3.3.png" width="256"> | <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/3.4.png" width="256"> |



