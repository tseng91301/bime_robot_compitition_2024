import cv2
import numpy as np

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

def show_img(windowName, img, size_x=800, size_y=600):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, size_x, size_y)
    cv2.imshow(windowName, img)

# 1. 讀取圖像
image = cv2.imread('test2.jpg')
image = cv2.resize(image, (300, 180))

image_red_out = pure_red(image)

# 2. 將圖像從 BGR 轉換為 HSV
hsv = cv2.cvtColor(image_red_out, cv2.COLOR_BGR2HSV)

# 3. 定義紅色範圍 (注意紅色分佈在兩個範圍內)
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([40, 255, 255])
lower_red2 = np.array([165, 120, 70])
upper_red2 = np.array([180, 255, 255])

# 4. 創建兩個掩模來篩選紅色區域
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

# 5. 合併兩個掩模
mask = mask1 + mask2

# 6. 將紅色區域外的部分設為黑色
result = cv2.bitwise_and(image, image, mask=mask)

# 7. 顯示結果
show_img('Original Image', image)
show_img('Red Only Image', result)
show_img('image red out', image_red_out)
# cv2.imshow('Original Image', image)
# cv2.imshow('Red Only Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
