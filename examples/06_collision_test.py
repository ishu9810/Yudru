import time

from examples._common import load_gcs


gcs = load_gcs()
gcs.connect()
time.sleep(2)
result = gcs.monitor_once()
print(result["events"])
