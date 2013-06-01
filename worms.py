import sqlite3
import serial

def setupDB():
	conn = sqlite3.connect('worms.db')
	c = conn.cursor()
	c.execute('''create table worms (time text, temp float, 
		humidity float, motion integer)''')
	conn.commit()
	conn.close()

def readArduino():
	ser = serial.Serial(port='/dev/tty.usbmodemfd121', baudrate=9600)
	line = ser.readline()
	print line
	[temp,humidity] = line.split(',')
	temp = float(temp)
	humidity = float(humidity)
	return temp, humidity

if __name__ == "__main__":
	print "hello world"