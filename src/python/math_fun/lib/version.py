from platform import platform, python_implementation, python_version

import numpy as np


def describe():
    return "{} {} with Numpy {} on {}".format(
        python_implementation(),
        python_version(),
        np.__version__,
        platform(),
    )
