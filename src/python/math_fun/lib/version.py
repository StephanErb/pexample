from platform import platform, python_implementation, python_version

import numpy as np


def describe():
    return '%s %s with Numpy %s on %s' % (
        python_implementation(), python_version(), np.__version__, platform())
