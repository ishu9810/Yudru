# 🚁 5-Drone ArduPilot Swarm Control System

**Production-ready Python Ground Control Station for coordinated flight of 5 SpeedyBee F405 V3 drones with ArduPilot firmware**

## 🎯 Features

- ✅ **Multi-Drone MAVLink Control**: Connect and control 5 drones simultaneously via USB serial
- ✅ **Formation Flying**: Square, line, circle, triangle, and grid formations
- ✅ **Collision Avoidance**: Real-time distance monitoring with automatic evasion
- ✅ **Failsafe System**: RTH + 5-second hold on signal loss
- ✅ **Real-time Telemetry**: GPS position, battery, altitude, speed monitoring
- ✅ **Mission Planning**: Autonomous waypoint missions
- ✅ **Safety First**: GPS validation, battery monitoring, geofence enforcement
- ✅ **Windows Compatible**: Python 3.9+ on Windows/Linux/Mac

## 📋 Requirements

### Hardware
- 5x SpeedyBee F405 V3 with ArduPilot firmware
- 5x GPS modules
- 5x USB-to-UART serial adapters
- USB hub (for 5 concurrent connections)
- Windows/Linux/Mac PC with Python 3.9+
- ELRS 2.4GHz RP1 receiver (for RC backup)

### Software
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Setup Configuration
Edit `config/drone_config.yaml` with your 5 drone COM ports

### 2. Run Examples
```bash
python examples/01_simple_arm_disarm.py
python examples/02_synchronized_takeoff.py
python examples/03_square_formation.py
```

## 📚 Documentation

See [docs/README.md](docs/README.md) for complete documentation

## 🚁 Flight Modes

- STABILIZE, GUIDED, AUTO, RTL, LAND

## ⚠️ Safety First

Always test in safe environments with manual RC override ready.

---

**Start with [docs/QUICKSTART.md](docs/QUICKSTART.md)** 🚀