import sqlite3


def get_db():
    conn = sqlite3.connect("myproject.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    # ==========================
    # SUBJECTS TABLE
    # ==========================
    conn.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # ==========================
    # STUDENTS TABLE
    # ==========================
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_number INTEGER,
        student_name TEXT NOT NULL,
        subject_id INTEGER,
        score INTEGER,
        percentage REAL,
        exam_date TEXT,
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )
    """)

    # Add subject_id column if old database exists
    try:
        conn.execute("ALTER TABLE students ADD COLUMN subject_id INTEGER")
    except sqlite3.OperationalError:
        pass

    # ==========================
    # USERS TABLE
    # ==========================
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'student'
    )
    """)

    try:
        conn.execute("""
        ALTER TABLE users
        ADD COLUMN role TEXT DEFAULT 'student'
        """)
    except sqlite3.OperationalError:
        pass

    # ==========================
    # EXAMS TABLE
    # ==========================
    conn.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # ==========================
    # DEFAULT SUBJECTS
    # ==========================
    default_subjects = [
        "Python",
        "Java",
        "SQL",
        "HTML",
        "CSS"
    ]

    for subject in default_subjects:
        try:
            conn.execute(
                "INSERT INTO subjects (name) VALUES (?)",
                (subject,)
            )
        except sqlite3.IntegrityError:
            pass

    # ==========================
    # UPDATE OLD STUDENTS
    # ==========================
    try:
        conn.execute("""
        UPDATE students
        SET subject_id = (
            SELECT id
            FROM subjects
            WHERE LOWER(subjects.name) = LOWER(students.subject_name)
        )
        WHERE subject_id IS NULL
        """)
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()