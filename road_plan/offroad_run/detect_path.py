import cv2
import numpy as np

# Definition
sampling_y_place = 0.6 # 在圖像y座標60%的地方取樣，作為判定直線距離的參考位置

# 加载图像并转换为灰度
img = cv2.imread('images/fence_terrible_detected.jpg')
img_height, img_width, img_channels = img.shape # Get the basic property of image
sampling_y_coordinate = int(img_height * sampling_y_place) # Get sampling y coordinate
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 边缘检测
edges = cv2.Canny(gray, 50, 150)

# 使用霍夫线变换检测直线
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

def line_intersection_y(x1, y1, x2, y2, y_r):
    if y_r in range(min(y1, y2), max(y1, y2)):
        if x1 <= x2:
            intercept_x = x2 - (x2 - x1) * (abs(y2 - y_r) / abs(y2 - y1))
        else:
            intercept_x = x1 - (x1 - x2) * (abs(y2 - y_r) / abs(y2 - y1))
        return intercept_x
    else:
        return -1

# 在图像中绘制检测到的线条
valid_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]

    # 驗證此線段是否可以作為參考邊界線，並且算出其與參考y做標線之焦點
    intercept_x = line_intersection_y(x1, y1, x2, y2, sampling_y_coordinate)
    if(intercept_x != -1):
        valid_lines.append([x1, y1, x2, y2, int(intercept_x), sampling_y_coordinate])
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        pass

# 使用 sort 方法进行排序(使用列表個項目中第4個值為基準下去排序)
valid_lines.sort(key=lambda x: x[4])

# 算各個焦點的距離，求其中最大值及最大值發生的第一點x值
largest_dist = 0
largest_dist_start_x = 0
for i, v in enumerate(valid_lines):
    if i >= len(valid_lines)-1:
        continue
    tmp_dist = valid_lines[i+1][4] - valid_lines[i][4]
    if tmp_dist >= largest_dist_start_x:
        largest_dist = tmp_dist
        largest_dist_start_x = valid_lines[i][4]

# 劃出基準y線
cv2.line(img, (0, sampling_y_coordinate), (img_width-1, sampling_y_coordinate), (255, 255, 0), 2)

# 將所有參考邊界線都顯示出來
for v in valid_lines:
    x, y = v[4], v[5]
    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

# 劃出路徑中線
road_center_x = int(largest_dist_start_x + largest_dist/2)
cv2.line(img, (road_center_x, 0), (road_center_x, img_height), (0, 255, 255), 2)
cv2.line(img, (int(img_width/2), 0), (int(img_width/2), img_height), (0, 136, 255), 2)

cv2.imshow('Detected Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
