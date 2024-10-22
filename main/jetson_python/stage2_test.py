from include import goose_weight, recognition, communication
import cv2

communication.start_ult_service()

while True:
    print(123)
    frame = recognition.get_frame()
    print(456)
    item = recognition.detect(frame)
    print(f"item: {item}")

    cv2.imshow('Detection Window', frame)

    # 檢查 item[1] 是否有偵測到物體
    if len(item[0]) > 0:
        print(item[0])
        #communication.send(communication.ser_ults, "l r 1000")

        # 取得中心點的 x 和 y
        center_x = item[0][0][4]
        center_y = item[0][0][5]
        print("Center x:", center_x)
        print("Center y:", center_y)

        cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)  # 圓圈半徑 10，紅色 (BGR: 0, 0, 255)

    else:
        print("No objects detected for class 0.")

    # 停止條件
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break
