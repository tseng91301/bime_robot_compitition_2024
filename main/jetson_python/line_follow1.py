from include import line_road, communication, recognition
import cv2
import threading
import json
import time

# 調適循線的PID 參數
line_follow_P = 0
line_follow_I = 0
line_follow_D = 0
LINE_FOLLOW_P_BIAS = 0.65
LINE_FOLLOW_I_BIAS = 0
LINE_FOLLOW_D_BIAS = 0

LINE_FOLLOW_BIAS_OFFSET = 0.65
LINE_FOLLOW_BIAS_DEG = 0.35

# 開啟各關卡定義文件
stage2_conf = json.loads(str(open("conf/stage2.json", 'r').read()))

communication.connect() # 連接 Arduino 板

# 關於循線服務的程式(已多線程的一個thread 呈現)
start_line_follow = True # 執行 Line follow 否則跳過
halt_line_follow = False # 立即結束 Line follow
def line_follow_service():
    global line_follow_P, line_follow_I, line_follow_D
    while True:
        if halt_line_follow:
            break
        if not start_line_follow:
            communication.motor_stop()
            continue
        else:
            frame = line_road.get_frame()
            lines_x, lines_y, line_x_slope, line_y_slope = line_road.load_frame(frame)
            x_offset, deg = line_road.calculate_direction(lines_x, line_x_slope)
            print(f"x-offset: {x_offset}, deg: {deg}, Now-step: {line_road.now_step}")

            line_follow_P_old = line_follow_P
            line_follow_P = (-1)*(x_offset * LINE_FOLLOW_BIAS_OFFSET) + ((deg-90) * LINE_FOLLOW_BIAS_DEG)
            line_follow_I += line_follow_P
            line_follow_D = line_follow_P - line_follow_P_old

            line_follow_PID = line_follow_P * LINE_FOLLOW_P_BIAS + line_follow_I * LINE_FOLLOW_I_BIAS + line_follow_D * LINE_FOLLOW_D_BIAS
            communication.motor_turn_deg(1, line_follow_PID + 90)
    pass
# 開啟循跡服務
LF_service = threading.Thread(target=line_follow_service, args=())
LF_service.start()

# 關於第二關的參數
stage_2_detect = True # 是否需要辨識小雞
stage_2_chicken_detect_times = 0 # 目前辨識到幾次小雞
stage_2_pink_chicken_detect_times = 0 # 目前辨識到幾次pink小雞
stage_2_yellow_chicken_detect_times = 0 # 目前辨識到幾次yellow小雞
try:
    while True:
        if line_road.now_step == 2 and stage_2_detect:
            # 獲取 detection 鏡頭畫面並裁減
            frame = recognition.get_frame()
            frame_cut2 = frame[300:480, 240:400]
            frame_detect = recognition.detect(frame_cut2, True)

            # 判斷是否看到小雞
            if frame_detect[recognition.detectObject.pink_chicken] or frame_detect[recognition.detectObject.yellow_chicken]:
                stage_2_chicken_detect_times += 1
                print(f"Detected {stage_2_chicken_detect_times} times small chick.")
                if frame_detect[recognition.detectObject.pink_chicken]:
                    stage_2_pink_chicken_detect_times += 1
                elif frame_detect[recognition.detectObject.yellow_chicken]:
                    stage_2_yellow_chicken_detect_times += 1
            # 判斷是否正確看到小雞，並判斷其顏色，做出決定
            if stage_2_chicken_detect_times >= stage2_conf["chicken_detect_valid_times"]:
                start_line_follow = False
                print("Detected chicken, stopping")
                if stage_2_yellow_chicken_detect_times >= stage2_conf["chicken_detect_valid_times"]:
                    print("Detected yellow chicken")
                elif stage_2_pink_chicken_detect_times >= stage2_conf["chicken_detect_valid_times"]:
                    print("Detected pink chicken")
                time.sleep(3)
                start_line_follow = True
                
        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Aborted!")
    start_line_follow = False
    halt_line_follow = True
    communication.motor_stop()