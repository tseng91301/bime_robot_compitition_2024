from include import goose_weight, communication, line_road
import time
import cv2

# 初始化 PID 變數
line_follow_P = 0
line_follow_I = 0
line_follow_D = 0
LINE_FOLLOW_P_BIAS = 0.65
LINE_FOLLOW_I_BIAS = 0
LINE_FOLLOW_D_BIAS = 0

LINE_FOLLOW_BIAS_OFFSET = 0.65
LINE_FOLLOW_BIAS_DEG = 0.35

def line_follow_duration(duration):
    start_time = time.time()
    while (time.time() - start_time) < duration:
        frame = line_road.get_frame()
        lines_x, lines_y, line_x_slope, line_y_slope = line_road.load_frame(frame)
        x_offset, deg = line_road.calculate_direction(lines_x, line_x_slope)

        global line_follow_P, line_follow_I, line_follow_D  # 引用全域變數
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

communication.send(communication.ser_motor, "c 110")  # lower the camera to see chicken

# first stage
box = 2  # 1 2 3
weight_level = 1  # 1 2 3
# second stage
yellow_position = 3  # 0 1 2 3 4
# third stage
bird_arr = [0, 0, 1, 0, 1]  # 0 is rooster and 1 is starling

first_stop = 0
weight_display = 0

if box == 1:
    first_stop = 15
elif box == 2:
    first_stop = 26
elif box == 3:
    first_stop = 37

rest_of_first_sec = 42 - first_stop

if weight_level == 1:
    weight_display = 34.6
elif weight_level == 2:
    weight_display = 51.2
elif weight_level == 3:
    weight_display = 60.9

communication.send(communication.ser_motor, "s " + str(weight_display))
line_follow_duration(first_stop)
communication.motor_stop()
time.sleep(2)
communication.send(communication.ser_ults, "l y 1500")
communication.send(communication.ser_motor, "g 1 650")
line_follow_duration(rest_of_first_sec)

communication.motor_stop()
time.sleep(2)


# second
line_follow_duration(6 + yellow_position * 3.3)
communication.motor_stop()
time.sleep(2)
communication.send(communication.ser_ults, "l r 1500")
time.sleep(3)
line_follow_duration(17.5 - yellow_position * 3.3)

communication.motor_stop()
time.sleep(2)


# third
line_follow_duration(8.25)
communication.motor_stop()
time.sleep(2)
for i in range(0, 4):
    if bird_arr[i] == 1:
        communication.send(communication.ser_ults, "l r 1500")
        time.sleep(0.5)
        communication.send(communication.ser_ults, "r 3000")
        time.sleep(3)
    else:
        communication.send(communication.ser_ults, "l g 1500")
        time.sleep(1.5)

    
    communication.motor_turn_deg(0.6, 90)
    time.sleep(3)
    communication.motor_stop()
    time.sleep(2)

communication.motor_turn_deg(0.6, 90)
time.sleep(3)
communication.motor_stop()
time.sleep(15)


