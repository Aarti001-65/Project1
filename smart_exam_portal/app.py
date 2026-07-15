from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import get_db, init_db
from groq import Groq
import os
from werkzeug.security import generate_password_hash, check_password_hash   

app = Flask(__name__)
app.secret_key = "smart_exam_portal"

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

    conn.close()

    return render_template(
        "home.html",
        students=students,
        passed_students=passed_students,
        failed_students=failed_students,
        total_attempts=total_attempts,
        average_score=average_score,
        highest_score=highest_score
    )


# ==========================
# RECORDS PAGE
# ==========================

@app.route("/records")
def records():

    status = request.args.get("status", "")

    conn = get_db()

    if status == "pass":

     students = conn.execute("""
      SELECT
        students.roll_number,
        students.student_name,
        students.score,
        students.percentage,
        students.exam_date,
        subjects.name AS subject_name
    FROM students
    LEFT JOIN subjects
        ON students.subject_id = subjects.id
    WHERE students.percentage >= 40
    """).fetchall()

    elif status == "fail":

      students = conn.execute("""
    SELECT
        students.roll_number,
        students.student_name,
        students.score,
        students.percentage,
        students.exam_date,
        subjects.name AS subject_name
    FROM students
    LEFT JOIN subjects
        ON students.subject_id = subjects.id
    WHERE students.percentage < 40
    """).fetchall()
    else:

        students = conn.execute("""
SELECT
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
        "records.html",
        students=students
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
        marks = request.form["marks"]

        if not student_name or not subject_id or not marks:

            flash(
                "All fields are required!",
                "danger"
            )

            conn.close()

            return redirect(url_for("add_students"))

        marks = int(marks)
        percentage = marks

        # Auto Generate Roll Number
        roll_number = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0] + 1

        conn.execute(
            """
            INSERT INTO students
            (
                roll_number,
                student_name,
                subject_id,
                score,
                percentage,
                exam_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                roll_number,
                student_name,
                subject_id,
                marks,
                percentage,
                "24/06/2026"
            )
        )

        conn.commit()

        flash(
            f"Student {student_name} added successfully!",
            "success"
        )

        conn.close()

        return redirect(url_for("records"))

    # Load Subjects for Dropdown
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

        users = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if users and check_password_hash(users["password"], password):

            session["username"] = username
            session["role"] = users["role"]
            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("exam")
            )
        else:
            flash(
            "Invalid Username or Password",
            "danger"
        )

    return render_template("login.html")
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
@app.route("/exam")
def exam():

    if "username" not in session:

        flash(
            "Please login first!",
            "warning"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "exam.html",
        questions=questions
    )
@app.route("/exam_instructions")
def exam_instructions():

    if "username" not in session:

        flash(
            "Please login first!",
            "warning"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "exam_instructions.html"
    )

# ==========================
# SUBMIT EXAM
# ==========================

@app.route("/submit_exam", methods=["POST"])
def submit_exam():

    score = 0

    for i, q in enumerate(questions):

        user_answer = request.form.get(
            f"q{i}"
        )

        if user_answer == q["answer"]:
            score += 1

    percentage = round(
        (score / len(questions)) * 100,
        2
    )

    if percentage >= 40:
        result = "Pass"
    else:
        result = "Fail"

    return render_template(
        "result.html",
        score=score,
        percentage=percentage,
        result=result
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

    if request.method == "POST":

        student_name = request.form["student_name"]
        score = int(request.form["score"])

        percentage = score

        conn.execute(
            """
            UPDATE students
            SET student_name = ?, score = ?, percentage = ?
            WHERE roll_number = ?
            """,
            (
                student_name,
                score,
                percentage,
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

    student = conn.execute(
        "SELECT * FROM students WHERE roll_number = ?",
        (roll_number,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit.html",
        student=student
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
@app.route('/students/<int:id>/tip')
def get_ai_tip(id):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()

    if student is None:
        flash(
            f"No student found with ID {id}!",
            "danger"
        )
        return redirect(url_for("records"))

    prompt=f"""
     name: {student['name']}
    score: {student['score']}
    student subject: {student['subject_id']}
    Please provide practical study tips,In Simple and encouraging tone.It should not be more than 2 lines.
    """
    client=Groq(api_key=os.environ.get("GROQ_API_KEY",""))

    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )

    tip=response.choices[0].message.content
    return render_template(
        "records.html",
        student=student,
        tip=tip
    )
# ==========================
# RUN APP
# ==========================
init_db()
if __name__ == "__main__":
    app.run(debug=True)