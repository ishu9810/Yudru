from __future__ import annotations

from typing import Any


def parse_message(msg: Any) -> dict[str, Any]:
    msg_type = getattr(msg, "get_type", lambda: "UNKNOWN")()
    result: dict[str, Any] = {"type": msg_type}

    if msg_type == "GLOBAL_POSITION_INT":
        result.update(
            {
                "lat": msg.lat / 1e7,
                "lon": msg.lon / 1e7,
                "alt_m": msg.relative_alt / 1000.0,
                "heading_deg": (msg.hdg / 100.0) if getattr(msg, "hdg", 65535) != 65535 else None,
            }
        )
    elif msg_type == "SYS_STATUS":
        voltage_mv = getattr(msg, "voltage_battery", -1)
        battery_remaining = getattr(msg, "battery_remaining", -1)
        result.update(
            {
                "battery_v": (voltage_mv / 1000.0) if voltage_mv >= 0 else None,
                "battery_pct": battery_remaining if battery_remaining >= 0 else None,
            }
        )
    elif msg_type == "GPS_RAW_INT":
        result.update(
            {
                "satellites_visible": getattr(msg, "satellites_visible", None),
                "fix_type": getattr(msg, "fix_type", None),
            }
        )
    elif msg_type == "HEARTBEAT":
        result.update(
            {
                "base_mode": getattr(msg, "base_mode", 0),
                "custom_mode": getattr(msg, "custom_mode", 0),
                "system_status": getattr(msg, "system_status", 0),
            }
        )

    return result
