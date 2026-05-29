from __future__ import annotations

from src.algorithms.formations import named_formation_offsets
from src.utils.helpers import offset_gps_m


class FormationController:
    def __init__(self, swarm_manager):
        self.swarm_manager = swarm_manager
        self.current_formation = None

    def calculate_targets(self, formation_name: str, center_lat: float, center_lon: float, altitude_m: float):
        offsets = named_formation_offsets(formation_name, len(self.swarm_manager.drones))
        targets = []
        for drone, (east_m, north_m, z_m) in zip(self.swarm_manager.drones, offsets):
            lat, lon = offset_gps_m(center_lat, center_lon, north_m=north_m, east_m=east_m)
            targets.append((drone, lat, lon, altitude_m + z_m))
        return targets

    def apply_formation(self, formation_name: str, center_lat: float, center_lon: float, altitude_m: float) -> None:
        for drone, lat, lon, alt in self.calculate_targets(formation_name, center_lat, center_lon, altitude_m):
            drone.move_to(lat, lon, alt)
        self.current_formation = formation_name.upper()
