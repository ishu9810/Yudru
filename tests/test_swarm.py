import unittest
from types import SimpleNamespace

from src.control.formation_controller import FormationController
from src.swarm_manager import SwarmManager


class DummyDrone:
    def __init__(self, drone_id):
        self.drone_id = drone_id
        self.moves = []

    def move_to(self, lat, lon, alt):
        self.moves.append((lat, lon, alt))


class TestSwarm(unittest.TestCase):
    def test_formation_assigns_targets(self):
        swarm = SimpleNamespace(drones=[DummyDrone(i) for i in range(5)])
        ctrl = FormationController(swarm)
        ctrl.apply_formation("LINE", 37.0, -122.0, 10)
        self.assertEqual("LINE", ctrl.current_formation)
        self.assertTrue(all(len(d.moves) == 1 for d in swarm.drones))


if __name__ == "__main__":
    unittest.main()
