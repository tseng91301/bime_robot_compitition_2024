import serial
import threading
import time
import json
import os
import numpy as np

# package_dir = os.path.dirname(__file__)
# ports_config_path = os.path.join(package_dir, "ports.json")
ports_config_path = "conf/ports.json"

# Check ports.json
with open(ports_config_path, 'r') as f:
    ports_config = json.loads(f.read())
    f.close()

ser_ults: serial.Serial
ser_motor: serial.Serial
ser_ults_connected = 0
ser_motor_connected = 0

ULT_NUM = ports_config["ults"]["ult_num"]
ults_value = [100] * ULT_NUM

LSPD = ports_config["motor"]["calibration"]["lspd"]
RSPD = ports_config["motor"]["calibration"]["rspd"]
MAX_SPEED = ports_config["motor"]["max_speed"]

def dump_ports_config():
    print(json.dumps(ports_config))

def poweron_init(ser: serial.Serial):
    while True:
        if ser.in_waiting > 0:
            recv_byte = ord(ser.read())
            if(recv_byte == 0xA1):
                hex_int = 0xA3
                ser.write(hex_int.to_bytes(1, byteorder='big'))
                break

def connect():
    global ser_motor, ser_ults, ser_ults_connected, ser_motor_connected
    # 配置串口参数
    try:
        ser_motor = serial.Serial(ports_config['motor']['port'], 115200)  # 替换为你的Arduino串口端口
        poweron_init(ser_motor)
        ser_motor_connected = 1
    except Exception as e:
        m_p = ports_config['motor']['port']
        print(f"Warning: Cannot connect to ser_motor ({m_p}), {str(e)}")
        pass
    try:
        ser_ults = serial.Serial(ports_config['ults']['port'], 115200)
        poweron_init(ser_ults)
        ser_ults_connected = 1
    except Exception as e:
        u_p = ports_config['ults']['port']
        print(f"Warning: Cannot connect to ser_motor ({u_p}), {str(e)}")

def send(ser: serial.Serial, inp_str: str):
    inp_str += "\r"
    ser.write(bytes(inp_str.encode('utf-8')))
    return

def wait_readln(ser: serial.Serial):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            return str(line)

def read_ult(dev_num: int):
    global ser_ults
    send(ser_ults, f"u {dev_num}")
    return float(wait_readln(ser_ults))

# 讀取每一個 Ultrasonic 訊號並放到陣列中
def read_all_ult():
    print("Start reading ultrasonic sensor")
    global ults_value
    while True:
        if ser_ults_connected != 1:
            continue
        for i in range(ULT_NUM):
            try:
                ults_value[i] = read_ult(i)
            except Exception as e:
                print(f"Read ults error: {str(e)}")
        time.sleep(0.1)
    pass

def start_ult_service():
    # 開啟一個獨立用於讀取 Ultrasonic 訊號的線程
    read_all_ult_service = threading.Thread(target=read_all_ult, args=())
    read_all_ult_service.start()

# 使雙馬達轉動的程式
def motor_turn_raw(spdL: int, spdR: int):
    send(ser_motor, f"o {spdL} {spdR}")
    return

def motor_turn_deg(spd: float, deg: float):
    if deg <= 90: # 要往右邊
        spdL, spdR = 1, np.sin(np.radians(deg))
        pass
    else:
        spdL, spdR = np.sin(np.radians(deg)), 1
    spdL *= spd * MAX_SPEED * LSPD
    spdR *= spd * MAX_SPEED * RSPD
    motor_turn_raw(int(spdL), int(spdR))
    return

def motor_stop():
    motor_turn_raw(0, 0)
    return

def motor_back():
    motor_stop()
    time.sleep(0.5)
    motor_turn_raw(int(-1 * MAX_SPEED * LSPD), int(-1 * MAX_SPEED * RSPD))