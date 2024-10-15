import cv2
import numpy as np


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

def create_red_mask(image):
    # 3. 將圖像轉換為 HSV 色彩空間
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 4. 從滑桿獲取當前 HSV 閾值
    low_h_1 = 0
    high_h_1 = 27
    low_h_2 = 139
    high_h_2 = 180
    low_s = 100
    high_s = 255
    low_v = 118
    high_v = 255

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