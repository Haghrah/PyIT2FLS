# PyIT2FLS

<center><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/><center>

PyIT2FLS is providing a set of tools for fast and easy modeling of Interval Type 2 Fuzzy Sets (IT2FS) and Systems (IT2FLS). There are two main classes in this toolkit, named **_IT2FS_** and **_IT2FLS_**. The first one is for defining IT2FSs and the latter is for defining IT2FLSs. There are many functions defined in PyIT2FLS for utilizing these two classes, which would be introduced in the following.

## IT2FS
In this section we are going to see how IT2FSs can be defined using the **_IT2FS_** class. An IT2FS is defined by its Lower Membership Function (LMF) and Upper Membership Function (UMF). So first we need to know functions, which can be used as LMFs and UMFs. The list of membership functions provided with the PyIT2FLS is presented below:

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

It must be noticed that the parameters of the introduced functions are passed as a list with items mentioned, respectively.

### Creating an IT2FS
The constructor function of the **_IT2FS_** class has six parameters, listed as below:

1.  domain: The universe of discourse of the interval type 2 fuzzy set
1.  umf: The UMF of the interval type 2 fuzzy set
1.  umf_params: The parameters of the UMF function
1.  lmf: The LMF of the interval type 2 fuzzy set
1.  lmf_params: The parameters of the LMF function
1.  check_set: Boolean with default **_False_** value. If it is set as **_True_** then while the set is creating the condition of LMF(x)<=UMF(x) is checked for each x in domain.

### Example 1
The first example demonstrates how to create a IT2FS with trapezoid LMF and triangular UMF functions:

```python
from pyit2fls import IT2FS, trapezoid_mf, tri_mf
from numpy import linspace

mySet = IT2FS(linspace(0., 1., 100), 
              trapezoid_mf, [0, 0.4, 0.6, 1., 1.], 
              tri_mf, [0.25, 0.5, 0.75, 0.6])
```

In the first line the **_IT2FS_** class and trapezoid and triangular membership functions are imported from the toolkit. Also in the second line, from the numpy the linspace is imported for creating the domain of the set. Then, using the **_IT2FS_** the interval type 2 fuzzy set named **_mySet_** is created.

### Plotting the IT2FSs
In order to plot an **_IT2FS_**, the function **_plot_** from the **_IT2FS_** class can be used. This function has three input parameters with **_None_** default value, named **_title_**, **_legend_text_**, and **_filename_**. If the **_title_** and **_legend_text_** parameters are set, the plot would be done using them. And if the **_filename_** is set, the output figure would be saved as a pdf file with the specified name.

## IT2FLS





