from flask import Flask, render_template
app = Flask(__name__)
stud = [
    {"name":"aarti","roll no":1,"marks":85},
    {"name":"priya","roll no":2,"marks":90},
    {"name":"riya","roll no":3,"marks":88}
]

@app.route("/")
def home():
    return  render_template('home.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/students")
def students_list():
    return render_template('students.html', students=stud)


if __name__ == "__main__":
    print("Inside main ")
    app.run(debug=True)