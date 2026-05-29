from __future__ import annotations

import math
from datetime import datetime, timezone

EARTH_RADIUS_M = 6371000.0


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1r, lon1r, lat2r, lon2r = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2r - lat1r
    dlon = lon2r - lon1r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1r) * math.cos(lat2r) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def offset_gps_m(lat: float, lon: float, north_m: float, east_m: float) -> tuple[float, float]:
    dlat = (north_m / EARTH_RADIUS_M) * (180.0 / math.pi)
    dlon = (east_m / (EARTH_RADIUS_M * math.cos(math.radians(lat)))) * (180.0 / math.pi)
    return lat + dlat, lon + dlon
