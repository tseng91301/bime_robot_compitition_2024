import cv2
from ultralytics import YOLO

# 加載模型
model = YOLO(r"C:\Users\user\Desktop\123456789\bime_robot_compitition_2024\sr5\best.pt")

# 載入自定義資料集設定
dataset_yaml = r"C:\Users\user\Desktop\datasets\datasets\coco128\coco128_custom.yaml"

# 使用 OpenCV 打開攝像頭
cap = cv2.VideoCapture(0)  # 0 代表第一個攝像頭

while True:
    # 讀取一幀影像
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break

    # 獲取影像大小
    height, width, channels = frame.shape
    
    # 等比例縮放影像
    frame_resized = cv2.resize(frame, (600, int(600 / width * height)))

    # 將影像轉換為 RGB 格式（YOLO 使用的是 RGB 格式）
    image_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # 預測影像
    results = model.predict(source=image_rgb, data=dataset_yaml)

    # 在影像上繪製檢測框並回傳中心座標
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # 取得邊界框座標
            confidence = box.conf[0]  # 取得信心分數
            class_id = int(box.cls[0])  # 取得類別 ID
            label = f'{model.names[class_id]}: {confidence:.2f}'  # 標籤
            
            # 計算中心點
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            print(f"物體 {model.names[class_id]} 的中心座標: ({center_x:.2f}, {center_y:.2f})")

            # 繪製矩形和標籤
            cv2.rectangle(frame_resized, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(frame_resized, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            # 繪製中心點
            cv2.circle(frame_resized, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)

    # 顯示影像
    cv2.imshow('Detected Image', frame_resized)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()  # 關閉所有視窗
