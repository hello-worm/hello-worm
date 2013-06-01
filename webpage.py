from flask import Flask, render_template
from jinja2 import Environment, PackageLoader
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    conn = sqlite3.connect('worms.db')
    c = conn.cursor()
    c.execute('''select * from worms''')
    data = c.fetchall()
    print data
    conn.commit()
    conn.close()

    env = Environment(loader=PackageLoader('webpage', 'templates'))
    # template = env.get_template('compost.html')

    return render_template('compost.html', hello="world")

if __name__ == '__main__':
    app.run()