from datetime import datetime
from http import client
from urllib import response
from dotenv import load_dotenv
from click import prompt
from flask import Flask, render_template, request, flash, redirect, url_for, session
import groq
from database import get_db, init_db
from groq import Groq
import os
load_dotenv()  # Load environment variables from .env file
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = "smart_exam_portal"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
# Create table
init_db()


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    conn = get_db()

    # Students with Subject Name (JOIN)
    students = conn.execute("""
        SELECT
            students.id,
            students.roll_number,
            students.student_name,
            students.score,
            students.percentage,
            students.exam_date,
            students.photo,
            subjects.name AS subject_name
        FROM students
        LEFT JOIN subjects
        ON students.subject_id = subjects.id
    """).fetchall()

    # Statistics
    passed_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE percentage >= 40"
    ).fetchone()[0]

    failed_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE percentage < 40"
    ).fetchone()[0]

    total_attempts = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    average_score = conn.execute(
        "SELECT AVG(score) FROM students"
    ).fetchone()[0] or 0

    highest_score = conn.execute(
        "SELECT MAX(score) FROM students"
    ).fetchone()[0] or 0

    available_exams = conn.execute(
    "SELECT COUNT(*) FROM exams WHERE status = 'active'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "home.html",
        students=students,
        passed_students=passed_students,
        failed_students=failed_students,
        total_attempts=total_attempts,
        average_score=average_score,
        highest_score=highest_score,
        available_exams=available_exams
    )
# ==========================
# RECORDS PAGE
# ==========================
@app.route("/records")
def records():

    status = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)

    # 5 students per page
    per_page = 5

    conn = get_db()

    # Base query
    query = """
    FROM students
    LEFT JOIN subjects
    ON students.subject_id = subjects.id
    """

    where_clause = ""

    if status == "pass":
        where_clause = " WHERE students.percentage >= 40"

    elif status == "fail":
        where_clause = " WHERE students.percentage < 40"

    # Total students according to filter
    total_students = conn.execute(
        "SELECT COUNT(*) " + query + where_clause
    ).fetchone()[0]

    # Calculate total pages
    total_pages = (total_students + per_page - 1) // per_page

    # Prevent invalid page numbers
    if total_pages > 0 and page > total_pages:
        page = total_pages

    if page < 1:
        page = 1

    # Calculate offset
    offset = (page - 1) * per_page

    # Student records - 5 per page
    students = conn.execute(
        """
        SELECT
            students.id,
            students.roll_number,
            students.student_name,
            students.score,
            students.percentage,
            students.exam_date,
            students.photo,
            subjects.name AS subject_name
        """
        + query +
        where_clause +
        " ORDER BY students.id ASC LIMIT ? OFFSET ?",
        (per_page, offset)
    ).fetchall()

    # Statistics
    passed_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE percentage >= 40"
    ).fetchone()[0]

    failed_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE percentage < 40"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "records.html",
        students=students,
        page=page,
        total_pages=total_pages,
        total_students=total_students,
        passed_students=passed_students,
        failed_students=failed_students,
        tip=None
    )
# student detail route
@app.route("/student/<int:student_id>")
def student_detail(student_id):

    conn = get_db()

    student = conn.execute(
        """
        SELECT
            students.id,
            students.roll_number,
            students.student_name,
            students.score,
            students.percentage,
            students.exam_date,
            students.photo,
            subjects.name AS subject_name
        FROM students
        LEFT JOIN subjects
            ON students.subject_id = subjects.id
        WHERE students.id = ?
        """,
        (student_id,)
    ).fetchone()

    conn.close()

    if student is None:
        flash("Student not found!", "danger")
        return redirect(url_for("records"))

    return render_template(
        "student_detail.html",
        student=student
    )


