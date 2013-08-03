import sqlite3
import serial
import time, os
from datetime import datetime
DBFILE = 'wormdata.db'
DATAFILE = 'TEST2.TXT'
N=5

def setupDB(n=3):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    if n == 3:
        c.execute('''create table worm (time text, temp float, hum float)''')
    elif n == 5:
        c.execute('''create table worm (time text, temp float, hum float, 
            gas1 float, gas2 float)''')
    elif n == 6:
        c.execute('''create table worm (time text, temp float, temp2 float, 
            hum float, gas1 float, gas2 float)''')
    else: 
        print "warning: n = 3, 5, 6"
    conn.commit()
    conn.close()

def insertintoDB(data):
    # insert data tuple into db
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    n = len(data)
    c.execute("insert into worm values (" + ('?,'*n).rstrip(',') + ")", data)
    conn.commit()
    conn.close()

def readDataFile():
    # extract data from text file and dump into sqlite db
    f = open(DATAFILE, 'r')
    for line in f.readlines():
        data = line.split(',')
        numdata = map(float, data[1:])
        if data[0][0:4] == '1970':
            print "line skipped: ", data
        else:
            numdata.insert(0, data[0])
            insertintoDB(numdata)

if __name__ == "__main__":
    if not os.path.exists(DBFILE):
        setupDB(N)
    readDataFile()


