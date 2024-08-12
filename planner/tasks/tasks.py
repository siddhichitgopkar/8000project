# tasks.py
import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from my_calendar import load_calendar, save_calendar, display_calendar

console = Console()

TASKS_FILE = "tasks_data.json"
DAYS_OF_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            console.print(f"[bold red]Error loading tasks: {e}[/bold red]")
    return []

def save_tasks(tasks_data):
    """Save tasks to the JSON file."""
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks_data, f)
    except IOError as e:
        console.print(f"[bold red]Error saving tasks: {e}[/bold red]")

def display_tasks():
    """Display all tasks."""
    tasks_data = load_tasks()
    if not tasks_data:
        console.print("[bold red]No tasks found. Add a new task![/bold red]")
        return

    sorted_tasks = sorted(tasks_data, key=lambda x: DAYS_OF_WEEK.index(x.get("day", "unassigned")) if x.get("day", "unassigned") in DAYS_OF_WEEK else len(DAYS_OF_WEEK))

    table = Table(title="Tasks List", show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("ID", style="bold #FC6C85")
    table.add_column("Task", style="bold #FC6C85")
    table.add_column("Day", style="bold #FC6C85")
    table.add_column("Time (min)", style="bold #FC6C85")
    table.add_column("Status", style="bold #FC6C85")
    table.add_column("Recurrence", style="bold #FC6C85")

    for i, task in enumerate(sorted_tasks):
        title = task.get("title", "Untitled")
        day = task.get("day", "Unassigned").capitalize()
        time = str(task.get("time", "N/A"))
        status = "Scheduled" if task.get("scheduled", False) else ("Done" if task.get("done") else "Not Done")
        recurrence = task.get("recurrence", "None").capitalize()
        table.add_row(str(i), title, day, time, status, recurrence)

    console.print(table)

def add_task():
    """Add a new task."""
    tasks_data = load_tasks()
    title = console.input("[#FC6C85]Task title: [/#FC6C85]")
    day = console.input("[#FC6C85]Day of the week (e.g., Monday): [/#FC6C85]").strip().lower()
    time = console.input("[#FC6C85]Time required (in minutes): [/#FC6C85]").strip()
    recurrence = console.input("[#FC6C85]Recurrence (none, daily, weekly): [/#FC6C85]").strip().lower() or "none"

    if day not in DAYS_OF_WEEK and day != "":
        console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
        return

    tasks_data.append({"title": title, "day": day, "time": int(time), "done": False, "scheduled": False, "recurrence": recurrence})
    save_tasks(tasks_data)
    console.print("[bold #FC6C85]Task added successfully![/bold #FC6C85]")

def modify_task():
    """Modify an existing task."""
    tasks_data = load_tasks()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to modify: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            title = console.input("[#FC6C85]New task title (leave empty to keep current): [/#FC6C85]") or tasks_data[task_id]["title"]
            day = console.input("[#FC6C85]New day of the week (leave empty to keep current): [/#FC6C85]").strip().lower() or tasks_data[task_id]["day"]
            time = console.input("[#FC6C85]New time required (in minutes) (leave empty to keep current): [/#FC6C85]").strip() or tasks_data[task_id]["time"]
            recurrence = console.input("[#FC6C85]New recurrence (none, daily, weekly) (leave empty to keep current): [/#FC6C85]").strip().lower() or tasks_data[task_id]["recurrence"]

            if day not in DAYS_OF_WEEK and day != "":
                console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
                return

            tasks_data[task_id].update({"title": title, "day": day, "time": int(time), "recurrence": recurrence})
            save_tasks(tasks_data)
            console.print("[bold #FC6C85]Task modified successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

def mark_task_done():
    """Mark a task as done."""
    tasks_data = load_tasks()
    calendar_data = load_calendar()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to mark as done: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            task = tasks_data.pop(task_id)
            recurrence = task.get("recurrence")

            # Mark the corresponding event in the calendar as completed
            for event in calendar_data:
                if event["title"] == task["title"] and not event.get("completed", False):
                    event["completed"] = True
                    break

            if recurrence in ["daily", "weekly"]:
                next_day = datetime.now() + (timedelta(days=1) if recurrence == "daily" else timedelta(weeks=1))
                new_task = {
                    "title": task["title"],
                    "day": next_day.strftime("%A").lower(),
                    "time": task["time"],
                    "done": False,
                    "scheduled": False,
                    "recurrence": recurrence
                }
                tasks_data.append(new_task)

            save_tasks(tasks_data)
            save_calendar(calendar_data)  # Save the updated calendar with the completed status
            console.print("[bold #FC6C85]Task marked as done successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

def delete_task():
    """Delete an existing task."""
    tasks_data = load_tasks()
    display_tasks()
    try:
        task_id = int(console.input("[#FC6C85]Enter task ID to delete: [/#FC6C85]"))
        if 0 <= task_id < len(tasks_data):
            tasks_data.pop(task_id)
            save_tasks(tasks_data)
            console.print("[bold #FC6C85]Task deleted successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid task ID.[/bold red]")

def schedule_task():
    """Schedule a task in the calendar."""
    tasks_data = load_tasks()
    calendar_data = load_calendar()
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

            if day in DAYS_OF_WEEK:
                week_start = datetime.now() - timedelta(days=datetime.now().weekday())
                task_day = week_start + timedelta(days=DAYS_OF_WEEK.index(day))

                start_time = datetime.combine(task_day, specified_time) if specified_time else task_day.replace(hour=9, minute=0)
                end_time = start_time + duration

                # Check for conflicts and adjust if necessary
                while any(event["start_time"] < end_time and start_time < event["end_time"] for event in calendar_data):
                    start_time += timedelta(minutes=30)
                    end_time = start_time + duration

                calendar_data.append({"title": title, "start_time": start_time, "end_time": end_time, "recurrence": recurrence})
                save_calendar(calendar_data)

                task["scheduled"] = True
                save_tasks(tasks_data)
                console.print(f"[bold #FC6C85]Task '{title}' scheduled successfully![/bold #FC6C85]")
            else:
                console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
        else:
            console.print("[bold red]Invalid task ID![/bold red]")
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
