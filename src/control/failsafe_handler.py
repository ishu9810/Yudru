from __future__ import annotations

import time


class FailsafeHandler:
    def __init__(self, heartbeat_timeout_sec: float, gps_min_satellites: int, low_battery_percent: int):
        self.heartbeat_timeout_sec = heartbeat_timeout_sec
        self.gps_min_satellites = gps_min_satellites
        self.low_battery_percent = low_battery_percent

    def should_trigger(self, drone) -> bool:
        now = time.time()
        if now - drone.last_telemetry_ts > self.heartbeat_timeout_sec:
            return True
        if drone.satellites_visible is not None and drone.satellites_visible < self.gps_min_satellites:
            return True
        if drone.battery_pct is not None and drone.battery_pct <= self.low_battery_percent:
            return True
        return False

    def execute(self, drone) -> None:
        drone.set_mode("RTL")
        time.sleep(5)
        drone.land()
