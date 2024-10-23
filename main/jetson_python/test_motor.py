from include import communication
import time

communication.connect()

communication.motor_turn_deg(1, 90)
time.sleep(7.5)
communication.motor_stop()