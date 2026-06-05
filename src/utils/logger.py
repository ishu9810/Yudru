"""Logger utility for drone swarm system"""
import logging
import sys
from pathlib import Path
from datetime import datetime

class DroneSwarmLogger:
    """Centralized logger for swarm operations"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DroneSwarmLogger, cls).__new__(cls)
            cls._instance._init_logger()
        return cls._instance
    
    def _init_logger(self):
        self.logger = logging.getLogger('DroneSwarm')
        self.logger.setLevel(logging.DEBUG)
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%H:%M:%S')
        console_handler.setFormatter(console_format)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_handler = logging.FileHandler(f'logs/swarm_{timestamp}.log')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self, name=None):
        if name:
            return logging.getLogger(f'DroneSwarm.{name}')
        return self.logger

def get_logger(name=None):
    logger_instance = DroneSwarmLogger()
    return logger_instance.get_logger(name)
