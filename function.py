def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
    students=["Dipak","kartik","rohit","pratik","satyarth"]
    marks_List=[90,80,70,60,50]
    for i in range(len(students)):
        grade = get_grade(marks_List[i])
        print(f"{students[i]} scored {marks_List[i]} and received grade {grade}.")