from examples._common import load_gcs


gcs = load_gcs()
gcs.connect()
gcs.arm_all()
gcs.takeoff_all(10)
