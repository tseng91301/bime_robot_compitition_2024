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

VIDEO_OUT_SIZE_X = line_config['resolution']['x']
VIDEO_OUT_SIZE_Y = line_config['resolution']['y']
VIDEO_ORIGINAL_VIDEO_NAME = ""
VIDEO_PROCESSED_VIDEO_NAME = ""

LINE_FOLLOWING_VERTICAL_DETECT_RANGE = int(line_config['vertical_line_detect_range'] * VIDEO_OUT_SIZE_X / 2)

VIDEO_OUT_PREVIEW = line_config['preview']

def show_lines(img, show_in_img = False):
    # 2. 將圖像轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 使用 Canny 邊緣檢測
    edges = cv2.Canny(gray, 50, 80, apertureSize=3)

    # 4. 使用 HoughLinesP 來偵測線條 (概率霍夫變換)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=115, minLineLength=100, maxLineGap=30)

    if(show_in_img):
        # 5. 繪製偵測到的線條
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return lines

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

def load_frame(return_frame = False):
    frame = get_frame()
    try:
        if type(frame) == int and frame == 0:
            print("Video got ended or corrupted")
            return None
    except Exception as e:
        print("Error occur when getting video: ", str(e))
        return None
    mask = create_red_mask(frame)
    frame_red_out = cv2.bitwise_and(frame, frame, mask=mask)
    if VIDEO_OUT_PREVIEW == 1:
        lines = show_lines(frame_red_out, True)
        VIDEO_ORIGINAL_VIDEO_NAME = line_config['preview_origin_name']
        VIDEO_PROCESSED_VIDEO_NAME = line_config['preview_processed_name']
        cv2.imshow(VIDEO_ORIGINAL_VIDEO_NAME, frame)
        cv2.imshow(VIDEO_PROCESSED_VIDEO_NAME, frame_red_out)
    else:
        lines = show_lines(frame_red_out, False)
        pass
    if return_frame:
        return lines, frame
    else:
        return lines