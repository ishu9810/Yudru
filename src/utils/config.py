from pathlib import Path
from typing import Any

import yaml


class ConfigError(Exception):
    """Raised when configuration loading fails."""


def load_yaml(path: str | Path) -> dict[str, Any]:
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise ConfigError(f"Missing configuration file: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"Configuration must be a mapping: {cfg_path}")
    return data
