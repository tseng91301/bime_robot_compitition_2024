import cv2
import numpy as np
import time

def show_lines(img, show_in_img = False):
    # 2. 將圖像轉換為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 使用 Canny 邊緣檢測
    edges = cv2.Canny(gray, 50, 80, apertureSize=3)

    # 4. 使用 HoughLinesP 來偵測線條 (概率霍夫變換)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=10, minLineLength=100, maxLineGap=30)

    if(show_in_img):
        # 5. 繪製偵測到的線條
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return lines

def calculate_max_diff(num_arr: dict, max_index):
    l = len(num_arr)
    add_sum = 0
    for i in range(l):
        if(i == max_index):
            continue
        add_sum += num_arr[i]
    add_sum /= (l-1)
    return num_arr[max_index] - add_sum

def get_max_channel_index(img):
    # 1. 拆分 RGB 通道
    blue_channel, green_channel, red_channel = cv2.split(img)

    # 2. 將三個通道堆疊成一個三維陣列
    stacked_channels = np.stack([blue_channel, green_channel, red_channel], axis=-1)

    # 3. 使用 np.argmax 來獲取每個像素的最大值所在的索引 (0=藍色, 1=綠色, 2=紅色)
    max_channel_indices = np.argmax(stacked_channels, axis=-1)

    return max_channel_indices

def pure_red(img):
    MIN_DIFF_VALUE = 60

    # 1. 拆分 RGB 通道
    blue_channel, green_channel, red_channel = cv2.split(img)
    print("Image shape:", img.shape)

    # 2. 對每個像素的紅色、綠色和藍色通道取最大值索引
    max_index = get_max_channel_index(img)

    # 3. 初始化 result_image，保持與 img 相同大小和類型
    result_image = np.zeros(img.shape, dtype=np.uint8)

    # 4. 將每個像素的最大通道設為 255，其他通道保持為 0
    for i in range(img.shape[0]):  # 對每一行
        for j in range(img.shape[1]):  # 對每一列
            if(max_index[i, j] == 2 and calculate_max_diff(img[i, j], 2) >= MIN_DIFF_VALUE):
                result_image[i, j, 2] = 255

    print("Result image shape:", result_image.shape)

    # 5. 直接返回 result_image 作為 OpenCV 圖片
    return result_image

video_path = "test3.mp4"

# 1. 打開影片文件
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: 無法打開影片文件")
    exit()

VIDEO_ORIGINAL_VIDEO_NAME = "Original"
VIDEO_PROCESSED_VIDEO_NAME = "Video Processed"

VIDEO_OUT_SIZE_X = 300
VIDEO_OUT_SIZE_Y = 450

cv2.namedWindow(VIDEO_ORIGINAL_VIDEO_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(VIDEO_ORIGINAL_VIDEO_NAME, VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y)

cv2.namedWindow(VIDEO_PROCESSED_VIDEO_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(VIDEO_PROCESSED_VIDEO_NAME, VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (VIDEO_OUT_SIZE_X, VIDEO_OUT_SIZE_Y))
    frame_red_out = pure_red(frame)
    show_lines(frame_red_out, True)
    cv2.imshow(VIDEO_ORIGINAL_VIDEO_NAME, frame)
    cv2.imshow(VIDEO_PROCESSED_VIDEO_NAME, frame_red_out)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
