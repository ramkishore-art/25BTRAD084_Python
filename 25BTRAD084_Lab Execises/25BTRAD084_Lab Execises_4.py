# Lab Exercise 11: Log File Reader Program


def read_log_file(filename):
  counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
  try:
    with open(filename, "r", encoding="utf-8") as file:
      for line in file:
        for keyword in counts:
          if keyword in line.upper():
            counts[keyword] += 1
            break
    if not any(counts.values()):
      print("The file is empty or contains no recognized log entries.")
    else:
      print("\n===== LOG SUMMARY =====")
      for keyword, total in counts.items():
        print(f"{keyword}: {total}")
  except FileNotFoundError:
    print("Error: Log file not found.")
  except OSError as error:
    print("Unable to read the file:", error)


if __name__ == "__main__":
  file_name = input("Enter log file name: ").strip()
  read_log_file(file_name)

# Lab Exercise 12: Student Data Manager Using Files
# Student records are stored in a JSON file.
import json
import os

FILE_NAME = "students.json"


def load_students():
  if not os.path.exists(FILE_NAME):
    return []
  try:
    with open(FILE_NAME, "r", encoding="utf-8") as file:
      data = json.load(file)
      return data if isinstance(data, list) else []
  except (json.JSONDecodeError, OSError):
    print("Could not read student data. Starting with an empty list.")
    return []


def save_students(students):
  with open(FILE_NAME, "w", encoding="utf-8") as file:
    json.dump(students, file, indent=4)


def add_student(students):
  student_id = input("Enter student ID: ").strip()
  if any(s["id"] == student_id for s in students):
    print("Student ID already exists.")
    return
  name = input("Enter student name: ").strip()
  course = input("Enter course: ").strip()
  try:
    mark = float(input("Enter mark (0-100): "))
    if not 0 <= mark <= 100:
      print("Mark must be between 0 and 100.")
      return
  except ValueError:
    print("Please enter a valid mark.")
    return
  students.append(
      {"id": student_id, "name": name, "course": course, "mark": mark}
  )
  save_students(students)
  print("Student record saved successfully.")


def search_student(students):
  student_id = input("Enter student ID to search: ").strip()
  for student in students:
    if student["id"] == student_id:
      print("\nStudent Found:")
      print(
          f"ID: {student['id']} | Name: {student['name']} | Course:"
          f" {student['course']} | Mark: {student['mark']}"
      )
      return
  print("Student not found.")


def display_students(students):
  if not students:
    print("No student records found.")
    return
  print("\n===== STUDENT RECORDS =====")
  for student in students:
    print(
        f"ID: {student['id']} | Name: {student['name']} | Course:"
        f" {student['course']} | Mark: {student['mark']}"
    )


def main():
  students = load_students()
  while True:
    print("\n===== STUDENT DATA MANAGER =====")
    print("1. Add Student")
    print("2. Search Student")
    print("3. Display All Students")
    print("4. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
      add_student(students)
    elif choice == "2":
      search_student(students)
    elif choice == "3":
      display_students(students)
    elif choice == "4":
      print("Thank you!")
      break
    else:
      print("Invalid choice!")


if __name__ == "__main__":
  main()

# STUDENT DATA MANAGER USING FILES
def search_student(students):
  student_id = input("Enter student ID to search: ").strip()
  for student in students:
    if student["id"] == student_id:
      print("Record found:", student)
      return
  print("Student record not found.")


def update_student(students):
  student_id = input("Enter student ID to update: ").strip()
  for student in students:
    if student["id"] == student_id:
      name = input(f"New name [{student['name']}]: ").strip()
      course = input(f"New course [{student['course']}]: ").strip()
      mark_text = input(f"New mark [{student['mark']}]: ").strip()
      if name:
        student["name"] = name
      if course:
        student["course"] = course
      if mark_text:
        try:
          mark = float(mark_text)
          if not 0 <= mark <= 100:
            print("Mark must be between 0 and 100.")
            return
          student["mark"] = mark
        except ValueError:
          print("Invalid mark.")
          return
      save_students(students)
      print("Student record updated successfully.")
      return
  print("Student record not found.")


def display_students(students):
  if not students:
    print("No student records available.")
    return
  print("\nID\tNAME\t\tCOURSE\t\tMARK")
  print("-" * 55)
  for student in students:
    print(
        f"{student['id']}\t{student['name']:<15}"
        f"{student['course']:<15}{student['mark']}"
    )


def main():
  students = load_students()
  while True:
    print("\n===== STUDENT DATA MANAGER =====")
    print("1. Add Student")
    print("2. Search Student")
    print("3. Update Student")
    print("4. Display All Students")
    print("5. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
      add_student(students)
    elif choice == "2":
      search_student(students)
    elif choice == "3":
      update_student(students)
    elif choice == "4":
      display_students(students)
    elif choice == "5":
      print("Thank you!")
      break
    else:
      print("Invalid choice!")


if __name__ == "__main__":
  main()
