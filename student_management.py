"""Student Record Management System.

This script stores core student details in CSV and extra details in JSON.
It includes add, view, search, update, and delete features with validation,
logging, custom exceptions, and simple error handling.
"""

import csv
import json
import os


field_names = ["RegistrationNo", "Name", "Gender", "Age", "Course", "Score"]
additional_fields = ["Address", "Contact", "Program"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "students.csv")
JSON_FILE = os.path.join(BASE_DIR, "students.json")
LOG_FILE = os.path.join(BASE_DIR, "student_system.log")


class StudentRecordError(Exception):
    """Custom exception for student record problems."""


def write_log(message):
    """Append a simple log line to the log file."""
    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")


def load_students_csv():
    """Load student rows from the CSV file."""
    students = []

    try:
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        write_log("ERROR: CSV file not found while loading students.")
        raise StudentRecordError("Student CSV file is missing.")

    return students


def save_students_csv(students):
    """Write the full list of student rows back to the CSV file."""
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(students)


def load_student_details():
    """Load the JSON file that stores extra student details."""
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        write_log("ERROR: JSON file not found while loading student details.")
        return {}
    except json.JSONDecodeError:
        write_log("ERROR: JSON file is corrupted or invalid.")
        raise StudentRecordError("Student JSON file is invalid.")


def save_student_details(details):
    """Save extra student details into the JSON file."""
    with open(JSON_FILE, "w") as file:
        json.dump(details, file, indent=4)


def ask_non_empty(prompt_text):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def ask_integer(prompt_text, minimum=None, maximum=None):
    """Ask the user for an integer and validate optional limits."""
    while True:
        value = input(prompt_text).strip()
        try:
            number = int(value)
            if minimum is not None and number < minimum:
                print(f"Enter a value greater than or equal to {minimum}.")
                continue
            if maximum is not None and number > maximum:
                print(f"Enter a value less than or equal to {maximum}.")
                continue
            return number
        except ValueError:
            print("Please enter a valid whole number.")


def ask_choice(prompt_text, options):
    """Ask for a value from a fixed set of options."""
    valid_options = [option.lower() for option in options]

    while True:
        value = input(prompt_text).strip()
        if value.lower() in valid_options:
            for option in options:
                if option.lower() == value.lower():
                    return option
        print(f"Choose one of these options: {', '.join(options)}")


def add_student():
    """Add a new student to both CSV and JSON files."""
    try:
        registration_number = ask_non_empty("Registration number: ")
        students = load_students_csv()

        for student in students:
            if student["RegistrationNo"] == registration_number:
                raise StudentRecordError("A student with that registration number already exists.")

        name = ask_non_empty("Name: ")
        gender = ask_choice("Gender (Male/Female): ", ["Male", "Female"])
        age = ask_integer("Age: ", minimum=1)
        course = ask_non_empty("Course: ")
        score = ask_integer("Score (0-100): ", minimum=0, maximum=100)
        address = ask_non_empty("Address: ")
        contact = ask_non_empty("Contact: ")
        program = ask_non_empty("Program: ")

        new_student = {
            "RegistrationNo": registration_number,
            "Name": name,
            "Gender": gender,
            "Age": str(age),
            "Course": course,
            "Score": str(score),
        }

        students.append(new_student)
        save_students_csv(students)

        details = load_student_details()
        details[registration_number] = {
            "Address": address,
            "Contact": contact,
            "Program": program,
        }
        save_student_details(details)

        write_log(f"Added student {registration_number}")
        print("Student added successfully.")
    except StudentRecordError as error:
        write_log(f"ERROR: Add student failed - {error}")
        print(error)
    except Exception as error:
        write_log(f"ERROR: Unexpected error while adding a student - {error}")
        print(f"An unexpected error occurred: {error}")
    finally:
        print("Add student operation finished.")


def view_students():
    """Display all students in a simple table."""
    try:
        students = load_students_csv()
        details = load_student_details()

        if not students:
            print("No student records found.")
            return

        print("\nALL STUDENTS")
        print("-" * 120)
        print(f"{'Reg No':<18} {'Name':<20} {'Gender':<10} {'Age':<6} {'Course':<22} {'Score':<8} {'Program':<12}")
        print("-" * 120)

        for student in students:
            extra = details.get(student["RegistrationNo"], {})
            print(
                f"{student['RegistrationNo']:<18} {student['Name']:<20} {student['Gender']:<10} "
                f"{student['Age']:<6} {student['Course']:<22} {student['Score']:<8} {extra.get('Program', '-'):<12}"
            )

        write_log("Viewed all students")
    except Exception as error:
        write_log(f"ERROR: Unexpected error while viewing students - {error}")
        print(f"An error occurred: {error}")
    finally:
        print("View students operation finished.")


