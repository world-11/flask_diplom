from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging
import logging.config
import yaml

app = Flask(__name__)

# Load logging configuration
with open('logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

# Инициализация БД
def init_db():
    conn = sqlite3.connect('athletes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS athletes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS athlete_competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id INTEGER NOT NULL,
            competition_id INTEGER NOT NULL,
            FOREIGN KEY (athlete_id) REFERENCES athletes (id),
            FOREIGN KEY (competition_id) REFERENCES competitions (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/athletes', methods=['GET', 'POST'])
def athletes():
    conn = sqlite3.connect('athletes.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form['name']
            age = request.form['age']
            cursor.execute('INSERT INTO athletes (name, age) VALUES (?, ?)', (name, age))
        elif 'edit' in request.form:
            id = request.form['id']
            name = request.form['name']
            age = request.form['age']
            cursor.execute('UPDATE athletes SET name=?, age=? WHERE id=?', (name, age, id))
        elif 'delete' in request.form:
            id = request.form['id']
            cursor.execute('DELETE FROM athletes WHERE id=?', (id,))
        conn.commit()

    cursor.execute('SELECT * FROM athletes')
    athletes = cursor.fetchall()
    conn.close()
    return render_template('athletes.html', athletes=athletes)

@app.route('/competitions', methods=['GET', 'POST'])
def competitions():
    conn = sqlite3.connect('athletes.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form['name']
            date = request.form['date']
            cursor.execute('INSERT INTO competitions (name, date) VALUES (?, ?)', (name, date))
        elif 'edit' in request.form:
            id = request.form['id']
            name = request.form['name']
            date = request.form['date']
            cursor.execute('UPDATE competitions SET name=?, date=? WHERE id=?', (name, date, id))
        elif 'delete' in request.form:
            id = request.form['id']
            cursor.execute('DELETE FROM competitions WHERE id=?', (id,))
        conn.commit()

    cursor.execute('SELECT * FROM competitions')
    competitions = cursor.fetchall()
    conn.close()
    return render_template('competitions.html', competitions=competitions)

@app.route('/athlete_competitions', methods=['GET', 'POST'])
def athlete_competitions():
    conn = sqlite3.connect('athletes.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        athlete_id = request.form['athlete_id']
        competition_id = request.form['competition_id']
        cursor.execute('INSERT INTO athlete_competitions (athlete_id, competition_id) VALUES (?, ?)', (athlete_id, competition_id))
        conn.commit()
    cursor.execute('''
        SELECT a.name, c.name, ac.competition_id
        FROM athlete_competitions ac
        JOIN athletes a ON ac.athlete_id = a.id
        JOIN competitions c ON ac.competition_id = c.id
    ''')
    athlete_competitions = cursor.fetchall()
    conn.close()
    return render_template('athlete_competitions.html', athlete_competitions=athlete_competitions)

if __name__ == '__main__':
    app.run(debug=True)
