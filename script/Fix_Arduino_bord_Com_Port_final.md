在 Linux 上使用 Arduino 板時，如果拔插會導致 COM port 名稱改變，例如 `/dev/ttyUSB0` 變成 `/dev/ttyUSB1`，你可以使用以下幾種方法來**固定 port**，避免程式無法辨識的問題：

---

### **使用特定 USB Port 位置來綁定**  
若你總是在相同的 USB 端口插 Arduino，可以用 **設備連接的物理位置信息** 來建立規則。

#### **步驟：**
1. **取得設備的位置信息 (devpath)**  
   使用以下命令檢查：
   ```bash
   udevadm info -a -n /dev/ttyUSB0 | grep '{devpath}' -m 1
   ```
   假設輸出：
   ```
   ATTRS{devpath}=="1-1.4"
   ```

2. **建立 udev 規則**  
   在 `/etc/udev/rules.d/99-arduino.rules` 中加入：
   ```
   SUBSYSTEM=="tty", ATTRS{devpath}=="1-1.4", SYMLINK+="arduino"
   ```

---

### **檢查 Udev 規則是否生效**  
如果你有疑慮規則沒有正確執行，可以用以下指令來檢查：
```bash
udevadm test /sys/class/tty/ttyUSB0
```

---

### **Troubleshooting 小提醒**
- **權限問題**：如果你的程式無法直接讀取 `/dev/arduino`，可以加上當前使用者至 `dialout` 群組：
  ```bash
  sudo usermod -aG dialout $USER
  ```
  然後登出再登入。

- **檢查重複規則**：確保沒有其他規則檔與你設置的規則衝突。

---

如果你已經確認 Arduino 板的**序列號 (serial number)** 不同，你可以利用這個序列號來**建立符號連結 (symlink)**，讓每次插拔後都能使用一個固定名稱。以下是詳細步驟：

### **重新載入 udev 規則並啟用**
執行以下命令，使新規則生效：
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### **測試**
插上你的 Arduino 板，檢查 `/dev/` 目錄內的符號連結：
```bash
ls -l /dev/arduino1
```
如果成功，你會看到類似以下的輸出：
```
lrwxrwxrwx 1 root root 7 Oct 22 14:22 /dev/arduino1 -> ttyUSB0
```

---

## **如何在程式中使用符號連結**
在你的程式中，無論 Arduino 插在哪個 USB 端口，都可以使用 `/dev/arduino1` 來存取它：

### **Python 範例程式**
```python
import serial

# 使用符號連結來打開串口
arduino = serial.Serial('/dev/arduino1', 9600)
print("Arduino connected!")

# 測試讀取資料
while True:
    data = arduino.readline().decode('utf-8').strip()
    print(f"Received: {data}")
```

---

## **Troubleshooting 小提醒**
- 如果 `/dev/arduino1` 無法被你的程式存取，請確保你的使用者在 `dialout` 群組中：
  ```bash
  sudo usermod -aG dialout $USER
  ```
  然後重新登出再登入。

- 使用 `udevadm test` 測試規則：
  ```bash
  udevadm test /sys/class/tty/ttyUSB0
  ```

---

### **總結**
通過這些步驟，你可以利用 Arduino 的**序列號**來創建固定的符號連結，即使重新拔插也不會影響你的程式執行。如果有多塊 Arduino 板，也可以分別為它們創建不同的符號連結，如 `/dev/arduino1` 和 `/dev/arduino2`。

### **總結**
透過使用 **序列號 (serial)** 或 **USB 連接位置**，你可以更精準地固定 Arduino 的連接名稱。如果序列號可用，這會是最可靠的方法。如果還有其他困難或細節需要調整，隨時告訴我！