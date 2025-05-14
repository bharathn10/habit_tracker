from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)
DB_NAME = 'database.db'

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            start_date TEXT NOT NULL,
            last_completed TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM habits')
    habits = c.fetchall()
    conn.close()
    return render_template('index.html', habits=habits, today=date.today())

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    frequency = request.form['frequency']
    start_date = request.form['start_date']

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO habits (name, frequency, start_date) VALUES (?, ?, ?)',
              (name, frequency, start_date))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM habits WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    today_str = str(date.today())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE habits SET last_completed = ? WHERE id = ?', (today_str, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
