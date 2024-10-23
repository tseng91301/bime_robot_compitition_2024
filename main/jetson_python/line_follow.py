from include import line_road
import cv2

while True:
    frame = line_road.get_frame()
    lines_x, lines_y, line_x_slope, line_y_slope = line_road.load_frame(frame)
    x_offset, deg = line_road.calculate_direction(lines_x, line_x_slope)
    print(f"x-offset: {x_offset}, deg: {deg}, Now-step: {line_road.now_step}")

    # 按 'q' 鍵退出
    while True:
        if cv2.waitKey(1) & 0xFF == ord('n'):
            break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break