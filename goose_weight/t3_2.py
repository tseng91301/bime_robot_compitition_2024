import cv2

def show_img(windowName, img, size_x=800, size_y=600):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, size_x, size_y)
    cv2.imshow(windowName, img)

# 读取图像并创建一个副本用于绘制轮廓
img = cv2.imread('images/boxes.jpg')
imgCountour = img.copy()

# 转换为灰度图像
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用Canny边缘检测
canny = cv2.Canny(img_gray, 150, 200)

# 查找轮廓
contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 绘制轮廓
for cnt in contours:
    cv2.drawContours(imgCountour, cnt, -1, (255, 0, 0), 4)

# 显示图像
show_img('Original Image', img)
show_img('Gray Image', img_gray)
show_img('Canny Edges', canny)
show_img('Contours', imgCountour)  # 显示绘制了轮廓的图像

cv2.waitKey(0)
cv2.destroyAllWindows()
