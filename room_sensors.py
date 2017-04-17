from database import Database

class Room_Sensors:
	sensors = {
	 'DHT': 'dht11_temperature',
	 'DHH': 'dht_humidity,'
	 'SND': 'sound',
	 'LIT': 'light',
	 'TMP': 'temperature'
	}

	def __init__(self):
		self.arduino = serial.Serial('COM1', 9600, timeout=.1)
		self.database = Database()

	def readSerial(self):
		readings = []
		data = self.arduino.readline()
		while(data.contains('>')):
			start = data.indexOf('<') + 1
			end = data.indexOf('>') + 1
			reading = data[start:end]
			data = reading[end:]
			readings.Add(
				{
					'sensor': self.sensors[reading[:2]],
					'value': float(reading[2:9]),
					'unit': reading[9:10]
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

	def getReadingsFromDB(self, sensors = self.sensors.values(), day='*', month='*', year='*')
		sensor_readings = []
		for sensor in sensors:
			select_query = "SELECT * FROM ? WHERE day = ? AND month = ? AND year = ?", (sensor, day, month, year)
			sensor_readings.Add('sensor': self.database.query(select_query))
		return sensor_readings

if __name__ == "__main__":
	room = Room_Sensors()
	room.sendSerial("read")
	readings = room.readSerial()
	room.saveSerial(readings)