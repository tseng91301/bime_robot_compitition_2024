import cv2
import numpy as np

# 開啟視頻捕捉，0 是內建攝像頭，1 是外接攝像頭
cap = cv2.VideoCapture(0)

# 設定顏色範圍（這裡是藍色的範圍）
lower_blue = np.array([100, 150, 0])  # 藍色範圍的低值 (H, S, V)
upper_blue = np.array([140, 255, 255])  # 藍色範圍的高值 (H, S, V)

lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

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

    # 創建遮罩，範圍內的顏色設為白色，其他顏色設為黑色
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 使用遮罩過濾出原影像中的顏色區域
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 顯示原影像、遮罩和結果
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝像頭資源並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
