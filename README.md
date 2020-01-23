PyIT2FLS
========
NumPy based toolkit for Interval Type 2 Fuzzy Logic Systems (IT2FLS) simulation.

## Licence
PyIT2FLS is published under GNU General Public License v3.0. If you are using the developed toolkit, please cite pre-print of our paper [PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems](https://arxiv.org/abs/1909.10051).

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

In the 4th example, the chaotic Mackey-Glass time series is predicted using PyIT2FLS toolkit. The designed IT2FLS has three inputs and an output. Inputs are three consecutive samples of the time series. For each input and for the ouput three IT2FSs are defined. The parameters of these sets are achieved using the Particle Swarm Optimization (PSO) algorithm to have minimum Mean Square Error (MSE). The full code of the example and the PSO solver are presented in examples folder.

See the pre-print of our paper [PyIT2FLS: A New Python Toolkit for Interval Type 2 Fuzzy Logic Systems](https://arxiv.org/abs/1909.10051) for more information.

## Some notes on running the examples
If you are using Anaconda, due to the inclusion of main ddeint package in its libraries pool, an error is raised while running the 5th example. This error is raised because the 5th example uses an updated version of ddeint which is included in the examples folder. For solving this issue, please change the ddeint.py's name to ddeint1.py (in examples folder) and change the 16th line of the ex_5.py as below:

```python
from ddeint1 import ddeint
```

