<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Interval Type II Fuzzy Logic Operators
Two essential operators in Interval Type 2 Fuzzy Logic, are the meet and join operators. These operators are defined in PyIY2FLS as two functions **_meet_** and **_join_**. Both functions have four inputs. For these functions, the first three inputs are common, the universe of discourse, the first **_IT2FS_**, and the second **_IT2FS_**. The 4th input of the **_meet_** function is the desired t-norm, and for the **_join_** function, is the desired s-norm.

The t-norms and s-norms provided by the PyIT2FLS are introduced in previous sections of the documentations.

It must be noted that the users can define new t-norms and s-norms, too. The user defined t-norm or s-norm functions must follow the structure below:

```python
def userdefined_norm(a, b)
	return some_calculations(a, b)
```

### Example
In this example we are going to apply the meet and join operators on IT2FSs and plot the outputs.

```python
from pyit2fls import IT2FS_Gaussian_UncertMean, IT2FS_plot, meet, join, min_t_norm, max_s_norm
from numpy import linspace

domain = linspace(0., 1., 1000)
A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.1, 1.])
B = IT2FS_Gaussian_UncertMean(domain, [0.5, 0.1, 0.1, 1.])
C = IT2FS_Gaussian_UncertMean(domain, [1., 0.1, 0.1, 1.])
IT2FS_plot(A, B, C, legends=["Small","Medium","Large"])

AB = meet(domain, A, B, min_t_norm)
AB.plot()

BC = join(domain, B, C, max_s_norm)
BC.plot()
```

The output plots of this example are represented as below.

|  **_SMALL_**, **_MEDIUM_**, and **_LARGE_** sets  | Meet of **_SMALL_** and **_MEDIUM_** | Join of **_MEDIUM_** and **_LARGE_** |
|:---------------------:|:-----------:|:------------------:|
| <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/2.1.png" width="150">               | <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/2.2.png" width="150"> | <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/docs/images/2.3.png" width="150"> |














