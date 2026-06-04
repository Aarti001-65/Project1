from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)