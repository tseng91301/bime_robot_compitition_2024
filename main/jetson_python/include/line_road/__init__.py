import os
import json
import numpy as np
import cv2

line_config_path = "conf/line_road.json"

with open(line_config_path, 'r') as f:
    line_config = json.loads(f.read())
    f.close()
    pass

source = line_config['source_type']
if source == "camera":
    camera_id = int(line_config[source])
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Can't access the camera: {camera_id}")
        exit()
        pass
    pass
elif source == "video":
    video_path = str(line_config[source])
    # 1. 打開影片文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 無法打開影片文件")
        exit()
        pass

VIDEO_OUT_SIZE_X = line_config['resolution']['x'] # 要換算的 x 解析度
VIDEO_OUT_SIZE_Y = line_config['resolution']['y'] # 要換算的 y 解析度
VIDEO_ORIGINAL_VIDEO_NAME = ""
VIDEO_PROCESSED_VIDEO_NAME = ""

LINE_FOLLOWING_VERTICAL_DETECT_RANGE = int(line_config['vertical_line_detect_range'] * VIDEO_OUT_SIZE_X / 2) # 換算出來垂直線的辨識範圍 (從中間往兩邊擴張)
LINE_FOLLOWING_HORIZONTAL_DETECT_RANGE = int(line_config['horizontal_line_detect_range'] * VIDEO_OUT_SIZE_Y) # 換算出來水平線的辨識範圍
LINE_FOLLOWING_HORIZONTAL_Y_BOTTOM = int(line_config['horizontal_line_detect_y_bottom'] * VIDEO_OUT_SIZE_Y) # 換算出來水平線辨識的起始 y 座標

VERTICAL_LINE_POS_M = np.tan(np.deg2rad(90 - line_config['vertical_line_degree'])) # 垂直線的正向斜率最小值
VERTICAL_LINE_NEG_M = np.tan(np.deg2rad(-90 + line_config['vertical_line_degree'])) # 垂直線的負向斜率最大值
HORIZONTAL_LINE_POS_M = np.tan(np.deg2rad(line_config['horizontal_line_degree'])) # 水平線的正向斜率最大值
HORIZONTAL_LINE_NEG_M = np.tan(np.deg2rad(-line_config['horizontal_line_degree'])) # 水平線的負向斜率最小值
HORIZONTAL_LINE = 0
VERTICAL_LINE = 1

VIDEO_OUT_PREVIEW = line_config['preview']

def show_lines(img, line_type: int, show_in_img = False):
    # 2. 將圖像轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 使用 Canny 邊緣檢測
    edges = cv2.Canny(gray, 50, 80, apertureSize=3)

    # 4. 使用 HoughLinesP 來偵測線條 (概率霍夫變換)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=115, minLineLength=100, maxLineGap=30)

    # 篩選線段，依照參數為HORIZONTAL 或 VERTICAL決定
    lines_filtered = []
    lines_slope = []
    if line_type == HORIZONTAL_LINE:
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # 避免垂直線 (斜率無法計算)
                if x2 - x1 == 0:
                    continue
                slope = -(y2 - y1) / (x2 - x1)
                if HORIZONTAL_LINE_NEG_M <= slope <= HORIZONTAL_LINE_POS_M:
                    lines_filtered.append(line)
                    lines_slope.append(slope)
                    pass
                pass
            pass
        pass
    elif line_type == VERTICAL_LINE:
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # 避免垂直線 (斜率無法計算)
                if x2 - x1 == 0:
                    lines_filtered.append(line)
                    lines_slope.append(1000)
                    continue
                slope = -(y2 - y1) / (x2 - x1)
                if slope >= VERTICAL_LINE_POS_M or slope <= VERTICAL_LINE_NEG_M:
                    lines_filtered.append(line)
                    lines_slope.append(slope)
                    pass
                pass
            pass
        pass

    if(show_in_img):
        # 5. 繪製偵測到的線條
        if lines_filtered is not None:
            for line in lines_filtered:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return lines_filtered, lines_slope

def create_red_mask(image): # 產生一個遮罩，使照片只顯示紅色部分(數值可以在conf配置文件修改)
    # 3. 將圖像轉換為 HSV 色彩空間
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 4. 從滑桿獲取當前 HSV 閾值
    low_h_1 = int(line_config['red_line']["low_h_1"])
    high_h_1 = int(line_config['red_line']["high_h_1"])
    low_h_2 = int(line_config['red_line']["low_h_2"])
    high_h_2 = int(line_config['red_line']["high_h_2"])
    low_s = int(line_config['red_line']["low_s"])
    high_s = int(line_config['red_line']["high_s"])
    low_v = int(line_config['red_line']["low_v"])
    high_v = int(line_config['red_line']["high_v"])

    # 5. 定義紅色的範圍，根據滑桿的值調整
    lower_red_1 = np.array([low_h_1, low_s, low_v])
    upper_red_1 = np.array([high_h_1, high_s, high_v])
    lower_red_2 = np.array([low_h_2, low_s, low_v])
    upper_red_2 = np.array([high_h_2, high_s, high_v])

    # 6. 創建遮罩，提取出紅色區域
    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = mask_1 + mask_2
    return mask

