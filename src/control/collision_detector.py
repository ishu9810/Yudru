from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import cos, radians

from src.algorithms.collision_avoidance import perpendicular_avoidance_vector
from src.utils.helpers import EARTH_RADIUS_M, haversine_distance_m, offset_gps_m, utc_now_iso


@dataclass
class CollisionEvent:
    level: str
    drone_a: int
    drone_b: int
    distance_m: float
    timestamp: str


class CollisionDetector:
    def __init__(self, min_safe_distance_m: float = 10.0, emergency_distance_m: float = 5.0, shift_m: float = 3.0):
        self.min_safe_distance_m = min_safe_distance_m
        self.emergency_distance_m = emergency_distance_m
        self.shift_m = shift_m
        self.events: list[CollisionEvent] = []

    def evaluate(self, drones) -> tuple[list[CollisionEvent], list[tuple[int, float, float]]]:
        events: list[CollisionEvent] = []
        avoidance_cmds: list[tuple[int, float, float]] = []

        for d1, d2 in combinations(drones, 2):
            if d1.lat is None or d2.lat is None:
                continue
            distance = haversine_distance_m(d1.lat, d1.lon, d2.lat, d2.lon)
            if distance < self.emergency_distance_m:
                evt = CollisionEvent("EMERGENCY", d1.drone_id, d2.drone_id, distance, utc_now_iso())
                events.append(evt)
                self.events.append(evt)
            elif distance < self.min_safe_distance_m:
                evt = CollisionEvent("WARNING", d1.drone_id, d2.drone_id, distance, utc_now_iso())
                events.append(evt)
                self.events.append(evt)
                mean_lat = radians((d1.lat + d2.lat) / 2)
                dx = radians(d2.lon - d1.lon) * EARTH_RADIUS_M * cos(mean_lat)
                dy = radians(d2.lat - d1.lat) * EARTH_RADIUS_M
                east, north = perpendicular_avoidance_vector(dx, dy, self.shift_m)
                new_lat, new_lon = offset_gps_m(d2.lat, d2.lon, north, east)
                avoidance_cmds.append((d2.drone_id, new_lat, new_lon))

        return events, avoidance_cmds
