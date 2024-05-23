//Include necessary dependencies/libraries


#include <WiFi.h>
#include <assert.h>
#include <Arduino.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  0
#define SS_PIN 21 // GPIO 21 ESP32

String server_url = "http://192.168.100.163:8080/api/recv";

// Create mfrc522 instance of MFRC522 Class
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Create wifi instance of WifiMulti Class

byte nuidPICC[4]; // Init array that will store new NUID

/*
  Function that sends a post request to the given url
*/
bool post_uuid(String url, String uuid, String ipaddr){
  String ip; // Create ip String
  HTTPClient http; // Create instance of HTTPClient
  JSONVar dataObject; // Create json instance of JSONVar

  Serial.print("[HTTP] begin...\n");
  http.begin(url);

  dataObject["uuid"] = String(uuid); // Add the uid data to the json object
  dataObject["ip"] = ipaddr; // Add the ip address to the json objet

  /*
  The json object currently looks as follows:

  {
    "uuid": uuid,
    "ip": ipaddr
  }
  
  */

  String jsonString = JSON.stringify(dataObject); // Cast the json object into String

  Serial.print("[HTTP] POST... \n");
  Serial.print("jsonString: ");
  Serial.print(jsonString);
  Serial.print("\n");
  http.addHeader("Content-Type", "application/json"); // Add the application/json HTTP header to the http object
  int httpResponseCode = http.POST(jsonString); // Execute the POST request and save the HTTP response code into httpResponseCode int variable
  
  Serial.print(httpResponseCode); // Print the response code
  Serial.print("\n");
  http.end();
}


String getID(){
  if (! mfrc522.PICC_ReadCardSerial()){
    return "";
  }
  unsigned long hex_num;
  hex_num = mfrc522.uid.uidByte[0] << 24;
  hex_num += mfrc522.uid.uidByte[1] << 16;
  hex_num += mfrc522.uid.uidByte[2] << 8;
  hex_num += mfrc522.uid.uidByte[3];
  mfrc522.PICC_HaltA(); // Stop reading
  return String(hex_num);
}



void setup() {
  Serial.begin(115200); // Begin serial monitor connection
  Serial.print("\n\n\n");

  SPI.begin();
  mfrc522.PCD_Init(); // Init mfrc522 rfid reader card

  delay(5);
  //mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details

  for(uint8_t t=4; t>0; t--){ // Wait until full boot
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(500);
  }
  WiFi.mode(WIFI_STA);
  WiFi.begin("FPWOM", "NHl7g371#0"); // Connect to WiFi Access Point
}


void loop() {
  Serial.print("Reading C:\n");
  while(true){
    //Serial.printf("\nStack:%d,Heap:%lu\n", uxTaskGetStackHighWaterMark(NULL), (unsigned long)ESP.getFreeHeap());

    // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
    if (mfrc522.PICC_IsNewCardPresent() && (WiFi.status() == WL_CONNECTED)){

      String uid = getID();
      if(uid != 0){
        String ipaddr = WiFi.localIP().toString();
        bool post_status = post_uuid(server_url, uid, ipaddr); // Call the post_uuid function
      }
  
    }
  }
}
