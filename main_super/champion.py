from include import goose_weight, communication
import time
from conf import stage_parameters
communication.connect()

communication(communication.send("c 110")) # lower the camera to see chicken

# first stage
box = 0 #1 2 3
weight_level = 0 #1 2 3
# second stage
yellow_position = 0 #0 1 2 3 4
# third stage
bird_arr = [0, 0, 0, 0, 0] # 0 is rooster and 1 is starling

first_stop = 0
weight_display = 0

if(box == 1):
    first_stop = 6
elif(box == 2):
    first_stop = 10
elif(box == 3):
    first_stop = 14

rest_of_first_sec = 20 - first_stop

if(weight_level == 1):
    weight_display = 34.6
elif(weight_level == 2):
    weight_display = 51.2
elif(weight_level == 3):
    weight_display = 60.9

communication.send(communication.ser_motor, "s " + weight_display)
communication.motor_turn_deg(0.6, 90)
time.sleep(first_stop)
communication.motor_stop()
communication.send(communication.ser_ults, "l y 1500")
communication.send(communication.ser_motor, "g 650")
communication.motor_turn_deg(0.6, 90)
time.sleep(rest_of_first_sec)



# second
communication.motor_turn_deg(0.6, 90)
time.sleep(4.68 + yellow_position * 1.445)
communication.motor_stop()
communication.send(communication.ser_ults, "l r 1500")
communication.motor_turn_deg(0.6, 90)
time.sleep((5 - yellow_position) * 1.445 + 1.156)

# third
communication.motor_turn_deg(0.6, 90)
time.sleep(3.179)
communication.motor_stop()
for i in range(0,4):
      if(bird_arr[i] == 1):
            communication.send(communication.ser_ults, "l r 1500")
            communication.send(communication.ser_ults, "r 3000")
      else:
            communication.send(communication.ser_ults, "l g 1500")
      communication.motor_turn_deg(0.6, 90)
      time.sleep(1.618)
      communication.motor_stop()
      time.sleep(1)

communication.motor_turn_deg(0.6, 90)
time.sleep(3)








    














    








