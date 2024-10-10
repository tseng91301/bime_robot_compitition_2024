import cv2
import numpy as np

def show_img(windowName, img, size_x=800, size_y=600):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, size_x, size_y)
    cv2.imshow(windowName, img)

# 1. 讀取圖像
image = cv2.imread('test1.png')

# 2. 將圖像從 BGR 轉換為 HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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
# cv2.imshow('Original Image', image)
# cv2.imshow('Red Only Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
