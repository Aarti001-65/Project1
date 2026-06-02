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

# Second Dictionary
student = {
    "roll_no": 0,
    "name": "",
    "score": 0,
    "percentage": 0,
    "exam_date": ""
}

def get_status(percentage):
    if percentage >= 40:
        return "PASS"
    else:
        return "FAIL"

def start_exam():
    score = 0

    print("\n===== SMART EXAM PORTAL =====")

    # Student Details
    student["roll_no"] = int(input("Enter Roll No: "))
    student["name"] = input("Enter Student Name: ")
    student["exam_date"] = input("Enter Exam Date (DD-MM-YYYY): ")

    question_no = 1

    for q in questions:
        print("\nQuestion", question_no)
        print(q["question"])

        option_no = 1
        for option in q["options"]:
            print(option_no, ".", option)
            option_no += 1

        choice = int(input("Enter Your Choice (1-4): "))

        if choice == q["answer"]:
            print("Correct Answer")
            score += 1
        else:
            print("Wrong Answer")
            print("Correct Answer is:",
                  q["options"][q["answer"] - 1])

        question_no += 1

    student["score"] = score

def show_result():
    total = len(questions)

    student["percentage"] = round(
        (student["score"] / total) * 100, 2
    )

    print("\n===== EXAM RESULT =====")
    print("Roll No :", student["roll_no"])
    print("Student Name :", student["name"])
    print("Exam Date :", student["exam_date"])
    print("Total Questions :", total)
    print("Correct Answers :", student["score"])
    print("Percentage :", student["percentage"], "%")
    print("Status :", get_status(student["percentage"]))

start_exam()
show_result()