def search_student():
    """Search and display one student by registration number."""
    try:
        registration_number = ask_non_empty("Enter registration number to search: ")
        students = load_students_csv()
        student = None

        for row in students:
            if row["RegistrationNo"] == registration_number:
                student = row
                break

        if student is None:
            raise StudentRecordError(
                f"Student with registration number {registration_number} was not found."
            )

        details = load_student_details().get(registration_number, {})

        print("\nSTUDENT FOUND")
        print("-" * 40)
        for field in field_names:
            print(f"{field}: {student[field]}")
        for field in additional_fields:
            print(f"{field}: {details.get(field, 'N/A')}")

        write_log(f"Searched student {registration_number}")
    except StudentRecordError as error:
        write_log(f"ERROR: Search failed - {error}")
        print(error)
    except Exception as error:
        write_log(f"ERROR: Unexpected error while searching for a student - {error}")
        print(f"An unexpected error occurred: {error}")
    finally:
        print("Search operation finished.")


def update_student():
    """Update a student record in both CSV and JSON files."""
    try:
        registration_number = ask_non_empty("Enter registration number to update: ")
        students = load_students_csv()
        index = None
        student = None

        for position, row in enumerate(students):
            if row["RegistrationNo"] == registration_number:
                index = position
                student = row
                break

        if index is None:
            raise StudentRecordError(
                f"Student with registration number {registration_number} was not found."
            )

        assert student is not None

        details = load_student_details()
        extra_details = details.get(registration_number, {field: "" for field in additional_fields})

        print("Press Enter to keep the existing value.")

        name = input(f"Name [{student['Name']}]: ").strip() or student["Name"]
        gender_input = input(f"Gender [{student['Gender']}]: ").strip()
        gender = ask_choice("Gender (Male/Female): ", ["Male", "Female"]) if gender_input else student["Gender"]

        age_input = input(f"Age [{student['Age']}]: ").strip()
        age = student["Age"]
        if age_input:
            age = str(int(age_input))

        course = input(f"Course [{student['Course']}]: ").strip() or student["Course"]

        score_input = input(f"Score [{student['Score']}]: ").strip()
        score = student["Score"]
        if score_input:
            score_number = int(score_input)
            if score_number < 0 or score_number > 100:
                raise StudentRecordError("Score must be between 0 and 100.")
            score = str(score_number)

        address = input(f"Address [{extra_details.get('Address', '')}]: ").strip() or extra_details.get("Address", "")
        contact = input(f"Contact [{extra_details.get('Contact', '')}]: ").strip() or extra_details.get("Contact", "")
        program = input(f"Program [{extra_details.get('Program', '')}]: ").strip() or extra_details.get("Program", "")

        students[index] = {
            "RegistrationNo": registration_number,
            "Name": name,
            "Gender": gender,
            "Age": age,
            "Course": course,
            "Score": score,
        }
        save_students_csv(students)

        details[registration_number] = {
            "Address": address,
            "Contact": contact,
            "Program": program,
        }
        save_student_details(details)

        write_log(f"Updated student {registration_number}")
        print("Student record updated successfully.")
    except (ValueError, StudentRecordError) as error:
        write_log(f"ERROR: Update failed - {error}")
        print(error)
    except Exception as error:
        write_log(f"ERROR: Unexpected error while updating a student - {error}")
        print(f"An unexpected error occurred: {error}")
    finally:
        print("Update operation finished.")


def delete_student():
    """Delete a student from both CSV and JSON files."""
    try:
        registration_number = ask_non_empty("Enter registration number to delete: ")
        students = load_students_csv()
        student = None

        for row in students:
            if row["RegistrationNo"] == registration_number:
                student = row
                break

        if student is None:
            raise StudentRecordError(
                f"Student with registration number {registration_number} was not found."
            )

        confirm = ask_choice(f"Delete {student['Name']}? (yes/no): ", ["yes", "no"])
        if confirm == "no":
            print("Delete operation cancelled.")
            return

        updated_students = [row for row in students if row["RegistrationNo"] != registration_number]
        save_students_csv(updated_students)

        details = load_student_details()
        details.pop(registration_number, None)
        save_student_details(details)

        write_log(f"Deleted student {registration_number}")
        print("Student record deleted successfully.")
    except StudentRecordError as error:
        write_log(f"ERROR: Delete failed - {error}")
        print(error)
    except Exception as error:
        write_log(f"ERROR: Unexpected error while deleting a student - {error}")
        print(f"An unexpected error occurred: {error}")
    finally:
        print("Delete operation finished.")


def menu():
    """Display the menu and handle user choices."""
    while True:
        print("\nSTUDENT RECORD MANAGEMENT SYSTEM")
        print("1. Add a new student")
        print("2. View all students")
        print("3. Search for a student by registration number")
        print("4. Update student details")
        print("5. Delete a student record")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                print("Goodbye.")
                write_log("User exited the program")
                break
            else:
                print("Invalid choice. Please select a number from 1 to 6.")
        except Exception as error:
            write_log(f"ERROR: Unexpected menu error - {error}")
            print(f"A menu error occurred: {error}")


def main():
    """Program entry point."""
    write_log("Student management system started")

    try:
        menu()
    finally:
        write_log("Student management system closed")


if __name__ == "__main__":
    main()