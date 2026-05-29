# Communication Protocols
- Drone-to-drone mesh: ESP-NOW over ESP32
- FC bridge: UART serial link between Betaflight and ESP32
- GCS telemetry/control model: MAVLink-compatible frame abstraction + swarm JSON messages

## Swarm Message
`SwarmMessage(source, destination, command, payload, timestamp)` encoded as JSON bytes.
