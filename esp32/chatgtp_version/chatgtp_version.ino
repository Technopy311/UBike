#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  0
#define SS_PIN 21 // GPIO 21 ESP32

#define HOLDER_CAPACITY 5

#define SOLENOID_OPEN_TIME 500 // In milliseconds

const char* ssid = "FPWOM";
const char* password = "NHl7g371#0";
const char* server_url = "http://192.168.100.163:8080/api/recv";

// Associate a solenoid with a pin, this is made to make programming less prone to errors
const short int solenoid_1 = 12;
const short int solenoid_2 = 13;
const short int solenoid_3 = 14;
const short int solenoid_4 = 15;
const short int solenoid_5 = 16;

unsigned short int solenoids[HOLDER_CAPACITY] = {solenoid_1, solenoid_2, solenoid_3, solenoid_4, solenoid_5}; // This array holds each solenoid's pin, ORDER MATTERS

MFRC522 mfrc522(SS_PIN, RST_PIN);

bool connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 10) {
    delay(750);
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

void success_buzzer_sound(){ // Make sound a nice pleasing sound that indicates all is fine
}

void success_2_buzzer_sound(){ // Make sound another nice pleasing sound that indicates all is fine
}

void error_buzzer_sound(){ // Make sounde a not nice sound that indicates something is wrong
}

void open_solenoid(int slot_position){
  Serial.print("\tOpening slot: " + String(slot_position)+ "\n");
  digitalWrite(solenoids[slot_position], HIGH);
  delay(SOLENOID_OPEN_TIME); // Open solenoide for 5 seconds
  digitalWrite(solenoids[slot_position], LOW);
  Serial.print("\tSlot closed\n");
}

void controller(const String& code, int slot_position){
  if (code == "0.1"){ // Code to add bicycle to holder
    success_buzzer_sound();
    open_solenoid(slot_position);
  } else if (code == "1.1"){ // Code to remove bicycle from holder
    success_2_buzzer_sound();
    open_solenoid(slot_position);
  } else{
    error_buzzer_sound();
    Serial.print("No bicycle change.");
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
  String response_data = http.getString();
  http.end();

  JSONVar response_data_json = JSON.parse(response_data);

  controller(response_data_json["code"], response_data_json["slot_to_open"]);

  Serial.print("Response data:\n\t");
  Serial.print(response_data + "\n\n");

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
  for(int i=0; i<HOLDER_CAPACITY; i++){
    pinMode(solenoids[i], OUTPUT); // Set every solenoid pin as OUTPUT
  }
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
      delay(200); // Delay to avoid sending data too frequently
    }
  }
  delay(20); // Delay between RFID scans
}
