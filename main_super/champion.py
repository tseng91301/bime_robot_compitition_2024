from include import goose_weight, communication, line_road
import time
import cv2

def line_follow_duration(duration):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        frame = line_road.get_frame()
        lines_x, lines_y, line_x_slope, line_y_slope = line_road.load_frame(frame)
        x_offset, deg = line_road.calculate_direction(lines_x, line_x_slope)

        line_follow_P_old = line_follow_P
        line_follow_P = (-1) * (x_offset * LINE_FOLLOW_BIAS_OFFSET) + ((deg - 90) * LINE_FOLLOW_BIAS_DEG)
        line_follow_I += line_follow_P
        line_follow_D = line_follow_P - line_follow_P_old

        line_follow_PID = line_follow_P * LINE_FOLLOW_P_BIAS + line_follow_I * LINE_FOLLOW_I_BIAS + line_follow_D * LINE_FOLLOW_D_BIAS
        communication.motor_turn_deg(0.6, line_follow_PID + 90)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    communication.motor_stop()

communication.connect()

communication.send(communication.ser_motor, "c 110") # lower the camera to see chicken

# first stage
box = 1 #1 2 3
weight_level = 1 #1 2 3
# second stage
yellow_position = 3 #0 1 2 3 4
# third stage
bird_arr = [0, 0, 1, 0, 1] # 0 is rooster and 1 is starling

first_stop = 0
weight_display = 0

if(box == 1):
    first_stop = 6
elif(box == 2):
    first_stop = 10
elif(box == 3):
    first_stop = 14

rest_of_first_sec = 23 - first_stop

if(weight_level == 1):
    weight_display = 34.6
elif(weight_level == 2):
    weight_display = 51.2
elif(weight_level == 3):
    weight_display = 60.9

communication.send(communication.ser_motor, "s " + weight_display)
line_follow_duration(first_stop)
communication.motor_stop()
communication.send(communication.ser_ults, "l y 1500")
communication.send(communication.ser_motor, "g 650")
line_follow_duration(rest_of_first_sec)



# second
line_follow_duration(4.68 + yellow_position * 1.445)
time.sleep()
communication.motor_stop()
communication.send(communication.ser_ults, "l r 1500")
line_follow_duration((5 - yellow_position) * 1.445 + 1.156)

# third
line_follow_duration(3.5)
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
      time.sleep(2)

communication.motor_turn_deg(0.6, 90)
time.sleep(3)








    














    








