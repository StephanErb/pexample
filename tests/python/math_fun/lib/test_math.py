from math_fun.lib.math import random_sum


def test_random_sum():
    assert random_sum(0) == 0
    assert 0 <= random_sum(1) <= 1
    assert 0 <= random_sum(1, 1, 1) <= 3


def test_expensive_sum():
    assert random_sum(125, 125, 125, 125) > 0
