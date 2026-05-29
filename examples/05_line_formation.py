from examples._common import load_gcs


gcs = load_gcs()
gcs.connect()
gcs.form("LINE", 37.123, -122.456, 10)
