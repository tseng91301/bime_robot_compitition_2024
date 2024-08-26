import communication as comm
import time
comm.connect()

while True:
    print(comm.read_ult())
    time.sleep(0.5)