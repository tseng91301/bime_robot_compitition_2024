import cv2

def show_img(windowName, img, size_x=800, size_y=600):
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, size_x, size_y)
    cv2.imshow(windowName, img)

img = cv2.imread('images/boxes.jpg')
imgCountour = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(img, 70, 75)
contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    cv2.drawContours(imgCountour, cnt, -1, (255, 0, 0), 4)
    # print(cv2.contourArea(cnt)).
    # print(cv2.arcLength(cnt, True))
    area = cv2.contourArea(cnt)
    if(area > 500):
        peri = cv2.arcLength(cnt, True)
        vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
        # print(len(vertices))
        corners = len(vertices)
        x, y, w, h = cv2.boundingRect(vertices)
        cv2.rectangle(imgCountour, (x, y), (x+w, y+h), (0, 255, 0), 4)
        if(corners == 3):
            cv2.putText(imgCountour, 'Triangle', (x, y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        elif corners == 4:
            cv2.putText(imgCountour, 'Rectangle', (x, y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        elif corners == 5:
            cv2.putText(imgCountour, 'Pentagon', (x, y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        elif corners >= 6:
            cv2.putText(imgCountour, 'Circle', (x, y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)


# cv2.imshow('img', img)
show_img('canny', canny)
show_img('Countours', imgCountour)
cv2.waitKey(0)
