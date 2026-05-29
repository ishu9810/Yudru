import time

from examples._common import load_gcs


gcs = load_gcs()
gcs.connect()
time.sleep(6)
print(gcs.monitor_once())
