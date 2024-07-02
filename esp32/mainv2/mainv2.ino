#include "mainv2.h"
#include "buzzrgb.h"

char* ssid = "dd-wrt";
char* password = "5iMLKcnkLk2MGc";
char* server_url = "http://192.168.1.102/api/recv";


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


void controller(const String& code, int slot_position){
  if (code == "0.1"){ // Code to add bicycle to holder
    rgb_set(1, 1, 1); // Set LED color to White
    success_buzzer_sound();
  } else if (code == "1.1"){ // Code to remove bicycle from holder
    rgb_set(1, 1, 1); // Set LED color to White
    success_2_buzzer_sound();
  } else{
    Serial.print("No bicycle change.\n");
    rgb_set(1, 1, 0); // Set LED color to Yellow
    error_buzzer_sound();
  }
  delay(1000); // Short delay after output message or action
}

bool sendUUID(const String& uuid, const String& ip) {
  Serial.println("Sending UUID to server...");
  Serial.print("UUID: ");
  Serial.println(uuid);
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

  if (httpResponseCode == HTTP_CODE_OK) {
    Serial.println("UUID sent successfully");
    return true;
  } 
  Serial.print("HTTP Error code: ");
  Serial.println(httpResponseCode);
  return false;
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
  init_periferals();
  SPI.begin();
  mfrc522.PCD_Init(); // Init mfcr522
  pinMode(LID_CHECK, INPUT);
  while (!Serial) {}
  
  connectToWiFi();
  Serial.println(WiFi.localIP().toString());
  rgb_set(0, 1, 0);
  emit_sound(10, 3); 
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    rgb_set(1, 0, 0);
    connectToWiFi();
  }
  // Check if lid is open
  //if (digitalRead(LID_CHECK)!=1){
    //MACHINE EMERGENCY
  //}
  else{
    rgb_set(0, 1, 0);
    String uuid = readRFID();
    if (uuid != "") {
      rgb_set(0, 1, 1);
      String ip = WiFi.localIP().toString();
      if (sendUUID(uuid, ip)) {
        delay(200); // Delay to avoid sending data too frequently
      }
      delay(20); // Delay between RFID scans
    }
  }
}
