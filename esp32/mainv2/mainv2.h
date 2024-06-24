#include "Arduino.h"
#include "WiFi.h"
#include "HTTPClient.h"
#include "Arduino_JSON.h"
#include "SPI.h"
#include "MFRC522.h"
#include "buzzrgb.h"


#ifndef RST_PIN
#define RST_PIN 0
#endif

#ifndef SS_PIN
#define SS_PIN 21 // GPIO 21 ESP32
#endif

#ifndef HOLDER_CAPACITY
#define HOLDER_CAPACITY 1
#endif

#ifndef SOLENOID_OPEN_TIME
#define SOLENOID_OPEN_TIME 500 // in ms
#endif

#ifndef LID_CHECK
#define LID_CHECK 33 // GPIO 33 ESP32
#endif


// Connect to Wifi
// Returns True if connected, else, false.
bool connectToWifi();

// Depeding on status_code, it opens or not a slot
// and calls other functions to emit or not sound/light.
void controller(const String&, int);

// Sends the given uuid through http, to the set server_url variable
bool sendUUID(const String&, const String&);


// Reads the RFID data if card/keychain is pressent, 
// returns the uuid of the scanned element.
String readRFID();
