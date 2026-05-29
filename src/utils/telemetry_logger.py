from __future__ import annotations

import csv
from pathlib import Path
from threading import Lock
from typing import Any


class TelemetryLogger:
    HEADER = [
        "timestamp",
        "drone_id",
        "lat",
        "lon",
        "alt_m",
        "battery_v",
        "battery_pct",
        "mode",
        "armed",
        "ground_speed_mps",
        "heading_deg",
    ]

    def __init__(self, output_file: str = "logs/telemetry.csv"):
        self.output_file = Path(output_file)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        if not self.output_file.exists():
            with self.output_file.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(self.HEADER)

    def log_row(self, row: dict[str, Any]) -> None:
        with self._lock, self.output_file.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([row.get(col, "") for col in self.HEADER])
