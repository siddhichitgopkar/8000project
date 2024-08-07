import calendar
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from my_calendar.my_calendar import display_calendar, add_event, modify_event, remove_event
from tasks.tasks import display_tasks, add_task, modify_task, mark_task_done, delete_task, schedule_task
from notes.notes import display_folders, display_notes_tree, new_folder, new_note, delete_note, delete_folder
from habits.habits import display_habits, add_habit, delete_habit, mark_habit_done
from students.students import display_students, add_student, delete_student, mark_attendance, display_receipts

console = Console()

def display_monthly_calendar(current_date):
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(current_date.year, current_date.month)

    table = Table(title=f"{current_date.strftime('%B %Y')}", show_header=True, header_style="bold magenta")
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for day in days:
        table.add_column(day, style="bold #FC6C85")

    for week in month_days:
        week_row = []
        for day in week:
            day_text = str(day) if day != 0 else " "
            week_row.append(day_text)
        table.add_row(*week_row)

    console.print(table)

def main():
    current_date = datetime.now()
    while True:
        display_monthly_calendar(current_date)
        console.print("[bold #FC6C85]Menu:[/bold #FC6C85] (cal, tasks, notes, habits, students, next, prev, exit)")
        choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")

        if choice == "next":
            current_date = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        elif choice == "prev":
            current_date = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
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
        elif choice == "tasks":
            while True:
                display_tasks()
                console.print("[bold #FC6C85]Options:[/bold #FC6C85] (add, modify, done, delete, schedule, back)")
                task_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
                if task_choice == "add":
                    add_task()
                elif task_choice == "modify":
                    modify_task()
                elif task_choice == "done":
                    mark_task_done()
                elif task_choice == "delete":
                    delete_task()
                elif task_choice == "schedule":
                    schedule_task()
                elif task_choice == "back":
                    break
        elif choice == "notes":
            while True:
                console.print("[bold #FC6C85]Options:[/bold #FC6C85] (newfolder, newnote, deletefolder, deletenote, show, back)")
                note_choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]")
                if note_choice == "newfolder":
                    new_folder()
                elif note_choice == "newnote":
                    new_note()
                elif note_choice == "deletefolder":
                    delete_folder()
                elif note_choice == "deletenote":
                    delete_note()
                elif note_choice == "show":
                    display_notes_tree()
                elif note_choice == "back":
                    break
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
        elif choice == "exit":
            break

if __name__ == "__main__":
    main()
