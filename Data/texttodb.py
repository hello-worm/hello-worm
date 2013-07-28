import sqlite3
import serial
import time
from datetime import datetime
DBFILE = 'wormdata.db'
DATAFILE = 'test-week1.txt'

def setupDB():
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute('''create table worm (time text, temp float, hum float)''')
    conn.commit()
    conn.close()

def insertintoDB(data):
    # insert data tuple into db
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    [datestr, temp, hum] = data
    c.execute("insert into worm values (?,?,?)",
        (datestr, temp, hum))
    conn.commit()
    conn.close()

def readDataFile():
    # extract data from text file and dump into sqlite db
    f = open(DATAFILE, 'r')
    for line in f.readlines():
        [datestr, temp, hum] = line.split(',')
        temp = float(temp)
        hum = float(hum)
        if datestr[0:4] == '1970':
            print "line skipped: ", datestr
        else:
            insertintoDB((datestr, temp, hum))

if __name__ == "__main__":
    readDataFile()


