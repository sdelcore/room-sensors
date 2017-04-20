from database import Database
import serial
import datetime
import time

class Room_Sensors:
	sensors = {
	 'DHT': 'dht11_temperature',
	 'DHH': 'dht11_humidity',
	 'SND': 'sound',
	 'LIT': 'light',
	 'TMP': 'temperature'
	}

	def __init__(self):
		self.arduino = serial.Serial('/dev/ttyUSB0', 9600)
		self.database = Database()

	def readSerial(self):
		readings = []
		data = self.arduino.readline().strip()

		while data.count("<<") != 1 or data.count(">>") != 1:
			time.sleep(1)
			data = self.arduino.readline().strip()

		data = data[2:-2]
		while '<' in data:
			start = data.find('<') + 1
			end = data.find('>')
			reading = data[start:end]
			data = data[end + 1:]
			readings.append(
				{
					'sensor': self.sensors[reading[:3]],
					'value': float(reading[4:]),
					'unit': reading[3:4]
				})
			
		return readings

	def sendSerial(self, message):
		self.arduino.write(message)

	def saveSerial(self, readings):
		date = datetime.datetime.now()
		month = date.strftime("%m")
		day = date.strftime("%d")
		year = date.strftime("%Y")
		time = date.strftime("%X")

		for reading in readings:
			query = "INSERT INTO ? (`value`, `unit`, 'day', 'month', 'year', 'time') VALUES (?, ?, ?, ?, ?, ?)", (reading['sensor'], reading['value'], reading['unit'], day, month, year, time)
			self.database.insert(query)

	def getReadingsFromDB(self, sensors = sensors.values(), day='*', month='*', year='*'):
		sensor_readings = []
		for sensor in sensors:
			select_query = "SELECT * FROM ? WHERE day = ? AND month = ? AND year = ?", (sensor, day, month, year)
			sensor_readings['sensor'] = self.database.query(select_query)
		return sensor_readings

if __name__ == "__main__":
	room = Room_Sensors()
	readings = room.readSerial()
	room.saveSerial(readings)
