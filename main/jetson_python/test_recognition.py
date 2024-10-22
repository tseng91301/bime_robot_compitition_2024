from include import recognition

while True:
    frame = recognition.get_frame()
    frame_detect = recognition.detect(frame)
    print(frame_detect)