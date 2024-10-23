from include import communication
from include import line_road
import cv2
import numpy as np
from include import recognition

log = ""
now_step = 0 # 紀錄目前做到第幾關

line_following_switch = 1 # 尋線開關

def send_to_arduino(command):
    # 這裡是你發送指令到Arduino的函數，根據你的通訊方式填入具體的邏輯
    pass

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
        lines_x, lines_y, lines_x_slope, lines_y_slope = line_road.load_frame(frame) # 從目前的影像獲取以上資訊
        x_offset, direction = line_road.calculate_direction(lines_x, lines_x_slope) # 計算目前的方向和 x 軸位移
        log += f"Direction: {direction}\n"

