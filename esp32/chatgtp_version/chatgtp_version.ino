#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  0
#define SS_PIN 21 // GPIO 21 ESP32

const char* ssid = "FPWOM";
const char* password = "NHl7g371#0";
const char* server_url = "http://192.168.100.163:8080/api/recv";

MFRC522 mfrc522(SS_PIN, RST_PIN);

bool connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 5) {
    delay(1000);
    Serial.println("Retrying...");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connected");
    return true;
  } else {
    Serial.println("Failed to connect to WiFi");
    return false;
  }
}

bool sendUUID(const String& uuid, const String& ip) {
  Serial.println("Sending UUID to server...");
  JSONVar dataObject;
  dataObject["uuid"] = uuid;
  dataObject["ip"] = ip;
  String jsonString = JSON.stringify(dataObject);
  HTTPClient http;
  http.begin(server_url);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);
  http.end();
  if (httpResponseCode == HTTP_CODE_OK) {
    Serial.println("UUID sent successfully");
    return true;
  } else {
    Serial.print("Failed to send UUID. Error code: ");
    Serial.println(httpResponseCode);
    return false;
  }
}

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
  while (!Serial) {}
  connectToWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }
  String uuid = readRFID();
  if (uuid != "") {
    String ip = WiFi.localIP().toString();
    if (sendUUID(uuid, ip)) {
      delay(250); // Delay to avoid sending data too frequently
    }
  }
  delay(20); // Delay between RFID scans
}
