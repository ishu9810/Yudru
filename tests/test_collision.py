import time
import unittest
from types import SimpleNamespace

from src.control.collision_detector import CollisionDetector


class TestCollisionDetector(unittest.TestCase):
    def _drone(self, drone_id, lat, lon):
        return SimpleNamespace(drone_id=drone_id, lat=lat, lon=lon)

    def test_emergency_detection(self):
        detector = CollisionDetector(min_safe_distance_m=10, emergency_distance_m=5)
        d1 = self._drone(1, 37.0, -122.0)
        d2 = self._drone(2, 37.0, -122.00001)
        events, cmds = detector.evaluate([d1, d2])
        self.assertTrue(any(e.level == "EMERGENCY" for e in events))
        self.assertEqual([], cmds)

    def test_warning_generates_avoidance(self):
        detector = CollisionDetector(min_safe_distance_m=20, emergency_distance_m=5)
        d1 = self._drone(1, 37.0, -122.0)
        d2 = self._drone(2, 37.0, -122.0001)
        events, cmds = detector.evaluate([d1, d2])
        self.assertTrue(any(e.level == "WARNING" for e in events))
        self.assertEqual(1, len(cmds))


if __name__ == "__main__":
    unittest.main()
