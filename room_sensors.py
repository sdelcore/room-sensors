#!/usr/bin/python    
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
		self.arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout =.5)
		self.database = Database()

	def readSerial(self):
		readings = []
		data = self.arduino.readline().strip()

		while data.count("<<") != 1 or data.count(">>") != 1:
			time.sleep(1)
			data = self.arduino.readline().strip()

		data = data[data.find('<<') + 1: data.find('>>') + 1]

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
			query = """INSERT INTO {0} (value, unit) 
				VALUES ({1}, '{2}')
				""".format(reading['sensor'], reading['value'], reading['unit'])
			self.database.insert(query)

	def getReadingsFromDB(self, data={}):
		sensor_readings = {}
		where = []
		query_where = ''
		
		if 'sensors' not in data:
			data['sensors'] = self.sensors.values()

		if 'day' in data:
			where.append('DAY(date) = {0}'.format(data['day']))

		if 'month' in data:
			where.append('MONTH(date) = {0}'.format(data['month']))
		
		if 'year' in data:
			where.append('YEAR(date) = {0}'.format(data['year']))

		if len(where) != 0:
			query_where = ' WHERE ' + where[0]
			where.pop(0)
			for cond in where:
				query_where += ' AND ' + cond

		for sensor in data['sensors']:
			if sensor not in self.sensors.values():
				continue

			select_query = 'SELECT * FROM {0}'.format(sensor)
			select_query += query_where
			sensor_readings[sensor] = self.database.query(select_query)

		return sensor_readings

if __name__ == "__main__":
	room = Room_Sensors()
	readings = room.readSerial()
	room.saveSerial(readings)
