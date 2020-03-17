PyIT2FLS
========

<img src="/PyIT2FLS_icon.png" width="256">

NumPy based toolkit for Interval Type 2 Fuzzy Logic Systems (IT2FLS) simulation.

## Licence
PyIT2FLS is published under MIT license. If you are using the developed toolkit, please cite preprint of our paper [PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems](https://arxiv.org/abs/1909.10051).

    @misc{haghrah2019pyit2fls,
        title={PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems},
        author={Amir Arslan Haghrah and Sehraneh Ghaemi},
        year={2019},
        eprint={1909.10051},
        archivePrefix={arXiv},
        primaryClass={eess.SY}
    }

## Installation
PyIT2FLS can be installed by unzipping the source code in a directory and using this command:

    (sudo) python3 setup.py install

Or you can use pip3:

    (sudo) pip3 install --upgrade pyit2fls

## Examples
There are five examples provided along with the toolkit which are as below:
* Ex1: Defining an Interval Type 2 Fuzzy Set (IT2FS)
* Ex2: Application of join and meet operators and plotting the outputs
* Ex3: Defining a simple (MIMO) IT2FLS
* Ex4: Prediction of the Mackey-Glass chaotic time series with PSO-based parameter tuning
* Ex5: Designing Interval Type 2 Fuzzy PID (IT2FPID) controller for a time-delay linear system
* Ex6: Create and plot ten types of interval type two fuzzy sets

## Some notes on running the examples
If you are using Anaconda, due to the inclusion of main ddeint package in its libraries pool, an error is raised while running the 5th example. This error is raised because the 5th example uses an updated version of ddeint which is included in the examples folder. For solving this issue, please change the ddeint.py's name to ddeint1.py (in examples folder) and change the 16th line of the ex_5.py as below:

```python
from ddeint1 import ddeint
```

