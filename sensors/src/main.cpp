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
        Sensor value sign: +/-
        Sensor value numbers: ###.##
        Unit indicator: 1 char indicating unit of data (C/F/%)
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

int light_reading;     // the analog reading from the sensor divider
float temp_reading;
int sound_digital_reading;
int sound_analog_reading;
int wait_time = 5000;

DHT dht(DHT_PIN, DHT11);

void setup(void) {
  Serial.begin(9600);

  dht.begin();
  pinMode(SOUND_DIGITAL_PIN, INPUT);

  delay(wait_time);//Wait before accessing sensors
}

void loop(void) {
    Serial.println("------HUMIDITY-------");
    float h = dht.readHumidity(); // Read temperature as percentage
    float t = dht.readTemperature(); // Read temperature as Celsius
    float f = dht.readTemperature(true); // Read temperature as Fahrenheit

    float hif = dht.computeHeatIndex(f, h); // Compute heat index in Fahrenheit
    float hic = dht.computeHeatIndex(t, h, false); // Compute heat index in Celsius

    Serial.print("Humidity: ");
    Serial.print(h);
    Serial.println(" %\t");
    Serial.print("Temperature: ");
    Serial.print(t);
    Serial.println(" *C ");
    Serial.print(f);
    Serial.println(" *F\t");
    Serial.print("Heat index: ");
    Serial.print(hic);
    Serial.println(" *C ");
    Serial.print(hif);
    Serial.println(" *F");

    Serial.println("--------LIGHT-------");
    light_reading = analogRead(LIGHT_PIN);
    Serial.print("Light Sensor: ");
    Serial.println(light_reading);     // the raw analog reading

    //gets and prints the raw data from the lm35
    Serial.println("----------TEMP----------");
    temp_reading = analogRead(TEMP_PIN);
    Serial.print("RAW DATA: ");
    Serial.print (temp_reading);
    Serial.println(" ");
    //converts raw data into degrees celsius and prints it out
    // 500mV/1024=.48828125
    temp_reading = temp_reading * 500/1024;
    Serial.print("CELSIUS: ");
    Serial.print(temp_reading);
    Serial.println("*C ");
    //converts celsius into fahrenheit
    temp_reading = temp_reading *9 / 5;
    temp_reading = temp_reading + 32;
    Serial.print("FAHRENHEIT: ");
    Serial.print(temp_reading);
    Serial.println("*F");

    Serial.println("----------SOUND----------");
    sound_digital_reading = digitalRead(SOUND_DIGITAL_PIN);
    sound_analog_reading = analogRead(SOUND_ANALOG_PIN);
    Serial.print("Sound digital output: ");
    Serial.println(sound_digital_reading);
    Serial.print("Sound analog output: ");
    Serial.println(sound_analog_reading);

    Serial.println("--------DONE-------");
    delay(wait_time);
}
