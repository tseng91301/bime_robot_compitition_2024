from include import line_road, communication
import cv2

line_follow_P = 0
line_follow_I = 0
line_follow_D = 0
LINE_FOLLOW_P_BIAS = 0.4
LINE_FOLLOW_I_BIAS = 0.2
LINE_FOLLOW_D_BIAS = 0.1

LINE_FOLLOW_BIAS_OFFSET = 0.65
LINE_FOLLOW_BIAS_DEG = 0.35

communication.connect()

try:
    while True:
        frame = line_road.get_frame()
        lines_x, lines_y, line_x_slope, line_y_slope = line_road.load_frame(frame)
        x_offset, deg = line_road.calculate_direction(lines_x, line_x_slope)
        print(f"x-offset: {x_offset}, deg: {deg}, Now-step: {line_road.now_step}")

        line_follow_P_old = line_follow_P
        line_follow_P = (-1)*(x_offset * LINE_FOLLOW_BIAS_OFFSET) + ((deg-90) * LINE_FOLLOW_BIAS_DEG)
        line_follow_I += line_follow_P
        line_follow_D = line_follow_P - line_follow_P_old

        line_follow_PID = line_follow_P * LINE_FOLLOW_P_BIAS + line_follow_I * LINE_FOLLOW_I_BIAS + line_follow_D * LINE_FOLLOW_D_BIAS
        communication.motor_turn_deg(1, line_follow_PID + 90)


        # 按 'q' 鍵退出
        # while True:
        #     if cv2.waitKey(1) & 0xFF == ord('n'):
        #         break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Aborted!")
    communication.motor_stop()