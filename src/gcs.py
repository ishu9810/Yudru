import argparse
import asyncio
from pathlib import Path

from src.drone import Drone
from src.swarm_manager import SwarmManager
from src.utils.config import load_yaml


def build_swarm(drone_config_path: str | Path) -> SwarmManager:
    config = load_yaml(drone_config_path)
    drones = [
        Drone(
            drone_id=item["id"],
            connection=item["connection"],
            video_stream=item["video_stream"],
        )
        for item in config.get("drones", [])
    ]
    return SwarmManager(drones)


async def execute_command(args: argparse.Namespace) -> None:
    swarm = build_swarm(args.drone_config)
    await swarm.connect_all()

    if args.command == "status":
        print(swarm.monitor_safety())
    elif args.command == "takeoff":
        await swarm.synchronized_takeoff(args.altitude)
        print("takeoff complete")
    elif args.command == "land":
        await swarm.synchronized_landing()
        print("landing complete")
    elif args.command == "formation":
        await swarm.synchronized_takeoff(args.altitude)
        await swarm.execute_formation(args.pattern, args.spacing, args.altitude)
        print(f"formation {args.pattern} executed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ground Control Station for 5-drone swarm")
    parser.add_argument("--drone-config", default="config/drone_config.yaml")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")

    takeoff = subparsers.add_parser("takeoff")
    takeoff.add_argument("--altitude", type=float, default=3.0)

    subparsers.add_parser("land")

    formation = subparsers.add_parser("formation")
    formation.add_argument("--pattern", choices=["line", "square", "circle", "triangle", "grid"], default="square")
    formation.add_argument("--spacing", type=float, default=2.0)
    formation.add_argument("--altitude", type=float, default=3.0)

    args = parser.parse_args()
    asyncio.run(execute_command(args))


if __name__ == "__main__":
    main()
