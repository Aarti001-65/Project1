import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'Linkkiwi2026'

def get_db():
    conn = sqlite3.connect('practise.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        marks INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()
    
@app.route('/')
def home():
    conn = get_db()
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('home.html',students=students)

def add_student():
    if request.method == "POST":
        name = request.form["student_name"]
        marks = request.form["marks"]
        roll = request.form["roll"]
        subject = request.form["subject"]
        attendance = request.form["attendance"]
        if not name or not marks:
            flash('Please provide both name and marks', 'danger')
            return render_template("add_students.html")
        
        conn = get_db()
        conn.execute('''INSERT INTO students
                     (name,roll,marks,subject,attendance) VALUES(?,?,?,?,?)''',
                     (name, roll, int(marks), subject, int(attendance))
                     )
        conn.commit()
        conn.close()
        
         # Print to terminal
        print(f"Received new student: {name} with marks: {marks}")
       
        # Flash message to user
        flash(f"Student {name} added successfully!", "success")
       
    return render_template("add_students.html")

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db()
    
    student = conn.execute('DELETE FROM students WHERE id = ?', (id))
    conn.commit()
    conn.close()
    
    flash(f"{student['name']} deleted", 'success')
    return redirect(url_for('student_page'))
    
    
    