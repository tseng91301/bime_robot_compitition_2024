from include import line_road
import cv2

cv2.namedWindow("show frame")
video_width = line_road.VIDEO_OUT_SIZE_X
video_height = line_road.VIDEO_OUT_SIZE_Y
v_detect_range = line_road.LINE_FOLLOWING_VERTICAL_DETECT_RANGE
print(v_detect_range)
while True:
    lines, frame = line_road.load_frame(return_frame=True)
    cv2.line(frame, (int(video_width/2) + 1, 0), (int(video_width/2) + 1, video_height - 1), (255, 255, 0), 2)
    if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("show frame", frame)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break