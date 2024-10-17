import cv2
from ultralytics import YOLO

# 加載模型
model = YOLO(r"C:\Users\user\Desktop\datasets\best.pt")

# 載入自定義資料集設定
dataset_yaml = r"C:\Users\user\Desktop\datasets\datasets\coco128\coco128_custom.yaml"

# 使用 OpenCV 讀取影像
image_path = r"C:\Users\user\Desktop\datasets\datasets\coco128\images\train\chicken_starling_goose_1.jpg"  # 替換為你的影像路徑
image = cv2.imread(image_path)
# 獲取影像大小
height, width, channels = image.shape  # channels 代表顏色通道數，通常是 3（RGB）
image = cv2.resize(image, (600, int(600/width*height)))

# 將影像轉換為 RGB 格式（YOLO 使用的是 RGB 格式）
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 預測影像
results = model.predict(source=image_rgb, data=dataset_yaml)

# 在影像上繪製檢測框
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]  # 取得邊界框座標
        confidence = box.conf[0]  # 取得信心分數
        class_id = int(box.cls[0])  # 取得類別 ID
        label = f'{model.names[class_id]}: {confidence:.2f}'  # 繪製標籤

        # 繪製矩形和標籤
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 顯示影像
cv2.imshow('Detected Image', image)
cv2.waitKey(0)  # 等待任意鍵按下
cv2.destroyAllWindows()  # 關閉所有視窗
