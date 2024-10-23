import cv2
import numpy as np
from ultralytics import YOLO
from enum import Enum
import json
import threading
import time

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
        print(f"Can't access the camera: {camera_id}")
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
service_frame = None

finish_recognition = True
detect_output = {0: [], 1: [], 2: [], 3: [], 4: []}

class detectObject(Enum):
    pink_chicken = 0
    yellow_chicken = 1
    goose = 2
    rooster = 3
    starling = 4

def get_frame(): # 取得當前攝影機的影像
    global service_frame
    ret, frame = cap.read()
    if not ret:
        return 0
    service_frame = frame
    return frame

def detect(frame):
    global finish_recognition
    if not finish_recognition:
        return
    finish_recognition = False
    # 将 OpenCV 图像传递给 YOLOv8 模型
    results = model(frame)
    time.sleep(0.99)
    global detect_output

    detect_output = {0: [], 1: [], 2: [], 3: [], 4: []}

    for result in results:
        # 遍历每个检测的物体
        for box in result.boxes.data.cpu().numpy():

            x1, y1, x2, y2, score, class_id = box
            # 转换为整数 (适合绘制)
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cen_x = int((x1 + x2) / 2)
            cen_y = int((y1 + y2) / 2)
            detect_output[class_id].append([x1, y1, x2, y2, cen_x, cen_y])
            
            # 打印物体位置
            # print(f"物件 {int(class_id)} 座標: (x1={x1}, y1={y1}), (x2={x2}, y2={y2})")
    finish_recognition = True

    return

def detect_service_func():
    while True:
        try:
            if service_frame == None:
                continue
        except:
            pass
        detect(service_frame)

def start_detect_service():
    detect_service = threading.Thread(target=detect_service_func, args=())
    detect_service.start()