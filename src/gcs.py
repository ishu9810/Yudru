from __future__ import annotations

import time

from src.control.collision_detector import CollisionDetector
from src.control.failsafe_handler import FailsafeHandler
from src.control.formation_controller import FormationController
from src.control.mission_executor import MissionExecutor
from src.swarm_manager import SwarmManager
from src.utils.helpers import utc_now_iso
from src.utils.telemetry_logger import TelemetryLogger


class DroneSwarmGCS:
    def __init__(self, swarm_manager: SwarmManager, swarm_cfg: dict):
        self.swarm = swarm_manager
        self.telemetry_hz = int(swarm_cfg.get("telemetry_hz", 10))
        self.collision_detector = CollisionDetector(
            min_safe_distance_m=float(swarm_cfg.get("min_safe_distance_m", 10)),
            emergency_distance_m=float(swarm_cfg.get("emergency_distance_m", 5)),
            shift_m=float(swarm_cfg.get("avoidance_shift_m", 3)),
        )
        self.failsafe = FailsafeHandler(
            heartbeat_timeout_sec=float(swarm_cfg.get("heartbeat_timeout_sec", 5)),
            gps_min_satellites=int(swarm_cfg.get("gps_min_satellites", 8)),
            low_battery_percent=int(swarm_cfg.get("low_battery_percent", 20)),
        )
        self.formations = FormationController(self.swarm)
        self.missions = MissionExecutor(self.swarm)
        self.telemetry_logger = TelemetryLogger()

    def connect(self) -> None:
        self.swarm.connect_all()

    def arm_all(self):
        self.swarm.arm_all()

    def takeoff_all(self, altitude_m: float):
        self.swarm.takeoff_all(altitude_m)

    def land_all(self):
        self.swarm.land_all()

    def form(self, name: str, center_lat: float, center_lon: float, altitude_m: float):
        self.formations.apply_formation(name, center_lat, center_lon, altitude_m)

    def monitor_once(self) -> dict:
        snapshot = self.swarm.telemetry_snapshot()
        for row in snapshot:
            row["timestamp"] = utc_now_iso()
            self.telemetry_logger.log_row(row)

        events, avoidance_cmds = self.collision_detector.evaluate(self.swarm.drones)
        emergency = any(e.level == "EMERGENCY" for e in events)
        if emergency:
            for drone in self.swarm.drones:
                self.failsafe.execute(drone)
        else:
            for drone_id, lat, lon in avoidance_cmds:
                for drone in self.swarm.drones:
                    if drone.drone_id == drone_id:
                        drone.move_to(lat, lon, drone.state.alt_m or 5.0)

        for drone in self.swarm.drones:
            if self.failsafe.should_trigger(drone):
                self.failsafe.execute(drone)

        return {"snapshot": snapshot, "events": events}

    def run_forever(self):
        period = 1 / max(self.telemetry_hz, 1)
        while True:
            self.monitor_once()
            time.sleep(period)
