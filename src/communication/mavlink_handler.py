"""MAVLink communication handler for ArduPilot drones"""
import threading
import time
from typing import Callable, Optional, Dict, Any
from pymavlink.dialects.v20 import ardupilotmega as mavlink
import serial
from src.utils.logger import get_logger

logger = get_logger('MAVLink')

class MAVLinkHandler:
    """Handle MAVLink protocol communication with drones"""
    
    def __init__(self, port: str, baud: int = 115200, system_id: int = 1):
        self.port = port
        self.baud = baud
        self.system_id = system_id
        self.serial = None
        self.mav = None
        self.connected = False
        self.message_callbacks = {}
        self.receive_thread = None
        self.stop_event = threading.Event()
        
    def connect(self, timeout: float = 5.0) -> bool:
        """Connect to drone via serial port"""
        try:
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
            self.mav = mavlink.MAVLink(self.serial)
            self.mav.srcComponent = 0
            self.mav.srcSystem = 255
            
            # Start receive thread
            self.stop_event.clear()
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            # Wait for heartbeat
            start = time.time()
            while not self.connected and (time.time() - start) < timeout:
                time.sleep(0.1)
            
            if self.connected:
                logger.info(f"Connected to drone on {self.port}")
                return True
            else:
                logger.error(f"No heartbeat received from drone on {self.port}")
                self.disconnect()
                return False
                
        except serial.SerialException as e:
            logger.error(f"Failed to open serial port {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from drone"""
        self.stop_event.set()
        if self.receive_thread:
            self.receive_thread.join(timeout=2)
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.connected = False
        logger.info(f"Disconnected from {self.port}")
    
    def _receive_loop(self):
        """Receive and process MAVLink messages"""
        while not self.stop_event.is_set():
            try:
                if self.serial and self.serial.in_waiting:
                    msg = self.mav.recv_msg()
                    if msg:
                        self._handle_message(msg)
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
            time.sleep(0.01)
    
    def _handle_message(self, msg):
        """Handle incoming MAVLink message"""
        msg_type = msg.get_type()
        
        if msg_type == 'HEARTBEAT':
            self.connected = True
        
        # Call registered callbacks
        if msg_type in self.message_callbacks:
            for callback in self.message_callbacks[msg_type]:
                try:
                    callback(msg)
                except Exception as e:
                    logger.error(f"Error in callback for {msg_type}: {e}")
    
    def register_callback(self, msg_type: str, callback: Callable):
        """Register callback for message type"""
        if msg_type not in self.message_callbacks:
            self.message_callbacks[msg_type] = []
        self.message_callbacks[msg_type].append(callback)
    
    def arm(self):
        """Arm the drone"""
        try:
            self.mav.command_long_send(
                self.system_id, 1,
                mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0, 1, 0, 0, 0, 0, 0, 0
            )
            logger.info(f"Arm command sent to drone {self.system_id}")
        except Exception as e:
            logger.error(f"Failed to arm drone: {e}")
    
    def disarm(self):
        """Disarm the drone"""
        try:
            self.mav.command_long_send(
                self.system_id, 1,
                mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                0, 0, 0, 0, 0, 0, 0, 0
            )
            logger.info(f"Disarm command sent to drone {self.system_id}")
        except Exception as e:
            logger.error(f"Failed to disarm drone: {e}")
    
    def takeoff(self, altitude: float):
        """Takeoff to specified altitude"""
        try:
            self.mav.command_long_send(
                self.system_id, 1,
                mavlink.MAV_CMD_NAV_TAKEOFF,
                0, 0, 0, 0, 0, 0, 0, altitude
            )
            logger.info(f"Takeoff command sent to drone {self.system_id} (alt: {altitude}m)")
        except Exception as e:
            logger.error(f"Failed to send takeoff command: {e}")
    
    def land(self):
        """Land the drone"""
        try:
            self.mav.command_long_send(
                self.system_id, 1,
                mavlink.MAV_CMD_NAV_LAND,
                0, 0, 0, 0, 0, 0, 0, 0
            )
            logger.info(f"Land command sent to drone {self.system_id}")
        except Exception as e:
            logger.error(f"Failed to send land command: {e}")
    
    def set_mode(self, mode: int):
        """Set flight mode"""
        try:
            self.mav.command_long_send(
                self.system_id, 1,
                mavlink.MAV_CMD_DO_SET_MODE,
                0, 1, mode, 0, 0, 0, 0, 0
            )
            logger.info(f"Mode set to {mode} on drone {self.system_id}")
        except Exception as e:
            logger.error(f"Failed to set mode: {e}")
    
    def set_position_target(self, lat: float, lon: float, alt: float, speed: float = 0):
        """Move drone to GPS position"""
        try:
            self.mav.set_position_target_global_int_send(
                int(time.time() * 1000),
                self.system_id, 1,
                3,  # MAV_FRAME_GLOBAL_RELATIVE_ALT
                0x0F08,  # Position target typemask
                int(lat * 1e7), int(lon * 1e7), alt,
                0, 0, 0,  # Velocity
                0, 0, 0,  # Acceleration
                0, 0      # Yaw
            )
        except Exception as e:
            logger.error(f"Failed to set position target: {e}")
