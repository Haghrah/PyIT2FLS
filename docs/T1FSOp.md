<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Type I Fuzzy Logic Operators
Two essential operators in Type I Fuzzy Logic, are the AND and OR operators. These operators are defined in PyIY2FLS as two functions **_T1FS_AND_** and **_T1FS_OR_**. Both functions have four inputs. For these functions, the first three inputs are common, the universe of discourse, first **_T1FS_**, and second **_T1FS_**. The 4th input of the **_T1FS_AND_** function is the desired t-norm, and for the **_T1FS_OR_** function, is the desired s-norm.

The t-norms and s-norms provided by the PyIT2FLS are introduced in previous sections of the documentations.

It must be noted that the users can define new t-norms and s-norms, too. The user defined t-norm or s-norm functions must follow the structure below:

```python
def userdefined_norm(a, b)
	return some_calculations(a, b)
```

### Example
In this example we are going to apply the AND and OR operators on T1FSs and plot the outputs.

```python
from pyit2fls import T1FS, gaussian_mf, T1FS_plot, T1FS_AND, T1FS_OR, min_t_norm, max_s_norm
from numpy import linspace

domain = linspace(0., 1., 1000)
A = T1FS(domain, gaussian_mf, [0., 0.1, 1.])
B = T1FS(domain, gaussian_mf, [0.5, 0.1, 1.])
C = T1FS(domain, gaussian_mf, [1., 0.1, 1.])
T1FS_plot(A, B, C, legends=["Small","Medium","Large"])

AB = T1FS_AND(domain, A, B, min_t_norm)
AB.plot()

BC = T1FS_OR(domain, B, C, max_s_norm)
BC.plot()
```

The output plots of this example are represented as below.

|  **_SMALL_**, **_MEDIUM_**, and **_LARGE_** sets  | AND of **_SMALL_** and **_MEDIUM_** | OR of **_MEDIUM_** and **_LARGE_** |
|:---------------------:|:-----------:|:------------------:|
| <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/2.1._.png" width="150"> | <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/2.2._.png" width="150"> | <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/2.3._.png" width="150"> |
















