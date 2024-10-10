import cv2
import numpy as np
import time

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

video_path = "test3.mp4"

# 1. 打開影片文件
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: 無法打開影片文件")
    exit()

VIDEO_ORIGINAL_VIDEO_NAME = "Original"
VIDEO_PROCESSED_VIDEO_NAME = "Video Processed"

VIDEO_OUT_SIZE_X = 400
VIDEO_OUT_SIZE_Y = 600

cv2.namedWindow(VIDEO_ORIGINAL_VIDEO_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(VIDEO_ORIGINAL_VIDEO_NAME, VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y)

cv2.namedWindow(VIDEO_PROCESSED_VIDEO_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(VIDEO_PROCESSED_VIDEO_NAME, VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y))
    mask = create_red_mask(frame)
    frame_red_out = cv2.bitwise_and(frame, frame, mask=mask)
    show_lines(frame_red_out, True)
    cv2.imshow(VIDEO_ORIGINAL_VIDEO_NAME, frame)
    cv2.imshow(VIDEO_PROCESSED_VIDEO_NAME, frame_red_out)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
