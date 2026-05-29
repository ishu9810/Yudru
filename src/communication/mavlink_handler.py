from __future__ import annotations

import threading
import time
from typing import Callable, Optional

from pymavlink import mavutil

from src.communication.message_parser import parse_message

MAVLINK_TIME_BOOT_MS_MASK = 0xFFFFFFFF


class MAVLinkHandler:
    def __init__(self, connection_str: str, baudrate: int = 115200):
        self.connection_str = connection_str
        self.baudrate = baudrate
        self.master: Optional[mavutil.mavfile] = None
        self._listen_thread: Optional[threading.Thread] = None
        self._running = False
        self.last_heartbeat_ts = 0.0
        self._boot_monotonic = time.monotonic()

    def connect(self, heartbeat_timeout: float = 10.0) -> None:
        self.master = mavutil.mavlink_connection(self.connection_str, baud=self.baudrate)
        try:
            self.master.wait_heartbeat(timeout=heartbeat_timeout)
        except Exception as exc:
            raise ConnectionError(
                f"No heartbeat received from {self.connection_str} within {heartbeat_timeout}s"
            ) from exc
        self.last_heartbeat_ts = time.time()

    def disconnect(self) -> None:
        self._running = False
        if self._listen_thread and self._listen_thread.is_alive():
            self._listen_thread.join(timeout=1.0)
        self.master = None

    def start_listener(self, callback: Callable[[dict], None]) -> None:
        if self.master is None:
            raise RuntimeError("Connect before starting listener")

        self._running = True

        def _run() -> None:
            while self._running and self.master is not None:
                msg = self.master.recv_match(blocking=True, timeout=0.2)
                if msg is None:
                    continue
                parsed = parse_message(msg)
                if parsed.get("type") == "HEARTBEAT":
                    self.last_heartbeat_ts = time.time()
                callback(parsed)

        self._listen_thread = threading.Thread(target=_run, daemon=True)
        self._listen_thread.start()

    def send_command_long(
        self,
        command: int,
        param1: float = 0,
        param2: float = 0,
        param3: float = 0,
        param4: float = 0,
        param5: float = 0,
        param6: float = 0,
        param7: float = 0,
    ) -> None:
        if self.master is None:
            raise RuntimeError("Not connected")
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            command,
            0,
            param1,
            param2,
            param3,
            param4,
            param5,
            param6,
            param7,
        )

    def set_mode(self, mode: str) -> None:
        if self.master is None:
            raise RuntimeError("Not connected")
        mode_id = self.master.mode_mapping().get(mode)
        if mode_id is None:
            raise ValueError(f"Unsupported mode: {mode}")
        self.master.set_mode(mode_id)

    def set_position_target_global_int(self, lat: float, lon: float, alt: float, yaw_deg: float = 0.0) -> None:
        if self.master is None:
            raise RuntimeError("Not connected")
        time_boot_ms = int((time.monotonic() - self._boot_monotonic) * 1000) & MAVLINK_TIME_BOOT_MS_MASK
        self.master.mav.set_position_target_global_int_send(
            time_boot_ms,
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            0b0000111111111000,
            int(lat * 1e7),
            int(lon * 1e7),
            alt,
            0,
            0,
            0,
            0,
            0,
            0,
            yaw_deg,
            0,
        )

    def arm(self) -> None:
        self.send_command_long(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=1)

    def disarm(self) -> None:
        self.send_command_long(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=0)

    def takeoff(self, altitude_m: float) -> None:
        self.send_command_long(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, param7=altitude_m)

    def land(self) -> None:
        self.send_command_long(mavutil.mavlink.MAV_CMD_NAV_LAND)
