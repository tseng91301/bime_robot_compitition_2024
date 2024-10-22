from include import goose_weight, recognition, communication
import cv2

while True:
    frame = recognition.get_frame()
    
    # 裁減影像，範圍為 x: 300 到 500, y: 50 到 350
    cropped_frame = frame[50:350, 300:500]

    # 在裁減的影像上進行物體偵測
    item = recognition.detect(cropped_frame)
    print(f"item: {item}")

    # 在原始影像上顯示裁減的範圍 (可選)
    cv2.rectangle(frame, (300, 50), (500, 350), (0, 255, 0), 2)  # 在原始影像上畫出範圍框

    # 顯示整個影像
    cv2.imshow('Detection Window', frame)

    # 檢查 item[3] 是否有偵測到 rooster
    rooster_exist = 0  # 初始化
    starling_exist = 0  # 初始化

    print("dfni")

    if len(item[3]) > 0:
        rooster_exist = 1
        print("Rooster detected in the specified range.")
    else:
        print("No roosters detected in the specified range.")

    if len(item[4]) > 0:
        starling_exist = 1
        print("Starling detected in the specified range.")
    else:
        print("No starlings detected in the specified range.")

    # 停止條件
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# 釋放資源，關閉所有視窗
cv2.destroyAllWindows()
