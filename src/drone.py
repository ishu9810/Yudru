import asyncio
from dataclasses import dataclass, field
from time import time


@dataclass
class DroneState:
    drone_id: str
    connected: bool = False
    armed: bool = False
    flying: bool = False
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)
    battery_voltage: float = 16.8
    gps_fix: int = 3
    last_update: float = field(default_factory=time)


class Drone:
    def __init__(self, drone_id: str, connection: str, video_stream: str) -> None:
        self.state = DroneState(drone_id=drone_id)
        self.connection = connection
        self.video_stream = video_stream
        self._lock = asyncio.Lock()

    @property
    def drone_id(self) -> str:
        return self.state.drone_id

    async def connect(self) -> None:
        async with self._lock:
            await asyncio.sleep(0)
            self.state.connected = True
            self.state.last_update = time()

    async def disconnect(self) -> None:
        async with self._lock:
            self.state.connected = False
            self.state.armed = False
            self.state.flying = False
            self.state.last_update = time()

    async def arm(self) -> None:
        if not self.state.connected:
            raise RuntimeError(f"{self.drone_id} is not connected")
        self.state.armed = True

    async def takeoff(self, altitude: float) -> None:
        if not self.state.armed:
            raise RuntimeError(f"{self.drone_id} must be armed before takeoff")
        self.state.flying = True
        self.state.position = (self.state.position[0], self.state.position[1], altitude)
        self.state.last_update = time()

    async def land(self) -> None:
        self.state.position = (self.state.position[0], self.state.position[1], 0.0)
        self.state.flying = False
        self.state.armed = False
        self.state.last_update = time()

    async def goto(self, x: float, y: float, z: float) -> None:
        if not self.state.flying:
            raise RuntimeError(f"{self.drone_id} is not flying")
        self.state.position = (x, y, z)
        self.state.last_update = time()

    def update_telemetry(
        self,
        battery_voltage: float | None = None,
        gps_fix: int | None = None,
        velocity: tuple[float, float, float] | None = None,
    ) -> None:
        if battery_voltage is not None:
            self.state.battery_voltage = battery_voltage
        if gps_fix is not None:
            self.state.gps_fix = gps_fix
        if velocity is not None:
            self.state.velocity = velocity
        self.state.last_update = time()
