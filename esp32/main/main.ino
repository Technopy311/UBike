
//Include necessary dependencies

#include <WiFi.h>
#include <assert.h>
#include <Arduino.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN  0
#define SS_PIN 21 // GPIO 21 ESP32

// Create mfrc522 instance of MFRC522 Class
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Create wifi instance of WifiMulti Class
WiFiMulti WiFiMulti;


byte nuidPICC[4]; // Init array that will store new NUID

/*
  Function that sends a post request to the given url
*/
bool post_uuid(String url, unsigned long uuid){
  String ip; // Create ip String
  HTTPClient http; // Create instance of HTTPClient
  JSONVar dataObject; // Create json instance of JSONVar
  ip = WiFi.localIP().toString(); // Get the ip address of the module

  Serial.print("[HTTP] begin...\n");
  http.begin(url);

  dataObject["uuid"] = String(uuid); // Add the uid data to the json object
  dataObject["ip"] = ip; // Add the ip address to the json objet

  /*
  The json object currently looks as follows:

  {
    "uuid": uuid,
    "ip": ip
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
}


unsigned long getID(){
  if (! mfrc522.PICC_ReadCardSerial()){
    return 0;
  }
  unsigned long hex_num;
  hex_num = mfrc522.uid.uidByte[0] << 24;
  hex_num += mfrc522.uid.uidByte[1] << 16;
  hex_num += mfrc522.uid.uidByte[2] << 8;
  hex_num += mfrc522.uid.uidByte[3];
  mfrc522.PICC_HaltA(); // Stop reading
  return hex_num;
}



void setup() {
  Serial.begin(115200); // Begin serial monitor connection
  Serial.print("\n\n\n");

  SPI.begin();
  mfrc522.PCD_Init(); // Init mfrc522

  delay(5);
  mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details

  for(uint8_t t=4; t>0; t--){ // Wait until full boot
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(500);
  }

  WiFiMulti.addAP("equisde", "lol1234xd"); // Connect to Wifi Access Point
}


void loop() {
  while((WiFiMulti.run() == WL_CONNECTED)){

    // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
    if (mfrc522.PICC_IsNewCardPresent()){
      
      unsigned long uid = getID();
      if(uid != 0){
        bool post_status = post_uuid("http://192.168.174.193:8080/picow", uid); // Call the post_uuid function
      }
  
    }
  

  }	
  
  delay(1000); //Wait 1 second, just for development 
}
