import asyncio
import unittest

from src.drone import Drone
from src.swarm_manager import SafetyLimits, SwarmManager


def run(coro):
    return asyncio.run(coro)


class SwarmManagerTests(unittest.TestCase):
    def test_swarm_takeoff_and_formation(self) -> None:
        drones = [Drone(f"drone{i}", "udp://", "udp://video") for i in range(1, 6)]
        swarm = SwarmManager(drones)

        run(swarm.connect_all())
        run(swarm.synchronized_takeoff(3.0))
        run(swarm.execute_formation("line", spacing=2.0, altitude=3.0))

        self.assertTrue(all(drone.state.connected for drone in drones))
        self.assertTrue(all(drone.state.flying for drone in drones))
        self.assertTrue(all(drone.state.position[2] == 3.0 for drone in drones))

    def test_safety_monitor_detects_low_battery_and_collision(self) -> None:
        drones = [Drone("drone1", "udp://", ""), Drone("drone2", "udp://", "")]
        swarm = SwarmManager(drones, limits=SafetyLimits(min_distance_m=1.0, min_battery_voltage=15.0))

        run(swarm.connect_all())
        run(swarm.synchronized_takeoff(3.0))
        run(drones[0].goto(0, 0, 3))
        run(drones[1].goto(0.4, 0, 3))
        drones[0].update_telemetry(battery_voltage=14.0)

        result = swarm.monitor_safety()
        self.assertTrue(any("low battery" in alert for alert in result["alerts"]))
        self.assertEqual(len(result["collisions"]), 1)
