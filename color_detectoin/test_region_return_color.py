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

    # 設定中心區域的範圍 (20x20 區域)
    offset = 15  # 一邊 10 個像素，形成 20x20 的區域
    center_x, center_y = width // 2, height // 2
    start_x, start_y = center_x - offset, center_y - offset
    end_x, end_y = center_x + offset, center_y + offset

    # 將影像從 BGR 轉換為 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 取得中央 20x20 區域的 HSV 值
    center_region = hsv[start_y:end_y, start_x:end_x]

    # 計算該區域的平均 HSV 值
    avg_hsv = np.mean(center_region, axis=(0, 1))

    # 判斷平均 HSV 值是否落入藍色、紅色、或綠色範圍
    if (lower_blue <= avg_hsv).all() and (avg_hsv <= upper_blue).all():
        print("B")  # 該區域內平均是藍色
    elif ((lower_red1 <= avg_hsv).all() and (avg_hsv <= upper_red1).all()) or \
         ((lower_red2 <= avg_hsv).all() and (avg_hsv <= upper_red2).all()):
        print("R")  # 該區域內平均是紅色
    elif (lower_green <= avg_hsv).all() and (avg_hsv <= upper_green).all():
        print("G")  # 該區域內平均是綠色
    else:
        print("N")  # 該區域內沒有明顯的紅、藍、或綠色

    # 在影像上標示中央 20x20 區域
    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    cv2.imshow('Frame', frame)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
