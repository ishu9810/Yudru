"""Individual drone controller"""
import time
from typing import Dict, Any, Optional
from src.communication.mavlink_handler import MAVLinkHandler
from src.utils.logger import get_logger

logger = get_logger('Drone')

class Drone:
    """Control and monitor a single drone"""
    
    def __init__(self, drone_id: int, config: Dict[str, Any]):
        self.drone_id = drone_id
        self.config = config
        self.mav = MAVLinkHandler(
            port=config['port'],
            baud=config['baud'],
            system_id=config['system_id']
        )
        
        self.telemetry = {
            'latitude': 0,
            'longitude': 0,
            'altitude': 0,
            'velocity_x': 0,
            'velocity_y': 0,
            'velocity_z': 0,
            'battery_voltage': 0,
            'battery_percent': 0,
            'mode': 'UNKNOWN',
            'armed': False,
            'gps_satellites': 0,
            'gps_hdop': 0,
        }
        
        # Register telemetry callbacks
        self.mav.register_callback('GLOBAL_POSITION_INT', self._handle_position)
        self.mav.register_callback('SYS_STATUS', self._handle_sys_status)
        self.mav.register_callback('HEARTBEAT', self._handle_heartbeat)
    
    def connect(self, timeout: float = 5.0) -> bool:
        """Connect to drone"""
        return self.mav.connect(timeout)
    
    def disconnect(self):
        """Disconnect from drone"""
        self.mav.disconnect()
    
    def is_connected(self) -> bool:
        """Check if drone is connected"""
        return self.mav.connected
    
    def arm(self) -> bool:
        """Arm the drone"""
        if not self.is_connected():
            logger.error(f"Drone {self.drone_id} not connected")
            return False
        self.mav.arm()
        time.sleep(0.5)
        return self.telemetry['armed']
    
    def disarm(self) -> bool:
        """Disarm the drone"""
        if not self.is_connected():
            logger.error(f"Drone {self.drone_id} not connected")
            return False
        self.mav.disarm()
        time.sleep(0.5)
        return not self.telemetry['armed']
    
    def takeoff(self, altitude: float) -> bool:
        """Takeoff to specified altitude"""
        if not self.is_connected():
            logger.error(f"Drone {self.drone_id} not connected")
            return False
        if not self.telemetry['armed']:
            logger.error(f"Drone {self.drone_id} not armed")
            return False
        self.mav.takeoff(altitude)
        logger.info(f"Drone {self.drone_id} taking off to {altitude}m")
        return True
    
    def land(self) -> bool:
        """Land the drone"""
        if not self.is_connected():
            logger.error(f"Drone {self.drone_id} not connected")
            return False
        self.mav.land()
        logger.info(f"Drone {self.drone_id} landing")
        return True
    
    def move_to(self, lat: float, lon: float, alt: float) -> bool:
        """Move drone to GPS position"""
        if not self.is_connected():
            logger.error(f"Drone {self.drone_id} not connected")
            return False
        self.mav.set_position_target(lat, lon, alt)
        return True
    
    def set_mode(self, mode: str) -> bool:
        """Set flight mode"""
        if not self.is_connected():
            logger.error(f"Drone {self.drone_id} not connected")
            return False
        
        mode_map = {
            'STABILIZE': 0,
            'GUIDED': 4,
            'AUTO': 10,
            'RTL': 11,
            'LAND': 9,
        }
        
        if mode not in mode_map:
            logger.error(f"Unknown mode: {mode}")
            return False
        
        self.mav.set_mode(mode_map[mode])
        return True
    
    def _handle_position(self, msg):
        """Handle position update from drone"""
        self.telemetry['latitude'] = msg.lat / 1e7
        self.telemetry['longitude'] = msg.lon / 1e7
        self.telemetry['altitude'] = msg.alt / 1000.0
        self.telemetry['velocity_x'] = msg.vx / 100.0
        self.telemetry['velocity_y'] = msg.vy / 100.0
        self.telemetry['velocity_z'] = msg.vz / 100.0
    
    def _handle_sys_status(self, msg):
        """Handle system status from drone"""
        self.telemetry['battery_voltage'] = msg.voltage_battery / 1000.0
        self.telemetry['battery_percent'] = msg.battery_remaining
    
    def _handle_heartbeat(self, msg):
        """Handle heartbeat from drone"""
        self.telemetry['armed'] = bool(msg.base_mode & 0x80)
        self.telemetry['mode'] = self._get_mode_name(msg.custom_mode)
    
    def _get_mode_name(self, mode_num: int) -> str:
        """Convert mode number to name"""
        modes = {0: 'STABILIZE', 4: 'GUIDED', 10: 'AUTO', 11: 'RTL', 9: 'LAND'}
        return modes.get(mode_num, 'UNKNOWN')
    
    def get_position(self) -> Dict[str, float]:
        """Get current drone position"""
        return {
            'lat': self.telemetry['latitude'],
            'lon': self.telemetry['longitude'],
            'alt': self.telemetry['altitude']
        }
    
    def get_battery_percent(self) -> int:
        """Get battery percentage"""
        return self.telemetry['battery_percent']
    
    def get_gps_status(self) -> Dict[str, Any]:
        """Get GPS status"""
        return {
            'satellites': self.telemetry['gps_satellites'],
            'hdop': self.telemetry['gps_hdop']
        }
