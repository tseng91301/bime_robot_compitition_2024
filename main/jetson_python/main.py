from include import communication as comm
import time

comm.dump_ports_config()
comm.connect()

while True:
    for i in range(0, 6):
        val = comm.read_ult(i)
        print(f"{val}", end=", ")
    print()
    time.sleep(0.01)