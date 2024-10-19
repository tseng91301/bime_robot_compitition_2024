from include import line_road
import cv2
import numpy as np
# from include import recognition

log = ""
now_step = 0 # 紀錄目前做到第幾關

line_following_switch = 1 # 尋線開關

def end():
    # 程式結束時會做的事情
    open("logs/workflow.log", "w").write(log)
    return

while True:
    frame = line_road.get_frame()
    try:
        if frame == 0:
            end()
            break
    except:
        pass

    if line_following_switch:
        lines_x, lines_y, lines_x_slope, lines_y_slope = line_road.load_frame(frame)
        x_offset, direction = line_road.calculate_direction(lines_x, lines_x_slope)
        log += f"Direction: {direction}\n"
        log += f"x_offset: {x_offset}\n"
        print(direction)
        if now_step != line_road.now_step:
            now_step = line_road.now_step
            log += "Now step changed to: " + str(now_step) + "\n"
        pass
    log += "\n"
    # print(recognition.detect())
    if cv2.waitKey(33) & 0xFF == ord('q'):
        end()
        break