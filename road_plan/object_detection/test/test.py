import cv2
import numpy as np

# 1. 讀取圖像
image = cv2.imread('test1.png')

# 2. 將圖像轉換為灰階
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

# 3. 使用 Canny 邊緣檢測
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# 4. 使用 HoughLinesP 來偵測線條 (概率霍夫變換)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

# 5. 繪製偵測到的線條
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 6. 顯示結果
cv2.imshow('Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
