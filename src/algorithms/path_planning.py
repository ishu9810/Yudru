from __future__ import annotations

from typing import Generator, Iterable


def linear_interpolation_waypoints(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    steps: int = 10,
) -> list[tuple[float, float, float]]:
    """Generate interpolated waypoints between start and end coordinates.

    Args:
        start: Starting waypoint (lat, lon, alt).
        end: Ending waypoint (lat, lon, alt).
        steps: Number of interpolation steps. Values below 2 return end only.
    """
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


def flatten_mission_segments(
    segments: Iterable[list[tuple[float, float, float]]],
) -> Generator[tuple[float, float, float], None, None]:
    """Flatten nested mission segments into a single waypoint stream."""
    for seg in segments:
        for waypoint in seg:
            yield waypoint
