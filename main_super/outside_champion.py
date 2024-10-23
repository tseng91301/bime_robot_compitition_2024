import time
from include import communication

def process_sensor_data():
    # 取得六顆超音波感測器的數據
    ult_left_front = communication.ults_value[0]    # 左前方
    ult_right_front = communication.ults_value[3]   # 右前方
    ult_left_side = communication.ults_value[2]     # 左側
    ult_right_side = communication.ults_value[5]    # 右側
    ult_front_left = communication.ults_value[1]    # 正前方左
    ult_front_right = communication.ults_value[4]   # 正前方右

    # 判斷前方的障礙物
    front_obstacle = (ult_front_left < 30 or ult_front_right < 30)

    # 根據左右兩側距離決定行進方向
    if front_obstacle:
        # 如果前方有障礙物，後退或轉向
        communication.motor_back()  # 可以修改這裡的邏輯，例如轉向
        time.sleep(0.5)
    elif ult_left_side < ult_right_side:
        # 左邊距離太近，向右轉
        communication.motor_turn_deg(0.5, 120)  # 半速向右轉
    elif ult_right_side < ult_left_side:
        # 右邊距離太近，向左轉
        communication.motor_turn_deg(0.5, 60)  # 半速向左轉
    else:
        # 兩側距離相當，向前直行
        communication.motor_turn_raw(100, 100)  # 全速直行

def main():
    # 初始化與連接
    communication.connect()
    communication.start_ult_service()
    
    # 持續進行超音波感測器回饋與馬達控制
    while True:
        if communication.ser_ults_connected and communication.ser_motor_connected:
            # 根據感測器的數據進行處理
            process_sensor_data()
        time.sleep(0.1)  # 稍微延遲以避免過度處理

if __name__ == "__main__":
    main()
