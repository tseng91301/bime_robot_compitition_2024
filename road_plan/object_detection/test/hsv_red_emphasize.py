import cv2
import numpy as np

def create_red_mask():
    # 3. 將圖像轉換為 HSV 色彩空間
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 4. 從滑桿獲取當前 HSV 閾值
    low_h_1 = 0
    high_h_1 = 27
    low_h_2 = 139
    high_h_2 = 180
    low_s = 123
    high_s = 255
    low_v = 186
    high_v = 255

    # 5. 定義紅色的範圍，根據滑桿的值調整
    lower_red_1 = np.array([low_h_1, low_s, low_v])
    upper_red_1 = np.array([high_h_1, high_s, high_v])
    lower_red_2 = np.array([low_h_2, low_s, low_v])
    upper_red_2 = np.array([high_h_2, high_s, high_v])

    # 6. 創建遮罩，提取出紅色區域
    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = mask_1 + mask_2
    return mask

def nothing(x):
    pass

def highlight_red_with_trackbar(image):

    while True:
        # 3. 將圖像轉換為 HSV 色彩空間
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 4. 從滑桿獲取當前 HSV 閾值
        low_h_1 = 0
        high_h_1 = 27
        low_h_2 = 139
        high_h_2 = 180
        low_s = 123
        high_s = 255
        low_v = 186
        high_v = 255

        # 5. 定義紅色的範圍，根據滑桿的值調整
        lower_red_1 = np.array([low_h_1, low_s, low_v])
        upper_red_1 = np.array([high_h_1, high_s, high_v])
        lower_red_2 = np.array([low_h_2, low_s, low_v])
        upper_red_2 = np.array([high_h_2, high_s, high_v])

        # 6. 創建遮罩，提取出紅色區域
        mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
        mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
        mask = mask_1 + mask_2

        # 7. 將紅色區域提取出來
        red_highlighted = cv2.bitwise_and(image, image, mask=mask)

        # 8. 將其他顏色轉換為灰度
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # 9. 合併紅色區域和灰度圖像，將紅色保持顏色，其他部分變灰
        result = np.where(red_highlighted != 0, red_highlighted, gray_colored)

        # 10. 顯示結果
        cv2.imshow('Highlight Red', result)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# 測試代碼
image_path = 'test1.png'  # 替換為圖片路徑
image = cv2.imread(image_path)
image = cv2.resize(image, (300, 550))
highlight_red_with_trackbar(image)
