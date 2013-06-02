import sqlite3
import serial
import time
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
    print "arduino opened"
    attempts = 0
    while(True):
        try:
            line = ser.readline()
            attempts += 1
            print line
            if len(map(float, line.split(','))) == 2:
                break
        except Exception, e:
            pass
        if attempts >= 20:
            raise Exception("Cannot find Arduino. Is it connected?")
    print line
    print "saving last line to DB"
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
    # get the last entry id and increment it
    c.execute("select * from worms order by id desc limit 1")
    olddata = c.fetchone()
    try:
    	index = int(olddata[0]) + 1
    except Exception, e:
    	index = 1
    # this is the actual data
    [timestamp, temp, humidity, motion] = data
    c.execute("insert into worms values (?,?,?,?,?)",
        (index, timestamp, temp, humidity, motion))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    while(1):
        data = readArduino()
        insertintoDB(data)
        time.sleep(10)