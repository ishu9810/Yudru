from dataclasses import dataclass


@dataclass
class VideoStream:
    drone_id: str
    url: str
    bitrate_kbps: int = 2000
    active: bool = False


class StreamAggregator:
    def __init__(self, streams: list[VideoStream]) -> None:
        self.streams = {stream.drone_id: stream for stream in streams}

    def start_all(self) -> None:
        for stream in self.streams.values():
            stream.active = True

    def stop_all(self) -> None:
        for stream in self.streams.values():
            stream.active = False

    def dashboard_state(self) -> dict[str, dict[str, str | int | bool]]:
        return {
            stream.drone_id: {
                "url": stream.url,
                "bitrate_kbps": stream.bitrate_kbps,
                "active": stream.active,
            }
            for stream in self.streams.values()
        }
