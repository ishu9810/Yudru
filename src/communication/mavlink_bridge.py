from dataclasses import dataclass


@dataclass
class TelemetryFrame:
    drone_id: str
    latitude: float
    longitude: float
    altitude: float
    battery_voltage: float
    gps_fix: int


class MavlinkBridge:
    def parse(self, payload: dict) -> TelemetryFrame:
        return TelemetryFrame(
            drone_id=str(payload.get("drone_id", "unknown")),
            latitude=float(payload.get("latitude", 0.0)),
            longitude=float(payload.get("longitude", 0.0)),
            altitude=float(payload.get("altitude", 0.0)),
            battery_voltage=float(payload.get("battery_voltage", 0.0)),
            gps_fix=int(payload.get("gps_fix", 0)),
        )
