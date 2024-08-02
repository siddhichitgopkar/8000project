import json
import os
from rich.console import Console
from rich.table import Table

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

    for i, task in enumerate(sorted_tasks):
        title = task.get("title", task.get("task", "Untitled"))
        day = task.get("day", "Unassigned").capitalize()
        table.add_row(str(i), title, day)

    console.print(table)

def add_task():
    """Add a new task."""
    load_tasks()
    title = console.input("[#FC6C85]Task title: [/#FC6C85]")
    day = console.input("[#FC6C85]Day of the week (e.g., Monday): [/#FC6C85]").strip().lower()
    tasks_data.append({"title": title, "day": day, "done": False})
    save_tasks()
    console.print("[bold #FC6C85]Task added successfully![/bold #FC6C85]")

def modify_task():
    """Modify an existing task."""
    load_tasks()
    display_tasks()
    task_id = int(console.input("[#FC6C85]Enter task ID to modify: [/#FC6C85]"))
    if 0 <= task_id < len(tasks_data):
        title = console.input("[#FC6C85]New task title (leave empty to keep current): [/#FC6C85]") or tasks_data[task_id].get("title", tasks_data[task_id].get("task", "Untitled"))
        day = console.input("[#FC6C85]New day of the week (leave empty to keep current): [/#FC6C85]").strip().lower() or tasks_data[task_id].get("day", "unassigned")
        tasks_data[task_id]["title"] = title
        tasks_data[task_id]["day"] = day
        save_tasks()
        console.print("[bold #FC6C85]Task modified successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid task ID![/bold red]")

def mark_task_done():
    """Mark a task as done and remove it."""
    load_tasks()
    display_tasks()
    task_id = int(console.input("[#FC6C85]Enter task ID to mark as done: [/#FC6C85]"))
    if 0 <= task_id < len(tasks_data):
        tasks_data.pop(task_id)  # Remove the task from the list
        save_tasks()
        console.print("[bold #FC6C85]Task marked as done and removed![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid task ID![/bold red]")

def delete_task():
    """Delete an existing task."""
    load_tasks()
    display_tasks()
    task_id = int(console.input("[#FC6C85]Enter task ID to delete: [/#FC6C85]"))
    if 0 <= task_id < len(tasks_data):
        tasks_data.pop(task_id)  # Remove the task from the list
        save_tasks()
        console.print("[bold #FC6C85]Task deleted successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid task ID![/bold red]")
