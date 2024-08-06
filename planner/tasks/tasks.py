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
    table.add_column("Time (min)", style="bold #FC6C85")
    table.add_column("Status", style="bold #FC6C85")

    for i, task in enumerate(sorted_tasks):
        title = task.get("title", task.get("task", "Untitled"))
        day = task.get("day", "Unassigned").capitalize()
        time = str(task.get("time", "N/A"))
        status = "Done" if task.get("done") else "Pending"
        table.add_row(str(i), title, day, time, status)

    console.print(table)

def add_task():
    """Add a new task."""
    load_tasks()
    title = console.input("[#FC6C85]Task title: [/#FC6C85]")
    day = console.input("[#FC6C85]Day of the week (e.g., Monday): [/#FC6C85]").strip().lower()
    time = console.input("[#FC6C85]Time required (in minutes): [/#FC6C85]").strip()
    if day not in days_of_week and day != "":
        console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
        return
    tasks_data.append({"title": title, "day": day, "time": time, "done": False})
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
        time = console.input("[#FC6C85]New time required (in minutes) (leave empty to keep current): [/#FC6C85]").strip() or tasks_data[task_id].get("time", "N/A")
        if day not in days_of_week and day != "":
            console.print("[bold red]Invalid day! Please enter a valid day of the week.[/bold red]")
            return
        tasks_data[task_id]["title"] = title
        tasks_data[task_id]["day"] = day
        tasks_data[task_id]["time"] = time
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

if __name__ == "__main__":
    # Example usage
    while True:
        console.print("[bold #FC6C85]Options:[/bold #FC6C85] (display, add, modify, done, delete, exit)")
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
        elif choice == "exit":
            break
        else:
            console.print("[bold red]Invalid choice! Please choose a valid option.[/bold red]")
