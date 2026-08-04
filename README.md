PyIT2FLS
========

<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="384"/></p>

NumPy and SciPy based toolkit for Type 1 and Interval Type 2 Fuzzy Logic Systems.

## License
PyIT2FLS is published under the MIT license. If you use this toolkit in your work, please cite our paper [PyIT2FLS: An open-source Python framework for flexible and scalable development of type 1 and interval type 2 fuzzy logic models](https://www.sciencedirect.com/science/article/pii/S235271102500113X).

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
PyIT2FLS requires Python 3.6 or newer. Its core dependencies — NumPy, SciPy, and Matplotlib — are installed automatically by pip.

### From PyPI (recommended)
Install or upgrade to the latest release directly from PyPI:

    pip3 install --upgrade pyit2fls

### With the Designer GUI
The [PyIT2FLS Designer](markdown%20docs/DesignerGUI.md), a graphical tool for building, simulating, and saving/loading fuzzy systems, additionally depends on PyQt5. Install it with the optional `gui` extra:

    pip3 install --upgrade "pyit2fls[gui]"

Once installed, launch it with the `pyit2fls-designer` console script, or with `python3 -m pyit2fls.designerui`.

### From source
To install from a local clone of the repository instead, clone it (or download and unzip the source), then run this command from inside the resulting `PyIT2FLS` folder:

    git clone https://github.com/Haghrah/PyIT2FLS.git
    cd PyIT2FLS
    pip3 install .


## Versions

### Features coming up in the next version
- Supporting Generalized Type 2 Fuzzy Sets and Systems.

### Some notes on version 0.9.0
- Support for the [IEC 61131-7 Fuzzy Control Language (FCL)](IEC61131-7.md) standard, through the new **_FCL_** class (`pyit2fls.FCL`): parses the core Mamdani subset of FCL (`FUNCTION_BLOCK`/`VAR_INPUT`/`VAR_OUTPUT`/`FUZZIFY`/`DEFUZZIFY`/`RULEBLOCK`) into a runnable **_T1Mamdani_** system, and exports a system back out as FCL text.
- The [IEEE 1855 Fuzzy Markup Language (FML)](IEEE1855.md) support (**_FML_** class, `pyit2fls.FML`) has been completed:
    - The rule base's `andMethod`/`activationMethod` now actually select the underlying fuzzy inference engine, instead of always defaulting to *Product*.
    - Clause-level negation (FML's `NOT="true"`, FCL's `IS NOT`) is now supported.
    - Rules whose antecedent clauses are OR-connected now raise a clear error instead of being silently (and incorrectly) combined with AND — the underlying **_T1Mamdani_**/**_T1TSK_** engines only support AND-combined antecedents; model an OR relationship as two separate rules sharing the same consequent instead.
    - A new **_FML.export_fml_** method serializes a system back out as FML XML.
- Introduction of a GUI for facilitating system design: the **_PyIT2FLS Designer_**, a PyQt5 application for building, simulating, and saving/loading Type 1 Mamdani fuzzy systems as FML or FCL files. Launch it with the `pyit2fls-designer` console script (after installing the optional GUI extra, `pip install pyit2fls[gui]`), or with `python3 -m pyit2fls.designerui`. See [markdown docs/DesignerGUI.md](markdown%20docs/DesignerGUI.md) for a tutorial.
- A new **_points_mf_** membership function (arbitrary piecewise-linear point list), the native term representation used by FCL.

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
- Starting initial support of machine learning models based on fuzzy systems. Depending on whether they are optimized for execution time or for the linguistic interpretability of their results, these models offer different trade-offs in computational efficiency.
    - Type 1 TSK Model
    - Type 1 Mamdani Model
    - Interval Type 2 TSK Model
    - Interval Type 2 Mamdani Model
- Starting initial support of Takagi-Sugeno models, widely used in the control of dynamic systems:
    - Type 1 Takagi-Sugeno System
    - Interval Type 2 Takagi-Sugeno System
- Documentation has been enhanced and published on [readthedocs](https://pyit2fls.readthedocs.io/en/latest/). More enhancements are on the way with more tutorials and examples.
- Some functions we relied on were deprecated in SciPy, NumPy, and Matplotlib; this version updates PyIT2FLS accordingly.
- More exception handling has been added to this version of PyIT2FLS, though this work is not yet complete.
- Minor enhancements have been made in plotting functions.

While we strive for quality and reliability, no software is perfect. If you encounter any issues or have suggestions, we warmly welcome your feedback. Your input is invaluable and helps us continue improving PyIT2FLS for the community. Please report any bugs or share your thoughts by opening a new issue. Thank you for your support and for being part of our journey to make PyIT2FLS even better!

### Some notes on version 0.7.9
- Some bugs (concerning EIASC algorithm) have been fixed in this version.

### Some notes on version 0.7.8
- Some bugs have been fixed in this version.

### Some notes on version 0.7.0-0.7.7
- Supporting fuzzy matrices and related operators.
- Faster IT2 FLS evaluation (see the [typereduction](https://github.com/Haghrah/PyIT2FLS/tree/master/typereduction) package).
- Introduction of the emphasize function for both type 1 and interval type 2 fuzzy sets (see the [16th example](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_16.py)).
- New options have been added when calling plot functions (**_T1FS.plot_**, **_IT2FS.plot_**, **_T1FS_plot_**, **_IT2FS_plot_**, and **_TR_plot_**).
	- Users can specify the output file format (png, eps, pdf, etc.) when calling the plot function by setting the **_ext_** input parameter (default **_pdf_**).
	- Users can toggle the grid in the output plot by setting the **_grid_** input parameter (default **_True_**).
	- Users can set the x- and y-axis labels via the **_xlabel_** and **_ylabel_** input parameters, respectively. The default **_xlabel_** is **_Domain_**, and the default **_ylabel_** is **_Membership degree_**.

- There are some deprecated functions and classes. After version 1.0.0 is released, these will no longer be supported:
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
- Some bugs have been fixed in this version. Now, it is possible to use different domains for FLS inputs and outputs.

### Some notes on version 0.4
- Some bugs have been fixed in this version, especially in the type reduction algorithms. Thanks to Dr. K.B. Badri Narayanan for reporting the errors.
- Some new IT2FSs have been added to the toolkit.
- In previous versions, the height of the IT2FS_Gaussian_UncertStd and IT2FS_Gaussian_UncertMean IT2FSs was fixed to 1 by default. In the new version, the user must give the height value in the parameters list as the last element.

## Examples
Some initial examples of using PyIT2FLS are provided below. All the examples are tested
against only the latest version of PyIT2FLS and may be incompatible with older versions.
Please update PyIT2FLS to the latest version before running them.

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

* [Ex6](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_6.py): Creating and plotting some different types of interval type 2 fuzzy sets.

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

* [Ex15](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_15.py): Using the emphasize function for type 1 and interval type 2 fuzzy sets.

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

* [Ex25](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_25.py): Parsing an IEEE 1855 (FML) document into a Type 1 Mamdani system, evaluating it, and round-tripping it back to FML.

* [Ex26](https://github.com/Haghrah/PyIT2FLS/blob/master/examples/ex_26.py): Parsing an IEC 61131-7 (FCL) document into a Type 1 Mamdani system, evaluating it, and round-tripping it back to FCL.