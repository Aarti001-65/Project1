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
    enrollment_no TEXT UNIQUE,
    password TEXT,
    name TEXT,
    score INTEGER,
    percentage REAL,
    exam_date TEXT
)
""")

    conn.commit()
    conn.close()