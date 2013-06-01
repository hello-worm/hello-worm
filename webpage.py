from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    conn = sqlite3.connect('worms.db')
    c = conn.cursor() 
    c.execute('''select * from worms order by id desc limit 1''')
    data = c.fetchone()
    [index, timestamp, temp, humidity, motion] = data

    conn.commit()
    conn.close()

    env = Environment(loader=PackageLoader('webpage', 'templates'))
    

    return render_template('compost.html', temp=str(temp), humidity=str(humidity))

if __name__ == '__main__':
    app.run()