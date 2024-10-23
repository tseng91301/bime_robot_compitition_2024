from include import recognition

recognition.start_detect_service()
while True:
    frame = recognition.get_frame()
    if recognition.finish_recognition:
        frame_detect = recognition.detect_output
        print(frame_detect)