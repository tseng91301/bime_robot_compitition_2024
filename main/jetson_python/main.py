from include import communication as comm
import threading
import time
import numpy as np

frame = np.array()
def detect_service():
    

comm.dump_ports_config()
comm.connect()

while True:
    for i in range(0, 6):
        val = comm.read_ult(i)
        print(f"{val}", end=", ")
    print()
    time.sleep(0.01)