import cv2
import numpy as np

# 開啟視頻捕捉，0 是內建攝像頭，1 是外接攝像頭
cap = cv2.VideoCapture(0)

# 設定藍色範圍
lower_blue = np.array([100, 150, 0])  # 藍色範圍的低值 (H, S, V)
upper_blue = np.array([140, 255, 255])  # 藍色範圍的高值 (H, S, V)

# 設定紅色範圍（紅色需要分兩個範圍處理，因為它跨越了 0 度）
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# 設定綠色範圍
lower_green = np.array([35, 100, 100])  # 綠色範圍的低值 (H, S, V)
upper_green = np.array([85, 255, 255])  # 綠色範圍的高值 (H, S, V)

while True:
    # 讀取一幀影像
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break

    # 將影像從 BGR 轉換為 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 創建藍色遮罩
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # 創建紅色遮罩（需要合併兩個範圍的遮罩）
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # 創建綠色遮罩
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # 使用遮罩過濾出原影像中的顏色區域
    result_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    result_green = cv2.bitwise_and(frame, frame, mask=mask_green)

    # 顯示原影像
    cv2.imshow('Original', frame)

    # 顯示藍色的遮罩和結果
    #cv2.imshow('Blue Mask', mask_blue)
    cv2.imshow('Blue Result', result_blue)

    # 顯示紅色的遮罩和結果
    #cv2.imshow('Red Mask', mask_red)
    cv2.imshow('Red Result', result_red)

    # 顯示綠色的遮罩和結果
    #cv2.imshow('Green Mask', mask_green)
    cv2.imshow('Green Result', result_green)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
