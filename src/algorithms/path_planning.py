def interpolate_waypoints(
    start: tuple[float, float, float], end: tuple[float, float, float], segments: int
) -> list[tuple[float, float, float]]:
    if segments <= 0:
        raise ValueError("segments must be positive")
    return [
        (
            start[0] + (end[0] - start[0]) * (idx / segments),
            start[1] + (end[1] - start[1]) * (idx / segments),
            start[2] + (end[2] - start[2]) * (idx / segments),
        )
        for idx in range(segments + 1)
    ]


def sequence_path(points: list[tuple[float, float, float]], segments_per_leg: int = 10) -> list[tuple[float, float, float]]:
    if len(points) < 2:
        return points
    path: list[tuple[float, float, float]] = []
    for idx in range(len(points) - 1):
        leg = interpolate_waypoints(points[idx], points[idx + 1], segments_per_leg)
        path.extend(leg if idx == 0 else leg[1:])
    return path
