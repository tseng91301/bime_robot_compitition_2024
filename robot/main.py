import communication as comm
import time
comm.connect()
print("connected")

while True:
    print(comm.read_ult(0))
    time.sleep(0.01)