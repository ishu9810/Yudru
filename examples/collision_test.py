from src.algorithms.collision_avoidance import detect_collision_risks


if __name__ == "__main__":
    positions = {
        "drone1": (0.0, 0.0, 3.0),
        "drone2": (0.6, 0.0, 3.0),
        "drone3": (3.0, 0.0, 3.0),
    }
    print(detect_collision_risks(positions, min_distance=1.0))
