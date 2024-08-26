import serial
import time
import json
import os

package_dir = os.path.dirname(__file__)
ports_config_path = os.path.join(package_dir, "ports.json")

# Check ports.json
with open(ports_config_path, 'r') as f:
    ports_config = json.loads(f.read())

ser_ults: serial.Serial
ser_motor: serial.Serial
def connect():
    global ser_motor
    global ser_ults
    # 配置串口参数
    try:
        ser_motor = serial.Serial(ports_config['motor']['port'], 115200)  # 替换为你的Arduino串口端口
    except Exception as e:
        m_p = ports_config['motor']['port']
        print(f"Warning: Cannot connect to ser_motor ({m_p}), {str(e)}")
    try:
        ser_ults = serial.Serial(ports_config['ults']['port'], 115200)
    except Exception as e:
        u_p = ports_config['ults']['port']
        print(f"Warning: Cannot connect to ser_motor ({u_p}), {str(e)}")

def send(ser: serial.Serial, inp_str):
    ser.write(bytes(inp_str))
    return

def wait_readln(ser: serial.Serial):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            return str(line)

def read_ult():
    send(ser_ults, "u")
    return int(wait_readln())
