import cv2
import numpy as np

def nothing(x):
    pass

def highlight_red_with_trackbar():
    # 1. 創建一個窗口
    cv2.namedWindow('Highlight Red')

    # 2. 創建滑桿來調整 HSV 範圍
    cv2.createTrackbar('Low H 1', 'Highlight Red', 0, 180, nothing)
    cv2.createTrackbar('High H 1', 'Highlight Red', 10, 180, nothing)
    cv2.createTrackbar('Low H 2', 'Highlight Red', 160, 180, nothing)
    cv2.createTrackbar('High H 2', 'Highlight Red', 180, 180, nothing)
    cv2.createTrackbar('Low S', 'Highlight Red', 120, 255, nothing)
    cv2.createTrackbar('High S', 'Highlight Red', 255, 255, nothing)
    cv2.createTrackbar('Low V', 'Highlight Red', 70, 255, nothing)
    cv2.createTrackbar('High V', 'Highlight Red', 255, 255, nothing)

    # 3. 打開攝像頭（0 表示預設攝像頭）
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("無法打開攝像頭")
        return

    while True:
        # 4. 從攝像頭讀取一幀影像
        ret, frame = cap.read()
        if not ret:
            print("無法獲取影像")
            break

        # 5. 將圖像轉換為 HSV 色彩空間
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 6. 從滑桿獲取當前 HSV 閾值
        low_h_1 = cv2.getTrackbarPos('Low H 1', 'Highlight Red')
        high_h_1 = cv2.getTrackbarPos('High H 1', 'Highlight Red')
        low_h_2 = cv2.getTrackbarPos('Low H 2', 'Highlight Red')
        high_h_2 = cv2.getTrackbarPos('High H 2', 'Highlight Red')
        low_s = cv2.getTrackbarPos('Low S', 'Highlight Red')
        high_s = cv2.getTrackbarPos('High S', 'Highlight Red')
        low_v = cv2.getTrackbarPos('Low V', 'Highlight Red')
        high_v = cv2.getTrackbarPos('High V', 'Highlight Red')

        # 7. 定義紅色的範圍，根據滑桿的值調整
        lower_red_1 = np.array([low_h_1, low_s, low_v])
        upper_red_1 = np.array([high_h_1, high_s, high_v])
        lower_red_2 = np.array([low_h_2, low_s, low_v])
        upper_red_2 = np.array([high_h_2, high_s, high_v])

        # 8. 創建遮罩，提取出紅色區域
        mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
        mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
        mask = mask_1 + mask_2

        # 9. 將紅色區域提取出來
        red_highlighted = cv2.bitwise_and(frame, frame, mask=mask)

        # 10. 將其他顏色轉換為灰度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # 11. 合併紅色區域和灰度圖像，保持紅色，其他部分變灰
        result = np.where(red_highlighted != 0, red_highlighted, gray_colored)

        # 12. 顯示結果
        cv2.imshow('Highlight Red', result)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 13. 釋放攝像頭並關閉所有窗口
    cap.release()
    cv2.destroyAllWindows()

# 測試代碼
highlight_red_with_trackbar()