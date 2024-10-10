import cv2
import numpy as np

def show_img(windowName, img, size_x=800, size_y=600):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, size_x, size_y)
    cv2.imshow(windowName, img)

def empty(v):
    pass

# 读取和调整图像大小
img = cv2.imread('images/fence_terrible.jpg')
img = cv2.resize(img, (0, 0), fx=2.5, fy=2.5)

# 创建窗口和滑动条
cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 640, 320)
cv2.createTrackbar('Hue Min', 'TrackBar', 0, 179, empty) # 色调
cv2.createTrackbar('Hue Max', 'TrackBar', 179, 179, empty)
cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty) # 饱和度
cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty) # 亮度
cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)

# 转换成HSV值
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

while True:
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')

    print(h_min, h_max, s_min, s_max, v_min, v_max)
    
    # 创建掩膜
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    
    # 显示图像
    show_img('Original', img)
    show_img('HSV', hsv)
    show_img('Mask', mask)
    show_img('Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
