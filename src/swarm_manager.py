"""Swarm manager for coordinating multiple drones"""
import time
from typing import Dict, List, Optional
from src.drone import Drone
from src.control.formation_controller import FormationController, CollisionDetector
from src.utils.config_loader import ConfigLoader
from src.utils.logger import get_logger

logger = get_logger('SwarmManager')

class SwarmManager:
    """Manage and coordinate a swarm of drones"""
    
    def __init__(self, num_drones: int = 5, config_dir: str = 'config'):
        self.num_drones = num_drones
        self.drones: Dict[int, Drone] = {}
        self.config_loader = ConfigLoader(config_dir)
        self.swarm_config = self.config_loader.get_swarm_config()
        self.formation_controller = FormationController(self.swarm_config)
        self.collision_detector = CollisionDetector(self.swarm_config)
        self.is_flying = False
    
    def initialize_drones(self) -> bool:
        """Initialize and connect to all drones"""
        logger.info(f"Initializing {self.num_drones} drones...")
        
        for drone_id in range(self.num_drones):
            try:
                config = self.config_loader.get_drone_config(drone_id)
                drone = Drone(drone_id, config)
                
                if drone.connect(timeout=5.0):
                    self.drones[drone_id] = drone
                    logger.info(f"✓ Drone {drone_id} connected on {config['port']}")
                else:
                    logger.error(f"✗ Failed to connect drone {drone_id}")
                    return False
                    
            except Exception as e:
                logger.error(f"Error initializing drone {drone_id}: {e}")
                return False
        
        logger.info(f"✓ All {self.num_drones} drones connected successfully")
        return True
    
    def shutdown(self):
        """Disconnect all drones"""
        logger.info("Shutting down swarm...")
        for drone in self.drones.values():
            if drone.is_connected():
                drone.disconnect()
        logger.info("✓ All drones disconnected")
    
    def arm_all(self) -> bool:
        """Arm all drones"""
        logger.info("Arming all drones...")
        success = True
        for drone_id, drone in self.drones.items():
            if drone.arm():
                logger.info(f"✓ Drone {drone_id} armed")
            else:
                logger.error(f"✗ Failed to arm drone {drone_id}")
                success = False
        return success
    
    def disarm_all(self) -> bool:
        """Disarm all drones"""
        logger.info("Disarming all drones...")
        success = True
        for drone_id, drone in self.drones.items():
            if drone.disarm():
                logger.info(f"✓ Drone {drone_id} disarmed")
            else:
                logger.error(f"✗ Failed to disarm drone {drone_id}")
                success = False
        return success
    
    def takeoff_all(self, altitude: float) -> bool:
        """Takeoff all drones to specified altitude"""
        logger.info(f"Taking off all drones to {altitude}m...")
        success = True
        for drone_id, drone in self.drones.items():
            if drone.takeoff(altitude):
                logger.info(f"✓ Drone {drone_id} takeoff initiated")
            else:
                logger.error(f"✗ Failed to takeoff drone {drone_id}")
                success = False
        
        if success:
            self.is_flying = True
        return success
    
    def land_all(self) -> bool:
        """Land all drones"""
        logger.info("Landing all drones...")
        success = True
        for drone_id, drone in self.drones.items():
            if drone.land():
                logger.info(f"✓ Drone {drone_id} landing initiated")
            else:
                logger.error(f"✗ Failed to land drone {drone_id}")
                success = False
        
        self.is_flying = False
        return success
    
    def form_formation(self, formation_name: str, center_lat: float, 
                      center_lon: float, center_alt: float) -> bool:
        """Move all drones to formation"""
        logger.info(f"Forming {formation_name} at ({center_lat:.6f}, {center_lon:.6f}, {center_alt}m)")
        
        try:
            formation = self.config_loader.get_formation(formation_name)
        except KeyError:
            logger.error(f"Formation {formation_name} not found")
            return False
        
        # Calculate target positions
        target_positions = self.formation_controller.calculate_formation_positions(
            formation, center_lat, center_lon, center_alt
        )
        
        # Send move commands to all drones
        for drone_id, target in target_positions.items():
            if drone_id in self.drones:
                self.drones[drone_id].move_to(target['lat'], target['lon'], target['alt'])
        
        logger.info(f"✓ Formation commands sent")
        return True
    
    def get_all_positions(self) -> Dict[int, Dict[str, float]]:
        """Get current positions of all drones"""
        positions = {}
        for drone_id, drone in self.drones.items():
            positions[drone_id] = drone.get_position()
        return positions
    
    def monitor_collisions(self) -> bool:
        """Check for collisions and trigger failsafe if needed"""
        positions = self.get_all_positions()
        collisions = self.collision_detector.check_collisions(positions)
        
        if self.collision_detector.is_emergency(collisions):
            logger.critical("EMERGENCY COLLISION DETECTED - TRIGGERING FAILSAFE!")
            self.emergency_land_all()
            return False
        
        return True
    
    def emergency_land_all(self):
        """Emergency landing procedure - RTH + 5sec hold + land"""
        logger.critical("EXECUTING EMERGENCY LANDING PROCEDURE")
        
        # Set all drones to RTL mode
        for drone_id, drone in self.drones.items():
            drone.set_mode('RTL')
            logger.warning(f"Drone {drone_id} set to RTL mode")
        
        # Hold for 5 seconds
        time.sleep(5)
        
        # Land all drones
        for drone_id, drone in self.drones.items():
            drone.set_mode('LAND')
            logger.warning(f"Drone {drone_id} landing")
        
        self.is_flying = False
    
    def get_swarm_status(self) -> Dict:
        """Get overall swarm status"""
        status = {
            'connected_drones': len(self.drones),
            'is_flying': self.is_flying,
            'positions': self.get_all_positions(),
            'battery_levels': {},
            'modes': {}
        }
        
        for drone_id, drone in self.drones.items():
            status['battery_levels'][drone_id] = drone.get_battery_percent()
            status['modes'][drone_id] = drone.telemetry['mode']
        
        return status
