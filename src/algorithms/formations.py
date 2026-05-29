from math import cos, pi, sin, sqrt


def line_formation(count: int, spacing: float, altitude: float) -> list[tuple[float, float, float]]:
    offset = (count - 1) / 2
    return [((idx - offset) * spacing, 0.0, altitude) for idx in range(count)]


def square_formation(count: int, spacing: float, altitude: float) -> list[tuple[float, float, float]]:
    side = int(sqrt(count))
    if side * side != count:
        side += 1
    points: list[tuple[float, float, float]] = []
    half = (side - 1) / 2
    for i in range(side):
        for j in range(side):
            if len(points) < count:
                points.append(((i - half) * spacing, (j - half) * spacing, altitude))
    return points


def circle_formation(count: int, spacing: float, altitude: float) -> list[tuple[float, float, float]]:
    radius = max(spacing, (count * spacing) / (2 * pi))
    return [
        (radius * cos((2 * pi * idx) / count), radius * sin((2 * pi * idx) / count), altitude)
        for idx in range(count)
    ]


def triangle_formation(count: int, spacing: float, altitude: float) -> list[tuple[float, float, float]]:
    points: list[tuple[float, float, float]] = []
    row = 1
    y = 0.0
    while len(points) < count:
        start_x = -((row - 1) * spacing) / 2
        for i in range(row):
            if len(points) < count:
                points.append((start_x + i * spacing, y, altitude))
        row += 1
        y += spacing * 0.866
    return points


def grid_formation(count: int, spacing: float, altitude: float) -> list[tuple[float, float, float]]:
    return square_formation(count, spacing, altitude)


def get_formation(pattern: str, count: int, spacing: float, altitude: float) -> list[tuple[float, float, float]]:
    generators = {
        "line": line_formation,
        "square": square_formation,
        "circle": circle_formation,
        "triangle": triangle_formation,
        "grid": grid_formation,
    }
    if pattern not in generators:
        raise ValueError(f"Unsupported formation pattern: {pattern}")
    return generators[pattern](count, spacing, altitude)


def interpolate_transition(
    start: list[tuple[float, float, float]],
    target: list[tuple[float, float, float]],
    steps: int,
) -> list[list[tuple[float, float, float]]]:
    if len(start) != len(target):
        raise ValueError("Start and target formations must have equal number of points")
    frames: list[list[tuple[float, float, float]]] = []
    for step in range(1, steps + 1):
        t = step / steps
        frames.append(
            [
                (
                    s[0] + (g[0] - s[0]) * t,
                    s[1] + (g[1] - s[1]) * t,
                    s[2] + (g[2] - s[2]) * t,
                )
                for s, g in zip(start, target)
            ]
        )
    return frames
