<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## IT2FS
In this section, we are going to see how IT2FSs can be defined using the **_IT2FS_** class. An IT2FS is defined by its Lower Membership Function (LMF) and Upper Membership Function (UMF). So first we need to know functions, which can be used as LMFs and UMFs. The list of membership functions provided with the PyIT2FLS is presented below:

### List of membership functions that can be used as LMF and UMF functions

|  Membership function  | Description | List of parameters |
|:---------------------:|:-----------:|:------------------:|
| zero_mf               | All zero membership function | None |
| singleton_mf          | Singleton membership function | Singleton's center and height |
| const_mf              | Constant membership function | Constant membership function's height |
| tri_mf                | Triangular membership function | The left end, the center, the right end, and the height of the triangular membership function |
| ltri_mf               | Left triangular membership function | The right end, the center, and the height of the triangular membership function |
| rtri_mf               | Right triangular membership function | The left end, the center, and the height of the triangular membership function |
| trapezoid_mf          | Trapezoidal membership function | The left end, the left center, the right center, the right end, and the height of the trapezoidal membership function |
| gaussian_mf           | Gaussian membership function | The center, the standard deviation, and the height of the gaussian membership function |
| gauss_uncert_mean_umf | Gaussian with uncertain mean UMF | The lower limit of mean, the upper limit of mean, the standard deviation, and the height of the gaussian membership function |
| gauss_uncert_mean_lmf | Gaussian with uncertain mean LMF | The lower limit of mean, the upper limit of mean, the standard deviation, and the height of the gaussian membership function |
| gauss_uncert_std_umf  | Gaussian with uncertain standard deviation UMF | The center, the lower limit of std., the upper limit of std., and the height of the gaussian membership function |
| gauss_uncert_std_lmf  | Gaussian with uncertain standard deviation LMF | The center, the lower limit of std., the upper limit of std., and the height of the gaussian membership function |
| rgauss_uncert_std_umf | Right Gaussian with uncertain standard deviation UMF | The center, the lower limit of std., the upper limit of std., and the height of the gaussian membership function |
| rgauss_uncert_std_lmf | Right Gaussian with uncertain standard deviation LMF | The center, the lower limit of std., the upper limit of std., and the height of the gaussian membership function |
| lgauss_uncert_std_umf | Left Gaussian with uncertain standard deviation UMF | The center, the lower limit of std., the upper limit of std., and the height of the gaussian membership function |
| lgauss_uncert_std_lmf | Left Gaussian with uncertain standard deviation LMF | The center, the lower limit of std., the upper limit of std., and the height of the gaussian membership function |

It must be noticed that the parameters of the introduced functions are passed as a list with items mentioned, respectively.

### Definition of a membership function in PyIT2FLS
The membership functions introduced in previous section are defined as below:

```python
def membership_function_name(x, params):
  # Some calculations ...
  return membership_degree
```

This template can be used by users to define their own new membership functions. It is recommended to use Numpy based mathematic functions for defining new membership functions. The first input of the membership function is a numpy array including some points of the universe of discourse, so the output also must be a numpy array with the same size and shape.

### Evaluating the membership functions
Let's see an example about how membership functions can be evaluated. In this example we are going to plot multiple membership functions to see their shapes.


