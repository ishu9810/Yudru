import json
from dataclasses import asdict, dataclass, field
from time import time
from typing import Any


@dataclass
class SwarmMessage:
    source: str
    destination: str
    command: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time)

    def encode(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")

    @staticmethod
    def decode(raw: bytes) -> "SwarmMessage":
        data = json.loads(raw.decode("utf-8"))
        return SwarmMessage(**data)
