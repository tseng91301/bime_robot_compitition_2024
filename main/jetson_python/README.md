# 機器人主程式
## 一、configuration 文件介紹
這是機器人Jetson nano程式的配置文件，裡面記錄著各項調適參數，藉由修改他們，可以改變機器人的運作方式，不需要去修改主程式或其他套件程式。
* configuration 文件都會放在主程式資料夾中的conf/ 目錄中
### 簡述: 
1. ports.json: 記錄每一個Arduino板的連接序列埠(COM port)
2. line_road.json: 紀錄關於路徑規劃(影像辨識賽道)的影像辨識相關參數

## 二、設定 configuration 文件
#### 相關設定範例都呈現在標準配置文件內
*line_road.json:*
* red_line:
    以下8個數值分別代表可以被算做紅線的範圍(以hsv色域來定義)，h 從0 到 180、s 和 v 都是 0 到 255
* source_type: 要使用哪一種影像資料媒介，支援影片(video)、存取攝影機(camera)
* "camera", "video": 分別要填入攝影機的位置(通常是0)以及影片的位置
* resolution: x, y 分別代表影像轉換的長寬(會先進行轉換在運算或辨識)
* preview: 是否要進行影像預覽(1: 是, 0: 否)
* vertical_line_detect_range: 指的是要以多少範圍內的影像作為辨識垂直線的範圍(從中間擴展到兩側，比例最大為1(全部))
* horizontal_line_detect_y_bottom: 辨識橫線區域在的起始y座標
* horizontal_line_detect_range: 辨識橫線區域從底部往上數的範圍(佔全螢幕高度的比例)
* min_valid_horizontal_line_detect_times: 辨識幾次有橫線才算是到下一關(去雜訊用途)
* another_horizontal_line_detect_interval: 在辨識是否到下一關時，最小需要經過沒有橫線的次數(避免在不停辨識到橫線時突然有一張沒有，接著如果又有橫線關卡又再 +1)
* vertical_line_degree: 辨識垂直線的角度範圍(Deg)(向左或向右個幾度)
* horizontal_line_degree: 辨識水平線的角度範圍(Deg)(向上或向下幾度)

*goose_weight.json:*
* color_range: 以下數值陣列是記錄各種顏色的讀取範圍 [H, S, V]
* detect_range: 紀錄偵測範圍的x, y起始點以及長寬範圍
* preview: 紀錄是否產生一個預覽視窗
* preview_window_name: 紀錄預覽視窗的名字