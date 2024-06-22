#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  0
#define SS_PIN 21 // GPIO 21 ESP32

#define HOLDER_CAPACITY 4

#define SOLENOID_OPEN_TIME 500 // In milliseconds

const char* ssid = "FPWOM";
const char* password = "NHl7g371#0";
const char* server_url = "http://192.168.100.18:8080/api/recv";

// Associate a solenoid with a pin, this is made to make programming less prone to errors
const short int solenoid_1 = 27;
const short int solenoid_2 = 26;
const short int solenoid_3 = 25;
const short int solenoid_4 = 33;

unsigned short int solenoids[HOLDER_CAPACITY] = {solenoid_1, solenoid_2, solenoid_3, solenoid_4}; // This array holds each solenoid's pin, ORDER MATTERS


// Set the Output peripherals GPIO pin location
const int buzzer = 0;
const int red = 0;
const int green = 0;
const int blue = 0;
const int RGB[3] = {red, green, blue};

const int pss = 0; // Primary Secure System pinout

MFRC522 mfrc522(SS_PIN, RST_PIN);

int status = 0;
// Status codes:
// 0 : Machine starting
// 1 : Neutral (Empty)
// 2 : Neutral (Busy)
// -1 : Emergency Mode

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

void emit_sound(int freq, int times){ // Basic buzzer controller. freq means times per second, not sound wave frequency
  freq = 500/freq;
  for (int a = 0; a<times; a++){
    digitalWrite(buzzer, HIGH);
    delay(freq);
    digitalWrite(buzzer, LOW);
    delay(freq);
  }
}
void success_buzzer_sound(){ // Make sound a nice pleasing sound that indicates all is fine
  emit_sound(1, 1);
}

void success_2_buzzer_sound(){ // Make sound another nice pleasing sound that indicates all is fine
  emit_sound(2, 2);
}

void error_buzzer_sound(){ // Make sounde a not nice sound that indicates something is wrong
  emit_sound(4, 4);
}
void rgb_set(int R, int G, int B){ // Set the color of the RGB Led diode
  digitalWrite(RGB[0], R);
  digitalWrite(RGB[1], G);
  digitalWrite(RGB[2], B);
}

void open_solenoid(int slot_position){
  Serial.print("\tOpening slot: " + String(slot_position)+ "\n");
  digitalWrite(solenoids[slot_position], HIGH);
  delay(SOLENOID_OPEN_TIME);
  digitalWrite(solenoids[slot_position], LOW);
  Serial.print("\tSlot closed\n");
  }

void controller(const String& code, int slot_position){
  if (code == "0.1"){ // Code to add bicycle to holder
    status = 2;
    rgb_set(1, 1, 1); // Set LED color to White
    success_buzzer_sound();
    open_solenoid(slot_position);
  } else if (code == "1.1"){ // Code to remove bicycle from holder
    status = 1;
    rgb_set(1, 1, 1); // Set LED color to White
    success_2_buzzer_sound();
    open_solenoid(slot_position);
  } else{
    Serial.print("No bicycle change.\n");
    rgb_set(1, 1, 0); // Set LED color to Yellow
    error_buzzer_sound();
  }
  delay(500) // Short delay after output message or action
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
  pinMode(buzzer, OUTPUT);
  pinMode(pss, INPUT);
  while (!Serial) {}
  for(int i=0; i<HOLDER_CAPACITY; i++){
    pinMode(solenoids[i], OUTPUT); // Set every solenoid pin as OUTPUT
  }
  for(int i=0; i<3; i++){
    pinMode(RGB[i], OUTPUT); // Set every LED pin as OUTPUT
  }
  rgb_set(1, 1, 1);
  emit_sound(2, 1);
  connectToWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    rgb_set(1, 0, 0);
    connectToWiFi();
  }
  if (status == -1){
    rgb_set(1, 0, 0);
  }
  else if (status != -1){
    // Set the status LED color acording the machine status 
    if (status == 1){
      rgb_set(0, 1, 0)
    }
    else if (status == 2)
    {
      rgb_set(0, 0, 1)
    }
    if (digitalRead(pss) != HIGH){ // Enters the emergency mode in case the case lid is open
      // Send status update to server
      status = -1
    }
    else{
      String uuid = readRFID();
      if (uuid != "") {
        emit_sound(4, 1); // Short sound to notify the user that the tag has been scaned
        String ip = WiFi.localIP().toString();
        if (sendUUID(uuid, ip)) {
          delay(200); // Delay to avoid sending data too frequently
        }
      }
    }
    delay(20); // Delay between RFID scans
  }
}
