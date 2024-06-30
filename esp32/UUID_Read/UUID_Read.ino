#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  0
#define SS_PIN 21 // GPIO 21 ESP32


MFRC522 mfrc522(SS_PIN, RST_PIN);

String readRFID() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return "";
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return "";
  }
  String uuid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uuid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    uuid += String(mfrc522.uid.uidByte[i], HEX);
  }
  mfrc522.PICC_HaltA();
  return uuid;
}

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  String uuid = readRFID();
  if (uuid != "") {
    Serial.println(uuid);
    delay(200); // Delay to avoid sending data too frequently
  }
  delay(20); // Delay between RFID scans
}
