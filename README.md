# room-sensors

## Project Setup
There are 4 sensors connected to an arduino, the readings from these sensors are then parsed and passed through the serial port to a Raspberry Pi. The Raspberry Pi takes readings from the arduino every 30 minutes, and stores it into a MySQL database.
A websocket server is hosted on the raspberry pi, and a web page as well. The web page charts the data that gets passed through the websocket.

## pip packages
 - pyserial
 - MySQL-python
 - platformio
 - SimpleWebSocketServer

 ## Start websocket server on startup
 Add `$proj_dir` to your list of start up scripts