def get_frame(): # 取得當前攝影機的影像
    ret, frame = cap.read()
    if not ret:
        return 0
    frame = cv2.resize(frame, (VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y))
    return frame

no_horizontal_line_times = 0 # 目前沒有偵測到的橫線次數
ANOTHER_HORIZONTAL_LINE_DETECT_INTERVAL = line_config['another_horizontal_line_detect_interval']
MIN_VALID_HORIZONTAL_LINE_DETECT_INTERVAL = line_config['min_valid_horizontal_line_detect_times']
horizontal_lines_detected = 0 # 目前偵測到橫線的次數
now_step = 1 # 目前進行的關卡

def load_frame(frame): # 載入輸入的影像，切分成多種顯示方式(辨識垂直線和辨識水平線)，並從其獲取各條線的起始點、終點及斜率
    global horizontal_lines_detected
    global no_horizontal_line_times
    global now_step
    
    frame_center = int(VIDEO_OUT_SIZE_X/2)
    mask = create_red_mask(frame)
    frame_red_out = cv2.bitwise_and(frame, frame, mask=mask)
    detection_crop_vertical = frame_red_out[0:VIDEO_OUT_SIZE_Y-1, frame_center - LINE_FOLLOWING_VERTICAL_DETECT_RANGE:frame_center + LINE_FOLLOWING_VERTICAL_DETECT_RANGE]
    detection_crop_horizontal = frame_red_out[LINE_FOLLOWING_HORIZONTAL_Y_BOTTOM - LINE_FOLLOWING_HORIZONTAL_DETECT_RANGE: LINE_FOLLOWING_HORIZONTAL_Y_BOTTOM, 0:VIDEO_OUT_SIZE_X-1]
    if VIDEO_OUT_PREVIEW == 1:
        lines_x, line_x_slope = show_lines(detection_crop_vertical, VERTICAL_LINE, show_in_img=True) # 儲存垂直的線條(在x軸分布)
        lines_y, line_y_slope = show_lines(detection_crop_horizontal, HORIZONTAL_LINE, show_in_img=True) # 儲存水平的線條(在y軸分布)
        VIDEO_ORIGINAL_VIDEO_NAME = line_config['preview_origin_name']
        VIDEO_PROCESSED_VIDEO_NAME = line_config['preview_processed_name']
        cv2.imshow("Vertical", detection_crop_vertical)
        cv2.imshow("Horizontal", detection_crop_horizontal)
        cv2.imshow(VIDEO_PROCESSED_VIDEO_NAME, frame_red_out)
    else:
        lines_x, line_x_slope = show_lines(detection_crop_vertical, VERTICAL_LINE, show_in_img=False) # 儲存垂直的線條(在x軸分布)
        lines_y, line_y_slope = show_lines(detection_crop_horizontal, HORIZONTAL_LINE, show_in_img=False) # 儲存水平的線條(在y軸分布)
        pass
    if len(lines_y) == 0:
        no_horizontal_line_times += 1
        if no_horizontal_line_times >= ANOTHER_HORIZONTAL_LINE_DETECT_INTERVAL:
            horizontal_lines_detected = 0
    else:
        horizontal_lines_detected += 1
        if no_horizontal_line_times >= ANOTHER_HORIZONTAL_LINE_DETECT_INTERVAL and horizontal_lines_detected >= MIN_VALID_HORIZONTAL_LINE_DETECT_INTERVAL:
            no_horizontal_line_times = 0
            now_step += 1

    return lines_x, lines_y, line_x_slope, line_y_slope

def calculate_direction(lines_x, lines_x_slope): # 透過各個線段極其斜率判斷車子的行進方向 0: 直走, 愈左邊愈正，右邊相反
    if(len(lines_x_slope) == 0):
        return 0, 0
    lines_x_deg = np.degrees(np.arctan(np.array(lines_x_slope)))
    x_deg_min = np.min(lines_x_deg)
    x_deg_max = np.max(lines_x_deg)
    if(x_deg_min < 0):
        x_deg_min += 180
    if(x_deg_max < 0):
        x_deg_max += 180

    # 計算目前距離中心點的偏移
    x_avg = 0
    for v in lines_x:
        x_avg += (v[0, 0] + v[0, 2])/2
        pass
    x_avg /= len(lines_x)
    x_offset = x_avg - (VIDEO_OUT_SIZE_X / 2)
    
    deg_avg = (x_deg_min + x_deg_max) / 2
    return x_offset, deg_avg