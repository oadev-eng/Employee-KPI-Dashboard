from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'employees.db'

# ----- Database Setup ----- #
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT NOT NULL,
            tasks_completed INTEGER DEFAULT 0,
            performance_score REAL DEFAULT 0.0,
            last_review_date TEXT DEFAULT CURRENT_DATE            
        )
    ''')
    conn.commit()
    conn.close()

# ----- Helper Functions ----- #
def add_employee_to_db(name, team, tasks_completed, performance_score):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, team, tasks_completed, performance_score, last_review_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, team, tasks_completed, performance_score, datetime.today().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

def get_all_employees():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    conn.close()
    employees = []
    for row in rows:
        employees.append({
            "id": row[0],
            "name": row[1],
            "team": row[2],
            "task_completed": row[3],
            "performance_score": row[4],
            "last_review_date": row[5]
        })
    return employees

# ----- Routes ----- #
@app.route('/')
def index():
    employees = get_all_employees()
    return render_template('dashboard.html', employees=employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.form
    add_employee_to_db(
        name=data.get('name'),
        team=data.get('team'),
        tasks_completed=int(data.get('tasks_completed', 0)),
        performance_score=float(data.get('performance_score', 0.0))
    )
    return jsonify({"message": "Employee added successfully"})

@app.route('/export_json')
def export_json():
    employees = get_all_employees()
    return jsonify(employees)

# -----Main----- #
if __name__ == '__main__':
    init_db()
    app.run(debug=True)    

