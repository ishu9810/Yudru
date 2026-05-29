from src.algorithms.path_planning import sequence_path


def build_mission(waypoints: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    return sequence_path(waypoints, segments_per_leg=5)
