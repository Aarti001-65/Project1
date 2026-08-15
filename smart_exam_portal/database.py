import os
import sqlite3

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "myproject.db")


# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database
def init_db():
    conn = get_db()

    # Subjects table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Students table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number INTEGER,
            student_name TEXT NOT NULL,
            subject_id INTEGER,
            score INTEGER,
            percentage REAL,
            exam_date TEXT,
            photo TEXT DEFAULT 'default.jpg',
            username TEXT,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    # Student columns
    student_columns = [
        ("subject_id", "INTEGER"),
        ("score", "INTEGER"),
        ("percentage", "REAL"),
        ("exam_date", "TEXT"),
        ("photo", "TEXT DEFAULT 'default.jpg'"),
        ("username", "TEXT")
    ]

    for column, definition in student_columns:
        try:
            conn.execute(
                f"ALTER TABLE students ADD COLUMN {column} {definition}"
            )
        except sqlite3.OperationalError:
            pass

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student'
        )
    """)

    # User role column
    try:
        conn.execute(
            "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'"
        )
    except sqlite3.OperationalError:
        pass

    # Exams table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            subject_id INTEGER,
            duration INTEGER DEFAULT 30,
            total_questions INTEGER DEFAULT 0,
            exam_date TEXT,
            status TEXT DEFAULT 'active',
            passing_score INTEGER DEFAULT 4,
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    # Exam columns
    exam_columns = [
        ("subject_id", "INTEGER"),
        ("duration", "INTEGER DEFAULT 30"),
        ("total_questions", "INTEGER DEFAULT 0"),
        ("exam_date", "TEXT"),
        ("status", "TEXT DEFAULT 'active'"),
        ("passing_score", "INTEGER DEFAULT 4")
    ]

    for column, definition in exam_columns:
        try:
            conn.execute(
                f"ALTER TABLE exams ADD COLUMN {column} {definition}"
            )
        except sqlite3.OperationalError:
            pass

    # Questions table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY(exam_id) REFERENCES exams(id)
        )
    """)

    # Exam attempts table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exam_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            student_name TEXT,
            roll_number INTEGER,
            photo TEXT DEFAULT 'default.jpg',
            exam_id INTEGER,
            exam_name TEXT,
            subject_id INTEGER,
            subject_name TEXT,
            score INTEGER,
            total_questions INTEGER,
            percentage REAL,
            exam_date TEXT,
            time_taken INTEGER,
            status TEXT,
            correct_answers INTEGER DEFAULT 0,
            wrong_answers INTEGER DEFAULT 0
        )
    """)

    # Exam attempt columns
    attempt_columns = [
        ("username", "TEXT"),
        ("student_name", "TEXT"),
        ("roll_number", "INTEGER"),
        ("photo", "TEXT DEFAULT 'default.jpg'"),
        ("exam_id", "INTEGER"),
        ("exam_name", "TEXT"),
        ("subject_id", "INTEGER"),
        ("subject_name", "TEXT"),
        ("score", "INTEGER"),
        ("total_questions", "INTEGER"),
        ("percentage", "REAL"),
        ("exam_date", "TEXT"),
        ("time_taken", "INTEGER"),
        ("status", "TEXT"),
        ("correct_answers", "INTEGER DEFAULT 0"),
        ("wrong_answers", "INTEGER DEFAULT 0")
    ]

    for column, definition in attempt_columns:
        try:
            conn.execute(
                f"ALTER TABLE exam_attempts ADD COLUMN {column} {definition}"
            )
        except sqlite3.OperationalError:
            pass

    # Exam attempt answers table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exam_attempt_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER,
            question_id INTEGER,
            selected_answer TEXT,
            correct_answer TEXT,
            is_correct INTEGER DEFAULT 0,
            FOREIGN KEY(attempt_id) REFERENCES exam_attempts(id),
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    """)

    # Default subjects
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

    # Update total questions for every exam
    conn.execute("""
        UPDATE exams
        SET total_questions = (
            SELECT COUNT(*)
            FROM questions
            WHERE questions.exam_id = exams.id
        )
    """)

    # Set default passing score
    conn.execute("""
        UPDATE exams
        SET passing_score = 4
        WHERE passing_score IS NULL
    """)

    # Save changes
    conn.commit()
    conn.close()