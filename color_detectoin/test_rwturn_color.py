import cv2
import numpy as np

# 開啟視頻捕捉，0 是內建攝像頭，1 是外接攝像頭
cap = cv2.VideoCapture(0)

# 設定藍色範圍
lower_blue = np.array([80, 0, 0])  # 藍色範圍的低值 (H, S, V)
upper_blue = np.array([140, 255, 255])  # 藍色範圍的高值 (H, S, V)

# 設定紅色範圍（紅色需要分兩個範圍處理，因為它跨越了 0 度）
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# 設定綠色範圍
lower_green = np.array([35, 100, 0])  # 綠色範圍的低值 (H, S, V)
upper_green = np.array([80, 255, 255])  # 綠色範圍的高值 (H, S, V)

while True:
    # 讀取一幀影像
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break

    # 獲取影像大小
    height, width, _ = frame.shape

    # 將影像從 BGR 轉換為 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 取得影像中央點的 HSV 值
    center_x, center_y = width // 2, height // 2
    center_pixel_hsv = hsv[center_y, center_x]

    # 判斷中央點的顏色
    if (lower_blue <= center_pixel_hsv).all() and (center_pixel_hsv <= upper_blue).all():
        print("B")  # 中央點是藍色
    elif ((lower_red1 <= center_pixel_hsv).all() and (center_pixel_hsv <= upper_red1).all()) or \
         ((lower_red2 <= center_pixel_hsv).all() and (center_pixel_hsv <= upper_red2).all()):
        print("R")  # 中央點是紅色
    elif (lower_green <= center_pixel_hsv).all() and (center_pixel_hsv <= upper_green).all():
        print("G")  # 中央點是綠色
    else:
        print("N")  # 中央點不是紅、藍、或綠色

    # 在影像上標示中央點
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
    cv2.imshow('Frame', frame)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
