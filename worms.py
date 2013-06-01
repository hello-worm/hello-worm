import sqlite3
import serial
from datetime import datetime

def setupDB():
	conn = sqlite3.connect('worms.db')
	c = conn.cursor()
	c.execute('''create table worms (id int, time text, temp float, 
		humidity float, motion integer)''')
	conn.commit()
	conn.close()

def readArduino():
	ser = serial.Serial(port='/dev/tty.usbmodemfd121', baudrate=9600)
	line = ser.readline()
	print line

	# first get the current time stamp
	curtime = datetime.now()
	timestamp = curtime.strftime("%Y-%m-%d_%H:%M:%S")

	# so far we only have temp and humidity sensors
	[temp,humidity] = line.split(',')
	temp = float(temp)
	humidity = float(humidity)
	# add other sensors here
	motion = 0

	return [timestamp, temp, humidity, motion]

def insertintoDB(data):
	conn = sqlite3.connect('worms.db')
	c = conn.cursor()
	c.execute("select * from worms order by id desc limit 1")
	data = c.fetchone()
	index = int(data[0])
	index += 1
	[timestamp, temp, humidity, motion] = data
	c.execute("insert into worms values (index, timestamp, temp, humidity, motion)")
	conn.commit()
	comm.close()

if __name__ == "__main__":
	data = readArduino()
	insertintoDB(data)