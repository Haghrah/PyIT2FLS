Typereduction
=============

Typereduction library contains Ctypes-based implementation of the type reduction algorithms ONLY for IT2FSs. It should be noted that some parts of the original type reduction algorithms have been edited for improving the execution speed.

### Installation

Typereduction can be installed by unzipping the source code in a directory and using this command inside the typereduction folder:

    pip3 install .

Or you can install from PyPI:

    pip3 install --upgrade typereduction

**Note that typereduction has only been tested with GNU C compiler on Linux. Please report any compatibility issues.**

### Connecting with PyIT2FLS

PyIT2FLS automatically detects whether the typereduction toolkit has been installed or not and uses it in computations if installed.




