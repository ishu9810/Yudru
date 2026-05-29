from __future__ import annotations

import argparse

from src.gcs import DroneSwarmGCS
from src.swarm_manager import SwarmManager
from src.utils.config_loader import ConfigLoader
from src.utils.logger import build_logger


def main() -> None:
    parser = argparse.ArgumentParser(description="5-drone real-world swarm GCS")
    parser.add_argument(
        "--config-dir",
        default="config",
        help="Path to config directory containing drone_config.yaml, swarm_config.yaml, and formations.yaml",
    )
    parser.add_argument("--run-loop", action="store_true", help="Run continuous monitor loop")
    args = parser.parse_args()

    logger = build_logger()
    cfg = ConfigLoader(args.config_dir).load_all()
    swarm = SwarmManager.from_config(cfg["drone"])
    gcs = DroneSwarmGCS(swarm, cfg["swarm"])

    logger.info("Connecting to all drones...")
    gcs.connect()
    logger.info("Connected to all drones")

    if args.run_loop:
        logger.info("Starting monitor loop")
        gcs.run_forever()


if __name__ == "__main__":
    main()
