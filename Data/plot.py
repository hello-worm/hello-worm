import sqlite3, time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.dates as mdates

DBFILE = 'wormdata.db'
GRAPHFILE = 'wk3_data.png'
GRAPHFILEWK = 'wk3_bywkday.png'


def getndat(all=False):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    if all:
        sql = 'select * from worm'# where rowid%100=0'
    else:
        sql = 'select * from worm order by rowid desc limit 288'
    c.execute(sql)
    data = c.fetchall()
    c.close()
    return(data)

def parsedata(data):
    date = []
    rawdata = []
    for row in data:
        # get temp and humidity data
        num = map(float, row[1:])
        rawdata.append(num)
        # get and parse date data
        dtstr = row[0]
        dt = datetime.strptime(dtstr, "%Y%m%d%H%M%S")
        date.append(dt)

    return date, rawdata

def plotdata(date, rawdata, cols='0123'):
    vardict = {
        '0': 'Temperature [F]',
        '1': 'Humidity [%]',
        '2': 'MQ4', 
        '3': 'MQ8'
        }
    fig = pl.figure(1)
    ax = fig.add_subplot(len(cols),1,1)
    ax.plot(date, rawdata[:,int(cols[0])], 'b')
    ax.set_ylabel(vardict[cols[0]])
    axes = [ax]

    if len(cols)>1:
        ax2 = fig.add_subplot(len(cols),1,2)
        ax2.plot(date, rawdata[:,int(cols[1])], 'g')
        ax2.set_ylabel(vardict[cols[1]])
        axes.append(ax2)
    if len(cols)>2:
        ax3 = fig.add_subplot(len(cols),1,3)
        ax3.plot(date, rawdata[:,int(cols[2])], 'r')
        ax3.set_ylabel(vardict[cols[2]])
        axes.append(ax3)
    if len(cols)>3:
        ax4 = fig.add_subplot(len(cols),1,4)
        ax4.plot(date, rawdata[:,int(cols[3])], 'r')
        ax4.set_ylabel(vardict[cols[3]])
        axes.append(ax4)

    ax.set_title('Hello Worm data '+ datetime.strftime(date[0], "%m/%d") \
        + "-" + datetime.strftime(date[-1], "%m/%d"))
    axes[-1].set_xlabel('Time')
    for axis in axes:
        axis.xaxis.set_major_locator(mdates.DayLocator())
        axis.xaxis.set_minor_locator(mdates.HourLocator(interval=4))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%a %m/%d'))
    
    fig.autofmt_xdate()
    pl.savefig(GRAPHFILE)
    pl.show()

def weekdays(date, rawdata):
    temp = rawdata[:,0]
    hum = rawdata[:,1]
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
    ax.set_title('Helloworm data by weekday ')
    ax.legend(['Mon', 'Tues', 'Wed', 'Thu', 'Fri'], prop={'size':10})
    fig.autofmt_xdate()
    pl.savefig(GRAPHFILEWK)
    pl.show()

if __name__ == "__main__":
    data = getndat(True)
    date, rawdata = parsedata(data) 
    #plotdata(date, np.array(rawdata))
    weekdays(date, np.array(rawdata))

