from include import communication
import time

communication.connect()
communication.start_ult_service()
while True:
    for i in range(communication.ULT_NUM):
        u_v = communication.ults_value
        print(f"Read Ults value: {str(u_v)}")
    time.sleep(0.1)