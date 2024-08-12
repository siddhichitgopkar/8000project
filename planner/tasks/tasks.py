import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from calendar_utils import load_calendar, save_calendar, calendar_data

console = Console()
tasks_file = "tasks_data.json"  # File to store task data
tasks_data = []  # List to hold tasks
days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def load_tasks():
    """Load tasks from the JSON file."""
    global tasks_data
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as f:
            tasks_data = json.load(f)

def save_tasks():
    """Save tasks to the JSON file."""
    with open(tasks_file, 'w') as f:
        json.dump(tasks_data, f, default=str)

def display_tasks():
    """Display all tasks."""
    load_tasks()
    if not tasks_data:
        console.print("[bold red]No tasks found. Add a new task![/bold red]")
        return

    # Sort tasks by day of the week
    sorted_tasks = sorted(tasks_data, key=lambda x: days_of_week.index(x.get("day", "unassigned")) if x.get("day", "unassigned") in days_of_week else len(days_of_week))
    
    table = Table(title="Tasks List", show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("ID", style="bold #FC6C85")
    table.add_column("Task", style="bold #FC6C85")
    table.add_column("Day", style="bold #FC6C85")
    table.add_column("Time (min)", style="bold #FC6C85")
    table.add_column("Status", style="bold #FC6C85")
    table.add_column("Recurrence", style="bold #FC6C85")

    for i, task in enumerate(sorted_tasks):
        title = task.get("title", task.get("task", "Untitled"))
        day = task.get("day", "Unassigned").capitalize()
        time = str(task.get("time", "N/A"))
        status = "Scheduled" if task.get("scheduled", False) else ("Done" if task.get("done") else "Not Done")
        recurrence = task.get("recurrence", "None").capitalize()
        table.add_row(str(i), title, day, time, status, recurrence)

    console.print(table)

def add_task():
    """Add a new task."""
    load_tasks()
    title = console.input("[#FC6C85]Task title: [/#FC6C85]")
    day = console.input("[#FC6C85]Day of the week (e.g., Monday): [/#FC6C85]").strip().lower()
    time = console.input("[#FC6C85]Time required (in minutes): [/#FC6C85]").strip()
    recurrence = console.input("[#FC6C85]Recurrence (none, daily, weekly): [/#FC6C85]").strip().lower() or "none"
    if day not in days_of_week and day != "":
        console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
        return
    tasks_data.append({"title": title, "day": day, "time": int(time), "done": False, "scheduled": False, "recurrence": recurrence})
    save_tasks()
    console.print("[bold #FC6C85]Task added successfully![/bold #FC6C85]")

def modify_task():
    """Modify an existing task."""
    load_tasks()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to modify: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            title = console.input("[#FC6C85]New task title (leave empty to keep current): [/#FC6C85]") or tasks_data[task_id].get("title", tasks_data[task_id].get("task", "Untitled"))
            day = console.input("[#FC6C85]New day of the week (leave empty to keep current): [/#FC6C85]").strip().lower() or tasks_data[task_id].get("day", "unassigned")
            time = console.input("[#FC6C85]New time required (in minutes) (leave empty to keep current): [/#FC6C85]").strip() or tasks_data[task_id].get("time", "N/A")
            recurrence = console.input("[#FC6C85]New recurrence (none, daily, weekly) (leave empty to keep current): [/#FC6C85]").strip().lower() or tasks_data[task_id].get("recurrence", "none")
            if day not in days_of_week and day != "":
                console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
                return
            tasks_data[task_id]["title"] = title
            tasks_data[task_id]["day"] = day
            tasks_data[task_id]["time"] = int(time)
            tasks_data[task_id]["recurrence"] = recurrence
            save_tasks()
            console.print("[bold #FC6C85]Task modified successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

def mark_task_done():
    """Mark a task as done."""
    load_tasks()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to mark as done: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            task = tasks_data.pop(task_id)  # Remove the task from the list
            if task.get("recurrence") == "daily":
                next_day = datetime.now() + timedelta(days=1)
                day = next_day.strftime("%A").lower()
                new_task = {"title": task["title"], "day": day, "time": task["time"], "done": False, "scheduled": False, "recurrence": "daily"}
                tasks_data.append(new_task)
            elif task.get("recurrence") == "weekly":
                next_week = datetime.now() + timedelta(days=7)
                day = next_week.strftime("%A").lower()
                new_task = {"title": task["title"], "day": day, "time": task["time"], "done": False, "scheduled": False, "recurrence": "weekly"}
                tasks_data.append(new_task)
            save_tasks()
            console.print("[bold #FC6C85]Task marked as done and handled successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

def delete_task():
    """Delete an existing task."""
    load_tasks()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to delete: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            tasks_data.pop(task_id)  # Remove the task from the list
            save_tasks()
            console.print("[bold #FC6C85]Task deleted successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

def schedule_task():
    """Schedule a task in the calendar."""
    load_tasks()
    load_calendar()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to schedule: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            task = tasks_data[task_id]
            title = task["title"]
            day = task["day"]
            duration = timedelta(minutes=int(task["time"]))
            recurrence = task["recurrence"]

            specified_time = console.input("[#FC6C85]Enter specific time to schedule (e.g., 2:30 PM) or leave empty for auto-schedule: [/#FC6C85]").strip()
            if specified_time:
                try:
                    specified_time = datetime.strptime(specified_time, "%I:%M %p").time()
                except ValueError:
                    console.print("[bold red]Invalid time format! Please enter time as e.g., 2:30 PM[/bold red]")
                    return
            else:
                specified_time = None

            days_of_week = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
            if day in days_of_week:
                week_start = datetime.now() - timedelta(days=datetime.now().weekday())
                task_day = week_start + timedelta(days=days_of_week[day])

                start_time = datetime.combine(task_day, specified_time) if specified_time else task_day.replace(hour=9, minute=0)
                end_time = start_time + duration

                # Check for conflicts and adjust if necessary
                while any(event["start_time"] < end_time and start_time < event["end_time"] for event in calendar_data):
                    start_time += timedelta(minutes=30)
                    end_time = start_time + duration

                # Add the event to the calendar
                calendar_data.append({"title": title, "start_time": start_time, "end_time": end_time, "recurrence": recurrence})
                save_calendar()

                tasks_data[task_id]["scheduled"] = True
                save_tasks()
                console.print(f"[bold #FC6C85]Task '{title}' scheduled successfully![/bold #FC6C85]")
            else:
                console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
        else:
            console.print("[bold red]Invalid task ID! Please enter a valid task ID.[/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

if __name__ == "__main__":
    while True:
        console.print("[bold #FC6C85]Options:[/bold #FC6C85] (display, add, modify, done, delete, schedule, exit)")
        choice = console.input("[#FC6C85]Enter your choice: [/#FC6C85]").strip().lower()
        if choice == "display":
            display_tasks()
        elif choice == "add":
            add_task()
        elif choice == "modify":
            modify_task()
        elif choice == "done":
            mark_task_done()
        elif choice == "delete":
            delete_task()
        elif choice == "schedule":
            schedule_task()
        elif choice == "exit":
            break
        else:
            console.print("[bold red]Invalid choice! Please choose a valid option.[/bold red]")
