# room-sensors

## Project Explaination
There are 4 sensors connected to an Arduino, the readings from these sensors are then parsed and written to the serial port. The Raspberry Pi reads from the serial port every 30 minutes, and stores the data into a MySQL database.
A websocket server and web page is hosted on the Raspberry Pi. The websocket server will pass the sensor data to the web page, and the web page contains a chart of the data.

## Packages
 - Python27:
   - pyserial
   - MySQL-python
   - SimpleWebSocketServer `sudo pip install git+https://github.com/dpallot/simple-websocket-server.git`
   - platformio
 - MySQL
 - python-devel
 - lighttpd
 - git

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

The Raspberry Pi will know when a new full set of readings occur when sees `<<` and `>>`

## Web page setup
Change line `192.168.0.12`  in `/var/www/html/figure.js` to the ip address of the RPi

## Install Script
This script will:
 1. clone from the git repo
 1. make needed scripts executable
 1. modify needed scripts with provided information at the top of the install script
 1. push the arduino code to the connected arduino
 1. create needed database and tables 
 1. copy the web pages to `/var/www/html`
 
