<center><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></center>

# PyIT2FLS
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

### Creating common gaussian interval type 2 fuzzy sets
Most of times the gaussian interval type 2 fuzzy sets are prefered in applications. There are two types of gaussian set, gaussian interval type 2 fuzzy set with uncertain mean value and gaussian interval type 2 fuzzy set with uncertain standard deviation value. In order to define sets of this types, it is not needed to define LMF and UMF functions and specify their parameters. There are two functions for defining these sets fast and easy, **_IT2FS_Gaussian_UncertMean_** and **_IT2FS_Gaussian_UncertStd_**. Each of these functions has two input parameters named **_domain_** and **_params_**. The **_domain_** input is the universe of discourse, which the set is defined on it. The **_params_** input for the **_IT2FS_Gaussian_UncertMean_** function is a list consisting of the mean center, the mean spread, and the standard deviation of the set. And for the **_IT2FS_Gaussian_UncertStd_** function it is a list consisting of the mean, the standard deviation center, and the standard deviation spread of the set.

### Plotting the IT2FSs
In order to plot an **_IT2FS_**, the **_plot_** function from the **_IT2FS_** class can be used. This function has three input parameters with **_None_** default value, named **_title_**, **_legend_text_**, and **_filename_**. If the **_title_** and **_legend_text_** parameters are set, the plot would be done using them. And if the **_filename_** is set, the output figure would be saved as a pdf file with the specified name. The Example 1 can be completed by plotting the output set using the **_plot_** function as below:

```python
from pyit2fls import IT2FS, trapezoid_mf, tri_mf
from numpy import linspace

mySet = IT2FS(linspace(0., 1., 100), 
              trapezoid_mf, [0, 0.4, 0.6, 1., 1.], 
              tri_mf, [0.25, 0.5, 0.75, 0.6])
mySet.plot(filename="mySet")
```

### Plotting multiple IT2FSs together
If there are many sets which we would like to plot them together, we can use the **_IT2FS_plot_** function from PyIT2FLS. The inputs of this function after an arbitrary number of **_IT2FSs_** are as **_plot's_**. It means that three **_title_**, **_legend_text_**, and **_filename_** parameters with **_None_** default value. In the second example below, it is shown how to use the **_IT2FS_plot_** function for plotting three **_IT2FSs_**.

### Example 2
The second example demonstrates how to define gaussian IT2FSs and plot them together.

```python
from pyit2fls import IT2FS_Gaussian_UncertMean, IT2FS_plot, meet, join, min_t_norm, max_s_norm
from numpy import linspace

domain = linspace(0., 1., 100)
A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.1])
B = IT2FS_Gaussian_UncertMean(domain, [0.33, 0.1, 0.1])
C = IT2FS_Gaussian_UncertMean(domain, [0.66, 0.1, 0.1])
IT2FS_plot(A, B, C, title="", legends=["Small","Medium","Large"], filename="multiSet")
```

### T-norms and S-norms
In the PyIT2FLS there are two T-norms and a S-norm by default, but new ones can be defined by the user himself. Any function that theoritically meets the being T-norm (or S-norm) requirements and is defined as following, can be used as a T-norm (or S-norm). The function that is going to be used as a T-norm (or S-norm) must have two input. These inputs would be numpy (n,) shaped arrays (or single float number). The output must be also of the type numpy (n,) shaped array (or single float number). The function must be compatible with these two input/output types. The functions from the PyIT2FLS, dedicated to T-norms and S-norms are as below:

- min_t_norm: Minimum T-norm
- product_t_norm: Product T-norm 
- max_s_norm: Maximum S-norm


### Meet and join operators
Two essential operators in Interval Type 2 Fuzzy Logic, are the meet and join operators. These operators are defined in PyIY2FLS as two functions **_meet_** and **_join_**. Both functions have four inputs. For these functions, the first three inputs are common, the universe of discourse, the first **_IT2FS_**, and the second **_IT2FS_**. The 4th input of the **_meet_** function is the desired T-norm function, and for the **_join_** function it is the desired S-norm function. 

### Example 3
Completing the second example, the **_meet_** of the sets **_A_** and **_B_**, and **_join_** of the sets **_B_** and **_C_** are calculated:

```python
from pyit2fls import IT2FS_Gaussian_UncertMean, IT2FS_plot, meet, join, min_t_norm, max_s_norm
from numpy import linspace

domain = linspace(0., 1., 100)
A = IT2FS_Gaussian_UncertMean(domain, [0., 0.1, 0.1])
B = IT2FS_Gaussian_UncertMean(domain, [0.33, 0.1, 0.1])
C = IT2FS_Gaussian_UncertMean(domain, [0.66, 0.1, 0.1])
IT2FS_plot(A, B, C, title="", legends=["Small","Medium","Large"], filename="multiSet")

AB = meet(domain, A, B, min_t_norm)
AB.plot(filename="meet")

BC = join(domain, B, C, max_s_norm)
BC.plot(filename="join")
```

### Type reduction algorithms
The type reduction play a key role in achieving crisp values from Type 2 Fuzzy Sets. The type reduction algorithms, which are implemented in the PyIT2FLS are listed as the table below.

|  Type reduction algorithm function  | Description |
|:-----------------------------------:|:-----------:|
| KM_algorithm | Karnik-Mendel algorithm |
| EKM_algorithm | Enhanced Karnik-Mendel algorithm |
| WEKM_algorithm | Weighted enhanced Karnik-Mendel algorithm |
| TWEKM_algorithm | Trapezoid weighted enhanced Karnik-Mendel algorithm |
| EIASC_algorithm | Enhanced Iterative Algorithm with Stopping Condition |
| WM_algorithm | Wu-Mendel algorithm |
| BMM_algorithm | Begian-Melek-Mendel algorithm |
| LBMM_algorithm | Li-Begian-Melek-Mendel algorithm |
| NT_algorithm | Nie-Tan algorithm |

## IT2FLS

### Calculating the system output




