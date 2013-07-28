import sqlite3
import serial
import time
from datetime import datetime
from subprocess import Popen
SERIAL_PORT = 'fa131'
DATAFILE = 'stream.txt'
numcols = 2

def getTimeStamp():
    # first get the current time stamp
    curtime = datetime.now()
    timestamp = curtime.strftime("%Y%m%d%H%M%S")
    return timestamp

def readArduino(numcols):
    ser = serial.Serial(port='/dev/tty.usbmodem' + SERIAL_PORT, baudrate=9600)
    #print "arduino opened"
    attempts = 0
    while(True):
        try:
            line = ser.readline()
            attempts += 1
            print line
            if len(line.split(',')) == numcols+1: # include "ok" line
                break
        except Exception, e:
            pass
        if attempts >= 20:
            raise Exception("Arduino read error. Is it connected?")
    #print "saving last line to DB"
    ser.flush()
    ser.close()

    return line

def writeToLog(timestamp, datarow):
    f = open(DATAFILE, 'a')
    datarow = datarow.lstrip('OK,')
    f.write(timestamp+','+datarow)
    f.close()

if __name__ == "__main__":

    while(1):
        timestamp = getTimeStamp()
        try:
            data = readArduino(numcols)
            writeToLog(timestamp, data)
        except Exception, e:
            print e
        time.sleep(1)


