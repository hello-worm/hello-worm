from flask import Flask
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
    html = "<html><head></head><body>" + str(data) + "</body></html>"
    return str(data)

if __name__ == '__main__':
    app.run()