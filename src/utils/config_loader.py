from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    def __init__(self, config_dir: str | Path):
        self.config_dir = Path(config_dir)

    def load_yaml(self, file_name: str) -> dict[str, Any]:
        path = self.config_dir / file_name
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Invalid config format in {path}: expected dict, got {type(data).__name__}")
        return data

    def load_all(self) -> dict[str, Any]:
        return {
            "drone": self.load_yaml("drone_config.yaml"),
            "swarm": self.load_yaml("swarm_config.yaml"),
            "formations": self.load_yaml("formations.yaml"),
        }
