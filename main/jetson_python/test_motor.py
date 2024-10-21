from include import communication
import time

communication.connect()

communication.motor_turn_raw(100, 100)
time.sleep(3)
communication.motor_turn_raw(0, 0)
time.sleep(1)
communication.motor_turn_raw(-100, -100)
time.sleep(1)
communication.motor_turn_raw(0, 0)