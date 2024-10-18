#define USE_BASE      // Enable the base controller code
//#undef USE_BASE     // Disable the base controller code

/* Define the motor controller and encoder library you are using */
#ifdef USE_BASE
   /* L298 Motor driver */
   #define L298_MOTOR_DRIVER
#endif

#include <Servo.h>   //載入函式庫，這是內建的，不用安裝
Servo myservo;  // 建立SERVO物件

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
  case ULTRA_SONIC_VALUE:
    Serial.println(ultra_sonic_arr[arg1].get_val());
    break;
  case SCREEN:
    screen.set_words(0, argv1);
    screen.set_words(1, argv2);
    break;
  case GOOSE:
    if(arg1 == 1){
      analogWrite(2, 50);
      analogWrite(3, 0);
      delay(arg2);
      analogWrite(2, 0);
      analogWrite(3, 0);
    }
    else if(arg1 == 0){
      analogWrite(3, 50);
      analogWrite(2, 0);
      delay(arg2);
      analogWrite(2, 0);
      analogWrite(3, 0);
    }
    break;
  case CAMERA:
    myservo.write(0);  //旋轉到0度，就是一般所說的歸零
    delay(1000);
    myservo.write(arg1); //旋轉到90度
    delay(1000);
    break;
  case LASER:
    digitalWrite(31, 1);
    delay(arg1);
    digitalWrite(31, 0);
    break; 
  case LED:
    if (strcmp(argv2, "r") == 0) {
      digitalWrite(49, 1);
      delay(atoi(argv2));  // 將字串轉爲整數
      digitalWrite(49, 0);
    } 
    if (strcmp(argv1, "y") == 0) {
      digitalWrite(51, 1);
      delay(atoi(argv2));  // 將字串轉爲整數
      digitalWrite(51, 0);
    } 
    else if (strcmp(argv1, "g") == 0) {
      digitalWrite(52, 1);
      delay(atoi(argv2));
      digitalWrite(52, 0);
    } 
    else {
      digitalWrite(49, 0);
      digitalWrite(51, 0);
      digitalWrite(52, 0);
    }
    break;
   

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
  myservo.attach(8);  // 設定要將伺服馬達接到哪一個PIN腳
  pinMode(2, OUTPUT); // goose
  pinMode(3, OUTPUT); // goose
  pinMode(31, OUTPUT); // laser
  pinMode(49, OUTPUT); // red
  pinMode(51, OUTPUT); // yellow
  pinMode(52, OUTPUT); // green
  Serial.begin(BAUDRATE);
  delay(100);
  check_connection();
  
  init_ults();

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
