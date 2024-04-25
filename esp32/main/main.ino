
#Include necessary dependencies

#include <WiFi.h>
#include <assert.h>
#include <Arduino.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

// Create wifi instance of WifiMulti Class

WiFiMulti WiFiMulti;

/*
  Function that sends a post request to the given url
*/
bool post_uuid(String url){
  String ip; // Create ip String
  HTTPClient http; // Create instance of HTTPClient
  JSONVar dataObject; // Create json instance of JSONVar
  
  int uuid = 123456; // UUID variable - Just to test by now
  ip = WiFi.localIP().toString(); // Get the ip address of the module

  Serial.print("[HTTP] begin...\n");
  http.begin(url);

  dataObject["uuid"] = uuid; // Add the uuid data to the json object
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



void setup() {
  Serial.begin(115200); // Begin serial monitor connection
  Serial.println();
  Serial.println();
  Serial.println();

  for(uint8_t t=4; t>0; t--){ // Wait until full boot
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(500);
  }

  WiFiMulti.addAP("equisde", "lol1234xd"); // Connect to Wifi Access Point
}


void loop() {
  if((WiFiMulti.run() == WL_CONNECTED)){
    bool post_status = post_uuid("http://192.168.174.193:8080/picow"); // Call the post_uuid function
  }
  delay(10000); //Wait 10 seconds, just for development 
}
