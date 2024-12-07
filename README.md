PyIT2FLS
========

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="384"/></p>

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
PyIT2FLS can be installed by unzipping the source code in a directory and using this command inside the PyIT2FLS folder:

    pip3 install .

Or you can install from PyPI:

    pip3 install --upgrade pyit2fls

## Support My Work with Tether (USDT)
If you find this Python library useful and would like to support its development, donations are greatly appreciated. You can send Tether (USDT) directly to the following address:

    TN1stagYLtqq4MUKPj6Q3fqtH3GittRawE

Thank you for your contribution, which helps maintain and improve this project!


## Versions

### Features coming up in the next version
- Supporting Generalized Type 2 Fuzzy Sets and Systems.

### Some notes on version 0.8.0
- Starting initial support of machine learning models based on fuzzy systems. Based on 
  optimization for execution time or linguistic interpretability of the results, these 
  models may have different computational efficiency. 
    - Type 1 TSK Model
    - Type 1 Mamdani Model
    - Interval Type 2 TSK Model
    - Interval Type 2 Mamdani Model
- Starting initial support of Takagi-Sugeno models, widely used in dynamic systems control:
    - Type 1 Takagi-Sugeno System
    - Interval Type 2 Takagi-Sugeno System
- Documentations have been enhanced and published over [readthedocs](https://pyit2fls.readthedocs.io/en/latest/). 
  More enhancement are on the way with more tutorials and examples.
- Some functions were deprecated in SciPy, NumPy, and Matplotlib. There are updates 
  concerning this issue.
- More exception handling have been done in the new version of the PyIT2FLS, but not 
  completed, yet.
- Minor enhancements have been made in plotting functions.

While we strive for quality and reliability, no software is perfect. If you encounter any issues or have suggestions, we warmly welcome your feedback. Your input is invaluable and helps us continue improving PyIT2FLS for the community. Please report any bugs or share your thoughts via opening a new issue. Thank you for your support and for being part of our journey to make PyIT2FLS even better!

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
- Some bugs have been fixed in this version.

### Some notes on version 0.5
- Supporting both Mamdani and TSK systems.
- Some bugs have been fixed in this vesion. Now, it is possible to use different domains for FLS inputs and outputs.

### Some notes on version 0.4
- Some bugs have been fixed in this version especially in type reduction algorithms. I would like to say thanks to Dr. K.B Badri Narayanan for reporting the errors.
- Some new IT2FSs have been added to the toolkit.
- In previous versions, the height of the IT2FS_Gaussian_UncertStd and IT2FS_Gaussian_UncertMean IT2FSs was fixed to 1, by default. But in the new version, user must give the height value in the parameters list as the last element.

## Examples
Some initial examples of using PyIT2FLS are provided below. All the examples are tested 
with just the latest version of the PyIT2FLS and they may be incompatible with older versions. 
So, please update your PyIT2FLS to the latest version. 

* [Ex1](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_1.py): Defining an Interval Type 2 Fuzzy Set (IT2FS).

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/1_1.png" width="200">

* [Ex2](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_2.py): Using join and meet operators and plotting the outputs.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/2_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/2_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/2_3.png" width="200">

* [Ex3](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_3.py): Defining a simple (MIMO) IT2Mamdani.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_1.png" width="200">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_3.png" width="200">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_5.png" width="200">

* [Ex4](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_4.py): Prediction of the Mackey-Glass chaotic time series with PSO-based parameter tuning.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/4_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/4_4.png" width="200">

* [Ex5](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_5.py): Designing Interval Type 2 Fuzzy PID (IT2FPID) controller for a time-delay linear system.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_3.png" width="200"> 

* [Ex6](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_6.py): Creating and plotting some different types of interval type two fuzzy sets.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_3.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_5.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_6.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_7.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_8.png" width="200">


* [Ex7](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_7.py): Defining a simple multi-input multi-output IT2 TSK FLS.

* [Ex8](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_8.py): Defining a multi-input multi-output IT2 TSK FLS and plotting the resulting 3D output planes.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_1.png" width="600"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_2.png" width="600"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_3.png" width="300"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_4.png" width="300"> 

* [Ex9](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_9.py): Defining a multi-input multi-output IT2FLS with different domains for each of input and output variables, and plotting the output surfaces of the system.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_2.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_3.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_4.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_5.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_6.png" width="200"> 

* [Ex10](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_10.py): Generating random rule-bases.



* [Ex11](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_11.py): Using six different t-norms with meet operator.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/11_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/11_2.png" width="200"> 

* [Ex12](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_12.py): Using six different s-norms with join operator.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/12_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/12_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/12_3.png" width="200"> 

* [Ex13](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_13.py): MIMO Type 1 Mamdani Fuzzy Logic System.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_2.png" width="200">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_3.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_4.png" width="200">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_5.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_6.png" width="200">

* [Ex14](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_14.py): MIMO Type 1 TSK Fuzzy Logic System.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_1.png" width="600">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_2.png" width="600"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_3.png" width="300">

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_5.png" width="200">

* [Ex15](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_15.py): Using emphasize function for type 1 and interval type 2 fuzzy sets.

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/15_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/15_2.png" width="200">

* [Ex16](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_16.py): Example concerning fuzzy matrices.

* [Ex17](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_17.py): Defining random rules and random sets for IT2F classifier with three inputs and one output (Based on the request of one of the users).

* [Ex18](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_18.py): 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_2.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_3.png" width="400"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_5.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_6.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_7.png" width="200"> 

* [Ex19](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_19.py): 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_2.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_3.png" width="400"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_5.png" width="200"> 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_6.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_7.png" width="200"> 

* [Ex20](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_20.py): 



* [Ex21](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_21.py): 



* [Ex22](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_22.py): 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/22_1.png" width="200"> 

* [Ex23](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_23.py): 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/23_1.png" width="200"> 

* [Ex24](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_24.py): 

<img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/24_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/24_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/24_3.png" width="200"> 