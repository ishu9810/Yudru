# drone_swarm_real

Production-ready Python ground control system for controlling a 5-drone SpeedyBee F405 V3 swarm running ArduPilot over USB-UART MAVLink links.

## Quick Start

```bash
pip install -r requirements.txt
python src/main.py --config-dir ./config
```

## Test

```bash
python -m unittest discover -s tests -v
```
