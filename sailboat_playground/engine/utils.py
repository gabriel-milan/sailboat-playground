import math
import numpy as np
from sailboat_playground.constants import constants


def compute_angle(vec: np.ndarray):
    try:
        assert vec.shape == (2,)
    except AssertionError:
        raise AssertionError(
            f"Failed to compute angle on vector with shape different from (2,): Shape is {vec.shape}")
    ang = math.atan2(vec[1], vec[0])
    while ang < 0:
        ang += 2 * np.pi
    while ang > 2 * np.pi:
        ang -= 2 * np.pi
    return ang


def norm_to_vector(norm: float, angle_rad: float):
    return np.array([np.cos(angle_rad), np.sin(angle_rad)]) * norm
