import json
import cv2
import numpy as np

conf_path = "conf/goose_weight.json"

with open(conf_path, 'r') as f:
    conf = json.loads(f.read())
    f.close()
    pass

COLOR_NONE = -1
COLOR_RED = 0
COLOR_GREEN = 1
COLOR_BLUE = 2

# 設定藍色範圍
lower_blue = np.array(conf["color_range"]["blue"]["lower"])  # 藍色範圍的低值 (H, S, V)
upper_blue = np.array(conf["color_range"]["blue"]["upper"])  # 藍色範圍的高值 (H, S, V)

# 設定紅色範圍（紅色需要分兩個範圍處理，因為它跨越了 0 度）
lower_red1 = np.array(conf["color_range"]["red1"]["lower"])
upper_red1 = np.array(conf["color_range"]["red1"]["upper"])
lower_red2 = np.array(conf["color_range"]["red2"]["lower"])
upper_red2 = np.array(conf["color_range"]["red2"]["upper"])

# 設定綠色範圍
lower_green = np.array(conf["color_range"]["green"]["lower"])  # 綠色範圍的低值 (H, S, V)
upper_green = np.array(conf["color_range"]["green"]["upper"])  # 綠色範圍的高值 (H, S, V)

x_start = conf["detect_range"]["x_start"]
x_width = conf["detect_range"]["width"]
y_start = conf["detect_range"]["y_start"]
y_height = conf["detect_range"]["height"]

PREVIEW = conf["preview"]
preview_window_name = conf["preview_window_name"]

def color_block_detect(frame: np.ndarray):
    # 獲取影像大小
    height, width, _ = frame.shape
    x_s = int(width * x_start)
    y_s = int(height * y_start)
    w = int(width * x_width)
    h = int(height * y_height)

    # 將影像從 BGR 轉換為 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detect_region = hsv[y_s:y_s + h, x_s:x_s + w]

    # 計算該區域的平均 HSV 值
    avg_hsv = np.mean(detect_region, axis=(0, 1))

    return_color = COLOR_NONE

    # 判斷平均 HSV 值是否落入藍色、紅色、或綠色範圍
    if (lower_blue <= avg_hsv).all() and (avg_hsv <= upper_blue).all():
        return_color =  COLOR_BLUE
    elif ((lower_red1 <= avg_hsv).all() and (avg_hsv <= upper_red1).all()) or \
         ((lower_red2 <= avg_hsv).all() and (avg_hsv <= upper_red2).all()):
        return_color =  COLOR_RED
    elif (lower_green <= avg_hsv).all() and (avg_hsv <= upper_green).all():
        return_color =  COLOR_GREEN
    else:
        return_color =  COLOR_NONE
        pass

    if PREVIEW:
        preview_frame = frame.copy()
        cv2.namedWindow(preview_window_name)
        cv2.rectangle(preview_frame, (x_s, y_s), (x_s + w, y_s + h), (0, 255, 0), 2)
        cv2.imshow(preview_window_name, preview_frame)
        pass

    return return_color
