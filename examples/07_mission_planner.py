from examples._common import load_gcs


gcs = load_gcs()
gcs.connect()
gcs.missions.execute("missions/simple_square.mission", dwell_sec=3)
