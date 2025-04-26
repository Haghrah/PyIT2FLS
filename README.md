PyIT2FLS
========

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="384"/></p>

NumPy and SciPy based toolkit for Type 1 and Interval Type 2 Fuzzy Logic Systems.

## Licence
PyIT2FLS is published under MIT license. If you are using the developed toolkit, please cite our paper [PyIT2FLS: An open-source Python framework for flexible and scalable development of type 1 and interval type 2 fuzzy logic models](https://www.sciencedirect.com/science/article/pii/S235271102500113X).

BibTeX:

    @article{haghrah2025pyit2fls,
        title={PyIT2FLS: An open-source Python framework for flexible and scalable development of type 1 and interval type 2 fuzzy logic models},
        author={Haghrah, Amir Arslan and Ghaemi, Sehraneh and Badamchizadeh, Mohammad Ali},
        journal={SoftwareX},
        volume={30},
        pages={102146},
        year={2025},
        publisher={Elsevier}
    }

MLA:

    Haghrah, Amir Arslan, Sehraneh Ghaemi, and Mohammad Ali Badamchizadeh. "PyIT2FLS: An open-source Python framework for flexible and scalable development of type 1 and interval type 2 fuzzy logic models." SoftwareX 30 (2025): 102146.


## Installation
PyIT2FLS can be installed by unzipping the source code in a directory and using this command inside the PyIT2FLS folder:

    pip3 install .

Or you can install from PyPI:

    pip3 install --upgrade pyit2fls

## Support My Work with Tether (USDT)
If you find this Python library useful and would like to support its development, donations are greatly appreciated. To donate USDT, please send to the following wallet address: 0x2c0fb11b56b10b5ddda6a8c9c1f6d0b559153de2. Ensure you select the Avalanche C-Chain network when making the transaction. Using the wrong network, such as Ethereum, may result in lost funds.

Thank you for your contribution, which helps maintain and improve this project!


## Versions

### Features coming up in the next version
- Supporting Generalized Type 2 Fuzzy Sets and Systems.
- Supporting FCL.
- Introduction of a GUI for facilitating system design.

### Some notes on version 0.8.6
- Minor bug fix concerning the *IT2Mamdani_ML_Model* class.

### Some notes on version 0.8.5
- Removing a deprecated numpy module ...

### Some notes on version 0.8.4
- Just some minor edits and improvements ...

### Some notes on version 0.8.3
- Supporting new optimization algorithms ...

### Some notes on version 0.8.1-0.8.2
- Just some minor edits and improvements ...

### Some notes on version 0.8.0
- Starting initial support of machine learning models based on fuzzy systems. Based on optimization for execution time or linguistic interpretability of the results, these models may have different computational efficiencies. 
    - Type 1 TSK Model
    - Type 1 Mamdani Model
    - Interval Type 2 TSK Model
    - Interval Type 2 Mamdani Model
- Starting initial support of Takagi-Sugeno models, widely used in dynamic systems control:
    - Type 1 Takagi-Sugeno System
    - Interval Type 2 Takagi-Sugeno System
- Documentations have been enhanced and published over [readthedocs](https://pyit2fls.readthedocs.io/en/latest/). More enhancements are on the way with more tutorials and examples.
- Some functions were deprecated in SciPy, NumPy, and Matplotlib. There are updates concerning this issue.
- More exception handling have been done in the new version of the PyIT2FLS, but not completed, yet.
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

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/1_1.png" width="200"></p>

* [Ex2](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_2.py): Using join and meet operators and plotting the outputs.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/2_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/2_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/2_3.png" width="200"></p>

* [Ex3](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_3.py): Defining a simple (MIMO) IT2Mamdani.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_1.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_3.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/3_5.png" width="200"></p>

* [Ex4](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_4.py): Prediction of the Mackey-Glass chaotic time series with PSO-based parameter tuning.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/4_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/4_4.png" width="200"></p>

* [Ex5](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_5.py): Designing Interval Type 2 Fuzzy PID (IT2FPID) controller for a time-delay linear system.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/5_3.png" width="200"></p>

* [Ex6](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_6.py): Creating and plotting some different types of interval type two fuzzy sets.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_3.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_5.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_6.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_7.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/6_8.png" width="200"></p>


* [Ex7](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_7.py): Defining a simple multi-input multi-output IT2 TSK FLS.

* [Ex8](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_8.py): Defining a multi-input multi-output IT2 TSK FLS and plotting the resulting 3D output planes.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_1.png" width="600"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_2.png" width="600"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_3.png" width="300"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/8_4.png" width="300"></p>

* [Ex9](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_9.py): Defining a multi-input multi-output IT2FLS with different domains for each of input and output variables, and plotting the output surfaces of the system.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_2.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_3.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_4.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_5.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/9_6.png" width="200"></p>

* [Ex10](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_10.py): Generating random rule-bases.



* [Ex11](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_11.py): Using six different t-norms with meet operator.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/11_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/11_2.png" width="200"></p>

* [Ex12](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_12.py): Using six different s-norms with join operator.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/12_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/12_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/12_3.png" width="200"></p>

* [Ex13](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_13.py): MIMO Type 1 Mamdani Fuzzy Logic System.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_2.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_3.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_4.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_5.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/13_6.png" width="200"></p>

* [Ex14](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_14.py): MIMO Type 1 TSK Fuzzy Logic System.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_1.png" width="600"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_2.png" width="600"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_3.png" width="300"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/14_5.png" width="200"></p>

* [Ex15](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_15.py): Using emphasize function for type 1 and interval type 2 fuzzy sets.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/15_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/15_2.png" width="200"></p>

* [Ex16](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_16.py): Example concerning fuzzy matrices.

* [Ex17](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_17.py): Defining random rules and random sets for IT2F classifier with three inputs and one output (Based on the request of one of the users).

* [Ex18](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_18.py): Fitting a 3D surface using type 1 TSK model and PSO algorithm.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_2.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_3.png" width="400"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_5.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_6.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/18_7.png" width="200"></p>

* [Ex19](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_19.py): Fitting a 3D surface using type 1 Mamdani model and GA algorithm.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_2.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_3.png" width="400"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_4.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_5.png" width="200"></p>

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_6.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/19_7.png" width="200"></p>

* [Ex20](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_20.py): Fitting a 3D surface using interval type 2 TSK model and GA algorithm.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/20_3.png" width="400"></p>

* [Ex21](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_21.py): Fitting a 3D surface using interval type 2 Mamdani model and PSO algorithm.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/21_3.png" width="400"></p>

* [Ex22](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_22.py): Using type 1 Takagi-Sugeno model for approximating a nonlinear system.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/22_1.png" width="200"></p>

* [Ex23](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_23.py): Using interval type 2 Takagi-Sugeno model for approximating a nonlinear system.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/23_1.png" width="200"></p>

* [Ex24](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_24.py): Example for new *MEET* and *JOIN* functions accepting many *IT2FS* s as input.

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/24_1.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/24_2.png" width="200"> <img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/examples/images/24_3.png" width="200"></p>