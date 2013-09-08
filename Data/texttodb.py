import sqlite3
import serial
import time, os
from datetime import datetime
from datetime import timedelta
DBFILE = 'wormdata.db'
DATAFILE = 'week6-7/TEST6.TXT'
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
    prevdt = None
    toffset = timedelta(0)
    for line in f.readlines():
        data = line.split(',')
        numdata = map(float, data[1:])
        if data[0]=="19700000000000":
            print "bad timestamp, datapoint skipped"
            continue
        dt = datetime.strptime(data[0], "%Y%m%d%H%M%S")

        # no timesync info, give up and skip data points
        if dt.year == 1970 and prevdt == None:
            #print "no timesync info, datapoint skipped:", line
            continue
        # first timesync'd datapoint received
        if prevdt == None:
            prevdt = dt
        # every datapoint gets the timestamp processed this way.
        # toffset is 0 until a timestamp glitch (below if stmt) is detected.
        dt = dt + toffset
        dtstr = datetime.strftime(dt, "%Y%m%d%H%M%S")

        # new timestamp is smaller than prev timestamp (including total loss of time sync resulting in year=1970).
        # I don't know how long the outage was ... assume it was 0. Define toffset to use from now on.
        if dt < prevdt:
            print "time reset occurred after", datetime.strftime(prevdt, "%Y%m%d%H%M%S")
            resetdt = prevdt
            toffset += resetdt - dt
            print "new toffset: ", toffset
            continue  # throw away this one datapoint

        numdata.insert(0, dtstr)
        insertintoDB(numdata)
        prevdt = dt

if __name__ == "__main__":
    if not os.path.exists(DBFILE):
        setupDB(N)
    readDataFile()


