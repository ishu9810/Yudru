from __future__ import annotations

import json
import time
from pathlib import Path


class MissionExecutor:
    def __init__(self, swarm_manager):
        self.swarm_manager = swarm_manager

    def load_mission(self, mission_file: str):
        with Path(mission_file).open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def execute(self, mission_file: str, dwell_sec: float = 2.0):
        waypoints = self.load_mission(mission_file)
        required_keys = {"lat", "lon", "alt"}
        for idx, wp in enumerate(waypoints):
            if not isinstance(wp, dict) or not required_keys.issubset(wp.keys()):
                raise ValueError(f"Invalid waypoint at index {idx}: expected keys {sorted(required_keys)}")
            self.swarm_manager.move_all(wp["lat"], wp["lon"], wp["alt"])
            time.sleep(dwell_sec)
