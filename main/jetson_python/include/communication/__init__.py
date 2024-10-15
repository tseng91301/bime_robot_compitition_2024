import serial
import time
import json
import os

# package_dir = os.path.dirname(__file__)
# ports_config_path = os.path.join(package_dir, "ports.json")
ports_config_path = "conf/ports.json"

# Check ports.json
with open(ports_config_path, 'r') as f:
    ports_config = json.loads(f.read())
    f.close()

ser_ults: serial.Serial
ser_motor: serial.Serial

def dump_ports_config():
    print(json.dumps(ports_config))

def poweron_init(ser):
    while True:
        if ser.in_waiting > 0:
            recv_byte = ord(ser.read())
            if(recv_byte == 0xA1):
                hex_int = 0xA3
                ser.write(hex_int.to_bytes(1, byteorder='big'))
                break

def connect():
    global ser_motor
    global ser_ults
    # 配置串口参数
    try:
        ser_motor = serial.Serial(ports_config['motor']['port'], 115200)  # 替换为你的Arduino串口端口
        poweron_init(ser_motor)
    except Exception as e:
        m_p = ports_config['motor']['port']
        print(f"Warning: Cannot connect to ser_motor ({m_p}), {str(e)}")
    try:
        ser_ults = serial.Serial(ports_config['ults']['port'], 115200)
        poweron_init(ser_ults)
    except Exception as e:
        u_p = ports_config['ults']['port']
        print(f"Warning: Cannot connect to ser_motor ({u_p}), {str(e)}")

def send(ser: serial.Serial, inp_str):
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




