from src.utils.helpers import euclidean_distance


def detect_collision_risks(
    positions: dict[str, tuple[float, float, float]], min_distance: float
) -> list[tuple[str, str, float]]:
    ids = list(positions.keys())
    collisions: list[tuple[str, str, float]] = []
    for i, left in enumerate(ids):
        for right in ids[i + 1 :]:
            dist = euclidean_distance(positions[left], positions[right])
            if dist < min_distance:
                collisions.append((left, right, dist))
    return collisions
