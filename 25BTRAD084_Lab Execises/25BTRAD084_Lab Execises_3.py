# Lab Exercise 8: Contact Book Using Lists and Dictionaries

contacts = []


def add_contact():
  name = input("Enter name: ").strip()
  phone = input("Enter phone number: ").strip()
  email = input("Enter email: ").strip()
  contact = {"Name": name, "Phone": phone, "Email": email}
  contacts.append(contact)
  print("Contact added successfully!")


def search_contact():
  name = input("Enter name to search: ").strip()
  for contact in contacts:
    if contact["Name"].lower() == name.lower():
      print("Contact found:", contact)
      return
  print("Contact not found.")


def update_contact():
  name = input("Enter name to update: ").strip()
  for contact in contacts:
    if contact["Name"].lower() == name.lower():
      contact["Phone"] = input("Enter new phone number: ").strip()
      contact["Email"] = input("Enter new email: ").strip()
      print("Contact updated successfully!")
      return
  print("Contact not found.")


def delete_contact():
  name = input("Enter name to delete: ").strip()
  for contact in contacts:
    if contact["Name"].lower() == name.lower():
      contacts.remove(contact)
      print("Contact deleted successfully!")
      return
  print("Contact not found.")


def display_contacts():
  if not contacts:
    print("No contacts available.")
    return
  print("\n--- CONTACT LIST ---")
  for contact in contacts:
    print(contact)


while True:
  print("\n===== CONTACT BOOK =====")
  print("1. Add Contact")
  print("2. Search Contact")
  print("3. Update Contact")
  print("4. Delete Contact")
  print("5. Display Contacts")
  print("6. Exit")

  choice = input("Enter your choice: ")

  if choice == "1":
    add_contact()
  elif choice == "2":
    search_contact()
  elif choice == "3":
    update_contact()
  elif choice == "4":
    delete_contact()
  elif choice == "5":
    display_contacts()
  elif choice == "6":
    print("Thank you!")
    break
  else:
    print("Invalid choice!")

# Lab Exercise 9: Student Grading System

students = {}


def calculate_grade(mark):
  if mark >= 90:
    return "A+"
  elif mark >= 80:
    return "A"
  elif mark >= 70:
    return "B"
  elif mark >= 60:
    return "C"
  elif mark >= 50:
    return "D"
  else:
    return "Fail"


number = int(input("Enter number of students: "))
for i in range(number):
  name = input("\nEnter student name: ").strip()
  mark = float(input("Enter student mark: "))
  if 0 <= mark <= 100:
    students[name] = mark
  else:
    print("Invalid mark! Enter a value from 0 to 100.")

print("\n===== STUDENT RESULTS =====")
for name, mark in students.items():
  print("\nStudent Name:", name)
  print("Mark:", mark)
  print("Grade:", calculate_grade(mark))

# Lab Exercise 10: Frequency Counter Using Dictionaries

sentence = input("Enter a sentence: ")
words = sentence.lower().split()
frequency = {}

for word in words:
  word = word.strip(".,!?;:")
  if word:
    if word in frequency:
      frequency[word] += 1
    else:
      frequency[word] = 1

print("\n===== WORD FREQUENCY =====")
for word, count in frequency.items():
  print(word, ":", count)

print("\nTotal words:", sum(frequency.values()))

