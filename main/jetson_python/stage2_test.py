from include import recognition
import cv2

while True:
    frame = recognition.get_frame()
    frame_cut2 = frame[300:480, 200:440]
    frame_detect = recognition.detect(frame_cut2, True)
    print(frame_detect)
    recognition.show_detection(frame_cut2, frame_detect)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break