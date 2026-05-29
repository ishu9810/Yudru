from __future__ import annotations

import math


def circle_offsets(count: int, radius_m: float) -> list[tuple[float, float, float]]:
    return [
        (
            radius_m * math.cos(2 * math.pi * i / count),
            radius_m * math.sin(2 * math.pi * i / count),
            0.0,
        )
        for i in range(count)
    ]


def named_formation_offsets(name: str, drone_count: int, side_or_radius_m: float = 20.0) -> list[tuple[float, float, float]]:
    key = name.upper()
    if key == "SQUARE":
        if drone_count != 5:
            raise ValueError("SQUARE formation currently requires exactly 5 drones")
        return [(-10, -10, 0), (10, -10, 0), (-20, 0, 0), (20, 0, 0), (0, 10, 0)]
    if key == "LINE":
        half = (drone_count - 1) / 2
        return [((idx - half) * 10, 0.0, 0.0) for idx in range(drone_count)]
    if key == "TRIANGLE":
        if drone_count != 5:
            raise ValueError("TRIANGLE formation currently requires exactly 5 drones")
        return [(0, 12, 0), (-10, -6, 0), (10, -6, 0), (-5, 2, 0), (5, 2, 0)]
    if key == "GRID":
        if drone_count != 5:
            raise ValueError("GRID formation currently requires exactly 5 drones")
        return [(-10, -10, 0), (0, -10, 0), (10, -10, 0), (-10, 0, 0), (0, 0, 0)]
    if key == "CIRCLE":
        return circle_offsets(drone_count, radius_m=side_or_radius_m / 2)
    raise ValueError(f"Unknown formation {name}")
