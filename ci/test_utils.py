import numpy as np
from sailboat_playground.engine.utils import *


def run_compute_angle(x, y):
    return round(compute_angle(np.array([x, y])) / np.pi * 180)


def test_compute_angle():
    cases = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (0.99999, -0.0001),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
    ]
    ans = [
        0,
        90,
        180,
        270,
        360,
        45,
        135,
        225,
        315,
    ]
    for i, case in enumerate(cases):
        assert run_compute_angle(*case) == ans[i]
    try:
        compute_angle(np.array([1, 2, 3]))
    except AssertionError:
        pass
    except Exception as e:
        raise e


def test_norm_to_vector():
    cases = [
        (1, 45 * np.pi / 180),
        (1, 0)
    ]
    ans = [
        [np.sqrt(2)/2, np.sqrt(2)/2],
        [1, 0]
    ]
    for i, case in enumerate(cases):
        vec = norm_to_vector(*case)
        assert round(vec[0], 7) == round(ans[i][0], 7)
        assert round(vec[1], 7) == round(ans[i][1], 7)
