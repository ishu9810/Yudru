import asyncio

from src.gcs import build_swarm


async def main() -> None:
    swarm = build_swarm("config/drone_config.yaml")
    await swarm.connect_all()
    await swarm.synchronized_takeoff(3.0)
    await swarm.execute_formation("square", spacing=2.0, altitude=3.0)
    print("Square formation done")
    await swarm.synchronized_landing()


if __name__ == "__main__":
    asyncio.run(main())
