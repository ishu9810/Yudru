from __future__ import annotations

from typing import Iterable


def linear_interpolation_waypoints(start: tuple[float, float, float], end: tuple[float, float, float], steps: int = 10):
    if steps < 2:
        return [end]
    out = []
    for i in range(1, steps + 1):
        t = i / steps
        out.append(
            (
                start[0] + (end[0] - start[0]) * t,
                start[1] + (end[1] - start[1]) * t,
                start[2] + (end[2] - start[2]) * t,
            )
        )
    return out


def flatten_mission_segments(segments: Iterable[list[tuple[float, float, float]]]):
    for seg in segments:
        for waypoint in seg:
            yield waypoint
