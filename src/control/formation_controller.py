"""Formation control system for drone swarm"""
import math
from typing import Dict, List, Tuple
from src.utils.helpers import offset_gps, gps_distance
from src.utils.logger import get_logger

logger = get_logger('FormationController')

class FormationController:
    """Manage formation flying for multiple drones"""
    
    FLIGHT_MODES = {
        'STABILIZE': 0,
        'GUIDED': 4,
        'AUTO': 10,
        'RTL': 11,
        'LAND': 9,
    }
    
    def __init__(self, swarm_config: Dict):
        self.swarm_config = swarm_config
        self.min_safe_distance = swarm_config.get('min_safe_distance', 10.0)
        self.emergency_distance = swarm_config.get('emergency_distance', 5.0)
        self.formation_tolerance = swarm_config.get('formation_hold_tolerance', 1.0)
    
    def calculate_formation_positions(self, formation: Dict, center_lat: float, center_lon: float, 
                                     center_alt: float) -> Dict[int, Dict[str, float]]:
        """
        Calculate target positions for all drones in formation.
        
        Args:
            formation: Formation definition from config
            center_lat: Formation center latitude
            center_lon: Formation center longitude
            center_alt: Formation center altitude
            
        Returns:
            Dict mapping drone_id to target position {lat, lon, alt}
        """
        positions = {}
        
        for drone_id_str, offset in formation.get('positions', {}).items():
            drone_id = int(drone_id_str.split('_')[1])
            
            # Apply offset from center
            target_lat, target_lon = offset_gps(
                center_lat, center_lon,
                offset[0],  # north
                offset[1]   # east
            )
            target_alt = center_alt + offset[2]  # altitude offset
            
            positions[drone_id] = {
                'lat': target_lat,
                'lon': target_lon,
                'alt': target_alt
            }
            
            logger.debug(f"Formation position for drone {drone_id}: "
                        f"({target_lat:.6f}, {target_lon:.6f}, {target_alt}m)")
        
        return positions
    
    def check_formation_error(self, current_positions: Dict[int, Dict[str, float]], 
                             target_positions: Dict[int, Dict[str, float]]) -> Dict[int, float]:
        """
        Calculate position error for each drone from target formation position.
        
        Args:
            current_positions: Current drone positions
            target_positions: Target formation positions
            
        Returns:
            Dict mapping drone_id to position error in meters
        """
        errors = {}
        
        for drone_id, current in current_positions.items():
            if drone_id not in target_positions:
                continue
            
            target = target_positions[drone_id]
            
            # Horizontal distance
            h_dist = gps_distance(
                current['lat'], current['lon'],
                target['lat'], target['lon']
            )
            
            # Vertical distance
            v_dist = abs(current['alt'] - target['alt'])
            
            # 3D distance
            error = math.sqrt(h_dist**2 + v_dist**2)
            errors[drone_id] = error
            
            if error > self.formation_tolerance:
                logger.warning(f"Drone {drone_id} formation error: {error:.2f}m "
                              f"(tolerance: {self.formation_tolerance}m)")
        
        return errors
    
    def is_formation_stable(self, errors: Dict[int, float]) -> bool:
        """Check if all drones are within formation tolerance"""
        if not errors:
            return False
        return all(err <= self.formation_tolerance for err in errors.values())


class CollisionDetector:
    """Real-time collision detection and avoidance"""
    
    def __init__(self, swarm_config: Dict):
        self.swarm_config = swarm_config
        self.min_safe_distance = swarm_config.get('min_safe_distance', 10.0)
        self.emergency_distance = swarm_config.get('emergency_distance', 5.0)
        self.collision_events = []
    
    def check_collisions(self, positions: Dict[int, Dict[str, float]]) -> List[Tuple[int, int, float]]:
        """
        Check for potential collisions between all drone pairs.
        
        Args:
            positions: Dict mapping drone_id to position {lat, lon, alt}
            
        Returns:
            List of (drone_id1, drone_id2, distance) tuples for close pairs
        """
        collisions = []
        drone_ids = list(positions.keys())
        
        for i, drone_a in enumerate(drone_ids):
            for drone_b in drone_ids[i+1:]:
                pos_a = positions[drone_a]
                pos_b = positions[drone_b]
                
                # Calculate distance
                h_dist = gps_distance(
                    pos_a['lat'], pos_a['lon'],
                    pos_b['lat'], pos_b['lon']
                )
                
                v_dist = abs(pos_a['alt'] - pos_b['alt'])
                distance = math.sqrt(h_dist**2 + v_dist**2)
                
                if distance < self.min_safe_distance:
                    collisions.append((drone_a, drone_b, distance))
                    
                    if distance < self.emergency_distance:
                        logger.critical(f"EMERGENCY: Drones {drone_a} and {drone_b} "
                                      f"only {distance:.1f}m apart! Triggering failsafe!")
                        self.collision_events.append({
                            'type': 'emergency',
                            'drone_a': drone_a,
                            'drone_b': drone_b,
                            'distance': distance
                        })
                    else:
                        logger.warning(f"Collision warning: Drones {drone_a} and {drone_b} "
                                     f"are {distance:.1f}m apart")
                        self.collision_events.append({
                            'type': 'warning',
                            'drone_a': drone_a,
                            'drone_b': drone_b,
                            'distance': distance
                        })
        
        return collisions
    
    def is_emergency(self, collisions: List[Tuple[int, int, float]]) -> bool:
        """Check if any collision is at emergency distance"""
        return any(dist < self.emergency_distance for _, _, dist in collisions)
