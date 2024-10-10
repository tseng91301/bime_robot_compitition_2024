import cv2
import numpy as np

# 加载图像并转换为灰度
img = cv2.imread('images/fence_terrible_detected.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 边缘检测
edges = cv2.Canny(gray, 50, 150)

# 使用霍夫线变换检测直线
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

# 在图像中绘制检测到的线条
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.line(img, (0, 500), (800, 500), (255, 255, 0), 2)

cv2.imshow('Detected Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
