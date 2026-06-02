from flask import Flask

app = Flask(__name__)

# project data - dictionary
stud = [
    {"name":"Shrusti", "roll": 1, "marks:": 85},
    {"name":"Pallavi", "roll": 2, "marks:": 92},
    {"name":"Shivam", "roll": 3, "marks:": 78},
    {"name":"Aarti", "roll": 4, "marks:": 65}
]

@app.route('/')
def home():
    # Create using HTML
    html = '<h1>College Portal - Students</h1>'
    html += '<ul>'
    for student in stud:
        html += f"<li>{student['name']} - Roll: {student['roll']}, Marks: {student['marks:']}</li>"
    html += '</ul>'
    return html

@app.route('/about')
def about():
    return '<h1>About Us</h1><p>This is a college management system.</p>'

@app.route('/students')
def students():
    return '<h1>Students List</h1><p>All students will show here</p>'

if __name__ == '__main__':
    app.run(debug=True)