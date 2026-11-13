/*
  SI 673 - OLED test for the XIAO Expansion Base.
  No camera, WiFi, or cloud. Open Serial Monitor at 115200 baud.
*/

#include <Arduino.h>
#include <Wire.h>
#include <U8x8lib.h>

U8X8_SSD1306_128X64_NONAME_HW_I2C oled(U8X8_PIN_NONE);

void scanBus() {
  Serial.print("[I2C] Devices found:");
  int count = 0;
  for (uint8_t address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    if (Wire.endTransmission() == 0) {
      Serial.printf(" 0x%02X", address);
      count++;
    }
  }
  Serial.println(count == 0 ? " NONE" : "");
}

void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.printf("\n[I2C] SDA=GPIO%d SCL=GPIO%d\n", SDA, SCL);

  Wire.begin(SDA, SCL);
  scanBus();

  oled.begin();
  oled.setPowerSave(0);
  oled.setFont(u8x8_font_chroma48medium8_r);
  oled.clearDisplay();
  oled.drawString(0, 0, "OLED test OK");
  oled.drawString(0, 2, "SI 673");
  Serial.println("[OLED] Text drawn");
}

void loop() {
  static int counter = 0;
  char line[17];
  snprintf(line, sizeof(line), "Count: %-8d", counter++);
  oled.drawString(0, 4, line);

  // Blink the whole screen every 2 s so even a dim panel is noticeable.
  oled.setInverseFont(counter % 2);
  oled.drawString(0, 6, "################");
  oled.setInverseFont(0);

  delay(1000);
}
