# Lab Exercise 14: Bank Account System Using OOP


class BankAccount:

  def __init__(self, account_holder, account_number, opening_balance=0):
    self.account_holder = account_holder
    self.account_number = account_number
    self.__balance = 0
    if opening_balance >= 0:
      self.__balance = opening_balance
    else:
      print("Opening balance cannot be negative.")

  def deposit(self, amount):
    if amount <= 0:
      print("Invalid deposit. Amount must be greater than zero.")
    else:
      self.__balance += amount
      print(f"Rs. {amount:.2f} deposited successfully.")

  def withdraw(self, amount):
    if amount <= 0:
      print("Invalid withdrawal. Amount must be greater than zero.")
    elif amount > self.__balance:
      print("Insufficient balance. Transaction cancelled.")
    else:
      self.__balance -= amount
      print(f"Rs. {amount:.2f} withdrawn successfully.")

  def balance_enquiry(self):
    print(f"Available balance: Rs. {self.__balance:.2f}")

  def display_account(self):
    print("\n----- ACCOUNT DETAILS -----")
    print("Account holder:", self.account_holder)
    print("Account number:", self.account_number)
    self.balance_enquiry()


def main():
  account = BankAccount("Ananya", "BA1001", 5000)
  while True:
    print("\n===== BANK ACCOUNT SYSTEM =====")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Balance Enquiry")
    print("4. Account Details")
    print("5. Exit")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
      try:
        amount = float(input("Enter deposit amount: Rs. "))
        account.deposit(amount)
      except ValueError:
        print("Please enter a valid amount.")
    elif choice == "2":
      try:
        amount = float(input("Enter withdrawal amount: Rs. "))
        account.withdraw(amount)
      except ValueError:
        print("Please enter a valid amount.")
    elif choice == "3":
      account.balance_enquiry()
    elif choice == "4":
      account.display_account()
    elif choice == "5":
      print("Thank you for using the Bank Account System.")
      break
    else:
      print("Invalid menu choice.")


if __name__ == "__main__":
  main()

# Lab Exercise 15: Library Management System Using OOP


class LibraryItem:

  def __init__(self, title, item_id):
    self.title = title
    self.item_id = item_id
    self.available = True

  def display_details(self):
    status = "Available" if self.available else "Issued"
    print(f"{self.item_id} | {self.title} | {status}")


class Book(LibraryItem):

  def __init__(self, title, item_id, author):
    super().__init__(title, item_id)
    self.author = author

  def issue_book(self):
    if self.available:
      self.available = False
      print(f'"{self.title}" issued successfully.')
    else:
      print(f'"{self.title}" is currently not available.')

  def return_book(self):
    if not self.available:
      self.available = True
      print(f'"{self.title}" returned successfully.')
    else:
      print(f'"{self.title}" was not issued.')

  def display_details(self):
    status = "Available" if self.available else "Issued"
    print(f"{self.item_id} | {self.title} | {self.author} | {status}")


class Library:

  def __init__(self):
    self.books = [
        Book("Python Basics", "B101", "John Smith"),
        Book("Data Structures", "B102", "Mary Jones"),
        Book("Object Oriented Programming", "B103", "David Lee"),
    ]

  def display_books(self):
    print("\nID    TITLE                         AUTHOR         STATUS")
    print("-" * 75)
    for book in self.books:
      book.display_details()

  def find_book(self, item_id):
    for book in self.books:
      if book.item_id.lower() == item_id.lower():
        return book
    return None


def main():
  library = Library()
  while True:
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Display Books")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
      library.display_books()
    elif choice in ("2", "3"):
      item_id = input("Enter book ID: ").strip()
      book = library.find_book(item_id)
      if book is None:
        print("Book ID not found.")
      elif choice == "2":
        book.issue_book()
      else:
        book.return_book()
    elif choice == "4":
      print("Thank you for using the Library System.")
      break
    else:
      print("Invalid menu choice.")


if __name__ == "__main__":
  main()

# Lab Exercise 16: Dice Simulator Using random Module
import random


def roll_dice(number_of_dice):
  results = []
  for _ in range(number_of_dice):
    results.append(random.randint(1, 6))
  return results


def main():
  frequency = {face: 0 for face in range(1, 7)}
  while True:
    print("\n===== DICE SIMULATOR =====")
    print("1. Roll Dice")
    print("2. Display Frequency")
    print("3. Exit")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
      try:
        count = int(input("How many dice do you want to roll? "))
        if count <= 0:
          print("Enter a number greater than zero.")
          continue
        results = roll_dice(count)
        print("Dice results:", results)
        for result in results:
          frequency[result] += 1
      except ValueError:
        print("Please enter a valid whole number.")
    elif choice == "2":
      print("\n----- FACE FREQUENCY -----")
      for face, total in frequency.items():
        print(f"Face {face}: {total} time(s)")
      print("Total dice rolled:", sum(frequency.values()))
    elif choice == "3":
      print("Thanks for playing!")
      break
    else:
      print("Invalid menu choice.")


if __name__ == "__main__":
  main()
