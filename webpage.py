from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
import sqlite3, os, datetime, time

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('worms.db')
    c = conn.cursor()
    c.execute('''select * from worms order by id desc limit 1''')
    data = c.fetchone()
    [index, timestamp, temp, humidity, motion, imagestr] = data

    conn.commit()
    conn.close()

    return data

def get_all_temp_humid_data():
    conn = sqlite3.connect('worms.db')
    c = conn.cursor()
    timestamp_list = []
    temp_list = []
    humidity_list = []
    for row in c.execute('''select * from worms'''):
        timestamp = row[1]
        t = datetime.datetime.strptime(timestamp, "%Y-%m-%d_%H:%M:%S")
        timestamp_list.append( time.mktime(t.timetuple()) )
        temp_list.append( row[2] )
        humidity_list.append( row[3] )
    conn.commit()
    conn.close()

    return [timestamp_list, temp_list, humidity_list]

def get_alerts():
    conn = sqlite3.connect('worms.db')
    c = conn.cursor()
    alerts_list = []
    for row in c.execute('''select * from alerts order by id limit 5'''):
        color = row[3]
        if color == 0: color = (0,215, 137)
        if color == 1: color = (255, 84, 0)
        if color == 2: color = (94, 94, 94)
        alerts_list.append( [row[1], row[2], color, row[4]] )
    conn.commit()
    conn.close()

    return alerts_list


@app.route('/')
def serve_home():
    

    [index, timestamp, temp, humidity, motion, imagestr] = get_data()
    
    return render_template('index.html', temp=str(temp), humidity=str(humidity))

@app.route('/photos/')
def serve_photos():
    photopath = "./static/images/"
    allfiles = [photopath+f for f in os.listdir(photopath)]
    latest_file = max(allfiles, key=os.path.getmtime)
    datestr = datetime.datetime.fromtimestamp(os.path.getmtime(latest_file)).strftime("%Y-%m-%d %H:%M:%S")
    return render_template('photos.html', 
        imagefilename=latest_file.lstrip('.'), datestr=datestr)

@app.route('/alerts/')
def serve_alerts():
    alerts_list = get_alerts()
    return render_template('alerts.html', alerts_list=alerts_list)

@app.route('/statistics/')
def serve_statistics():
    [timestamp_list, temp_list, humidity_list] = get_all_temp_humid_data()
    datastr = '['
    for time, temp, humid in zip(timestamp_list, temp_list, humidity_list):
        datastr = datastr+ '{ x:'+ str(time)+', y: '+str(temp)+' },'
    datastr = datastr + ']'

    return render_template('statistics.html', datastr=datastr)    

@app.route('/about/')
def serve_about():

    return render_template('about.html')

@app.route('/settings/')
def serve_settings():

    return render_template('settings.html')

@app.route('/mobilegraph/')
def serve_mobilegraph():

    return render_template('mobilegraph.html')


if __name__ == '__main__':
    app.run()