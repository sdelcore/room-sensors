class Room_Sensors:
	sensors = {
	 'DHT': 'dht11',
	 'SND': 'sound',
	 'LIT': 'light',
	 'TMP': 'temperature'
	}

	arduino = serial.Serial('COM1', 9600, timeout=.1)

	def readSerial():
		readings = []
		data = arduino.readline()
		while(data.contains('>')):
			start = data.indexOf('<') + 1
			end = data.indexOf('>') + 1
			reading = data[start:end]
			data = reading[end:]
			readings.Add(
				{
					'sensor': sensors[reading[:2]],
					'value': float(reading[2:9]),
					'unit': reading[9:10]
				})
		return readings

	def sendSerial(message):
		arduino.write(message)

	def start():
		db = Database()
		Room_Sensors.sendSerial("START")
		readings = Room_Sensors.readSerial
		date = datetime.datetime.now()
		month = date.strftime("%m")
		day = date.strftime("%d")
		year = date.strftime("%Y")
		time = date.strftime("%X")
		for reading in readings:
			query = "INSERT INTO ? (`value`, `unit`, 'day', 'month', 'year', 'time') VALUES (?, ?, ?, ?, ?, ?)", (reading[sensor], reading[value], reading[unit], day, month, year, time)
			db.insert(query)