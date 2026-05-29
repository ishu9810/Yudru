from __future__ import annotations

import queue
import time
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from pymavlink import mavutil

from src.communication.mavlink_handler import MAVLinkHandler


@dataclass
class DroneState:
    lat: float | None = None
    lon: float | None = None
    alt_m: float | None = None
    battery_v: float | None = None
    battery_pct: int | None = None
    mode: str = "UNKNOWN"
    armed: bool = False
    flying: bool = False
    heading_deg: float | None = None
    ground_speed_mps: float | None = None
    satellites_visible: int | None = None
    last_telemetry_ts: float = field(default_factory=time.time)


class DroneController:
    def __init__(self, drone_id: int, connection: str, baudrate: int = 115200):
        self.drone_id = drone_id
        self.mavlink = MAVLinkHandler(connection, baudrate=baudrate)
        self.state = DroneState()
        self._state_lock = Lock()
        self._command_queue: queue.Queue[tuple[str, tuple[Any, ...]]] = queue.Queue()

    @property
    def lat(self):
        return self.state.lat

    @property
    def lon(self):
        return self.state.lon

    @property
    def last_telemetry_ts(self):
        return self.state.last_telemetry_ts

    @property
    def satellites_visible(self):
        return self.state.satellites_visible

    @property
    def battery_pct(self):
        return self.state.battery_pct

    def connect(self) -> None:
        self.mavlink.connect()
        self.mavlink.start_listener(self._on_message)

    def _on_message(self, payload: dict[str, Any]) -> None:
        with self._state_lock:
            self.state.last_telemetry_ts = time.time()
            p_type = payload.get("type")
            if p_type == "GLOBAL_POSITION_INT":
                self.state.lat = payload.get("lat")
                self.state.lon = payload.get("lon")
                self.state.alt_m = payload.get("alt_m")
                self.state.heading_deg = payload.get("heading_deg")
                self.state.flying = (self.state.alt_m or 0) > 0.5
            elif p_type == "SYS_STATUS":
                self.state.battery_v = payload.get("battery_v")
                self.state.battery_pct = payload.get("battery_pct")
            elif p_type == "GPS_RAW_INT":
                self.state.satellites_visible = payload.get("satellites_visible")
            elif p_type == "HEARTBEAT":
                self.state.armed = bool(payload.get("base_mode", 0) & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)

    def enqueue(self, command: str, *args: Any) -> None:
        self._command_queue.put((command, args))

    def drain_commands(self) -> None:
        while not self._command_queue.empty():
            command, args = self._command_queue.get_nowait()
            getattr(self, command)(*args)

    def set_mode(self, mode: str) -> None:
        self.mavlink.set_mode(mode)
        self.state.mode = mode

    def arm(self) -> None:
        self.mavlink.arm()

    def disarm(self) -> None:
        self.mavlink.disarm()

    def takeoff(self, altitude_m: float) -> None:
        self.mavlink.takeoff(altitude_m)

    def land(self) -> None:
        self.mavlink.land()

    def move_to(self, lat: float, lon: float, alt_m: float) -> None:
        self.mavlink.set_position_target_global_int(lat, lon, alt_m)

    def snapshot(self) -> dict[str, Any]:
        with self._state_lock:
            return {
                "drone_id": self.drone_id,
                "lat": self.state.lat,
                "lon": self.state.lon,
                "alt_m": self.state.alt_m,
                "battery_v": self.state.battery_v,
                "battery_pct": self.state.battery_pct,
                "mode": self.state.mode,
                "armed": self.state.armed,
                "flying": self.state.flying,
                "heading_deg": self.state.heading_deg,
                "ground_speed_mps": self.state.ground_speed_mps,
                "satellites_visible": self.state.satellites_visible,
                "last_telemetry_ts": self.state.last_telemetry_ts,
            }
