import serial
import time

# 配置串口参数
ser = serial.Serial('COM20', 115200)  # 替换为你的Arduino串口端口
# 等待Arduino重启
# 接收Arduino发送的数据
while True:
    if ser.in_waiting > 0:
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

ser.close()  # 关闭串口"
