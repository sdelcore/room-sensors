/*
    Room Sensor Project

    Light sensor: A0
    Temperature Sensor: A1
    Humidity/Temperature Sensor: D3
    Sound Sensor: A2, D6

    Read from the sensors and parse it through the serial port in the created protocol

    Protocol for sending sensor through serial port
        Start sending a sensor reading: <
        Sensor indicator: 3 chars indicating sensor (XXX)
        Unit indicator: 1 char indicating unit of data (C/F/%)
        Sensor value numbers: ##
        Finish sending a sensor reading: >

        Example: <DHT+021.21C>
*/

#include "Arduino.h"
#include "DHT.h"

#define LIGHT_PIN 0
#define TEMP_PIN 1 // the cell and 10K pulldown are connected to a0
#define DHT_PIN 3
#define SOUND_DIGITAL_PIN 6
#define SOUND_ANALOG_PIN 2
#define START_READ_PIN 13

int start_read = 0;
int light_reading;     // the analog reading from the sensor divider
float temp_reading_raw;
int temp_reading;
int sound_digital_reading;
int sound_analog_reading;
int wait_time = 5000;

DHT dht(DHT_PIN, DHT11);

void setup(void) {
  Serial.begin(9600);

  dht.begin();
  pinMode(SOUND_DIGITAL_PIN, INPUT);
  pinMode(START_READ_PIN, INPUT);
  delay(wait_time);//Wait before accessing sensors
}

void loop(void) {
    start_read = digitalRead(START_READ_PIN);

    if(!start_read)
    {
        return;
    }

    int h = dht.readHumidity(); // Read temperature as percentage
    int t = dht.readTemperature(); // Read temperature as Celsius
    char dht_temp_str[10];
    sprintf(dht_temp_str, "<DHTC%d>", t);
    char dht_humid_str[10];
    sprintf(dht_humid_str, "<DHH%%%d>", h);

    light_reading = analogRead(LIGHT_PIN);
    char light_str[10];
    sprintf(light_str, "<LIT-%d>", light_reading);

    //gets and prints the raw data from the lm35
    temp_reading_raw = analogRead(TEMP_PIN);
    //converts raw data into degrees celsius and prints it out
    // 500mV/1024=.48828125
    temp_reading = temp_reading_raw * 500/1024;
    char temp_str[10];
    sprintf(temp_str, "<TMPC%d>", temp_reading);

    sound_digital_reading = digitalRead(SOUND_DIGITAL_PIN);
    sound_analog_reading = analogRead(SOUND_ANALOG_PIN);
    char sound_str[10];
    sprintf(sound_str, "<SND-%d>", sound_analog_reading);

    Serial.print(dht_humid_str);
    Serial.print(dht_temp_str);
    Serial.print(light_str);
    Serial.print(temp_str);
    Serial.print(sound_str);
}
