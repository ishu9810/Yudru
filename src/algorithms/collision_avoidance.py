from __future__ import annotations

import math


def perpendicular_avoidance_vector(dx_m: float, dy_m: float, shift_m: float = 3.0) -> tuple[float, float]:
    length = math.hypot(dx_m, dy_m)
    if length == 0:
        return shift_m, 0.0
    px, py = -dy_m / length, dx_m / length
    return px * shift_m, py * shift_m
