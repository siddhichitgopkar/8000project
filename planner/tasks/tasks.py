import json
import os
from rich.console import Console
from rich.table import Table

console = Console()
tasks_file = "tasks_data.json"  # File to store task data
tasks_data = []  # List to hold tasks

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

    table = Table(title="Tasks List", show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("ID", style="bold #FC6C85")
    table.add_column("Task", style="bold #FC6C85")
    table.add_column("Status", style="bold #FC6C85")

    for i, task in enumerate(tasks_data):
        status = "Done" if task["done"] else "Pending"
        table.add_row(str(i), task["title"], status)

    console.print(table)

def add_task():
    """Add a new task."""
    load_tasks()
    title = console.input("[#FC6C85]Task title: [/#FC6C85]")
    tasks_data.append({"title": title, "done": False})
    save_tasks()
    console.print("[bold #FC6C85]Task added successfully![/bold #FC6C85]")

def modify_task():
    """Modify an existing task."""
    load_tasks()
    display_tasks()
    task_id = int(console.input("[#FC6C85]Enter task ID to modify: [/#FC6C85]"))
    if 0 <= task_id < len(tasks_data):
        title = console.input("[#FC6C85]New task title: [/#FC6C85]") or tasks_data[task_id]["title"]
        tasks_data[task_id]["title"] = title
        save_tasks()
        console.print("[bold #FC6C85]Task modified successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid task ID![/bold red]")

def mark_task_done():
    """Mark a task as done."""
    load_tasks()
    display_tasks()
    task_id = int(console.input("[#FC6C85]Enter task ID to mark as done: [/#FC6C85]"))
    if 0 <= task_id < len(tasks_data):
        tasks_data[task_id]["done"] = True
        save_tasks()
        console.print("[bold #FC6C85]Task marked as done![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid task ID![/bold red]")
