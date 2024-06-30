#include "buzzrgb.h"

const int RGBpin [3] = {RED_LED_PIN, GRN_LED_PIN, BLUE_LED_PIN};

void emit_sound(int freq, int times){ // Basic buzzer controller. freq means times per second, not sound wave frequency
  freq = 800/freq;
  for (int a = 0; a<times; a++){
    digitalWrite(BUZZER_PIN, 1);
    delay(freq);
    digitalWrite(BUZZER_PIN, 0);
    delay(freq);
  }
}

void success_buzzer_sound(){ // Make sound a nice pleasing sound that indicates all is fine
  emit_sound(6, 3);
}

void success_2_buzzer_sound(){ // Make sound another nice pleasing sound that indicates all is fine
  emit_sound(4, 2);
}

void error_buzzer_sound(){ // Make sounde a not nice sound that indicates something is wrong
  emit_sound(3, 4);
}
void rgb_set(int R, int G, int B){ // Set the color of the RGB Led diode
  digitalWrite(RGBpin[0], R);
  digitalWrite(RGBpin[1], G);
  digitalWrite(RGBpin[2], B);
}

void init_periferals(){
  for(int i=0; i<3; i++){
    pinMode(RGBpin[i], OUTPUT); // Set every LED pin as OUTPUT
  }
  
  rgb_set(1, 1, 1);
  emit_sound(2, 1);
}
