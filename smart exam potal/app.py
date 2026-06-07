from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "smart_exam_portal"

students = [
    {
        "roll_no": 101,
        "name": "Rahul",
        "score": 2,
        "percentage": 66.67,
        "exam_date": "03-06-2026"
    },
    {
        "roll_no": 102,
        "name": "Priya",
        "score": 3,
        "percentage": 100,
        "exam_date": "03-06-2026"
    },
    {
        "roll_no": 103,
        "name": "Amit",
        "score": 1,
        "percentage": 33.33,
        "exam_date": "03-06-2026"
    }
]

# Home Page
@app.route("/")
def home():
    return render_template("home.html", students=students)

# Records Page
@app.route("/records")
def records():
    return render_template("records.html", students=students)

# Add Student Page
@app.route("/add", methods=["GET", "POST"])
def add_students():

    if request.method == "POST":

        name = request.form["Student_name"]
        marks = request.form["marks"]

        # Validation
        if not name or not marks:
            flash("All fields are required!", "danger")
            return redirect(url_for("add_students"))

        marks = int(marks)

        new_student = {
            "roll_no": len(students) + 101,
            "name": name,
            "score": marks,
            "percentage": round((marks / 3) * 100, 2),
            "exam_date": "07-06-2026"
        }

        students.append(new_student)

        flash(f"Student {name} added successfully!", "success")

        return redirect(url_for("records"))

    return render_template("add_students.html")


if __name__ == "__main__":
    app.run(debug=True)