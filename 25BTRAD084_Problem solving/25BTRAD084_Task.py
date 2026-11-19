# Task 1: Print Name, Department and College
print("Jane Doe")
print("Computer Science")
print("Tech University")
#output
Jane Doe
Computer Science
Tech University

# Task 2: Print Star Pattern
for i in range(3):
    for j in range(7):
        print("*", end="")
    print()
#output
*******
*******
*******

# Task 3: Print Python is Easy
print("Python is Easy")
#output
Python is Easy

# Task 4: Print Number Pyramid
pattern = ""
for i in range(1, 6):
    pattern += str(i)
    print(pattern)
#output
1
12
123
1234
12345

# Task 5: Use New Line (\n)
print("Computer\nScience\nEngineering")
#output
Computer
Science
Engineering

# Task 6: Use Tab Space (\t)
print("Name\tAge\tCity")
#output
Name    Age    City

# Task 7: Single Line Comment
# Program to calculate area of rectangle
length = 5
width = 10
print("Area:", length * width)
#output
Area: 50

# Task 8: Multi-Line Comment
"""
This program calculates the sum
of two numbers.
"""
a = 10
b = 20
print("Sum:", a + b)
#output
Sum: 30

# Task 9: Three Comments and Three Print Statements
# Display greeting
print("Hello!")
#output
Hello!
Learning Python basics.
Goodbye!

# Display status
print("Learning Python basics.")
#output
Learning Python basics.

# Display farewell
print("Goodbye!")
#output
Goodbye!

# Task 10: Create and Print Name Variable
name = "Alex"
print(name)
#output
Alex

# Task 11: Store and Print Three Numbers
a = 10
b = 20
c = 30

print(a)
print(b)
print(c)
#output
10
20
30

#Convert the string "100" into an integer and display its value and data type. 
value = "100" 
number = int(value)  
print(number) 
print(type(number)) 
#output
100 
<class 'int'> 

#Convert the integer 25 into a float and display the result and its type. 
number = 25
result = float(number)

print(result)
print(type(result))
#output
25.0
<class 'float'>

#Accept the user's age using input(), convert it to an integer, and display the age. 
age = int(input("Enter your age: ")) 
print("Age:", age) 
#output
Enter your age: 20 
Age: 20 

#Accept two numbers from the user, convert them to integers, and display their sum. 
num1 = int(input("Enter first number: ")) 
num2 = int(input("Enter second number: ")) 
print("Sum:", num1 + num2) 
#output
Enter first number: 10 
Enter second number: 20 
Sum: 30 

#Using an f-string, accept a student's name, age, and CGPA and display the required sentence. 
name = input("Enter student name: ") 
age = int(input("Enter age: ")) 
cgpa = float(input("Enter CGPA: ")) 
print(f"My name is {name}. I am {age} years old and my CGPA is {cgpa}.") 
#output
Enter student name: Rahul Enter age: 20 
Enter CGPA: 8.5 My name is Rahul.
I am 20 years old and my CGPA is 8.5. 

#Accept temperature in Celsius and convert it into Fahrenheit. Display the result using an fstring with two decimal places. 
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = (celsius * 9 / 5) + 32 
print(f"Temperature in Fahrenheit: {fahrenheit:.2f}") 
#output
Enter temperature in Celsius: 25 
Temperature in Fahrenheit: 77.00 

#Accept an integer and determine whether it is even or odd using the % operator. 
number = int(input("Enter number: ")) 
if number % 2 == 0: 
  print(f"{number} is Even") 
else: 
  print(f"{number} is Odd") 
#output
Enter number: 25
25 is Odd 
