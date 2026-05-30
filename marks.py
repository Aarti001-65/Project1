java=int(input("Enter java mark's:"))
python=int(input("Enter python mark's:"))
math=int(input("Enter Math mark's:"))
eng=int(input("Enter English mark's:"))
che=int(input("Enter chemistry mark's:"))
total=(java+python+math+eng+che)
per=(total/5)
print("****************************************************")
print("****************************************************")
name=input("Enter student name:")
rollno=input("Enter student roll no.:")
print("java mark's:",java)
print("python mark's:",python)
print("math mark's:",math)
print("English mark's:",eng)
print("chemistry mark's:",che)
print("Total marks:",total)
print("percentage:",per)
print("****************************************************")
print("****************************************************")


if(per>=75):
    print("Distinction")
elif(per>=60):
    print("First class")
elif(per>=45):
    print("pass only")
else:
    print("Fail")







