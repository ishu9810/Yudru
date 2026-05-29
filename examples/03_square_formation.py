import time

from examples._common import load_gcs


gcs = load_gcs()
gcs.connect()
gcs.arm_all()
gcs.takeoff_all(10)
gcs.form("SQUARE", 37.123, -122.456, 10)
time.sleep(30)
gcs.land_all()
