#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "i2cLcd.h"

// 設定 LCD 的 I2C 位址，通常是 0x27 或 0x3F
LiquidCrystal_I2C lcd(0x27, 16, 2);
LcdWords screen;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(115200);

  screen.set_words(0, "Hello");
  screen.set_words(1, "This is a looooong word");
  
  // 在第一行顯示文字
  // lcd.setCursor(-1, 1);
  // lcd.print("Scrolling Text");

  // 啟動自動捲動
}

void loop() {
  screen.start_service();
  screen.show(lcd);
  // 在自動捲動模式下逐字打印文字，讓文字慢慢移出螢幕
}
