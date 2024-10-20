import cv2
import numpy as np
from ultralytics import YOLO
from enum import Enum
import json

detection_config_path = "conf/detection.json"

with open(detection_config_path, 'r') as f:
    detection_config = json.loads(f.read())
    f.close()
    pass

source = detection_config['source_type']
if source == "camera":
    camera_id = int(detection_config[source])
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Can't access the camera: {camera_id}")
        exit()
        pass
    pass
elif source == "video":
    video_path = str(detection_config[source])
    # 1. 打開影片文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 無法打開影片文件")
        exit()
        pass

model = YOLO(detection_config['model_path'])  # 可换成 yolov8s.pt, yolov8m.pt 等

class detectObject(Enum):
    pink_chicken = 0
    yellow_chicken = 1
    goose = 2
    rooster = 3
    starling = 4

def get_frame(): # 取得當前攝影機的影像
    ret, frame = cap.read()
    if not ret:
        return 0
    return frame

def detect(frame):
    # 将 OpenCV 图像传递给 YOLOv8 模型
    results = model(frame)

    output = {0: [], 1: [], 2: [], 3: [], 4: []}

    for result in results:
        # 遍历每个检测的物体
        for box in result.boxes.data.numpy():

            x1, y1, x2, y2, score, class_id = box
            # 转换为整数 (适合绘制)
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cen_x = int((x1 + x2) / 2)
            cen_y = int((y1 + y2) / 2)
            output[class_id].append([x1, y1, x2, y2, cen_x, cen_y])
            
            # 打印物体位置
            # print(f"物件 {int(class_id)} 座標: (x1={x1}, y1={y1}), (x2={x2}, y2={y2})")

    return output