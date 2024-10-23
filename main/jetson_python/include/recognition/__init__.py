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
    cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
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

detect_items: list = detection_config["items"]

def get_frame(): # 取得當前攝影機的影像
    global service_frame
    ret, frame = cap.read()
    if not ret:
        return 0
    service_frame = frame
    return frame

def detect(frame, ret=False):
    global finish_recognition
    if not finish_recognition:
        return
    finish_recognition = False
    # 将 OpenCV 图像传递给 YOLOv8 模型
    print("start model")
    results = model(frame)
    print("finish model")
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
            detect_output[class_id].append([x1, y1, x2, y2, cen_x, cen_y, score])
            
            # 打印物体位置
            # print(f"物件 {int(class_id)} 座標: (x1={x1}, y1={y1}), (x2={x2}, y2={y2})")
    finish_recognition = True

    if ret:
        return detect_output
    else:
        return
    
def show_detection(frame: np.ndarray, data: dict):
    # 在影像上繪製檢測框並回傳中心座標
    show_frame = frame.copy()
    for key, values in data.items():
        if values:
            for value in values:
                x1, y1, x2, y2, cen_x, cen_y, score = value
                if(score >= 0.5):
                    # 繪製矩形和標籤
                    cv2.rectangle(show_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(show_frame, detect_items[int(key)], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    # 繪製中心點
                    cv2.circle(show_frame, (cen_x, cen_y), 5, (0, 255, 0), -1)
    cv2.imshow("show_detection", show_frame)

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