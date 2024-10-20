from include import goose_weight, recognition, line_road
import cv2

while True:
    frame = recognition.get_frame()
    color = goose_weight.color_block_detect(frame)
    print(f"Color: {color}")

    if cv2.waitKey(33) & 0xFF == ord('q'):
        break
