# Drone Swarm Control (Yudru)

Python-based ground control station and ESP32 mesh bridge for a 5-drone Betaflight FPV swarm.

## Features
- Async multi-drone control and state management
- Formation execution (line, square, circle, triangle, grid)
- Collision and geofence safety monitoring
- ESP-NOW mesh protocol abstraction and MAVLink telemetry bridge
- Multi-stream FPV aggregation model
- Example scripts for formation, mission planning, and safety tests

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/gcs.py status
python src/gcs.py formation --pattern square --spacing 2 --altitude 3
```

## Project Layout
See `docs/` for setup, protocol, and API details.
