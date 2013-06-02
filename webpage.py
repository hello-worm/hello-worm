from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
import sqlite3

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
    
    [index, timestamp, temp, humidity, motion, imagestr] = get_data();

    env = Environment(loader=PackageLoader('webpage', 'templates'))
    
    return render_template('compost.html', temp=str(temp), humidity=str(humidity))

@app.route('/photos/')
def serve_photos():

    return 'photos'

@app.route('/alerts/')
def serve_alerts():

    return 'alerts'

@app.route('/about/')
def serve_about():

    return 'about'

@app.route('/settings/')
def serve_settings():

    return 'settings'


if __name__ == '__main__':
    app.run()