在 Linux 上使用 Arduino 板時，如果拔插會導致 COM port 名稱改變，例如 `/dev/ttyUSB0` 變成 `/dev/ttyUSB1`，你可以使用以下幾種方法來**固定 port**，避免程式無法辨識的問題：

**目前使用 [使用特定usb port位置綁定](#2-使用特定-usb-port-位置來綁定)解決**

---

### 1. 使用 **符號連結 (symlink)** 固定名稱
Linux 提供 udev 來管理設備。你可以為 Arduino 設置一個固定的符號連結。

#### **步驟：**
1. **找出 Arduino 的設備資訊**  
   插上 Arduino 板，然後執行以下命令查看它的 `idVendor` 和 `idProduct`：
   ```bash
   udevadm info -a -n /dev/ttyUSB0 | grep '{idVendor}' -m 1
   udevadm info -a -n /dev/ttyUSB0 | grep '{idProduct}' -m 1
   ```
   假設輸出：
   ```
   ATTRS{idVendor}=="2341"
   ATTRS{idProduct}=="0043"
   ```

2. **創建 udev 規則文件**  
   在 `/etc/udev/rules.d/` 目錄下創建一個新的規則文件：
   ```bash
   sudo nano /etc/udev/rules.d/99-arduino.rules
   ```

3. **加入規則**  
   在文件中加入如下內容，將 `2341` 和 `0043` 替換為你的板子的 `idVendor` 和 `idProduct` 值：
   ```
   SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="arduino"
   ```

4. **重啟 udev 並插拔 Arduino**  
   執行以下命令使規則生效：
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

5. **使用新名稱連結設備**  
   插上 Arduino 板後，你應該能用 `/dev/arduino` 來存取它：
   ```bash
   ls -l /dev/arduino
   ```

---

### 2. 使用 **by-id** 方式來存取固定設備
Linux 在 `/dev/serial/by-id/` 目錄下為每個設備創建唯一的 ID 名稱，這名稱不會因重新拔插而改變。

#### **步驟：**
1. 插上 Arduino，執行：
   ```bash
   ls -l /dev/serial/by-id/
   ```
2. 你會看到類似以下的輸出：
   ```
   usb-Arduino__www.arduino.cc__0043_854343134313511011A0-if00 -> ../../ttyUSB0
   ```
3. 使用這個完整的路徑 `/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_854343134313511011A0-if00` 在程式中存取你的 Arduino。

---

### 3. 修改程式邏輯：自動偵測 Arduino
你也可以在程式中加入自動掃描 `/dev/serial/by-id/` 目錄的邏輯，這樣就不用手動設置 port。例如：

```python
import glob

def find_arduino_port():
    ports = glob.glob('/dev/serial/by-id/*Arduino*')
    if ports:
        return ports[0]
    else:
        raise Exception("Arduino port not found")

arduino_port = find_arduino_port()
print(f"Arduino connected on {arduino_port}")
```

---

### 總結
- **符號連結**：用 udev 固定成 `/dev/arduino`。
- **by-id**：使用 `/dev/serial/by-id` 內的唯一 ID 存取設備。
- **程式偵測**：程式自動掃描連接的 Arduino。  

這些方法能有效解決 Arduino 連接埠變動的問題，避免拔插後的識別錯誤。


# 序列號均相同之處理方式：
如果你發現多次插拔 Arduino 板時，`idVendor` 和 `idProduct` **都一樣**，而且埠名稱還是隨拔插變動，可能是因為你的系統無法單靠這兩個屬性唯一辨識出某個特定設備。幸運的是，還有其他方式可以精準識別每塊設備，以下幾個解法能進一步幫助你**固定特定的 Arduino 板**：

---

### **1. 使用序列號 (Serial Number)**
許多 Arduino 板（例如 Arduino Uno 或 Nano）帶有唯一的序列號。你可以透過 `udevadm` 命令找到這個序列號，並用它來建立 udev 規則。

#### **步驟：**
1. **找出序列號**  
   使用以下命令來檢查設備的詳細資訊：
   ```bash
   udevadm info -a -n /dev/ttyUSB0 | grep '{serial}' -m 1
   ```
   假設輸出：
   ```
   ATTRS{serial}=="854343134313511011A0"
   ```

2. **建立 udev 規則**  
   在 `/etc/udev/rules.d/99-arduino.rules` 中加入：
   ```
   SUBSYSTEM=="tty", ATTRS{serial}=="854343134313511011A0", SYMLINK+="arduino"
   ```

3. **重新載入規則並重啟 udev**：
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

4. **測試**  
   插上 Arduino，檢查 `/dev/arduino` 是否存在：
   ```bash
   ls -l /dev/arduino
   ```

---

### **2. 使用特定 USB Port 位置來綁定**  
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

### **3. 使用 Vendor + Serial + Port 混合匹配**  
如果單靠序列號或物理位址不夠準確，可以**混合條件**來增加規則的精確度。

#### **範例規則**：
```bash
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", ATTRS{serial}=="854343134313511011A0", SYMLINK+="arduino"
```

---

### **4. 檢查 Udev 規則是否生效**  
如果你有疑慮規則沒有正確執行，可以用以下指令來檢查：
```bash
udevadm test /sys/class/tty/ttyUSB0
```

---

### **5. Troubleshooting 小提醒**
- **權限問題**：如果你的程式無法直接讀取 `/dev/arduino`，可以加上當前使用者至 `dialout` 群組：
  ```bash
  sudo usermod -aG dialout $USER
  ```
  然後登出再登入。

- **檢查重複規則**：確保沒有其他規則檔與你設置的規則衝突。

---

### **總結**
透過使用 **序列號 (serial)** 或 **USB 連接位置**，你可以更精準地固定 Arduino 的連接名稱。如果序列號可用，這會是最可靠的方法。如果還有其他困難或細節需要調整，隨時告訴我！