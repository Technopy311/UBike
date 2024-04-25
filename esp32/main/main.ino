#include <assert.h>
#include <WiFi.h>
#include <Arduino.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>


WiFiMulti WiFiMulti;


bool post_uuid(String url){
  String ip;
  HTTPClient http;
  JSONVar dataObject;
  
  int uuid = 123456; // Just to test by now
  ip = WiFi.localIP().toString();

  Serial.print("[HTTP] begin...\n");
  http.begin(url);


  dataObject["uuid"] = uuid;
  dataObject["ip"] = ip;

  String jsonString = JSON.stringify(dataObject);

  Serial.print("[HTTP] POST... \n");
  Serial.print("jsonString: ");
  Serial.print(jsonString);
  Serial.print("\n");
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);
  
  Serial.print(httpResponseCode);
  Serial.print("\n");
}



void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println();
  Serial.println();

  for(uint8_t t=4; t>0; t--){
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFiMulti.addAP("equisde", "lol1234xd");
}


void loop() {
  if((WiFiMulti.run() == WL_CONNECTED)){
    bool post_status = post_uuid("http://192.168.174.193:8080/picow");
  }
  delay(10000);
}
