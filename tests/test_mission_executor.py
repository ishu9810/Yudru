import json
import os
import tempfile
import unittest

from src.control.mission_executor import MissionExecutor


class DummySwarm:
    def __init__(self):
        self.calls = []

    def move_all(self, lat, lon, alt):
        self.calls.append((lat, lon, alt))


class TestMissionExecutor(unittest.TestCase):
    def test_execute_mission_waypoints(self):
        mission = [
            {"lat": 37.0, "lon": -122.0, "alt": 10},
            {"lat": 37.1, "lon": -122.1, "alt": 11},
        ]
        with tempfile.NamedTemporaryFile("w", suffix=".mission", delete=False) as tf:
            json.dump(mission, tf)
            mission_file = tf.name

        try:
            swarm = DummySwarm()
            executor = MissionExecutor(swarm)
            executor.execute(mission_file, dwell_sec=0)
            self.assertEqual([(37.0, -122.0, 10), (37.1, -122.1, 11)], swarm.calls)
        finally:
            os.unlink(mission_file)

    def test_execute_rejects_bad_waypoint(self):
        mission = [{"lat": 37.0, "lon": -122.0}]
        with tempfile.NamedTemporaryFile("w", suffix=".mission", delete=False) as tf:
            json.dump(mission, tf)
            mission_file = tf.name

        try:
            swarm = DummySwarm()
            executor = MissionExecutor(swarm)
            with self.assertRaises(ValueError):
                executor.execute(mission_file, dwell_sec=0)
        finally:
            os.unlink(mission_file)


if __name__ == "__main__":
    unittest.main()
