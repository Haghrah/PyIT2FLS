from .pyit2fls import *
from .fuzzymatrix import *
from .learning import *
from .FML import *
from .FCL import *

try:
    from .designerui import *
except ImportError:
    # The designer GUI depends on PyQt5, an optional extra
    # (`pip install pyit2fls[gui]`). The rest of the toolkit must remain
    # usable without it.
    pass
