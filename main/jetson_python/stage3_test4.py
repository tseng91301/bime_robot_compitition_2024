from include import goose_weight, recognition, communication
import cv2

while True:
    frame = recognition.get_frame()  # 獲取當前影像

    # 裁減影像，範圍為 x: 300 到 500, y: 50 到 350
    cropped_frame = frame[50:350, 300:500]

    # 在裁減的影像上進行物體偵測
    item = recognition.detect(cropped_frame)
    print(f"item: {item}")

    # 顯示裁減後的影像
    cv2.imshow('Detection Window', frame)
    cv2.imshow('Cropped Detection Window', cropped_frame)
    
    if len(item[4]) > 0:
        print("starling")
        communication.send(communication.ser_ults,"l r 3000")
        communication.send(communication.ser_ults,"r 3000")
        #communication.send(communication.ser_ults,"m ")

    # 停止條件
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# 釋放資源，關閉所有視窗
cv2.destroyAllWindows()
