students=["dipak","kartik","rohit","pratik","satyarth"]
print(students)
print(students[0])
print(students[1])
print(students[2])
print(students[3])
print(students[4])


#Loop -to print all the elements of the list
marks_List=[90,80,70,60,50]
for marks in marks_List:
    if marks>=90:
        print(f"Excellent!You scored {marks}")
    elif marks>=80:
        print(f"good job!You scored {marks}")
    else:
        print(f"Keep trying!You scored {marks}")


marks_List=[90,80,70,60,50]
for i in range(len(marks_List)):
    print(f"Line number{i}:")

for i in range(1,6):
    print(f"student number {i}")

#Define function
def greet(name):
    print(f"Hello, {name}! welcome to the programming world.")
greet("aarti")
greet("satyarth")
greet("pratik")
greet("rohit")
greet("kartik")

for student in students:
    greet(student)