
#define USE_BASE      // Enable the base controller code
//#undef USE_BASE     // Disable the base controller code

/* Define the motor controller and encoder library you are using */
#ifdef USE_BASE
   /* L298 Motor driver */
   #define L298_MOTOR_DRIVER
#endif

//#define USE_SERVOS  // Enable use of PWM servos as defined in servos.h
#undef USE_SERVOS     // Disable use of PWM servos

/* Serial port baud rate */
#define BAUDRATE     115200

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

/* Include definition of serial commands */
#include "commands.h"

/* Sensor functions */
#include "sensors.h"

/* Include servo support if required */
#ifdef USE_SERVOS
   #include <Servo.h>
   #include "servos.h"
#endif

#ifdef USE_BASE
  /* Motor driver function definitions */
  #include "motor_driver.h"

  /* Stop the robot if it hasn't received a movement command
   in this number of milliseconds */
  #define AUTO_STOP_INTERVAL 2000
  long lastMotorCommand = AUTO_STOP_INTERVAL;
#endif

#include "ultrasonic_ckk.h"

#define ULTRASONIC_SENSOR_NUM 6
const int ULTRASONIC_SENSOR_PINS[ULTRASONIC_SENSOR_NUM][2] = { // This will be changed to [ULTRASONIC_SENSOR_NUM][2] after complete building
  {34, 35},
  {36, 37},
  {38, 39},
  {40, 41},
  {10, 11},
  {12, 13}
};

#include "stepper_motor.h"
#include "i2cLcd.h"
LiquidCrystal_I2C lcd(0x27, 16, 2);
LcdWords screen;

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

// the object of ultrasonic_ckk
Ults ultra_sonic_arr[ULTRASONIC_SENSOR_NUM];

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
    Serial.println(ultra_sonic_arr[arg1].get_val());
    break;
  case SCREEN:
    screen.set_words(0, argv1);
    screen.set_words(1, argv2);
    break;
  case GOOSE:
    if(arg1 == 1){
      analogWrite(13, 50);
      analogWrite(12, 0);
      delay(arg2);
      analogWrite(13, 0);
      analogWrite(12, 0);
    }
    else if(arg1 == 0){
      analogWrite(12, 50);
      analogWrite(13, 0);
      delay(arg2);
      analogWrite(12, 0);
      analogWrite(13, 0);

    }
    break;
  case WEIGHT_CALIBRATE:
    hx711_calibrate();
    break;
  case WEIGHT_CALIBRATE_VAL_INPUT:
    

#ifdef USE_BASE
  case MOTOR_RAW_PWM:
    /* Reset the auto stop timer */
    lastMotorCommand = millis();
    setMotorSpeeds(arg1, arg2);
    Serial.println("OK"); 
    break;
#endif
  default:
    Serial.println("Invalid Command");
    break;
  }
}

void init_ults(){
  for(int a=0; a<ULTRASONIC_SENSOR_NUM; a++){
    ultra_sonic_arr[a].init(ULTRASONIC_SENSOR_PINS[a][0], ULTRASONIC_SENSOR_PINS[a][1]);
  }
}

void check_connection(){
  while(1){
    if(Serial.available() > 0){
      byte recv1 = Serial.read();
      if(recv1 == byte(0xa3)){ // Get the 1-byte message from main computer
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
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, 0);
  digitalWrite(13, 0);
  Serial.begin(BAUDRATE);
  delay(100);
  check_connection();
  
  init_ults();

  hx711_init();

  lcd.init();
  lcd.backlight();

/* Initialize the motor controller if used */
#ifdef USE_BASE
  initMotorController();
#endif

/* Attach servos if used */
#ifdef USE_SERVOS
  int i;
  for (i = 0; i < N_SERVOS; i++) {
    servos[i].initServo(
        servoPins[i],
        stepDelay[i],
        servoInitPosition[i]);
  }
#endif
}

/* Enter the main loop.  Read and parse input from the serial port
   and run any valid commands. */
void loop() {
  screen.start_service();
  screen.show(lcd);
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
