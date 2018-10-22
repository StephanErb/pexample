from math_fun.lib.version import describe


def test_describe():
    assert "Numpy" in describe()
    assert "Python" in describe()
