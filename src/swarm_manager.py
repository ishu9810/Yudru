from __future__ import annotations

from typing import Any

from src.drone import DroneController


class SwarmManager:
    def __init__(self, drones: list[DroneController]):
        self.drones = drones

    @classmethod
    def from_config(cls, drone_cfg: dict[str, Any]):
        drones = [
            DroneController(
                drone_id=d["id"],
                connection=d["connection"],
                baudrate=d.get("baudrate", 115200),
            )
            for d in drone_cfg["drones"]
        ]
        return cls(drones)

    def connect_all(self):
        for drone in self.drones:
            drone.connect()

    def arm_all(self):
        for drone in self.drones:
            drone.enqueue("set_mode", "GUIDED")
            drone.enqueue("arm")
        self.flush_command_queues()

    def disarm_all(self):
        for drone in self.drones:
            drone.enqueue("disarm")
        self.flush_command_queues()

    def takeoff_all(self, altitude_m: float):
        for drone in self.drones:
            drone.enqueue("takeoff", altitude_m)
        self.flush_command_queues()

    def land_all(self):
        for drone in self.drones:
            drone.enqueue("land")
        self.flush_command_queues()

    def move_all(self, lat: float, lon: float, alt_m: float):
        for drone in self.drones:
            drone.enqueue("move_to", lat, lon, alt_m)
        self.flush_command_queues()

    def flush_command_queues(self):
        for drone in self.drones:
            drone.drain_commands()

    def telemetry_snapshot(self):
        return [drone.snapshot() for drone in self.drones]
