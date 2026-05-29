from src.video.stream_aggregator import StreamAggregator, VideoStream


if __name__ == "__main__":
    streams = [
        VideoStream(f"drone{i}", f"udp://239.0.0.1:56{i:02d}")
        for i in range(1, 6)
    ]
    aggregator = StreamAggregator(streams)
    aggregator.start_all()
    print(aggregator.dashboard_state())
