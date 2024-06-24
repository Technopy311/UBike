#include "Arduino.h"

#ifndef BUZZER_PIN
#define BUZZER_PIN 13
#endif

#ifndef RED_LED_PIN
#define RED_LED_PIN 12
#endif

#ifndef BLUE_LED_PIN
#define BLUE_LED_PIN 27
#endif

#ifndef GRN_LED_PIN
#define GRN_LED_PIN 14
#endif

// Emit sound through buzzer
// freq (times/s); times: times to repeat sound.
void emit_sound(int, int);

//Emit success sound v1
void success_buzzer_sound();

// Emit success sound v2
void success_2_buzzer_sound();

// Emit success sound v3 
void error_buzzer_sound();

// Write the rgb colours depending on
// R, G, B. 0-1024 values

void rgb_set(int, int, int); // Set the color of the RGB Led diode

void init_periferals();
