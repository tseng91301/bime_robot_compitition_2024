import serial
import time
import json
import os

package_dir = os.path.dirname(__file__)
ports_config_path = os.path.join(package_dir, "ports.json")

# Check ports.json
with open(ports_config_path, 'r') as f:
    ports_config = json.loads(f.read())

ser_ults
ser_motor
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


# 等待Arduino重启
# 接收Arduino发送的数据
while True:
    if ser_motor.in_waiting > 0:
        recv_byte = ord(ser.read())
        if(recv_byte == 0xA1):
            hex_int = 0xA3
            ser.write(hex_int.to_bytes(1, byteorder='big'))
            break

print("Arduino on")

# 向Arduino发送数据
str_out = b"o 100 100\r"
ser.write(str_out)  # 发送一个字节数据到Arduino

time.sleep(1)
ser.write(b"o 0 0\r")

print("tr-end")

# 接收Arduino发送的数据
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Received from Arduino: {line}")
        break

ser.close()  # 关闭串口