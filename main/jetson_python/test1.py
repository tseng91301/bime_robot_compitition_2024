from include import line_road
import cv2
import numpy as np
# from include import recognition

log = ""
now_step = 0

while True:
    frame = line_road.get_frame()
    lines_x, lines_y, lines_x_slope, lines_y_slope = line_road.load_frame(frame)
    direction = line_road.calculate_direction(lines_x, lines_x_slope)
    log += f"Direction: {direction}\n"
    print(direction)
    # log += f"lines_x: {np.degrees(np.arctan(np.array(lines_x_slope)))}\n"
    # log += f"lines_y: {np.degrees(np.arctan(np.array(lines_y_slope)))}\n"
    if now_step != line_road.now_step:
        now_step = line_road.now_step
        log += "Now step changed to: " + str(now_step) + "\n"
    log += "\n"
    # print(recognition.detect())
    if cv2.waitKey(33) & 0xFF == ord('q'):
        open("logs/workflow.log", "w").write(log)
        break