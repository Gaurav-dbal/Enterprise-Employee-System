"""
===========================================
Enterprise Employee Management System
Author : Gaurav Sharma
Version : 1.0
===========================================
"""

# ===========================================
# Global Variables
# ===========================================
import json
employees = []


# ===========================================
# Functions
# ===========================================

def add_employee():

    print("\n========== Add Employee ==========")

    employee_id = input("Enter Employee ID       : ")
    employee_name = input("Enter Employee Name     : ")
    employee_age = int(input("Enter Employee Age      : "))
    department = input("Enter Department        : ")
    designation = input("Enter Designation       : ")
    salary = float(input("Enter Monthly Salary    : "))

    employee = {
        "id": employee_id,
        "name": employee_name,
        "age": employee_age,
        "department": department,
        "designation": designation,
        "salary": salary
    }

    employees.append(employee)
    save_data()
    print("\nEmployee Added Successfully!")
    print(f"Total Employees : {len(employees)}")



def view_employees():

    print("DEBUG: view_employees() called")

    print("\n========== Employee List ==========")
  

    if len(employees) == 0:
        print("No Employees Found.")
        return

    for emp in employees:

      ##  print("-" * 40)
        print(f"Employee ID   : {emp['id']}")
        print(f"Name          : {emp['name']}")
        print(f"Age           : {emp['age']}")
        print(f"Department    : {emp['department']}")
        print(f"Designation   : {emp['designation']}")
        print(f"Salary        : ₹{emp['salary']:,.2f}")

    print("-" * 40)


def search_employee():
    if len(employees) == 0:
        print("No Employees Found.")
        return

    search_id = input("Enter Employee ID : ")

    for emp in employees:

        if emp["id"] == search_id:

            print("\nEmployee Found")
            print("-" * 40)
            print(f"Employee ID   : {emp['id']}")
            print(f"Name          : {emp['name']}")
            print(f"Age           : {emp['age']}")
            print(f"Department    : {emp['department']}")
            print(f"Designation   : {emp['designation']}")
            print(f"Salary        : ₹{emp['salary']:,.2f}")
            print("-" * 40)

            return

    print("\nEmployee Not Found.")

def update_employee():
    print("\n========== Update Employee ==========")

    if len(employees) == 0:
        print("No Employees Found.")
        return

    update_id = input("Enter Employee ID : ")

    for emp in employees:

        if emp["id"] == update_id:

            print("\nEmployee Found")
            print("Enter new employee details.")

            emp["name"] = input("Enter New Name        : ")
            emp["age"] = int(input("Enter New Age         : "))
            emp["department"] = input("Enter New Department  : ")
            emp["designation"] = input("Enter New Designation : ")
            emp["salary"] = float(input("Enter New Salary      : "))

            print("\nEmployee Updated Successfully.")

            return

    print("\nEmployee Not Found.")

def delete_employee():

    print("\n========== Delete Employee ==========")

    if len(employees) == 0:
        print("No Employees Found.")
        return

    delete_id = input("Enter Employee ID : ")

    for emp in employees:

        if emp["id"] == delete_id:

            employees.remove(emp)

            print("\nEmployee Deleted Successfully.")

            return

    print("\nEmployee Not Found.")


def salary_calculator():
  def salary_calculator():

    print("\n========== Salary Calculator ==========")

    if len(employees) == 0:
        print("No Employees Found.")
        return

    employee_id = input("Enter Employee ID : ")

    for emp in employees:

        if emp["id"] == employee_id:

            monthly_salary = emp["salary"]

            annual_salary = monthly_salary * 12

            bonus = annual_salary * 0.10

            total_annual_income = annual_salary + bonus

            print("\n========== Salary Details ==========")
            print(f"Employee ID       : {emp['id']}")
            print(f"Employee Name     : {emp['name']}")
            print(f"Monthly Salary    : ₹{monthly_salary:,.2f}")
            print(f"Annual Salary     : ₹{annual_salary:,.2f}")
            print(f"Annual Bonus 10%  : ₹{bonus:,.2f}")
            print(f"Total Annual Income: ₹{total_annual_income:,.2f}")

            return

    print("\nEmployee Not Found.")


def attendance_analyzer():
    print("\n========== Attendance Analyzer ==========")

    if len(employees) == 0:
        print("No Employees Found.")
        return

    employee_id = input("Enter Employee ID : ")

    for emp in employees:

        if emp["id"] == employee_id:

            working_days = int(input("Enter Total Working Days : "))
            present_days = int(input("Enter Present Days       : "))

            absent_days = working_days - present_days

            attendance_percentage = (present_days / working_days) * 100

            print("\n========== Attendance Details ==========")
            print(f"Employee ID        : {emp['id']}")
            print(f"Employee Name      : {emp['name']}")
            print(f"Working Days       : {working_days}")
            print(f"Present Days       : {present_days}")
            print(f"Absent Days        : {absent_days}")
            print(f"Attendance         : {attendance_percentage:.2f}%")

            if attendance_percentage >= 90:
                print("Status             : Excellent")
            elif attendance_percentage >= 75:
                print("Status             : Good")
            else:
                print("Status             : Needs Improvement")

            return

    print("\nEmployee Not Found.")


 
def expense_tracker():

    print("\n========== Expense Tracker ==========")

    expenses = []

    while True:

        print("\n1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Exit")

        choice = input("\nEnter your choice : ")

        if choice == "1":

            expense_name = input("Enter Expense Name : ")
            expense_amount = float(input("Enter Amount       : "))

            expense = {
                "name": expense_name,
                "amount": expense_amount
            }

            expenses.append(expense)

            print("Expense Added Successfully.")

        elif choice == "2":

            if len(expenses) == 0:
                print("No Expenses Found.")
                continue

            print("\n========== Expense List ==========")

            for expense in expenses:

                print(
                    f"{expense['name']} : "
                    f"₹{expense['amount']:,.2f}"
                )

        elif choice == "3":

            total_expense = 0

            for expense in expenses:
                total_expense += expense["amount"]

            print(
                f"\nTotal Expenses : "
                f"₹{total_expense:,.2f}"
            )

        elif choice == "4":

            print("Returning to Main Menu.")
            break

        else:

            print("Invalid Choice.")


def statistics():

    print("\n========== Employee Statistics ==========")

    if len(employees) == 0:
        print("No Employees Found.")
        return

    total_employees = len(employees)

    total_salary = 0

    for emp in employees:
        total_salary += emp["salary"]

    average_salary = total_salary / total_employees

    print(f"Total Employees : {total_employees}")
    print(f"Total Salary    : ₹{total_salary:,.2f}")
    print(f"Average Salary  : ₹{average_salary:,.2f}")


# ===========================================
# Main Program
# ===========================================
def load_data():

    global employees

    try:

        with open("employees.json", "r") as file:

            employees = json.load(file)

    except FileNotFoundError:

        employees = []

def save_data():

    with open("employees.json", "w") as file:

        json.dump(employees, file, indent=4)
load_data()

while True:

    print("\n========================================")
    print(" Enterprise Employee Management System ")
    print("========================================")

    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Salary Calculator")
    print("7. Attendance Analyzer")
    print("8. Expense Tracker")
    print("9. Statistics")
    print("10. Exit")

    choice = input("\nEnter your choice : ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_employee()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        salary_calculator()

    elif choice == "7":
        attendance_analyzer()

    elif choice == "8":
        expense_tracker()

    elif choice == "9":
        statistics()

    elif choice == "10":
        print("\nThank you for using Enterprise Employee Management System.")
        break

    else:
        print("\nInvalid Choice! Please enter a number between 1 and 10.")