# ==========================
# ADD STUDENT
# ==========================
@app.route("/add", methods=["GET", "POST"])
def add_students():

    if session.get("role") != "admin":
        flash(
            "Admin only! You do not have permission to add students.",
            "danger"
        )
        return redirect(url_for("home"))

    conn = get_db()

    if request.method == "POST":

        student_name = request.form["student_name"]
        subject_id = request.form["subject_id"]
        marks = int(request.form["marks"])

        # Automatic Roll Number
        result = conn.execute(
            "SELECT MAX(roll_number) FROM students"
        ).fetchone()

        last_roll_number = result[0] if result[0] is not None else 0
        roll_number = last_roll_number + 1

        percentage = marks

        # Photo Upload
        file = request.files.get("photo")
        filename = "default.jpg"

        if file and file.filename != "" and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"

            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        conn.execute(
            """
            INSERT INTO students
            (
                roll_number,
                student_name,
                subject_id,
                score,
                percentage,
                exam_date,
                photo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                roll_number,
                student_name,
                subject_id,
                marks,
                percentage,
                "24/06/2026",
                filename
            )
        )

        conn.commit()
        conn.close()

        flash(
            f"Student {student_name} added successfully! "
            f"Roll Number: {roll_number}",
            "success"
        )

        return redirect(url_for("records"))

    subjects = conn.execute(
        "SELECT * FROM subjects ORDER BY name"
    ).fetchall()

    conn.close()

    return render_template(
        "add_students.html",
        subjects=subjects
    )
# ==========================
# MCQ QUESTIONS
# ==========================

questions = [

    {
        "question": "Python is a ____ language?",
        "options": [
            "Programming",
            "Gaming",
            "Cooking",
            "Design"
        ],
        "answer": "Programming"
    },

    {
        "question": "Which keyword is used to create a function?",
        "options": [
            "func",
            "def",
            "define",
            "function"
        ],
        "answer": "def"
    },

    {
        "question": "Flask is a ____ ?",
        "options": [
            "Database",
            "Web Framework",
            "Browser",
            "Operating System"
        ],
        "answer": "Web Framework"
    },

    {
        "question": "HTML stands for?",
        "options": [
            "Hyper Text Markup Language",
            "High Text Machine Language",
            "Hyper Transfer Markup Language",
            "None"
        ],
        "answer": "Hyper Text Markup Language"
    },

    {
        "question": "Which data type stores multiple values?",
        "options": [
            "int",
            "float",
            "list",
            "string"
        ],
        "answer": "list"
    }

]
# =========================
# Login route
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        # Login successful
        if user and check_password_hash(
            user["password"],
            password
        ):

            session["username"] = username
            session["role"] = user["role"]

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("available_exams")
            )

        # Login failed
        else:

            flash(
                "Invalid Username or Password",
                "danger"
            )

            return render_template(
                "login.html"
            )

    return render_template(
        "login.html"
    )
# ===========================
# logout route
# ==========================
@app.route("/logout")
def logout():
    session.clear()
    session.pop("username", None)
    session.pop("role", None)
    flash(
        "Logged Out Successfully!",
        "success"
    )
    return redirect(url_for("login"))
# ==========================
# Register route
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash(
                "Passwords do not match!",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        conn = get_db()

        # Check if user already exists
        existing_user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:

            flash(
                "Username already exists!",
                "danger"
            )

            conn.close()

            return redirect(
                url_for("register")
            )

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template("register.html")
# ==========================
# START EXAM
# ==========================

@app.route("/exam/<int:exam_id>")
def exam(exam_id):

    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    conn = get_db()

    # Selected exam ke questions hi fetch honge
    rows = conn.execute("""
        SELECT
            id,
            exam_id,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        FROM questions
        WHERE exam_id = ?
        ORDER BY id
    """, (exam_id,)).fetchall()

    # Selected exam ki details
    exam = conn.execute("""
        SELECT
            exams.id,
            exams.name,
            exams.duration,
            exams.exam_date,
            subjects.name AS subject_name
        FROM exams
        LEFT JOIN subjects
            ON exams.subject_id = subjects.id
        WHERE exams.id = ?
    """, (exam_id,)).fetchone()

    conn.close()

    # Exam exist nahi karta
    if exam is None:
        flash("Exam not found!", "danger")
        return redirect(url_for("available_exams"))

    # Is exam ke questions nahi hain
    if not rows:
        flash("No questions available for this exam!", "warning")
        return redirect(url_for("available_exams"))

    # Questions ko exam.html ke format me convert karo
    questions = []

    for q in rows:
        questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": [
                q["option_a"],
                q["option_b"],
                q["option_c"],
                q["option_d"]
            ],
            "correct_answer": q["correct_answer"]
        })
        session["exam_start_time"] = datetime.now().timestamp()
        session["current_exam_id"] = exam_id

    return render_template(
       "exam.html",
       questions=questions,
       exam=exam,
       exam_id=exam_id
     )

# ==========================
# EXAM INSTRUCTIONS
# ==========================

@app.route("/exam_instructions")
def exam_instructions():

    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    return render_template(
        "exam_instructions.html"
    )
# Submit exam
@app.route("/submit_exam", methods=["POST"])
def submit_exam():

    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    exam_id = request.form.get("exam_id")

    if not exam_id:
        flash("Invalid exam!", "danger")
        return redirect(url_for("available_exams"))

    from datetime import datetime

    # Calculate time taken
    start_time = session.get("exam_start_time")

    if start_time:
        time_taken_seconds = int(
            datetime.now().timestamp() - start_time
        )
    else:
        time_taken_seconds = 0

    minutes = time_taken_seconds // 60
    seconds = time_taken_seconds % 60

    time_taken = f"{minutes} min {seconds} sec"

    conn = get_db()

    # Get exam and subject
    exam = conn.execute("""
        SELECT
            exams.*,
            subjects.name AS subject_name
        FROM exams
        LEFT JOIN subjects
            ON exams.subject_id = subjects.id
        WHERE exams.id = ?
    """, (exam_id,)).fetchone()

    if not exam:
        conn.close()
        flash("Exam not found!", "danger")
        return redirect(url_for("available_exams"))

    # Get questions
    questions = conn.execute("""
        SELECT *
        FROM questions
        WHERE exam_id = ?
        ORDER BY id
    """, (exam_id,)).fetchall()

    if not questions:
        conn.close()
        flash("No questions found for this exam!", "warning")
        return redirect(url_for("available_exams"))

    # Check answers
    correct_answers = 0
    wrong_answers = 0

    for i, q in enumerate(questions):

        user_answer = request.form.get(f"q{i}")

        if user_answer == q["correct_answer"]:
            correct_answers += 1
        else:
            wrong_answers += 1

    # Calculate score
    total_questions = len(questions)
    score = correct_answers

    # Calculate percentage
    percentage = round(
        (correct_answers / total_questions) * 100,
        2
    )

    # Check pass or fail
    passing_score = exam["passing_score"] or 4

    if correct_answers >= passing_score:
        result = "Pass"
    else:
        result = "Fail"

    # Get student details
    username = session.get("username")

    student = conn.execute("""
        SELECT
            id,
            roll_number,
            student_name,
            photo
        FROM students
        WHERE username = ?
    """, (username,)).fetchone()

    student_name = username
    roll_number = None
    photo = "default.jpg"

    if student:
        student_name = student["student_name"]
        roll_number = student["roll_number"]
        photo = student["photo"] or "default.jpg"

    # Get exam date
    exam_date = datetime.now().strftime("%d/%m/%Y")

    # Save exam attempt
    conn.execute("""
        INSERT INTO exam_attempts (
            username,
            student_name,
            roll_number,
            photo,
            exam_id,
            exam_name,
            subject_id,
            subject_name,
            score,
            total_questions,
            percentage,
            exam_date,
            time_taken,
            status,
            correct_answers,
            wrong_answers
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        student_name,
        roll_number,
        photo,
        exam["id"],
        exam["name"],
        exam["subject_id"],
        exam["subject_name"],
        score,
        total_questions,
        percentage,
        exam_date,
        time_taken_seconds,
        result,
        correct_answers,
        wrong_answers
    ))

    # Get attempt ID
    attempt_id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    # Save each question answer
    for i, q in enumerate(questions):

        selected_answer = request.form.get(
            f"q{i}"
        )

        correct_answer = q["correct_answer"]

        is_correct = (
            1
            if selected_answer == correct_answer
            else 0
        )

        conn.execute("""
            INSERT INTO exam_attempt_answers (
                attempt_id,
                question_id,
                selected_answer,
                correct_answer,
                is_correct
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            attempt_id,
            q["id"],
            selected_answer,
            correct_answer,
            is_correct
        ))

    # Save database changes
    conn.commit()
    conn.close()

    # Clear exam session
    session.pop("exam_start_time", None)
    session.pop("current_exam_id", None)

    # Show exam result
    return render_template(
        "exam_results.html",
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        percentage=percentage,
        result=result,
        time_taken=time_taken,
        exam=exam,
        attempt_id=attempt_id
    )
# ==========================
# DELETE - Remove by Roll No
# ==========================
@app.route("/delete/<int:roll_number>", methods=["POST"])
def delete_student(roll_number):

    if session.get("role") != "admin":
        flash(
            "Admin only! You do not have permission to delete students.",
            "danger"
        )
        return redirect(url_for("home"))

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE roll_number = ?",
        (roll_number,)
    ).fetchone()

    if student is None:
        conn.close()

        flash(
            f"No student found with Roll No {roll_number}!",
            "danger"
        )

        return redirect(url_for("records"))

    conn.execute(
        "DELETE FROM students WHERE roll_number = ?",
        (roll_number,)
    )

    conn.commit()
    conn.close()

    flash(
        f"Student with Roll No {roll_number} deleted successfully!",
        "success"
    )

    return redirect(url_for("records"))
# ==========================
# Edit student records
# ==========================
@app.route("/edit/<int:roll_number>", methods=["GET", "POST"])
def edit_student(roll_number):

    if session.get("role") != "admin":
        flash(
            "Admin only! You do not have permission to edit students.",
            "danger"
        )
        return redirect(url_for("home"))

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE roll_number=?",
        (roll_number,)
    ).fetchone()

    if not student:
        conn.close()
        flash("Student not found!", "danger")
        return redirect(url_for("records"))

    if request.method == "POST":

        new_roll_number = request.form["roll_number"]
        student_name = request.form["student_name"]
        score = int(request.form["score"])
        percentage = float(request.form["percentage"])
        exam_date = request.form["exam_date"]
        subject_id = request.form["subject_id"]

        photo = student["photo"]

        file = request.files.get("photo")

        if file and file.filename != "" and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            photo = filename

        conn.execute(
            """
            UPDATE students
            SET
                roll_number=?,
                student_name=?,
                subject_id=?,
                score=?,
                percentage=?,
                exam_date=?,
                photo=?
            WHERE roll_number=?
            """,
            (
                new_roll_number,
                student_name,
                subject_id,
                score,
                percentage,
                exam_date,
                photo,
                roll_number
            )
        )

        conn.commit()
        conn.close()

        flash(
            "Student Updated Successfully!",
            "success"
        )

        return redirect(url_for("records"))

    subjects = conn.execute(
        "SELECT * FROM subjects ORDER BY name"
    ).fetchall()

    conn.close()

    return render_template(
        "edit.html",
        student=student,
        subjects=subjects
    )
# ==========================
# search student
# ==========================

@app.route("/search")
def search():

    q = request.args.get("q", "")

    conn = get_db()

    if q:

        students = conn.execute("""
            SELECT
                students.id,
                students.roll_number,
                students.student_name,
                students.score,
                students.percentage,
                students.exam_date,
                students.photo,
                subjects.name AS subject_name
            FROM students
            LEFT JOIN subjects
            ON students.subject_id = subjects.id
            WHERE students.student_name LIKE ?
            OR CAST(students.roll_number AS TEXT) LIKE ?
        """, (f"%{q}%", f"%{q}%")).fetchall()

    else:

        students = conn.execute("""
            SELECT
                students.id,
                students.roll_number,
                students.student_name,
                students.score,
                students.percentage,
                students.exam_date,
                subjects.name AS subject_name
            FROM students
            LEFT JOIN subjects
            ON students.subject_id = subjects.id
        """).fetchall()

    conn.close()

    return render_template(
        "search.html",
        students=students,
        query=q
    )
# ==========================
# subject route
# ==========================
@app.route('/subjects')
def subjects():
    conn=get_db()
    rows=conn.execute('''
                      SELECT subjects_name
                      FROM subjects
                      ''').fetchall()

#  Al tip route
@app.route('/students/<int:id>/tip')
def get_ai_tip(id):
    conn = get_db()

    # Selected student with subject name
    student = conn.execute("""
        SELECT
            students.id,
            students.student_name,
            students.score,
            students.photo,
            subjects.name AS subject_name
        FROM students
        LEFT JOIN subjects
            ON students.subject_id = subjects.id
        WHERE students.id = ?
    """, (id,)).fetchone()

    if student is None:
        conn.close()
        flash(f"No student found with ID {id}!", "danger")
        return redirect(url_for("records"))

    # Personalized AI prompt
    prompt = f"""
You are a friendly and helpful study mentor.

Student Name: {student['student_name']}
Score: {student['score']}
Subject: {student['subject_name']}

Give personalized study tips specifically for {student['student_name']}.
Mention the student's name in the advice.
Consider the student's score and subject.
Keep the advice simple, practical, encouraging, and easy to follow.
Give a complete study tip in 2 short sentences. Do not stop mid-sentence.
"""

    # Create Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Generate AI response
    response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.6,
    max_completion_tokens=300,
    include_reasoning=False
)

    tip = response.choices[0].message.content.strip()
    print("AI RESPONSE:", repr(response.choices[0].message.content))
    print("AI TIP:", repr(tip))


    # Pagination
    page = 1
    per_page = 5

    # Total students
    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_pages = (total_students + per_page - 1) // per_page

    # First page students
    students = conn.execute("""
        SELECT
            students.id,
            students.roll_number,
            students.student_name,
            students.score,
            students.percentage,
            students.exam_date,
            students.photo,
            subjects.name AS subject_name
        FROM students
        LEFT JOIN subjects
            ON students.subject_id = subjects.id
        LIMIT ? OFFSET ?
    """, (per_page, 0)).fetchall()

    # Statistics
    passed_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE percentage >= 40"
    ).fetchone()[0]

    failed_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE percentage < 40"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "records.html",
        students=students,
        page=page,
        total_pages=total_pages,
        total_students=total_students,
        passed_students=passed_students,
        failed_students=failed_students,
        tip=tip
    )
#create exam route
@app.route("/create_exam", methods=["GET", "POST"])
def create_exam():

    if session.get("role") != "admin":
        flash("Admin only!", "danger")
        return redirect(url_for("home"))

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        subject_id = request.form["subject_id"]
        duration = request.form["duration"]
        exam_date = request.form["exam_date"]

        try:
            cursor = conn.execute("""
                INSERT INTO exams
                (name, subject_id, duration, exam_date)
                VALUES (?, ?, ?, ?)
            """, (name, subject_id, duration, exam_date))

            exam_id = cursor.lastrowid

            conn.commit()
            conn.close()

            flash("Exam created successfully!", "success")

            return redirect(
                url_for("add_question", exam_id=exam_id)
            )

        except sqlite3.IntegrityError:
            conn.close()

            flash(
                "Exam with this name already exists!",
                "warning"
            )

            return redirect(
                url_for("create_exam")
            )

    subjects = conn.execute(
        "SELECT * FROM subjects ORDER BY name"
    ).fetchall()

    conn.close()

    return render_template(
        "create_exam.html",
        subjects=subjects
    )
# ==========================
# EDIT EXAM
# ==========================

@app.route("/edit_exam/<int:exam_id>", methods=["GET", "POST"])
def edit_exam(exam_id):

    if session.get("role") != "admin":
        flash("Admin only!", "danger")
        return redirect(url_for("home"))

    conn = get_db()

    exam = conn.execute("""
        SELECT *
        FROM exams
        WHERE id = ?
    """, (exam_id,)).fetchone()

    if not exam:
        conn.close()
        flash("Exam not found!", "danger")
        return redirect(url_for("available_exams"))

    subjects = conn.execute("""
        SELECT *
        FROM subjects
        ORDER BY name
    """).fetchall()

    if request.method == "POST":

        name = request.form["name"]
        subject_id = request.form["subject_id"]
        duration = request.form["duration"]
        exam_date = request.form["exam_date"]
        status = request.form["status"]

        conn.execute("""
            UPDATE exams
            SET name = ?,
                subject_id = ?,
                duration = ?,
                exam_date = ?,
                status = ?
            WHERE id = ?
        """, (
            name,
            subject_id,
            duration,
            exam_date,
            status,
            exam_id
        ))

        conn.commit()
        conn.close()

        flash("Exam updated successfully!", "success")
        return redirect(url_for("available_exams"))

    conn.close()

    return render_template(
        "edit_exam.html",
        exam=exam,
        subjects=subjects
    )


# ==========================
# DELETE EXAM
# ==========================

@app.route("/delete_exam/<int:exam_id>", methods=["POST", "GET"])
def delete_exam(exam_id):

    if session.get("role") != "admin":
        flash("Admin only!", "danger")
        return redirect(url_for("home"))

    conn = get_db()

    # Delete questions belonging to this exam first
    conn.execute("""
        DELETE FROM questions
        WHERE exam_id = ?
    """, (exam_id,))

    # Delete exam
    cursor = conn.execute("""
        DELETE FROM exams
        WHERE id = ?
    """, (exam_id,))

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        flash("Exam not found!", "danger")
    else:
        flash("Exam deleted successfully!", "success")

    return redirect(url_for("available_exams"))
#available exams route
@app.route("/available_exams")
def available_exams():

    if not session.get("username"):
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    conn = get_db()

    exams = conn.execute("""
        SELECT
            exams.*,
            subjects.name AS subject_name
        FROM exams
        LEFT JOIN subjects
            ON exams.subject_id = subjects.id
        ORDER BY
            CASE
                -- Python
                WHEN exams.name = '🐍 Python Programming Basics' THEN 1
                WHEN exams.name = '🐍 Python Advanced Concepts' THEN 2

                -- HTML
                WHEN exams.name = '🌐 HTML Fundamentals' THEN 3
                WHEN exams.name = '🌐 HTML Forms & Web Structure' THEN 4

                -- Java
                WHEN exams.name = '☕ Java Programming Basics' THEN 5
                WHEN exams.name = '☕ Java OOP & Advanced' THEN 6

                -- CSS
                WHEN exams.name = '🎨 CSS Fundamentals' THEN 7
                WHEN exams.name = '🎨 CSS Advanced Styling' THEN 8

                -- SQL
                WHEN exams.name = '🗄️ SQL & Database Basics' THEN 9
                WHEN exams.name = '🗄️ SQL Queries & Advanced Database' THEN 10

                -- Any new exam
                ELSE 999
            END,
            exams.id ASC
    """).fetchall()

    print("AVAILABLE EXAMS:", [dict(exam) for exam in exams])

    conn.close()

    return render_template(
        "available_exams.html",
        exams=exams
    )
# add_questions route
@app.route("/add_question/<int:exam_id>", methods=["GET", "POST"])
def add_question(exam_id):

    if session.get("role") != "admin":
        flash("Admin only!", "danger")
        return redirect(url_for("home"))

    conn = get_db()

    exam = conn.execute(
        "SELECT * FROM exams WHERE id = ?",
        (exam_id,)
    ).fetchone()

    if not exam:
        conn.close()
        flash("Exam not found!", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":

        question = request.form["question"]
        option_a = request.form["option_a"]
        option_b = request.form["option_b"]
        option_c = request.form["option_c"]
        option_d = request.form["option_d"]
        correct_answer = request.form["correct_answer"]

        conn.execute("""
            INSERT INTO questions
            (exam_id, question, option_a, option_b,
             option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            exam_id,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        ))

        conn.commit()

        flash("Question added successfully!", "success")

    questions = conn.execute("""
        SELECT *
        FROM questions
        WHERE exam_id = ?
        ORDER BY id
    """, (exam_id,)).fetchall()

    conn.close()

    return render_template(
        "add_question.html",
        exam=exam,
        questions=questions
    )
# Review exam answers
@app.route("/review_answers/<int:attempt_id>")
def review_answers(attempt_id):

    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    conn = get_db()

    # Get attempt details
    attempt = conn.execute("""
        SELECT *
        FROM exam_attempts
        WHERE id = ? AND username = ?
    """, (attempt_id, session["username"])).fetchone()

    if not attempt:
        conn.close()
        flash("Exam attempt not found!", "danger")
        return redirect(url_for("available_exams"))

    # Get submitted answers
    answers = conn.execute("""
        SELECT
            eaa.question_id,
            eaa.selected_answer,
            eaa.correct_answer,
            eaa.is_correct,
            q.question,
            q.option_a,
            q.option_b,
            q.option_c,
            q.option_d
        FROM exam_attempt_answers eaa
        JOIN questions q
            ON eaa.question_id = q.id
        WHERE eaa.attempt_id = ?
        ORDER BY q.id
    """, (attempt_id,)).fetchall()

    conn.close()

    return render_template(
        "review_answers.html",
        attempt=attempt,
        answers=answers
    )

# ==========================
# RUN APP
# ==========================
init_db()

if __name__ == "__main__":
    app.run(debug=True)