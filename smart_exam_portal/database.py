import sqlite3

def get_db():
    conn = sqlite3.connect("myproject.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():

    conn = get_db()

    conn.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no INTEGER,
    subject_name TEXT,
    student_name TEXT,
    score INTEGER,
    percentage REAL,
    exam_date TEXT
)
""")
    conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

    conn.commit()
    conn.close()