```python
from numpy import linspace
import matplotlib.pyplot as plt
from pyit2fls import zero_mf, singleton_mf, const_mf, tri_mf, ltri_mf, rtri_mf, \
    trapezoid_mf, gaussian_mf, gauss_uncert_mean_umf, gauss_uncert_mean_lmf, \
    gauss_uncert_std_umf, gauss_uncert_std_lmf, rgauss_uncert_std_umf, \
    rgauss_uncert_std_lmf, lgauss_uncert_std_umf, lgauss_uncert_std_lmf

domain = linspace(0., 1., 1001)

zero = zero_mf(domain)
singleton = singleton_mf(domain, [0.5, 1.])
const = const_mf(domain, [1.])
tri = tri_mf(domain, [0., 0.5, 1., 1.])
ltri = ltri_mf(domain, [0.5, 1., 1.])
rtri = rtri_mf(domain, [0.5, 0., 1.])
trapezoid = trapezoid_mf(domain, [0., 0.25, 0.75, 1., 1.])
gaussian = gaussian_mf(domain, [0.5, 0.1, 1.])
gauss_uncert_meanu = gauss_uncert_mean_umf(domain, [0.25, 0.75, 0.2, 1.])
gauss_uncert_meanl = gauss_uncert_mean_lmf(domain, [0.25, 0.75, 0.3, 1.])
gauss_uncert_stdu = gauss_uncert_std_umf(domain, [0.5, 0.1, 0.05, 1.])
gauss_uncert_stdl = gauss_uncert_std_lmf(domain, [0.5, 0.1, 0.05, 1.])
rgauss_uncert_stdu = rgauss_uncert_std_umf(domain, [0.5, 0.1, 0.05, 1.])
rgauss_uncert_stdl = rgauss_uncert_std_lmf(domain, [0.5, 0.1, 0.05, 1.])
lgauss_uncert_stdu = lgauss_uncert_std_umf(domain, [0.5, 0.1, 0.05, 1.])
lgauss_uncert_stdl = lgauss_uncert_std_lmf(domain, [0.5, 0.1, 0.05, 1.])


fig, axs = plt.subplots(3, 3, figsize=(15,15))
axs[0, 0].plot(domain, zero, label="All zero MF")
axs[0, 0].plot(domain, const, label="Const MF")
axs[0, 0].grid(True)

axs[0, 1].plot(domain, singleton, label="Singleton MF")
axs[0, 1].grid(True)

axs[0, 2].plot(domain, tri, label="Triangular MF")
axs[0, 2].plot(domain, ltri, label="Left triangular MF")
axs[0, 2].plot(domain, rtri, label="Right triangular MF")
axs[0, 2].grid(True)

axs[1, 0].plot(domain, trapezoid, label="Trapezoid MF")
axs[1, 0].grid(True)

axs[1, 1].plot(domain, gaussian, label="Gaussian MF")
axs[1, 1].grid(True)

axs[1, 2].plot(domain, gauss_uncert_meanu, label="Gaussian UMF with uncertain mean value")
axs[1, 2].plot(domain, gauss_uncert_meanl, label="Gaussian LMF with uncertain mean value")
axs[1, 2].grid(True)

axs[2, 0].plot(domain, gauss_uncert_stdu, label="Gaussian UMF with uncertain std value")
axs[2, 0].plot(domain, gauss_uncert_stdl, label="Gaussian LMF with uncertain std value")
axs[2, 0].grid(True)

axs[2, 1].plot(domain, lgauss_uncert_stdu, label="Left gaussian UMF with uncertain std value")
axs[2, 1].plot(domain, lgauss_uncert_stdl, label="Left gaussian LMF with uncertain std value")
axs[2, 1].grid(True)

axs[2, 2].plot(domain, rgauss_uncert_stdu, label="Right gaussian UMF with uncertain std value")
axs[2, 2].plot(domain, rgauss_uncert_stdl, label="Right gaussian LMF with uncertain std value")
axs[2, 2].grid(True)

for ax in axs.flat:
    ax.set(xlabel="Domain", ylabel="Membership degree")

for ax in axs.flat:
    ax.label_outer()
```


## IT2FS Class
The IT2FS class is designed for defining Interval Type 2 Fuzzy Sets. It's constructor function has six parameters, which are described below:
1. domain: Universe of discourse is defined by setting the domain parameter.
2. umf: The Upper Memebrship Function of the IT2FS. The umf must be among the introduced membership functions or a self defined membership function with the introduced structure.
3. umf_params: Parameters of the given UMF function.
4. lmf: The Lower Membership Function of the IT2FS. The lmf must be among the introduced membership functions or a self defined membership function with the introduced structure.
5. lmf_params: Parameters of the given LMF function.
6. check_set: The defualt value of this parameter is false. When it is set true, the UMF(x) > LMF(x) condition, for all x in the universe of discourse, is checked. This is useful when the user does not know the parameters of UMF and LMF functions are selected correctly or not.

### Defining an IT2FS



### Examples









