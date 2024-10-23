/* Define single-letter commands that will be sent by the PC over the
   serial link.
*/

#ifndef COMMANDS_H
#define COMMANDS_H

#define ANALOG_READ    'a'
#define GET_BAUDRATE   'b'
#define PIN_MODE       'c'
#define DIGITAL_READ   'd'
#define MOTOR_RAW_PWM  'o'
#define SCREEN         's'
#define ULTRA_SONIC_VALUE 'u'
#define DIGITAL_WRITE  'w'
#define ANALOG_WRITE   'x'
#define GOOSE          'g'
#define WEIGHT_CALIBRATE 'i' // 獲取 weight calibration 數值
#define WEIGHT_CALIBRATE_VAL_INPUT 'I'
#define WEIGHT_GET 'j' // 獲取 weight 數值
#define LEFT            0
#define RIGHT           1

#endif


