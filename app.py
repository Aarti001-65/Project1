from flask import Flask
app = Flask(__name__)
stud = [
    {"name":"aarti","roll no":1,"marks":85},
    {"name":"priya","roll no":2,"marks":90},
    {"name":"riya","roll no":3,"marks":88}
]

@app.route("/")
def home():
    return '<h1>Welcome to My project</h1>'
@app.route("/about")
def about():
    return '<h1>about us</h1><p>This is a college management system.</p>'
@app.route("/students")
def students_list():
    html = '<h1>Students List</h1><ul>'
    for student in students:
        html += f"<li>{student['name']} - Roll No: {student['roll no']} - Marks: {student['marks']}</li>"
    html += '</ul>'
    return html

if __name__ == "__main__":
    app.run(debug=True)