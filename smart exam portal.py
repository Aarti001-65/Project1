# ==========================================
# SMART EXAM PORTAL
# (Online Tests, MCQs, Scores & Results)
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

# Function to conduct exam
def start_exam():
    score = 0

    print("\n===================================")
    print("      SMART EXAM PORTAL ")
    print("===================================")

    name = input("Enter Student Name: ")

    for i, q in enumerate(questions, start=1):
        print("\n-----------------------------------")
        print("Question", i)
        print(q["question"])

        for j, option in enumerate(q["options"], start=1):
            print(j, ".", option)

        choice = int(input("Enter Your Choice (1-4): "))

        if choice == q["answer"]:
            print(" Correct Answer")
            score += 1
        else:
            print(" Wrong Answer")

    return name, score

# Function to show result
def show_result(name, score):
    total = len(questions)
    percentage = (score / total) * 100

    print("\n===================================")
    print("           EXAM RESULT")
    print("===================================")
    print("Student Name :", name)
    print("Total Questions :", total)
    print("Correct Answers :", score)
    print("Percentage :", round(percentage, 2), "%")

    if percentage >= 80:
        print("Grade : A+")
    elif percentage >= 60:
        print("Grade : A")
    elif percentage >= 40:
        print("Grade : B")
    else:
        print("Grade : C")

    if percentage >= 40:
        print(" RESULT : PASS")
    else:
        print(" RESULT : FAIL")

# Main Program
student_name, marks = start_exam()
show_result(student_name, marks)