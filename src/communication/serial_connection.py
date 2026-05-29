from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

import serial


@dataclass
class SerialConfig:
    port: str
    baudrate: int = 115200
    timeout: float = 0.2


class SerialConnection:
    def __init__(self, config: SerialConfig):
        self.config = config
        self._conn: Optional[serial.Serial] = None

    def connect(self) -> None:
        self._conn = serial.Serial(
            self.config.port,
            self.config.baudrate,
            timeout=self.config.timeout,
        )

    def ensure_connected(self, retries: int = 3, retry_delay: float = 0.5) -> None:
        if self._conn and self._conn.is_open:
            return
        last_error: Exception | None = None
        for _ in range(retries):
            try:
                self.connect()
                return
            except serial.SerialException as exc:
                last_error = exc
                time.sleep(retry_delay)
        raise ConnectionError(f"Unable to connect to {self.config.port}") from last_error

    def write(self, payload: bytes) -> None:
        self.ensure_connected()
        assert self._conn is not None
        self._conn.write(payload)

    def read(self, size: int = 1) -> bytes:
        self.ensure_connected()
        assert self._conn is not None
        return self._conn.read(size)

    def close(self) -> None:
        if self._conn and self._conn.is_open:
            self._conn.close()
