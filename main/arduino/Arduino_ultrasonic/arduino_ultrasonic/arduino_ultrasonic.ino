#include "Arduino.h"
/* Serial port baud rate */
#define BAUDRATE     115200

/* Include definition of serial commands */
#include "commands.h"

#include "ultrasonic_ckk.h"

/* Variable initialization */

// A pair of variables to help parse serial commands
int arg = 0;
int index = 0;

// Variable to hold an input character
char chr;

// Variable to hold the current single-character command
char cmd;

// Character arrays to hold the first and second arguments
char argv1[16];
char argv2[16];

// The arguments converted to integers
long arg1;
long arg2;

// objects of ultrasonic_ckk
Ults ultra_sonic_l1(2, 3);
Ults ultra_sonic_l2(4, 5);
Ults ultra_sonic_l3(6, 7);
Ults ultra_sonic_r1(8, 9);
Ults ultra_sonic_r2(10, 11);
Ults ultra_sonic_r3(12, 13);

/* Clear the current command parameters */
void resetCommand() {
  cmd = NULL;
  memset(argv1, 0, sizeof(argv1));
  memset(argv2, 0, sizeof(argv2));
  arg1 = 0;
  arg2 = 0;
  arg = 0;
  index = 0;
}

/* Run a command.  Commands are defined in commands.h */
int runCommand() {
  arg1 = atoi(argv1);
  arg2 = atoi(argv2);
  
  switch(cmd) {
  case GET_BAUDRATE:
    Serial.println(BAUDRATE);
    break;
  case ANALOG_READ:
    Serial.println(analogRead(arg1));
    break;
  case DIGITAL_READ:
    Serial.println(digitalRead(arg1));
    break;
  case ANALOG_WRITE:
    analogWrite(arg1, arg2);
    Serial.println("OK");  
    break;
  case DIGITAL_WRITE:
    if (arg2 == 0) digitalWrite(arg1, LOW);
    else if (arg2 == 1) digitalWrite(arg1, HIGH);
    Serial.println("OK"); 
    break;
  case PIN_MODE:
    if (arg2 == 0) pinMode(arg1, INPUT);
    else if (arg2 == 1) pinMode(arg1, OUTPUT);
    Serial.println("OK");
    break;
  case ULTRA_SONIC_VALUE:
    switch (arg1){
    case L1:
        Serial.println(ultra_sonic_l1.get_val());
        break;

    case L2:
        Serial.println(ultra_sonic_l2.get_val());
        break;

    case L3:
        Serial.println(ultra_sonic_l3.get_val());
        break;

    case R1:
        Serial.println(ultra_sonic_r1.get_val());
        break;

    case R2:
        Serial.println(ultra_sonic_r2.get_val());
        break;

    case R3:
        Serial.println(ultra_sonic_r3.get_val());
        break;
    
    default:
        break;
    }
    break;

  default:
    Serial.println("Invalid Command");
    break;
  }
}

void check_connection(){
  while(1){
    if(Serial.available() > 0){
      byte recv1 = Serial.read();
      if(recv1 == byte(0xa2)){ // Get the 1-byte message from main computer
        break;
      }
    }else{
      Serial.write(byte(0xa1)); // Send the power on message (1-byte number)
      delay(50);
    }
  }
}

/* Setup function--runs once at startup. */
void setup() {
  Serial.begin(BAUDRATE);
  delay(100);
  check_connection();
}

void loop() {
  while (Serial.available() > 0) {
    
    // Read the next character
    chr = Serial.read();

    // Terminate a command with a CR
    if (chr == 13) {
      if (arg == 1) argv1[index] = NULL;
      else if (arg == 2) argv2[index] = NULL;
      runCommand();
      resetCommand();
    }
    // Use spaces to delimit parts of the command
    else if (chr == ' ') {
      // Step through the arguments
      if (arg == 0) arg = 1;
      else if (arg == 1)  {
        argv1[index] = NULL;
        arg = 2;
        index = 0;
      }
      continue;
    }
    else {
      if (arg == 0) {
        // The first arg is the single-letter command
        cmd = chr;
      }
      else if (arg == 1) {
        // Subsequent arguments can be more than one character
        argv1[index] = chr;
        index++;
      }
      else if (arg == 2) {
        argv2[index] = chr;
        index++;
      }
    }
  }
}
