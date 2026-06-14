from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import get_db, init_db

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

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

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
    "SELECT AVG(score) FROM students").fetchone()[0] or 0

    highest_score = conn.execute(
    "SELECT MAX(score) FROM students").fetchone()[0] or 0

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

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

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

    if request.method == "POST":

        enrollment_no = request.form["enrollment_no"]
        password = request.form["password"]
        name = request.form["Student_name"]
        marks = request.form["marks"]

        if not enrollment_no or not password or not name or not marks:

            flash(
                "All fields are required!",
                "danger"
            )

            return redirect(
                url_for("add_students")
            )

        marks = int(marks)

        percentage = marks

        conn = get_db()

        roll_no = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0] + 1

        conn.execute(
            """
            INSERT INTO students
            (roll_no, enrollment_no, password, name, score, percentage, exam_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                roll_no,
                enrollment_no,
                password,
                name,
                marks,
                percentage,
                "09-06-2026"
            )
        )

        conn.commit()
        conn.close()

        flash(
            f"Student {name} added successfully!",
            "success"
        )

        return redirect(
            url_for("records")
        )

    return render_template(
        "add_students.html")
    


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
#Login route
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        enrollment_no = request.form["enrollment_no"]
        password = request.form["password"]

        conn = get_db()

        student = conn.execute(
            """
            SELECT * FROM students
            WHERE enrollment_no = ?
            AND password = ?
            """,
            (enrollment_no, password)
        ).fetchone()

        conn.close()

        if student:

            session["student_id"] = student["id"]

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(
                url_for("exam")
            )

        flash(
            "Invalid Enrollment Number or Password",
            "danger"
        )

    return render_template("login.html")

# ==========================
# START EXAM
# ==========================
@app.route("/exam")
def exam():

    if "student_id" not in session:

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
@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged Out Successfully!",
        "success"
    )

    return redirect(
        url_for("login")
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

# DELETE - Remove by Roll No
@app.route("/delete/<int:roll_no>")
def delete_student(roll_no):

    conn = get_db()

    # First check if student exists
    student = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?",
        (roll_no,)
    ).fetchone()

    if student is None:

        conn.close()

        flash(
            f"No student found with Roll No {roll_no}!",
            "danger"
        )

        return redirect(
            url_for("records")
        )

    conn.execute(
        "DELETE FROM students WHERE roll_no = ?",
        (roll_no,)
    )

    conn.commit()
    conn.close()

    flash(
        f"Student with Roll No {roll_no} deleted successfully!",
        "success"
    )

    return redirect(
        url_for("records")
    )
#search student 
@app.route("/search")
def search():
    #step-1 -get 
    q=request.args.get('q','')
    #request.args GET parameters
    #q- Form - name='q
    conn=get_db()

    if q:
        students=conn.execute(''' SELECT*FROM students
                              WHERE name LIKE ?
                              OR roll_no LIKE ?''',
                              (f'%{q}%',f'%{q}%')).fetchall()
    else:
        students=conn.execute(''' SELECT*FROM students''').fetchall()
    conn.close()
    return render_template('records.html',students=students,q=q)

#Edit student records
@app.route("/edit/<int:roll_no>", methods=["GET", "POST"])
def edit_student(roll_no):
    conn = get_db()

    if request.method == "POST":
        name = request.form["name"]
        score = request.form["score"]

        conn.execute(
            "UPDATE students SET name=?, score=? WHERE roll_no=?",
            (name, score, roll_no)
        )
        conn.commit()
        conn.close()

        flash("Student Updated Successfully!", "success")
        return redirect(url_for("records"))

    student = conn.execute(
        "SELECT * FROM students WHERE roll_no=?",
        (roll_no,)
    ).fetchone()

    conn.close()
    return render_template("edit.html", student=student)

# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)