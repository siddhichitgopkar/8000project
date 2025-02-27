import os
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
import subprocess

console = Console()

students_file = "students_data.json"  # File to store student data
attendance_file = "attendance_data.json"  # File to store attendance data

students_data = {}  # Dictionary to hold student information
attendance_data = {}  # Dictionary to hold attendance information

def load_students():
    global students_data
    if os.path.exists(students_file):
        with open(students_file, 'r') as f:
            students_data = json.load(f)
        # Ensure all students have the cost_per_class key
        for student in students_data.values():
            if 'cost_per_class' not in student:
                student['cost_per_class'] = 0.0
    else:
        students_data = {}

def save_students():
    with open(students_file, 'w') as f:
        json.dump(students_data, f, default=str)

def load_attendance():
    global attendance_data
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            attendance_data = json.load(f)
    else:
        attendance_data = {}

def save_attendance():
    with open(attendance_file, 'w') as f:
        json.dump(attendance_data, f, default=str)

def display_students():
    load_students()
    if not students_data:
        console.print("[bold red]No students found. Add a new student![/bold red]")
        return

    table = Table(title="Students List", show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("ID", style="bold #FC6C85")
    table.add_column("Name", style="bold #FC6C85")
    table.add_column("Cost per Class", style="bold #FC6C85")

    for student_id, student in students_data.items():
        table.add_row(str(student_id), student["name"], f"${student['cost_per_class']}")

    console.print(table)

def add_student():
    load_students()
    name = console.input("[#FC6C85]Student name: [/#FC6C85]")
    cost_per_class = float(console.input("[#FC6C85]Cost per class: [/#FC6C85]"))
    student_id = max([int(k) for k in students_data.keys()], default=0) + 1  # Increment the highest ID
    students_data[str(student_id)] = {"name": name, "cost_per_class": cost_per_class, "sessions": 0}
    save_students()
    console.print("[bold #FC6C85]Student added successfully![/bold #FC6C85]")

def delete_student():
    load_students()
    if not students_data:
        console.print("[bold red]No students to delete![/bold red]")
        return

    display_students()
    try:
        student_id = int(console.input("[#FC6C85]Enter student ID to delete: [/#FC6C85]"))
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid numeric student ID.[/bold red]")
        return

    if str(student_id) in students_data:
        del students_data[str(student_id)]
        if str(student_id) in attendance_data:
            del attendance_data[str(student_id)]
        save_students()
        save_attendance()
        console.print("[bold #FC6C85]Student deleted successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid student ID![/bold red]")

def mark_attendance():
    load_students()
    load_attendance()
    if not students_data:
        console.print("[bold red]No students to mark attendance for![/bold red]")
        return

    display_students()
    try:
        student_id = int(console.input("[#FC6C85]Enter student ID to mark attendance: [/#FC6C85]"))
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid numeric student ID.[/bold red]")
        return

    if str(student_id) in students_data:
        date = datetime.now().strftime("%Y-%m-%d")
        if str(student_id) not in attendance_data:
            attendance_data[str(student_id)] = []
        attendance_data[str(student_id)].append(date)
        students_data[str(student_id)]["sessions"] += 1
        save_attendance()
        save_students()
        console.print("[bold #FC6C85]Attendance marked for today![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid student ID![/bold red]")

def generate_receipt(student_id):
    load_students()
    load_attendance()
    if str(student_id) in students_data and str(student_id) in attendance_data:
        student = students_data[str(student_id)]
        attendance_dates = attendance_data[str(student_id)]
        month = datetime.now().strftime("%B")
        year = datetime.now().year
        cost_per_class = student["cost_per_class"]
        total_cost = student["sessions"] * cost_per_class

        receipt_content = f"{student['name']} {month} {year}\n"
        receipt_content += "------------------------------------------\n"
        receipt_content += "Classes Attended:\n"
        for date in attendance_dates:
            receipt_content += f"- {date}\n"
        receipt_content += "\n"
        receipt_content += f"Number of Classes: {student['sessions']}\n"
        receipt_content += f"Cost per Class: ${cost_per_class}\n"
        receipt_content += f"Total Due: ${total_cost}\n"

        receipt_file = f"receipt_{student_id}_{month}_{year}.txt"
        with open(receipt_file, 'w') as f:
            f.write(receipt_content)

        console.print(f"[bold #FC6C85]Receipt generated: {receipt_file}[/bold #FC6C85]")

        # Open the receipt file with the default text editor
        try:
            if os.name == 'nt':  # Windows
                os.startfile(receipt_file)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.call(['open', receipt_file])
            else:
                subprocess.call(['xdg-open', receipt_file])
        except Exception as e:
            console.print(f"[bold red]Failed to open the receipt file: {e}[/bold red]")
    else:
        console.print("[bold red]Invalid student ID or no attendance records found![/bold red]")

def display_receipts():
    load_students()
    display_students()
    try:
        student_id = int(console.input("[#FC6C85]Enter student ID to generate receipt: [/#FC6C85]"))
        generate_receipt(student_id)
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid numeric student ID.[/bold red]")
