from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
import sqlite3, os, datetime

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

    return render_template('alerts.html')

@app.route('/statistics/')
def serve_alerts():

    return render_template('statistics.html')

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