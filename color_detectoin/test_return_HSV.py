import cv2
import numpy as np

# 開啟視頻捕捉，0 代表第一個攝像頭，1 代表外接攝像頭
cap = cv2.VideoCapture(0)

while True:
    # 讀取一幀影像
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break

    # 獲取影像大小
    height, width, _ = frame.shape

    # 計算影像中心點的座標
    center_x, center_y = width // 2, height // 2

    # 將影像從 BGR 轉換為 HSV 格式
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 讀取中心點的 HSV 值
    center_pixel_hsv = hsv_frame[center_y, center_x]
    h, s, v = center_pixel_hsv  # 分別取色相、飽和度和亮度

    # 打印出中心點的 HSV 值
    print(f"中心點的 HSV 值: H: {h}, S: {s}, V: {v}")

    # 在影像上標示出中心點
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), 2)

    # 顯示影像
    cv2.imshow('Frame', frame)

    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
