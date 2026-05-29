from dataclasses import dataclass, field
from time import time
from typing import Callable

from src.communication.protocol import SwarmMessage


@dataclass
class PeerStatus:
    last_seen: float = field(default_factory=time)
    packets_sent: int = 0


class EspNowMesh:
    def __init__(self) -> None:
        self.peers: dict[str, PeerStatus] = {}
        self.handlers: list[Callable[[SwarmMessage], None]] = []

    def add_peer(self, peer_id: str) -> None:
        self.peers.setdefault(peer_id, PeerStatus())

    def subscribe(self, handler: Callable[[SwarmMessage], None]) -> None:
        self.handlers.append(handler)

    def send(self, message: SwarmMessage) -> None:
        if message.destination in self.peers:
            self.peers[message.destination].packets_sent += 1
            self.peers[message.destination].last_seen = time()
        for handler in self.handlers:
            handler(message)

    def health_snapshot(self) -> dict[str, dict[str, float | int]]:
        return {
            peer: {"last_seen": status.last_seen, "packets_sent": status.packets_sent}
            for peer, status in self.peers.items()
        }
