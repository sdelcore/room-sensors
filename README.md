# room-sensors

## Project Explaination
There are 4 sensors connected to an Arduino, the readings from these sensors are then parsed and passed through the serial port to a Raspberry Pi. The Raspberry Pi takes the readings from the arduino every 30 minutes, and stores it into a MySQL database.
A websocket server and web page is hosted on the Raspberry Pi. The websocket server will pass the sensor data to the web page, and the web page will chart the data.

## Packages
 - pyserial
 - MySQL-python
 - platformio
 - SimpleWebSocketServer

## Sensors
 - DHT11 - for temperature and humidity
 - TMP36 - for temperature
 -  - for sound
 -  - for light

## Arduino Connections

