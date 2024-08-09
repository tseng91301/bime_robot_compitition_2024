from ultralytics import YOLO
import cv2

# model = YOLO("yolov8n.pt")
model = YOLO("best.pt")

results = model.predict(source="0", show = True)

print(results)