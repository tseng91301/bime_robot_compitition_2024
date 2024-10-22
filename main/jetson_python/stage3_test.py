from include import goose_weight, recognition, communication
import cv2

while True:
    frame = recognition.get_frame()
    item = recognition.detect(frame)
    print(f"item: {item}")

    # 裁減影像，範圍為 x: 300 到 500, y: 0 到 400 (y 不變)
    cropped_frame = frame[:, 300:500]

    # 顯示裁減後的影像
    cv2.imshow('Detection Window', cropped_frame)

    # 檢查 item[3] 是否有偵測到物體
    rooster_exist = 0  # 初始化
    starling_exist = 0  # 初始化

    if len(item[3]) > 0:
        rooster_exist = 1
    if len(item[4]) > 0:
        starling_exist = 1

    # 停止條件
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# 釋放資源，關閉所有視窗
cv2.destroyAllWindows()
