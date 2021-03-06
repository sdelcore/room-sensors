/*
    Room Sensor Project

    Light sensor: A0
    Temperature Sensor: A1
    Humidity/Temperature Sensor: D3
    Sound Sensor: A2, D6

    Read from the sensors and parse it through the serial port using the following protocol

    Protocol:
        Start sending multiple sensors data: <
	Start sending a sensor reading: <
        Sensor indicator: 3 chars indicating sensor (XXX)
        Unit indicator: 1 char indicating unit of data (C/F/%)
        Sensor value numbers: ##
        Finish sending a sensor reading: >
	Finish sending multiple sensor data: >

        Example: <<DHT##C><TMP##C>>
*/

#include "Arduino.h"
#include "DHT.h"

#define LIGHT_PIN 0
#define TEMP_PIN 1
#define DHT_PIN 3
#define SOUND_DIGITAL_PIN 6
#define SOUND_ANALOG_PIN 2
#define START_READ_PIN 13

int light_reading;
float temp_reading_raw;
int temp_reading;
int sound_digital_reading;
int sound_analog_reading;

DHT dht(DHT_PIN, DHT11);

void setup(void) {
  Serial.begin(9600);

  dht.begin();
  pinMode(SOUND_DIGITAL_PIN, INPUT);
  pinMode(START_READ_PIN, INPUT);
  delay(5000);//Wait before accessing sensors
}

void serialFlush(){
  while(Serial.available() > 0) {
    Serial.read();
  }
}

void loop(void) {
    int h = dht.readHumidity(); // Read temperature as percentage
    int t = dht.readTemperature(); // Read temperature as Celsius
    char dht_temp_str[10];
    sprintf(dht_temp_str, "<DHTC%d>", t);
    char dht_humid_str[10];
    sprintf(dht_humid_str, "<DHH%%%d>", h);

    light_reading = analogRead(LIGHT_PIN);
    char light_str[10];
    sprintf(light_str, "<LIT-%d>", light_reading);

    temp_reading_raw = analogRead(TEMP_PIN);
    temp_reading = temp_reading_raw * 500/1024;//converts raw data into degrees celsius and prints it out
    char temp_str[10];
    sprintf(temp_str, "<TMPC%d>", temp_reading);

    sound_digital_reading = digitalRead(SOUND_DIGITAL_PIN);
    sound_analog_reading = analogRead(SOUND_ANALOG_PIN);
    char sound_str[10];
    sprintf(sound_str, "<SND-%d>", sound_analog_reading);

    serialFlush();
    Serial.print('<');
    Serial.print(dht_humid_str);
    Serial.print(dht_temp_str);
    Serial.print(light_str);
    Serial.print(temp_str);
    Serial.print(sound_str);
    Serial.println('>');
    delay(5000);
}
