import sqlite3, time
from datetime import datetime
import matplotlib.pyplot as pl
import matplotlib.dates as mdates

DBFILE = 'wormdata.db'
GRAPHFILE = 'wk1_data.png'
GRAPHFILEWK = 'wk1_bywkday.png'


def getndat(all=False):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    if all:
        sql = 'select * from worm where rowid%100=0'
    else:
        sql = 'select * from worm order by rowid desc limit 288'
    c.execute(sql)
    data = c.fetchall()
    c.close()
    return(data)

def parsedata(data):
    date = []
    temp = []
    hum = []
    for row in data:
        # get temp and humidity data
        num = map(float, row[1:])
        temp.append(num[0])
        hum.append(num[1])
        # get and parse date data
        dtstr = row[0]
        dt = datetime.strptime(dtstr, "%Y%m%d%H%M%S")
        date.append(dt)

    return date, temp, hum

def plotdata(date, temp, hum):
    fig = pl.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(date, temp, 'b')
    ax.set_ylabel('Temperature [F]')

    ax2 = fig.add_subplot(212)
    ax2.plot(date, hum, 'g')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Humidity [%]')

    ax.set_title('Hello Worm data week 1')

    ax2.xaxis.set_major_locator(mdates.DayLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%a %m/%d'))
    ax2.xaxis.set_minor_locator(mdates.HourLocator(interval=4))
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=4))
    fig.autofmt_xdate()
    pl.savefig(GRAPHFILE)
    pl.show()

def weekdays(date, temp, hum):
    tempbywkday = [[],[],[],[],[]]
    datebywkday = [[],[],[],[],[]]
    for d, t, h in zip(date, temp, hum):
        wkday = d.weekday()
        if wkday in [0,1,2,3,4]:
            d = d.replace(day=1)
            datebywkday[wkday].append(d)
            tempbywkday[wkday].append(t)

    fig = pl.figure(2)
    ax = fig.add_subplot(111)
    for i in range(5):
        ax.plot(datebywkday[i], tempbywkday[i])
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:00'))
    #ax.xaxis.set_minor_locator(mdates.HourLocator(interval=4))
    ax.set_xlabel('Time [hr]')
    ax.set_ylabel('Temperature [F]')
    ax.set_title('Helloworm data week 1 by weekday')
    ax.legend(['Mon', 'Tues', 'Wed', 'Thu', 'Fri'], prop={'size':10})
    fig.autofmt_xdate()
    pl.savefig(GRAPHFILEWK)
    pl.show()

if __name__ == "__main__":
    data = getndat(True)
    date, temp, hum = parsedata(data) 
    plotdata(date, temp, hum)
    weekdays(date, temp, hum)

