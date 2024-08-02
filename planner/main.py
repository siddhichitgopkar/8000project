# Import necessary modules and functions
import calendar
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from my_calendar.calendar import display_calendar, add_event, modify_event, remove_event
from tasks.tasks import display_tasks, add_task, modify_task, mark_task_done
from notes.notes import display_notes, add_note, modify_note
from habits.habits import display_habits, add_habit, delete_habit, view_habit_info, mark_habit_done
from students.students import display_students, add_student, delete_student, mark_attendance, display_receipts

# Create a console object for rich text output
console = Console()

def display_monthly_calendar(current_date):
    # Create a calendar object for the current month
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(current_date.year, current_date.month)

    # Create a table with the month and year as the title
    table = Table(title=f"{current_date.strftime('%B %Y')}", show_header=True, header_style="bold magenta")
    # Add columns for the days of the week
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for day in days:
        table.add_column(day, style="bold #FC6C85")

    # Fill the table with the days of the month
    for week in month_days:
        week_row = []
        for day in week:
            day_text = str(day) if day != 0 else " "  # Add a space for days that are not part of the month
            week_row.append(day_text)
        table.add_row(*week_row)

    # Print the table to the console
    console.print(table)

def main():
    # Get the current date
    current_date = datetime.now()
    while True:
        # Display the calendar for the current month
        display_monthly_calendar(current_date)
        console.print("[bold #FC6C85]Menu:[/bold #FC6C85] (cal, tasks, note, habits, students, next, prev, exit)")
        choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")

        # Change the month to the next month
        if choice == "next":
            current_date = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        # Change the month to the previous month
        elif choice == "prev":
            current_date = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        # Handle calendar events
        elif choice == "cal":
            week_start = datetime.now() - timedelta(days=datetime.now().weekday())
            while True:
                display_calendar(week_start)
                console.print("[bold #FC6C85]Options:[/bold #FC6C85] (add, modify, remove, back, next, prev)")
                cal_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
                if cal_choice == "add":
                    add_event()
                elif cal_choice == "modify":
                    modify_event()
                elif cal_choice == "remove":
                    remove_event()
                elif cal_choice == "next":
                    week_start += timedelta(days=7)
                elif cal_choice == "prev":
                    week_start -= timedelta(days=7)
                elif cal_choice == "back":
                    break

        # Handle tasks
        elif choice == "tasks":
            display_tasks()
            console.print("[bold #FC6C85]Options:[/bold #FC6C85] (add, modify, done, back)")
            task_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
            if task_choice == "add":
                add_task()
            elif task_choice == "modify":
                modify_task()
            elif task_choice == "done":
                mark_task_done()

        # Handle notes
        elif choice == "note":
            display_notes()
            console.print("[bold #FC6C85]Options:[/bold #FC6C85] (add, modify, back)")
            note_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
            if note_choice == "add":
                add_note()
            elif note_choice == "modify":
                modify_note()

        # Handle habits
        elif choice == "habits":
            while True:
                display_habits()
                console.print("[bold #FC6C85]Options:[/bold #FC6C85] (add, delete, info, done, back)")
                habit_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
                if habit_choice == "add":
                    add_habit()
                elif habit_choice == "delete":
                    delete_habit()
                elif habit_choice == "info":
                    view_habit_info()
                elif habit_choice == "done":
                    mark_habit_done()
                elif habit_choice == "back":
                    break

        # Handle student management
        elif choice == "students":
            while True:
                display_students()
                console.print("[bold #FC6C85]Options:[/bold #FC6C85] (add, delete, attendance, receipts, back)")
                student_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
                if student_choice == "add":
                    add_student()
                elif student_choice == "delete":
                    delete_student()
                elif student_choice == "attendance":
                    mark_attendance()
                elif student_choice == "receipts":
                    display_receipts()
                elif student_choice == "back":
                    break

        # Exit the program
        elif choice == "exit":
            break

# Run the main function if this file is executed
if __name__ == "__main__":
    main()
