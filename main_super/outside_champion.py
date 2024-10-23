import time
from include import communication

SAFE_DISTANCE_FRONT = 50  # 前方感測器認為安全的距離（單位：公分）
BACK_DURATION = 0.5  # 後退持續時間

def process_sensor_data():
    # 取得六顆超音波感測器的數據
    ult_left_front = communication.ults_value[0]    # 左前方
    ult_front_left = communication.ults_value[1]    # 正前方左
    ult_left_rear = communication.ults_value[2]     # 左後方
    ult_right_front = communication.ults_value[3]   # 右前方
    ult_front_right = communication.ults_value[4]   # 正前方右
    ult_right_rear = communication.ults_value[5]    # 右後方

    # 計算前方的距離（平均左右正前方的數值）
    avg_front_distance = (ult_front_left + ult_front_right) / 2

    if avg_front_distance < SAFE_DISTANCE_FRONT:
        # 前方有障礙物，後退並向後移動
        print("Front obstacle detected, backing up...")
        communication.motor_back()  # 後退
        time.sleep(BACK_DURATION)
    else:
        # 沒有前方障礙物，選擇左右側較遠的方向
        print("No front obstacle, checking sides...")
        avg_left_distance = (ult_left_front) / 2  # 左側距離
        avg_right_distance = (ult_right_front) / 2  # 右側距離

        if avg_left_distance > avg_right_distance:
            print("Left side is clearer, moving left...")
            communication.motor_turn_deg(0.6, 35)  # 向左轉
        else:
            print("Right side is clearer, moving right...")
            communication.motor_turn_deg(0.6, 165)  # 向右轉

def main():
    # 初始化與連接
    communication.connect()
    communication.start_ult_service()
    
    try:
        # 持續進行超音波感測器回饋與馬達控制
        while True:
            if communication.ser_ults_connected and communication.ser_motor_connected:
                # 根據感測器的數據進行處理
                process_sensor_data()
            time.sleep(0.1)  # 稍微延遲以避免過度處理
    except KeyboardInterrupt:
        # 捕捉 Ctrl+C 並停止馬達
        print("Program interrupted. Stopping motors...")
        communication.motor_stop()  # 停止馬達

if __name__ == "__main__":
    main()
