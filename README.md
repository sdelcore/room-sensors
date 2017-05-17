# room-sensors

## Project Explaination
There are 4 sensors connected to an Arduino, the readings from these sensors are then parsed and written to the serial port. The Raspberry Pi reads from the serial port every 30 minutes, and stores the data into a MySQL database.
A websocket server and web page is hosted on the Raspberry Pi. The websocket server will pass the sensor data to the web page, and the web page contains a chart of the data.

## Packages
 - Python27:
   - pyserial
   - MySQL-python
   - SimpleWebSocketServer
 - platformio
 - MySQL
 - lighttpd

## Sensors
 - DHT11 - Digital PWM Pin 3
 - LM36 - Analog Pin 1
 - Sound Sensor - Analog Pin 2
 - Photocell - Analog Pin 0

## Serial Port Protocol
Start sending multiple sensors data: `<`
Start sending a sensor reading: `<`
Sensor indicator: 3 chars indicating sensor `XXX`
Unit indicator: 1 char indicating unit of data `C/F/%`
Sensor value numbers(any length): `##`
Finish sending a sensor reading: `>`
Finish sending multiple sensor data: `>`

Example: `<<DHT##C><TMP##C>>`

The Raspberry Pi will know when a new set of readings start and end when it sees `<<` and `>>` respectivly
