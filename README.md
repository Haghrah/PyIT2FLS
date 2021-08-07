PyIT2FLS
========

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="256"/></p>

NumPy and SciPy based toolkit for Type 1 and Interval Type 2 Fuzzy Logic Systems.

## Licence
PyIT2FLS is published under MIT license. If you are using the developed toolkit, please cite preprint of our paper [PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems](https://arxiv.org/abs/1909.10051).

BibTeX:

    @misc{haghrah2019pyit2fls,
        title={PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems},
        author={Amir Arslan Haghrah and Sehraneh Ghaemi},
        year={2019},
        eprint={1909.10051},
        archivePrefix={arXiv},
        primaryClass={eess.SY}
    }

MLA:

    Haghrah, Amir Arslan, and Sehraneh Ghaemi. "PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems." arXiv preprint arXiv:1909.10051 (2019).

## Installation
PyIT2FLS can be installed by unzipping the source code in a directory and using this command:

    (sudo) python3 setup.py install

Or you can use pip3:

    (sudo) pip3 install --upgrade pyit2fls

## Versions

### Features coming up in the next version
- Exception handling.
- Supporting Generalized Type 2 Fuzzy Sets and Systems.

### Some notes on version 0.7.9
- Some bugs (concerning EIASC algorithm) have been fixed in this version.

### Some notes on version 0.7.8
- Some bugs have been fixed in this version.

### Some notes on version 0.7.0-0.7.7
- Supporting fuzzy matrices and related operators.
- Faster IT2 FLS evaluation (Please visit [typereduction](https://github.com/Haghrah/PyIT2FLS/tree/master/typereduction) package).
- Introduction of emphasize function for both type 1 and interval type 2 fuzzy sets (See [16th](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_16.py) example).
- New options while calling plot functions (**_T1FS.plot_**, **_IT2FS.plot_**, **_T1FS_plot_**, **_IT2FS_plot_**, and **_TR_plot_**) have been added.
	- Users can specify the output file format (png, eps, pdf, etc.) while calling the plot function by setting the **_ext_** input parameter (with **_pdf_** default value).
	- Users can edit the status of the grid in the output plot by setting the **_grid_** input parameter (with **_True_** default value).
	- Users can edit the x and y-labels by setting the input parameters **_xlabel_** and **_ylabel_**, respectively. The default value of the **_xlabel_** is **_Domain_**, and the default value of the **_ylabel_** is **_Membership degree_**.

- There are some deprecated functions and classes. After releasing version 1.0.0, deprecated functions and classes will no longer be supported. So:
	- Please use the function **_IT2FS_LGaussian_UncertStd_** instead of **_L_IT2FS_Gaussian_UncertStd_**.
	- Please use the function **_IT2FS_RGaussian_UncertStd_** instead of **_R_IT2FS_Gaussian_UncertStd_**.
	- Please use the class **_IT2Mamdani_** instead of **_IT2FLS_**.
	- Please use the class **_IT2Mamdani_** instead of **_Mamdani_**.
	- Please use the class **_IT2TSK_** instead of **_TSK_**.

### Some notes on version 0.6.1
- Some bugs have been fixed in this version.

### Some notes on version 0.6
- Supporting Type 1 Fuzzy Sets and Systems.
- Supporting elliptic and semi-elliptic membership functions.
- Supporting generalized bell shaped membership function.
- Supporting many new t-norms and s-norms.
- Some bugs are fixed in this version.

### Some notes on version 0.5
- Supporting both Mamdani and TSK systems.
- Some bugs have been fixed in this vesion. Now, it is possible to use different domains for FLS inputs and outputs.

### Some notes on version 0.4
- Some bugs have been fixed in this version especially in type reduction algorithms. I would like to say thanks to Dr. K.B Badri Narayanan for reporting the errors.
- Some new IT2FSs have been added to the toolkit.
- In previous versions, the height of the IT2FS_Gaussian_UncertStd and IT2FS_Gaussian_UncertMean IT2FSs was fixed to 1, by default. But in the new version, user must give the height value in the parameters list as the last element.

## Docstrings
Further information about the functions and classes in the PyIT2FLS are accessible by docstrings. After importing a function or class, they can be seen by calling the help function. For example:

```python
>>> from pyit2fls import IT2FS_Gaussian_UncertStd
>>> help(IT2FS_Gaussian_UncertStd)
```

## Examples
There are some examples provided along with the toolkit which are as below:
* [Ex1](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_1.py): Defining an Interval Type 2 Fuzzy Set (IT2FS).
* [Ex2](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_2.py): Using join and meet operators and plotting the outputs.
* [Ex3](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_3.py): Defining a simple (MIMO) IT2FLS.
* [Ex3 (updated)](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_3_0.7.0.py): Example 3 using the IT2Mamdani class.
* [Ex4](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_4.py): Prediction of the Mackey-Glass chaotic time series with PSO-based parameter tuning.
* [Ex4 (updated)](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_4_0.7.0.py): Example 4 using the IT2Mamdani class.
* [Ex5](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_5.py): Designing Interval Type 2 Fuzzy PID (IT2FPID) controller for a time-delay linear system.
* [Ex6](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_6.py): Creating and plotting ten types of interval type two fuzzy sets. **(PyIT2FLS v0.4.0 and upper)**
* [Ex7](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_7.py): Similar to Ex3 but implemented using the new Mamdani class. **(PyIT2FLS v0.5.0 and upper)**
* [Ex8](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_8.py): Defining a simple multi-input multi-output IT2 TSK FLS. **(PyIT2FLS v0.5.0 and upper)**
* [Ex9](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_9.py): Defining a multi-input multi-output IT2 TSK FLS and plotting the 3D resulting output planes. **(PyIT2FLS v0.5.0 and upper)**
* [Ex10](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_10.py): Defining a multi-input multi-output IT2FLS with different domains for each of input and output variables, and plotting the output surfaces of the system. **(PyIT2FLS v0.5.0 and upper)**
* [Ex11](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_11.py): Generating random rule-bases. **(PyIT2FLS v0.5.0 and upper)**
* [Ex12](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_12.py): Using six different t-norms with meet operator. **(PyIT2FLS v0.6.0 and upper)**
* [Ex13](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_13.py): Using six different s-norms with join operator. **(PyIT2FLS v0.6.0 and upper)**
* [Ex14](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_14.py): MIMO Type 1 Mamdani Fuzzy Logic System. **(PyIT2FLS v0.6.0 and upper)**
* [Ex15](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_15.py): MIMO Type 1 TSK Fuzzy Logic System. **(PyIT2FLS v0.6.0 and upper)**
* [Ex16](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_16.py): Using emphasize function for type 1 and interval type 2 fuzzy sets. **(PyIT2FLS v0.7.0 and upper)**
* [Ex17](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_17.py): Example concerning fuzzy matrices. **(PyIT2FLS v0.7.0 and upper)**
* [Ex18](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_18.py): Defining random rules and random sets for IT2F classifier with three inputs and one output (Based on the request of one of the users). **(PyIT2FLS v0.7.0 and upper)**


### Some output plots

* Ex4:

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/4_2.png" width="256"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/4_4.png" width="256">

* Ex5:

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_1.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_2.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_3.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_4.png" width="128">

* Ex6:

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_1.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_2.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_3.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_4.png" width="128">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_5.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_6.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_7.png" width="128"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_8.png" width="128">

* Ex9: 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_1.png" width="512">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_2.png" width="512">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/IT2TSKFLSY1.png" width="256"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/IT2TSKFLSY2.png" width="256">

* Ex10: 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/10_1.png" width="256"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/10_3.png" width="256">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/10_5.png" width="256"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/10_6.png" width="256">
