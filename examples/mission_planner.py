from src.mission_planner import build_mission


if __name__ == "__main__":
    waypoints = [(0, 0, 3), (10, 0, 3), (10, 10, 3), (0, 10, 3)]
    mission = build_mission(waypoints)
    print("Mission points:", mission)
