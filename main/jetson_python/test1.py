from include import goose_weight, recognition, communication
import cv2

while True:
    frame = recognition.get_frame()
    item = recognition.detect(frame)
    print(f"item: {item}")

    # 檢查 item[0] 是否有偵測到物體
    if len(item[0]) > 0:
        #print(item[0])

        # 取得中心點的 x 和 y
        center_x = item[0][0][4]
        center_y = item[0][0][5]
        print("Center x:", center_x)
        print("Center y:", center_y)

        # 在中心點畫一個圓圈 (使用紅色 BGR)
        cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), -1)  # 圓圈半徑 10，紅色 (BGR: 0, 0, 255)

        if 400<center_x<600 :
            print("goal")
            


        # 或者使用 drawMarker 畫出標記
        # cv2.drawMarker(frame, (center_x, center_y), (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

    else:
        print("No objects detected for class 0.")

    # 顯示帶有標記的偵測影像
    cv2.imshow('Detection Window', frame)

    # 停止條件：按 'q' 鍵退出
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# 釋放資源，關閉所有視窗
cv2.destroyAllWindows()
