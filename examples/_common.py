from src.gcs import DroneSwarmGCS
from src.swarm_manager import SwarmManager
from src.utils.config_loader import ConfigLoader


def load_gcs(config_dir: str = "config") -> DroneSwarmGCS:
    cfg = ConfigLoader(config_dir).load_all()
    swarm = SwarmManager.from_config(cfg["drone"])
    return DroneSwarmGCS(swarm, cfg["swarm"])
