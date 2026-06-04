from flask import Flask
app = Flask(__name__)
# ==========================================
# SMART EXAM PORTAL
# ==========================================
questions = [
    {
        "question": "Python is a __ language?",
        "options": ["Programming", "Gaming", "Cooking", "Design"],
        "answer": 1
    },
    {
        "question": "Which keyword is used to create a function?",
        "options": ["func", "def", "define", "function"],
        "answer": 2
    },
    {
        "question": "Which data type stores multiple values?",
        "options": ["int", "float", "list", "char"],
        "answer": 3
    }
]

student = {
    "roll_no": 101,
    "name": "Rahul",
    "score": 2,
    "percentage": 66.67,
    "exam_date": "03-06-2026"
}

def get_status(percentage):
    if percentage >= 40:
        return "PASS"
    else:
        return "FAIL"


# Route 1 : Home Page
@app.route("/")
def home():
    return """
    <h1>SMART EXAM PORTAL</h1>
    <p>This project is used to conduct exams and display student results.</p>

    <a href="/records">View Student Record</a><br><br>

    <a href="/questions">View Questions</a>
    """
# Route 2 : Records Page
@app.route("/records")
def records():
    return f"""
    <h1>Student Record</h1>

    <p><b>Roll No:</b> {student['roll_no']}</p>
    <p><b>Name:</b> {student['name']}</p>
    <p><b>Score:</b> {student['score']}</p>
    <p><b>Percentage:</b> {student['percentage']}%</p>
    <p><b>Exam Date:</b> {student['exam_date']}</p>
    <p><b>Status:</b> {get_status(student['percentage'])}</p>
    """
# Route 3 : Questions Page (Extra Route)
@app.route("/questions")
def show_questions():

    output = "<h1>Exam Questions</h1>"

    q_no = 1

    for q in questions:
        output += f"<h3>Question {q_no}: {q['question']}</h3>"

        for option in q["options"]:
            output += f"<li>{option}</li>"

        q_no += 1

    return output

if __name__ == "__main__":
    app.run(debug=True)