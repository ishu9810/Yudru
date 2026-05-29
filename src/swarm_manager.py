import asyncio
from dataclasses import dataclass

from src.algorithms.collision_avoidance import detect_collision_risks
from src.algorithms.formations import get_formation
from src.drone import Drone


@dataclass
class SafetyLimits:
    min_distance_m: float = 1.5
    min_battery_voltage: float = 14.0
    min_gps_fix: int = 2
    geofence_radius_m: float = 250.0


class SwarmManager:
    def __init__(self, drones: list[Drone], limits: SafetyLimits | None = None) -> None:
        self.drones = drones
        self.limits = limits or SafetyLimits()

    async def connect_all(self) -> None:
        await asyncio.gather(*(drone.connect() for drone in self.drones))

    async def synchronized_takeoff(self, altitude: float) -> None:
        await asyncio.gather(*(drone.arm() for drone in self.drones))
        await asyncio.gather(*(drone.takeoff(altitude) for drone in self.drones))

    async def synchronized_landing(self) -> None:
        await asyncio.gather(*(drone.land() for drone in self.drones))

    async def execute_formation(self, pattern: str, spacing: float, altitude: float) -> None:
        points = get_formation(pattern, len(self.drones), spacing, altitude)
        await asyncio.gather(*(drone.goto(*point) for drone, point in zip(self.drones, points)))

    def positions(self) -> dict[str, tuple[float, float, float]]:
        return {drone.drone_id: drone.state.position for drone in self.drones}

    def monitor_safety(self) -> dict[str, list[str] | list[tuple[str, str, float]]]:
        alerts: list[str] = []
        flying_positions: dict[str, tuple[float, float, float]] = {}
        for drone in self.drones:
            if drone.state.battery_voltage < self.limits.min_battery_voltage:
                alerts.append(f"{drone.drone_id}: low battery")
            if drone.state.gps_fix < self.limits.min_gps_fix:
                alerts.append(f"{drone.drone_id}: weak gps")
            x, y, _ = drone.state.position
            if (x**2 + y**2) ** 0.5 > self.limits.geofence_radius_m:
                alerts.append(f"{drone.drone_id}: geofence breach")
            if drone.state.flying:
                flying_positions[drone.drone_id] = drone.state.position

        collisions = detect_collision_risks(flying_positions, self.limits.min_distance_m)
        return {"alerts": alerts, "collisions": collisions}

    async def emergency_land_all(self) -> None:
        await self.synchronized_landing()
