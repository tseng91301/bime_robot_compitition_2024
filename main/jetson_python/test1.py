from include import line_road
import cv2
from include import recognition

while True:
    frame = line_road.get_frame()
    lines_x, lines_y = line_road.load_frame(frame)
    print(recognition.detect())
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break