from __future__ import annotations

import time
from threading import Lock, Thread


class FailsafeHandler:
    def __init__(
        self,
        heartbeat_timeout_sec: float,
        gps_min_satellites: int,
        low_battery_percent: int,
        hold_seconds: float = 5.0,
    ):
        self.heartbeat_timeout_sec = heartbeat_timeout_sec
        self.gps_min_satellites = gps_min_satellites
        self.low_battery_percent = low_battery_percent
        self.hold_seconds = hold_seconds
        self._active_drones: set[int] = set()
        self._lock = Lock()

    def should_trigger(self, drone) -> bool:
        now = time.time()
        if now - drone.last_telemetry_ts > self.heartbeat_timeout_sec:
            return True
        if drone.satellites_visible is not None and drone.satellites_visible < self.gps_min_satellites:
            return True
        if drone.battery_pct is not None and drone.battery_pct < self.low_battery_percent:
            return True
        return False

    def execute(self, drone) -> None:
        with self._lock:
            if drone.drone_id in self._active_drones:
                return
            self._active_drones.add(drone.drone_id)

        drone.set_mode("RTL")

        def _complete_landing() -> None:
            try:
                time.sleep(self.hold_seconds)
                drone.land()
            finally:
                with self._lock:
                    self._active_drones.discard(drone.drone_id)

        Thread(target=_complete_landing, daemon=True).start()
