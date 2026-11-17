# Python and VS Code Setup Guide

## Windows Setup

### Step 1: Download the Python Installer via Chrome
1. Open Google Chrome.
2. Navigate to the official website: [python.org/downloads](https://www.python.org/downloads).
3. Click the yellow "Download Python" button to download the latest installer `.exe` file.
4. Once downloaded, click the file directly from Chrome's download bar (top right) or press `Ctrl + J` and click "Show in folder" to locate the file in your Downloads folder.

### Step 2: Run the Installer
1. Double-click the downloaded file (e.g., `python-3.x.x-amd64.exe`).
2. **Crucial Step:** At the bottom of the installation window, check the box that says **"Add python.exe to PATH"**. (Skipping this step will make it difficult to run Python from the Command Prompt).
3. Check "Install launcher for all users".
4. Click "Install Now".

### Step 3: Verify the Installation
1. Press `Win + R`, type `cmd`, and press Enter to open the Command Prompt.
2. Type the following command and hit Enter:
   ```bash
   python --version

# Write and Execute a Basic Python Program 
print("Hello, World!") 
print("Welcome to Python Programming.") 


#Programs Using Variables, Operators, and Input/Output 
# Input/Output and Variables
name = input("Enter your name: ")
age = int(input("Enter your age: "))

# Basic Arithmetic Operators
next_year_age = age + 1
double_age = age * 2

# Output using formatted string (f-string)
print(f"\nHello, {name}!")
print(f"You are currently {age} years old.")
print(f"Next year, you will be {next_year_age} years old.")
print(f"Twice your age is {double_age}.")
